# === 와이파이 신호 세기(RSSI) 실시간 대시보드 ===
# 피코가 작은 웹서버가 되어, 같은 와이파이의 스마트폰/PC 브라우저에서
# 신호 세기를 실시간 그래프로 볼 수 있게 합니다.
import network
import socket
import json
import time
from wifi_config import WIFI_SSID as SSID, WIFI_PASSWORD as PASSWORD

wlan = network.WLAN(network.STA_IF)


def connect_wifi():
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Wi-Fi 연결 중", end="")
    timeout = 20
    while not wlan.isconnected() and timeout > 0:
        print(".", end="")
        time.sleep(0.5)
        timeout -= 1
    if wlan.isconnected():
        ip = wlan.ifconfig()[0]
        print("\n✅ 연결 완료!  →  http://%s" % ip)
        return ip
    print("\n❌ Wi-Fi 연결 실패")
    return None


HTML = b"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Wi-Fi 신호 세기 모니터</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  body { font-family: 'Noto Sans KR', sans-serif; max-width: 860px;
         margin: 24px auto; padding: 0 16px; background: #f5f7fb; color: #222; }
  h1 { text-align: center; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
          gap: 14px; margin: 20px 0; }
  .card { background: #fff; border-radius: 14px; padding: 18px; text-align: center;
          box-shadow: 0 2px 6px rgba(0,0,0,.06); }
  .label { font-size: 12px; color: #888; letter-spacing: 1px; margin-bottom: 8px; }
  .big { font-size: 38px; font-weight: 800; color: #3b82f6; }
  .unit { font-size: 11px; color: #aaa; margin-top: 4px; }
  .chart-wrap { background: #fff; border-radius: 14px; padding: 18px;
                box-shadow: 0 2px 6px rgba(0,0,0,.06); }
</style>
</head>
<body>
  <h1>📶 Wi-Fi 신호 세기 모니터</h1>
  <div class="grid">
    <div class="card">
      <div class="label">RSSI</div>
      <div class="big" id="rssiVal">---</div>
      <div class="unit">dBm (0에 가까울수록 강함)</div>
    </div>
    <div class="card">
      <div class="label">상태</div>
      <div class="big" id="statusVal" style="font-size:24px">측정중</div>
      <div class="unit">신호 품질</div>
    </div>
  </div>
  <div class="chart-wrap">
    <canvas id="chart" height="110"></canvas>
  </div>
<script>
const labels = [], data = [];
const MAX = 40;
function quality(r) {
  if (r >= -55) return { t: '아주 강함', c: '#22c55e' };
  if (r >= -67) return { t: '강함',     c: '#84cc16' };
  if (r >= -75) return { t: '보통',     c: '#f59e0b' };
  return                { t: '약함',     c: '#ef4444' };
}
const chart = new Chart(document.getElementById('chart'), {
  type: 'line',
  data: { labels, datasets: [{ label: 'RSSI', data,
    borderColor: '#3b82f6', backgroundColor: 'rgba(59,130,246,.1)',
    fill: true, tension: .3, pointRadius: 0 }] },
  options: { animation: false,
    scales: { y: { suggestedMin: -90, suggestedMax: -30 } },
    plugins: { legend: { display: false } } }
});
async function update() {
  try {
    const res = await fetch('/data');
    const j = await res.json();
    const r = j.value;
    const q = quality(r);
    document.getElementById('rssiVal').textContent = r;
    document.getElementById('rssiVal').style.color = q.c;
    document.getElementById('statusVal').textContent = q.t;
    document.getElementById('statusVal').style.color = q.c;
    labels.push(new Date().toLocaleTimeString());
    data.push(r);
    if (labels.length > MAX) { labels.shift(); data.shift(); }
    chart.update('none');
  } catch (e) { console.warn('응답 없음', e); }
}
setInterval(update, 1000);
update();
</script>
</body>
</html>"""


def send_response(conn, content_type, body):
    header = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: %s\r\n"
        "Content-Length: %d\r\n"
        "Connection: close\r\n"
        "\r\n"
    ) % (content_type, len(body))
    conn.sendall(header.encode() + body)


def run_server():
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(addr)
    srv.listen(3)
    print("서버 대기 중... (브라우저로 위 주소에 접속하세요)")
    while True:
        conn, _ = srv.accept()
        try:
            req = conn.recv(512).decode("utf-8", "ignore")
            if "GET /data" in req:
                value = wlan.status("rssi")
                body = json.dumps({"value": value}).encode()
                send_response(conn, "application/json", body)
            else:
                send_response(conn, "text/html; charset=utf-8", HTML)
        except Exception as e:
            code = e.args[0] if e.args else None
            tip = {104: "브라우저가 연결을 먼저 끊음 (정상, 무시 OK)",
                   32:  "응답 도중 연결이 끊김 (정상)",
                   110: "응답 대기 시간 초과",
                   11:  "데이터가 아직 안 옴 (일시적)"}.get(code)
            print("요청 처리:", ("[%s] %s" % (code, tip)) if tip else ("오류 " + str(e)))
        finally:
            conn.close()


ip = connect_wifi()
if ip:
    run_server()
