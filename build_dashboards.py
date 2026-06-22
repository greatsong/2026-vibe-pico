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
         src_name="", src_url="", refs=(), maps=False):
    src = (f'<a class="srclink" href="{src_url}" target="_blank" rel="noopener">🔗 원 데이터 출처: {src_name} ↗</a>'
           if src_url else "")
    refhtml = ""
    if refs:
        chips = "".join(f'<a class="refchip" href="{u}" target="_blank" rel="noopener">{l}</a>' for l, u in refs)
        refhtml = f'<div class="refs"><span class="refs-t">📺 더 보기</span>{chips}</div>'
    html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · 라이브 대시보드</title>
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<link rel="stylesheet" href="lab.css">
{CHART if chart else ""}
{LEAFLET if maps else ""}
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

  <section class="card apply">
    <h2>💡 이렇게 응용해 보세요</h2>
    {apply_html}
  </section>

  <footer>데이터 기반 탐구 프로젝트 · 바이브 피지컬 코딩 &nbsp;|&nbsp; 데이터는 각 API 제공처의 것입니다.</footer>
</div>
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
.pico-accent{background:linear-gradient(120deg,var(--pico1),var(--pico2));-webkit-background-clip:text;background-clip:text;color:transparent;font-weight:900;}
'''
with open(os.path.join(OUT, "lab.css"), "w", encoding="utf-8") as f:
    f.write(LAB_CSS)

SEOUL = ('<div class="controls">'
         '<label>위도</label><input id="lat" value="37.5665">'
         '<label>경도</label><input id="lon" value="126.9780">'
         '<button onclick="run()">불러오기</button></div>')

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
    <li>강수확률을 <b>10칸 LED</b>로(3장 ‘날씨 시계’)</li>
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
       '<div class="stat"><div class="lab">PM10 (미세)</div><div class="val" id="v10">--</div><div class="unit">µg/m³</div></div></div>'
       '<div class="chartbox"><canvas id="ch" height="120"></canvas></div>',
  chart=True,
  js='''let chart;
function grade(pm){ if(pm<=15)return['좋음','#22c55e']; if(pm<=35)return['보통','#3b82f6']; if(pm<=75)return['나쁨','#f59e0b']; return['매우나쁨','#ef4444']; }
async function run(){
  const lat=document.getElementById('lat').value, lon=document.getElementById('lon').value;
  const s=document.getElementById('status'); s.className='status'; s.textContent='불러오는 중…';
  try{
    const u=`https://air-quality-api.open-meteo.com/v1/air-quality?latitude=${lat}&longitude=${lon}&current=pm2_5,pm10&hourly=pm2_5&timezone=Asia%2FSeoul&forecast_days=1`;
    const j=await (await fetch(u)).json();
    const pm=j.current.pm2_5, [name,color]=grade(pm);
    document.getElementById('v25').textContent=pm; document.getElementById('v25').style.color=color;
    document.getElementById('t25').textContent='µg/m³ · '+name;
    document.getElementById('g25').style.borderColor=color;
    document.getElementById('v10').textContent=j.current.pm10;
    s.textContent='✓ 현재 기준 · 등급: '+name;
    const labels=j.hourly.time.map(x=>x.slice(11,16)), data=j.hourly.pm2_5;
    if(chart) chart.destroy();
    chart=new Chart(document.getElementById('ch'),{type:'line',data:{labels,datasets:[{label:'PM2.5',data,borderColor:color,backgroundColor:color+'22',fill:true,tension:.3,pointRadius:0}]},options:{responsive:true,plugins:{legend:{display:false}}}});
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
  body='<div class="controls"><label>기간·규모</label><select id="feed">'
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
    <tr><td class="k">그림</td><td>같은 주소의 <code>/PNG</code> 로 2D 구조 이미지를 받습니다</td></tr>
  </table>''',
  apply_html='''<ul>
    <li>여러 물질 <b>분자량 비교</b>(물·포도당·카페인…)</li>
    <li>분자량 크기를 <b>LED 막대</b>로</li>
    <li>화학식만 보여 주고 <b>물질 맞히기 퀴즈</b></li>
  </ul>''',
  body=f'<div class="controls"><label>인기 물질</label><select id="preset" onchange="pick()">{PRESET}</select>'
       f'<label>또는 직접</label><input id="name" list="cmplist" value="caffeine" style="width:160px" placeholder="영문 이름">'
       f'<datalist id="cmplist">{DLIST}</datalist><button onclick="run()">검색</button></div>'
       '<div style="font-size:12px;color:#7a7f95;margin:-6px 2px 12px">영문 이름으로 검색돼요(예: water, glucose). 목록에 없는 물질은 '
       '<a href="https://pubchem.ncbi.nlm.nih.gov" target="_blank" rel="noopener" style="color:#3b47c2;font-weight:600">PubChem에서 직접 검색 ↗</a> 후 영문명을 넣어 보세요.</div>'
       '<div id="status" class="status">불러오는 중…</div>'
       '<div class="molwrap"><img id="img" alt="구조" src=""><div>'
       '<div class="grid" style="grid-template-columns:1fr"><div class="stat"><div class="lab">분자식</div><div class="val" id="formula" style="font-size:24px">--</div></div>'
       '<div class="stat"><div class="lab">분자량</div><div class="val" id="mw">--</div><div class="unit">g/mol</div></div></div></div></div>',
  js='''function pick(){ const v=document.getElementById('preset').value; if(v){ document.getElementById('name').value=v; run(); } }
async function run(){
  const name=document.getElementById('name').value.trim();
  const s=document.getElementById('status'); s.className='status'; s.textContent='불러오는 중…';
  try{
    const base='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/'+encodeURIComponent(name);
    const j=await (await fetch(base+'/property/MolecularFormula,MolecularWeight/JSON')).json();
    const p=j.PropertyTable.Properties[0];
    document.getElementById('formula').textContent=p.MolecularFormula;
    document.getElementById('mw').textContent=parseFloat(p.MolecularWeight).toFixed(2);
    document.getElementById('img').src=base+'/PNG';
    s.textContent='✓ '+name+' (CID '+p.CID+')';
  }catch(e){ s.className='status err'; s.textContent='그 이름의 물질을 못 찾았어요. 영문 이름으로 다시 시도해 보세요.'; }
}
run();''')

# 8) GBIF 생물
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
  maps=True,
  body='<div class="controls"><label>학명</label><input id="sp" value="Pica pica" style="width:180px"><button onclick="run()">검색</button>'
       '<span style="font-size:12px;color:#7a7f95">예: Pica pica(까치) · Egretta(백로) · Cervus nippon(꽃사슴)</span></div>'
       '<div id="status" class="status">불러오는 중…</div>'
       '<div class="grid"><div class="stat"><div class="lab">한국 관찰 기록</div><div class="val" id="cnt">--</div><div class="unit">건</div></div>'
       '<div class="stat"><div class="lab">지도에 표시(좌표 있는 것)</div><div class="val" id="mcnt" style="font-size:22px">--</div><div class="unit">개 지점</div></div></div>'
       '<div id="map" class="map"></div>'
       '<div style="font-size:11px;color:#7a7f95;margin:8px 2px;text-align:center">최근 좌표가 있는 관찰 지점을 지도에 표시 · 점을 누르면 관찰 날짜·장소</div>'
       '<ul class="list" id="list"></ul>'
       '<div class="qbox"><div class="qbox-t">🔎 탐구 질문</div><ul>'
       '<li>이 생물은 도시 근처에 많나요, 산·강 근처에 많나요? 왜 그럴까요?</li>'
       '<li>관찰이 특정 계절에 몰려 있나요? 철새·곤충이라면 무엇을 뜻할까요?</li>'
       '<li>다른 종으로 바꿔 검색해 분포를 비교해 보세요(흔한 종 vs 보기 드문 종).</li>'
       '</ul></div>',
  js='''let map, layer;
async function run(){
  const sp=document.getElementById('sp').value.trim();
  const s=document.getElementById('status'); s.className='status'; s.textContent='불러오는 중…';
  if(!map){ map=L.map('map').setView([36.4,127.8],6);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'© OpenStreetMap',maxZoom:14}).addTo(map); }
  try{
    const u=`https://api.gbif.org/v1/occurrence/search?country=KR&scientificName=${encodeURIComponent(sp)}&hasCoordinate=true&limit=120`;
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
    <tr><td class="k">API 키</td><td><b>필요</b> · <b>api.nasa.gov</b>에서 무료 발급(이 페이지엔 키가 들어 있어요)</td></tr>
    <tr><td class="k">요청 예</td><td><code>api.nasa.gov/planetary/apod?api_key=…</code><br><code>api.nasa.gov/neo/rest/v1/feed?start_date=…&amp;end_date=…&amp;api_key=…</code></td></tr>
    <tr><td class="k">확장</td><td>같은 키로 지구사진(EPIC), 화성 날씨 등 다른 API도 호출 가능</td></tr>
  </table>''',
  apply_html='''<ul>
    <li>교실 모니터에 <b>매일 우주사진</b> 띄우기(설명 번역해 ‘오늘의 천문 이야기’)</li>
    <li>오늘 가장 가까이 오는 소행성 <b>거리·크기 비교</b>(달까지 거리와 견주기)</li>
    <li><b>위험 소행성</b>(PHA)이 있으면 알림 LED — 지름·거리 데이터로 탐구</li>
  </ul>''',
  body='<div class="controls"><label>API 키</label><input id="key" value="SCIgZnFwHKdey57AE3CkOMG87y4DDRDiUi152ry2" style="width:300px"><button onclick="run()">불러오기</button></div>'
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

# ===================================================================
# 갤러리 index
GAL = [
 ("weather","🌤️","오늘의 날씨","지구과학·환경","오늘 하루 기온은 어떻게 변할까? 일교차가 큰 날은 언제?"),
 ("airquality","🌫️","미세먼지","환경","지금 우리 동네 공기는 안전할까? 언제 가장 나쁠까?"),
 ("earthquake","🌍","전 세계 지진","지구과학","지진은 왜 특정 띠(불의 고리)에 몰릴까?","map"),
 ("iss","🛰️","ISS 위치","천문·물리","우주정거장은 지금 어디를? 경로는 왜 물결칠까?","map"),
 ("sunrise","🌅","일출·일몰","천문·지구","계절마다 낮 길이는 왜 달라질까? 극지방은?"),
 ("spaceweather","🌞","우주날씨 Kp","천문·지구","태양 폭풍이 세지면 오로라가 보일까?"),
 ("pubchem","⚗️","물질 정보","화학","물·카페인·포도당… 분자량은 얼마나 다를까?"),
 ("gbif","🐦","생물 관찰","생물","이 생물은 어디에 사나? 도시 vs 산?","map"),
 ("nasa","🔭","NASA 우주 데이터","천문","오늘의 우주 사진은? 지구 곁 소행성은 몇 개?"),
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
    여기 9곳은 모두 <b>무료</b>이고, NASA만 키가 필요합니다(페이지에 포함). 더 자세한 설명은 교재 3장과 부록에 있어요.</p>
  </div>

  <footer>모두 공개 데이터 · 브라우저에서 바로 호출(CORS 허용 확인) · 데이터는 각 제공처의 것입니다.</footer>
</div>
</body></html>'''
with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)

print("대시보드 생성 완료 ·", len(GAL), "개 페이지 + 갤러리 + lab.css")
