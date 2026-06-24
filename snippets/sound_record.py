# 소리 인식 ③ — 내가 고른 소리들을 직접 모으기 (혼자, 콘솔 키 라벨링) · 특징 3개
from machine import ADC, Pin
from neopixel import NeoPixel
import time, math

mic = ADC(Pin(27))
WIN_MS = 200       # ★ 한 번에 '0.2초'를 한 덩어리로 (수집 길이가 정확히 정해져요!)
def grab():
    buf = []; t0 = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), t0) < WIN_MS:
        buf.append(mic.read_u16())
    return buf
def features(buf):
    n = len(buf); m = sum(buf) / n; ss = 0.0; zc = 0; peak = 0.0; prev = buf[0] - m
    for v in buf:
        d = v - m; ad = d if d >= 0 else -d; ss += d * d
        if ad > peak: peak = ad
        if (d >= 0) != (prev >= 0): zc += 1
        prev = d
    r = math.sqrt(ss / n); return r, zc, peak / (r + 1e-9)
def level(n=120):
    b = [mic.read_u16() for _ in range(n)]; m = sum(b) / n
    return math.sqrt(sum((v - m) ** 2 for v in b) / n)

TIMING = (280, 515, 515, 745); NUM = 10
np = NeoPixel(Pin(16), NUM, timing=TIMING)
def flash(c, t=0.2): np.fill(c); np.write(); time.sleep(t); np.fill((0, 0, 0)); np.write()

# ★★ 가르칠 소리 이름 — 마음대로 바꾸세요 ★★
LABELS = {"1": "휘파람", "2": "박수", "3": "말소리", "4": "노크"}

# 녹음은 임계값이 필요 없어요 — 키를 누른 뒤 '가장 또렷한 0.2초'를 잡습니다(작은 소리도 OK).
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
    while time.ticks_diff(time.ticks_ms(), t0) < 3000:        # 3초 동안 0.2초 조각들을 보며
        rms, zcr, crest = features(grab())
        if rms > bestr: bestr = rms; best = (rms, zcr, crest)  # 가장 또렷한 조각 채택(임계값 없음!)
    rms, zcr, crest = best
    open("sounds.csv", "a").write("%.0f,%d,%.2f,%s\n" % (rms, zcr, crest, name))
    flash((0, 40, 0))
    print("  저장! %s (크기=%.0f 높낮이=%d 들쭉=%.2f) | 현재: %s" % (name, rms, zcr, crest, counts()))
    time.sleep(0.3)
print("끝! sounds.csv 저장됨:", counts())
