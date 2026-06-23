# === 오늘의 비 예보를 10개 LED에 담는 '날씨 시계' (설치 불필요) ===
# 내장 socket + ssl 로 Open-Meteo에 접속 — 추가 설치 없이 복붙 실행됩니다.
#   맑음(연초록) → 흐림(노랑) → 비 가능(파랑) → 비 확실(보라)
import network, socket, ssl, json, time, gc
from machine import Pin
from neopixel import NeoPixel
from wifi_config import WIFI_SSID as SSID, WIFI_PASSWORD as PASSWORD

LAT = 37.5665      # 우리 지역 위도
LON = 126.9780     # 우리 지역 경도
HOST = "api.open-meteo.com"

TIMING = (280, 515, 515, 745)
NUM = 10
np = NeoPixel(Pin(16), NUM, timing=TIMING)

# 6시~23시를 LED 칸 수만큼 고르게 나눈 대표 시각 (NUM만 바꾸면 자동 적용)
HOURS = [round(6 + i * (23 - 6) / (NUM - 1)) for i in range(NUM)]


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Wi-Fi 연결 중", end="")
    timeout = 20
    while not wlan.isconnected() and timeout > 0:
        print(".", end=""); time.sleep(0.5); timeout -= 1
    if wlan.isconnected():
        ip = wlan.ifconfig()[0]
        print("\n✅ 연결 완료!  IP:", ip)
        return ip
    print("\n❌ Wi-Fi 연결 실패")
    return None


def http_get_json(host, path):
    gc.collect()
    addr = socket.getaddrinfo(host, 443)[0][-1]
    s = socket.socket()
    s.connect(addr)
    try:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.verify_mode = ssl.CERT_NONE          # 피코엔 인증서 목록이 없어 검증 생략
        s = ctx.wrap_socket(s, server_hostname=host)
    except AttributeError:                       # 옛 펌웨어 호환
        s = ssl.wrap_socket(s, server_hostname=host)
    s.write(("GET %s HTTP/1.0\r\nHost: %s\r\nConnection: close\r\n\r\n"
             % (path, host)).encode())
    buf = b""
    while True:
        chunk = s.read(512)
        if not chunk:
            break
        buf += chunk
    s.close()
    return json.loads(buf.split(b"\r\n\r\n", 1)[1])


def get_rain_probs():
    path = ("/v1/forecast?latitude=%s&longitude=%s"
            "&hourly=precipitation_probability"
            "&timezone=Asia%%2FSeoul&forecast_days=1" % (LAT, LON))
    return http_get_json(HOST, path)["hourly"]["precipitation_probability"]


def prob_to_color(p):
    if p is None:  return (0, 0, 0)
    if p < 20:     return (0, 30, 5)     # 맑음 - 연초록
    if p < 50:     return (30, 25, 0)    # 흐림 - 노랑
    if p < 80:     return (0, 10, 40)    # 비 가능 - 파랑
    return (15, 0, 40)                   # 비 확실 - 보라


def show(probs):
    for i, hour in enumerate(HOURS):
        p = probs[hour]
        np[i] = prob_to_color(p)
        print("LED %d = %2d시 → %s%%" % (i, hour, p))
    np.write()


# 10분마다 새 예보를 받아 LED를 갱신
ip = connect_wifi()
if ip:
    while True:
        try:
            show(get_rain_probs())
        except Exception as e:
            print("오류:", e)
        time.sleep(600)
