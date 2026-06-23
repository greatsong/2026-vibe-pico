# 센서값을 구글 시트에 보내기 (설치할 것 없음)
import network, socket, ssl, time, gc
from machine import ADC, Pin
from wifi_config import WIFI_SSID as SSID, WIFI_PASSWORD as PASSWORD

# ↓ 구글에서 복사한 주소를 그대로 붙여넣으세요 (.../exec 로 끝나는 주소)
WEB_APP_URL = "https://script.google.com/macros/s/여기에_붙여넣기/exec"
INTERVAL = 60                 # 몇 초마다 보낼지 (60 = 1분)
gas = ADC(Pin(26))           # 가스센서 (그로브 A0)

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
    s.close()
    return buf

def send(value):
    resp = https_get(WEB_APP_URL + "?value=" + str(value))
    head = resp.split(b"\r\n\r\n", 1)[0]
    if b" 302 " in head or b" 301 " in head:     # 구글이 다른 주소로 넘기면 따라가기
        for line in head.split(b"\r\n"):
            if line.lower().startswith(b"location:"):
                https_get(line.split(b":", 1)[1].strip().decode())
                break

if connect_wifi():
    while True:
        v = gas.read_u16()
        try:
            send(v)
            print("시트로 보냄:", v)
        except Exception as e:
            print("실패(잠시 뒤 다시 시도):", e)
        time.sleep(INTERVAL)
