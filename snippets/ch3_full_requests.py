# === 오늘의 비 예보를 10개 LED에 담는 '날씨 시계' ===
# 6시~23시를 10칸으로 나눠, 각 칸의 색으로 강수확률을 보여 줍니다.
#   맑음(연초록) → 흐림(노랑) → 비 가능(파랑) → 비 확실(보라)
import network, time
from machine import Pin
from neopixel import NeoPixel
from wifi_config import WIFI_SSID as SSID, WIFI_PASSWORD as PASSWORD

try:
    import requests
except ImportError:
    import urequests as requests

LAT = 37.5665      # 우리 지역 위도
LON = 126.9780     # 우리 지역 경도

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


def get_rain_probs():
    url = ("https://api.open-meteo.com/v1/forecast"
           "?latitude=%s&longitude=%s"
           "&hourly=precipitation_probability"
           "&timezone=Asia%%2FSeoul&forecast_days=1" % (LAT, LON))
    res = requests.get(url)
    data = res.json()
    res.close()
    return data["hourly"]["precipitation_probability"]   # 24개 (0~23시)


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
