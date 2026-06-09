# -*- coding: utf-8 -*-
"""노션 스타일 코드·프롬프트 페이지 생성기 (Ch1·2·3)"""
import json, html, re, os

# ---------- Chapter 1: astro 원고에서 추출 ----------
ch1_raw = json.load(open("/tmp/ch1_extract.json", encoding="utf-8"))

def ch1_sections():
    secs = []
    for u in ch1_raw:
        # "Unit 1-1. 피코와 첫 만남" → 제목 정리
        t = u["title"].replace("🔥", "").replace("🎯", "").strip()
        items = []
        for p in u["prompts"]:
            items.append({"type": "prompt", "label": f"샘플 프롬프트 {p['id']}", "text": p["text"]})
        for b in u["blocks"]:
            items.append({"type": "code", "label": b["label"], "lang": b["lang"], "code": b["code"]})
        if items:
            secs.append({"title": t, "items": items})
    return secs

# ---------- Chapter 2 ----------
CH2 = [
 ("활동 1 · 주변 와이파이 확인", [
   {"type":"code","label":"와이파이 스캔 (셸에서 한 줄씩)","lang":"python","code":
"""import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True); print(wlan.scan())"""},
 ]),
 ("1·2단계 · 손 코딩으로 측정 확인", [
   {"type":"code","label":"코드 블록 1 · 와이파이 연결하고 신호 세기 읽기 (main.py)","lang":"python","code":
"""import network, time
SSID = "your_wifi"          # 연결할 와이파이 이름 (2.4GHz)
PASSWORD = "your_password"  # 와이파이 비밀번호
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    time.sleep(1)
print("연결됨! IP:", wlan.ifconfig()[0])
while True:
    rssi = wlan.status('rssi')
    print("신호 세기:", rssi)
    time.sleep(1)"""},
   {"type":"code","label":"코드 블록 2 · 설정 파일 분리하기 (wifi_config.py)","lang":"python","code":
"""# 1) 새 파일 wifi_config.py 를 만들어 이렇게만 적습니다
SSID = "your_wifi"
PASSWORD = "your_password"

# 2) main.py 의 맨 위에서 불러옵니다
from wifi_config import SSID, PASSWORD"""},
 ]),
 ("3단계 · 바이브 코딩으로 웹앱 만들기", [
   {"type":"prompt","label":"AI 도구에게 이렇게 부탁해 보세요","text":
"""지금 피코가 wifi_config.py로 와이파이에 연결하고 wlan.status('rssi')로 신호 세기를 읽고 있어.
이 신호 세기를, 같은 와이파이에 연결된 스마트폰 브라우저에서 볼 수 있는 웹 화면으로 만들어 줘.
피코가 직접 웹서버가 되는 방식(소켓 기반)으로, 외부 라이브러리 없이 만들어 줘."""},
 ]),
 ("6단계 · 살아 움직이는 대시보드로 업그레이드", [
   {"type":"prompt","label":"AI 도구에게 이렇게 부탁해 보세요","text":
"""지금 만든 피코 웹앱을 업그레이드해 줘.
1) 새로고침을 누르지 않아도 5초마다 화면이 저절로 갱신되게 해 줘.
2) 최근 20개의 신호 세기 값을 막대그래프로 보여 줘.
3) 다만 피코가 버거워하지 않도록, 주변 와이파이를 전부 훑는 작업은 30초에 한 번만 하게 해 줘."""},
   {"type":"code","label":"코드 블록 3 · 피코 웹서버 (main.py)","lang":"python","code":
"""import network, socket, time
from wifi_config import SSID, PASSWORD
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    time.sleep(1)
ip = wlan.ifconfig()[0]
print("브라우저에서 접속:", "http://" + ip)
history = []
def make_page(rssi, hist):
    bars = ""
    for v in hist:
        h = max(8, min(100, (v + 90) * 2))
        bars += "<div class='bar' style='height:%dpx'></div>" % h
    return PAGE % (rssi, bars)
s = socket.socket()
s.bind(("0.0.0.0", 80))
s.listen(1)
while True:
    cl, addr = s.accept()
    cl.recv(1024)
    rssi = wlan.status("rssi")
    history.append(rssi)
    if len(history) > 20:
        history.pop(0)
    cl.send("HTTP/1.1 200 OK\\r\\nContent-Type: text/html\\r\\n\\r\\n")
    cl.send(make_page(rssi, history))
    cl.close()"""},
   {"type":"code","label":"코드 블록 4 · 브라우저에 보여 줄 화면 (PAGE 템플릿)","lang":"html","code":
"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="5">
  <title>우리 집 와이파이 탐험대</title>
  <style>
    body { font-family: sans-serif; background:#FFF6F9; text-align:center; }
    .rssi { font-size:48px; color:#D4537E; font-weight:bold; }
    .chart { display:flex; align-items:flex-end; height:110px;
             gap:3px; justify-content:center; }
    .bar { width:12px; background:#F4C0D1; border-radius:4px; }
  </style>
</head>
<body>
  <h2>지금 신호 세기</h2>
  <p class="rssi">%d dBm</p>
  <div class="chart">%s</div>
  <p>5초마다 저절로 새로고침돼요</p>
</body>
</html>"""},
 ]),
]

# ---------- Chapter 3 ----------
CH3 = [
 ("3.2 LED 다루기 · 빛으로 표현하기", [
   {"type":"code","label":"코드 1 · LED 한 칸 켜기","lang":"python","code":
"""from machine import Pin
from neopixel import NeoPixel
np = NeoPixel(Pin(16), 10)   # GP16, LED 10개
np[0] = (50, 0, 0)           # 첫 번째 칸 빨강
np.write()"""},
   {"type":"code","label":"코드 2 · 전체를 한 색으로 (fill 함수)","lang":"python","code":
"""from machine import Pin
from neopixel import NeoPixel
import time
NUM = 10
np = NeoPixel(Pin(16), NUM)
def fill(color):
    for i in range(NUM):
        np[i] = color
    np.write()
fill((0, 40, 0))   # 전체 초록
time.sleep(1)
fill((0, 0, 0))    # 전체 끄기"""},
   {"type":"code","label":"코드 3 · 게이지처럼 칸 수 조절하기","lang":"python","code":
"""def gauge(level):
    # level: 0~10, 켤 칸 수
    for i in range(NUM):
        if i < level:
            np[i] = (0, 40, 0)   # 켜진 칸: 초록
        else:
            np[i] = (0, 0, 0)    # 꺼진 칸
    np.write()
for n in range(0, 11):
    gauge(n)
    time.sleep(0.2)"""},
 ]),
 ("3.3 가스 센서 · 공기를 숫자로", [
   {"type":"code","label":"코드 4 · 한 번 읽기","lang":"python","code":
"""from machine import ADC, Pin
gas = ADC(Pin(26))        # GP26 = ADC0
value = gas.read_u16()    # 0 ~ 65535
print(value)"""},
   {"type":"code","label":"코드 5 · 반복해서 읽기 (플로터로 보기)","lang":"python","code":
"""from machine import ADC, Pin
import time
gas = ADC(Pin(26))
while True:
    value = gas.read_u16()
    print(value)          # Thonny 플로터로 그래프 보기
    time.sleep(0.5)"""},
   {"type":"code","label":"코드 6 · 이동 평균으로 안정시키기","lang":"python","code":
"""def read_average(sensor, count=10):
    total = 0
    for _ in range(count):
        total += sensor.read_u16()
        time.sleep_ms(10)
    return total // count
while True:
    avg = read_average(gas, 10)
    print(avg)
    time.sleep(0.5)"""},
 ]),
 ("3.4 둘을 잇기 · LED 게이지", [
   {"type":"code","label":"코드 7 · 가스 값 → LED 게이지 (main.py)","lang":"python","code":
"""from machine import ADC, Pin
from neopixel import NeoPixel
import time
gas = ADC(Pin(26))
np = NeoPixel(Pin(16), 10)
SAFE = 15000      # 이 아래는 안전
DANGER = 30000    # 이 위는 위험
def read_average(s, count=10):
    total = 0
    for _ in range(count):
        total += s.read_u16(); time.sleep_ms(10)
    return total // count
def show_gauge(value):
    # 값을 0~10칸으로 바꾸기
    level = int((value - SAFE) / (DANGER - SAFE) * 10)
    level = max(0, min(10, level))
    for i in range(10):
        if i >= level:        np[i] = (0, 0, 0)
        elif i < 6:           np[i] = (0, 40, 0)   # 초록
        elif i < 8:           np[i] = (40, 30, 0)  # 노랑
        else:                 np[i] = (40, 0, 0)   # 빨강
    np.write()
while True:
    value = read_average(gas, 10)
    print(value)
    if value >= DANGER:
        for _ in range(3):                 # 위험! 전체 빨강 깜빡
            for i in range(10): np[i] = (60, 0, 0)
            np.write(); time.sleep(0.2)
            for i in range(10): np[i] = (0, 0, 0)
            np.write(); time.sleep(0.2)
    else:
        show_gauge(value)
    time.sleep(0.5)"""},
 ]),
 ("3.5 웹 대시보드까지 (바이브 코딩)", [
   {"type":"prompt","label":"AI 도구에게 이렇게 부탁해 보세요","text":
"""지금 피코가 MQ2 값을 read_average로 읽고, show_gauge로 LED 게이지를 켜고 있어.
여기에 Chapter 2처럼 웹 대시보드를 더해 줘. 같은 와이파이의 스마트폰에서 접속하면,
지금 가스 값, 안전/주의/위험 상태, 그리고 최근 20개 값의 막대그래프가 보이게 해 줘.
LED 게이지와 웹 화면이 같은 값으로 동시에 갱신되고, 5초마다 저절로 새로고침되게 해 줘."""},
   {"type":"prompt","label":"AI 도구에게 이렇게 다듬어 달라고 해보세요","text":
"""\"게이지가 한 칸씩 바뀔 때 부드럽게 채워지게 해 줘\"
\"위험할 때 깜빡이는 속도를 더 빠르게 해 줘\"
— 동작을 우리말로 부탁하면 AI가 코드를 고쳐 줍니다. 받은 코드가 내 기준값과 맞는지 꼭 확인하세요."""},
   {"type":"code","label":"코드 8 · LED와 웹을 함께 갱신하는 핵심 부분","lang":"python","code":
"""# (와이파이 연결은 Chapter 2의 wifi_config.py 방식 그대로)
while True:
    cl, addr = s.accept()
    cl.recv(1024)
    value = read_average(gas, 10)
    history.append(value)
    if len(history) > 20:
        history.pop(0)
    show_gauge(value)              # LED도 함께 갱신
    cl.send("HTTP/1.1 200 OK\\r\\nContent-Type: text/html\\r\\n\\r\\n")
    cl.send(make_page(value, history))
    cl.close()"""},
 ]),
]

def tup(sec_list):
    return [{"title":t, "items":items} for (t, items) in sec_list]

CHAPTERS = [
  {"id":"ch1","num":"01","title":"피코와 첫 걸음","subtitle":"피코·MicroPython·Thonny 첫 만남부터 Wi-Fi 감도 웹 대시보드까지 — 손 코딩으로 기초를 다지고 바이브 코딩으로 도약합니다.","accent":"#5B6CF0","sections":ch1_sections()},
  {"id":"ch2","num":"02","title":"우리 집 와이파이 탐험대","subtitle":"와이파이 신호 세기(RSSI)를 측정해 실시간 대시보드로 만듭니다.","accent":"#E0568A","sections":tup(CH2)},
  {"id":"ch3","num":"03","title":"우리 교실 공기 지킴이","subtitle":"가스 센서와 LED 게이지를 잇고, 웹 대시보드로 공기 상태를 보여 줍니다.","accent":"#1F9D63","sections":tup(CH3)},
]

# ---------- 통계 ----------
n_code = sum(1 for c in CHAPTERS for s in c["sections"] for it in s["items"] if it["type"]=="code")
n_prompt = sum(1 for c in CHAPTERS for s in c["sections"] for it in s["items"] if it["type"]=="prompt")

def esc(s): return html.escape(s, quote=True)
def slug(s):
    return re.sub(r'[^a-z0-9가-힣]+','-', s.lower()).strip('-')

# ---------- HTML 생성 ----------
def render():
    nav, main = [], []
    for c in CHAPTERS:
        nav.append(f'<div class="nav-ch"><a href="#{c["id"]}" class="nav-ch-link" data-target="{c["id"]}"><span class="nav-dot" style="background:{c["accent"]}"></span>{esc(c["title"])}</a><div class="nav-secs">')
        sec_html = []
        for si, s in enumerate(c["sections"]):
            sid = f'{c["id"]}-{si}'
            nav.append(f'<a href="#{sid}" class="nav-sec" data-target="{sid}">{esc(s["title"])}</a>')
            items_html = []
            for it in s["items"]:
                if it["type"]=="code":
                    code = esc(it["code"])
                    tag = it["lang"].upper()
                    items_html.append(f'''<div class="block code-block">
<div class="block-head"><span class="block-label">{esc(it["label"]) if it["label"] else "코드"}</span><span class="lang-tag">{tag}</span><button class="copy-btn" aria-label="복사">복사</button></div>
<pre><code class="language-{it["lang"]}">{code}</code></pre></div>''')
                else:
                    items_html.append(f'''<div class="block prompt-block" style="--accent:{c["accent"]}">
<div class="block-head"><span class="prompt-ico">🤖</span><span class="block-label">{esc(it["label"])}</span><button class="copy-btn" aria-label="복사">복사</button></div>
<div class="prompt-body">{esc(it["text"])}</div></div>''')
            sec_html.append(f'''<section class="sec" id="{sid}"><h3 class="sec-title">{esc(s["title"])}</h3>{"".join(items_html)}</section>''')
        nav.append('</div></div>')
        main.append(f'''<div class="chapter" id="{c["id"]}">
<div class="ch-head"><span class="ch-num" style="color:{c["accent"]}">CHAPTER {c["num"]}</span>
<h2 class="ch-title"><span class="ch-bar" style="background:{c["accent"]}"></span>{esc(c["title"])}</h2>
<p class="ch-sub">{esc(c["subtitle"])}</p></div>
{"".join(sec_html)}</div>''')

    return TEMPLATE.format(nav="".join(nav), main="".join(main),
                           n_code=n_code, n_prompt=n_prompt)

TEMPLATE = r'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>피코 바이브 코딩 · 코드 & 프롬프트 모음</title>
<meta name="description" content="라즈베리파이 피코로 배우는 피지컬 컴퓨팅 — Chapter 1·2·3에 쓰이는 모든 MicroPython 코드와 AI 샘플 프롬프트 모음.">
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/github.min.css">
<style>
:root{{
  --bg:#ffffff; --fg:#37352f; --muted:#7b7872; --line:#ededec;
  --sidebar:#fbfbfa; --code-bg:#f7f6f3; --radius:10px;
  --font:'Pretendard',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  --mono:'SFMono-Regular',ui-monospace,Menlo,Consolas,'D2Coding',monospace;
}}
*{{box-sizing:border-box;}}
html{{scroll-behavior:smooth;}}
body{{margin:0;font-family:var(--font);color:var(--fg);background:var(--bg);line-height:1.6;-webkit-font-smoothing:antialiased;}}
a{{color:inherit;text-decoration:none;}}
.layout{{display:flex;max-width:1180px;margin:0 auto;}}
/* 사이드바 */
.sidebar{{position:sticky;top:0;height:100vh;width:280px;flex:0 0 280px;overflow-y:auto;
  background:var(--sidebar);border-right:1px solid var(--line);padding:26px 16px 60px;}}
.brand{{font-weight:800;font-size:15px;padding:6px 10px 14px;letter-spacing:-.02em;}}
.brand small{{display:block;font-weight:500;color:var(--muted);font-size:12px;margin-top:3px;}}
.nav-ch{{margin-top:10px;}}
.nav-ch-link{{display:flex;align-items:center;gap:8px;font-weight:700;font-size:13.5px;padding:7px 10px;border-radius:7px;}}
.nav-ch-link:hover{{background:#efefee;}}
.nav-dot{{width:9px;height:9px;border-radius:50%;flex:0 0 9px;}}
.nav-secs{{display:flex;flex-direction:column;margin:2px 0 8px 18px;border-left:1px solid var(--line);}}
.nav-sec{{font-size:12.5px;color:var(--muted);padding:5px 10px;border-left:2px solid transparent;margin-left:-1px;}}
.nav-sec:hover{{color:var(--fg);}}
.nav-sec.active{{color:var(--fg);font-weight:600;border-left-color:var(--fg);}}
/* 본문 */
.main{{flex:1;min-width:0;padding:0 56px 120px;}}
.hero{{padding:64px 0 30px;border-bottom:1px solid var(--line);margin-bottom:18px;}}
.hero h1{{font-size:38px;font-weight:800;letter-spacing:-.03em;margin:0 0 14px;line-height:1.2;}}
.hero p{{font-size:15.5px;color:var(--muted);margin:0 0 22px;max-width:640px;}}
.stats{{display:flex;gap:10px;flex-wrap:wrap;}}
.stat{{display:flex;align-items:baseline;gap:7px;background:var(--code-bg);border:1px solid var(--line);
  border-radius:999px;padding:7px 15px;font-size:13px;color:var(--muted);}}
.stat b{{font-size:15px;color:var(--fg);font-weight:800;}}
.chapter{{padding-top:30px;}}
.ch-head{{margin:40px 0 8px;}}
.ch-num{{font-size:12px;font-weight:800;letter-spacing:.12em;}}
.ch-title{{display:flex;align-items:center;gap:12px;font-size:27px;font-weight:800;letter-spacing:-.02em;margin:6px 0 8px;}}
.ch-bar{{width:5px;height:26px;border-radius:3px;flex:0 0 5px;}}
.ch-sub{{color:var(--muted);font-size:14.5px;margin:0 0 6px;max-width:660px;}}
.sec{{padding-top:14px;}}
.sec-title{{font-size:16.5px;font-weight:700;margin:26px 0 12px;letter-spacing:-.01em;}}
/* 블록 공통 */
.block{{border:1px solid var(--line);border-radius:var(--radius);margin:12px 0;overflow:hidden;background:#fff;}}
.block-head{{display:flex;align-items:center;gap:9px;padding:9px 13px;background:var(--code-bg);border-bottom:1px solid var(--line);}}
.block-label{{font-size:12.5px;font-weight:600;color:#55524c;flex:1;min-width:0;}}
.lang-tag{{font-family:var(--mono);font-size:10.5px;font-weight:700;color:var(--muted);
  background:#fff;border:1px solid var(--line);border-radius:5px;padding:1px 7px;letter-spacing:.04em;}}
.copy-btn{{font-family:var(--font);font-size:11.5px;font-weight:600;color:var(--muted);cursor:pointer;
  background:#fff;border:1px solid var(--line);border-radius:6px;padding:4px 11px;transition:.15s;flex:0 0 auto;}}
.copy-btn:hover{{color:var(--fg);border-color:#d6d5d2;}}
.copy-btn.done{{color:#0a7f54;border-color:#9bd9bd;background:#f0faf5;}}
.code-block pre{{margin:0;padding:16px 18px;overflow-x:auto;background:#fff;}}
.code-block code{{font-family:var(--mono);font-size:13px;line-height:1.62;background:none;padding:0;}}
/* 프롬프트 콜아웃 */
.prompt-block{{border-color:color-mix(in srgb,var(--accent) 30%,var(--line));}}
.prompt-block .block-head{{background:color-mix(in srgb,var(--accent) 8%,#fff);
  border-bottom-color:color-mix(in srgb,var(--accent) 18%,var(--line));}}
.prompt-block .block-label{{color:color-mix(in srgb,var(--accent) 55%,#37352f);}}
.prompt-ico{{font-size:15px;}}
.prompt-body{{font-family:var(--mono);font-size:13px;line-height:1.7;color:#3a3833;
  white-space:pre-wrap;word-break:break-word;padding:15px 18px;
  background:color-mix(in srgb,var(--accent) 4%,#fff);}}
footer{{margin-top:60px;padding-top:24px;border-top:1px solid var(--line);color:var(--muted);font-size:12.5px;}}
/* 모바일 토글 */
.menu-btn{{display:none;position:fixed;top:14px;left:14px;z-index:50;background:#fff;border:1px solid var(--line);
  border-radius:9px;width:42px;height:42px;font-size:18px;cursor:pointer;box-shadow:0 2px 10px rgba(0,0,0,.07);}}
.scrim{{display:none;}}
@media(max-width:920px){{
  .main{{padding:0 22px 100px;}}
  .hero{{padding-top:74px;}}
  .hero h1{{font-size:30px;}}
  .menu-btn{{display:block;}}
  .sidebar{{position:fixed;left:0;top:0;z-index:45;transform:translateX(-100%);transition:.25s;box-shadow:0 0 40px rgba(0,0,0,.12);}}
  .sidebar.open{{transform:none;}}
  .scrim.show{{display:block;position:fixed;inset:0;background:rgba(0,0,0,.3);z-index:44;}}
}}
</style>
</head>
<body>
<button class="menu-btn" id="menuBtn" aria-label="메뉴">☰</button>
<div class="scrim" id="scrim"></div>
<div class="layout">
  <aside class="sidebar" id="sidebar">
    <div class="brand">🔌 피코 바이브 코딩<small>코드 &amp; 프롬프트 모음 · Ch 1·2·3</small></div>
    {nav}
  </aside>
  <main class="main">
    <header class="hero">
      <h1>피코 바이브 코딩<br>코드 &amp; 프롬프트 모음</h1>
      <p>라즈베리파이 피코로 배우는 피지컬 컴퓨팅. Chapter 1·2·3에 쓰이는 모든 MicroPython 코드와 AI 샘플 프롬프트를 한곳에 모았습니다. 각 블록의 <b>복사</b> 버튼으로 바로 가져다 쓰세요.</p>
      <div class="stats">
        <div class="stat"><b>3</b>개 챕터</div>
        <div class="stat"><b>{n_code}</b>개 코드 블록</div>
        <div class="stat"><b>{n_prompt}</b>개 샘플 프롬프트</div>
      </div>
    </header>
    {main}
    <footer>
      라즈베리파이 피코 · MicroPython · Thonny &nbsp;·&nbsp; 손 코딩 → 바이브 코딩<br>
      이 페이지의 코드와 프롬프트는 수업 자료로 자유롭게 활용할 수 있습니다.
    </footer>
  </main>
</div>
<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js"></script>
<script>
hljs.configure({{cssSelector:'pre code'}});
document.querySelectorAll('pre code').forEach(el=>hljs.highlightElement(el));
// 복사 버튼
document.querySelectorAll('.block').forEach(block=>{{
  const btn=block.querySelector('.copy-btn'); if(!btn) return;
  btn.addEventListener('click',()=>{{
    const code=block.querySelector('code');
    const body=block.querySelector('.prompt-body');
    const text=code?code.innerText:(body?body.innerText:'');
    navigator.clipboard.writeText(text).then(()=>{{
      btn.textContent='복사됨'; btn.classList.add('done');
      setTimeout(()=>{{btn.textContent='복사'; btn.classList.remove('done');}},1400);
    }});
  }});
}});
// 모바일 메뉴
const sb=document.getElementById('sidebar'),scrim=document.getElementById('scrim'),mb=document.getElementById('menuBtn');
function toggle(o){{sb.classList.toggle('open',o);scrim.classList.toggle('show',o);}}
mb.addEventListener('click',()=>toggle(!sb.classList.contains('open')));
scrim.addEventListener('click',()=>toggle(false));
sb.addEventListener('click',e=>{{if(e.target.closest('a')&&window.innerWidth<=920)toggle(false);}});
// 스크롤스파이
const secs=[...document.querySelectorAll('.sec, .chapter')];
const links=new Map();
document.querySelectorAll('.nav-sec,.nav-ch-link').forEach(a=>links.set(a.dataset.target,a));
const io=new IntersectionObserver(es=>{{
  es.forEach(e=>{{if(e.isIntersecting){{
    document.querySelectorAll('.nav-sec.active').forEach(x=>x.classList.remove('active'));
    const l=links.get(e.target.id); if(l&&l.classList.contains('nav-sec'))l.classList.add('active');
  }}}});
}},{{rootMargin:'-10% 0px -80% 0px',threshold:0}});
secs.forEach(s=>io.observe(s));
</script>
</body>
</html>'''

open("/Users/greatsong/2026-vibe-pico/index.html","w",encoding="utf-8").write(render())
print(f"생성 완료 · 코드 {n_code}개 · 프롬프트 {n_prompt}개")
