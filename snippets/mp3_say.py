# MP3 출력 ② — k-NN이 알아맞힌 소리의 '주인공'을 목소리로 (Grove MP3 v4.0 · WT2605CX)
# 듣기(마이크) → 생각(k-NN) → 말하기(MP3).  ⚠ v4.0은 AT 명령 / 115200 baud!
# ※ 소리 분류 챕터에서 만든 sounds.csv(rms,zcr,crest,label)가 피코에 들어 있어야 해요.
import time, math
from machine import ADC, Pin, UART
from neopixel import NeoPixel

# ── 마이크 (아날로그 A1) — 소리 챕터와 똑같이 '듣기' · 특징 3개 ──
mic = ADC(Pin(27))
WIN_MS = 200       # 한 번에 '0.2초'를 한 덩어리로 (소리 챕터와 동일한 길이!)
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

# ── MP3 출력기 (Grove MP3 v4.0 · WT2605CX) — '말하기' : AT 명령 ──
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))   # ★ v4.0 = 115200
time.sleep(1.0)                                          # 모듈 부팅 대기
def at(s):
    uart.write((s + "\r\n").encode()); time.sleep(0.1)
at("AT+VOL=22")                                          # 볼륨 0~31

# ── ★ 라벨 → 트랙 번호 (룩업 테이블) ──
# SD(FAT32)에 0001.mp3="휘파람이에요", 0002.mp3="박수네요" … 순서대로 넣어두세요.
TRACK = {"휘파람": 1, "박수": 2, "말소리": 3, "노크": 4}

# ── LED (소리마다 색) ──
TIMING = (280, 515, 515, 745); NUM = 10
np = NeoPixel(Pin(16), NUM, timing=TIMING)
PALETTE = [(40, 0, 0), (0, 40, 0), (0, 0, 40), (40, 40, 0), (40, 0, 40), (0, 40, 40)]
def paint(c, lv):
    for i in range(NUM): np[i] = c if i < lv else (0, 0, 0)
    np.write()

# ── sounds.csv 불러오기 + 정규화 + k-NN (소리 챕터와 동일 · 특징 3개) ──
rows = []
for ln in open("sounds.csv"):
    ln = ln.strip()
    if ln == "" or ln.startswith("rms"): continue
    r, z, c, nm = ln.split(","); rows.append((float(r), float(z), float(c), nm))
names = sorted(set(r[3] for r in rows)); cidx = {nm: i for i, nm in enumerate(names)}
mins = [min(r[i] for r in rows) for i in range(3)]
maxs = [max(r[i] for r in rows) for i in range(3)]
def norm(v): return [(v[i] - mins[i]) / (maxs[i] - mins[i] + 1e-9) for i in range(3)]
ex = [(norm(r[:3]), r[3]) for r in rows]
def predict(feat, k=5):
    q = norm(feat)
    def d2(e): return sum((e[0][i] - q[i]) ** 2 for i in range(3))
    near = sorted(ex, key=d2)[:k]; vote = {}
    for e in near: vote[e[1]] = vote.get(e[1], 0) + 1
    b = max(vote, key=vote.get); return b, vote[b] / sum(vote.values())

# ── 배경소음 → 임계값 ──
print("조용히… 배경소음 측정 중")
base = max(level() for _ in range(20)); THRESH = base * 2   # 민감하게(작은 소리도)

# ── ★ '말하기' — 자기 소리 되먹임 방지(말하는 동안 + 잔향까지 귀 닫기) ──
SPEAK_SEC = 2.5      # 멘트 길이만큼. 음성이 잘리면 늘리세요.
def say(track):
    at("AT+PLAY=sd0,%d" % track)         # ← 그 소리의 '이름'을 목소리로!
    time.sleep(SPEAK_SEC)
    t0 = time.ticks_ms()
    while level(120) > THRESH and time.ticks_diff(time.ticks_ms(), t0) < 2000:
        time.sleep(0.05)

CONF_MIN = 0.6       # 확신이 이보다 낮으면 '모르겠어요' → 침묵
print("준비! 소리를 내면 누구인지 말해줄게요. (멈추려면 Ctrl+C)")
while True:
    if level(120) > THRESH:
        feat = features(grab()); name, conf = predict(feat)
        if conf >= CONF_MIN and name in TRACK:
            print("이건… %s!  (확신 %d%%)" % (name, conf * 100))
            paint(PALETTE[cidx[name] % len(PALETTE)], max(1, int(conf * NUM)))
            say(TRACK[name])
        else:
            print("음… 잘 모르겠어요 (확신 %d%%) — 조용히 있을게요" % (conf * 100))
            paint((8, 8, 8), NUM); time.sleep(0.8)
        paint((0, 0, 0), 0)
    time.sleep(0.005)
