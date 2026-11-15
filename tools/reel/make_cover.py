"""Thumbnail / cover (1080x1920 JPG) for a reel: strongest frame(s) + 2–3 big words + VOID SURVIVORS tag.

Usage: python3 make_cover.py cover.json
cover.json:
{"out": "v/2026-11-16_REEL05_minute-1-vs-20_cover.jpg",
 "layout": "split",                              # "single" = one frame, "split" = before (top) / after (bottom)
 "frames": [{"src": "rec/hra2.mp4", "t": 88.0}, {"src": "rec/hra.mp4", "t": 562.8}],
 "title": [["MINUTE 1", "#5ad8ff"], ["VS", "#ffffff"], ["MINUTE 20", "#ff3b4f"]],
 "tag": "VOID SURVIVORS"}
Rules: max 3 short words per line, text inside the middle square (y 420–1500) so it survives the 1:1 / 4:5 grid crop,
the frame must show real gameplay (no menus, cards, desktop or Czech text).
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

W, H = 1080, 1920
TITLE_FONTS = ["/usr/share/fonts/opentype/inter/InterDisplay-Black.otf", "C:/Windows/Fonts/ariblk.ttf",
               "/root/build/proj/assets/fonts/ChakraPetch-SemiBold.ttf"]
TAG_FONTS = ["/root/build/proj/assets/fonts/ChakraPetch-SemiBold.ttf", "../VOID_SURVIVORS_v0_6_3D_UNIVERSE/assets/fonts/ChakraPetch-SemiBold.ttf"]


def font(cands, size):
    for p in cands:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def grab(src, t):
    fd, p = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", src, "-frames:v", "1", p], check=True)
    im = Image.open(p).convert("RGB")
    os.remove(p)
    return im


def cover_fit(im, w, h, zoom=1.0):
    s = max(w / im.width, h / im.height) * zoom
    im = im.resize((int(im.width * s + 0.5), int(im.height * s + 0.5)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def fit_size(d, text, fnt_cands, max_w, start):
    size = start
    while size > 40:
        f = font(fnt_cands, size)
        if d.textlength(text, font=f) <= max_w:
            return f
        size -= 6
    return font(fnt_cands, size)


def main(p):
    c = json.load(open(p, encoding="utf-8"))
    fr = [grab(f["src"], f["t"]) for f in c["frames"]]
    if c.get("layout") == "split" and len(fr) >= 2:
        top = ImageEnhance.Brightness(cover_fit(fr[0], W, H // 2, 1.25)).enhance(0.85)
        bot = ImageEnhance.Brightness(cover_fit(fr[1], W, H // 2, 1.25)).enhance(1.05)
        img = Image.new("RGB", (W, H))
        img.paste(top, (0, 0))
        img.paste(bot, (0, H // 2))
    else:
        img = ImageEnhance.Brightness(cover_fit(fr[0], W, H, 1.15)).enhance(0.9)
    img = img.convert("RGBA")
    # dark band behind the title, centred
    lines = c["title"]
    d0 = ImageDraw.Draw(img)
    fonts = [fit_size(d0, t, TITLE_FONTS, 940, 210 if len(t) > 3 else 120) for t, _ in lines]
    heights = [f.size * 1.02 for f in fonts]
    total = sum(heights)
    y0 = H / 2 - total / 2
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    bd.rectangle([0, y0 - 50, W, y0 + total + 40], fill=(6, 3, 14, 170))
    img = Image.alpha_composite(img, band.filter(ImageFilter.GaussianBlur(18)))
    d = ImageDraw.Draw(img)
    d.rectangle([90, y0 - 52, W - 90, y0 - 46], fill=(255, 59, 79, 255))
    d.rectangle([90, y0 + total + 34, W - 90, y0 + total + 40], fill=(255, 59, 79, 255))
    y = y0
    for (t, col), f, h in zip(lines, fonts, heights):
        tw = d.textlength(t, font=f)
        d.text(((W - tw) / 2, y - f.size * 0.08), t, font=f, fill=col, stroke_width=8, stroke_fill=(8, 4, 16, 255))
        y += h
    tag = c.get("tag", "VOID SURVIVORS")
    ft = font(TAG_FONTS, 46)
    tw = d.textlength(tag, font=ft)
    d.text(((W - tw) / 2, y0 + total + 60), tag, font=ft, fill=(90, 216, 255, 255), stroke_width=4, stroke_fill=(8, 4, 16, 255))
    os.makedirs(os.path.dirname(os.path.abspath(c["out"])), exist_ok=True)
    img.convert("RGB").save(c["out"], quality=92)
    print("cover:", c["out"])


if __name__ == "__main__":
    main(sys.argv[1])
