# Reads the video track's sync-sample table (stss) straight from the moov box and
# writes keyframe times/offsets using the packet list from ffprobe (decode order).
import struct, csv, json, sys
F = "/root/build/rec1118/rec1118_sparse.mp4"
MOOV = 3724098124
P = 50331648
f = open(F, "rb"); f.seek(MOOV)
size, typ = struct.unpack(">I4s", f.read(8)); assert typ == b"moov", typ
moov = f.read(size - 8)
def boxes(buf, off=0, end=None):
    end = len(buf) if end is None else end
    while off + 8 <= end:
        sz, t = struct.unpack(">I4s", buf[off:off+8]); h = 8
        if sz == 1: sz = struct.unpack(">Q", buf[off+8:off+16])[0]; h = 16
        yield t, off + h, off + sz
        off += sz
def find(buf, path, off=0, end=None):
    for t, a, b in boxes(buf, off, end):
        if t == path[0]:
            if len(path) == 1: yield a, b
            else: yield from find(buf, path[1:], a, b)
for a, b in find(moov, [b"trak"]):
    hd = [x for x in find(moov, [b"mdia", b"hdlr"], a, b)][0]
    if moov[hd[0]+8:hd[0]+12] != b"vide": continue
    st = [x for x in find(moov, [b"mdia", b"minf", b"stbl", b"stss"], a, b)][0]
    n = struct.unpack(">I", moov[st[0]+4:st[0]+8])[0]
    sync = struct.unpack(">%dI" % n, moov[st[0]+8:st[0]+8+4*n])
rows = [r for r in csv.reader(open("/root/build/rec1118/vpk.csv")) if len(r) >= 4]
kf = []
for s in sync:
    r = rows[s - 1]
    kf.append([round(float(r[0]), 4), int(r[2])])
kf.sort()
json.dump(kf, open("/root/build/rec1118/keyframes.json", "w"))
gaps = sorted(b[0] - a[0] for a, b in zip(kf, kf[1:]))
print("sync samples", len(sync), "first", kf[:3], "median gap", round(gaps[len(gaps)//2], 3), "max gap", round(gaps[-1], 3))
