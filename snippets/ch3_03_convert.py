# 원시값을 전압과 비율로 바꿔 보기
from machine import ADC, Pin
import time

gas_sensor = ADC(Pin(26))
while True:
    value = gas_sensor.read_u16()
    voltage = value / 65535 * 3.3
    percent = value / 65535 * 100
    print("ADC: %5d  |  %.2fV  |  %.1f%%" % (value, voltage, percent))
    time.sleep(0.5)
