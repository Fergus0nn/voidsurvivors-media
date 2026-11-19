# Contact sheet of all keyframes inside the given parts: python3 sheet.py OUTPREFIX N [N...]
import json, sys, subprocess, os
P = 50331648
kf = json.load(open("/root/build/rec1118/keyframes.json"))
out = sys.argv[1]; parts = [int(x) for x in sys.argv[2:]]
tmp = out + "_frames"; os.makedirs(tmp, exist_ok=True)
sel = [(t, pos) for t, pos in kf if pos // P in parts and (pos // P + 1) * P > pos]
imgs = []
for t, pos in sel:
    o = f"{tmp}/k_{t:08.2f}.jpg"
    if not os.path.exists(o):
        subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", "/root/build/rec1118/rec1118_sparse.mp4",
                        "-frames:v", "1", "-vf", f"scale=480:-1,drawtext=text='{int(t//60)}\\:{t%60:04.1f}':x=6:y=6:fontsize=22:fontcolor=yellow:box=1:boxcolor=black@0.6",
                        "-q:v", "4", o], stderr=subprocess.DEVNULL)
    if os.path.exists(o) and os.path.getsize(o) > 3000: imgs.append(o)
print(len(sel), "keyframes,", len(imgs), "decoded")
cols = 4
for i in range(0, len(imgs), 16):
    chunk = imgs[i:i+16]
    args = ["ffmpeg", "-v", "error", "-y"]
    for c in chunk: args += ["-i", c]
    n = len(chunk); rows = (n + cols - 1) // cols
    layout = "|".join(f"{(j%cols)*480}_{(j//cols)*270}" for j in range(n))
    args += ["-filter_complex", "".join(f"[{j}:v]" for j in range(n)) + f"xstack=inputs={n}:layout={layout}:fill=black" if n > 1 else "null",
             "-q:v", "4", f"{out}_{i//16:02d}.jpg"]
    subprocess.run(args)
    print(f"{out}_{i//16:02d}.jpg")
