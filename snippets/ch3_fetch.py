# === 1단계: 오늘의 강수확률 가져오기 (설치 불필요) ===
# 피코에 기본 내장된 socket + ssl 만으로 Open-Meteo(HTTPS)에 접속합니다.
import network, socket, ssl, json, time, gc
from wifi_config import WIFI_SSID as SSID, WIFI_PASSWORD as PASSWORD

LAT = 37.5665      # 위도 (우리 지역 좌표로 바꾸세요)
LON = 126.9780     # 경도
HOST = "api.open-meteo.com"


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Wi-Fi 연결 중", end="")
    while not wlan.isconnected():
        print(".", end=""); time.sleep(0.5)
    print("\n연결 완료!")


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
    body = buf.split(b"\r\n\r\n", 1)[1]          # 헤더 떼고 본문(JSON)만
    return json.loads(body)


connect_wifi()
path = ("/v1/forecast?latitude=%s&longitude=%s"
        "&hourly=precipitation_probability"
        "&timezone=Asia%%2FSeoul&forecast_days=1" % (LAT, LON))
data = http_get_json(HOST, path)

probs = data["hourly"]["precipitation_probability"]   # 24개 (0~23시)
for hour in range(6, 24):
    print("%2d시 강수확률: %s%%" % (hour, probs[hour]))
