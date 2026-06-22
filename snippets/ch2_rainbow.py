# 10칸에 무지개 펼치기 (HSV로 색상환 한 바퀴)
from machine import Pin
from neopixel import NeoPixel
import time

TIMING = (280, 515, 515, 745)
NUM = 10
np = NeoPixel(Pin(16), NUM, timing=TIMING)
BRIGHT = 0.3                          # 밝기 0~1 (낮게 권장)

def hsv_to_rgb(h, s, v):
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    if   h < 60:  r, g, b = c, x, 0
    elif h < 120: r, g, b = x, c, 0
    elif h < 180: r, g, b = 0, c, x
    elif h < 240: r, g, b = 0, x, c
    elif h < 300: r, g, b = x, 0, c
    else:         r, g, b = c, 0, x
    return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))

for i in range(NUM):
    hue = i / NUM * 360               # 칸마다 색상 조금씩 다르게
    np[i] = hsv_to_rgb(hue, 1, BRIGHT)
np.write()
