# -*- coding: utf-8 -*-
"""오픈 API 라이브 대시보드 생성기 → dashboards/*.html

API별로 브라우저에서 직접 데이터를 받아(fetch) 그리는 샘플 대시보드 한 장씩.
각 페이지: API 기본 정보 + 라이브 대시보드 + 응용 가능성.
모두 CORS 허용을 확인한 API만 사용(브라우저에서 바로 호출 가능).
"""
import os
BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "dashboards")
os.makedirs(OUT, exist_ok=True)

CHART = '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>'
LEAFLET = ('<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">'
           '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>')

def page(slug, emoji, title, subject, region, info, apply_html, body, js, chart=False, lead="",
         src_name="", src_url="", refs=(), maps=False, head=""):
    src = (f'<a class="srclink" href="{src_url}" target="_blank" rel="noopener">🔗 원 데이터 출처: {src_name} ↗</a>'
           if src_url else "")
    refhtml = ""
    if refs:
        chips = "".join(f'<a class="refchip" href="{u}" target="_blank" rel="noopener">{l}</a>' for l, u in refs)
        refhtml = f'<div class="refs"><span class="refs-t">📺 더 보기</span>{chips}</div>'
    import html as _h
    corehtml = ""
    _core = CORE.get(slug, "")
    if _core:
        corehtml = (
            '<section class="card core"><h2>🐍 API 핵심 코드 '
            '<span class="hint">— 복사해 내 프로젝트·AI에 응용</span></h2>'
            '<p class="coreintro">이 데이터를 받아오는 <b>핵심만</b> 추린 파이썬 코드예요'
            '(<code>requests</code> 사용). <b>Streamlit</b> 앱에 바로 쓰거나, 복사해서 '
            'AI(Claude 등)에게 “이 데이터로 ___ 만들어 줘”처럼 넘기면 됩니다.</p>'
            '<p class="corenote">📦 <b>Streamlit Cloud에 배포</b>한다면 <code>requirements.txt</code>에 '
            '<code>requests</code>를 한 줄 적어 주세요 (없으면 <code>ModuleNotFoundError</code>).</p>'
            '<details class="corefold"><summary>💻 파이썬 코드 보기 · 복사</summary>'
            '<div class="vibebox"><div class="vibehead">'
            f'<span class="vibelabel">{title} · Python (requests)</span>'
            '<button class="vibecopy" onclick="corecopy(this)">복사</button></div>'
            f'<pre class="vibetext">{_h.escape(_core)}</pre></div></details></section>')
    promptshtml = ""
    _pr = PROMPTS.get(slug, ())
    if _pr:
        import html as _h
        common = (
            '<details class="vibecommon"><summary>🔧 공통 조건 — 아래 모든 프롬프트에 자동 포함 (펼쳐 보기)</summary>'
            '<div class="vibebox"><div class="vibehead"><span class="vibelabel">공통 조건 · 피코·와이파이·LED</span>'
            '<button class="vibecopy" onclick="vcopypre(this)">복사</button></div>'
            f'<pre id="vibepre" class="vibetext">{_h.escape(PICO_PRE)}</pre></div></details>')
        boxes = []
        for label, text in _pr:
            boxes.append(
                '<div class="vibebox"><div class="vibehead">'
                f'<span class="vibelabel">{label}</span>'
                '<button class="vibecopy" onclick="vcopy(this)">복사</button></div>'
                f'<pre class="vibetext">{_h.escape(text)}</pre></div>')
        promptshtml = (
            '<section class="card vibe"><h2>🤖 바이브코딩 프롬프트 '
            '<span class="hint">— 복사해 AI(Claude 등)에 붙여넣기</span></h2>'
            '<p class="vibeintro">이 데이터를 받아 <b>라즈베리파이 피코·LED</b>로 만드는 코드를 받을 수 있어요. '
            '각 프롬프트의 <b>[복사]</b>를 누르면 위 <b>공통 조건</b>(피코·와이파이·LED 설정)까지 함께 복사돼, '
            '<b>아무 맥락 없는 새 대화</b>에 그대로 붙여넣을 수 있어요.</p>'
            + common + "".join(boxes) + '</section>')
    html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" type="image/svg+xml" href="../favicon.svg">
<title>{title} · 라이브 대시보드</title>
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<link rel="stylesheet" href="lab.css">
{CHART if chart else ""}
{LEAFLET if maps else ""}
{head}
</head>
<body>
<div class="wrap">
  <a class="back" href="index.html">← 대시보드 갤러리</a>
  <header class="phead">
    <div class="bigemoji">{emoji}</div>
    <h1>{title}</h1>
    <div class="tags"><span class="tag subj">{subject}</span><span class="tag region">{region}</span></div>
  </header>

  <section class="card info">
    <h2>📋 어떤 데이터인가요?</h2>
    {f'<p class="lead">{lead}</p>' if lead else ""}
    {info}
    {src}
    {refhtml}
  </section>

  <section class="card live">
    <h2>📡 라이브 대시보드 <span class="hint">— 지금 데이터를 받아옵니다</span></h2>
    {body}
  </section>

  {corehtml}

  <section class="card apply">
    <h2>💡 이렇게 응용해 보세요</h2>
    {apply_html}
  </section>

  {promptshtml}

  <footer>데이터 기반 탐구 프로젝트 · 바이브 피지컬 코딩 &nbsp;|&nbsp; 데이터는 각 API 제공처의 것입니다.</footer>
</div>
{COPY_JS}
<script>
{js}
</script>
</body>
</html>'''
    with open(os.path.join(OUT, slug + ".html"), "w", encoding="utf-8") as f:
        f.write(html)

# ===================================================================
LAB_CSS = r'''
:root{
  --bg:#f6f7fb; --panel:#ffffff; --ink:#2b2d3a; --muted:#7a7f95; --line:#eceef5;
  --pico1:#5B6CF0; --pico2:#E0568A;
  --font:'Pretendard',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  --mono:'SFMono-Regular',ui-monospace,Menlo,Consolas,monospace;
}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--bg);color:var(--ink);font-family:var(--font);line-height:1.65;-webkit-font-smoothing:antialiased;}
.wrap{max-width:840px;margin:0 auto;padding:18px 16px 80px;}
.back{display:inline-block;color:var(--muted);font-size:13px;font-weight:600;margin:6px 0 14px;}
.back:hover{color:var(--pico1);}
a{text-decoration:none;color:inherit;}
.phead{text-align:center;margin:8px 0 22px;}
.bigemoji{font-size:46px;line-height:1;}
.phead h1{font-size:clamp(22px,5vw,30px);font-weight:800;letter-spacing:-.02em;margin:8px 0 10px;}
.tags{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;}
.tag{font-size:12px;font-weight:700;border-radius:999px;padding:4px 12px;}
.tag.subj{background:#eef0ff;color:#3b47c2;}
.tag.region{background:#fff0f6;color:#b83d72;}
.card{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:20px 22px;margin:14px 0;
  box-shadow:0 4px 18px rgba(40,50,90,.04);}
.card h2{font-size:15px;font-weight:800;margin-bottom:12px;letter-spacing:-.01em;}
.card h2 .hint{font-weight:500;font-size:12px;color:var(--muted);}
.lead{font-size:14.5px;line-height:1.8;color:#3a3d4d;background:linear-gradient(180deg,#f7f8ff,#fff);
  border-left:4px solid #5B6CF0;border-radius:0 12px 12px 0;padding:13px 16px;margin-bottom:14px;}
.lead b{color:#3b47c2;}
.info table{width:100%;border-collapse:collapse;font-size:13.5px;}
.info td{padding:7px 4px;border-bottom:1px solid var(--line);vertical-align:top;}
.info td.k{width:108px;color:var(--muted);font-weight:600;}
.info code,.live code{font-family:var(--mono);font-size:12px;background:#f3f4fa;border:1px solid var(--line);
  border-radius:5px;padding:1px 6px;word-break:break-all;}
.srclink{display:inline-block;margin-top:14px;font-size:13px;font-weight:700;color:#3b47c2;
  background:#eef0ff;border:1px solid #d7defb;border-radius:10px;padding:8px 14px;}
.srclink:hover{background:#e3e7ff;}
.refs{margin-top:12px;display:flex;flex-wrap:wrap;gap:8px;align-items:center;}
.refs-t{font-size:12px;font-weight:700;color:var(--muted);}
.refchip{font-size:12.5px;font-weight:600;color:#b83d72;background:#fff0f6;border:1px solid #f6d3e3;
  border-radius:999px;padding:6px 12px;}
.refchip:hover{background:#ffe3ef;}
/* 소행성 애니메이션 시각화 */
.astro{width:100%;height:auto;background:radial-gradient(120% 140% at 12% 50%,#0b1224,#070a16);
  border:1px solid #1d2540;border-radius:16px;margin:6px 0 6px;}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
@keyframes twinkle{0%,100%{opacity:.55}50%{opacity:1}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes pop{from{opacity:0;transform:scale(.2)}to{opacity:1;transform:scale(1)}}
.ast{animation:bob 4s ease-in-out infinite;transform-box:fill-box;transform-origin:center;}
.ast .rock{transform-box:fill-box;transform-origin:center;}
.ast-pop{animation:pop .5s ease-out both;transform-box:fill-box;transform-origin:center;}
.earthpulse{animation:twinkle 3s ease-in-out infinite;transform-box:fill-box;transform-origin:center;}
.apply ul{margin:0;padding-left:18px;}
.apply li{font-size:14px;margin:7px 0;}
.vibe .vibeintro{font-size:13.5px;color:#3a3d4d;margin-bottom:12px;}
.core .coreintro{font-size:13.5px;color:#3a3d4d;margin-bottom:12px;}
.core .coreintro code,.core .corenote code{font-family:var(--mono);font-size:12.5px;background:#eef0ff;color:#3b47c2;
  padding:1px 6px;border-radius:6px;}
.core .corenote{font-size:12.5px;color:#6b5e2e;background:#fdf8ec;border:1px solid #f0e4c4;
  border-radius:10px;padding:9px 12px;margin-bottom:12px;}
.core .corenote code{background:#f3ead0;color:#7a6a2e;}
.corefold{border:1px dashed #cfd5ef;border-radius:12px;background:#fafbff;}
.corefold summary{cursor:pointer;font-size:12.5px;font-weight:700;color:#3b47c2;padding:11px 13px;list-style:none;}
.corefold summary::-webkit-details-marker{display:none;}
.corefold summary:before{content:'▸ ';}
.corefold[open] summary:before{content:'▾ ';}
.corefold[open] summary{border-bottom:1px solid var(--line);}
.corefold .vibebox{margin:10px;}
.vibecommon{margin:0 0 14px;border:1px dashed #cfd5ef;border-radius:12px;background:#fafbff;}
.vibecommon summary{cursor:pointer;font-size:12.5px;font-weight:700;color:#3b47c2;padding:10px 13px;list-style:none;}
.vibecommon summary::-webkit-details-marker{display:none;}
.vibecommon summary:before{content:'▸ ';}
.vibecommon[open] summary:before{content:'▾ ';}
.vibecommon[open] summary{border-bottom:1px solid var(--line);}
.vibecommon .vibebox{margin:10px;}
.vibebox{border:1px solid var(--line);border-radius:12px;margin:10px 0;overflow:hidden;background:#fbfbfe;}
.vibehead{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:8px 12px;
  background:#f3f4fa;border-bottom:1px solid var(--line);}
.vibelabel{font-size:12.5px;font-weight:700;color:#3b47c2;}
.vibecopy{font-family:var(--font);font-size:12px;font-weight:700;color:#fff;cursor:pointer;border:none;
  border-radius:8px;padding:5px 12px;background:linear-gradient(120deg,var(--pico1),var(--pico2));white-space:nowrap;}
.vibecopy:hover{filter:brightness(1.05);}
.vibecopy.done{background:#22b07d;}
.vibetext{font-family:var(--mono);font-size:12px;line-height:1.6;color:#2b2d3a;white-space:pre-wrap;
  word-break:break-word;padding:12px 14px;margin:0;}
.controls{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:16px;}
.controls input,.controls select{font-family:var(--font);font-size:14px;border:1px solid var(--line);
  border-radius:10px;padding:9px 12px;background:#fff;min-width:0;}
.controls input{width:120px;}
.controls button{font-family:var(--font);font-size:14px;font-weight:700;color:#fff;cursor:pointer;border:none;
  border-radius:10px;padding:9px 18px;background:linear-gradient(120deg,var(--pico1),var(--pico2));}
.controls button:hover{filter:brightness(1.05);}
.controls label{font-size:12.5px;color:var(--muted);font-weight:600;}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:12px;}
.stat{background:#fafbff;border:1px solid var(--line);border-radius:14px;padding:16px;text-align:center;}
.stat .lab{font-size:11px;letter-spacing:1px;color:var(--muted);text-transform:uppercase;}
.stat .val{font-size:30px;font-weight:800;margin-top:6px;line-height:1.1;}
.stat .unit{font-size:11px;color:var(--muted);margin-top:3px;}
.status{font-size:13px;color:var(--muted);padding:8px 0;}
.status.err{color:#d94a5a;}
.chartbox{margin-top:14px;}
.map{height:360px;border-radius:14px;overflow:hidden;border:1px solid var(--line);margin-top:6px;}
.leaflet-popup-content{font-family:var(--font);font-size:13px;}
.qbox{background:linear-gradient(180deg,#fff8fb,#fff);border:1px solid #f6d3e3;border-radius:12px;
  padding:12px 16px;margin-top:14px;}
.qbox-t{font-weight:800;font-size:13px;color:#b83d72;margin-bottom:6px;}
.qbox ul{margin:0;padding-left:18px;}
.qbox li{font-size:13.5px;margin:5px 0;}
.list{list-style:none;padding:0;margin:8px 0 0;}
.list li{display:flex;gap:12px;align-items:baseline;padding:10px 4px;border-bottom:1px solid var(--line);font-size:13.5px;}
.badge{flex:0 0 auto;font-weight:800;font-size:13px;border-radius:8px;padding:3px 9px;color:#fff;}
.list .meta{color:var(--muted);font-size:12px;}
.bigimg{width:100%;border-radius:14px;border:1px solid var(--line);margin-top:8px;display:block;}
.molwrap{display:flex;gap:18px;align-items:center;flex-wrap:wrap;}
.molwrap img{width:180px;height:180px;background:#fff;border:1px solid var(--line);border-radius:14px;}
.seg{display:inline-flex;border:1px solid var(--line);border-radius:11px;overflow:hidden;margin-bottom:14px;}
.seg button{font-family:var(--font);font-size:13px;font-weight:700;border:none;background:#fff;color:var(--muted);padding:9px 18px;cursor:pointer;}
.seg button.seg-on{background:linear-gradient(120deg,var(--pico1),var(--pico2));color:#fff;}
.molimg{width:220px;height:220px;display:block;margin:0 auto;background:#fff;border:1px solid var(--line);border-radius:16px;}
.mol3d{height:340px;position:relative;border-radius:16px;overflow:hidden;border:1px solid var(--line);background:#f4f6fc;}
footer{margin-top:30px;text-align:center;color:var(--muted);font-size:12px;}
.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;}
.gcard{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:18px;transition:.15s;
  box-shadow:0 4px 18px rgba(40,50,90,.04);}
.gcard:hover{transform:translateY(-2px);border-color:#cdd3f3;}
.gcard .ge{font-size:30px;}
.gcard .ge{display:flex;align-items:center;justify-content:space-between;}
.gcard .gt{font-weight:800;font-size:15px;margin:8px 0 4px;}
.gcard .gs{font-size:12.5px;color:var(--muted);}
.gcard .ghook{font-size:12px;color:#3b47c2;margin-top:10px;padding-top:9px;border-top:1px dashed #e6e8f5;line-height:1.5;}
.gmap{font-size:10.5px;font-weight:700;color:#1f7a63;background:#e6f7f0;border:1px solid #c4ebdd;border-radius:999px;padding:2px 8px;}
.steps3{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;margin:4px 0 18px;}
.s3{background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px 16px;position:relative;
  box-shadow:0 4px 18px rgba(40,50,90,.04);}
.s3 .s3n{width:24px;height:24px;border-radius:50%;background:linear-gradient(120deg,var(--pico1),var(--pico2));
  color:#fff;font-weight:800;font-size:13px;text-align:center;line-height:24px;margin-bottom:7px;}
.s3 b{font-size:14px;}
.s3 span{display:block;font-size:12px;color:var(--muted);margin-top:3px;line-height:1.5;}
.recgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;}
.reccard{display:block;background:#fafbff;border:1px solid var(--line);border-radius:12px;padding:13px 15px;transition:.15s;}
.reccard:hover{border-color:#cdd3f3;background:#f4f6ff;}
.reccard .re{font-size:22px;}
.reccard .rt{font-weight:800;font-size:14px;margin:5px 0 2px;}
.reccard .rf{font-size:11.5px;color:#3b47c2;font-weight:600;}
.reccard .rd{font-size:12px;color:var(--muted);margin-top:5px;line-height:1.5;}
.pico-accent{background:linear-gradient(120deg,var(--pico1),var(--pico2));-webkit-background-clip:text;background-clip:text;color:transparent;font-weight:900;}
'''
with open(os.path.join(OUT, "lab.css"), "w", encoding="utf-8") as f:
    f.write(LAB_CSS)

SEOUL = ('<div class="controls">'
         '<label>위도</label><input id="lat" value="37.5665">'
         '<label>경도</label><input id="lon" value="126.9780">'
         '<button onclick="run()">불러오기</button></div>')

# ===================================================================
# 바이브코딩 프롬프트 (각 대시보드 하단에 표시 · [복사] 시 공통 조건이 함께 붙음)
PICO_PRE = (
    "[공통 조건]\n"
    "- 라즈베리파이 피코 2 W(MicroPython)에서 도는 완결형 main.py로 만들어 줘.\n"
    "- 인터넷 접속은 외부 라이브러리 없이 피코 기본 내장 socket+ssl만 사용(requests 설치 금지). https는 인증서 검증 생략(CERT_NONE).\n"
    "- 와이파이는 wifi_config.py 파일에 WIFI_SSID, WIFI_PASSWORD 두 변수로 저장해 두고 거기서 불러와.\n"
    "- WS2813 LED 10개는 GP16에 연결, NeoPixel을 timing=(280,515,515,745)로 생성(없으면 색 깨짐), 밝기는 낮게(최대 60 정도).\n"
    "- 응답이 크면 필요한 항목만 받아 메모리를 아끼고, 무한 루프엔 sleep으로 쉬어 줘."
)

COPY_JS = (
    "<script>"
    "function _vflash(b){var o=b.textContent;b.textContent='복사됨!';b.classList.add('done');"
    "setTimeout(function(){b.textContent=o;b.classList.remove('done');},1200);}"
    "function _vfallback(t,b){try{var ta=document.createElement('textarea');ta.value=t;"
    "ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();"
    "document.execCommand('copy');document.body.removeChild(ta);_vflash(b);}"
    "catch(e){window.prompt('아래 내용을 복사하세요 (Ctrl/\\u2318+C):',t);}}"
    "function _vwrite(t,b){if(navigator.clipboard&&navigator.clipboard.writeText){"
    "navigator.clipboard.writeText(t).then(function(){_vflash(b);},function(){_vfallback(t,b);});}"
    "else{_vfallback(t,b);}}"
    "function vcopypre(b){var p=document.getElementById('vibepre');_vwrite(p?p.textContent:'',b);}"
    "function vcopy(b){var s=b.closest('.vibebox').querySelector('.vibetext').textContent;"
    "var p=document.getElementById('vibepre');var pre=p?p.textContent.replace(/\\s+$/,'')+'\\n\\n':'';"
    "_vwrite(pre+s,b);}"
    "function corecopy(b){var s=b.closest('.vibebox').querySelector('.vibetext').textContent;_vwrite(s,b);}"
    "</script>"
)

PROMPTS = {
  "weather": [
    ("강수확률 → LED 날씨 시계",
     "[API] Open-Meteo(키 불필요): GET https://api.open-meteo.com/v1/forecast?latitude=LAT&longitude=LON&hourly=precipitation_probability&timezone=Asia%2FSeoul&forecast_days=1 → 응답의 hourly.precipitation_probability 는 0~23시 24개 강수확률(%) 배열, hourly.time 은 같은 길이의 시각 배열.\n[만들 것] 오늘 6~23시(18시간)를 LED 10칸에 시간순으로 균등 배분(앞 칸이 이른 시각)해, 각 칸을 그 구간 평균 강수확률로 색칠해 줘. 0~20% 초록(맑음)·21~50% 노랑(흐림)·51~80% 파랑(비 가능)·81~100% 보라(비 확실). 10분마다 다시 받아 갱신.\n[설정] 위도·경도(LAT/LON)는 코드 맨 위 변수로 두고 쉽게 바꿀 수 있게 해 줘. 기본값은 서울(LAT=37.5665, LON=126.9780)."),
    ("현재 기온 → 무드등 색",
     "[API] Open-Meteo(키 불필요): GET https://api.open-meteo.com/v1/forecast?latitude=LAT&longitude=LON&current=temperature_2m&timezone=Asia%2FSeoul → 응답의 current.temperature_2m 가 현재 기온(℃) 숫자 하나.\n[만들 것] LED 10칸을 모두 같은 색 무드등으로 켜 줘. 28℃ 이상 빨강(더움)·16~27℃ 초록(적당)·15℃ 이하 파랑(추움). 10분마다 다시 받아 색을 갱신.\n[설정] 위도·경도(LAT/LON)는 코드 맨 위 변수로 두고 쉽게 바꿀 수 있게 해 줘. 기본값은 서울(LAT=37.5665, LON=126.9780)."),
  ],
  "airquality": [
    ("초미세먼지(PM2.5) → LED 신호등",
     "[API] 키 불필요. GET https://air-quality-api.open-meteo.com/v1/air-quality?latitude=LAT&longitude=LON&current=pm2_5&timezone=Asia%2FSeoul&forecast_days=1 → current.pm2_5(초미세먼지 현재 농도 ㎍/㎥)를 사용해 줘.\n[만들 것] PM2.5 등급을 LED 10칸 신호등으로: 좋음(0~15) 초록·보통(16~35) 노랑·나쁨(36~75) 주황·매우나쁨(76+) 빨강 깜빡. 농도가 높을수록 켜는 칸 수를 늘려(0~150㎍/㎥를 10칸에 비례 매핑) 0칸~10칸으로 표시하고, 10분마다 갱신해 줘.\n[설정] 위도·경도(LAT/LON)는 코드 맨 위 변수로 두고 쉽게 바꿀 수 있게 해 줘. 기본값은 서울(37.5665/126.9780)."),
    ("PM2.5+PM10 → 앞5칸·뒤5칸 동시 표시",
     "[API] 키 불필요. GET https://air-quality-api.open-meteo.com/v1/air-quality?latitude=LAT&longitude=LON&current=pm2_5,pm10&timezone=Asia%2FSeoul&forecast_days=1 → current.pm2_5와 current.pm10(둘 다 현재 농도 ㎍/㎥)를 함께 사용해 줘.\n[만들 것] LED 10칸을 반으로 나눠 앞 5칸은 PM2.5, 뒤 5칸은 PM10 막대그래프로. 각 막대는 등급별 색(좋음 초록·보통 노랑·나쁨 주황·매우나쁨 빨강). PM2.5는 0~75㎍/㎥를 5칸에, PM10은 0~150㎍/㎥를 5칸에 비례 매핑하고, 둘 중 하나라도 매우나쁨이면 해당 막대를 깜빡여 줘. 10분마다 갱신.\n[설정] 위도·경도(LAT/LON)는 코드 맨 위 변수로 두고 쉽게 바꿀 수 있게 해 줘. 기본값은 서울(37.5665/126.9780)."),
    ("시간별 PM2.5 추이 → 흐름 막대",
     "[API] 키 불필요. GET https://air-quality-api.open-meteo.com/v1/air-quality?latitude=LAT&longitude=LON&hourly=pm2_5&timezone=Asia%2FSeoul&forecast_days=1 → hourly.pm2_5(시간별 농도 배열)와 hourly.time(시각 배열)을 사용해 줘.\n[만들 것] hourly.time에서 지금 시각 이후 시각을 찾아, 그때부터 최대 10시간의 PM2.5를 LED 10칸에 시간순으로 한 칸씩 매핑해 각 칸을 그 시각 등급 색(좋음 초록·보통 노랑·나쁨 주황·매우나쁨 빨강)으로 켜서 '대기질 흐름'을 보여 줘. 남은 데이터가 10개보다 적으면 있는 만큼만 켜고 나머지 칸은 꺼 줘. 30분마다 갱신.\n[설정] 위도·경도(LAT/LON)는 코드 맨 위 변수로 두고 쉽게 바꿀 수 있게 해 줘. 기본값은 서울(37.5665/126.9780)."),
  ],
  "earthquake": [
    ("최근 최대 지진 → LED 게이지",
     "[API] 키 불필요. GET https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson → features 배열에서 각 features[i].properties.mag(규모)만 꺼내 최댓값을 구해 줘.\n[만들 것] 최근 하루 M4.5+ 중 최대 규모를 10칸 LED 게이지로(규모 0~9를 0~10칸에 비례, 가득 차면 10칸). 평소 초록, M6+이면 빨강으로 1초 간격 깜빡, 10분마다 다시 불러와 갱신.\n[설정] 감시할 피드는 코드 맨 위 FEED 변수로 두고 쉽게 바꿀 수 있게 해 줘(선택지: 2.5_day, 4.5_day, significant_week, all_day). 기본값은 \"4.5_day\". 깜빡 시작 규모도 ALERT_MAG 변수로 두고 기본값 6.0."),
    ("하루 지진 건수 → 활동 막대",
     "[API] 키 불필요. GET https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson → features 배열의 길이(len)가 최근 하루 M2.5+ 발생 건수야. mag·place는 안 써도 돼.\n[만들 것] 발생 건수를 10칸 LED 막대로 표시(0건=모두 꺼짐, 건수가 늘수록 한 칸씩 채움). 적으면 초록, 중간이면 노랑, 가득 차면 빨강으로 채워 지구가 얼마나 들썩였는지 보여 줘. 10분마다 갱신.\n[설정] 막대가 가득 차는 기준 건수를 코드 맨 위 FULL_COUNT 변수로 두고 쉽게 바꿀 수 있게 해 줘(건수÷FULL_COUNT×10을 칸 수로). 기본값은 50. 피드는 FEED 변수로 두고 기본값 \"2.5_day\"."),
    ("우리 동네 근접 경보 → 거리 LED",
     "[API] 키 불필요. GET https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson → 각 features[i]의 geometry.coordinates([경도, 위도, 깊이])와 properties.mag을 꺼내 줘.\n[만들 것] 내 위치에서 가장 가까운 지진까지의 거리를 10칸 LED로(가까울수록 많이 켜짐: 0km=10칸, 멀수록 줄어 0칸). 평소 파랑, 가장 가까운 지진이 M6+이면 빨강으로 강조. 위경도 거리는 간단한 유클리드 근사로 계산, 10분마다 갱신.\n[설정] 내 위도·경도(MY_LAT/MY_LON)와 LED가 0칸이 되는 경보 반경(RANGE_KM)을 코드 맨 위 변수로 두고 쉽게 바꿀 수 있게 해 줘. 기본값은 서울(MY_LAT=37.5665, MY_LON=126.9780), RANGE_KM=3000."),
  ],
  "iss": [
    ("내 위치 → ISS 머리 위 통과 알림",
     "[API] wheretheiss(키 불필요): GET https://api.wheretheiss.at/v1/satellites/25544 → 응답 JSON(딕셔너리)의 latitude, longitude가 ISS 현재 위치.\n[만들 것] 내 위치(MY_LAT/MY_LON)와 ISS 사이 거리를 구해, 5000km 이상이면 LED 1칸, 가까워질수록 칸을 늘려 500km 이하면 10칸 모두 켜. 200km 이내(머리 위 통과)면 초록으로 0.3초 간격 깜빡 알림. 30초마다 갱신.\n[설정] 내 위도·경도는 코드 맨 위에 MY_LAT/MY_LON 변수로 두고 쉽게 바꿀 수 있게 해 줘. 기본값은 서울(MY_LAT=37.5665 / MY_LON=126.9780)."),
    ("ISS 고도 → 고도 게이지",
     "[API] wheretheiss(키 불필요): GET https://api.wheretheiss.at/v1/satellites/25544 → 응답 JSON의 altitude(고도 km)를 꺼내.\n[만들 것] ISS 고도(보통 400~430km)를 LED 10칸 게이지로 표시: 400km 이하면 1칸, 430km 이상이면 10칸으로 선형 매핑하고, 낮을수록 노랑·높을수록 파랑으로 칸 색을 채워. 30초마다 갱신.\n[설정] 게이지의 최소·최대 고도는 코드 맨 위에 ALT_MIN/ALT_MAX 변수로 두고 바꿀 수 있게 해 줘. 기본값은 ALT_MIN=400, ALT_MAX=430(km)."),
    ("ISS 속도 → 속도 표시등",
     "[API] wheretheiss(키 불필요): GET https://api.wheretheiss.at/v1/satellites/25544 → 응답 JSON의 velocity(속도 km/h)를 꺼내.\n[만들 것] ISS 속도(보통 약 27,500km/h)를 LED 10칸으로 표시: 27000km/h를 기준으로 빠를수록 칸 수를 늘리고, 기준 초과면 빨강·기준 이하면 초록으로 채워. 30초마다 갱신해 속도 변화를 한눈에 보이게.\n[설정] 기준 속도는 코드 맨 위에 SPEED_REF 변수로 두고 쉽게 바꿀 수 있게 해 줘. 기본값은 SPEED_REF=27000(km/h)."),
  ],
  "sunrise": [
    ("낮 길이 → LED 게이지",
     "[API] 키 불필요. GET https://api.sunrise-sunset.org/json?lat=LAT&lng=LON&formatted=0 → results.day_length(낮 길이, 초 단위 정수)만 사용해.\n[만들 것] 낮 길이를 LED 10칸 게이지로 표시해 줘. 8시간(28800초)이면 0칸, 16시간(57600초)이면 10칸으로 비례 환산하고, 길수록 노란색을 더 밝게(밝기는 60 이하). 하루에 1~2번만 갱신하면 되니 갱신 사이에는 길게 sleep.\n[설정] 위도·경도(LAT/LON)는 코드 맨 위 변수로 두고 쉽게 바꿀 수 있게 해 줘. 기본값은 서울(LAT=37.5665, LON=126.9780)."),
    ("일출·일몰 → 시각 LED",
     "[API] 키 불필요. GET https://api.sunrise-sunset.org/json?lat=LAT&lng=LON&formatted=0 → results.sunrise / results.sunset(둘 다 UTC ISO 문자열). UTC라서 한국시간은 여기에 +9시간 해야 해.\n[만들 것] 일출·일몰 시각의 '시(hour)'를 한국시간으로 바꾼 뒤, 일출 시각만큼 앞쪽 LED를, 일몰 시각만큼 뒤쪽 LED를 켜서 낮 구간을 띠처럼 보여 줘(예: 일출 5시·일몰 19시면 0~4번은 끄고 5~10번 켜기 식, 10칸에 맞게 0~24시를 비례 배치). 일출 쪽은 주황, 일몰 쪽은 빨강, 밝기 60 이하. 하루 1~2회 갱신하고 사이에는 길게 sleep.\n[설정] 위도·경도(LAT/LON)는 코드 맨 위 변수로 두고 쉽게 바꿀 수 있게 해 줘. 기본값은 서울(LAT=37.5665, LON=126.9780)."),
  ],
  "spaceweather": [
    ("Kp 지수 → 오로라 경보등",
     "[API] 키 불필요. GET https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json → 딕셔너리 배열, 배열의 마지막 항목에서 \"Kp\"(0~9, 최신 지자기 교란값)와 \"time_tag\"(측정 시각, 3시간 간격)를 꺼내 써.\n[만들 것] 최신 Kp를 LED 10칸에 막대로 표시(Kp 1당 약 1칸, Kp9면 9~10칸 켜짐). Kp가 클수록 색을 초록→노랑→빨강으로 바꾸고, Kp 5 이상이면 보라색으로 전체를 천천히 깜빡여 오로라 경보를 알려 줘. 30분마다 갱신.\n[설정] 오로라 경보 기준값(KP_ALERT)과 갱신 주기(분)는 코드 맨 위 변수로 빼서 쉽게 바꿀 수 있게 해 줘. 기본값은 KP_ALERT=5, 갱신 30분으로 해 줘."),
    ("최근 3회 Kp → 상승·하강 추이 표시등",
     "[API] 키 불필요. GET https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json → 딕셔너리 배열. 배열 끝에서 최근 항목 3개의 \"Kp\" 값(3시간 간격)을 꺼내 비교에 써.\n[만들 것] 가장 최신 Kp를 LED 10칸 막대로 표시하고, 직전 값과 비교해 추이를 색으로 알려 줘: 오르면 빨강, 내리면 파랑, 변화 없으면 초록. 지자기 폭풍이 커지는지(상승) 잦아드는지(하강)를 한눈에 보이게 해. 30분마다 갱신.\n[설정] 비교에 쓸 최근 항목 개수(N_RECENT)와 갱신 주기(분)는 코드 맨 위 변수로 두고 쉽게 바꿀 수 있게 해 줘. 기본값은 N_RECENT=3, 갱신 30분으로 해 줘."),
  ],
  "pubchem": [
    ("물질 이름 목록 → 분자량 LED 게이지",
     "[API] PubChem(키 불필요). GET https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/물질명/property/MolecularWeight/JSON → PropertyTable.Properties[0].MolecularWeight(분자량)을 꺼내 써. 물질명은 영문(water, glucose, caffeine 등).\n[만들 것] 목록의 물질을 하나씩 차례로 조회해서, 분자량을 LED 10칸 게이지로 표시해 줘(0~400을 0~10칸에 매핑, 400 넘으면 10칸 꽉). 가벼운 물질(<100)은 초록, 보통(100~250)은 노랑, 무거운 물질(>250)은 빨강으로 켜 줘. 한 물질당 4초씩 보여 주고, 마지막 물질까지 끝나면 다시 처음부터 반복해.\n[설정] 비교할 물질 목록은 코드 맨 위에 MATERIALS = [\"water\", \"glucose\", \"caffeine\"] 변수로 두고 쉽게 바꿀 수 있게 해 줘. 기본값은 이 세 가지로."),
    ("두 물질 분자량·분자식 → 무거운 쪽 색으로 비교",
     "[API] PubChem(키 불필요). GET https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/물질명/property/MolecularFormula,MolecularWeight/JSON → PropertyTable.Properties[0].MolecularWeight(분자량)과 .MolecularFormula(분자식, 예 C8H10N4O2)를 꺼내 써.\n[만들 것] 두 물질 A·B의 분자량과 분자식을 각각 조회해서, 조회할 때마다 물질명·분자식·분자량을 한 줄씩 print로 보여 줘(분자식 확인용). 그리고 더 무거운 쪽을 LED로 보여 줘: 왼쪽 5칸은 A, 오른쪽 5칸은 B 영역으로 나누고, 더 무거운 물질 쪽 칸들을 파랑으로 환하게, 가벼운 쪽은 어둡게 켜 줘. 두 분자량 차이가 10 미만이면 '비슷함' 의미로 10칸 모두 보라색. 6초마다 다시 조회해서 갱신해.\n[설정] 비교할 두 물질은 코드 맨 위에 MAT_A = \"caffeine\", MAT_B = \"glucose\" 변수로 두고 쉽게 바꿀 수 있게 해 줘. 기본값은 카페인과 포도당으로."),
  ],
  "gbif": [
    ("종 학명 → 관찰 수 자릿수 LED",
     "[API] GBIF(키 불필요): GET https://api.gbif.org/v1/occurrence/search?country=KR&scientificName=SCI_NAME&limit=0 → 응답 JSON의 최상위 count가 그 종의 국내(한국) 관찰 기록 수.\n[만들 것] count의 자릿수만큼 LED를 채워 줘. 국내 기록 수는 보통 1~6자리라 1자리=1칸 ~ 7자리 이상=10칸으로 매핑하고(예: 40,631 → 5자리 → 5칸), 자릿수가 적을수록(1~2칸) 빨강, 중간(3~4칸)은 노랑, 많을수록(5칸 이상) 초록으로 색을 정해 흔할수록 초록이 길게 보이게 해 줘. 시작할 때 한 번만 불러오고 그 상태로 유지해.\n[설정] 학명 SCI_NAME은 코드 맨 위 변수로 두고 쉽게 바꿀 수 있게 해 줘. 기본값은 까치(\"Pica pica\")로 하고, 집비둘기는 \"Columba livia\"처럼 바꾸면 된다고 주석으로 적어 줘."),
    ("두 종 학명 → 누가 더 흔한가 LED",
     "[API] GBIF(키 불필요): 같은 엔드포인트 .../occurrence/search?country=KR&scientificName=SCI_NAME&limit=0 를 두 종에 대해 각각 호출해, 응답 JSON의 최상위 count(국내 관찰 기록 수) 두 개를 비교.\n[만들 것] LED 10칸을 두 종이 count 비율대로 나눠 가져 줘(예: A가 40,000, B가 15,000이면 약 7칸 초록 + 약 3칸 파랑). 더 흔한 쪽 색이 더 길게 켜져 한눈에 승자가 보이게 하고, 두 count의 합이 0이면 전체를 빨강으로 켜서 데이터 없음을 표시해. 시작할 때 한 번만 불러와.\n[설정] 비교할 두 학명을 코드 맨 위 변수 SCI_A, SCI_B로 두고 쉽게 바꾸게 해 줘. 기본값은 까치(\"Pica pica\")와 집비둘기(\"Columba livia\")로 해 줘."),
  ],
  "nasa": [
    ("근접 소행성 → 위험 알림 LED",
     "[API] NASA NeoWs(키 필요, 우선 DEMO_KEY): GET https://api.nasa.gov/neo/rest/v1/feed?start_date=DATE&end_date=DATE&api_key=KEY → start_date와 end_date에 같은 날짜를 넣어 하루치만 조회해. 응답 JSON의 near_earth_objects[DATE] 배열에서 각 항목의 is_potentially_hazardous_asteroid(위험 PHA 여부, true/false)와 estimated_diameter.meters.estimated_diameter_max(최대 지름 m)를 꺼내 써.\n[만들 것] 그날 지구 근접 천체 개수만큼 LED 칸을 켜고(10개 초과면 10칸까지), 위험(PHA) 천체가 하나라도 있으면 빨강 깜빡·없으면 초록 고정. 천체 중 가장 큰 지름이 200m를 넘으면 그 칸만 주황으로 강조해. 하루 1회 갱신.\n[설정] api_key와 조회 날짜는 코드 맨 위 변수(API_KEY/DATE)로 두고 쉽게 바꿀 수 있게 해 줘. 기본값은 API_KEY=\"DEMO_KEY\", DATE=\"2026-06-25\"(YYYY-MM-DD 형식의 고정 문자열). 다른 날을 보려면 DATE만 바꾸면 되게."),
    ("오늘의 천문사진 → 사진 도착 신호등",
     "[API] NASA APOD(키 필요, 우선 DEMO_KEY): GET https://api.nasa.gov/planetary/apod?api_key=KEY → 응답 JSON의 title(제목), media_type(\"image\" 또는 \"video\"), url(사진·영상 주소). explanation(설명)도 함께 옴.\n[만들 것] 오늘의 천문사진이 잘 도착했는지 알리는 신호등: media_type이 \"image\"면 LED 10칸을 은은한 파랑으로 차오르듯 켜고, \"video\"면 보라로 켜. 응답에 title이 비어 있거나 요청 실패면 빨강 1칸으로 표시. 받은 title과 url은 print로 한 번 출력해 줘(LED는 도착 여부만 표현). 하루 1회 갱신.\n[설정] api_key는 코드 맨 위 변수(API_KEY)로 두고 쉽게 바꿀 수 있게 해 줘. 기본값은 API_KEY=\"DEMO_KEY\"."),
  ],
  "energy": [
    ("이번 달 일사량 → 태양광 LED 게이지",
     "[API] 키 불필요. GET https://power.larc.nasa.gov/api/temporal/climatology/point?parameters=ALLSKY_SFC_SW_DWN&community=RE&longitude=LON&latitude=LAT&format=JSON → properties.parameter.ALLSKY_SFC_SW_DWN는 {\"JAN\":..,..,\"DEC\":..,\"ANN\":연평균} 딕셔너리(월평균 일사량 kWh/m²/day).\n[만들 것] 선택한 달(MONTH)의 일사량을 LED 10칸 막대 게이지로. 0~8 kWh/m²/day를 10칸에 매핑(약 0.8당 1칸), 채운 칸은 노란색·빈 칸은 꺼짐. 값이 클수록(여름) 더 많이·노랗게 차오르게. 1시간마다 한 번만 갱신.\n[설정] 위도·경도(LAT/LON)와 조회할 달(MONTH, 1~12)을 코드 맨 위 변수로 두고 쉽게 바꿀 수 있게 해 줘. 기본값은 서울(LAT=37.5665, LON=126.9780), MONTH=6."),
    ("이번 달 풍속 → 풍력 LED 게이지",
     "[API] 키 불필요. GET https://power.larc.nasa.gov/api/temporal/climatology/point?parameters=WS10M&community=RE&longitude=LON&latitude=LAT&format=JSON → properties.parameter.WS10M는 {\"JAN\":..,..,\"DEC\":..,\"ANN\":연평균} 딕셔너리(10m 높이 월평균 풍속 m/s).\n[만들 것] 선택한 달(MONTH)의 풍속을 LED 10칸 게이지로. 0~10 m/s를 10칸에 매핑(1 m/s당 1칸), 채운 칸은 하늘색. 3 m/s 미만이면 1~2칸만 켜고, 6 m/s 이상이면 끝 2칸을 흰색으로 깜빡여 '강풍'을 표시. 1시간마다 갱신.\n[설정] 위도·경도(LAT/LON)와 조회할 달(MONTH, 1~12)을 코드 맨 위 변수로 두고 쉽게 바꿀 수 있게 해 줘. 기본값은 서울(LAT=37.5665, LON=126.9780), MONTH=6."),
    ("태양 vs 바람 → 어느 쪽이 셀까 비교등",
     "[API] 키 불필요. GET https://power.larc.nasa.gov/api/temporal/climatology/point?parameters=ALLSKY_SFC_SW_DWN,WS10M&community=RE&longitude=LON&latitude=LAT&format=JSON → properties.parameter.ALLSKY_SFC_SW_DWN(일사량 kWh/m²/day)와 properties.parameter.WS10M(풍속 m/s) 둘 다 {\"JAN\":..,..,\"DEC\":..,\"ANN\":..} 딕셔너리.\n[만들 것] 선택한 달(MONTH)에서 태양과 바람 중 어느 자원이 상대적으로 강한지 비교. 일사량은 8로, 풍속은 10으로 각각 나눠 0~1 비율로 환산한 뒤, LED 10칸을 절반씩 나눠 왼쪽 5칸은 태양 비율만큼 노랗게·오른쪽 5칸은 바람 비율만큼 하늘색으로 채워. 더 높은 쪽 끝 칸을 1초 간격으로 천천히 깜빡여 '오늘의 승자'를 표시. 1시간마다 갱신.\n[설정] 위도·경도(LAT/LON)와 조회할 달(MONTH, 1~12)을 코드 맨 위 변수로 두고 쉽게 바꿀 수 있게 해 줘. 기본값은 서울(LAT=37.5665, LON=126.9780), MONTH=6."),
  ],
  "worldbank": [
    ("나라 코드 → 1인당 CO₂ LED 게이지",
     "[API] World Bank(키 불필요): GET https://api.worldbank.org/v2/country/KOR/indicator/EN.GHG.CO2.PC.CE.AR5?format=json&per_page=5&mrnev=1 → 응답은 [메타데이터, 데이터배열] 2요소 배열이야. 응답[1]이 데이터배열이고, 응답[1][0]['value']가 1인당 CO₂ 배출량(톤), 응답[1][0]['date']가 연도야. (응답[0]은 메타데이터이니 헷갈리지 마.)\n[만들 것] 한 나라의 1인당 CO₂를 LED 10칸 게이지로 표시(0~20t → 0~10칸, 1칸당 2t). 세계 평균(약 4.5t)보다 높으면 빨강, 낮으면 초록. 하루 1회만 갱신하고 나머지 시간은 sleep.\n[설정] 나라 코드(country)를 코드 맨 위 변수로 두고 쉽게 바꿀 수 있게 해 줘. 기본값은 한국(KOR), 그 외 USA·JPN·CHN 등으로 바꿔 비교하게."),
    ("나라 코드 → 재생에너지 비중 게이지",
     "[API] World Bank(키 불필요): GET https://api.worldbank.org/v2/country/KOR/indicator/EG.FEC.RNEW.ZS?format=json&per_page=5&mrnev=1 → 응답은 [메타데이터, 데이터배열] 2요소 배열이야. 응답[1]이 데이터배열이고, 응답[1][0]['value']가 최종에너지 중 재생에너지 비중(%), 응답[1][0]['date']가 연도야. (응답[0]은 메타데이터.)\n[만들 것] 재생에너지 비중(0~100%)을 LED 10칸 게이지로 표시(10% → 1칸). 높을수록 칸을 많이·초록으로 켜고, 15% 미만이면 빨강으로 경고. 하루 1회만 갱신하고 나머지는 sleep.\n[설정] 나라 코드(country)를 코드 맨 위 변수로 두고 쉽게 바꿀 수 있게 해 줘. 기본값은 한국(KOR), 그 외 NOR·SWE·BRA 등으로 바꿔 비교하게."),
    ("두 나라 → CO₂ 좌우 비교 막대",
     "[API] World Bank(키 불필요): 같은 지표 EN.GHG.CO2.PC.CE.AR5를 두 나라에 각각 GET https://api.worldbank.org/v2/country/{CODE}/indicator/EN.GHG.CO2.PC.CE.AR5?format=json&per_page=5&mrnev=1 → 각 응답은 [메타데이터, 데이터배열] 2요소 배열이고, 응답[1][0]['value']가 그 나라의 1인당 CO₂(톤)야. (응답[0]은 메타데이터.)\n[만들 것] LED 10칸을 왼쪽 5칸·오른쪽 5칸으로 나눠, 두 나라의 1인당 CO₂를 각각 0~20t→0~5칸 막대로 표시. CO₂가 더 많은 쪽을 빨강, 적은 쪽을 초록으로. 하루 1회 갱신하고 나머지는 sleep.\n[설정] 비교할 두 나라 코드를 코드 맨 위에 country_a, country_b 변수로 두고 바꾸기 쉽게 해 줘. 기본값은 한국(KOR)과 미국(USA)."),
  ],
}

# ===================================================================
# 각 API의 '핵심만' 추린 Python 코드 (requests). 복붙해서 Streamlit·
# 바이브코딩에 쓰거나, AI(Claude 등)에게 그대로 넘겨 응용하기 좋은 정도.
# PROMPTS의 URL·필드와 대시보드 js를 그대로 옮긴 것.
CORE = {
  "weather":
"""import requests

LAT, LON = 37.5665, 126.9780  # 서울 (위도, 경도만 바꾸면 어디든)

data = requests.get("https://api.open-meteo.com/v1/forecast", params={
    "latitude": LAT, "longitude": LON,
    "hourly": "precipitation_probability",  # 시간별 강수확률
    "timezone": "Asia/Seoul", "forecast_days": 1,
}).json()

probs = data["hourly"]["precipitation_probability"]  # 0~23시 강수확률(%) 24개
print(probs)""",

  "airquality":
"""import requests

LAT, LON = 37.5665, 126.9780  # 서울

data = requests.get("https://air-quality-api.open-meteo.com/v1/air-quality", params={
    "latitude": LAT, "longitude": LON,
    "current": "pm2_5,pm10", "timezone": "Asia/Seoul",
}).json()

pm25 = data["current"]["pm2_5"]  # 초미세먼지 PM2.5 (㎍/㎥)
pm10 = data["current"]["pm10"]   # 미세먼지 PM10
print(pm25, pm10)""",

  "earthquake":
"""import requests

# 최근 하루 동안의 규모 4.5+ 지진 (키 불필요)
data = requests.get(
    "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson"
).json()

for q in data["features"]:
    mag = q["properties"]["mag"]      # 규모
    place = q["properties"]["place"]  # 발생 위치
    print(mag, place)""",

  "iss":
"""import requests

# 국제우주정거장(ISS)의 현재 위치 (키 불필요)
iss = requests.get("https://api.wheretheiss.at/v1/satellites/25544").json()

lat, lon = iss["latitude"], iss["longitude"]  # 현재 위도/경도
alt = iss["altitude"]                          # 고도(km)
print(lat, lon, alt)""",

  "sunrise":
"""import requests

LAT, LON = 37.5665, 126.9780  # 서울

r = requests.get("https://api.sunrise-sunset.org/json", params={
    "lat": LAT, "lng": LON, "formatted": 0,
}).json()["results"]

day_length = r["day_length"]            # 낮 길이(초)
sunrise, sunset = r["sunrise"], r["sunset"]  # 일출·일몰 (UTC, ISO 시각)
print(sunrise, sunset, day_length)""",

  "spaceweather":
"""import requests

# 우주날씨 Kp 지수 (지자기 교란·오로라 지표, 키 불필요)
rows = requests.get(
    "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
).json()

# 각 행은 딕셔너리: {"time_tag": .., "Kp": .., ...}
latest = rows[-1]
kp = float(latest["Kp"])        # 가장 최근 Kp 지수 (0~9)
when = latest["time_tag"]       # 측정 시각(3시간 간격)
print(when, kp)""",

  "pubchem":
"""import requests

name = "caffeine"  # 물질 영문 이름 (water, glucose, ethanol ...)

url = ("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"
       f"{name}/property/MolecularFormula,MolecularWeight/JSON")
props = requests.get(url).json()["PropertyTable"]["Properties"][0]

formula = props["MolecularFormula"]  # 분자식 (예: C8H10N4O2)
mw = props["MolecularWeight"]        # 분자량
print(formula, mw)""",

  "gbif":
"""import requests

sci_name = "Pica pica"  # 학명 (예: 까치). 우리나라(country=KR) 관찰 기록

data = requests.get("https://api.gbif.org/v1/occurrence/search", params={
    "country": "KR", "scientificName": sci_name, "limit": 0,
}).json()

count = data["count"]  # 국내 관찰 기록 수
print(count)""",

  "nasa":
"""import requests
from datetime import date

API_KEY = "DEMO_KEY"  # api.nasa.gov 에서 무료 발급 (DEMO_KEY는 횟수 제한)
today = date.today().isoformat()

data = requests.get("https://api.nasa.gov/neo/rest/v1/feed", params={
    "start_date": today, "end_date": today, "api_key": API_KEY,
}).json()

for n in data["near_earth_objects"][today]:  # 오늘 지구 근접 천체들
    name = n["name"]
    hazardous = n["is_potentially_hazardous_asteroid"]  # 위험(PHA) 여부
    print(name, hazardous)""",

  "energy":
"""import requests

LAT, LON = 37.5665, 126.9780  # 서울

data = requests.get("https://power.larc.nasa.gov/api/temporal/climatology/point", params={
    "parameters": "ALLSKY_SFC_SW_DWN",  # 지표 일사량
    "community": "RE", "latitude": LAT, "longitude": LON, "format": "JSON",
}).json()

monthly = data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
# {"JAN": .., "FEB": .., ..., "ANN": 연평균}  월평균 일사량(kWh/m²/day)
print(monthly)""",

  "worldbank":
"""import requests

country = "KOR"  # 나라 코드 (KOR, USA, JPN ...)
indicator = "EN.GHG.CO2.PC.CE.AR5"  # 1인당 CO₂ 배출량(톤)

url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
arr = requests.get(url, params={"format": "json", "per_page": 5, "mrnev": 1}).json()

latest = arr[1][0]            # 응답은 [메타데이터, 데이터배열] 구조
co2 = latest["value"]         # 1인당 CO₂ 배출량(t)
year = latest["date"]         # 연도
print(year, co2)""",
}

# ===================================================================
# 1) 날씨 (Open-Meteo)
page("weather", "🌤️", "오늘의 날씨", "지구과학·환경", "🇰🇷 국내 OK · 🌍 전 세계",
  lead="독일의 비영리 팀이 전 세계 여러 나라 기상청의 <b>슈퍼컴퓨터 예보</b>를 모아 무료로 공개해요. 위도·경도만 찍으면 <b>지구 어디든</b> 시간별 기온·강수확률·바람을 돌려줍니다. 회원가입도, API 키도 필요 없어요.",
  src_name="Open-Meteo", src_url="https://open-meteo.com",
  refs=[("Open-Meteo 공식 문서", "https://open-meteo.com/en/docs")],
  info='''<table>
    <tr><td class="k">무엇</td><td>전 세계 시간별 기온·강수확률·바람 등 (Open-Meteo)</td></tr>
    <tr><td class="k">API 키</td><td><b>필요 없음</b> · 무료 · 교육용 자유 사용</td></tr>
    <tr><td class="k">요청 예</td><td><code>api.open-meteo.com/v1/forecast?latitude=..&amp;longitude=..&amp;hourly=temperature_2m</code></td></tr>
    <tr><td class="k">받는 형식</td><td>JSON · <code>hourly.time[]</code> 과 <code>hourly.temperature_2m[]</code> 가 짝</td></tr>
  </table>''',
  apply_html='''<ul>
    <li>하루 <b>기온 곡선</b>으로 일교차·최고/최저 시각 찾기</li>
    <li>강수확률을 <b>10칸 LED</b>로(5장 ‘날씨 시계’)</li>
    <li>과거 데이터(archive)로 <b>10년 전과 올해 기온 비교</b> → 기후변화 탐구</li>
  </ul>''',
  body=SEOUL + '<div id="status" class="status">불러오는 중…</div>'
       '<div class="grid"><div class="stat"><div class="lab">현재 기온</div><div class="val" id="now">--</div><div class="unit">°C</div></div>'
       '<div class="stat"><div class="lab">오늘 최고/최저</div><div class="val" id="hilo" style="font-size:22px">--</div><div class="unit">°C</div></div>'
       '<div class="stat"><div class="lab">최대 강수확률</div><div class="val" id="pop">--</div><div class="unit">%</div></div></div>'
       '<div class="chartbox"><canvas id="ch" height="120"></canvas></div>',
  chart=True,
  js='''let chart;
async function run(){
  const lat=document.getElementById('lat').value, lon=document.getElementById('lon').value;
  const s=document.getElementById('status'); s.className='status'; s.textContent='불러오는 중…';
  try{
    const u=`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m&hourly=temperature_2m,precipitation_probability&timezone=Asia%2FSeoul&forecast_days=1`;
    const j=await (await fetch(u)).json();
    const t=j.hourly.temperature_2m, p=j.hourly.precipitation_probability;
    const labels=j.hourly.time.map(x=>x.slice(11,16));
    document.getElementById('now').textContent=j.current.temperature_2m;
    document.getElementById('hilo').textContent=Math.max(...t)+' / '+Math.min(...t);
    document.getElementById('pop').textContent=Math.max(...p.filter(v=>v!=null));
    s.textContent='✓ '+(j.timezone||'')+' · 오늘 0~23시';
    const ctx=document.getElementById('ch');
    if(chart) chart.destroy();
    chart=new Chart(ctx,{data:{labels,datasets:[
      {type:'line',label:'기온(°C)',data:t,borderColor:'#5B6CF0',backgroundColor:'rgba(91,108,240,.1)',fill:true,tension:.3,pointRadius:0,yAxisID:'y'},
      {type:'bar',label:'강수확률(%)',data:p,backgroundColor:'rgba(224,86,138,.35)',yAxisID:'y1'}]},
      options:{responsive:true,interaction:{intersect:false,mode:'index'},
        scales:{y:{position:'left',title:{display:true,text:'°C'}},
                y1:{position:'right',min:0,max:100,grid:{drawOnChartArea:false},title:{display:true,text:'%'}}}}});
  }catch(e){ s.className='status err'; s.textContent='데이터를 받지 못했어요: '+e; }
}
run();''')

# 2) 대기질
page("airquality", "🌫️", "미세먼지 (대기질)", "환경", "🌍 전 지구(국내 포함)",
  lead="같은 Open-Meteo가 유럽 <b>CAMS 대기질 모델</b>로 전 지구의 미세먼지(PM2.5·PM10)·오존을 시간별로 알려줘요. 위·경도만 바꾸면 여러 지역의 공기질을 숫자로 비교해 볼 수 있습니다.",
  src_name="Open-Meteo Air Quality", src_url="https://open-meteo.com/en/docs/air-quality-api",
  refs=[("에어코리아(국내 공식)", "https://www.airkorea.or.kr")],
  info='''<table>
    <tr><td class="k">무엇</td><td>PM2.5·PM10·오존 등 대기질 (Open-Meteo Air Quality)</td></tr>
    <tr><td class="k">API 키</td><td><b>필요 없음</b> · 무료</td></tr>
    <tr><td class="k">요청 예</td><td><code>air-quality-api.open-meteo.com/v1/air-quality?...&amp;current=pm2_5,pm10</code></td></tr>
    <tr><td class="k">참고</td><td>전 지구 모델 기반. <b>공식 국내값은 ‘에어코리아’</b> 권장</td></tr>
  </table>''',
  apply_html='''<ul>
    <li>등급에 따라 <b>LED 신호등</b>(좋음·보통·나쁨·매우나쁨)</li>
    <li>교실 안(센서)과 바깥(API) <b>비교 탐구</b></li>
    <li>하루 중 미세먼지가 높은 <b>시간대 찾기</b></li>
  </ul>''',
  body=SEOUL + '<div id="status" class="status">불러오는 중…</div>'
       '<div class="grid"><div class="stat" id="g25"><div class="lab">PM2.5 (초미세)</div><div class="val" id="v25">--</div><div class="unit" id="t25">µg/m³</div></div>'
       '<div class="stat" id="g10"><div class="lab">PM10 (미세)</div><div class="val" id="v10">--</div><div class="unit" id="t10">µg/m³</div></div></div>'
       '<div class="controls"><label>그래프</label><select id="metric" onchange="draw()">'
       '<option value="pm2_5">PM2.5 (초미세먼지)</option><option value="pm10">PM10 (미세먼지)</option></select></div>'
       '<div class="chartbox"><canvas id="ch" height="120"></canvas></div>',
  chart=True,
  js='''let chart, HOURLY=null;
function grade(pm){ if(pm<=15)return['좋음','#22c55e']; if(pm<=35)return['보통','#3b82f6']; if(pm<=75)return['나쁨','#f59e0b']; return['매우나쁨','#ef4444']; }
function grade10(pm){ if(pm<=30)return['좋음','#22c55e']; if(pm<=80)return['보통','#3b82f6']; if(pm<=150)return['나쁨','#f59e0b']; return['매우나쁨','#ef4444']; }
function gradeOf(metric, v){ return metric==='pm10'?grade10(v):grade(v); }
function draw(){
  if(!HOURLY) return;
  const metric=document.getElementById('metric').value;
  const series=HOURLY[metric], labels=HOURLY.time.map(x=>x.slice(11,16));
  const cur=series.find(v=>v!=null) ?? 0, color=gradeOf(metric,cur)[1];
  const name=metric==='pm10'?'PM10':'PM2.5';
  if(chart) chart.destroy();
  chart=new Chart(document.getElementById('ch'),{type:'line',data:{labels,datasets:[{label:name,data:series,borderColor:color,backgroundColor:color+'22',fill:true,tension:.3,pointRadius:0}]},options:{responsive:true,plugins:{legend:{display:false}}}});
}
async function run(){
  const lat=document.getElementById('lat').value, lon=document.getElementById('lon').value;
  const s=document.getElementById('status'); s.className='status'; s.textContent='불러오는 중…';
  try{
    const u=`https://air-quality-api.open-meteo.com/v1/air-quality?latitude=${lat}&longitude=${lon}&current=pm2_5,pm10&hourly=pm2_5,pm10&timezone=Asia%2FSeoul&forecast_days=1`;
    const j=await (await fetch(u)).json();
    const pm=j.current.pm2_5, [n25,c25]=grade(pm);
    document.getElementById('v25').textContent=pm; document.getElementById('v25').style.color=c25;
    document.getElementById('t25').textContent='µg/m³ · '+n25; document.getElementById('g25').style.borderColor=c25;
    const p10=j.current.pm10, [n10,c10]=grade10(p10);
    document.getElementById('v10').textContent=p10; document.getElementById('v10').style.color=c10;
    document.getElementById('t10').textContent='µg/m³ · '+n10; document.getElementById('g10').style.borderColor=c10;
    s.textContent='✓ 현재 기준 · PM2.5 '+n25+' / PM10 '+n10;
    HOURLY={time:j.hourly.time, pm2_5:j.hourly.pm2_5, pm10:j.hourly.pm10};
    draw();
  }catch(e){ s.className='status err'; s.textContent='데이터를 받지 못했어요: '+e; }
}
run();''')

# 3) 지진 (USGS)
page("earthquake", "🌍", "전 세계 지진", "지구과학", "🌎 해외 위주(국내 지진은 드묾)",
  lead="미국 <b>지질조사국(USGS)</b>이 전 세계 지진계 네트워크로 잡은 지진을 <b>1분 단위</b>로 갱신해 공개합니다. 지금 이 순간 지구 어딘가에서 흔들린 땅을 실시간으로 만나 보세요.",
  src_name="USGS Earthquake Hazards Program", src_url="https://earthquake.usgs.gov",
  refs=[("USGS 실시간 지진 지도", "https://earthquake.usgs.gov/earthquakes/map/"), ("기상청 지진정보(국내)", "https://www.weather.go.kr/w/eqk-vol/search/korea.do")],
  info='''<table>
    <tr><td class="k">무엇</td><td>실시간 지진 목록(규모·위치·깊이·시각), GeoJSON (USGS)</td></tr>
    <tr><td class="k">API 키</td><td><b>필요 없음</b> · 무료</td></tr>
    <tr><td class="k">요청 예</td><td><code>earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson</code></td></tr>
    <tr><td class="k">국내</td><td>한반도 지진은 드물게 잡힘 → <b>국내는 기상청 권장</b></td></tr>
  </table>''',
  apply_html='''<ul>
    <li>지진 위치를 <b>세계 지도</b>에 찍어 <b>판 경계(불의 고리)</b>와 비교</li>
    <li>규모별로 지진 <b>개수 세기</b>(통계 탐구)</li>
    <li>가장 큰 규모를 <b>LED 게이지</b>로 표현</li>
  </ul>''',
  maps=True,
  body='<div class="controls"><label>기간·규모</label><select id="feed" onchange="run()">'
       '<option value="2.5_day">최근 하루 · M2.5+</option>'
       '<option value="4.5_day">최근 하루 · M4.5+</option>'
       '<option value="significant_week">최근 일주일 · 큰 지진</option>'
       '<option value="all_day">최근 하루 · 전체</option>'
       '</select><button onclick="run()">불러오기</button></div>'
       '<div id="status" class="status">불러오는 중…</div>'
       '<div class="grid"><div class="stat"><div class="lab">발생 건수</div><div class="val" id="cnt">--</div></div>'
       '<div class="stat"><div class="lab">최대 규모</div><div class="val" id="mx">--</div><div class="unit">M</div></div></div>'
       '<div id="map" class="map"></div>'
       '<div style="font-size:11px;color:#7a7f95;margin:8px 2px;text-align:center">원의 크기·색 = 지진 규모 · 점을 누르면 상세 (규모가 큰 지진이 어디에 몰려 있나요?)</div>'
       '<ul class="list" id="list"></ul>'
       '<div class="qbox"><div class="qbox-t">🔎 탐구 질문</div><ul>'
       '<li>큰 지진은 주로 어떤 선(라인)을 따라 모여 있나요? 지도의 그 띠를 무엇이라 부를까요?</li>'
       '<li>우리나라 주변에는 지진이 많나요, 적나요? 왜 그럴까요?</li>'
       '<li>규모가 1 커지면 에너지는 약 32배! 규모 5와 6의 차이를 이야기해 보세요.</li>'
       '</ul></div>',
  js='''let map, layer;
function mcolor(m){ return m<3?'#22c55e':m<5?'#f59e0b':'#ef4444'; }
function ago(t){ const s=(Date.now()-t)/1000; if(s<3600)return Math.round(s/60)+'분 전'; if(s<86400)return Math.round(s/3600)+'시간 전'; return Math.round(s/86400)+'일 전'; }
async function run(){
  const feed=document.getElementById('feed').value;
  const s=document.getElementById('status'); s.className='status'; s.textContent='불러오는 중…';
  if(!map){ map=L.map('map',{worldCopyJump:true}).setView([20,140],1);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'© OpenStreetMap',maxZoom:8}).addTo(map); }
  try{
    const j=await (await fetch(`https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/${feed}.geojson`)).json();
    const q=j.features.filter(f=>f.properties.mag!=null).sort((a,b)=>b.properties.mag-a.properties.mag);
    document.getElementById('cnt').textContent=j.metadata.count;
    document.getElementById('mx').textContent=q.length?q[0].properties.mag.toFixed(1):'--';
    s.textContent='✓ '+j.metadata.title;
    if(layer) layer.remove();
    layer=L.layerGroup().addTo(map);
    q.forEach(f=>{ const p=f.properties, c=f.geometry.coordinates;
      L.circleMarker([c[1],c[0]],{radius:Math.max(4,p.mag*2.2),color:mcolor(p.mag),weight:1,fillColor:mcolor(p.mag),fillOpacity:.55})
        .bindPopup(`<b>M${p.mag.toFixed(1)}</b> · ${p.place||'-'}<br>깊이 ${c[2]}km · ${ago(p.time)}`).addTo(layer); });
    document.getElementById('list').innerHTML=q.slice(0,10).map(f=>{
      const p=f.properties, c=mcolor(p.mag);
      return `<li><span class="badge" style="background:${c}">M${p.mag.toFixed(1)}</span>
        <span>${p.place||'-'}<br><span class="meta">${ago(p.time)} · 깊이 ${f.geometry.coordinates[2]}km</span></span></li>`;
    }).join('') || '<li class="meta">이 조건에 해당하는 지진이 없어요.</li>';
  }catch(e){ s.className='status err'; s.textContent='데이터를 받지 못했어요: '+e; }
}
run();''')

# 4) ISS
page("iss", "🛰️", "국제우주정거장 ISS", "천문·물리", "🌍 전 지구(국내 상공 포함)",
  lead="축구장만 한 <b>국제우주정거장(ISS)</b>이 지금 지구 위 약 <b>420km</b>에서 <b>시속 27,000km</b>로 날고 있어요. 약 90분에 지구를 한 바퀴! 그 위치를 초 단위로 알려주는 서비스입니다.",
  src_name="Where the ISS at?", src_url="https://wheretheiss.at",
  refs=[("NASA Spot the Station", "https://spotthestation.nasa.gov"), ("ISS 실시간 영상(NASA)", "https://www.nasa.gov/live/")],
  info='''<table>
    <tr><td class="k">무엇</td><td>ISS의 실시간 위·경도·고도·속도 (wheretheiss.at)</td></tr>
    <tr><td class="k">API 키</td><td><b>필요 없음</b> · 무료</td></tr>
    <tr><td class="k">요청 예</td><td><code>api.wheretheiss.at/v1/satellites/25544</code></td></tr>
    <tr><td class="k">갱신</td><td>이 페이지는 <b>5초마다 자동 갱신</b>됩니다</td></tr>
  </table>''',
  apply_html='''<ul>
    <li>실시간 위치를 <b>세계 지도</b>에 표시하고 <b>궤도 경로</b> 그리기</li>
    <li>내 위치와의 <b>거리</b>로 ‘머리 위 통과’ 알림 LED</li>
    <li>속도(약 27,000km/h)로 <b>궤도 운동</b> 체감</li>
  </ul>''',
  maps=True,
  body='<div class="controls"><label>내 위도</label><input id="lat" value="37.5665"><label>경도</label><input id="lon" value="126.9780"></div>'
       '<div id="status" class="status">불러오는 중…</div>'
       '<div id="map" class="map"></div>'
       '<div style="font-size:11px;color:#7a7f95;margin:8px 2px;text-align:center">🛰️ = 현재 ISS · 노란 선 = 방금 지나온 경로 · 📍 = 내 위치 · 5초마다 자동 갱신</div>'
       '<div class="grid"><div class="stat"><div class="lab">ISS 위도</div><div class="val" id="ilat" style="font-size:24px">--</div></div>'
       '<div class="stat"><div class="lab">ISS 경도</div><div class="val" id="ilon" style="font-size:24px">--</div></div>'
       '<div class="stat"><div class="lab">고도</div><div class="val" id="alt" style="font-size:24px">--</div><div class="unit">km</div></div>'
       '<div class="stat"><div class="lab">속도</div><div class="val" id="vel" style="font-size:20px">--</div><div class="unit">km/h</div></div></div>'
       '<div class="stat" id="distbox" style="margin-top:12px"><div class="lab">내 위치에서 거리</div><div class="val" id="dist">--</div><div class="unit" id="overhead">km</div></div>'
       '<div class="qbox"><div class="qbox-t">🔎 탐구 질문</div><ul>'
       '<li>ISS 경로가 <b>위아래로 물결치며</b> 동쪽으로 가요. 왜 직선이 아닐까요?(궤도 경사각)</li>'
       '<li>약 90분에 지구 한 바퀴! 하루에 몇 번 돌까요? 직접 계산해 보세요.</li>'
       '<li>고도 약 420km는 서울~부산(약 325km)보다 조금 멀어요. ‘우주’는 생각보다 가깝죠?</li>'
       '</ul></div>',
  js='''let map, iss, ring, me, path=[];
function dkm(la1,lo1,la2,lo2){const R=6371,r=Math.PI/180;
  const a=Math.sin((la2-la1)*r/2)**2+Math.cos(la1*r)*Math.cos(la2*r)*Math.sin((lo2-lo1)*r/2)**2;
  return 2*R*Math.asin(Math.sqrt(a));}
const issIcon=L.divIcon({html:'<div style="font-size:26px;line-height:1">🛰️</div>',className:'',iconSize:[26,26],iconAnchor:[13,13]});
const meIcon=L.divIcon({html:'<div style="font-size:22px;line-height:1">📍</div>',className:'',iconSize:[22,22],iconAnchor:[11,22]});
async function tick(){
  const s=document.getElementById('status');
  if(!map){ map=L.map('map',{worldCopyJump:true}).setView([20,0],1);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'© OpenStreetMap',maxZoom:8}).addTo(map);
    ring=L.polyline([],{color:'#f5c542',weight:2,opacity:.7}).addTo(map); }
  try{
    const j=await (await fetch('https://api.wheretheiss.at/v1/satellites/25544')).json();
    document.getElementById('ilat').textContent=j.latitude.toFixed(2);
    document.getElementById('ilon').textContent=j.longitude.toFixed(2);
    document.getElementById('alt').textContent=Math.round(j.altitude);
    document.getElementById('vel').textContent=Math.round(j.velocity).toLocaleString();
    const pos=[j.latitude,j.longitude];
    if(!iss){ iss=L.marker(pos,{icon:issIcon}).addTo(map); map.setView(pos,3); }
    else iss.setLatLng(pos);
    path.push(pos); if(path.length>60) path.shift(); ring.setLatLngs(path);
    const la=parseFloat(document.getElementById('lat').value), lo=parseFloat(document.getElementById('lon').value);
    if(!me){ me=L.marker([la,lo],{icon:meIcon}).addTo(map).bindPopup('내 위치'); } else me.setLatLng([la,lo]);
    const d=dkm(la,lo,j.latitude,j.longitude);
    document.getElementById('dist').textContent=Math.round(d).toLocaleString();
    const over=d<2200; document.getElementById('overhead').textContent=over?'km · 🛰️ 머리 위 하늘권!':'km';
    document.getElementById('distbox').style.borderColor=over?'#5B6CF0':'';
    s.textContent='✓ 5초마다 자동 갱신 중';
  }catch(e){ s.className='status err'; s.textContent='데이터를 받지 못했어요: '+e; }
}
tick(); setInterval(tick,5000);''')

# 5) 일출·일몰
page("sunrise", "🌅", "일출·일몰·낮 길이", "천문·지구과학", "🇰🇷 국내 OK",
  lead="전 세계 <b>어떤 좌표든</b> 오늘 해가 뜨고 지는 시각을 천문 계산으로 알려줘요. 위도를 북극 가까이 바꿔 보면 해가 안 지는 <b>백야</b>도 데이터로 확인할 수 있습니다.",
  src_name="Sunrise-Sunset.org", src_url="https://sunrise-sunset.org",
  info='''<table>
    <tr><td class="k">무엇</td><td>일출·일몰·남중·낮 길이·박명 시각 (sunrise-sunset.org)</td></tr>
    <tr><td class="k">API 키</td><td><b>필요 없음</b> · 무료</td></tr>
    <tr><td class="k">요청 예</td><td><code>api.sunrise-sunset.org/json?lat=..&amp;lng=..&amp;formatted=0</code></td></tr>
    <tr><td class="k">시각</td><td>UTC로 옵니다 → 이 페이지가 <b>한국 시간으로 변환</b>해 표시</td></tr>
  </table>''',
  apply_html='''<ul>
    <li>계절별 <b>낮 길이 변화</b> 그래프(하지·동지 비교)</li>
    <li>낮 길이만큼 <b>LED 게이지</b></li>
    <li>위도를 바꿔 <b>적도 vs 극지방</b> 낮 길이 비교</li>
  </ul>''',
  body=SEOUL + '<div id="status" class="status">불러오는 중…</div>'
       '<div class="grid"><div class="stat"><div class="lab">일출</div><div class="val" id="sr" style="font-size:24px">--</div></div>'
       '<div class="stat"><div class="lab">일몰</div><div class="val" id="ss" style="font-size:24px">--</div></div>'
       '<div class="stat"><div class="lab">낮 길이</div><div class="val" id="dl" style="font-size:22px">--</div></div>'
       '<div class="stat"><div class="lab">남중(정오)</div><div class="val" id="noon" style="font-size:24px">--</div></div></div>',
  js='''function hm(iso){ return new Date(iso).toLocaleTimeString('ko-KR',{hour:'2-digit',minute:'2-digit',hour12:false}); }
async function run(){
  const lat=document.getElementById('lat').value, lon=document.getElementById('lon').value;
  const s=document.getElementById('status'); s.className='status'; s.textContent='불러오는 중…';
  try{
    const r=(await (await fetch(`https://api.sunrise-sunset.org/json?lat=${lat}&lng=${lon}&formatted=0`)).json()).results;
    document.getElementById('sr').textContent=hm(r.sunrise);
    document.getElementById('ss').textContent=hm(r.sunset);
    document.getElementById('noon').textContent=hm(r.solar_noon);
    const h=Math.floor(r.day_length/3600), m=Math.round(r.day_length%3600/60);
    document.getElementById('dl').textContent=h+'시간 '+m+'분';
    s.textContent='✓ 오늘 · 한국 시간 기준';
  }catch(e){ s.className='status err'; s.textContent='데이터를 받지 못했어요: '+e; }
}
run();''')

# 6) 우주날씨 Kp
page("spaceweather", "🌞", "우주날씨 (Kp 지수)", "천문·지구과학", "🌍 전 지구 공통",
  lead="미국 해양대기청(NOAA) <b>우주기상예보센터(SWPC)</b>가 태양 폭풍이 지구 자기장을 흔드는 정도(<b>Kp 지수</b>)를 3시간마다 발표해요. 뉴스에 나오는 ‘오로라 예보’가 바로 이 데이터랍니다.",
  src_name="NOAA 우주기상예보센터(SWPC)", src_url="https://www.swpc.noaa.gov",
  refs=[("NOAA 오로라 예보", "https://www.swpc.noaa.gov/products/aurora-30-minute-forecast"), ("SpaceWeatherLive(한국어)", "https://www.spaceweatherlive.com/ko.html")],
  info='''<table>
    <tr><td class="k">무엇</td><td>지자기 폭풍 정도 Kp 지수(0~9)·태양 활동 (NOAA SWPC)</td></tr>
    <tr><td class="k">API 키</td><td><b>필요 없음</b> · 무료</td></tr>
    <tr><td class="k">요청 예</td><td><code>services.swpc.noaa.gov/products/noaa-planetary-k-index.json</code></td></tr>
    <tr><td class="k">의미</td><td>Kp가 클수록 지자기 교란 ↑ · 고위도 <b>오로라</b> 가능성 ↑</td></tr>
  </table>''',
  apply_html='''<ul>
    <li>Kp가 높으면 LED를 <b>보라색</b>으로(오로라 경보)</li>
    <li>며칠치 Kp <b>변화 그래프</b>로 태양 활동 관찰</li>
    <li>뉴스의 ‘태양 폭풍’ 기사와 <b>데이터로 비교</b></li>
  </ul>''',
  body='<div id="status" class="status">불러오는 중…</div>'
       '<div class="grid"><div class="stat" id="kbox"><div class="lab">현재 Kp 지수</div><div class="val" id="kp">--</div><div class="unit" id="kstate">0~9</div></div></div>'
       '<div class="chartbox"><canvas id="ch" height="120"></canvas></div>',
  chart=True,
  js='''let chart;
function kcolor(k){ return k<4?'#22c55e':k<6?'#f59e0b':'#8b5cf6'; }
async function run(){
  const s=document.getElementById('status'); s.className='status'; s.textContent='불러오는 중…';
  try{
    const arr=await (await fetch('https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json')).json();
    const last=arr.slice(-24);
    const kp=arr[arr.length-1].Kp, c=kcolor(kp);
    document.getElementById('kp').textContent=kp.toFixed(1); document.getElementById('kp').style.color=c;
    document.getElementById('kstate').textContent=kp<4?'조용함':kp<6?'활동적':'폭풍! 오로라 가능';
    document.getElementById('kbox').style.borderColor=c;
    s.textContent='✓ 최근 '+last.length+'개 측정값(3시간 간격)';
    if(chart) chart.destroy();
    chart=new Chart(document.getElementById('ch'),{type:'bar',data:{labels:last.map(r=>r.time_tag.slice(5,16).replace('T',' ')),
      datasets:[{label:'Kp',data:last.map(r=>r.Kp),backgroundColor:last.map(r=>kcolor(r.Kp))}]},
      options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{min:0,max:9}}}});
  }catch(e){ s.className='status err'; s.textContent='데이터를 받지 못했어요: '+e; }
}
run();''')

# 7) PubChem 화학
CMP = [
 ("물","water"),("산소","oxygen"),("이산화탄소","carbon dioxide"),("질소","nitrogen"),
 ("포도당","glucose"),("설탕(수크로스)","sucrose"),("소금(염화나트륨)","sodium chloride"),
 ("에탄올(알코올)","ethanol"),("아세트산(식초)","acetic acid"),("암모니아","ammonia"),
 ("메테인","methane"),("과산화수소","hydrogen peroxide"),("베이킹소다","sodium bicarbonate"),
 ("카페인","caffeine"),("비타민C","ascorbic acid"),("아스피린","aspirin"),
 ("아세트아미노펜(타이레놀)","acetaminophen"),("니코틴","nicotine"),
]
PRESET = '<option value="">— 인기 물질 고르기 —</option>' + ''.join(f'<option value="{e}">{k}</option>' for k, e in CMP)
DLIST = ''.join(f'<option value="{e}">{k}</option>' for k, e in CMP)
page("pubchem", "⚗️", "물질 정보 (화학)", "화학", "🌐 국적 무관",
  lead="미국 국립보건원(NIH)이 운영하는 세계 최대 화학 백과 <b>PubChem</b>. <b>1억 종</b>이 넘는 물질의 이름만 넣으면 분자식·분자량은 물론 <b>구조 그림</b>까지 그려 줍니다.",
  src_name="PubChem (미국 국립보건원 NIH)", src_url="https://pubchem.ncbi.nlm.nih.gov",
  info='''<table>
    <tr><td class="k">무엇</td><td>물질 이름으로 분자식·분자량·구조 그림 (PubChem)</td></tr>
    <tr><td class="k">API 키</td><td><b>필요 없음</b> · 무료</td></tr>
    <tr><td class="k">요청 예</td><td><code>pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/<i>caffeine</i>/property/MolecularWeight/JSON</code></td></tr>
    <tr><td class="k">2D 그림</td><td>같은 주소의 <code>/PNG</code> 로 평면 구조 이미지를 받습니다</td></tr>
    <tr><td class="k">3D 구조</td><td>PubChem이 <b>계산한 3D 입체구조 좌표(SDF, <code>record_type=3d</code>)</b>를 받아 <a href="https://3Dmol.org" target="_blank" rel="noopener" style="color:#3b47c2">3Dmol.js</a>로 회전 가능하게 그립니다 — 데이터는 <b>PubChem</b>이 제공</td></tr>
  </table>''',
  apply_html='''<ul>
    <li>여러 물질 <b>분자량 비교</b>(물·포도당·카페인…)</li>
    <li><b>3D 구조</b>를 돌려 보며 분자 모양·입체 이해(2D보다 직관적!)</li>
    <li>화학식만 보여 주고 <b>물질 맞히기 퀴즈</b></li>
  </ul>''',
  head='<script src="https://3Dmol.org/build/3Dmol-min.js"></script>',
  body=f'<div class="controls"><label>인기 물질</label><select id="preset" onchange="pick()">{PRESET}</select>'
       f'<label>또는 직접</label><input id="name" list="cmplist" value="caffeine" style="width:160px" placeholder="영문 이름">'
       f'<datalist id="cmplist">{DLIST}</datalist><button onclick="run()">검색</button></div>'
       '<div style="font-size:12px;color:#7a7f95;margin:-6px 2px 12px">영문 이름으로 검색돼요(예: water, glucose). 목록에 없는 물질은 '
       '<a href="https://pubchem.ncbi.nlm.nih.gov" target="_blank" rel="noopener" style="color:#3b47c2;font-weight:600">PubChem에서 직접 검색 ↗</a> 후 영문명을 넣어 보세요.</div>'
       '<div id="status" class="status">불러오는 중…</div>'
       '<div class="grid" style="grid-template-columns:1fr 1fr;margin-bottom:14px">'
       '<div class="stat"><div class="lab">분자식</div><div class="val" id="formula" style="font-size:24px">--</div></div>'
       '<div class="stat"><div class="lab">분자량</div><div class="val" id="mw">--</div><div class="unit">g/mol</div></div></div>'
       '<div class="seg"><button id="b2d" class="seg-on" onclick="setView(\'2d\')">평면 2D</button>'
       '<button id="b3d" onclick="setView(\'3d\')">입체 3D 🧊</button></div>'
       '<div id="view2d"><img id="img" class="molimg" alt="구조" src=""></div>'
       '<div id="view3d" style="display:none"><div id="v3d" class="mol3d"></div>'
       '<div class="cpk"><b>색 = 원소</b>'
       '<span><i style="background:#909090"></i>탄소 C</span>'
       '<span><i style="background:#ffffff"></i>수소 H</span>'
       '<span><i style="background:#ff0d0d"></i>산소 O</span>'
       '<span><i style="background:#3050f8"></i>질소 N</span>'
       '<span><i style="background:#ffe000"></i>황 S</span></div>'
       '<div style="font-size:11px;color:#7a7f95;text-align:center;margin-top:6px">3D 분자는 글씨 대신 <b>색으로 원소를 구분</b>해요 · 드래그로 회전 · 휠로 확대 (3D 모양이 없는 단순 물질도 있어요)</div></div>',
  js='''let CID=null, viewer=null, mode='2d';
function pick(){ const v=document.getElementById('preset').value; if(v){ document.getElementById('name').value=v; run(); } }
function setView(m){
  mode=m;
  document.getElementById('b2d').className = m==='2d'?'seg-on':'';
  document.getElementById('b3d').className = m==='3d'?'seg-on':'';
  document.getElementById('view2d').style.display = m==='2d'?'':'none';
  document.getElementById('view3d').style.display = m==='3d'?'':'none';
  if(m==='3d' && CID) render3d(CID);
}
function render3d(cid){
  const box=document.getElementById('v3d');
  if(!viewer){ viewer=$3Dmol.createViewer(box,{backgroundColor:'0xf4f6fc'}); }
  viewer.clear();
  $3Dmol.download('cid:'+cid, viewer, {}, ()=>{
    viewer.setStyle({}, {stick:{radius:0.14}, sphere:{scale:0.28}});
    viewer.zoomTo(); viewer.render();
  });
}
async function run(){
  const name=document.getElementById('name').value.trim();
  const s=document.getElementById('status'); s.className='status'; s.textContent='불러오는 중…';
  try{
    const base='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/'+encodeURIComponent(name);
    const j=await (await fetch(base+'/property/MolecularFormula,MolecularWeight/JSON')).json();
    const p=j.PropertyTable.Properties[0];
    CID=p.CID;
    document.getElementById('formula').textContent=p.MolecularFormula;
    document.getElementById('mw').textContent=parseFloat(p.MolecularWeight).toFixed(2);
    document.getElementById('img').src=base+'/PNG';
    s.textContent='✓ '+name+' (CID '+p.CID+')';
    if(mode==='3d') render3d(CID);
  }catch(e){ s.className='status err'; s.textContent='그 이름의 물질을 못 찾았어요. 영문 이름으로 다시 시도해 보세요.'; }
}
run();''')

# 8) GBIF 생물
SP_GROUPS = [
 ("새", [("까치","Pica pica"),("왜가리","Ardea cinerea"),("중대백로","Ardea alba"),
         ("참새","Passer montanus"),("직박구리","Hypsipetes amaurotis"),("박새","Parus major")]),
 ("포유류", [("고라니","Hydropotes inermis"),("멧돼지","Sus scrofa"),("청설모","Sciurus vulgaris")]),
 ("양서류·곤충", [("청개구리","Dryophytes japonicus"),("호랑나비","Papilio xuthus")]),
 ("식물", [("소나무","Pinus densiflora"),("은행나무","Ginkgo biloba"),("왕벚나무","Prunus yedoensis")]),
]
PRESET_SP = '<option value="">— 생물 고르기 —</option>' + ''.join(
    f'<optgroup label="{g}">' + ''.join(f'<option value="{sci}">{ko} ({sci})</option>' for ko, sci in items) + '</optgroup>'
    for g, items in SP_GROUPS)
DLIST_SP = ''.join(f'<option value="{sci}">{ko}</option>' for g, items in SP_GROUPS for ko, sci in items)
page("gbif", "🐦", "우리나라 생물 관찰", "생물", "🇰🇷 국내 OK",
  lead="전 세계 박물관·연구자·시민과학자가 모은 생물 관찰 기록 <b>20억 건 이상</b>을 한곳에 모은 <b>GBIF</b>. ‘우리나라에서 까치가 언제·어디서 관찰됐나’ 같은 것도 찾을 수 있어요(한국 약 880만 건).",
  src_name="GBIF (세계생물다양성정보기구)", src_url="https://www.gbif.org/country/KR/summary",
  refs=[("국립생물자원관", "https://www.nibr.go.kr")],
  info='''<table>
    <tr><td class="k">무엇</td><td>전 세계 생물 관찰 기록 DB(종·위치·날짜·사진) (GBIF)</td></tr>
    <tr><td class="k">API 키</td><td><b>필요 없음</b> · 무료</td></tr>
    <tr><td class="k">요청 예</td><td><code>api.gbif.org/v1/occurrence/search?country=KR&amp;scientificName=Pica%20pica</code></td></tr>
    <tr><td class="k">국내</td><td>한국 관찰기록 약 <b>880만 건</b> — 풍부</td></tr>
  </table>''',
  apply_html='''<ul>
    <li>관찰 <b>위치를 지도</b>에 찍어 종의 <b>분포</b> 살피기(도시 vs 산지)</li>
    <li>관찰 기록 수를 <b>자릿수 LED</b>로(흔한 종 vs 희귀종)</li>
    <li>계절별 관찰 <b>시기 비교</b>(철새는 언제 많이 보일까?)</li>
  </ul>''',
  maps=True, chart=True,
  body=f'<div class="controls"><label>생물 고르기</label><select id="preset" onchange="pick()">{PRESET_SP}</select>'
       f'<label>또는 학명</label><input id="sp" list="splist" value="Pica pica" style="width:170px" placeholder="학명(라틴어)">'
       f'<datalist id="splist">{DLIST_SP}</datalist><button onclick="run()">검색</button></div>'
       '<div style="font-size:12px;color:#7a7f95;margin:-6px 2px 12px">학명(라틴어)으로 검색돼요. 목록에 없는 종은 '
       '<a href="https://www.gbif.org/species/search" target="_blank" rel="noopener" style="color:#3b47c2;font-weight:600">GBIF 종 검색 ↗</a>에서 학명을 찾아 넣어 보세요.</div>'
       '<div id="status" class="status">불러오는 중…</div>'
       '<div class="grid"><div class="stat"><div class="lab">한국 관찰 기록</div><div class="val" id="cnt">--</div><div class="unit">건</div></div>'
       '<div class="stat"><div class="lab">지도에 표시(좌표 있는 것)</div><div class="val" id="mcnt" style="font-size:22px">--</div><div class="unit">개 지점</div></div></div>'
       '<div id="map" class="map"></div>'
       '<div style="font-size:11px;color:#7a7f95;margin:8px 2px;text-align:center">📍 관찰 지점(좌표 있는 것) · 점을 누르면 관찰 날짜·장소</div>'
       '<h3 style="margin:18px 0 2px;font-size:14px">📅 월별 관찰 분포 (계절성)</h3>'
       '<div class="chartbox"><canvas id="mchart" height="110"></canvas></div>'
       '<div style="font-size:11px;color:#7a7f95;margin:6px 2px 4px;text-align:center">한국 내 전체 관찰 기록을 월별로 — 특정 계절에 몰려 있나요?</div>'
       '<ul class="list" id="list"></ul>'
       '<div class="qbox"><div class="qbox-t">🔎 탐구 질문</div><ul>'
       '<li>이 생물은 도시 근처에 많나요, 산·강 근처에 많나요? 왜 그럴까요?</li>'
       '<li>월별 그래프가 특정 계절에 솟아 있나요? 철새라면 봄·가을(이동철)에, 곤충은 여름에 몰릴 수 있어요.</li>'
       '<li>다른 종(철새 vs 텃새)으로 바꿔 월별 분포를 비교해 보세요.</li>'
       '</ul></div>',
  js='''let map, layer, mchart;
function pick(){ const v=document.getElementById('preset').value; if(v){ document.getElementById('sp').value=v; run(); } }
const MON=['1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월'];
function seasonColor(m){ return (m>=3&&m<=5)?'#22c55e':(m>=6&&m<=8)?'#ef4444':(m>=9&&m<=11)?'#f59e0b':'#3b82f6'; }
async function run(){
  const sp=document.getElementById('sp').value.trim();
  const s=document.getElementById('status'); s.className='status'; s.textContent='불러오는 중…';
  if(!map){ map=L.map('map').setView([36.4,127.8],6);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'© OpenStreetMap',maxZoom:14}).addTo(map); }
  try{
    const u=`https://api.gbif.org/v1/occurrence/search?country=KR&scientificName=${encodeURIComponent(sp)}&hasCoordinate=true&facet=month&facetLimit=12&limit=120`;
    const j=await (await fetch(u)).json();
    document.getElementById('cnt').textContent=j.count.toLocaleString();
    const pts=(j.results||[]).filter(r=>r.decimalLatitude!=null);
    document.getElementById('mcnt').textContent=pts.length;
    s.textContent='✓ 한국 내 '+sp+' 관찰';
    if(layer) layer.remove();
    layer=L.layerGroup().addTo(map);
    const ll=[];
    pts.forEach(r=>{ const a=[r.decimalLatitude,r.decimalLongitude]; ll.push(a);
      L.circleMarker(a,{radius:5,color:'#1f9d63',weight:1,fillColor:'#22c55e',fillOpacity:.6})
        .bindPopup(`<b>${r.scientificName||sp}</b><br>${r.locality||r.stateProvince||'위치 미상'}<br>${(r.eventDate||'').slice(0,10)||'날짜 미상'}`).addTo(layer); });
    if(ll.length) map.fitBounds(ll,{padding:[30,30],maxZoom:11});
    const months=Array(12).fill(0);
    const mf=(j.facets||[]).find(f=>f.field==='MONTH');
    if(mf) mf.counts.forEach(c=>{ const m=parseInt(c.name); if(m>=1&&m<=12) months[m-1]=c.count; });
    if(mchart) mchart.destroy();
    mchart=new Chart(document.getElementById('mchart'),{type:'bar',data:{labels:MON,
      datasets:[{label:'관찰 수',data:months,backgroundColor:months.map((_,i)=>seasonColor(i+1))}]},
      options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true}}}});
    document.getElementById('list').innerHTML=pts.slice(0,8).map(r=>
      `<li><span>${r.scientificName||sp}<br><span class="meta">${r.locality||r.stateProvince||'위치 미상'} · ${(r.eventDate||'').slice(0,10)||'날짜 미상'}</span></span></li>`
    ).join('') || '<li class="meta">좌표가 있는 관찰 기록이 없어요. 학명을 확인해 보세요.</li>';
  }catch(e){ s.className='status err'; s.textContent='데이터를 받지 못했어요: '+e; }
}
run();''')

# 9) NASA APOD
page("nasa", "🔭", "NASA 우주 데이터", "천문", "🌐 국적 무관 · 키 필요",
  lead="<b>NASA</b>의 공개 데이터 두 가지를 함께 봅니다. 1995년부터 <b>매일 한 장씩</b> 올라오는 천문사진(APOD)과, 오늘 <b>지구 가까이 지나가는 소행성</b>(NeoWs) 목록이에요. 같은 API 키 하나로 여러 우주 데이터에 접근할 수 있죠.",
  src_name="NASA Open APIs", src_url="https://api.nasa.gov",
  refs=[("오늘의 천문사진 APOD", "https://apod.nasa.gov/apod/"), ("소행성 NeoWs 안내", "https://api.nasa.gov/")],
  info='''<table>
    <tr><td class="k">무엇</td><td>천문사진(APOD) + 근지구 소행성(NeoWs) — NASA Open APIs</td></tr>
    <tr><td class="k">API 키</td><td><b>필요</b> · 기본은 공용 <code>DEMO_KEY</code>(횟수 제한) · 막히면 <b>api.nasa.gov</b>에서 무료 키 발급해 입력</td></tr>
    <tr><td class="k">요청 예</td><td><code>api.nasa.gov/planetary/apod?api_key=…</code><br><code>api.nasa.gov/neo/rest/v1/feed?start_date=…&amp;end_date=…&amp;api_key=…</code></td></tr>
    <tr><td class="k">확장</td><td>같은 키로 지구사진(EPIC), 화성 날씨 등 다른 API도 호출 가능</td></tr>
  </table>''',
  apply_html='''<ul>
    <li>교실 모니터에 <b>매일 우주사진</b> 띄우기(설명 번역해 ‘오늘의 천문 이야기’)</li>
    <li>오늘 가장 가까이 오는 소행성 <b>거리·크기 비교</b>(달까지 거리와 견주기)</li>
    <li><b>위험 소행성</b>(PHA)이 있으면 알림 LED — 지름·거리 데이터로 탐구</li>
  </ul>''',
  body='<div class="controls"><label>API 키</label><input id="key" value="DEMO_KEY" style="width:200px"><button onclick="run()">불러오기</button>'
       '<span style="font-size:12px;color:#7a7f95">DEMO_KEY는 횟수 제한이 있어요 → 막히면 <a href="https://api.nasa.gov" target="_blank" rel="noopener" style="color:#3b47c2">무료 키 발급</a> 후 입력</span></div>'
       '<h3 style="margin:6px 0 2px;font-size:15px">🌌 오늘의 천문사진 (APOD)</h3>'
       '<div id="status" class="status">불러오는 중…</div>'
       '<h3 id="title" style="margin:6px 0;font-size:17px"></h3><div class="meta" id="date" style="color:#7a7f95;font-size:12px"></div>'
       '<div id="media"></div>'
       '<p id="exp" style="font-size:13px;color:#44464f;margin-top:10px;line-height:1.8"></p>'
       '<h3 style="margin:24px 0 2px;font-size:15px;border-top:1px solid #eceef5;padding-top:18px">🪨 오늘 지구 곁을 지나는 소행성 (NeoWs)</h3>'
       '<div id="nstatus" class="status">불러오는 중…</div>'
       '<div class="grid"><div class="stat"><div class="lab">오늘 접근 소행성</div><div class="val" id="ncnt">--</div><div class="unit">개</div></div></div>'
       '<div id="astro"></div>'
       '<div style="font-size:11px;color:#8a8fa6;margin:2px 2px 10px;text-align:center">⬤ 크기=지름 · 색=위험(빨강)/안전(파랑) · 가로축=지구로부터 거리(달까지 거리의 배수, 로그) · 점에 마우스를 올리면 상세</div>'
       '<ul class="list" id="nlist"></ul>',
  js='''const MOON=384400; // 달까지 평균거리(km)
async function loadApod(key){
  const s=document.getElementById('status'); s.className='status'; s.textContent='불러오는 중…';
  try{
    const ctrl=new AbortController(); const to=setTimeout(()=>ctrl.abort(),12000);
    const res=await fetch('https://api.nasa.gov/planetary/apod?api_key='+key,{signal:ctrl.signal}); clearTimeout(to);
    if(res.status===429||res.status===503) throw new Error('호출 제한 — 잠시 후 다시');
    const j=await res.json(); if(j.error) throw new Error(j.error.message);
    document.getElementById('title').textContent=j.title;
    document.getElementById('date').textContent=j.date+(j.copyright?(' · © '+j.copyright):'');
    document.getElementById('media').innerHTML = j.media_type==='image'
      ? `<img class="bigimg" src="${j.url}" alt="${j.title}">`
      : `<iframe class="bigimg" style="height:420px" src="${j.url}" allowfullscreen></iframe>`;
    document.getElementById('exp').textContent=j.explanation;
    s.textContent='✓ '+j.date;
  }catch(e){ s.className='status err'; s.textContent='사진을 못 받았어요: '+e.message; }
}
async function loadNeo(key){
  const s=document.getElementById('nstatus'); s.className='status'; s.textContent='불러오는 중…';
  try{
    const t=new Date().toISOString().slice(0,10);
    const ctrl=new AbortController(); const to=setTimeout(()=>ctrl.abort(),12000);
    const res=await fetch(`https://api.nasa.gov/neo/rest/v1/feed?start_date=${t}&end_date=${t}&api_key=${key}`,{signal:ctrl.signal}); clearTimeout(to);
    if(res.status===429||res.status===503) throw new Error('호출 제한 — 잠시 후 다시');
    const j=await res.json(); if(j.error_message) throw new Error(j.error_message);
    document.getElementById('ncnt').textContent=j.element_count;
    const arr=(Object.values(j.near_earth_objects)[0]||[]).map(a=>({
      name:a.name, dia:Math.round(a.estimated_diameter.meters.estimated_diameter_max),
      km:+a.close_approach_data[0].miss_distance.kilometers,
      vel:Math.round(+a.close_approach_data[0].relative_velocity.kilometers_per_hour),
      haz:a.is_potentially_hazardous_asteroid
    })).sort((x,y)=>x.km-y.km);
    s.textContent='✓ '+t+' 기준';
    drawAstro(arr);
    document.getElementById('nlist').innerHTML=arr.map(a=>{
      const moon=(a.km/MOON).toFixed(1);
      const c=a.haz?'#ef4444':'#64748b';
      return `<li><span class="badge" style="background:${c}">${a.haz?'위험':'안전'}</span>
        <span>${a.name}<br><span class="meta">지름 약 ${a.dia.toLocaleString()}m · 최근접 ${Math.round(a.km).toLocaleString()}km(달까지 거리의 ${moon}배) · ${a.vel.toLocaleString()}km/h</span></span></li>`;
    }).join('') || '<li class="meta">오늘 접근 기록이 없어요.</li>';
  }catch(e){ s.className='status err'; s.textContent='소행성 데이터를 못 받았어요: '+e.message; }
}
function drawAstro(arr){
  const XMIN=110, XMAX=688, CY=120, EX=54;
  const xOf=ld=>{ ld=Math.max(1,Math.min(220,ld)); return XMIN+(Math.log10(ld)/Math.log10(220))*(XMAX-XMIN); };
  const n=arr.length;
  let g='<svg class="astro" viewBox="0 0 720 244" xmlns="http://www.w3.org/2000/svg">';
  g+='<defs><radialGradient id="eg" cx="34%" cy="30%"><stop offset="0" stop-color="#8fb8ff"/><stop offset="1" stop-color="#1f4fc0"/></radialGradient></defs>';
  for(let k=0;k<46;k++){ g+=`<circle cx="${(k*149)%720}" cy="${(k*83)%244}" r="${k%6?0.8:1.5}" fill="#fff" opacity="0.16"/>`; }
  g+=`<line x1="${EX}" y1="${CY}" x2="${XMAX}" y2="${CY}" stroke="#2a3553" stroke-width="1" stroke-dasharray="3 6"/>`;
  [1,10,100].forEach(v=>{ const x=xOf(v); g+=`<line x1="${x}" y1="30" x2="${x}" y2="208" stroke="#1d2742" stroke-width="1"/><text x="${x}" y="226" fill="#5b678c" font-size="10" text-anchor="middle">달거리 ${v}×</text>`; });
  g+=`<circle class="earthpulse" cx="${EX}" cy="${CY}" r="30" fill="#3b82f6" opacity="0.16"/><circle cx="${EX}" cy="${CY}" r="22" fill="url(#eg)"/><text x="${EX}" y="${CY+40}" fill="#9fb3e8" font-size="11" text-anchor="middle">지구</text>`;
  const mx=xOf(1); g+=`<circle cx="${mx}" cy="${CY}" r="6" fill="#cfd4e2"/><text x="${mx}" y="${CY-13}" fill="#8b93ab" font-size="10" text-anchor="middle">달</text>`;
  arr.forEach((a,i)=>{
    const ld=a.km/MOON, x=xOf(ld);
    const y = n>1 ? 56+(i*(126/(n-1))) : CY;
    const r = Math.max(5, Math.min(18, 5+a.dia/28));
    const c = a.haz ? '#ef4444' : '#9aa7d6';
    g+=`<g transform="translate(${x.toFixed(1)},${y.toFixed(1)})"><g class="ast" style="animation-delay:${(i*0.3).toFixed(2)}s"><g class="ast-pop" style="animation-delay:${(i*0.09).toFixed(2)}s">`
      +`<title>${a.name} · 지름 ${a.dia.toLocaleString()}m · ${Math.round(a.km).toLocaleString()}km(달거리 ${ld.toFixed(1)}배) · ${a.vel.toLocaleString()}km/h${a.haz?' · ⚠️위험':''}</title>`
      +`<circle r="${(r+7).toFixed(1)}" fill="${c}" opacity="0.16"/><circle r="${r.toFixed(1)}" fill="${c}"/>`
      +(a.dia>=140?`<text y="3.4" text-anchor="middle" font-size="9" font-weight="800" fill="#0b1224">${a.dia}m</text>`:'')
      +`</g></g></g>`;
  });
  g+='</svg>';
  document.getElementById('astro').innerHTML=g;
}
function run(){ const key=document.getElementById('key').value.trim()||'DEMO_KEY'; loadApod(key); loadNeo(key); }
run();''')

# 10) 태양·바람 에너지 (NASA POWER)
page("energy", "⚡", "태양·바람 에너지", "에너지·물리·지구", "🇰🇷 국내 OK · 🌍 전 세계",
  lead="<b>NASA POWER</b>는 위성 관측으로 전 세계 어디든 <b>태양 복사량·풍속</b>을 알려줘요. 태양광·풍력 발전소를 어디에 세우면 좋을지 가늠하는, 진짜 <b>신재생에너지 설계용</b> 데이터랍니다.",
  src_name="NASA POWER", src_url="https://power.larc.nasa.gov",
  info='''<table>
    <tr><td class="k">무엇</td><td>위치별 월평균 태양복사량·풍속 등 (NASA POWER, 위성 기반)</td></tr>
    <tr><td class="k">API 키</td><td><b>필요 없음</b> · 무료</td></tr>
    <tr><td class="k">요청 예</td><td><code>power.larc.nasa.gov/api/temporal/climatology/point?parameters=ALLSKY_SFC_SW_DWN,WS10M&amp;...</code></td></tr>
    <tr><td class="k">단위</td><td>태양복사 kWh/m²/일 · 풍속 m/s (30년 기후 평년값)</td></tr>
  </table>''',
  apply_html='''<ul>
    <li>위도가 다른 지역(<b>적도·사막·극지방</b>)을 골라 <b>서울과 일사량 비교</b></li>
    <li>우리 지역 <b>태양광 발전 잠재력</b> 가늠(일사량이 높은 달은?)</li>
    <li>태양광 LED 게이지: 일사량을 10칸으로(여름↑ 겨울↓)</li>
  </ul>''',
  chart=True,
  body='<div class="controls"><label>비교 지역</label><select id="loc" onchange="run()">'
       '<option value="-0.18|-78.47|적도 · 키토(위도 0°)">적도 · 키토 (위도 0°)</option>'
       '<option value="1.35|103.82|적도 부근 · 싱가포르(위도 1°)">적도 부근 · 싱가포르 (위도 1°)</option>'
       '<option value="25.0|30.0|사하라 사막(위도 25°)">사하라 사막 (위도 25°)</option>'
       '<option value="-23.7|133.9|호주 내륙(위도 -24°)">호주 내륙 (위도 -24°)</option>'
       '<option value="37.57|126.98|🇰🇷 서울(위도 37°)">🇰🇷 서울 (위도 37°)</option>'
       '<option value="64.13|-21.9|아이슬란드 레이캬비크(위도 64°)">아이슬란드 (위도 64°)</option>'
       '<option value="78.22|15.65|극지방 · 스발바르(위도 78°)">극지방 · 스발바르 (위도 78°)</option>'
       '</select>'
       '<label>그래프</label><select id="metric" onchange="draw()"><option value="sun">☀️ 태양 일사량</option><option value="wind">💨 풍속</option></select>'
       '<button onclick="run()">비교</button></div>'
       '<div style="font-size:12px;color:#7a7f95;margin:-6px 2px 12px">선택한 지역을 <b>막대</b>로, <b>🇰🇷서울</b>을 선으로 겹쳐 보여줘요. <b>그래프</b>를 일사량↔풍속으로 바꿔 둘 다 비교하세요!</div>'
       '<div id="status" class="status">불러오는 중…</div>'
       '<div class="grid"><div class="stat"><div class="lab">선택 지역 연평균 일사량</div><div class="val" id="sun">--</div><div class="unit">kWh/m²/일</div></div>'
       '<div class="stat"><div class="lab">🇰🇷 서울 연평균 일사량</div><div class="val" id="sunS" style="color:#E0568A">--</div><div class="unit">kWh/m²/일</div></div>'
       '<div class="stat"><div class="lab">선택 지역 연평균 풍속</div><div class="val" id="wind">--</div><div class="unit">m/s</div></div></div>'
       '<div class="chartbox"><canvas id="ch" height="130"></canvas></div>'
       '<div class="qbox"><div class="qbox-t">🔎 탐구 질문</div><ul>'
       '<li>적도(키토)와 극지방(스발바르)의 일사량을 서울과 비교해 보세요. 위도가 높아질수록 일사량은 어떻게 변하나요?</li>'
       '<li>극지방은 여름·겨울 일사량 차이가 왜 그렇게 클까요?(백야·극야) 적도는 왜 일 년 내내 비슷할까요?</li>'
       '<li>사막은 위도가 높아도 일사량이 매우 큰 편이에요. 왜 그럴까요?(구름·강수)</li>'
       '</ul></div>',
  js='''let chart, seoulCache=null, cur=null, curName='';
const M=['1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월'];
const K=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'];
async function fetchPoint(lat,lon){
  const u=`https://power.larc.nasa.gov/api/temporal/climatology/point?parameters=ALLSKY_SFC_SW_DWN,WS10M&community=RE&longitude=${lon}&latitude=${lat}&format=JSON`;
  return (await (await fetch(u)).json()).properties.parameter;
}
function draw(){
  if(!cur||!seoulCache) return;
  const metric=document.getElementById('metric').value;
  const PK = metric==='sun'?'ALLSKY_SFC_SW_DWN':'WS10M';
  const unit = metric==='sun'?'태양 일사량 (kWh/m²/일)':'풍속 (m/s, 10m 높이)';
  const tag = metric==='sun'?' 일사량':' 풍속';
  const col = metric==='sun'?'rgba(245,158,11,.65)':'rgba(59,130,246,.55)';
  const a=K.map(k=>cur[PK][k]), b=K.map(k=>seoulCache[PK][k]);
  const isSeoul=curName.includes('서울');
  const ds=[{type:'bar',label:curName+tag,data:a,backgroundColor:col,yAxisID:'y'}];
  if(!isSeoul) ds.push({type:'line',label:'🇰🇷 서울'+tag,data:b,borderColor:'#E0568A',backgroundColor:'rgba(224,86,138,.08)',tension:.3,pointRadius:0,borderWidth:2,yAxisID:'y'});
  if(chart) chart.destroy();
  chart=new Chart(document.getElementById('ch'),{data:{labels:M,datasets:ds},
    options:{responsive:true,interaction:{intersect:false,mode:'index'},
      scales:{y:{beginAtZero:true,title:{display:true,text:unit}}}}});
}
async function run(){
  const [lat,lon,name]=document.getElementById('loc').value.split('|');
  const s=document.getElementById('status'); s.className='status'; s.textContent='불러오는 중…';
  try{
    const p=await fetchPoint(lat,lon);
    if(!seoulCache) seoulCache=await fetchPoint(37.57,126.98);
    cur=p; curName=name;
    document.getElementById('sun').textContent=p.ALLSKY_SFC_SW_DWN.ANN.toFixed(2);
    document.getElementById('sunS').textContent=seoulCache.ALLSKY_SFC_SW_DWN.ANN.toFixed(2);
    document.getElementById('wind').textContent=p.WS10M.ANN.toFixed(1);
    s.textContent='✓ '+name+' vs 서울 · 30년 기후 평년값';
    draw();
  }catch(e){ s.className='status err'; s.textContent='데이터를 받지 못했어요: '+e; }
}
document.getElementById('loc').value='-0.18|-78.47|적도 · 키토(위도 0°)';
run();''')

# 12) 나라별 CO2·에너지 (World Bank)
page("worldbank", "🌱", "나라별 CO₂·에너지", "환경·에너지·물리", "🌍 전 세계(국내 포함)",
  lead="<b>세계은행(World Bank)</b>이 모은 나라별 통계예요. 1인당 CO₂ 배출량, 재생에너지 비중 같은 지표로 <b>우리나라와 다른 나라를 데이터로 비교</b>해 볼 수 있어요.",
  src_name="World Bank Open Data", src_url="https://data.worldbank.org",
  info='''<table>
    <tr><td class="k">무엇</td><td>200여 개국 개발·환경·에너지 지표 (World Bank)</td></tr>
    <tr><td class="k">API 키</td><td><b>필요 없음</b> · 무료</td></tr>
    <tr><td class="k">요청 예</td><td><code>api.worldbank.org/v2/country/KR;JP;US/indicator/<i>지표코드</i>?format=json</code></td></tr>
    <tr><td class="k">예시 지표</td><td>1인당 CO₂ <code>EN.GHG.CO2.PC.CE.AR5</code> · 재생에너지 비중 <code>EG.FEC.RNEW.ZS</code></td></tr>
  </table>''',
  apply_html='''<ul>
    <li>한국 vs 주요국 <b>1인당 CO₂ 배출 비교</b></li>
    <li>나라별 <b>재생에너지 비중</b> 비교 → 우리나라의 위치는?</li>
    <li>지표를 바꿔 인구·GDP 등 다른 데이터로 확장</li>
  </ul>''',
  chart=True,
  head='<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>',
  body='<div class="controls"><label>지표</label><select id="ind" onchange="run()">'
       '<option value="EN.GHG.CO2.PC.CE.AR5|1인당 CO₂ 배출량 (톤)|Reds">1인당 CO₂ 배출량 (톤)</option>'
       '<option value="EG.FEC.RNEW.ZS|재생에너지 비중 (%)|Greens">재생에너지 비중 (%)</option>'
       '</select><button onclick="run()">불러오기</button></div>'
       '<div id="status" class="status">불러오는 중…</div>'
       '<div id="wmap" style="height:400px;border-radius:14px;overflow:hidden;border:1px solid var(--line);"></div>'
       '<div style="font-size:11.5px;color:#7a7f95;margin:8px 2px;text-align:center"><b id="yr">--</b> · 색이 진할수록 값이 큰 나라 · 나라에 마우스를 올리면 값이 보여요</div>'
       '<div class="grid"><div class="stat" style="border-color:#E0568A"><div class="lab">🇰🇷 한국 값</div><div class="val" id="kr">--</div><div class="unit" id="kru"></div></div>'
       '<div class="stat"><div class="lab">세계 중앙값</div><div class="val" id="med" style="font-size:24px">--</div><div class="unit" id="medu"></div></div>'
       '<div class="stat"><div class="lab">한국 순위 (값 큰 순)</div><div class="val" id="rank" style="font-size:22px">--</div><div class="unit" id="ranku"></div></div></div>'
       '<h3 style="margin:18px 0 2px;font-size:14px">📊 주요국 비교</h3>'
       '<div class="chartbox"><canvas id="ch" height="150"></canvas></div>'
       '<h3 style="margin:22px 0 2px;font-size:14px">🫧 CO₂ vs 재생에너지 — 한국은 어디에?</h3>'
       '<div class="chartbox"><canvas id="scatter" height="150"></canvas></div>'
       '<div style="font-size:11.5px;color:#7a7f95;margin:6px 2px;text-align:center">가로=1인당 CO₂(톤) · 세로=재생에너지 비중(%) · 원 크기=인구 · <b style="color:#E0568A">🇰🇷 한국은 분홍 큰 원</b> · <i>각국 최신 자료 기준</i></div>'
       '<div class="qbox"><div class="qbox-t">🔎 탐구 질문</div><ul>'
       '<li>지도에서 색이 진한(값이 큰) 나라들은 주로 어느 대륙에 있나요? 어떤 공통점이 있을까요?</li>'
       '<li>버블 차트에서 한국은 어느 구역에 있나요? (오른쪽 아래 = CO₂ 많고 재생E 적음)</li>'
       '<li>우리나라의 세계 순위는 몇 위인가요? 생각보다 높나요, 낮나요?</li>'
       '<li>지표를 CO₂ ↔ 재생에너지로 바꿔 보세요. 두 지도의 색 분포는 반대인가요, 비슷한가요?</li>'
       '</ul></div>',
  js='''let chart, META=null;
const MAJ=[['KOR','한국'],['JPN','일본'],['USA','미국'],['DEU','독일'],['FRA','프랑스'],['CHN','중국'],['IND','인도'],['BRA','브라질']];
// 명시적 색 스케일 — 값이 클수록 '진하게'(낮음=연함 → 높음=진함)
const SCALES={
  Reds:[[0,'#fff5f0'],[0.5,'#fb6a4a'],[1,'#99000d']],
  Greens:[[0,'#f7fcf5'],[0.5,'#74c476'],[1,'#00441b']]
};
async function getMeta(){
  if(META) return META;
  const d=await (await fetch('https://api.worldbank.org/v2/country?format=json&per_page=400')).json();
  META={}; (d[1]||[]).forEach(c=>{ if(c.region && c.region.value!=='Aggregates') META[c.id]={name:c.name}; });
  return META;
}
async function run(){
  const [code,label,scale]=document.getElementById('ind').value.split('|');
  const s=document.getElementById('status'); s.className='status'; s.textContent='불러오는 중…';
  try{
    const meta=await getMeta();
    const u=`https://api.worldbank.org/v2/country/all/indicator/${code}?format=json&date=2018:2023&per_page=2000`;
    const arr=(await (await fetch(u)).json())[1]||[];
    // 기준 연도 = '한국(KOR)이 가진 가장 최근 연도'. 그 해에 자료 있는 나라만 같은 해로 비교
    // (전체 국가 수가 적더라도 한국의 최신값을 우선해서 보여줌)
    const krYears=arr.filter(r=>r.countryiso3code==='KOR'&&r.value!=null).map(r=>r.date).sort();
    const anyYears=[...new Set(arr.filter(r=>r.value!=null&&r.countryiso3code&&meta[r.countryiso3code]).map(r=>r.date))].sort();
    const refYear=(krYears.length?krYears:anyYears).pop();
    const latest={};
    arr.forEach(r=>{ const k=r.countryiso3code; if(r.value==null||!k||!(k in meta)||r.date!==refYear)return; latest[k]={v:r.value,y:r.date}; });
    const locs=Object.keys(latest), z=locs.map(k=>latest[k].v),
          text=locs.map(k=>`${meta[k].name}: ${latest[k].v.toFixed(1)}`);
    s.textContent='✓ '+label+' · '+refYear+'년(한국 최신 자료) · '+locs.length+'개국 같은 해 비교';
    document.getElementById('yr').textContent=refYear+'년 기준(한국 최신 자료)';
    // 세계 지도(choropleth)
    const krv = latest['KOR'] ? latest['KOR'].v.toFixed(1) : '-';
    Plotly.newPlot('wmap',[
      {type:'choropleth',locationmode:'ISO-3',locations:locs,z,text,
       hoverinfo:'text',colorscale:(SCALES[scale]||scale),reversescale:false,zmin:0,
       marker:{line:{color:'#ffffff',width:0.4}},colorbar:{thickness:12,len:0.9}},
      {type:'scattergeo',lon:[127.8],lat:[36.3],mode:'markers+text',
       text:['🇰🇷 한국 '+krv],textposition:'middle right',hoverinfo:'skip',showlegend:false,
       textfont:{size:12,color:'#b3245e'},marker:{size:9,color:'#E0568A',line:{color:'#fff',width:1.5}}}
    ],
      {geo:{showframe:false,showcoastlines:false,projection:{type:'natural earth'},bgcolor:'rgba(0,0,0,0)'},
       margin:{t:6,b:6,l:0,r:0},paper_bgcolor:'rgba(0,0,0,0)'},
      {displayModeBar:false,responsive:true});
    // 한국 값 · 세계 중앙값 · 순위(상/하위)
    const kr=latest['KOR'];
    const vals=locs.map(k=>latest[k].v);
    const desc=[...vals].sort((a,b)=>b-a);
    const med=[...vals].sort((a,b)=>a-b)[Math.floor(vals.length/2)];
    const unit=label.replace(/.*\\(|\\)/g,'');
    document.getElementById('kr').textContent = kr? kr.v.toFixed(1):'-';
    document.getElementById('kru').textContent = unit;
    document.getElementById('med').textContent = med.toFixed(1);
    document.getElementById('medu').textContent = unit;
    if(kr){ const rank=desc.indexOf(kr.v)+1;
      const pos = rank<=vals.length*0.25?'상위권 🔺' : rank>=vals.length*0.75?'하위권 🔻' : '중간권';
      document.getElementById('rank').textContent = rank+'위';
      document.getElementById('ranku').textContent = `전체 ${vals.length}개국 중 · ${pos}`;
    } else { document.getElementById('rank').textContent='-'; document.getElementById('ranku').textContent=''; }
    // 주요국 비교 막대
    const rows=MAJ.map(([id,ko])=>({ko,v:latest[id]?latest[id].v:null})).filter(r=>r.v!=null).sort((a,b)=>b.v-a.v);
    if(chart) chart.destroy();
    chart=new Chart(document.getElementById('ch'),{type:'bar',data:{labels:rows.map(r=>r.ko),
      datasets:[{label,data:rows.map(r=>r.v),backgroundColor:rows.map(r=>r.ko==='한국'?'#E0568A':'#5B6CF0')}]},
      options:{indexAxis:'y',responsive:true,plugins:{legend:{display:false}}}});
  }catch(e){ s.className='status err'; s.textContent='데이터를 받지 못했어요: '+e; }
}
// 버블 차트용: 지표별 최신 비공백값 한 번에
async function fetchLatest(code){
  const u=`https://api.worldbank.org/v2/country/all/indicator/${code}?format=json&date=2018:2023&per_page=2000`;
  const arr=(await (await fetch(u)).json())[1]||[];
  const o={};
  arr.forEach(r=>{ const k=r.countryiso3code; if(r.value==null||!k)return; if(!(k in o)||r.date>o[k].y) o[k]={v:r.value,y:r.date}; });
  const m={}; for(const k in o) m[k]=o[k].v; return m;
}
let scatChart;
async function drawScatter(){
  try{
    const meta=await getMeta();
    const [co2,ren,pop]=await Promise.all([
      fetchLatest('EN.GHG.CO2.PC.CE.AR5'), fetchLatest('EG.FEC.RNEW.ZS'), fetchLatest('SP.POP.TOTL')]);
    const others=[], krp=[];
    for(const k in meta){ if(co2[k]==null||ren[k]==null) continue;
      const r=pop[k]?Math.max(4,Math.min(34,Math.sqrt(pop[k])/1250)):5;
      const pt={x:co2[k],y:ren[k],r,name:meta[k].name};
      (k==='KOR'?krp:others).push(pt); }
    if(krp[0]) krp[0].r=Math.max(krp[0].r,11);
    if(scatChart) scatChart.destroy();
    scatChart=new Chart(document.getElementById('scatter'),{type:'bubble',data:{datasets:[
      {label:'다른 나라',data:others,backgroundColor:'rgba(91,108,240,.35)',borderColor:'rgba(91,108,240,.5)'},
      {label:'🇰🇷 한국',data:krp,backgroundColor:'#E0568A',borderColor:'#fff',borderWidth:2}]},
      options:{responsive:true,plugins:{legend:{display:true,position:'top'},
        tooltip:{callbacks:{label:c=>`${c.raw.name}: CO₂ ${c.raw.x.toFixed(1)}t · 재생E ${c.raw.y.toFixed(1)}%`}}},
        scales:{x:{title:{display:true,text:'1인당 CO₂ 배출량 (톤)'},beginAtZero:true},
                y:{title:{display:true,text:'재생에너지 비중 (%)'},beginAtZero:true}}}});
  }catch(e){ /* 버블 실패는 조용히 무시 */ }
}
run();
drawScatter();''')

# ===================================================================
# 갤러리 index
GAL = [
 ("weather","🌤️","오늘의 날씨","지구과학·환경","오늘 하루 기온은 어떻게 변할까? 일교차가 큰 날은 언제?"),
 ("airquality","🌫️","미세먼지","환경","지금 우리 동네 공기는 안전할까? 언제 가장 나쁠까?"),
 ("earthquake","🌍","전 세계 지진","지구과학","지진은 왜 특정 띠(불의 고리)에 몰릴까?","map"),
 ("iss","🛰️","ISS 위치","천문·물리","우주정거장은 지금 어디를? 경로는 왜 물결칠까?","map"),
 ("sunrise","🌅","일출·일몰","천문·지구과학","계절마다 낮 길이는 왜 달라질까? 극지방은?"),
 ("spaceweather","🌞","우주날씨 Kp","천문·지구과학","태양 폭풍이 세지면 오로라가 보일까?"),
 ("pubchem","⚗️","물질 정보","화학","물·카페인·포도당… 분자량은 얼마나 다를까?"),
 ("gbif","🐦","생물 관찰","생물","이 생물은 어디에 사나? 도시 vs 산?","map"),
 ("nasa","🔭","NASA 우주 데이터","천문","오늘의 우주 사진은? 지구 곁 소행성은 몇 개?"),
 ("energy","⚡","태양·바람 에너지","에너지·물리·지구","우리 지역은 태양광·풍력 중 뭐가 유리?"),
 ("worldbank","🌱","나라별 CO₂·에너지","환경·에너지·물리","우리나라 1인당 CO₂는 다른 나라보다?"),
]
def gcard(item):
    s, e, t, sub, hook = item[0], item[1], item[2], item[3], item[4]
    badge = '<span class="gmap">🗺️ 지도</span>' if (len(item) > 5 and item[5] == "map") else ''
    return (f'<a class="gcard" href="{s}.html"><div class="ge">{e}{badge}</div>'
            f'<div class="gt">{t}</div><div class="gs">{sub}</div>'
            f'<div class="ghook">🔎 {hook}</div></a>')
cards = "".join(gcard(it) for it in GAL)
index_html = f'''<!DOCTYPE html>
<html lang="ko"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" type="image/svg+xml" href="../favicon.svg">
<title>오픈 API 라이브 대시보드 갤러리</title>
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<link rel="stylesheet" href="lab.css">
</head><body>
<div class="wrap">
  <a class="back" href="../index.html">← 교재로 돌아가기</a>
  <header class="phead">
    <div class="bigemoji">🛰️🌤️⚗️</div>
    <h1>오픈 API <span class="pico-accent">데이터 탐구실</span></h1>
    <p style="color:#7a7f95;font-size:14px;max-width:600px;margin:6px auto 0">
      세상의 <b>공개 데이터(Open API)</b>를 브라우저에서 직접 받아와 그려 보는 탐구실이에요.
      카드를 눌러 <b>살아 있는 데이터</b>를 만나고, 아래 3단계로 탐구해 보세요.</p>
  </header>

  <div class="steps3">
    <div class="s3"><div class="s3n">1</div><b>관찰</b><span>지금 데이터가 어떤 모습인지 살펴보기</span></div>
    <div class="s3"><div class="s3n">2</div><b>질문</b><span>각 페이지의 ‘🔎 탐구 질문’에 답해 보기</span></div>
    <div class="s3"><div class="s3n">3</div><b>연결</b><span>이 데이터를 피코·LED로 만들면? (교재 부록)</span></div>
  </div>

  <div class="gallery">{cards}</div>

  <div class="card" style="margin-top:18px">
    <h2 style="font-size:14px;font-weight:800;margin-bottom:8px">💡 API가 뭐예요? — 한 줄 요약</h2>
    <p style="font-size:13.5px;color:#44464f;line-height:1.8">관공서에서 <b>등본</b>을 떼듯, ‘데이터를 가진 기관에 정해진 양식으로 신청(요청)하면 정해진 형식으로 발급(응답)해 주는 창구’가 <b>API</b>예요.
    위 대시보드는 모두 <b>무료</b>로 브라우저에서 바로 호출해요(NASA만 키 필요, 페이지에 포함). 더 자세한 설명은 교재 5장과 부록에 있어요.</p>
    <p style="font-size:12.5px;color:#7a7f95;line-height:1.7;margin-top:10px">🇰🇷 <b>국내 공식 데이터</b>가 필요하면 <a href="https://www.data.go.kr" target="_blank" rel="noopener" style="color:#3b47c2;font-weight:600">공공데이터포털 ↗</a>에서 무료 키를 받아 쓰세요 — 기상청(날씨·지진), 에어코리아(미세먼지), 전력거래소(전력수급) 등 국내 정확도가 높습니다.</p>
  </div>

  <footer>모두 공개 데이터 · 브라우저에서 바로 호출(CORS 허용 확인) · 데이터는 각 제공처의 것입니다.</footer>
</div>
</body></html>'''
with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)

print("대시보드 생성 완료 ·", len(GAL), "개 페이지 + 갤러리 + lab.css")
