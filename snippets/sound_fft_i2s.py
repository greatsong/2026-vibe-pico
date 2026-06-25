# 소리 인식 ⑤ (심화 · INMP441) — FFT 주파수밴드 특징으로 더 똑똑하게
# 8개 주파수 대역의 에너지를 특징으로 쓰면 '음색(timbre)'까지 구분해요.
# ulab 없이 Goertzel 알고리즘으로 각 대역 에너지를 직접 계산합니다.
# 한 번 실행에서 [수집] → 'go' 입력 → [예측] 흐름으로 끝납니다.
from machine import I2S, Pin
from neopixel import NeoPixel
import struct, time, math

audio = I2S(0, sck=Pin(18), ws=Pin(19), sd=Pin(20),
            mode=I2S.RX, bits=32, format=I2S.MONO, rate=16000, ibuf=40000)
N = 1600; raw = bytearray(N * 4)
def grab():
    audio.readinto(raw)
    return [x >> 16 for x in struct.unpack("<%di" % N, raw)]

BANDS = [200, 350, 600, 1000, 1700, 2800, 4500, 7000]   # 8개 대역 중심 주파수(Hz)
def goertzel(x, f):                 # 특정 주파수 f의 에너지(파워)
    k = 2 * math.cos(2 * math.pi * f / 16000); s1 = 0.0; s2 = 0.0
    for v in x:
        s0 = v + k * s1 - s2; s2 = s1; s1 = s0
    return s1 * s1 + s2 * s2 - k * s1 * s2
def features(x):                    # 음량과 무관한 '스펙트럼 모양' 8개
    m = sum(x) / len(x); x = [v - m for v in x]
    e = [max(goertzel(x, f), 0.0) for f in BANDS]; tot = sum(e) + 1e-9
    return [math.log(ei / tot + 1e-6) for ei in e]

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

# ★ 음색이 다른 소리일수록 효과 큼 (예: 휘파람 vs 쉬익, 모음 '아' vs '이') ★
LABELS = {"1": "휘파람", "2": "말소리", "3": "노크", "4": "박수"}
D = len(BANDS)
print("조용히… 배경소음 측정 중")
for _ in range(8): level()                              # I2S는 켜진 직후 값이 튀어요 → 워밍업으로 버림
bg = sorted(level() for _ in range(25)); base = bg[len(bg) // 2]   # 중앙값(튀는 값에 안 휘둘림)
THRESH = base * 2.5 + 25   # 예측이 안 뜨면 ↓, 너무 잦으면 ↑

data = []
print("\n[수집] 숫자키 누르고 소리내기 · go=예측 시작")
for k, v in LABELS.items(): print("  %s = %s" % (k, v))
while True:
    cmd = input("라벨(go=예측)> ").strip()
    if cmd == "go": break
    nm = LABELS.get(cmd)
    if not nm: continue
    print("  ▶ '%s' 소리를 지금 내세요… (3초)" % nm)
    best = None; bestr = -1.0; t0 = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), t0) < 3000:        # 3초 중 '가장 또렷한' 조각
        x = grab(); mm = sum(x) / len(x); rr = sum((v - mm) ** 2 for v in x)
        if rr > bestr: bestr = rr; best = features(x)
    data.append((best, nm)); print("  저장 (총 %d개)" % len(data))

names = sorted(set(d[1] for d in data)); cidx = {n: i for i, n in enumerate(names)}
mins = [min(d[0][i] for d in data) for i in range(D)]
maxs = [max(d[0][i] for d in data) for i in range(D)]
def norm(f): return [(f[i] - mins[i]) / (maxs[i] - mins[i] + 1e-9) for i in range(D)]
ex = [(norm(d[0]), d[1]) for d in data]
def predict(f, k=5):
    q = norm(f)
    def d2(e): return sum((e[0][i] - q[i]) ** 2 for i in range(D))
    near = sorted(ex, key=d2)[:k]; vote = {}
    for e in near: vote[e[1]] = vote.get(e[1], 0) + 1.0 / (d2(e) + 1e-6)
    b = max(vote, key=vote.get); return b, vote[b] / sum(vote.values())

print("\n[예측] 소리를 내보세요.")
while True:
    if level() > THRESH:
        nm, conf = predict(features(grab()))
        print("이건… %s!  (확신 %d%%)" % (nm, conf * 100))
        show(cidx[nm], max(1, int(conf * NUM))); time.sleep(1.0); show(0, 0)
