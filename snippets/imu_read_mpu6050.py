# 동작 인식 ①-MPU : MPU6050(GY-521)을 그로브 쉴드로 연결해 값 읽기 (외부 라이브러리 없이)
#
# ▶ 연결: 그로브 I2C 포트 ↔ MPU6050  (그로브–점퍼(암) 변환 케이블 필요)
#     노랑(SCL) → MPU6050  SCL
#     흰색(SDA) → MPU6050  SDA
#     빨강(VCC) → MPU6050  VCC
#     검정(GND) → MPU6050  GND
#   ※ 쉴드 전원 스위치는 반드시 3.3V! (피코 핀은 5V를 못 견뎌요)
from machine import I2C, Pin
import time, struct

ADDR         = 0x68    # MPU6050 기본 주소 (AD0=LOW). AD0를 VCC에 연결하면 0x69
WHO_AM_I     = 0x75
PWR_MGMT_1   = 0x6B
ACCEL_CONFIG = 0x1C
GYRO_CONFIG  = 0x1B
ACCEL_XOUT_H = 0x3B    # 가속도 출력 시작(6바이트: X,Y,Z)
GYRO_XOUT_H  = 0x43    # 자이로 출력 시작(6바이트: X,Y,Z)

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)   # 그로브 I2C 포트(SDA=GP4, SCL=GP5)

# 연결 확인
if ADDR not in i2c.scan():
    raise RuntimeError("MPU6050 못 찾음 — 배선(SCL/SDA/VCC/GND)과 전원 3.3V 스위치 확인")
print("MPU6050 찾음! WHO_AM_I=0x%02X" % i2c.readfrom_mem(ADDR, WHO_AM_I, 1)[0])

# 1) 잠에서 깨우기 — 전원을 켜면 '슬립' 상태라 이 줄이 꼭 필요해요!
i2c.writeto_mem(ADDR, PWR_MGMT_1, bytes([0x00]))
time.sleep(0.1)
# 2) ★ 빠른 플립용 '최대 범위' (포화 방지)
i2c.writeto_mem(ADDR, ACCEL_CONFIG, bytes([0x18]))   # ±16g     (AFS_SEL=3)
i2c.writeto_mem(ADDR, GYRO_CONFIG,  bytes([0x18]))   # ±2000°/s (FS_SEL=3)
time.sleep(0.05)

def read3(reg):                        # 6바이트 → int16 3개 (★MPU6050은 빅엔디언: >hhh)
    return struct.unpack(">hhh", i2c.readfrom_mem(ADDR, reg, 6))

A_SCALE = 1/2048      # ±16g  → 2048 LSB/g
G_SCALE = 1/16.4      # ±2000 → 16.4 LSB/(°/s)

while True:
    ax, ay, az = read3(ACCEL_XOUT_H)
    gx, gy, gz = read3(GYRO_XOUT_H)
    print("a(g): %+.2f %+.2f %+.2f  |  회전(°/s): %+6.0f %+6.0f %+6.0f" %
          (ax*A_SCALE, ay*A_SCALE, az*A_SCALE, gx*G_SCALE, gy*G_SCALE, gz*G_SCALE))
    time.sleep(0.1)
