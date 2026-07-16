# 동작 인식 ① — IMU(LSM6DS3) 값 읽기 (외부 라이브러리 없이 복사-실행)
# Grove 6축 가속도·자이로를 쉴드의 UART1 포트(GP4/GP5)에 꽂으세요. (I2C0/I2C1 포트 아님!)
from machine import I2C, Pin
import time, struct

# ── LSM6DS3 레지스터 (ST 데이터시트) ──
WHO_AM_I, CTRL1_XL, CTRL2_G = 0x0F, 0x10, 0x11
OUTX_L_G, OUTX_L_XL = 0x22, 0x28          # 자이로/가속도 출력(각 6바이트: X,Y,Z)

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)   # 쉴드 UART1 포트의 GP4/GP5를 I2C로 사용

# 주소 자동 찾기 (그로브 모듈은 0x6A 또는 0x6B)
ADDR = None
for a in (0x6A, 0x6B):
    try:
        if i2c.readfrom_mem(a, WHO_AM_I, 1)[0] in (0x69, 0x6A):   # LSM6DS3 / TR-C
            ADDR = a
            print("IMU 찾음! 주소=0x%02X" % a)
            break
    except OSError:
        pass
if ADDR is None:
    raise RuntimeError("IMU 못 찾음 — UART1 포트(GP4/GP5)에 꽂았는지 확인")

# ★ 빠른 플립에 대비해 '최대 범위'로 (포화 방지!) ★
i2c.writeto_mem(ADDR, CTRL1_XL, bytes([0x64]))   # 가속도: 416Hz, ±16g
i2c.writeto_mem(ADDR, CTRL2_G,  bytes([0x6C]))   # 자이로 : 416Hz, ±2000°/s
time.sleep(0.1)

def read3(reg):                            # 6바이트 → int16 3개(리틀엔디언·2의보수)
    return struct.unpack("<hhh", i2c.readfrom_mem(ADDR, reg, 6))

A_SCALE, G_SCALE = 0.488/1000, 70.0/1000   # 원시값 → g / °/s

while True:
    ax, ay, az = read3(OUTX_L_XL)
    gx, gy, gz = read3(OUTX_L_G)
    print("a(g): %+.2f %+.2f %+.2f  |  회전(°/s): %+6.0f %+6.0f %+6.0f" %
          (ax*A_SCALE, ay*A_SCALE, az*A_SCALE, gx*G_SCALE, gy*G_SCALE, gz*G_SCALE))
    time.sleep(0.1)
