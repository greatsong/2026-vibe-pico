# 동작 인식 ②-MPU : 플립 감지 + 특징 추출 (MPU6050 버전)
# MPU6050(GY-521)을 쉴드 UART1 포트(GP4/GP5)에 변환 케이블로 연결, 전원 스위치 3.3V!
from machine import I2C, Pin
from neopixel import NeoPixel
import time, struct, math

# ── MPU6050 준비 ──
ADDR = 0x68          # AD0=HIGH면 0x69
PWR_MGMT_1, ACCEL_CONFIG, GYRO_CONFIG = 0x6B, 0x1C, 0x1B
ACCEL_XOUT_H, GYRO_XOUT_H = 0x3B, 0x43
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
if ADDR not in i2c.scan():
    raise RuntimeError("MPU6050 못 찾음 — 배선·전원 3.3V 확인 (AD0=H면 ADDR=0x69)")
i2c.writeto_mem(ADDR, PWR_MGMT_1,   bytes([0x00]))   # 깨우기(슬립 해제)
time.sleep(0.1)
i2c.writeto_mem(ADDR, ACCEL_CONFIG, bytes([0x18]))   # ±16g
i2c.writeto_mem(ADDR, GYRO_CONFIG,  bytes([0x18]))   # ±2000°/s
time.sleep(0.05)
A_SCALE, G_SCALE = 1/2048, 1/16.4

def read():                                # 가속도·회전 '크기'(magnitude)
    a = struct.unpack(">hhh", i2c.readfrom_mem(ADDR, ACCEL_XOUT_H, 6))   # 빅엔디언
    g = struct.unpack(">hhh", i2c.readfrom_mem(ADDR, GYRO_XOUT_H, 6))
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
