# 게이지처럼 켜진 칸 수 조절하기 (뒤의 공기질·날씨 LED의 기초!)
from machine import Pin
from neopixel import NeoPixel
import time

TIMING = (280, 515, 515, 745)
NUM = 10
np = NeoPixel(Pin(16), NUM, timing=TIMING)

def gauge(level, on_color=(0, 30, 0)):
    # level: 0~10, 켤 칸 수
    for i in range(NUM):
        np[i] = on_color if i < level else (0, 0, 0)
    np.write()

for n in range(0, NUM + 1):           # 0칸 → 10칸 차오르기
    gauge(n)
    time.sleep(0.2)
time.sleep(1)
gauge(0)                              # 모두 끄기
