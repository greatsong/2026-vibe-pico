# 주변에 어떤 와이파이가 있는지 스캔해 봅니다
import network

wlan = network.WLAN(network.STA_IF)   # STA = 와이파이에 '접속하는' 모드
wlan.active(True)

for net in wlan.scan():
    ssid = net[0].decode()            # 와이파이 이름
    rssi = net[3]                     # 신호 세기 (dBm, 0에 가까울수록 강함)
    print("%-22s  %d dBm" % (ssid, rssi))
