"""Kai's spoken lines (voiceover) for reels – offline text-to-speech (Kokoro, Apache-2.0).

Usage:  python kai_voice.py lines.json out_dir
lines.json: {"voice": "am_puck", "speed": 1.08, "lines": [[0.15, "Yep. That's me in there."], [2.2, "..."]]}
Writes out_dir/line_00.wav ... and out_dir/voice.json = [[t, wav_path], ...] for clean_audio.py ("voice": ...).
Model files (download once from github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0):
  KOKORO_MODEL  = path to kokoro-v1.0.onnx   (default /root/tts_models/kokoro-v1.0.onnx)
  KOKORO_VOICES = path to voices-v1.0.bin    (default /root/tts_models/voices-v1.0.bin)
Rules: Kai never mentions AI; no "play / download / demo / free" lines (the game is not public yet).
"""
import json, os, sys
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

MODEL = os.environ.get("KOKORO_MODEL", "/root/tts_models/kokoro-v1.0.onnx")
VOICES = os.environ.get("KOKORO_VOICES", "/root/tts_models/voices-v1.0.bin")


def trim(x, sr, thr=0.01, pad=0.03):
    """Cut leading/trailing silence so the line starts exactly at its time."""
    idx = np.where(np.abs(x) > thr)[0]
    if len(idx) == 0:
        return x
    a = max(0, idx[0] - int(pad * sr))
    b = min(len(x), idx[-1] + int(pad * sr))
    return x[a:b]


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    k = Kokoro(MODEL, VOICES)
    voice, speed = spec.get("voice", "am_puck"), spec.get("speed", 1.05)
    res = []
    for i, line in enumerate(spec["lines"]):
        t, text = line[0], line[1]
        v = line[2] if len(line) > 2 else voice
        samples, sr = k.create(text, voice=v, speed=speed, lang="en-us")
        samples = trim(np.asarray(samples, dtype=np.float32), sr)
        path = os.path.join(out, f"line_{i:02d}.wav")
        sf.write(path, samples, sr)
        res.append([t, os.path.abspath(path)])
        print(f"{t:6.2f}s  {len(samples) / sr:4.2f}s  {text}")
    json.dump(res, open(os.path.join(out, "voice.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
