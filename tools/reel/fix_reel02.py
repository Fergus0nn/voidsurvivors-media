"""Oprava reel02: END OF DEMO -> posledni gameplay pred koncem, Kai 'Follow for the demo!' -> nova veta, Steam radek -> novy text."""
import subprocess, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FF=r"C:\Users\GameBox\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe"
SRC=r"C:\Users\GameBox\Desktop\nahrávky ze hry\2026-11-08 01-06-39.mp4"
REEL=r"C:\Users\GameBox\Downloads\voidsurvivors-media\v\reel02_survive.mp4"
OUT=sys.argv[1]
W,H=1080,1920; FPS=30; N=810
BAND_Y0, BAND_H = 470, 698
HOOK_N = 75                       # snimky 0..74 dostanou novy pas (17..74 bylo END OF DEMO)
SRC_T0 = 572.55 - HOOK_N / FPS    # REC A 570.05 -> 572.517 (posledni hratelne snimky pred 20:00)
NEW_BUBBLE = ["How long would YOU survive?", "Tell me!"]
NEW_LINE = "NEW UPDATE EVERY FRIDAY"
FONT = r"C:\Windows\Fonts\bahnschrift.ttf"

def fnt(sz, var="SemiBold"):
    f = ImageFont.truetype(FONT, sz); f.set_variation_by_name(var); return f

def reader(path, ss, n, vf):
    cmd=[FF,"-v","error","-ss",str(ss),"-i",path,"-vf",vf,"-frames:v",str(n),"-f","rawvideo","-pix_fmt","rgb24","-"]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE)

def readf(p, w, h):
    b = p.stdout.read(w*h*3)
    return None if len(b) < w*h*3 else np.frombuffer(b, np.uint8).reshape(h, w, 3).copy()

# --- staticky konec: radek se Steamem ---
def grab(t):
    p = reader(REEL, t, 1, "null"); f = readf(p, W, H); p.wait(); return f
static = grab(25.5).astype(np.float32)
RY0, RY1, RX0, RX1 = 1125, 1218, 60, 1020
old = static[RY0:RY1, RX0:RX1]
top = static[RY0-3:RY0, RX0:RX1].mean(axis=0); bot = static[RY1:RY1+3, RX0:RX1].mean(axis=0)
k = np.ones(31)/31
top = np.stack([np.convolve(np.pad(top[:,c],15,mode='edge'),k,'valid') for c in range(3)],1)
bot = np.stack([np.convolve(np.pad(bot[:,c],15,mode='edge'),k,'valid') for c in range(3)],1)
w = np.linspace(0,1,RY1-RY0)[:,None,None]
plate = (1-w)*top[None] + w*bot[None]
lay = Image.new("RGBA", (RX1-RX0, RY1-RY0), (0,0,0,0)); d = ImageDraw.Draw(lay)
F = fnt(62); SP = 2.6
widths = [F.getlength(ch) for ch in NEW_LINE]; tw = sum(widths) + SP*(len(NEW_LINE)-1)
x = 540 - tw/2 - RX0; BASE = 1193 - RY0
for ch, cw in zip(NEW_LINE, widths):
    d.text((x, BASE), ch, font=F, fill=(255,176,92,255), anchor="ls"); x += cw + SP
la = np.asarray(lay).astype(np.float32); al = la[:,:,3:4]/255
new = plate*(1-al) + la[:,:,:3]*al
delta = new - old
# pruhlednost radku behem prolinani: kontrast pismen vuci okoli (gameplay pod nim se vyprumeruje)
M = (old.min(axis=2) > 60) & (old[:,:,0] > 180)
ring = np.asarray(Image.fromarray((M*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9))) > 0
ring &= ~M
C0 = old[M].mean() - old[ring].mean()
def alpha_of(cur):
    return float(np.clip((cur[M].mean() - cur[ring].mean()) / C0, 0, 1))

# --- bublina ---
BF = fnt(51); TXT=(19,15,34); BASE1, BASE2, TX = 541, 603, 178
FX0, FX1, FY0, FY1 = 152, 928, 488, 629
def bubble_fix(fr, t, final_dark):
    reg = fr[380:700, 100:980]
    lt = reg.min(axis=2) > 200
    if lt.sum() < 500: return
    ys, xs = np.nonzero(lt); x0, x1, y0, y1 = xs.min()+100, xs.max()+100, ys.min()+380, ys.max()+380
    bw = x1 - x0
    inner = (244,241,249)
    if 770 <= bw <= 800 and 205 <= y1-y0 <= 230:
        sub = fr[FY0:FY1, FX0:FX1]
        dark = (sub.max(axis=2) < 110).sum()
        ratio = min(1.0, dark/final_dark)
        col = fr[620, 905].astype(int)
        fr[FY0:FY1, FX0:FX1] = col
        total = sum(len(s) for s in NEW_BUBBLE); n = int(round(total*ratio))
        im = Image.fromarray(fr); dd = ImageDraw.Draw(im)
        l1 = NEW_BUBBLE[0][:n]; l2 = NEW_BUBBLE[1][:max(0, n-len(NEW_BUBBLE[0]))]
        if l1: dd.text((TX, BASE1), l1, font=BF, fill=TXT, anchor="ls")
        if l2: dd.text((TX, BASE2), l2, font=BF, fill=TXT, anchor="ls")
        fr[:] = np.asarray(im)
    elif t > 26.0 and bw < 770:
        s = bw / 793.0; cx = (x0+x1)/2; cy = y1 - 83*s
        a0, a1 = int(cx-380*s), int(cx+380*s); b0, b1 = int(cy-62*s), int(cy+66*s)
        if a1 > a0 and b1 > b0:
            fr[b0:b1, a0:a1] = fr[min(b1+2, y1-1), int(cx)] if False else np.array(inner)*0 + fr[int(cy), x1-int(12*s)-2]

fin = grab(26.3); final_dark = (fin[FY0:FY1, FX0:FX1].max(axis=2) < 110).sum()

src = reader(SRC, SRC_T0, HOOK_N, f"fps={FPS},scale=1241:698:flags=lanczos,crop=1080:698:80:0")
rd = reader(REEL, 0, N, "null")
enc = subprocess.Popen([FF,"-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
    "-i",REEL,"-map","0:v","-map","1:a","-c:v","libx264","-preset","slow","-crf","17","-pix_fmt","yuv420p",
    "-c:a","copy","-movflags","+faststart","-shortest",OUT], stdin=subprocess.PIPE)
log=[]
for i in range(N):
    fr = readf(rd, W, H)
    if fr is None: break
    t = i / FPS
    if i < HOOK_N:
        s = readf(src, 1080, BAND_H)
        fr[BAND_Y0:BAND_Y0+BAND_H] = s
    if t >= 23.7:
        cur = fr[RY0:RY1, RX0:RX1].astype(np.float32)
        a = alpha_of(cur) if t < 24.6 else 1.0
        if a < 0.05: a = 0.0
        if a > 0.95: a = 1.0
        if a > 0:
            fr[RY0:RY1, RX0:RX1] = np.clip(cur + a*delta, 0, 255).astype(np.uint8)
        bubble_fix(fr, t, final_dark)
        if t < 24.7: log.append((round(t,2), round(a,2)))
    enc.stdin.write(fr.tobytes())
enc.stdin.close(); enc.wait(); rd.kill(); src.kill()
print("fade", log[:12]); print("HOTOVO", OUT)
