# 소리 인식 ①(I2S) — INMP441 마이크 값 읽기 (음질 업그레이드 버전)
# 점퍼 연결: VDD→3.3V(⚠5V 금지), GND→GND, SCK→GP18, WS→GP19, SD→GP20, L/R→GND
from machine import I2S, Pin
import struct, math, time

audio = I2S(0, sck=Pin(18), ws=Pin(19), sd=Pin(20),
            mode=I2S.RX, bits=32, format=I2S.MONO, rate=16000, ibuf=40000)
buf = bytearray(512 * 4)

def level():                       # 짧게 512표본의 '소리 크기'(RMS)
    audio.readinto(buf)
    v = [x >> 16 for x in struct.unpack("<512i", buf)]   # 32→16비트로 줄여 보기 쉽게
    m = sum(v) / 512
    return math.sqrt(sum((x - m) ** 2 for x in v) / 512)

print("준비됐어요! 휘파람·박수·말소리를 내보세요. (Thonny 플로터 추천)")
while True:
    print(level())
    time.sleep(0.05)
