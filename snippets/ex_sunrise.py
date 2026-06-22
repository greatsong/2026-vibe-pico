# === 부록 예제 · 낮 길이 게이지 (sunrise-sunset) ===
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

HOST = "api.sunrise-sunset.org"
LAT, LON = 37.5665, 126.9780


if connect_wifi():
    r = http_get_json(HOST, "/json?lat=%s&lng=%s&formatted=0" % (LAT, LON))["results"]
    hours = r["day_length"] / 3600
    print("낮 길이: %.1f 시간" % hours)
    print("일출(UTC):", r["sunrise"])
    print("일몰(UTC):", r["sunset"])
    n = min(10, round(hours / 24 * 10))    # 하루 24시간 중 낮의 비율
    show_bar(n, (40, 25, 0))               # 햇빛색
