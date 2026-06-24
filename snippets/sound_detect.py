# 소리 인식 ② — 소리를 한 덩어리로 잡아 '특징' 세 개 뽑기
# 크기(RMS)=얼마나 큰가 · 높낮이(ZCR)=얼마나 높은가 · 들쭉날쭉(crest)=톡 치는 소리인가
from machine import ADC, Pin
from neopixel import NeoPixel
import time, math

mic = ADC(Pin(27))
WIN_MS = 200       # 한 번에 '0.2초'를 한 덩어리로 (녹음·예측과 동일한 길이!)
def grab():
    buf = []; t0 = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), t0) < WIN_MS:
        buf.append(mic.read_u16())
    return buf

def features(buf):                 # 한 조각 → (크기, 높낮이, 들쭉날쭉)
    n = len(buf); m = sum(buf) / n
    ss = 0.0; zc = 0; peak = 0.0; prev = buf[0] - m
    for v in buf:
        d = v - m; ad = d if d >= 0 else -d
        ss += d * d
        if ad > peak: peak = ad          # 가장 큰 순간값
        if (d >= 0) != (prev >= 0): zc += 1
        prev = d
    rms = math.sqrt(ss / n)
    return rms, zc, peak / (rms + 1e-9)  # 들쭉날쭉 = 최댓값 ÷ 평균크기

def level(n=120):
    b = [mic.read_u16() for _ in range(n)]; m = sum(b) / n
    return math.sqrt(sum((v - m) ** 2 for v in b) / n)

TIMING = (280, 515, 515, 745); NUM = 10
np = NeoPixel(Pin(16), NUM, timing=TIMING)
def flash(c, t=0.2): np.fill(c); np.write(); time.sleep(t); np.fill((0, 0, 0)); np.write()

print("조용히 해주세요… 배경소음 측정 중")
base = max(level() for _ in range(20)); THRESH = base * 2   # 민감하게(작은 소리도)
print("준비! 소리를 내보세요. (임계값=%.0f)" % THRESH)
while True:
    if level(120) > THRESH:
        rms, zcr, crest = features(grab())
        print("소리 감지!  크기=%.0f  높낮이=%d  들쭉날쭉=%.2f" % (rms, zcr, crest))
        flash((0, 0, 40)); time.sleep(0.4)
    time.sleep(0.005)
