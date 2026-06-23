# MQ-2 공기질을 LED 10칸으로 — 폰 없이 흘끗 보기
# 앞 장(웹 대시보드)에서 읽던 센서값을, 2장에서 배운 LED 게이지로 표현합니다.
from machine import ADC, Pin
from neopixel import NeoPixel
import time

TIMING = (280, 515, 515, 745)   # WS2813 필수! 없으면 색 깨짐
NUM = 10
np  = NeoPixel(Pin(16), NUM, timing=TIMING)   # LED → D16
gas = ADC(Pin(26))                            # MQ-2 → A0

# 앞 장 대시보드와 같은 임계값 (우리 교실에 맞게 조정하세요)
SAFE_MAX  = 20000   # 이 아래 = 안전(초록)
WARN_MAX  = 45000   # 이 아래 = 주의(노랑), 넘으면 위험(빨강)
GAUGE_MAX = 60000   # 게이지가 꽉 차는 기준값

def read_avg(n=10):                 # 흔들리는 값 → 이동평균으로 안정화
    total = 0
    for _ in range(n):
        total += gas.read_u16()
        time.sleep(0.02)
    return total // n

def color_of(v):
    if v < SAFE_MAX:
        return (0, 40, 0)           # 초록 = 안전
    if v < WARN_MAX:
        return (45, 30, 0)          # 노랑 = 주의
    return (60, 0, 0)               # 빨강 = 위험

def show(v):
    level = min(NUM, v * NUM // GAUGE_MAX)   # 값 → 0~10칸
    c = color_of(v)
    for i in range(NUM):
        np[i] = c if i < level else (0, 0, 0)
    np.write()

while True:
    v = read_avg()
    show(v)
    print("ADC:", v)
    if v >= WARN_MAX:               # 위험하면 빠르게 3번 깜빡여 눈에 띄게
        for _ in range(3):
            np.fill((0, 0, 0)); np.write(); time.sleep(0.12)   # 껐다
            show(v); time.sleep(0.12)                          # 켰다
    else:
        time.sleep(0.6)
