# 반복해서 읽기 — Thonny의 '플로터'로 그래프를 볼 수 있어요
from machine import ADC, Pin
import time

gas_sensor = ADC(Pin(26))
while True:
    print(gas_sensor.read_u16())
    time.sleep(0.5)
