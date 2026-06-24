# 소리 인식 ① — 마이크 값 읽기 (Grove 아날로그 마이크)
# 마이크를 그로브 쉴드의 'A1' 포트에 톡 꽂고 실행하세요. (A0은 가스센서가 쓰니 A1!)
# 휘파람·박수·말소리를 내면 숫자가 출렁여요. Thonny의 '플로터'를 켜면 그래프로 보입니다.
from machine import ADC, Pin
import time, math

mic = ADC(Pin(27))                 # A1 그로브 포트 = GP27

def level(n=300):                  # 짧게 n개를 재서 '소리 크기'(RMS)를 구함
    b = [mic.read_u16() for _ in range(n)]
    m = sum(b) / n                 # 평균(=무음일 때의 가운데 값)을 빼고
    return math.sqrt(sum((v - m) ** 2 for v in b) / n)   # 출렁임의 크기

print("준비됐어요! 휘파람·박수·말소리를 내보세요. (Thonny 플로터 추천)")
while True:
    print(level())
    time.sleep(0.05)
