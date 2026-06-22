# === 부록 예제 · 미세먼지 신호등 (Open-Meteo 대기질) ===
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

HOST = "air-quality-api.open-meteo.com"
LAT, LON = 37.5665, 126.9780     # 우리 지역 위도·경도


def grade(pm):
    # 한국 PM2.5 등급 (좋음/보통/나쁨/매우나쁨)
    if pm <= 15:  return "좋음",     (0, 0, 40)
    if pm <= 35:  return "보통",     (0, 30, 0)
    if pm <= 75:  return "나쁨",     (30, 25, 0)
    return                "매우나쁨", (40, 0, 0)


if connect_wifi():
    path = "/v1/air-quality?latitude=%s&longitude=%s&current=pm2_5,pm10" % (LAT, LON)
    cur = http_get_json(HOST, path)["current"]
    pm25 = cur["pm2_5"]
    name, color = grade(pm25)
    print("PM2.5 = %s  ->  %s" % (pm25, name))
    show_bar(10, color)          # 전체 LED를 등급 색으로 (미세먼지 신호등)
