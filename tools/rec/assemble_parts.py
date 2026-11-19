# Writes every staged rec1118.partNNN into a sparse full-size copy of the recording.
import os, sys, json, glob
SRC = "/mnt/user-data/uploads/VOID_SURVIVORS_v0_6_3D_UNIVERSE/nahravky_casti"
OUT = "/root/build/rec1118/rec1118_sparse.mp4"
DONE = "/root/build/rec1118/written.json"
PART = 50331648
TOTAL = 3725494053
if not os.path.exists(OUT):
    with open(OUT, "wb") as f: f.truncate(TOTAL)
done = set(json.load(open(DONE))) if os.path.exists(DONE) else set()
new = []
with open(OUT, "r+b") as out:
    for p in sorted(glob.glob(SRC + "/rec1118.part*")):
        n = int(p.rsplit("part", 1)[1])
        exp = PART if n < 74 else TOTAL - 74 * PART
        if n in done or os.path.getsize(p) != exp: continue
        out.seek(n * PART)
        with open(p, "rb") as f:
            while True:
                b = f.read(1 << 22)
                if not b: break
                out.write(b)
        done.add(n); new.append(n)
json.dump(sorted(done), open(DONE, "w"))
print("written now:", new, "| have:", sorted(done))
