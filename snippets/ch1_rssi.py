# 와이파이에 연결하고, 신호 세기(RSSI)를 계속 읽어 봅니다
import network, time
from wifi_config import WIFI_SSID as SSID, WIFI_PASSWORD as PASSWORD

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Wi-Fi 연결 중", end="")
while not wlan.isconnected():
    print(".", end="")
    time.sleep(0.5)
print("\n연결 완료! IP =", wlan.ifconfig()[0])

while True:
    rssi = wlan.status("rssi")        # 현재 신호 세기 (예: -55 dBm)
    print("신호 세기:", rssi, "dBm")
    time.sleep(1)
