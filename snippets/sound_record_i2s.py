# 소리 인식 ③(I2S) — INMP441로 소리 모으기 (콘솔 키 라벨링) · 특징 3개
from machine import I2S, Pin
from neopixel import NeoPixel
import struct, time, math

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
def flash(c, t=0.2): np.fill(c); np.write(); time.sleep(t); np.fill((0, 0, 0)); np.write()

LABELS = {"1": "휘파람", "2": "박수", "3": "말소리", "4": "노크"}
print("조용히… 배경소음 측정 중")
# 녹음은 임계값 없이 — 키 누른 뒤 '가장 또렷한 한 조각'(약 0.15초)을 잡아요(작은 소리도 OK).
try: open("sounds.csv").close()
except OSError: open("sounds.csv", "w").write("rms,zcr,crest,label\n")
def counts():
    c = {}
    for ln in open("sounds.csv"):
        ln = ln.strip()
        if ln == "" or ln.startswith("rms"): continue
        nm = ln.split(",")[3]; c[nm] = c.get(nm, 0) + 1
    return c

print("\n=== 소리 모으기 ===")
for k, v in LABELS.items(): print("  %s = %s" % (k, v))
print("  s = 끝내기\n숫자 키를 누른 뒤, 3초 안에 그 소리를 '한 번' 내세요! (큰 소리 아니어도 돼요)")
while True:
    cmd = input("라벨> ").strip()
    if cmd == "s": break
    name = LABELS.get(cmd)
    if not name:
        print("  ↑ 1~4 또는 s"); continue
    print("  ▶ '%s' 소리를 지금 내세요… (3초 동안 들어요)" % name); np.fill((40, 25, 0)); np.write()
    best = None; bestr = -1.0; t0 = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), t0) < 3000:
        rms, zcr, crest = features(grab())
        if rms > bestr: bestr = rms; best = (rms, zcr, crest)
    rms, zcr, crest = best
    open("sounds.csv", "a").write("%.0f,%d,%.2f,%s\n" % (rms, zcr, crest, name))
    flash((0, 40, 0))
    print("  저장! %s (크기=%.0f 높낮이=%d 들쭉=%.2f) | 현재: %s" % (name, rms, zcr, crest, counts()))
    time.sleep(0.3)
print("끝! sounds.csv 저장됨:", counts())
