# WS2813 LED 10개 — 한 칸 켜기
from machine import Pin
from neopixel import NeoPixel
import time

TIMING = (280, 515, 515, 745)        # ★ WS2813 전용 타이밍 (없으면 색이 깨집니다!)
NUM = 10
np = NeoPixel(Pin(16), NUM, timing=TIMING)   # 그로브 D16 = GP16

np[0] = (40, 0, 0)                   # 0번 칸 빨강 (밝기는 낮게)
np.write()                           # write()를 해야 실제로 켜집니다
time.sleep(2)

np[0] = (0, 0, 0)                    # 끄기
np.write()
