import network
import socket
import json
from machine import ADC, Pin
import time
from wifi_config import WIFI_SSID as SSID, WIFI_PASSWORD as PASSWORD

gas_sensor = ADC(Pin(26))

# ── 임계값: 우리 교실에 맞게 이 두 숫자만 바꾸세요 (웹 화면 색도 함께 바뀜) ──
SAFE_MAX = 20000   # 이 아래 = 안전(초록)
WARN_MAX = 45000   # 이 아래 = 주의(노랑), 넘으면 위험(빨강)


def read_average(sensor, count=10):
    total = 0
    for _ in range(count):
        total += sensor.read_u16()
        time.sleep_ms(10)
    return total // count


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
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
        print(f"\n✅ 연결 완료!  →  http://{ip}")
        return ip
    print("\n❌ Wi-Fi 연결 실패")
    return None


HTML = b"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MQ-2 가스 센서 모니터</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Noto+Sans+KR:wght@300;400;700&display=swap');

  :root {
    --bg:      #0b0f1a;
    --panel:   #111827;
    --border:  #1f2d45;
    --safe:    #22d3a6;
    --warn:    #f59e0b;
    --danger:  #ef4444;
    --accent:  #3b82f6;
    --text:    #e2e8f0;
    --muted:   #64748b;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: var(--bg); color: var(--text);
         font-family: 'Noto Sans KR', sans-serif;
         min-height: 100vh; padding: 24px 16px; }

  header { text-align: center; margin-bottom: 28px; }
  header h1 {
    font-family: 'Orbitron', monospace;
    font-size: clamp(18px, 4vw, 28px);
    letter-spacing: 4px;
    color: var(--accent);
    text-shadow: 0 0 20px rgba(59,130,246,0.5);
  }
  header p { color: var(--muted); font-size: 13px; margin-top: 4px; }

  .grid { display: grid;
          grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
          gap: 14px; max-width: 860px; margin: 0 auto 24px; }
  .card { background: var(--panel); border: 1px solid var(--border);
          border-radius: 14px; padding: 18px 14px; text-align: center;
          transition: border-color .3s; }
  .card .label { font-size: 11px; letter-spacing: 2px;
                 text-transform: uppercase; color: var(--muted);
                 margin-bottom: 10px; }
  .card .big { font-family: 'Orbitron', monospace;
               font-size: clamp(28px, 6vw, 40px); font-weight: 900;
               transition: color .3s; }
  .card .unit { font-size: 11px; color: var(--muted); margin-top: 4px; }

  #statusCard { border-color: var(--safe);
                box-shadow: 0 0 20px rgba(34,211,166,.12); }
  #statusText { font-family: 'Orbitron', monospace;
                font-size: clamp(14px, 3vw, 20px);
                font-weight: 700; letter-spacing: 3px; }

  .chart-wrap { max-width: 860px; margin: 0 auto;
                background: var(--panel); border: 1px solid var(--border);
                border-radius: 14px; padding: 20px; }
  .chart-wrap h2 { font-family: 'Orbitron', monospace;
                   font-size: 12px; letter-spacing: 3px;
                   color: var(--muted); margin-bottom: 16px; }

  #dot { display: inline-block; width: 8px; height: 8px;
         border-radius: 50%; background: var(--safe);
         margin-right: 6px; animation: pulse 1.4s infinite; }
  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%      { opacity: .4; transform: scale(1.4); }
  }
</style>
</head>
<body>
<header>
  <h1>MQ-2 GAS SENSOR MONITOR</h1>
  <p><span id="dot"></span>Raspberry Pi Pico 2 WH &mdash; 실시간 측정</p>
</header>

<div class="grid">
  <div class="card">
    <div class="label">ADC RAW</div>
    <div class="big" id="rawVal">---</div>
    <div class="unit">0 ~ 65535</div>
  </div>
  <div class="card">
    <div class="label">전압</div>
    <div class="big" id="voltVal">-.-</div>
    <div class="unit">Volt (3.3 V ref)</div>
  </div>
  <div class="card">
    <div class="label">농도 비율</div>
    <div class="big" id="pctVal">--%</div>
    <div class="unit">풀스케일 대비</div>
  </div>
  <div class="card" id="statusCard">
    <div class="label">상태</div>
    <div id="statusText" style="color:var(--safe)">SAFE</div>
  </div>
</div>

<div class="chart-wrap">
  <h2>REALTIME WAVEFORM &nbsp;(최근 60초)</h2>
  <canvas id="chart" height="120"></canvas>
</div>

<script>
const MAX = 60;
const times = [], vals = [];

const ctx = document.getElementById('chart').getContext('2d');
const chart = new Chart(ctx, {
  type: 'line',
  data: { labels: times,
    datasets: [{ label: 'ADC (이동평균)', data: vals,
      borderColor: '#3b82f6',
      backgroundColor: 'rgba(59,130,246,0.08)',
      borderWidth: 2, fill: true, tension: 0.4,
      pointRadius: 0, pointHitRadius: 8 }] },
  options: { animation: false, responsive: true,
    scales: {
      y: { suggestedMin: 0, suggestedMax: 65535,
           grid: { color: 'rgba(255,255,255,.06)' },
           ticks: { color: '#64748b',
                    font: { family: 'monospace', size: 10 },
                    callback: v => v.toLocaleString() } },
      x: { grid: { color: 'rgba(255,255,255,.06)' },
           ticks: { color: '#64748b',
                    font: { family: 'monospace', size: 10 },
                    maxTicksLimit: 8 } }
    },
    plugins: { legend: { display: false } }
  }
});

let TH = { safe: 20000, warn: 45000 };   // /data 가 코드 상단 임계값을 알려주면 갱신됨
function levelOf(v) {
  if (v < TH.safe) return { label: 'SAFE',    color: '#22d3a6' };
  if (v < TH.warn) return { label: 'WARNING', color: '#f59e0b' };
  return                 { label: 'DANGER',   color: '#ef4444' };
}

async function poll() {
  try {
    const res  = await fetch('/data');
    const json = await res.json();
    if (json.safe != null) { TH.safe = json.safe; TH.warn = json.warn; }
    const v    = json.value;
    const now  = new Date().toLocaleTimeString('ko-KR', { hour12: false });
    const lv   = levelOf(v);

    document.getElementById('rawVal').textContent  = v.toLocaleString();
    document.getElementById('rawVal').style.color  = lv.color;
    document.getElementById('voltVal').textContent = (v / 65535 * 3.3).toFixed(3);
    document.getElementById('pctVal').textContent  = (v / 65535 * 100).toFixed(1) + '%';
    document.getElementById('statusText').textContent  = lv.label;
    document.getElementById('statusText').style.color  = lv.color;
    document.getElementById('statusCard').style.borderColor  = lv.color;
    document.getElementById('statusCard').style.boxShadow    =
      `0 0 20px ${lv.color}30`;

    times.push(now); vals.push(v);
    if (times.length > MAX) { times.shift(); vals.shift(); }

    const margin = 2000;
    const yMin = Math.max(0,     Math.min(...vals) - margin);
    const yMax = Math.min(65535, Math.max(...vals) + margin);
    chart.options.scales.y.min = yMin;
    chart.options.scales.y.max = yMax;

    chart.data.datasets[0].borderColor     = lv.color;
    chart.data.datasets[0].backgroundColor = lv.color + '18';
    chart.update('none');
  } catch (e) {
    console.warn('센서 응답 없음', e);
  }
}

setInterval(poll, 500);
poll();
</script>
</body>
</html>"""


def send_response(conn, status, content_type, body_bytes):
    header = (
        f"HTTP/1.1 {status}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        "Access-Control-Allow-Origin: *\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode()
    conn.sendall(header + body_bytes)


def run_server():
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    srv  = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(addr)
    srv.listen(3)
    print("서버 대기 중... (Ctrl+C로 종료)")

    while True:
        conn, _ = srv.accept()
        try:
            req = conn.recv(512).decode("utf-8", "ignore")
            if "GET /data" in req:
                value = read_average(gas_sensor, 10)
                body  = json.dumps({"value": value, "safe": SAFE_MAX, "warn": WARN_MAX}).encode()
                send_response(conn, "200 OK", "application/json", body)
            else:
                send_response(conn, "200 OK", "text/html; charset=utf-8", HTML)
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