# 동작 인식 ② — '플립(던지는 동작)'을 감지하고 특징을 뽑기
# 큰 회전이 일어나면 한 동작으로 잡아, 회전피크·가속피크·지속시간을 계산합니다.
from machine import I2C, Pin
from neopixel import NeoPixel
import time, struct, math

# ── IMU 준비 (코드①과 동일) ──
WHO_AM_I, CTRL1_XL, CTRL2_G, OUTX_L_G, OUTX_L_XL = 0x0F, 0x10, 0x11, 0x22, 0x28
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
ADDR = None
for a in (0x6A, 0x6B):
    try:
        if i2c.readfrom_mem(a, WHO_AM_I, 1)[0] in (0x69, 0x6A):
            ADDR = a; break
    except OSError:
        pass
if ADDR is None:
    raise RuntimeError("IMU 못 찾음 — UART1 포트(GP4/GP5) 확인")
i2c.writeto_mem(ADDR, CTRL1_XL, bytes([0x64]))   # ±16g
i2c.writeto_mem(ADDR, CTRL2_G,  bytes([0x6C]))   # ±2000°/s
time.sleep(0.1)
A_SCALE, G_SCALE = 0.488/1000, 70.0/1000

def read():                                # 가속도·회전 '크기'(magnitude)
    a = struct.unpack("<hhh", i2c.readfrom_mem(ADDR, OUTX_L_XL, 6))
    g = struct.unpack("<hhh", i2c.readfrom_mem(ADDR, OUTX_L_G, 6))
    am = math.sqrt(sum((v*A_SCALE)**2 for v in a))
    gm = math.sqrt(sum((v*G_SCALE)**2 for v in g))
    return am, gm

# ── LED ──
TIMING = (280, 515, 515, 745); NUM = 10
np = NeoPixel(Pin(16), NUM, timing=TIMING)
def flash(color, t=0.25):
    np.fill(color); np.write(); time.sleep(t); np.fill((0,0,0)); np.write()

# ── 플립 감지 ──
START_G = 300        # 회전속도가 이 값(°/s)을 넘으면 '동작 시작' (세기에 맞게 조정)
WINDOW  = 0.4        # 동작을 0.4초 동안 관찰
print("준비됐어요! 손에 쥐고 플립 동작을 해보세요.")

while True:
    am, gm = read()
    if gm > START_G:                       # 동작 시작 감지!
        peak_a, peak_g, n, t0 = am, gm, 1, time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), t0) < WINDOW*1000:
            am, gm = read()
            peak_a = max(peak_a, am); peak_g = max(peak_g, gm); n += 1
        print("플립 감지! 회전피크=%.0f°/s  가속피크=%.1fg  표본=%d" % (peak_g, peak_a, n))
        flash((0, 0, 40))                  # 파랑 점멸 = 감지 성공
        time.sleep(0.4)                    # 쿨다운(중복 감지 방지)
    time.sleep(0.005)
