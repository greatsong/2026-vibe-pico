# 동작 인식 ③-MPU : 짝 활동 데이터 모으기 (MPU6050 버전, 피코=서버)
# MPU6050을 그로브 I2C 포트에 변환 케이블로 연결, 전원 3.3V!  던지는 사람: 손목+보조배터리.
import network, socket, time, struct, math
from machine import I2C, Pin
from neopixel import NeoPixel
from wifi_config import WIFI_SSID, WIFI_PASSWORD

# ── MPU6050 준비 ──
ADDR = 0x68          # AD0=HIGH면 0x69
PWR_MGMT_1, ACCEL_CONFIG, GYRO_CONFIG = 0x6B, 0x1C, 0x1B
ACCEL_XOUT_H, GYRO_XOUT_H = 0x3B, 0x43
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
if ADDR not in i2c.scan():
    raise RuntimeError("MPU6050 못 찾음 — 배선·전원 3.3V 확인 (AD0=H면 ADDR=0x69)")
i2c.writeto_mem(ADDR, PWR_MGMT_1,   bytes([0x00]))   # 깨우기
time.sleep(0.1)
i2c.writeto_mem(ADDR, ACCEL_CONFIG, bytes([0x18]))   # ±16g
i2c.writeto_mem(ADDR, GYRO_CONFIG,  bytes([0x18]))   # ±2000°/s
time.sleep(0.05)
A_SCALE, G_SCALE = 1/2048, 1/16.4
def read():
    a = struct.unpack(">hhh", i2c.readfrom_mem(ADDR, ACCEL_XOUT_H, 6))
    g = struct.unpack(">hhh", i2c.readfrom_mem(ADDR, GYRO_XOUT_H, 6))
    am = math.sqrt(sum((v*A_SCALE)**2 for v in a))
    gm = math.sqrt(sum((v*G_SCALE)**2 for v in g))
    return am, gm

# ── LED ──
TIMING = (280,515,515,745); NUM = 10
np = NeoPixel(Pin(16), NUM, timing=TIMING)
def led(c): np.fill(c); np.write()

# ── 와이파이 ──
wlan = network.WLAN(network.STA_IF); wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)
for _ in range(20):
    if wlan.isconnected(): break
    time.sleep(0.5)
print("폰에서 여세요 →  http://%s" % wlan.ifconfig()[0])

# ── 데이터 파일 ──
try:
    open("flips.csv").close()
except OSError:
    open("flips.csv", "w").write("peak_g,peak_a,label\n")
def counts():
    s = f = 0
    for ln in open("flips.csv"):
        ln = ln.strip()
        if ln.endswith(",1"): s += 1
        elif ln.endswith(",0"): f += 1
    return s, f

# ── 상태 ──
READY, PENDING = 0, 1
state, pend, START_G = READY, (0, 0), 300
def page():
    s, f = counts()
    if state == PENDING:
        top = ("<h2 style='color:#e67e22'>🟠 방금 플립!</h2><p>회전 %.0f°/s · 가속 %.1fg</p>"
               "<a href='/r?v=1'><button style='background:#27ae60'>성공 ✅</button></a>"
               "<a href='/r?v=0'><button style='background:#c0392b'>실패 ❌</button></a>"
               "<a href='/cancel'><button style='background:#7f8c8d'>취소</button></a>") % pend
    else:
        top = "<h2 style='color:#2c3e50'>🟢 플립하세요!</h2><p>던지면 여기에 버튼이 떠요.</p>"
    return ("<!DOCTYPE html><html><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<meta http-equiv='refresh' content='1.5'><style>body{font-family:sans-serif;"
            "text-align:center;padding:20px}button{font-size:1.4em;padding:16px 20px;margin:5px;"
            "border:0;border-radius:12px;color:#fff}</style></head><body>%s<hr>"
            "<p>기록: 성공 %d · 실패 %d (합 %d)</p>"
            "<a href='/end'><button style='background:#34495e'>종료</button></a></body></html>") % (top, s, f, s+f)

# ── 서버 + IMU 동시 루프 (논블로킹) ──
srv = socket.socket(); srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("0.0.0.0", 80)); srv.listen(1); srv.setblocking(False)
led((0,30,0)); print("준비 완료! 짝 활동 시작.")
while True:
    if state == READY:                          # (1) 플립 감지
        am, gm = read()
        if gm > START_G:
            pg, pa, t0 = gm, am, time.ticks_ms()
            while time.ticks_diff(time.ticks_ms(), t0) < 400:
                am, gm = read(); pg = max(pg, gm); pa = max(pa, am)
            pend, state = (pg, pa), PENDING; led((40,25,0))   # 주황=라벨 대기
    try: cl, _ = srv.accept()                    # (2) 폰 요청 처리
    except OSError: cl = None
    if cl:
        try:
            path = cl.recv(512).split(b" ")[1]
            if path.startswith(b"/r?v=") and state == PENDING:
                open("flips.csv", "a").write("%.0f,%.1f,%d\n" % (pend[0], pend[1], 1 if b"v=1" in path else 0))
                state = READY; led((0,45,0)); time.sleep(0.15); led((0,30,0))
            elif path.startswith(b"/cancel"):
                state = READY; led((0,30,0))
            elif path.startswith(b"/end"):
                cl.send(b"HTTP/1.0 200 OK\r\nContent-Type:text/html; charset=utf-8\r\n\r\n")
                cl.send("<h2>기록 종료! flips.csv 저장됨.</h2>".encode()); cl.close(); break
            cl.send(b"HTTP/1.0 200 OK\r\nContent-Type:text/html; charset=utf-8\r\n\r\n")
            cl.send(page().encode())
        except (OSError, IndexError): pass
        cl.close()
    time.sleep(0.005)
s, f = counts(); print("끝! 성공 %d · 실패 %d → flips.csv" % (s, f)); led((0,0,0))
