"""Rebuild a reel's soundtrack WITHOUT the recorded audio (recordings can contain Spotify/Discord etc.).

New audio = game music bed + clean game SFX accents at key moments + a light layer of hit/death sounds
during action shots. The video stream is copied untouched.

Usage: python clean_audio.py plan.json      (FFMPEG env var = path to ffmpeg if it is not on PATH)
plan.json:
{
  "video": "v/reel03_three_bosses.mp4", "out": "v/reel03_three_bosses_clean.mp4",
  "sfx_dir": "assets/audio/sfx", "music": "assets/audio/music/boss.ogg", "music_start": 0.0,
  "bed_lufs": -16, "duck_db": 4, "target": -14,
  "accents": [[t, "boss_prichod", gain_db, max_len_s], ...],
  "action": [[t0, t1], ...], "action_db": -13, "seed": 7
}
"""
import json, os, random, re, subprocess, sys
import numpy as np

FF = os.environ.get("FFMPEG", "ffmpeg")
SR = 48000


def dec(path):
    raw = subprocess.run([FF, "-v", "error", "-i", path, "-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).astype(np.float64)


def duration(path):
    out = subprocess.run([FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-select_streams", "v:0",
                          "-show_entries", "stream=duration", "-of", "csv=p=0", path],
                         check=True, capture_output=True, text=True).stdout
    return float(out.strip())


def write_wav(path, x):
    subprocess.run([FF, "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", path],
                   input=x.astype(np.float32).tobytes(), check=True)


def lufs(path):
    err = subprocess.run([FF, "-hide_banner", "-nostats", "-i", path, "-map", "0:a", "-af", "ebur128=peak=true",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    s = err[err.rfind("Summary"):]
    return float(re.search(r"I:\s+(-?[\d.]+) LUFS", s).group(1))


def db(x):
    return 10 ** (x / 20)


def place(bus, clip, t, gain=1.0, pan=0.0, max_len=None, fade=0.5):
    clip = clip.copy()
    if max_len:
        n = int(max_len * SR)
        if len(clip) > n:
            clip = clip[:n]
            f = min(int(fade * SR), n)
            clip[-f:] *= np.linspace(1, 0, f)[:, None]
    clip[:, 0] *= gain * min(1, 1 - pan)
    clip[:, 1] *= gain * min(1, 1 + pan)
    i = int(round(t * SR))
    if i >= len(bus):
        return
    j = min(len(bus), i + len(clip))
    bus[i:j] += clip[: j - i]


def main():
    arg = sys.argv[1]
    plan = json.load(open(arg, encoding="utf-8")) if arg.endswith(".json") else json.loads(arg)
    work = plan.get("work", os.path.splitext(plan["out"])[0] + "_tmp")
    os.makedirs(work, exist_ok=True)
    dur = duration(plan["video"])
    n = int(round(dur * SR))
    sfx_cache = {}

    def sfx(name):
        if name not in sfx_cache:
            sfx_cache[name] = dec(os.path.join(plan["sfx_dir"], name + ".ogg"))
        return sfx_cache[name]

    # 1) music bed (looped from music_start), loudness-matched
    m = dec(plan["music"])
    off = int(round(plan.get("music_start", 0.0) * SR)) % len(m)
    bed = np.tile(m, (int(np.ceil((off + n) / len(m))) + 1, 1))[off:off + n]
    write_wav(f"{work}/bed.wav", bed)
    bed *= db(plan.get("bed_lufs", -16) - lufs(f"{work}/bed.wav"))
    t = np.arange(n) / SR
    bed *= (np.clip(t / 0.05, 0, 1) * np.clip((dur - t) / plan.get("fade_out", 1.8), 0, 1))[:, None]

    # 2) accents
    acc = np.zeros((n, 2))
    for a in plan.get("accents", []):
        at, name, gdb = a[0], a[1], a[2]
        max_len = a[3] if len(a) > 3 else None
        place(acc, sfx(name), at, db(gdb), 0.0, max_len, fade=min(0.6, (max_len or 1) * 0.4))

    # 3) light action layer: enemy hits + deaths, random timing / pan, only inside action windows
    rnd = random.Random(plan.get("seed", 7))
    act = np.zeros((n, 2))
    hits = [f"zasah_{i}" for i in range(4)]
    deaths = [f"smrt_{i}" for i in range(3)]
    for t0, t1 in plan.get("action", []):
        for pool, rate, glo, ghi, ml in ((hits, 5.0, -4, 0, None), (deaths, 2.2, -6, -1, 0.9)):
            tt = t0 + rnd.expovariate(rate)
            while tt < t1:
                place(act, sfx(rnd.choice(pool)), tt, db(rnd.uniform(glo, ghi)), rnd.uniform(-0.35, 0.35), ml, 0.3)
                tt += rnd.expovariate(rate)
    act *= db(plan.get("action_db", -13))

    # 4) duck the bed a little while accents play (fast attack, slow release)
    env = np.sqrt(np.convolve((acc ** 2).mean(1), np.ones(int(0.03 * SR)) / int(0.03 * SR), mode="same"))
    k = np.clip((20 * np.log10(env + 1e-9) + 40) / 15, 0, 1)
    a_c, r_c = np.exp(-1 / (0.015 * SR)), np.exp(-1 / (0.5 * SR))
    s = np.empty_like(k)
    p = 0.0
    for i, v in enumerate(k):
        p = a_c * p + (1 - a_c) * v if v > p else r_c * p + (1 - r_c) * v
        s[i] = p
    bed *= db(-plan.get("duck_db", 4) * s)[:, None]

    mix = bed + acc + act
    write_wav(f"{work}/mix.wav", mix)
    gain = plan.get("target", -14.0) - lufs(f"{work}/mix.wav")
    subprocess.run([FF, "-v", "error", "-y", "-i", f"{work}/mix.wav", "-af",
                    f"volume={gain:.2f}dB,alimiter=limit=0.80:attack=3:release=60:level=disabled",
                    "-ar", str(SR), f"{work}/final.wav"], check=True)
    subprocess.run([FF, "-v", "error", "-y", "-i", plan["video"], "-i", f"{work}/final.wav", "-map", "0:v:0",
                    "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", str(SR),
                    "-movflags", "+faststart", plan["out"]], check=True)
    print(json.dumps({"out": plan["out"], "dur": round(dur, 3), "final_lufs": lufs(plan["out"])}))


if __name__ == "__main__":
    main()
