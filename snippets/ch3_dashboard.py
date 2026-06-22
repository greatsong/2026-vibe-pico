# === 오늘의 비 예보: 10개 LED + 웹 대시보드 (설치 불필요) ===
# 피코가 LED 날씨 시계이면서 동시에 웹서버가 됩니다.
# 같은 와이파이의 스마트폰/PC에서 접속하면:
#   · 피코 10칸 LED와 똑같은 색의 칸 (이 시각에 비가 오는지)
#   · 색이 무슨 뜻인지 알려 주는 범례
#   · 6시~23시 시간별 강수확률 막대그래프
import network, socket, ssl, json, time, gc
from machine import Pin
from neopixel import NeoPixel
from wifi_config import WIFI_SSID as SSID, WIFI_PASSWORD as PASSWORD

LAT = 37.5665       # 우리 지역 위도 (바꾸세요)
LON = 126.9780      # 우리 지역 경도
HOST = "api.open-meteo.com"
REFRESH = 600       # 날씨 갱신 주기(초). 600 = 10분

TIMING = (280, 515, 515, 745)
NUM = 10
np = NeoPixel(Pin(16), NUM, timing=TIMING)
HOURS = [round(6 + i * (23 - 6) / (NUM - 1)) for i in range(NUM)]

# 강수확률 단계 → LED 색(rgb). 웹 범례 색·의미와 똑같이 맞춰 둡니다.
#   0~20 맑음(연초록) · 20~50 흐림(노랑) · 50~80 비 가능(파랑) · 80~ 비 확실(보라)
LEVELS = [(20, (0, 30, 5)), (50, (30, 25, 0)), (80, (0, 10, 40)), (101, (15, 0, 40))]

state = {"probs": [None] * 24, "date": "", "fetched": None}


def level_index(p):
    p = p if p is not None else 0
    for i, (thr, _rgb) in enumerate(LEVELS):
        if p < thr:
            return i
    return len(LEVELS) - 1


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


def refresh():
    path = ("/v1/forecast?latitude=%s&longitude=%s"
            "&hourly=precipitation_probability"
            "&timezone=Asia%%2FSeoul&forecast_days=1" % (LAT, LON))
    hourly = http_get_json(HOST, path)["hourly"]
    state["probs"] = hourly["precipitation_probability"]   # 24개 (0~23시)
    state["date"] = hourly["time"][0][:10]                 # "YYYY-MM-DD"
    state["fetched"] = time.ticks_ms()
    for i, h in enumerate(HOURS):                          # LED 갱신
        np[i] = LEVELS[level_index(state["probs"][h])][1]
    np.write()
    print("날씨 갱신:", state["date"])


def refresh_if_due():
    if (state["fetched"] is None or
            time.ticks_diff(time.ticks_ms(), state["fetched"]) > REFRESH * 1000):
        try:
            refresh()
        except Exception as e:
            print("갱신 오류:", e)


def data_json():
    p = state["probs"]
    ago = 0 if state["fetched"] is None else \
        time.ticks_diff(time.ticks_ms(), state["fetched"]) // 1000
    leds = [{"h": h, "p": p[h], "lv": level_index(p[h])} for h in HOURS]
    hourly = [{"h": h, "p": p[h], "lv": level_index(p[h])} for h in range(6, 24)]
    return json.dumps({"date": state["date"], "ago": ago,
                       "leds": leds, "hourly": hourly})


HTML = b"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>오늘의 비 예보 · LED 날씨 시계</title>
<style>
  :root{ --bg:#0b1020; --panel:#161c30; --line:#26304d; --text:#e8edf7; --muted:#8b93ab; }
  *{ box-sizing:border-box; margin:0; padding:0; }
  body{ background:var(--bg); color:var(--text); padding:22px 14px; min-height:100vh;
        font-family:'Noto Sans KR',system-ui,-apple-system,sans-serif; }
  .wrap{ max-width:760px; margin:0 auto; }
  header{ text-align:center; margin-bottom:18px; }
  h1{ font-size:clamp(18px,4.5vw,26px); }
  .sub{ color:var(--muted); font-size:13px; margin-top:7px; }
  .card{ background:var(--panel); border:1px solid var(--line);
         border-radius:16px; padding:18px; margin:14px 0; }
  .h2{ font-size:12px; letter-spacing:1px; color:var(--muted); margin-bottom:14px; }
  .leds{ display:grid; grid-template-columns:repeat(10,1fr); gap:7px; }
  .led{ text-align:center; }
  .dot{ height:44px; border-radius:10px; border:1px solid rgba(255,255,255,.08);
        box-shadow:0 0 14px var(--g,transparent); transition:.5s; }
  .led .hr{ font-size:11px; color:var(--muted); margin-top:7px; }
  .led .pp{ font-size:12px; font-weight:700; margin-top:2px; }
  .legend{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; }
  .lg{ display:flex; align-items:center; gap:10px; font-size:13px; }
  .sw{ width:22px; height:22px; border-radius:6px; flex:0 0 22px; }
  .lg .r{ color:var(--muted); font-size:11px; }
  .bars{ display:flex; align-items:flex-end; gap:4px; height:130px; }
  .bar{ flex:1; display:flex; flex-direction:column; justify-content:flex-end;
        align-items:center; height:100%; }
  .bar .b{ width:100%; border-radius:4px 4px 0 0; transition:.5s; min-height:2px; }
  .bar .t{ font-size:9px; color:var(--muted); margin-top:5px; }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>🌧️ 오늘의 비 예보 · LED 날씨 시계</h1>
    <div class="sub" id="sub">불러오는 중…</div>
  </header>

  <div class="card">
    <div class="h2">LED 바 — 피코의 10칸과 똑같은 색</div>
    <div class="leds" id="leds"></div>
  </div>

  <div class="card">
    <div class="h2">색이 뜻하는 것</div>
    <div class="legend" id="legend"></div>
  </div>

  <div class="card">
    <div class="h2">시간별 강수확률 (6시 → 23시)</div>
    <div class="bars" id="bars"></div>
  </div>
</div>

<script>
// 웹 범례 — 피코 LEVELS와 같은 의미/순서
const LV = [
  { n:'맑음',    c:'#22c55e', r:'0–20%'  },
  { n:'흐림',    c:'#eab308', r:'20–50%' },
  { n:'비 가능', c:'#3b82f6', r:'50–80%' },
  { n:'비 확실', c:'#8b5cf6', r:'80–100%'}
];

document.getElementById('legend').innerHTML = LV.map(l =>
  `<div class="lg"><span class="sw" style="background:${l.c}"></span>
   <div><div>${l.n}</div><div class="r">강수확률 ${l.r}</div></div></div>`).join('');

const pct = p => (p == null ? '-' : p + '%');

async function load(){
  try{
    const j = await (await fetch('/data')).json();
    document.getElementById('sub').textContent =
      `${j.date} 예보 · ${j.ago}초 전 갱신 · 10분마다 자동 갱신`;
    document.getElementById('leds').innerHTML = j.leds.map(d => {
      const c = LV[d.lv].c;
      return `<div class="led">
                <div class="dot" style="background:${c}; --g:${c}"></div>
                <div class="hr">${d.h}시</div>
                <div class="pp" style="color:${c}">${pct(d.p)}</div>
              </div>`;
    }).join('');
    document.getElementById('bars').innerHTML = j.hourly.map(d => {
      const c = LV[d.lv].c;
      const h = (d.p == null ? 2 : Math.max(2, d.p));
      return `<div class="bar" title="${d.h}시 ${pct(d.p)}">
                <div class="b" style="height:${h}%; background:${c}"></div>
                <div class="t">${d.h}</div>
              </div>`;
    }).join('');
  }catch(e){
    document.getElementById('sub').textContent = '응답 없음 — 다시 시도 중…';
  }
}
load();
setInterval(load, 30000);
</script>
</body>
</html>"""


def send_response(conn, status, content_type, body):
    header = ("HTTP/1.1 %s\r\nContent-Type: %s\r\nContent-Length: %d\r\n"
              "Access-Control-Allow-Origin: *\r\nConnection: close\r\n\r\n"
              % (status, content_type, len(body))).encode()
    conn.sendall(header + body)


def run_server():
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(addr)
    srv.listen(3)
    srv.settimeout(REFRESH)        # 방문자가 없어도 주기적으로 깨어나 날씨를 갱신
    print("대시보드 열림 — 위 주소로 접속하세요 (Ctrl+C로 종료)")
    while True:
        refresh_if_due()
        try:
            conn, _ = srv.accept()
        except OSError:            # accept 타임아웃 → 위로 올라가 날씨 갱신
            continue
        try:
            req = conn.recv(512).decode("utf-8", "ignore")
            if "GET /data" in req:
                send_response(conn, "200 OK", "application/json", data_json().encode())
            else:
                send_response(conn, "200 OK", "text/html; charset=utf-8", HTML)
        except Exception as e:
            print("요청 처리 오류:", e)
        finally:
            conn.close()


ip = connect_wifi()
if ip:
    refresh()
    print("대시보드 주소:  http://%s" % ip)
    run_server()
