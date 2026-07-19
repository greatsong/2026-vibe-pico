# 공기질 기록 노트 — 센서값을 구글 시트에 1분마다 자동 기록 (설치할 것 없음)
import network, socket, ssl, time, gc
from machine import ADC, Pin
from wifi_config import WIFI_SSID as SSID, WIFI_PASSWORD as PASSWORD

# ↓ 이 따옴표 안 주소 전체를, 구글에서 복사한 웹 앱 주소(.../exec)로 바꾸세요
WEB_APP_URL = "https://script.google.com/macros/s/...여기에_주소_붙여넣기.../exec"
INTERVAL = 60                 # 몇 초마다 보낼지 (60 = 1분)
gas = ADC(Pin(26))           # 가스센서 (그로브 A0)

def read_avg(n=20):           # 3장에서 배운 대로 — 여러 번 읽어 평균(출렁임 줄이기)
    return sum(gas.read_u16() for _ in range(n)) // n

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Wi-Fi 연결 중", end="")
    t = 20
    while not wlan.isconnected() and t > 0:
        print(".", end=""); time.sleep(0.5); t -= 1
    print("\nOK" if wlan.isconnected() else "\n실패")
    return wlan.isconnected()

def https_get(url):           # 전체 주소(https://...)를 받아 요청
    host, _, path = url[8:].partition("/")
    gc.collect()
    s = socket.socket()
    try:                      # 도중에 실패해도 소켓은 꼭 닫는다 (밤새 돌려도 안 새게)
        s.connect(socket.getaddrinfo(host, 443)[0][-1])
        try:
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ctx.verify_mode = ssl.CERT_NONE
            s = ctx.wrap_socket(s, server_hostname=host)
        except AttributeError:
            s = ssl.wrap_socket(s, server_hostname=host)
        s.write(("GET /%s HTTP/1.0\r\nHost: %s\r\nConnection: close\r\n\r\n"
                 % (path, host)).encode())
        buf = b""
        while True:
            c = s.read(512)
            if not c:
                break
            buf += c
        return buf
    finally:
        s.close()

def send(value):
    resp = https_get(WEB_APP_URL + "?value=" + str(value))
    head = resp.split(b"\r\n\r\n", 1)[0]
    if b" 302 " in head or b" 301 " in head:     # 구글이 다른 주소로 넘기면 따라가기
        for line in head.split(b"\r\n"):
            if line.lower().startswith(b"location:"):
                https_get(line.split(b":", 1)[1].strip().decode())
                break

if connect_wifi():
    n = 0
    while True:
        v = read_avg()
        try:
            send(v)
            n += 1
            print("시트로 보냄:", v, "(누적 %d줄)" % n)
        except Exception as e:
            print("실패(잠시 뒤 다시 시도):", e)
            if not network.WLAN(network.STA_IF).isconnected():
                connect_wifi()          # 밤새 기록 중 와이파이가 끊겨도 다시 붙는다
        time.sleep(INTERVAL)
