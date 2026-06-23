# MQ-2 가스센서 값 한 번 읽기 (그로브 A0 = GP26 = ADC0)
from machine import ADC, Pin

gas_sensor = ADC(Pin(26))
print(gas_sensor.read_u16())     # 0 ~ 65535
