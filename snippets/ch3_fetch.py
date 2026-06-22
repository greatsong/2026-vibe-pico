# === 1단계: 인터넷에서 오늘의 강수확률 가져오기 (손코딩) ===
# Open-Meteo는 무료이고 API 키가 필요 없습니다. 위도/경도만 넣으면 됩니다.
import network, time
from wifi_config import WIFI_SSID as SSID, WIFI_PASSWORD as PASSWORD

# urequests(=requests)는 한 번만 설치하면 됩니다 (아래 설명 참고)
try:
    import requests
except ImportError:
    import urequests as requests

LAT = 37.5665     # 위도  (서울시청 기준 — 우리 지역 좌표로 바꾸세요)
LON = 126.9780    # 경도

# 1) 와이파이 연결
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
print("Wi-Fi 연결 중", end="")
while not wlan.isconnected():
    print(".", end=""); time.sleep(0.5)
print("\n연결 완료!")

# 2) 강수확률 요청
url = ("https://api.open-meteo.com/v1/forecast"
       "?latitude=%s&longitude=%s"
       "&hourly=precipitation_probability"
       "&timezone=Asia%%2FSeoul&forecast_days=1" % (LAT, LON))

res = requests.get(url)
data = res.json()
res.close()

# 3) 0시~23시 강수확률 24개 중, 6시~23시만 출력
probs = data["hourly"]["precipitation_probability"]
for hour in range(6, 24):
    print("%2d시 강수확률: %s%%" % (hour, probs[hour]))
