# LED로 감정 표현하기 — 색과 움직임으로 기분을 나타내요
# 버튼이 없으니, 맨 아래 MOOD 한 줄만 바꿔서 내 기분을 골라요.
from machine import Pin
from neopixel import NeoPixel
import time, random

TIMING = (280, 515, 515, 745)   # WS2813 필수!
NUM = 10
np = NeoPixel(Pin(16), NUM, timing=TIMING)

def fill(c):
    for i in range(NUM):
        np[i] = c
    np.write()

def pulse(c, times=3):          # 숨쉬듯 밝아졌다 어두워지기
    for _ in range(times):
        for b in list(range(0, 60, 4)) + list(range(60, 0, -4)):
            fill((c[0] * b // 60, c[1] * b // 60, c[2] * b // 60))
            time.sleep(0.02)

def blink(c, times=6):          # 깜빡깜빡
    for _ in range(times):
        fill(c); time.sleep(0.15)
        fill((0, 0, 0)); time.sleep(0.15)

def sparkle(c, times=40):       # 반짝반짝 (랜덤 칸)
    for _ in range(times):
        fill((0, 0, 0))
        np[random.randint(0, NUM - 1)] = c
        np.write()
        time.sleep(0.05)

# 감정 프리셋: 색 + 움직임을 골라 함수로 묶었어요
def joy():     pulse((50, 40, 0))     # 기쁨: 따뜻한 노랑, 두근두근
def calm():    pulse((0, 20, 40))     # 평온: 파랑, 천천히 숨쉬기
def anger():   blink((60, 0, 0))      # 화남: 빨강 깜빡
def excited(): sparkle((0, 50, 30))   # 신남: 청록 반짝

MOODS = {"기쁨": joy, "평온": calm, "화남": anger, "신남": excited}

MOOD = "기쁨"        # ← 여기만 바꿔서 내 기분을 골라요! (기쁨/평온/화남/신남)

while True:
    MOODS[MOOD]()
    time.sleep(0.5)
