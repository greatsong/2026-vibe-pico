# 소리 인식 ④(I2S) — INMP441 + k-NN(거리가중)으로 알아맞히기 + LED · 특징 3개
import struct, time, math
from machine import I2S, Pin
from neopixel import NeoPixel

audio = I2S(0, sck=Pin(18), ws=Pin(19), sd=Pin(20),
            mode=I2S.RX, bits=32, format=I2S.MONO, rate=16000, ibuf=40000)
N = 2400; raw = bytearray(N * 4)
def grab():
    audio.readinto(raw)
    return [x >> 16 for x in struct.unpack("<%di" % N, raw)]
def features(buf):
    n = len(buf); m = sum(buf) / n; ss = 0.0; zc = 0; peak = 0.0; prev = buf[0] - m
    for v in buf:
        d = v - m; ad = d if d >= 0 else -d; ss += d * d
        if ad > peak: peak = ad
        if (d >= 0) != (prev >= 0): zc += 1
        prev = d
    r = math.sqrt(ss / n); return r, zc, peak / (r + 1e-9)
small = bytearray(512 * 4)
def level():
    audio.readinto(small); v = [x >> 16 for x in struct.unpack("<512i", small)]; m = sum(v) / 512
    return math.sqrt(sum((x - m) ** 2 for x in v) / 512)

TIMING = (280, 515, 515, 745); NUM = 10
np = NeoPixel(Pin(16), NUM, timing=TIMING)
PALETTE = [(40, 0, 0), (0, 40, 0), (0, 0, 40), (40, 40, 0), (40, 0, 40), (0, 40, 40)]
def show(ci, lv):
    c = PALETTE[ci % len(PALETTE)]
    for i in range(NUM): np[i] = c if i < lv else (0, 0, 0)
    np.write()

rows = []
for ln in open("sounds.csv"):
    ln = ln.strip()
    if ln == "" or ln.startswith("rms"): continue
    r, z, c, nm = ln.split(","); rows.append((float(r), float(z), float(c), nm))
names = sorted(set(r[3] for r in rows)); cidx = {nm: i for i, nm in enumerate(names)}
print("예시 %d개, 소리 종류: %s" % (len(rows), names))
mins = [min(r[i] for r in rows) for i in range(3)]
maxs = [max(r[i] for r in rows) for i in range(3)]
def norm(v): return [(v[i] - mins[i]) / (maxs[i] - mins[i] + 1e-9) for i in range(3)]
ex = [(norm(r[:3]), r[3]) for r in rows]
def predict(feat, k=5):
    q = norm(feat)
    def d2(e): return sum((e[0][i] - q[i]) ** 2 for i in range(3))
    near = sorted(ex, key=d2)[:k]; vote = {}
    for e in near: vote[e[1]] = vote.get(e[1], 0) + 1.0 / (d2(e) + 1e-6)
    b = max(vote, key=vote.get); return b, vote[b] / sum(vote.values())

print("조용히… 배경소음 측정 중")
base = max(level() for _ in range(20)); THRESH = base * 2   # 민감하게(작은 소리도). 잦으면 ↑
print("준비! 소리를 내면 알아맞힐게요.")
while True:
    if level() > THRESH:
        feat = features(grab()); name, conf = predict(feat)
        print("이건… %s!  (확신 %d%%, 크기=%.0f 높낮이=%d 들쭉=%.2f)"
              % (name, conf * 100, feat[0], feat[1], feat[2]))
        show(cidx[name], max(1, int(conf * NUM))); time.sleep(1.0); show(0, 0)
