# === 부록 예제 · 우주날씨 Kp 지수 (NOAA) ===
# 설치 불필요(socket+ssl) · 와이파이는 wifi_config.py 필요 · LED는 GP16, WS2813 10개
import network, socket, ssl, json, time, gc
from machine import Pin
from neopixel import NeoPixel
from wifi_config import WIFI_SSID as SSID, WIFI_PASSWORD as PASSWORD

np = NeoPixel(Pin(16), 10, timing=(280, 515, 515, 745))


def connect_wifi():
    w = network.WLAN(network.STA_IF)
    w.active(True)
    w.connect(SSID, PASSWORD)
    print("Wi-Fi 연결 중", end="")
    for _ in range(20):
        if w.isconnected():
            break
        print(".", end="")
        time.sleep(0.5)
    ok = w.isconnected()
    print(" 연결 완료!" if ok else " 연결 실패")
    return ok


def http_get_json(host, path):
    gc.collect()
    s = socket.socket()
    s.connect(socket.getaddrinfo(host, 443)[0][-1])
    try:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.verify_mode = ssl.CERT_NONE
        s = ctx.wrap_socket(s, server_hostname=host)
    except AttributeError:
        s = ssl.wrap_socket(s, server_hostname=host)
    s.write(("GET %s HTTP/1.0\r\nHost: %s\r\nConnection: close\r\n\r\n" % (path, host)).encode())
    buf = b""
    while True:
        chunk = s.read(512)
        if not chunk:
            break
        buf += chunk
    s.close()
    return json.loads(buf.split(b"\r\n\r\n", 1)[1])


def show_bar(n, color):
    # 0~10칸을 color로 켜고 나머지는 끔 (LED 게이지)
    for i in range(10):
        np[i] = color if i < n else (0, 0, 0)
    np.write()

HOST = "services.swpc.noaa.gov"


if connect_wifi():
    arr = http_get_json(HOST, "/products/noaa-planetary-k-index.json")
    kp = arr[-1]["Kp"]                     # 가장 최근 Kp (0~9)
    print("현재 Kp 지수: %.1f" % kp)
    n = min(10, round(kp / 9 * 10))
    color = (0, 30, 0) if kp < 4 else (30, 25, 0) if kp < 6 else (25, 0, 40)
    show_bar(n, color)                     # Kp 높을수록 보라(오로라 가능성)
    if kp >= 6:
        print("지자기 폭풍! 고위도에서 오로라 가능성이 높아요")
