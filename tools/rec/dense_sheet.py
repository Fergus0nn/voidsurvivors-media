# Dense contact sheet (1 frame per STEP s) for a contiguous fully-staged time range:
# python3 dense.py OUTPREFIX START_S END_S [STEP]
import sys, subprocess, os, glob
out, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
step = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
tmp = out + "_f"; os.makedirs(tmp, exist_ok=True)
for f in glob.glob(tmp + "/*.jpg"): os.remove(f)
subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a:.3f}", "-t", f"{b-a:.3f}", "-i", "/root/build/rec1118/rec1118_sparse.mp4",
    "-vf", f"fps={1/step:.6f},scale=384:-1,drawtext=text='%{{eif\\:({a}+t)/60\\:d}}\\:%{{eif\\:mod({a}+t\\,60)\\:d\\:2}}':x=5:y=5:fontsize=20:fontcolor=yellow:box=1:boxcolor=black@0.6",
    "-q:v", "5", tmp + "/f_%04d.jpg"], stderr=subprocess.DEVNULL)
imgs = sorted(glob.glob(tmp + "/f_*.jpg"))
cols, per = 5, 25
for i in range(0, len(imgs), per):
    ch = imgs[i:i+per]; n = len(ch)
    args = ["ffmpeg", "-v", "error", "-y"]
    for c in ch: args += ["-i", c]
    lay = "|".join(f"{(j%cols)*384}_{(j//cols)*216}" for j in range(n))
    args += ["-filter_complex", "".join(f"[{j}:v]" for j in range(n)) + f"xstack=inputs={n}:layout={lay}:fill=black", "-q:v", "5", f"{out}_{i//per:02d}.jpg"]
    subprocess.run(args); print(f"{out}_{i//per:02d}.jpg")
