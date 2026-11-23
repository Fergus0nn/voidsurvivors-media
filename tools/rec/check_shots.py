# Verifies every shot in a spec only needs parts that are already staged: python3 check_shots.py spec.json
import json, csv, sys, bisect
P = 50331648
have = set(json.load(open("/root/build/rec1118/written.json")))
kf = json.load(open("/root/build/rec1118/keyframes.json"))
kft = [k[0] for k in kf]
pk = sorted((float(r[0]), int(r[2])) for r in csv.reader(open("/root/build/rec1118/vpk.csv")) if len(r) >= 4 and r[0] not in ("", "N/A"))
pkt = [p[0] for p in pk]
spec = json.load(open(sys.argv[1]))
items = spec.get("shots") or spec.get("frames")
ok = True
for s in items:
    ss = s.get("ss", s.get("t")); dur = s.get("dur", 0.05) * s.get("speed", 1.0)   # slow-mo shots read less source
    i = bisect.bisect_right(kft, ss) - 1
    k0 = kf[i]
    lo = bisect.bisect_left(pkt, k0[0]); hi = bisect.bisect_right(pkt, ss + dur + 0.1)
    need = sorted({p[1] // P for p in pk[lo:hi]} | {(p[1] + 200000) // P for p in pk[lo:hi]})
    miss = [n for n in need if n not in have]
    if miss: ok = False
    print(f"{ss:8.2f} +{dur:.1f}s  keyframe {k0[0]:.2f}  parts {need}  {'MISSING ' + str(miss) if miss else 'ok'}")
print("ALL OK" if ok else "SOME PARTS MISSING")
