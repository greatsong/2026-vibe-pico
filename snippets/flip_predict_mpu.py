# 동작 인식 ④-MPU : k-NN으로 '성공/실패' 예측 (MPU6050 버전)
# flips.csv(짝 활동으로 모은 데이터)를 '모델'로 삼아 새 플립의 결과를 예측합니다.
import time, struct, math
from machine import I2C, Pin
from neopixel import NeoPixel

# ── MPU6050 준비 ──
ADDR = 0x68          # AD0=HIGH면 0x69
PWR_MGMT_1, ACCEL_CONFIG, GYRO_CONFIG = 0x6B, 0x1C, 0x1B
ACCEL_XOUT_H, GYRO_XOUT_H = 0x3B, 0x43
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
if ADDR not in i2c.scan():
    raise RuntimeError("MPU6050 못 찾음 — 배선·전원 3.3V 확인 (AD0=H면 ADDR=0x69)")
i2c.writeto_mem(ADDR, PWR_MGMT_1,   bytes([0x00]))   # 깨우기
time.sleep(0.1)
i2c.writeto_mem(ADDR, ACCEL_CONFIG, bytes([0x18]))   # ±16g
i2c.writeto_mem(ADDR, GYRO_CONFIG,  bytes([0x18]))   # ±2000°/s
time.sleep(0.05)
A_SCALE, G_SCALE = 1/2048, 1/16.4
def read():
    a = struct.unpack(">hhh", i2c.readfrom_mem(ADDR, ACCEL_XOUT_H, 6))
    g = struct.unpack(">hhh", i2c.readfrom_mem(ADDR, GYRO_XOUT_H, 6))
    return (math.sqrt(sum((v*A_SCALE)**2 for v in a)),
            math.sqrt(sum((v*G_SCALE)**2 for v in g)))

# ── LED ──
TIMING = (280,515,515,745); NUM = 10
np = NeoPixel(Pin(16), NUM, timing=TIMING)
def show(color, level):
    for i in range(NUM): np[i] = color if i < level else (0,0,0)
    np.write()

# ── 1) flips.csv 불러오기 = '학습'(예시를 기억) ──
rows = []
for ln in open("flips.csv"):
    ln = ln.strip()
    if ln == "" or ln.startswith("peak_g"): continue
    pg, pa, lab = ln.split(",")
    rows.append((float(pg), float(pa), int(lab)))
ns = sum(r[2] == 1 for r in rows); nf = sum(r[2] == 0 for r in rows)
print("예시 %d개 (성공 %d · 실패 %d)" % (len(rows), ns, nf))
if ns < 5 or nf < 5:
    print("⚠️ 데이터가 부족해요. ③-MPU로 성공·실패 각각 10개+ 모으세요.")

# ── 2) 정규화 준비 (★ 두 특징을 0~1로, 공평하게) ──
g_min = min(r[0] for r in rows); g_max = max(r[0] for r in rows)
a_min = min(r[1] for r in rows); a_max = max(r[1] for r in rows)
def norm(pg, pa):
    ng = (pg - g_min) / (g_max - g_min + 1e-9)
    na = (pa - a_min) / (a_max - a_min + 1e-9)
    return ng, na
examples = [(*norm(r[0], r[1]), r[2]) for r in rows]   # (정규화회전, 정규화가속, 라벨)

# ── 3) k-NN 예측 ──
def predict(pg, pa, k=5):
    ng, na = norm(pg, pa)
    near = sorted(examples, key=lambda e: (e[0]-ng)**2 + (e[1]-na)**2)[:k]
    win = sum(e[2] for e in near)          # 성공(1)에 투표한 이웃 수
    label = 1 if win > k/2 else 0
    conf = max(win, k-win) / k             # 다수쪽 비율 = 확신도
    return label, conf

# ── 4) 새 플립을 기다렸다 예측 ──
START_G = 300
print("준비! 플립하면 예측합니다.")
while True:
    am, gm = read()
    if gm > START_G:                       # 플립 감지 → 0.4초 관찰
        pg, pa, t0 = gm, am, time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), t0) < 400:
            am, gm = read(); pg = max(pg, gm); pa = max(pa, am)
        label, conf = predict(pg, pa)
        bars = max(1, int(conf*NUM))
        if label == 1:
            print("예측: 성공 ✅  확신 %d%%  (회전 %.0f 가속 %.1f)" % (conf*100, pg, pa))
            show((0,40,0), bars)
        else:
            print("예측: 실패 ❌  확신 %d%%  (회전 %.0f 가속 %.1f)" % (conf*100, pg, pa))
            show((40,0,0), bars)
        time.sleep(1.0); show((0,0,0), 0)
