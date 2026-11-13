"""Add a game-music bed under a finished reel (video stream is copied untouched).

Usage: python add_music.py settings.json   (FFMPEG env var = path to ffmpeg.exe if not on PATH)
settings.json example (reel03):
{"video": "v/reel03_three_bosses.mp4", "music": "assets/audio/music/boss.ogg", "music_start": 44.632,
 "bed_lufs": -16, "orig_lufs": -20.5, "out": "v/reel03_three_bosses_music.mp4", "work": "tmp_mix"}
Optional: "duck_db": 8, "duck_thr_db": -32 (bed dips while game audio is loud), "fade_out": 1.8, "target": -14
"""
import json, os, subprocess, sys, re
import numpy as np
FF = os.environ.get("FFMPEG", "ffmpeg"); SR = 48000
def run(cmd): return subprocess.run(cmd, check=True, capture_output=True, text=True)
def dec(path):  # -> float32 [n,2]
    out = subprocess.run([FF, "-v", "error", "-i", path, "-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(out, dtype=np.float32).reshape(-1, 2).astype(np.float64)
def lufs(path):
    e = subprocess.run([FF, "-hide_banner", "-nostats", "-i", path, "-map", "0:a", "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    s = e[e.rfind("Summary"):]
    return float(re.search(r"I:\s+(-?[\d.]+) LUFS", s).group(1)), float(re.search(r"Peak:\s+(-?[\d.inf]+) dBFS", s).group(1))
def wav(path, x):
    subprocess.run([FF, "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", path],
                   input=x.astype(np.float32).tobytes(), check=True)
def db(x): return 10 ** (x / 20)

arg = sys.argv[1]
cfg = json.load(open(arg, encoding="utf-8")) if arg.endswith(".json") else json.loads(arg)
os.makedirs(cfg["work"], exist_ok=True)
video, music, out, work = cfg["video"], cfg["music"], cfg["out"], cfg["work"]
orig = dec(video); n = len(orig); dur = n / SR
m = dec(music)
off = int(round(cfg["music_start"] * SR)) % len(m)
bed = np.tile(m, (int(np.ceil((off + n) / len(m))) + 1, 1))[off:off + n]
# loudness-match: bed and original measured separately
wav(f"{work}/bed.wav", bed); wav(f"{work}/orig.wav", orig)
Lb, _ = lufs(f"{work}/bed.wav"); Lo, _ = lufs(f"{work}/orig.wav")
bed *= db(cfg["bed_lufs"] - Lb)
orig *= db(cfg["orig_lufs"] - Lo)
t = np.arange(n) / SR
# fades on the bed
fi, fo = cfg.get("fade_in", 0.08), cfg.get("fade_out", 1.8)
g = np.clip(t / fi, 0, 1) * np.clip((dur - t) / fo, 0, 1)
# optional ducking of the bed while the original is loud (envelope follower)
if cfg.get("duck_db", 0) > 0:
    env = np.sqrt(np.convolve(orig.mean(1) ** 2, np.ones(int(0.05 * SR)) / int(0.05 * SR), mode="same"))
    thr = db(cfg.get("duck_thr_db", -30))
    k = np.clip((20 * np.log10(env + 1e-9) - 20 * np.log10(thr)) / 10.0, 0, 1)   # 0..1 over 10 dB above thr
    # smooth: fast attack, slow release
    a, r = np.exp(-1 / (0.02 * SR)), np.exp(-1 / (0.45 * SR)); s = np.empty_like(k); p = 0.0
    for i, v in enumerate(k):
        p = a * p + (1 - a) * v if v > p else r * p + (1 - r) * v; s[i] = p
    g = g * db(-cfg["duck_db"] * s)
mix = orig + bed * g[:, None]
wav(f"{work}/mix.wav", mix)
L, P = lufs(f"{work}/mix.wav")
gain = cfg.get("target", -14.0) - L
run([FF, "-v", "error", "-y", "-i", f"{work}/mix.wav", "-af", f"volume={gain:.2f}dB,alimiter=limit=0.80:attack=3:release=60:level=disabled",
     "-ar", str(SR), f"{work}/final.wav"])
run([FF, "-v", "error", "-y", "-i", video, "-i", f"{work}/final.wav", "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
     "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-movflags", "+faststart", out])
Lf, Pf = lufs(out)
print(json.dumps({"dur": round(dur, 3), "bed_src_lufs": Lb, "orig_src_lufs": Lo, "mix_lufs_before": L, "final_lufs": Lf, "final_peak_dbfs": Pf}))
