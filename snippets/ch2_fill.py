# 전체를 한 색으로 — fill 함수 만들기
from machine import Pin
from neopixel import NeoPixel
import time

TIMING = (280, 515, 515, 745)
NUM = 10
np = NeoPixel(Pin(16), NUM, timing=TIMING)

def fill(color):
    for i in range(NUM):
        np[i] = color
    np.write()

fill((0, 30, 0))     # 전체 초록
time.sleep(1)
fill((0, 0, 30))     # 전체 파랑
time.sleep(1)
fill((0, 0, 0))      # 전체 끄기
