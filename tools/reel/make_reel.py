"""REEL 03 – 3 BOSSES. 1 RUN.  (9:16, 30 fps, bez hudby – zvuk jen ze hry)
Skládá video snímek po snímku: záběry ze hry + Kai + bubliny + titulky + efekty."""
import math, os, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

BIN = r"C:\Users\GameBox\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin"
FF = os.path.join(BIN, "ffmpeg.exe")
SRC = r"C:\Users\GameBox\Desktop\nahrávky ze hry\Ufon tank + dmg + ats.mp4"
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT_V = os.path.join(HERE, "reel_video.mp4")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "reel03_three_bosses.mp4")
PREVIEW = "--preview" in sys.argv          # jen pár snímků na kontrolu

W, H, FPS = 1080, 1920, 30
BAND_Y, BAND_H = 300, 1350                 # pás s gameplayem (4:5)
random.seed(7)

# ------------------------------------------------------------------ fonty
def font(size, weight="Bold"):
    f = ImageFont.truetype(r"C:\Windows\Fonts\bahnschrift.ttf", size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f

# ------------------------------------------------------------------ easing
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease_out_back(x, s=1.70158):
    x = clamp(x); x -= 1
    return x * x * ((s + 1) * x + s) + 1
def ease_out_cubic(x): x = clamp(x); return 1 - (1 - x) ** 3

# ------------------------------------------------------------------ střih (zdroj s, konec s, rychlost, režim)
SEGS = [
    # HÁČEK – plná výška, rychlé střihy
    dict(id="H1", a=1000.0, b=1000.6, sp=1.0, mode="full", cut=True),
    dict(id="H2", a=1341.0, b=1341.6, sp=1.0, mode="full", cut=True),
    dict(id="H3", a=593.0,  b=593.6,  sp=1.0, mode="full", cut=True),
    # BOSS 1 – Lord of Darkness
    dict(id="L1", a=569.6, b=572.2, sp=1.0, mode="band", boss=1, flash=True),
    dict(id="L2", a=587.5, b=589.1, sp=1.0, mode="band", boss=1, cut=True),
    dict(id="L3", a=601.8, b=603.7, sp=1.0, mode="band", boss=1, cut=True),
    dict(id="L4", a=603.7, b=604.3, sp=0.5, mode="band", boss=1),
    dict(id="L5", a=604.3, b=604.6, sp=1.0, mode="band", boss=1),
    # BOSS 2 – Leviathan (16:29–16:38 má české nápisy -> vynecháno)
    dict(id="V1", a=985.2,  b=988.4,  sp=1.0, mode="band", boss=2, flash=True),
    dict(id="V2", a=1002.4, b=1003.7, sp=1.0, mode="band", boss=2, cut=True),
    dict(id="V3", a=1003.7, b=1004.5, sp=0.4, mode="band", boss=2),
    dict(id="V4", a=1004.5, b=1004.65, sp=1.0, mode="band", boss=2),
    # BOSS 3 – Mothership
    dict(id="M1", a=1337.0, b=1340.8, sp=1.0, mode="band", boss=3, flash=True),
    dict(id="M2", a=1344.0, b=1345.5, sp=1.0, mode="band", boss=3, cut=True),
    dict(id="M3", a=1347.7, b=1348.3, sp=0.5, mode="band", boss=3),
    dict(id="M4", a=1348.3, b=1349.3, sp=1.0, mode="band", boss=3),
    # FINÁLE – Blood Moon
    dict(id="B1", a=1664.0, b=1666.6, sp=1.0, mode="band", boss=4, flash=True),
    # KONEC
    dict(id="END", dur=3.3, mode="end", flash=True),
]
KILLS = {"L": 604.0, "V": 1004.0, "M": 1348.0}   # zdrojový čas záblesku smrti bosse

t = 0.0
for s in SEGS:
    s["t0"] = t
    s["dur"] = s.get("dur") or (s["b"] - s["a"]) / s["sp"]
    s["n"] = int(round(s["dur"] * FPS))
    t += s["n"] / FPS
    s["t1"] = t
TOTAL = t
T = {s["id"]: s for s in SEGS}

def out_time(seg_id, src_time):
    s = T[seg_id]
    return s["t0"] + (src_time - s["a"]) / s["sp"]

KILL_T = {1: out_time("L4", KILLS["L"]), 2: out_time("V3", KILLS["V"]), 3: out_time("M3", KILLS["M"])}
BOSS_START = {1: T["L1"]["t0"], 2: T["V1"]["t0"], 3: T["M1"]["t0"], 4: T["B1"]["t0"]}

# ------------------------------------------------------------------ Kai – repliky (od, do, text, nálada)
LINES = [
    (0.15, T["L1"]["t0"], "I built 3 bosses...", "talk"),
    (T["L1"]["t0"], T["L3"]["t0"], "...then fought them all in ONE run.", "talk"),
    (T["L3"]["t0"], T["V1"]["t0"], "Lord of Darkness. Mind the beams!", "serious"),
    (T["V1"]["t0"], T["V2"]["t0"], "This snake is bigger than the screen!", "surprised"),
    (T["V2"]["t0"], T["M1"]["t0"], "Slow down... and hit it hard.", "serious"),
    (T["M1"]["t0"], T["M2"]["t0"], "The Mothership. Dodge the laser!", "surprised"),
    (T["M2"]["t0"], T["B1"]["t0"], "Last stand... BOOM.", "talk"),
    (T["B1"]["t0"], T["END"]["t0"], "...then the moon turned red.", "surprised"),
    (T["END"]["t0"] + 0.25, TOTAL + 1, "Tell me in the comments!", "happy"),
]
MOOD_BASE = {"talk": 0, "serious": 4, "surprised": 2, "happy": 3}
MOOD_OPEN = {"talk": 5, "serious": 5, "surprised": 2, "happy": 5}

CAPS = {
    1: ("BOSS 1 / 3", "LORD OF DARKNESS", (255, 77, 109)),
    2: ("BOSS 2 / 3", "THE ANCIENT LEVIATHAN", (186, 120, 255)),
    3: ("BOSS 3 / 3", "THE MOTHERSHIP", (93, 255, 143)),
    4: ("MINUTE 19", "BLOOD MOON", (255, 60, 70)),
}

# ------------------------------------------------------------------ grafické prvky (předpočítané)
def glow_text(text, size, fill, glow, stroke=0, weight="Bold", glow_r=14, max_w=None):
    f = font(size, weight)
    if max_w:
        while f.getlength(text) > max_w and size > 40:
            size -= 4; f = font(size, weight)
    bb = f.getbbox(text, stroke_width=stroke)
    pad = glow_r * 3
    w, h = bb[2] - bb[0] + pad * 2, bb[3] - bb[1] + pad * 2
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    g = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(g).text((pad - bb[0], pad - bb[1]), text, font=f, fill=glow + (230,), stroke_width=stroke + 4, stroke_fill=glow + (230,))
    g = g.filter(ImageFilter.GaussianBlur(glow_r))
    img.alpha_composite(g)
    d = ImageDraw.Draw(img)
    d.text((pad - bb[0] + 4, pad - bb[1] + 6), text, font=f, fill=(0, 0, 0, 150), stroke_width=stroke, stroke_fill=(0, 0, 0, 150))
    d.text((pad - bb[0], pad - bb[1]), text, font=f, fill=fill + (255,), stroke_width=stroke, stroke_fill=(10, 6, 20, 255))
    return img

def pill(text, size, fg, bg):
    f = font(size, "Bold")
    bb = f.getbbox(text)
    w, h = bb[2] - bb[0] + 48, bb[3] - bb[1] + 26
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=bg + (235,))
    d.text((24 - bb[0], 13 - bb[1]), text, font=f, fill=fg + (255,))
    return img

def radial(w, h, color, inner=0.0, power=1.6):
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    a = np.clip(1 - r, 0, 1) ** power
    arr = np.zeros((h, w, 4), np.uint8)
    arr[..., :3] = color
    arr[..., 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")

def vignette(w, h, strength=170):
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    a = np.clip((r - 0.55) / 0.75, 0, 1) ** 1.5 * strength
    arr = np.zeros((h, w, 4), np.uint8)
    arr[..., 3] = a.astype(np.uint8)
    return Image.fromarray(arr, "RGBA")

KAI_SCALE = 1.4
KAI = [Image.open(os.path.join(ASSETS, f"kai_{i}.png")).convert("RGBA") for i in range(6)]
KAI = [k.resize((int(k.width * KAI_SCALE), int(k.height * KAI_SCALE)), Image.LANCZOS) for k in KAI]
KAI_GLOW = radial(560, 560, (150, 70, 255), power=2.2)
LOGO = Image.open(os.path.join(ASSETS, "logo.png")).convert("RGBA")
LOGO = LOGO.resize((900, int(LOGO.height * 900 / LOGO.width)), Image.LANCZOS)
LOGO_GLOW = LOGO.copy().filter(ImageFilter.GaussianBlur(18))
VIG_BAND = vignette(W, BAND_H, 150)
VIG_FULL = vignette(W, H, 190)

CAP_IMG = {}
for k, (lab, title, col) in CAPS.items():
    CAP_IMG[k] = (pill(lab, 40, (20, 12, 30), (255, 176, 64) if k < 4 else (255, 90, 90)),
                  glow_text(title, 104, (255, 255, 255), col, stroke=3, max_w=1010, glow_r=16))
HOOK1 = glow_text("3 BOSSES.", 200, (255, 255, 255), (170, 90, 255), stroke=5, glow_r=22)
HOOK2 = glow_text("1 RUN.", 200, (255, 176, 64), (255, 90, 40), stroke=5, glow_r=22)
STAMP = glow_text("DEFEATED", 150, (255, 255, 255), (255, 60, 80), stroke=6, glow_r=20).rotate(-8, expand=True, resample=Image.BICUBIC)
END1 = glow_text("HOW LONG WOULD", 92, (255, 255, 255), (150, 80, 255), stroke=3)
END2 = glow_text("YOU SURVIVE?", 120, (255, 176, 64), (255, 90, 40), stroke=4)
END3 = glow_text("COMMENT BELOW", 60, (235, 225, 255), (150, 80, 255), stroke=2, weight="SemiBold", glow_r=10)
END4 = glow_text("COMING SOON TO STEAM", 44, (200, 185, 255), (90, 50, 180), stroke=0, weight="SemiBold", glow_r=8)

BUB_F = font(42, "SemiBold")
LAB_F = font(26, "Bold")

def wrap(text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        test = (cur + " " + w_).strip()
        if f.getlength(test) <= maxw: cur = test
        else: lines.append(cur); cur = w_
    lines.append(cur)
    return lines

def bubble(text, shown):
    """Bublina s psaným textem – rozměr podle celého textu, vykreslí jen `shown` znaků."""
    maxw = 560
    lines = wrap(text, BUB_F, maxw)
    lh = 52
    tw = max(BUB_F.getlength(l) for l in lines)
    bw, bh = int(tw) + 56, lh * len(lines) + 40
    img = Image.new("RGBA", (bw + 40, bh + 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    ox, oy = 30, 34
    d.rounded_rectangle((ox + 4, oy + 8, ox + bw + 4, oy + bh + 8), radius=26, fill=(0, 0, 0, 90))
    d.polygon([(ox + 2, oy + bh * 0.42), (ox - 26, oy + bh * 0.62), (ox + 2, oy + bh * 0.70)], fill=(166, 102, 255, 255))
    d.rounded_rectangle((ox, oy, ox + bw, oy + bh), radius=26, fill=(246, 241, 255, 255), outline=(166, 102, 255, 255), width=5)
    d.polygon([(ox + 6, oy + bh * 0.46), (ox - 16, oy + bh * 0.62), (ox + 6, oy + bh * 0.66)], fill=(246, 241, 255, 255))
    d.text((ox + 8, 0), "KAI", font=LAB_F, fill=(200, 170, 255, 255))
    left = shown
    y = oy + 22
    for l in lines:
        part = l[:max(0, left)]
        d.text((ox + 28, y), part, font=BUB_F, fill=(30, 20, 48, 255))
        left -= len(l) + 1
        y += lh
    return img

# ------------------------------------------------------------------ čtení snímků ze záznamu
def frames(seg):
    if seg["mode"] == "end":
        for _ in range(seg["n"]): yield None
        return
    rate = FPS * seg["sp"]
    cmd = [FF, "-v", "error", "-ss", f"{seg['a']:.3f}", "-i", SRC, "-t", f"{seg['b'] - seg['a'] + 0.2:.3f}",
           "-an", "-vf", f"fps={rate}", "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    size = 1280 * 720 * 3
    last = None
    for _ in range(seg["n"]):
        buf = p.stdout.read(size)
        if len(buf) == size:
            last = Image.frombuffer("RGB", (1280, 720), buf)
        yield last
    p.stdout.close(); p.kill()

END_BG = Image.open(os.path.join(HERE, "title.png")).convert("RGB").crop((640, 0, 1045, 720))

# ------------------------------------------------------------------ pomocné efekty
def shake_at(tt):
    dx = dy = 0.0
    for kt in KILL_T.values():
        d = tt - kt
        if 0 <= d < 0.9:
            a = 26 * math.exp(-d * 5)
            dx += a * math.sin(d * 63); dy += a * math.cos(d * 51)
    for k, bt in BOSS_START.items():
        d = tt - bt
        if 0 <= d < 0.4:
            a = 12 * math.exp(-d * 9); dx += a * math.sin(d * 70)
    for hid in ("H1", "H2", "H3"):
        d = tt - T[hid]["t0"]
        if 0 <= d < 0.35:
            a = 16 * math.exp(-d * 10); dx += a * math.sin(d * 80); dy += a * math.cos(d * 66)
    return int(dx), int(dy)

def flash_at(tt):
    a = 0.0
    for kt in KILL_T.values():
        d = tt - kt
        if -0.03 <= d < 0.45: a = max(a, 0.85 * (1 - clamp(d / 0.45)))
    for s in SEGS:
        if s.get("flash"):
            d = tt - s["t0"]
            if 0 <= d < 0.22: a = max(a, 0.9 * (1 - d / 0.22))
    return a

def rgb_split(img, px):
    arr = np.asarray(img).copy()
    arr[..., 0] = np.roll(arr[..., 0], px, axis=1)
    arr[..., 2] = np.roll(arr[..., 2], -px, axis=1)
    return Image.fromarray(arr)

def paste_center(canvas, img, cx, cy, scale=1.0, alpha=1.0):
    if scale != 1.0:
        img = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))), Image.BICUBIC)
    if alpha < 1.0:
        img = img.copy()
        img.putalpha(img.getchannel("A").point(lambda v: int(v * alpha)))
    canvas.alpha_composite(img, (int(cx - img.width / 2), int(cy - img.height / 2)))

# ------------------------------------------------------------------ vykreslení jednoho snímku
def render(seg, fr, i, tt):
    p = i / max(1, seg["n"] - 1)
    sx, sy = shake_at(tt)
    mode = seg["mode"]
    if mode == "full":
        z = 1.0 + 0.22 * (1 - ease_out_cubic(i / 8))            # zoom „punch“
        cw, ch = 405 / z, 720 / z
        crop = fr.crop((640 - cw / 2, 360 - ch / 2, 640 + cw / 2, 360 + ch / 2)).resize((W, H), Image.BICUBIC)
        canvas = Image.new("RGBA", (W, H))
        canvas.paste(crop, (sx, sy))
        canvas.alpha_composite(VIG_FULL)
    elif mode == "band":
        small = fr.crop((440, 0, 840, 720)).resize((60, 108), Image.BILINEAR).filter(ImageFilter.GaussianBlur(4))
        bg = small.resize((W, H), Image.BILINEAR)
        bg = Image.blend(bg, Image.new("RGB", (W, H), (14, 6, 28)), 0.55)
        canvas = bg.convert("RGBA")
        segp = (tt - BOSS_START.get(seg["boss"], seg["t0"]))
        z = 1.0 + 0.012 * segp                                   # pomalé najíždění
        if seg["id"] in ("L4", "V3", "M3"): z += 0.06 * p         # zpomalený zásah – víc přiblížit
        cw, ch = 576 / z, 720 / z
        band = fr.crop((640 - cw / 2, 360 - ch / 2, 640 + cw / 2, 360 + ch / 2)).resize((W, BAND_H), Image.BICUBIC).convert("RGBA")
        if seg["boss"] == 4:                                      # Blood Moon – rudé pulzování
            pulse = 0.5 + 0.5 * math.sin(tt * 7)
            band = Image.blend(band, Image.new("RGBA", band.size, (255, 20, 40, 255)), 0.08 + 0.08 * pulse)
        band.alpha_composite(VIG_BAND)
        canvas.alpha_composite(band, (sx, BAND_Y + sy))
        d = ImageDraw.Draw(canvas)
        col = CAPS[seg["boss"]][2]
        d.line((0, BAND_Y + sy, W, BAND_Y + sy), fill=col + (200,), width=4)
        d.line((0, BAND_Y + BAND_H + sy, W, BAND_Y + BAND_H + sy), fill=col + (200,), width=4)
    else:  # END
        zz = 1.0 + 0.05 * p
        cw, ch = 405 / zz, 720 / zz
        bg = END_BG.crop((202 - cw / 2, 360 - ch / 2, 202 + cw / 2, 360 + ch / 2)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(5))
        canvas = Image.blend(bg, Image.new("RGB", (W, H), (10, 5, 22)), 0.6).convert("RGBA")
        canvas.alpha_composite(VIG_FULL)

    # ---------- titulky
    if mode == "full":
        a1 = tt - 0.05
        if a1 > 0:
            paste_center(canvas, HOOK1, W / 2 + sx * 0.5, 700, scale=0.55 + 0.45 * ease_out_back(a1 / 0.28), alpha=clamp(a1 / 0.1))
        a2 = tt - 0.85
        if a2 > 0:
            paste_center(canvas, HOOK2, W / 2 + sx * 0.5, 920, scale=0.55 + 0.45 * ease_out_back(a2 / 0.28), alpha=clamp(a2 / 0.1))
    elif mode == "band":
        b = seg["boss"]
        lab, title = CAP_IMG[b]
        ct = tt - BOSS_START[b]
        paste_center(canvas, lab, W / 2, 62, scale=0.7 + 0.3 * ease_out_back(ct / 0.3), alpha=clamp(ct / 0.12))
        ct2 = ct - 0.08
        if ct2 > 0:
            paste_center(canvas, title, W / 2, 168, scale=0.6 + 0.4 * ease_out_back(ct2 / 0.32), alpha=clamp(ct2 / 0.12))
        # tři ikonky bossů – odškrtávají se
        d = ImageDraw.Draw(canvas)
        for k in (1, 2, 3):
            cx, cy = W / 2 + (k - 2) * 60, 262
            dead = tt >= KILL_T[k] + 0.15
            active = (b == k)
            colk = CAPS[k][2]
            r = 17 + (3 if active and not dead else 0) * (0.5 + 0.5 * math.sin(tt * 10))
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(colk + (255,)) if dead else (30, 18, 50, 220), outline=colk + (255,), width=3)
            if dead:
                d.line((cx - 8, cy, cx - 2, cy + 7, cx + 9, cy - 7), fill=(20, 10, 30, 255), width=5)
        # razítko DEFEATED
        if b in KILL_T:
            dt = tt - (KILL_T[b] + 0.12)
            if dt > 0:
                paste_center(canvas, STAMP, W / 2, BAND_Y + 340, scale=1.0 + 1.3 * (1 - ease_out_cubic(dt / 0.22)), alpha=clamp(dt / 0.08))
        # Blood Moon – počítadlo comba
        if b == 4:
            n = int(31330 + (tt - BOSS_START[4]) * 95)
            cimg = glow_text(f"{n:,}x COMBO", 96, (255, 255, 255), (255, 40, 60), stroke=3, glow_r=14)
            paste_center(canvas, cimg, W / 2, BAND_Y + BAND_H - 210, scale=0.7 + 0.3 * ease_out_back((tt - BOSS_START[4] - 0.3) / 0.3), alpha=clamp((tt - BOSS_START[4] - 0.3) / 0.1))
    else:
        et = tt - seg["t0"]
        paste_center(canvas, LOGO_GLOW, W / 2, 470, scale=0.7 + 0.3 * ease_out_back(et / 0.4), alpha=clamp(et / 0.15) * (0.55 + 0.25 * math.sin(et * 5)))
        paste_center(canvas, LOGO, W / 2, 470, scale=0.7 + 0.3 * ease_out_back(et / 0.4), alpha=clamp(et / 0.15))
        for img, y, delay in ((END1, 790, 0.35), (END2, 905, 0.5), (END3, 1040, 0.8), (END4, 1185, 0.95)):
            e = et - delay
            if e > 0:
                paste_center(canvas, img, W / 2, y, scale=0.6 + 0.4 * ease_out_back(e / 0.3), alpha=clamp(e / 0.1))
        e = et - 0.9
        if e > 0:   # šipka dolů ke komentářům
            d = ImageDraw.Draw(canvas)
            yy = 1092 + 8 * math.sin(et * 8)
            d.polygon([(W / 2 - 22, yy), (W / 2 + 22, yy), (W / 2, yy + 22)], fill=(255, 176, 64, int(255 * clamp(e / 0.1))))

    # ---------- Kai + bublina
    line = None
    for (a, b_, txt, mood) in LINES:
        if a <= tt < b_: line = (a, txt, mood)
    if line:
        a, txt, mood = line
        lt = tt - a
        shown = int(lt * 30)
        talking = shown < len(txt)
        kt = tt - 0.15
        pop = ease_out_back(kt / 0.4) if kt >= 0 else 0
        bob = math.sin(tt * 3.2) * 6
        base = MOOD_BASE[mood]
        idx = MOOD_OPEN[mood] if (talking and (int(tt * 30) // 3 + i) % 2 == 0 and txt[min(shown, len(txt) - 1)] != " ") else base
        kai = KAI[idx]
        kx = 10
        ky = H - kai.height + int((1 - pop) * 480) + int(bob) + 6
        canvas.alpha_composite(KAI_GLOW, (kx + kai.width // 2 - 280, ky + 40 - 200))
        canvas.alpha_composite(kai, (kx, ky))
        if lt > 0.05:
            bub = bubble(txt, shown)
            bpop = ease_out_back(lt / 0.25)
            paste_center(canvas, bub, kx + kai.width + 10 + bub.width / 2, H - 300 + bob * 0.5, scale=0.6 + 0.4 * bpop, alpha=clamp(lt / 0.1))

    # ---------- záblesk, ukazatel průběhu, RGB split
    fa = flash_at(tt)
    if fa > 0.01:
        canvas.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(255 * fa))))
    d = ImageDraw.Draw(canvas)
    d.rectangle((0, 0, W, 9), fill=(20, 10, 35, 200))
    d.rectangle((0, 0, int(W * tt / TOTAL), 9), fill=(176, 107, 255, 255))
    rgb = canvas.convert("RGB")
    for hid in ("H2", "H3", "L1", "V1", "M1", "B1"):
        d0 = tt - T[hid]["t0"]
        if 0 <= d0 < 0.1:
            rgb = rgb_split(rgb, int(18 * (1 - d0 / 0.1)) + 4)
    return rgb

# ------------------------------------------------------------------ hlavní smyčka
def main():
    print(f"délka {TOTAL:.2f} s, {sum(s['n'] for s in SEGS)} snímků")
    for s in SEGS: print(f"  {s['id']:4s} {s['t0']:6.2f}–{s['t1']:6.2f}")
    print("zabití:", {k: round(v, 2) for k, v in KILL_T.items()})
    if PREVIEW:
        os.makedirs(os.path.join(HERE, "prev"), exist_ok=True)
        picks = [0.5, 1.2, 2.3, 7.8, 10.5, 16.5, 19.0, 23.0, 26.5, 29.5]
        for s in SEGS:
            for i, fr in enumerate(frames(s)):
                tt = s["t0"] + i / FPS
                for pk in picks:
                    if abs(tt - pk) < 0.5 / FPS:
                        render(s, fr, i, tt).save(os.path.join(HERE, "prev", f"p_{pk:05.1f}.jpg"), quality=88)
        return
    enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", OUT_V], stdin=subprocess.PIPE)
    k = 0
    for s in SEGS:
        for i, fr in enumerate(frames(s)):
            tt = s["t0"] + i / FPS
            enc.stdin.write(render(s, fr, i, tt).tobytes())
            k += 1
        print(f"  hotovo {s['id']} ({k} snímků)", flush=True)
    enc.stdin.close(); enc.wait()

    # zvuk: stejné úseky, zpomalené části s nižším tónem, vyrovnaná hlasitost
    parts, labels = [], []
    for j, s in enumerate(SEGS):
        if s["mode"] == "end": continue
        f = f"[0:a]atrim=start={s['a']}:end={s['a'] + s['n'] / FPS * s['sp']:.4f},asetpts=PTS-STARTPTS"
        if s["sp"] != 1.0:
            f += f",asetrate={int(48000 * s['sp'])},aresample=48000"
        parts.append(f + f"[a{j}]"); labels.append(f"[a{j}]")
    fc = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(labels)}:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000," \
         f"afade=t=out:st={T['END']['t0'] - 0.1:.2f}:d=1.2,apad=whole_dur={TOTAL:.3f}[aout]"
    subprocess.run([FF, "-v", "error", "-y", "-i", SRC, "-i", OUT_V, "-filter_complex", fc, "-map", "1:v", "-map", "[aout]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", OUT], check=True)
    print("HOTOVO:", OUT)

if __name__ == "__main__":
    main()
