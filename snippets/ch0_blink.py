from machine import Pin    # 핀 제어 도구
import time               # 시간(대기) 도구

led = Pin("LED", Pin.OUT)  # 피코 보드 위의 작은 LED

while True:               # 아래를 계속 반복
    led.value(1)          # 켜기
    time.sleep(0.5)       # 0.5초 대기
    led.value(0)          # 끄기
    time.sleep(0.5)
