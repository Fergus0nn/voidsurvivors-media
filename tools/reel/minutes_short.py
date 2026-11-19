"""'Minute 1 vs minute 20' style short: hard cuts through a run, big in-game clock on top, Kai at the bottom.

Usage: python3 minutes_short.py spec.json out_video_no_audio.mp4
spec.json:
{
 "shots": [{"src": "/root/build/rec/hra.mp4", "ss": 562.0, "dur": 1.6, "clock": "19:49", "label": "LAST MINUTE"}, ...],
 "end_text": [["WHICH MINUTE", "#ffffff"], ["ENDS YOU?", "#ff3b4f"]],   # top text on the last shot (optional)
 "end_at": 12.1,     # optional: absolute time when end_text replaces the last shot's top text
 # per shot instead of "clock": "counter": [from, to] (+ "suffix": "×", "color") or "big": "SOLAR FLARE" (+ "color");
 # optional "bar": fraction or [from, to] for the progress bar under the title; "cx": crop x (0–576, default 288 = centre)
 "kai": [{"t0": 0.1, "t1": 1.5, "expr": "smirk", "text": "This is the last minute."}, ...]
}
Layout (1080x1920): blurred gameplay background, square gameplay zoom (centre 704x704 of the 1280x720 recording) at y=470,
clock + minute bar in the top area (below TikTok's top UI), Kai bottom-left (kai_overlay.py). White flash + zoom punch on every cut.
Audio is added afterwards with clean_audio.py (never the recording's own audio).
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
FG_Y = 470
FONT = "/root/build/proj/assets/fonts/ChakraPetch-SemiBold.ttf"
DEV = "/root/build/dev"


def run(cmd):
    subprocess.run(cmd, check=True)


def clock_color(minute):
    """cyan (calm) -> yellow -> orange -> red (death) by game minute."""
    stops = [(0, (90, 220, 255)), (6, (120, 255, 170)), (10, (255, 220, 70)), (14, (255, 140, 40)), (18, (255, 59, 79))]
    for (m0, c0), (m1, c1) in zip(stops, stops[1:]):
        if minute <= m1:
            k = max(0.0, (minute - m0) / (m1 - m0))
            return tuple(int(a + (b - a) * k) for a, b in zip(c0, c1))
    return stops[-1][1]


def text_center(d, y, txt, font, fill, stroke=8):
    tw = d.textlength(txt, font=font)
    d.text(((W - tw) / 2, y), txt, font=font, fill=fill, stroke_width=stroke, stroke_fill=(8, 4, 16, 255))


def main(spec_p, out):
    sp = json.load(open(spec_p, encoding="utf-8"))
    shots = sp["shots"]
    work = os.path.splitext(out)[0] + "_work"
    os.makedirs(work, exist_ok=True)
    # 1) base segments: blurred bg + square zoom fg with a punch-in at the start of every shot
    segs = []
    masks = sp.get("masks", [])   # [[x, y, w, h], ...] in source pixels – blurred in every shot (e.g. untranslated HUD text)
    for i, s in enumerate(shots):
        p = f"{work}/seg{i:02d}.mp4"
        mk, src_lbl = "", "[b]"
        for j, (mx, my, mw, mh) in enumerate(masks):
            mk += (f"{src_lbl}split[mb{j}][mc{j}];[mc{j}]crop={mw}:{mh}:{mx}:{my},boxblur=7:2[mm{j}];"
                   f"[mb{j}][mm{j}]overlay={mx}:{my}[mo{j}];")
            src_lbl = f"[mo{j}]"
        fc = ("[0:v]fps=30,split[a][b];"
              "[a]scale=-2:1920,crop=1080:1920,boxblur=22:2,eq=brightness=-0.30:saturation=1.15[bg];" + mk +
              src_lbl + "crop=704:704:" + str(s.get("cx", 288)) + ":4,scale=w='1080*(1+0.07*max(0,1-t/0.28))':h=-2:eval=frame,"
              "crop=1080:1080[fg];"
              f"[bg][fg]overlay=0:{FG_Y}[v]")
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(s["ss"]), "-t", str(s["dur"]), "-i", s["src"],
             "-filter_complex", fc, "-map", "[v]", "-an", "-r", "30", "-c:v", "libx264", "-preset", "veryfast",
             "-crf", "16", "-pix_fmt", "yuv420p", p])
        segs.append(p)
    lst = f"{work}/list.txt"
    open(lst, "w").write("".join(f"file '{p}'\n" for p in segs))
    base = f"{work}/base.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", base])
    # 2) top overlay frames: label, ticking clock, minute bar, flash on cuts
    starts, t = [], 0.0
    for s in shots:
        starts.append(t)
        t += s["dur"]
    dur = t
    big = ImageFont.truetype(FONT, 150)
    small = ImageFont.truetype(FONT, 50)
    endf = ImageFont.truetype(FONT, 96)
    odir = f"{work}/ov"
    os.makedirs(odir, exist_ok=True)
    nfr = int(round(dur * FPS))
    for fi in range(nfr):
        tt = fi / FPS
        k = max(i for i, st in enumerate(starts) if st <= tt + 1e-6)
        s, el = shots[k], tt - starts[k]
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        frac = min(1.0, el / max(1e-6, s["dur"]))
        bar = None
        if "clock" in s:                      # ticking in-game clock
            mm, ss = (int(x) for x in s["clock"].split(":"))
            sec = mm * 60 + ss + int(el)
            col = clock_color(sec / 60.0) + (255,)
            main_txt = f"{sec // 60:02d}:{sec % 60:02d}"
            bar = sec / 1200.0
        elif "counter" in s:                  # ticking number, e.g. combo [32318, 32399]
            c0, c1 = s["counter"]
            val = int(round(c0 + (c1 - c0) * frac))
            col = tuple(int(x) for x in bytes.fromhex(s.get("color", "#ff4070")[1:])) + (255,)
            main_txt = f"{val:,}{s.get('suffix', '')}"
        else:                                 # plain big title, e.g. "SOLAR FLARE"
            col = tuple(int(x) for x in bytes.fromhex(s.get("color", "#ffffff")[1:])) + (255,)
            main_txt = s.get("big", "")
        if "bar" in s:
            b = s["bar"]
            bar = (b[0] + (b[1] - b[0]) * frac) if isinstance(b, list) else b
        last = k == len(shots) - 1 and sp.get("end_text") and tt >= sp.get("end_at", starts[k])
        if last:
            y = 170
            for txt, c in sp["end_text"]:
                text_center(d, y, txt, endf, c)
                y += 105
        else:
            if s.get("label"):
                text_center(d, 150, s["label"], small, (235, 235, 245, 255), 6)
            fbig = big
            while d.textlength(main_txt, font=fbig) > 980 and fbig.size > 60:
                fbig = ImageFont.truetype(FONT, fbig.size - 8)
            text_center(d, 205 + (150 - fbig.size) // 2, main_txt, fbig, col, 10)
        # progress bar (run time, combo progress or step k/n)
        if bar is not None:
            x0, x1, yb = 140, W - 140, 425
            d.rounded_rectangle([x0, yb, x1, yb + 10], 5, fill=(255, 255, 255, 60))
            fx = x0 + (x1 - x0) * max(0.0, min(1.0, bar))
            d.rounded_rectangle([x0, yb, fx, yb + 10], 5, fill=col)
            d.ellipse([fx - 11, yb - 6, fx + 11, yb + 16], fill=(255, 255, 255, 255))
        # flash right after every cut (not at t=0 so the first frame is clean gameplay)
        if k > 0 and el < 3 / FPS:
            a = int(150 * (1 - el / (3 / FPS)))
            im = Image.alpha_composite(im, Image.new("RGBA", (W, H), (255, 255, 255, a)))
        im.save(f"{odir}/{fi:04d}.png")
    # 3) Kai layer
    kj = f"{work}/kai.json"
    json.dump(sp.get("kai", []), open(kj, "w"))
    kdir = f"{work}/kai"
    run(["python3", f"{DEV}/kai_overlay.py", kj, kdir, str(dur)])
    # 4) compose (no audio; clean_audio.py adds the sound)
    run(["ffmpeg", "-v", "error", "-y", "-i", base, "-framerate", "30", "-i", f"{odir}/%04d.png",
         "-framerate", "30", "-i", f"{kdir}/%04d.png", "-f", "lavfi", "-t", f"{dur:.3f}", "-i", "anullsrc=r=48000:cl=stereo",
         "-filter_complex", "[0:v][1:v]overlay=0:0[a];[a][2:v]overlay=0:0,format=yuv420p[v]",
         "-map", "[v]", "-map", "3:a", "-t", f"{dur:.3f}", "-r", "30", "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "18", "-c:a", "aac", "-movflags", "+faststart", out])
    print(json.dumps({"out": out, "dur": round(dur, 3), "cuts": [round(x, 2) for x in starts]}))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
