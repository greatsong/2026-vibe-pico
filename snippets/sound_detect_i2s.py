# 소리 인식 ②(I2S) — INMP441로 소리를 잡아 '특징' 세 개 뽑기
# 크기(RMS) · 높낮이(ZCR) · 들쭉날쭉(crest=peak/RMS)
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

print("조용히… 배경소음 측정 중")
for _ in range(8): level()                              # I2S는 켜진 직후 값이 튀어요 → 워밍업으로 버림
bg = sorted(level() for _ in range(25)); base = bg[len(bg) // 2]   # 중앙값(튀는 값에 안 휘둘림)
THRESH = base * 2.5 + 25   # 감지가 안 되면 ↓, 너무 잦으면 ↑
print("준비! 소리를 내보세요.")
while True:
    if level() > THRESH:
        rms, zcr, crest = features(grab())
        print("소리 감지!  크기=%.0f  높낮이=%d  들쭉날쭉=%.2f" % (rms, zcr, crest))
        flash((0, 0, 40)); time.sleep(0.4)
