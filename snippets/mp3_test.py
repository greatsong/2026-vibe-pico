# MP3 출력 ① — Grove MP3 v4.0 (WT2605CX) 모듈 단독 테스트
# 피코는 "몇 번 곡 틀어/볼륨 얼마로" 같은 '명령'만 보냅니다. 재생은 모듈이 해요.
# ⚠ v2.0(KT403A)과 명령이 '완전히' 다릅니다! v4.0은 7E..EF 바이너리가 아니라
#    'AT+' 텍스트 명령을 \r\n 으로 끝맺어 115200 baud로 보냅니다.
from machine import UART, Pin
import time

# Grove 케이블 → 쉴드의 UART 포트. 피코 TX=GP0, RX=GP1
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))   # ★ 115200! (v2.0은 9600)
time.sleep(1.0)                                          # 모듈 부팅 대기

def at(cmd, wait=0.4):
    uart.write((cmd + "\r\n").encode())                  # AT 텍스트 + 줄바꿈
    print(">", cmd)
    time.sleep(wait)
    if uart.any():
        print("  <", uart.read())                        # 모듈 응답(보통 'OK')

at("AT+VOL=22")                                          # 볼륨 0~31 (시끄러우면 낮추기)
print("1번 곡(0001.mp3) 재생…")
at("AT+PLAY=sd0,1")                                      # SD카드 루트의 1번 곡
time.sleep(3)
print("2번 곡(0002.mp3) 재생…")
at("AT+PLAY=sd0,2")
time.sleep(3)
at("AT+STOP")
print("끝! 소리가 났나요?")
