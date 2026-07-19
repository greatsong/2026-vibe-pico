# -*- coding: utf-8 -*-
"""피코 바이브 코딩 연수 자료 사이트 생성기 (Ch0~5)

- 연수생 배포용 정적 HTML. 모든 코드는 snippets/ 의 검증된 .py 파일에서 읽어
  '복사하면 그대로 실행되는' 완결형으로 싣는다.
- 독학용 교재 스타일: 왜 배우나요 → 핵심개념 → 따라하기 → 전체코드
  → 자주 하는 실수 → 스스로 점검 블록을 지원한다.
"""
import html, os, re

BASE = os.path.dirname(os.path.abspath(__file__))

def load(rel):
    """snippets 등 파일 내용을 그대로 읽어온다."""
    with open(os.path.join(BASE, rel), encoding="utf-8") as f:
        return f.read()

def esc(s):
    return html.escape(s, quote=True)

# ===================================================================
#  펌웨어 다운로드 카드 (Ch0)
# ===================================================================
FW_VER = "v1.28.0"
FW_FILE = "firmware/RPI_PICO2_W-v1.28.0.uf2"
FW_SIZE = "1.64 MB"
FW_CARD = f'''<div class="fw-card">
  <div class="fw-top">
    <div class="fw-info">
      <span class="fw-badge">🔌 처음 한 번만 — 펌웨어 설치</span>
      <h3 class="fw-title">MicroPython 펌웨어 다운로드</h3>
      <p class="fw-meta">Raspberry Pi Pico 2&nbsp;W&nbsp;/&nbsp;WH 전용 · MicroPython <b>{FW_VER}</b> · UF2 {FW_SIZE}</p>
    </div>
    <a class="dl-btn" href="{FW_FILE}" download>⬇&nbsp;&nbsp;펌웨어 내려받기 (.uf2)</a>
  </div>
  <div class="fw-steps-wrap">
    <div class="fw-steps-title">이렇게 설치해요 — 드래그 한 번이면 끝</div>
    <ol class="fw-steps">
      <li><b>BOOTSEL 버튼을 누른 채</b> 피코를 USB 케이블로 컴퓨터에 연결합니다. <span class="fw-dim">(순서 중요! 버튼 먼저 누르고 꽂기)</span></li>
      <li>컴퓨터에 <code>RP2350</code> 이라는 USB 드라이브가 나타나면 버튼에서 손을 뗍니다. <span class="fw-dim">(Pico 2 계열. 구형 Pico는 <code>RPI-RP2</code>)</span></li>
      <li>위 버튼으로 받은 <b>.uf2 파일을 <code>RP2350</code> 드라이브로 복사(드래그)</b>합니다.</li>
      <li>피코가 자동으로 재부팅되며 <b>설치 완료</b> — 이제 Thonny에서 코드를 올릴 수 있어요.</li>
    </ol>
  </div>
  <p class="fw-note">⚠️ 이 파일은 <b>Pico&nbsp;2&nbsp;W (WH)</b> 전용입니다. 다른 보드라면 <a href="https://micropython.org/download/RPI_PICO2_W/" target="_blank" rel="noopener">MicroPython 공식 다운로드 페이지</a>에서 맞는 펌웨어를 받으세요. · Thonny의 <i>‘Install MicroPython…’</i> 메뉴로 설치해도 됩니다.</p>
</div>'''

# 하드웨어 연결 다이어그램 (SVG)
HW_FIGURE = '''<div class="figure"><svg class="hw-svg" viewBox="0 0 780 256" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="피코와 그로브 쉴드, LED, 가스센서 연결도">
  <defs>
    <marker id="ah" markerWidth="10" markerHeight="10" refX="6.5" refY="4.5" orient="auto">
      <path d="M0,0 L9,4.5 L0,9 z" fill="#aeb4c8"/>
    </marker>
    <filter id="sh" x="-20%" y="-20%" width="140%" height="150%">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#2a3568" flood-opacity="0.12"/>
    </filter>
  </defs>

  <!-- 연결선 -->
  <line x1="152" y1="122" x2="246" y2="122" stroke="#c6cadb" stroke-width="2.5" marker-end="url(#ah)"/>
  <text x="199" y="113" text-anchor="middle" font-size="11.5" fill="#8a8fa6" font-weight="600">USB</text>
  <line x1="486" y1="150" x2="556" y2="150" stroke="#c6cadb" stroke-width="2.5" marker-end="url(#ah)"/>
  <line x1="486" y1="192" x2="556" y2="192" stroke="#c6cadb" stroke-width="2.5" marker-end="url(#ah)"/>
  <text x="521" y="140" text-anchor="middle" font-size="10.5" fill="#a7adc0" font-weight="600">그로브 케이블</text>

  <!-- PC / 노트북 -->
  <g filter="url(#sh)">
    <rect x="20" y="86" width="132" height="92" rx="16" fill="#ffffff" stroke="#e7e9f3"/></g>
  <rect x="42" y="102" width="88" height="48" rx="5" fill="#f2f4fb" stroke="#d7dbeb"/>
  <rect x="74" y="150" width="24" height="7" rx="2" fill="#d7dbeb"/>
  <rect x="62" y="157" width="48" height="5" rx="2.5" fill="#e7e9f3"/>
  <text x="86" y="174" text-anchor="middle" font-size="12.5" font-weight="700" fill="#2b2d3a">PC / 노트북</text>

  <!-- 피코 + 그로브 쉴드 -->
  <g filter="url(#sh)">
    <rect x="254" y="60" width="232" height="150" rx="20" fill="#eef0ff" stroke="#c3c9f5"/></g>
  <text x="370" y="94"  text-anchor="middle" font-size="11" fill="#6b78e8" font-weight="600">Raspberry Pi</text>
  <text x="370" y="116" text-anchor="middle" font-size="18" font-weight="800" fill="#2b2d3a">Pico 2 WH</text>
  <text x="370" y="137" text-anchor="middle" font-size="11.5" fill="#8a8fb0">+ 그로브 쉴드</text>
  <!-- 포트 (오른쪽 가장자리, 제목과 겹치지 않게 아래쪽) -->
  <text x="470" y="154" text-anchor="end" font-size="12" font-weight="800" fill="#1f9d63">D16</text>
  <circle cx="486" cy="150" r="7" fill="#fff" stroke="#1f9d63" stroke-width="2.5"/>
  <circle cx="486" cy="150" r="3" fill="#1f9d63"/>
  <text x="470" y="196" text-anchor="end" font-size="12" font-weight="800" fill="#d4762a">A0</text>
  <circle cx="486" cy="192" r="7" fill="#fff" stroke="#d4762a" stroke-width="2.5"/>
  <circle cx="486" cy="192" r="3" fill="#d4762a"/>

  <!-- WS2813 LED 바 -->
  <g filter="url(#sh)">
    <rect x="558" y="124" width="204" height="54" rx="15" fill="#ffffff" stroke="#d7defb"/></g>
  <rect x="576" y="139" width="11" height="24" rx="2.5" fill="#3b82f6"/>
  <rect x="589" y="139" width="11" height="24" rx="2.5" fill="#22c55e"/>
  <rect x="602" y="139" width="11" height="24" rx="2.5" fill="#f59e0b"/>
  <text x="624" y="147" font-size="12.5" font-weight="700" fill="#2b2d3a">WS2813 LED 바 · 10개</text>
  <text x="624" y="165" font-size="10.5" fill="#8a8fa6">그로브 D16 = GP16 · 디지털</text>

  <!-- MQ-2 가스센서 -->
  <g filter="url(#sh)">
    <rect x="558" y="166" width="204" height="54" rx="15" fill="#ffffff" stroke="#f3e1cb"/></g>
  <circle cx="588" cy="193" r="12" fill="#b45309"/>
  <circle cx="588" cy="193" r="6" fill="#e8a45c"/>
  <text x="612" y="189" font-size="12.5" font-weight="700" fill="#2b2d3a">MQ-2 가스센서 (핀헤더형)</text>
  <text x="612" y="207" font-size="10.5" fill="#8a8fa6">암 점퍼 케이블 → A0 = GP26 · 노랑→AO</text>

  <!-- 범례 -->
  <text x="20" y="244" font-size="10.5" fill="#a7adc0">● 그로브 포트  ·  LED → D16(GP16, 디지털·그로브 케이블)  ·  MQ-2 → A0(GP26, 아날로그·암 점퍼 케이블)</text>
</svg></div>'''

# API = 관공서 등본 발급 비유 (애니메이션 SVG)
API_ANALOGY_SVG = '''<p style="margin:0 0 12px">API는 <b>‘정해진 양식을 채워 보내면, 원하는 결과물을 정해진 형식으로 돌려주는 창구’</b>예요. 아래 <b>두 줄을 각각 클릭</b>해 보세요 — 동사무소 등본 떼기와 피코의 날씨 받기가 똑같이 ‘<b>요청 → 응답</b>’으로 흐릅니다.</p>
<svg class="api-svg" viewBox="0 0 760 500" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="클릭하면 신청서가 가고 결과물이 돌아오는 API 비유 애니메이션">
  <defs>
    <marker id="arR" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#7d93ef"/></marker>
    <marker id="arL" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#e98bb6"/></marker>
    <filter id="ds2" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#2a3568" flood-opacity="0.14"/></filter>
  </defs>
  <rect x="14" y="58" width="732" height="184" rx="14" fill="transparent" style="cursor:pointer" onclick="playLane(&#39;A&#39;)"/>
  <text x="380" y="100" text-anchor="middle" font-size="11.5" font-weight="800" fill="#3b47c2" style="pointer-events:none">👆 ‘비유’ 클릭 — 등본 신청해 보기</text>
  <g filter="url(#ds2)" style="pointer-events:none"><rect x="24" y="112" width="140" height="76" rx="16" fill="#ffffff" stroke="#e6e8f2"/></g>
  <text x="94" y="148" text-anchor="middle" font-size="27" style="pointer-events:none">🙋</text>
  <text x="94" y="174" text-anchor="middle" font-size="12" font-weight="800" fill="#2b2d3a" style="pointer-events:none">나 = 민원인</text>
  <g filter="url(#ds2)" style="pointer-events:none"><rect x="596" y="112" width="140" height="76" rx="16" fill="#eef0ff" stroke="#c3c9f5"/></g>
  <text x="666" y="146" text-anchor="middle" font-size="25" style="pointer-events:none">🏛️</text>
  <text x="666" y="168" text-anchor="middle" font-size="11.5" font-weight="800" fill="#3b47c2" style="pointer-events:none">관공서 창구</text>
  <text x="666" y="182" text-anchor="middle" font-size="9.5" fill="#8a8fb0" style="pointer-events:none">데이터 보관</text>
  <line x1="172" y1="135" x2="586" y2="135" stroke="#9fb0f5" stroke-width="2" stroke-dasharray="5 5" marker-end="url(#arR)" style="pointer-events:none"/>
  <text x="378" y="127" text-anchor="middle" font-size="10" fill="#5B6CF0" font-weight="700" style="pointer-events:none">요청(신청서) →</text>
  <line x1="586" y1="165" x2="172" y2="165" stroke="#f0b9d2" stroke-width="2" stroke-dasharray="5 5" marker-end="url(#arL)" style="pointer-events:none"/>
  <text x="378" y="183" text-anchor="middle" font-size="10" fill="#E0568A" font-weight="700" style="pointer-events:none">← 응답(결과물)</text>
  <g opacity="0" style="pointer-events:none">
    <rect x="-36" y="-23" width="72" height="46" rx="5" fill="#ffffff" stroke="#b9c0f5"/>
    <rect x="-36" y="-23" width="72" height="12" rx="5" fill="#5B6CF0"/><rect x="-36" y="-17" width="72" height="6" fill="#5B6CF0"/>
    <text x="0" y="-14" text-anchor="middle" font-size="7.5" font-weight="700" fill="#ffffff">📝 등본 신청서</text>
    <text x="0" y="1" text-anchor="middle" font-size="8" font-weight="700" fill="#3b47c2" opacity="0">이름: 홍길동<animate attributeName="opacity" begin="reqMoveA.begin" dur="2.4s" keyTimes="0;0.08;0.14;1" values="0;0;1;1"/></text>
    <text x="0" y="12" text-anchor="middle" font-size="8" font-weight="700" fill="#3b47c2" opacity="0">주소: 서울 ○○구<animate attributeName="opacity" begin="reqMoveA.begin" dur="2.4s" keyTimes="0;0.16;0.22;1" values="0;0;1;1"/></text>
    <animate attributeName="opacity" begin="reqMoveA.begin" dur="2.4s" keyTimes="0;0.05;0.30;0.85;1" values="0;1;1;1;0"/>
    <animateTransform id="reqMoveA" attributeName="transform" type="translate" begin="indefinite" dur="2.4s" calcMode="spline" keyTimes="0;0.30;1" values="200,135;200,135;556,135" keySplines="0 0 1 1;0.42 0 0.2 1"/>
  </g>
  <g opacity="0" style="pointer-events:none">
    <rect x="-36" y="-26" width="72" height="52" rx="5" fill="#ffffff" stroke="#f0c6da"/>
    <rect x="-36" y="-26" width="72" height="12" rx="5" fill="#E0568A"/><rect x="-36" y="-20" width="72" height="6" fill="#E0568A"/>
    <text x="0" y="-17" text-anchor="middle" font-size="7.5" font-weight="700" fill="#ffffff">📄 주민등록등본</text>
    <text x="0" y="-2" text-anchor="middle" font-size="8.5" font-weight="800" fill="#2b2d3a">홍길동</text>
    <text x="0" y="9" text-anchor="middle" font-size="7.5" fill="#55524c">서울 ○○구</text>
    <circle cx="0" cy="18" r="6" fill="none" stroke="#e0392f" stroke-width="1.2"/><text x="0" y="20.5" text-anchor="middle" font-size="6" font-weight="800" fill="#e0392f">印</text>
    <animate attributeName="opacity" begin="reqMoveA.end" dur="2.4s" keyTimes="0;0.05;0.15;0.85;1" values="0;1;1;1;0"/>
    <animateTransform attributeName="transform" type="translate" begin="reqMoveA.end" dur="2.4s" calcMode="spline" keyTimes="0;0.10;1" values="556,165;556,165;200,165" keySplines="0 0 1 1;0.42 0 0.2 1"/>
  </g>
  <line x1="40" y1="262" x2="720" y2="262" stroke="#eceef5" stroke-width="1"/>
  <rect x="14" y="280" width="732" height="184" rx="14" fill="transparent" style="cursor:pointer" onclick="playLane(&#39;B&#39;)"/>
  <text x="380" y="322" text-anchor="middle" font-size="11.5" font-weight="800" fill="#0e9488" style="pointer-events:none">👆 ‘피코’ 클릭 — 강수확률 받아 보기</text>
  <g filter="url(#ds2)" style="pointer-events:none"><rect x="24" y="334" width="140" height="76" rx="16" fill="#ffffff" stroke="#e6e8f2"/></g>
  <text x="94" y="370" text-anchor="middle" font-size="27" style="pointer-events:none">🔌</text>
  <text x="94" y="396" text-anchor="middle" font-size="12" font-weight="800" fill="#2b2d3a" style="pointer-events:none">피코 · 브라우저</text>
  <g filter="url(#ds2)" style="pointer-events:none"><rect x="596" y="334" width="140" height="76" rx="16" fill="#eef0ff" stroke="#c3c9f5"/></g>
  <text x="666" y="368" text-anchor="middle" font-size="25" style="pointer-events:none">☁️</text>
  <text x="666" y="390" text-anchor="middle" font-size="11.5" font-weight="800" fill="#3b47c2" style="pointer-events:none">Open-Meteo</text>
  <text x="666" y="404" text-anchor="middle" font-size="9.5" fill="#8a8fb0" style="pointer-events:none">= 관공서(API)</text>
  <line x1="172" y1="357" x2="586" y2="357" stroke="#9fb0f5" stroke-width="2" stroke-dasharray="5 5" marker-end="url(#arR)" style="pointer-events:none"/>
  <text x="378" y="349" text-anchor="middle" font-size="10" fill="#5B6CF0" font-weight="700" style="pointer-events:none">요청(신청서) →</text>
  <line x1="586" y1="387" x2="172" y2="387" stroke="#f0b9d2" stroke-width="2" stroke-dasharray="5 5" marker-end="url(#arL)" style="pointer-events:none"/>
  <text x="378" y="405" text-anchor="middle" font-size="10" fill="#E0568A" font-weight="700" style="pointer-events:none">← 응답(결과물)</text>
  <g opacity="0" style="pointer-events:none">
    <rect x="-36" y="-29" width="72" height="57" rx="5" fill="#ffffff" stroke="#b9c0f5"/>
    <rect x="-36" y="-29" width="72" height="12" rx="5" fill="#0e9488"/><rect x="-36" y="-23" width="72" height="6" fill="#0e9488"/>
    <text x="0" y="-20" text-anchor="middle" font-size="7.5" font-weight="700" fill="#ffffff">📝 요청 (URL)</text>
    <text x="0" y="-5" text-anchor="middle" font-size="8" font-weight="700" fill="#3b47c2" opacity="0">위도: 37.5<animate attributeName="opacity" begin="reqMoveB.begin" dur="2.4s" keyTimes="0;0.06;0.12;1" values="0;0;1;1"/></text>
    <text x="0" y="6" text-anchor="middle" font-size="8" font-weight="700" fill="#3b47c2" opacity="0">경도: 127<animate attributeName="opacity" begin="reqMoveB.begin" dur="2.4s" keyTimes="0;0.12;0.18;1" values="0;0;1;1"/></text>
    <text x="0" y="17" text-anchor="middle" font-size="8" font-weight="700" fill="#3b47c2" opacity="0">시간: 15시<animate attributeName="opacity" begin="reqMoveB.begin" dur="2.4s" keyTimes="0;0.18;0.24;1" values="0;0;1;1"/></text>
    <animate attributeName="opacity" begin="reqMoveB.begin" dur="2.4s" keyTimes="0;0.05;0.30;0.85;1" values="0;1;1;1;0"/>
    <animateTransform id="reqMoveB" attributeName="transform" type="translate" begin="indefinite" dur="2.4s" calcMode="spline" keyTimes="0;0.30;1" values="200,357;200,357;556,357" keySplines="0 0 1 1;0.42 0 0.2 1"/>
  </g>
  <g opacity="0" style="pointer-events:none">
    <rect x="-36" y="-26" width="72" height="52" rx="5" fill="#ffffff" stroke="#f0c6da"/>
    <rect x="-36" y="-26" width="72" height="12" rx="5" fill="#0e9488"/><rect x="-36" y="-20" width="72" height="6" fill="#0e9488"/>
    <text x="0" y="-17" text-anchor="middle" font-size="7.5" font-weight="700" fill="#ffffff">📦 응답 (JSON)</text>
    <text x="0" y="3" text-anchor="middle" font-size="16" font-weight="800" fill="#2b2d3a">☔ 60%</text>
    <text x="0" y="18" text-anchor="middle" font-size="7.5" fill="#8a8fa6">강수확률</text>
    <animate attributeName="opacity" begin="reqMoveB.end" dur="2.4s" keyTimes="0;0.05;0.15;0.85;1" values="0;1;1;1;0"/>
    <animateTransform attributeName="transform" type="translate" begin="reqMoveB.end" dur="2.4s" calcMode="spline" keyTimes="0;0.10;1" values="556,387;556,387;200,387" keySplines="0 0 1 1;0.42 0 0.2 1"/>
  </g>
  <text x="380" y="476" text-anchor="middle" font-size="11" fill="#7a7f95" style="pointer-events:none">이름·주소 = 위도·경도·시간(신청) · 주민등록등본 = 강수확률(결과) · 관공서 = API 서버 · 🔑 일부는 ‘신분증=키’ 필요</text>
</svg>
<script>function playLane(L){var m=document.getElementById("reqMove"+L);if(m){try{m.beginElement();}catch(e){}}}</script>'''

# ===================================================================
#  콘텐츠 정의
# ===================================================================
SHEETS_FLOW_SVG = '''<div class="figure"><svg class="hw-svg" viewBox="0 0 760 252" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="피코가 센서값을 구글 시트에 보내 한 줄씩 쌓이는 과정">
  <!-- 피코 + 센서 카드 -->
  <rect x="24" y="78" width="186" height="104" rx="14" fill="#eef0ff" stroke="#c9d0fb"/>
  <text x="117" y="108" text-anchor="middle" font-size="14" font-weight="800" fill="#3b47c2">🔌 피코 + 센서</text>
  <text x="117" y="130" text-anchor="middle" font-size="11" fill="#7a7f95">지금 잰 값</text>
  <rect x="73" y="138" width="88" height="34" rx="8" fill="#fff" stroke="#c9d0fb"/>
  <text x="117" y="161" text-anchor="middle" font-size="19" font-weight="800" fill="#3b47c2">42</text>

  <!-- 인터넷 화살표 -->
  <line x1="216" y1="130" x2="470" y2="130" stroke="#cbd2e6" stroke-width="2" stroke-dasharray="6 6"/>
  <text x="343" y="116" text-anchor="middle" font-size="11" fill="#8a8fa6">인터넷으로 전송</text>
  <polygon points="472,130 461,124 461,136" fill="#cbd2e6"/>

  <!-- 날아가는 값(엽서) -->
  <g>
    <rect x="196" y="114" width="48" height="32" rx="8" fill="#5B6CF0"/>
    <text x="220" y="136" text-anchor="middle" font-size="14" font-weight="800" fill="#fff">42</text>
    <animateTransform attributeName="transform" type="translate" values="0,0; 252,0; 252,0" keyTimes="0;0.45;1" dur="3s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.08;0.45;0.52;1" dur="3s" repeatCount="indefinite"/>
  </g>

  <!-- 구글 시트 카드 -->
  <rect x="486" y="36" width="250" height="186" rx="14" fill="#f0fdf4" stroke="#bbf7d0"/>
  <text x="611" y="62" text-anchor="middle" font-size="14" font-weight="800" fill="#15803d">📊 구글 시트</text>
  <rect x="506" y="76" width="210" height="26" rx="6" fill="#dcfce7"/>
  <text x="556" y="94" text-anchor="middle" font-size="11" font-weight="700" fill="#15803d">시각</text>
  <text x="666" y="94" text-anchor="middle" font-size="11" font-weight="700" fill="#15803d">값</text>
  <line x1="611" y1="76" x2="611" y2="208" stroke="#bbf7d0"/>
  <text x="556" y="122" text-anchor="middle" font-size="11" fill="#555">09:58</text><text x="666" y="122" text-anchor="middle" font-size="11" fill="#555">39</text>
  <text x="556" y="144" text-anchor="middle" font-size="11" fill="#555">09:59</text><text x="666" y="144" text-anchor="middle" font-size="11" fill="#555">45</text>
  <text x="556" y="166" text-anchor="middle" font-size="11" fill="#555">10:00</text><text x="666" y="166" text-anchor="middle" font-size="11" fill="#555">41</text>
  <!-- 새로 추가되는 줄 -->
  <g>
    <rect x="506" y="178" width="210" height="24" rx="5" fill="#bbf7d0"/>
    <text x="556" y="195" text-anchor="middle" font-size="11" font-weight="800" fill="#15803d">10:01</text>
    <text x="666" y="195" text-anchor="middle" font-size="11" font-weight="800" fill="#15803d">42</text>
    <animate attributeName="opacity" values="0;0;1;1" keyTimes="0;0.5;0.62;1" dur="3s" repeatCount="indefinite"/>
  </g>

  <text x="380" y="242" text-anchor="middle" font-size="11.5" fill="#7a7f95">보낼 때마다 시트에 <tspan font-weight="800" fill="#15803d">새 줄이 하나씩</tspan> 쌓여요</text>
</svg></div>'''

CHAPTERS = [
# ----------------------------------------------------------------- CH0
{
  "id": "ch0", "num": "00", "title": "준비하기", "accent": "#5B6CF0",
  "subtitle": "Thonny 설치부터 피코·그로브 쉴드·센서 조립, 펌웨어 설치, 첫 코드까지 — 여기만 끝내면 모든 장을 따라올 수 있어요.",
  "goals": [
    "Thonny(코드 편집기)를 설치하고 실행할 수 있다",
    "피코 2 WH에 그로브 쉴드와 센서를 바르게 연결할 수 있다",
    "MicroPython 펌웨어를 설치하고 Thonny와 피코를 연결할 수 있다",
    "보드 위 LED를 깜빡이는 첫 코드를 실행할 수 있다",
  ],
  "why": "피코는 손바닥만 한 작은 컴퓨터예요. 다만 처음 한 번은 <b>① 코드를 쓸 도구(Thonny) 설치 → ② 하드웨어 조립 → ③ 피코에 ‘운영체제’ 격인 펌웨어 설치 → ④ 도구와 피코 연결</b> 순서를 거쳐야 합니다. 이 4단계만 통과하면, 다음 장부터는 코드를 복사해 붙여넣고 ▶ 버튼만 누르면 돼요.",
  "extra": "",
  "sections": [
    {"title": "0.1 · 준비물 확인", "items": [
      {"type": "text", "html": "책상 위에 아래 물건이 모두 있는지 먼저 확인하세요."},
      {"type": "check_list", "items": [
        "Raspberry Pi <b>Pico 2 WH</b> (핀 헤더가 납땜된 버전)",
        "그로브 쉴드 <b>(Grove Shield for Pi Pico v1.0)</b>",
        "<b>WS2813 RGB LED 바</b> (10개짜리) + <b>그로브 케이블</b> 1개",
        "<b>MQ-2 가스센서</b> 모듈 — <b>그로브 모듈이 아니에요!</b> 핀이 4개 나온 <b>핀헤더형</b>",
        "<b>그로브 암(Female) 점퍼 케이블</b> 1개 — 한쪽은 그로브 커넥터, 반대쪽은 까만 <b>암 단자 4가닥</b> (MQ-2 연결용)",
        "데이터 전송이 되는 <b>Micro 5핀 USB 케이블</b> (충전 전용 케이블 ✗)",
        "Windows 또는 macOS 컴퓨터",
      ]},
      {"type": "callout", "kind": "warn", "title": "USB 케이블 주의",
       "html": "세상에는 ‘충전만 되는’ USB 케이블이 의외로 많아요. 피코가 컴퓨터에 인식되지 않으면, 가장 먼저 <b>다른 케이블</b>로 바꿔 보세요. 이게 연수 현장에서 제일 흔한 막힘 지점입니다."},
      {"type": "teacher", "kind": "say", "title": "진행 멘트 — 준비물 점검 (2분)",
       "html": "“책상 위 준비물이 다 있는지 <b>옆 사람과 서로</b> 확인해 주세요. 하나라도 없으면 지금 손 들어 주세요.” — 케이블 불량이 가장 흔하니 <b>데이터용 여분 케이블을 3~4개</b> 미리 챙겨 두면 진행이 매끄럽습니다. 그리고 <b>그로브 케이블(LED용)</b>과 <b>암 점퍼 케이블(MQ-2용)</b>을 미리 구분하게 해 주세요 — 여기서 헷갈리면 조립 단계가 밀립니다."},
    ]},
    {"title": "0.2 · Thonny 설치 (코드 편집기)", "items": [
      {"type": "text", "html": "<b>Thonny</b>는 우리가 쓴 코드를 피코에게 전달하고, 피코가 보내는 메시지를 받아 보여 주는 <b>창구</b>예요. 파이썬 입문용으로 가장 쉽고, 피코를 기본 지원합니다."},
      {"type": "linkbtn", "href": "https://thonny.org", "label": "thonny.org — Thonny 내려받기"},
      {"type": "steps", "items": [
        {"t": "thonny.org 접속", "d": "위 버튼을 눌러 공식 사이트로 갑니다."},
        {"t": "내 운영체제용 설치파일 받기", "d": "오른쪽 위에서 <b>Windows</b> 또는 <b>macOS</b>에 맞는 파일을 내려받습니다."},
        {"t": "설치 실행", "d": "받은 파일을 더블클릭해 안내대로 설치합니다. (옵션은 기본값 그대로 두면 됩니다)"},
        {"t": "Thonny 실행", "d": "설치가 끝나면 Thonny를 엽니다. 위에 코드 쓰는 칸, 아래에 <b>Shell</b>(셸) 칸이 보이면 성공이에요."},
      ]},
      {"type": "mistakes", "items": [
        {"sym": "설치 파일이 백신/보안 경고로 막힘", "cause": "다운로드 직후 일부 백신이 과민 반응합니다.", "fix": "공식 사이트(<a class=\"ilink\" href=\"https://thonny.org\" target=\"_blank\" rel=\"noopener\">thonny.org</a>)에서 받았다면 안전합니다. ‘허용’ 또는 ‘추가 정보 → 실행’을 선택하세요."},
      ]},
    ]},
    {"title": "0.3 · 하드웨어 조립", "items": [
      {"type": "text", "html": "그로브 베이스 쉴드는 피코 위에 ‘덮어 끼우는’ 확장 보드예요. 센서를 납땜 없이 케이블로 톡 꽂을 수 있게 해 줍니다. 아래 그림처럼 연결합니다."},
      {"type": "figure_hw"},
      {"type": "steps", "items": [
        {"t": "피코를 그로브 쉴드에 꽂기", "d": "핀 방향을 맞춰 피코를 쉴드에 끝까지 눌러 끼웁니다. <b>USB 단자가 쉴드 바깥쪽을 향하도록</b> 방향을 확인하세요. 한 줄이라도 핀이 어긋나면 안 됩니다."},
        {"t": "LED 바 → D16 포트", "d": "WS2813 LED 바의 그로브 케이블을 쉴드의 <b>D16</b> 포트에 꽂습니다. (코드에서는 GP16)"},
        {"t": "MQ-2 센서 → A0 포트 (암 점퍼 케이블)", "d": "MQ-2는 <b>그로브 모듈이 아니라서</b> 케이블이 달라요. <b>그로브 암 점퍼 케이블</b>의 그로브 쪽을 쉴드의 <b>A0</b> 포트에 꽂고, 반대쪽 암 단자를 센서 핀 글자를 보며 하나씩: <b>빨강 → VCC · 검정 → GND · 노랑 → AO</b>. <b>흰선과 센서의 DO 핀은 아무 데도 안 꽂고 비워 둡니다.</b> (코드에서는 GP26 / ADC0)"},
        {"t": "USB로 컴퓨터에 연결", "d": "USB 케이블로 피코와 컴퓨터를 연결합니다. (펌웨어를 처음 설치할 때는 0.4의 BOOTSEL 순서를 따르세요)"},
      ]},
      {"type": "callout", "kind": "warn", "title": "꽂는 위치를 헷갈리지 마세요",
       "html": "D16(디지털)과 A0(아날로그)는 쓰임이 다릅니다. LED는 <b>D16</b>, 가스센서는 <b>A0</b>. 반대로 꽂으면 값이 이상하거나 LED가 안 켜져요."},
      {"type": "callout", "kind": "warn", "title": "MQ-2의 AO와 DO — 노란선은 반드시 AO에",
       "html": "MQ-2 핀은 <b>VCC · GND · DO · AO</b> 네 개예요. 우리가 읽는 건 <b>AO(아날로그 출력)</b> — 노란선이 <b>DO</b>에 꽂히면 값이 0이나 65535 근처에 붙어 움직이지 않습니다. 3장에서 값이 이상하면 <b>제일 먼저 노란선이 AO에 있는지</b> 보세요. (센서 보드의 파란 네모(가변저항)는 DO 감도 조절용이라 우리 실습과는 무관해요.)"},
      {"type": "callout", "kind": "warn", "title": "쉴드 모서리의 전원 스위치는 5V에",
       "html": "그로브 쉴드에는 포트 전원을 고르는 <b>3V3 ↔ 5V 스위치</b>가 있어요. 이 교재의 부품은 <b>5V</b> 쪽에 두면 모두 잘 동작합니다. LED는 양쪽 다 되지만, ML 확장판에서 쓰는 <b>MP3 모듈은 5V가 아니면 부팅을 못 해요</b>. (아날로그 포트 A0~A2는 스위치와 상관없이 항상 3.3V라 가스센서는 어느 쪽이든 괜찮습니다.)"},
    ]},
    {"title": "0.4 · MicroPython 펌웨어 설치", "items": [
      {"type": "text", "html": "갓 산 피코에는 아직 파이썬을 실행할 ‘속살’이 없어요. <b>MicroPython 펌웨어</b>를 한 번 설치하면, 그때부터 피코가 파이썬 코드를 알아듣습니다. (처음 한 번만 하면 됩니다)"},
      {"type": "raw", "html": FW_CARD},
      {"type": "dig", "title": "펌웨어? MicroPython? BOOTSEL? — 용어 정리",
       "html": "<b>펌웨어(firmware)</b>는 어떤 기기를 켰을 때 가장 먼저 돌아가는 ‘기본 소프트웨어’예요. 컴퓨터의 운영체제(윈도우·macOS)에 해당하는, 피코의 속살이라고 보면 됩니다.<br><br><b>MicroPython</b>은 피코 같은 작은 컴퓨터(마이크로컨트롤러)에서 돌아가도록 만든 <b>파이썬</b>이에요. 이 펌웨어를 설치하면, 그때부터 피코가 우리가 쓴 파이썬 코드를 알아듣습니다. (C/C++로도 쓸 수 있지만, 파이썬이 가장 쉬워요.)<br><br><b>BOOTSEL 버튼</b>은 피코를 ‘펌웨어를 새로 받을 준비(부트로더) 모드’로 켜는 버튼이에요. 이 버튼을 누른 채 USB를 꽂으면 컴퓨터에 USB 드라이브처럼 나타나고, 거기에 <code>.uf2</code> 파일을 끌어다 놓으면 설치됩니다.<br><br><b>.uf2</b>는 이런 보드에 드래그&드롭으로 펌웨어를 넣도록 만든 파일 형식(USB Flashing Format)입니다."},
      {"type": "mistakes", "items": [
        {"sym": "RP2350 드라이브가 안 나타남", "cause": "BOOTSEL 버튼을 누르지 않고 꽂았거나, 충전 전용 케이블입니다.", "fix": "케이블을 뽑고 → <b>BOOTSEL 버튼을 누른 채</b> 다시 꽂으세요. 그래도 안 되면 데이터용 케이블로 교체합니다."},
      ]},
      {"type": "teacher", "kind": "err", "title": "예상 오류 — 펌웨어 단계에서 반드시 나오는 것",
       "html": "매 기수 2~3명은 <b>BOOTSEL을 안 누르고 꽂거나, 드라이브가 뜨기 전에 손을 뗍니다.</b> ‘버튼 먼저, 꽂는 건 나중’을 두 번 외치고 시작하세요. 이미 MicroPython이 깔린 피코는 드라이브가 안 뜨는 게 정상이니 ‘내 것만 안 떠요’ 질문에는 셸 연결(0.5)로 바로 넘어가면 됩니다."},
    ]},
    {"title": "0.5 · Thonny와 피코 연결 + 첫 코드", "items": [
      {"type": "steps", "items": [
        {"t": "인터프리터 선택", "d": "Thonny 창 <b>맨 아래 오른쪽 상태바</b>(‘Local Python 3…’이라고 적힌 곳)를 클릭 → <b>‘MicroPython (Raspberry Pi Pico)’</b>를 고릅니다. (안 보이면 메뉴 <b>실행(Run) → 인터프리터 설정</b>) 포트는 보통 자동으로 잡혀요."},
        {"t": "셸에서 인사해 보기", "d": "아래 Shell 칸에 다음을 한 줄 입력하고 Enter."},
      ]},
      {"type": "code", "label": "셸에 직접 입력", "lang": "python", "file": "snippets/ch0_hello.py"},
      {"type": "text", "html": "<code>안녕, 피코!</code>가 셸에 찍히면, 컴퓨터와 피코가 <b>대화에 성공</b>한 거예요. 🎉 이제 보드 위 작은 LED를 깜빡여 봅시다."},
      {"type": "step_head", "html": "이번엔 여러 줄 코드라, 셸이 아니라 <b>위쪽 편집기 칸</b>에 붙여넣고 실행해요."},
      {"type": "code", "label": "보드 LED 깜빡이기 (편집기에 쓰고 ▶ 실행)", "lang": "python", "file": "snippets/ch0_blink.py"},
      {"type": "callout", "kind": "key", "title": "버튼 3개만 기억하세요 — ▶ 실행 · ⏹ 정지 · 💾 저장",
       "html": "① <b>▶ 실행(Run)</b> — 편집기에 쓴 코드를 피코에서 돌립니다.<br>② <b>⏹ 정지(Stop)</b> — <code>while True</code>처럼 계속 도는 코드를 멈춰요. <b>코드를 고쳐 다시 실행할 땐 먼저 ⏹로 멈춘 뒤 ▶</b>를 누르세요(안 멈추면 ‘사용 중’이라 새로 안 돌아요).<br>③ <b>💾 저장</b> — 저장하면 ‘<b>This computer</b>(내 컴퓨터)’와 ‘<b>Raspberry Pi Pico</b>’ 중 어디에 저장할지 물어봐요. 꼭 <b>Raspberry Pi Pico</b>를 고르고 파일 이름은 <b><code>main.py</code></b>로 하세요. (그래야 전원만 넣어도 자동 실행되고, 뒤 장의 코드들이 서로(예: wifi_config.py)를 찾을 수 있어요.)"},
      {"type": "mistakes", "items": [
        {"sym": "포트/장치가 목록에 안 보임", "cause": "펌웨어 미설치, 또는 케이블 문제.", "fix": "0.4를 다시 확인하고, 케이블을 데이터용으로 바꾸세요. Thonny를 재시작하면 잡히기도 합니다."},
        {"sym": "코드를 멈출 수 없음 (무한 반복)", "cause": "<code>while True</code>는 일부러 무한 반복합니다.", "fix": "Thonny의 ⏹ 정지 버튼을 누르거나 셸에서 Ctrl+C."},
      ]},
      {"type": "check", "items": [
        {"q": "Thonny에서 셸(Shell) 칸은 무슨 역할을 하나요?", "a": "코드를 한 줄씩 바로 실행해 보고, 피코가 print로 보낸 메시지를 보여 주는 ‘대화창’입니다."},
        {"q": "펌웨어는 매번 설치해야 하나요?", "a": "아니요. 처음 한 번만 설치하면 계속 유지됩니다."},
        {"q": "보드 LED를 코드에서 어떻게 가리켰나요?", "a": "<code>Pin(\"LED\", Pin.OUT)</code> — 피코 보드에 내장된 LED를 출력 모드로 잡았습니다."},
      ]},
      {"type": "callout", "kind": "info", "title": "다음 장부터 — AI에게 시키는 ‘바이브코딩’",
       "html": "이 연수에서는 긴 코드를 손으로 다 치지 않고, <b>AI에게 우리말로 설명해 코드를 받습니다.</b> AI 도구가 처음이라면: <a class=\"ilink\" href=\"https://claude.ai\" target=\"_blank\" rel=\"noopener\"><b>claude.ai</b></a>(또는 쓰는 AI)에 접속 → 로그인 → <b>새 대화</b> → 교재의 ‘<b>AI에게 이렇게 설명하세요</b>’ 프롬프트를 복사해 붙여넣고 Enter. 받은 코드를 Thonny 편집기에 붙여넣어 <b>▶ 실행</b>하면 돼요."},
    ]},
  ],
},
# ----------------------------------------------------------------- CH1
{
  "id": "ch1", "num": "01", "title": "와이파이 사각지대 찾기", "accent": "#E0568A",
  "subtitle": "피코를 들고 교실을 돌아다니며 와이파이 신호 세기(RSSI)를 측정해, 신호가 약한 ‘사각지대’를 찾고 스마트폰으로 실시간 확인합니다. 첫 IoT 작품이에요.",
  "goals": [
    "피코를 와이파이(STA 모드)에 연결할 수 있다",
    "신호 세기(RSSI)가 무엇이고 어떻게 읽는지 안다",
    "측정하며 돌아다녀 신호가 약한 ‘사각지대’를 찾을 수 있다",
    "피코를 작은 웹서버로 만들어 브라우저에서 데이터를 본다",
    "‘피코는 /data로 값만 주고, 그래프는 브라우저가 그린다’는 구조를 이해한다",
  ],
  "why": "교실·집 어디나 와이파이가 똑같이 잘 터지진 않아요. 피코로 신호 세기(RSSI)를 재면서 돌아다니면 <b>어디가 약한지(사각지대)</b>를 찾을 수 있어요. 게다가 피코가 <b>웹서버</b>가 되면 같은 와이파이의 누구나 스마트폰으로 실시간 값을 함께 볼 수 있죠. 이 장에서 익히는 <b>‘피코=서버, 브라우저=화면’</b> 구조는 뒤의 공기질·날씨 대시보드에서도 똑같이 재사용됩니다.",
  "sections": [
    {"title": "핵심 개념", "items": [
      {"type": "concept", "items": [
        {"t": "STA 모드", "d": "피코가 집/학교 와이파이에 <b>접속하는</b> 모드. <code>network.WLAN(network.STA_IF)</code>"},
        {"t": "RSSI", "d": "신호 세기. 단위는 dBm이고 <b>음수</b>예요. -50처럼 0에 가까울수록 강하고, -80처럼 작을수록 약합니다."},
        {"t": "소켓 웹서버", "d": "포트 80에서 브라우저의 접속을 기다리다가, 요청이 오면 HTML이나 데이터를 돌려주는 작은 서버."},
        {"t": "/data 폴링", "d": "브라우저가 1초마다 <code>/data</code>를 불러 최신 값을 받고, Chart.js로 그래프를 갱신하는 방식."},
      ]},
      {"type": "dig", "title": "RSSI는 왜 -50, -80처럼 ‘음수’일까? (dBm과 데시벨)",
       "html": "RSSI(Received Signal Strength Indicator)의 단위 <b>dBm</b>은 ‘1밀리와트(mW)에 견준 신호 세기를 데시벨로 나타낸 값’이에요. 정의상 <b>0 dBm = 1 mW</b>입니다.<br><br>와이파이 신호가 안테나에 도달할 때의 전력은 1 mW보다 <b>훨씬 작아서</b>(보통 1mW의 수만분의 1 ~ 1억분의 1 수준), 로그(데시벨)로 바꾸면 <b>음수</b>가 됩니다. 그래서 값이 항상 마이너스예요.<br>· -30 dBm ≈ 아주 강함(공유기 바로 옆)<br>· -67 dBm ≈ 영상통화도 무난<br>· -80 dBm ≈ 약함, 끊길 수 있음<br><br>데시벨은 <b>로그 스케일</b>이라, 10 dB 차이가 전력 <b>10배</b> 차이예요. 즉 -60에서 -70으로 떨어지면 신호 전력이 1/10로 준 겁니다. 숫자 차이는 작아 보여도 체감 차이가 큰 이유죠."},
      {"type": "teacher", "kind": "ask", "title": "발문 — 개념을 몸으로 먼저",
       "html": "“신호 세기가 <b>-50</b>인 자리와 <b>-80</b>인 자리, 어디가 더 잘 터질까요? 왜 0이 아니라 음수로 잴까요?” — 답을 주지 말고 스캔(Step 1) 결과를 보며 스스로 확인하게 하세요. ‘공유기에서 멀어지면 어떻게 될까?’로 사각지대 활동을 예고하면 동기부여가 됩니다."},
      {"type": "teacher", "kind": "say", "title": "진행 팁 — 네트워크는 강사 핫스팟이 제일 안전",
       "html": "학교망은 기기 간 통신(피코↔폰)이 막힌 경우가 많습니다. <b>강사 휴대폰 핫스팟(2.4GHz)</b>을 하나 열어 두고, 막히는 학생은 그리로 옮기게 하세요. SSID·비밀번호를 칠판에 크게 적어 두면 wifi_config.py 오타 질문이 크게 줄어듭니다."},
    ]},
    {"title": "따라하기", "items": [
      {"type": "step_head", "html": "<b>Step 1.</b> 주변에 어떤 와이파이가 있는지 스캔해 봅니다. (셸에서 실행)"},
      {"type": "code", "label": "Step 1 · 와이파이 스캔", "lang": "python", "file": "snippets/ch1_scan.py"},
      {"type": "step_head", "html": "<b>Step 2.</b> 와이파이 이름·비밀번호를 <b>wifi_config.py</b> 파일에 따로 저장해요. Thonny <b>파일 → 새 파일</b> → 아래 두 줄 입력 → <b>💾 저장 → ‘Raspberry Pi Pico’</b> 선택 → 파일 이름을 정확히 <b><code>wifi_config.py</code></b>로. (와이파이를 쓰는 코드는 모두 이 파일을 함께 씁니다.)"},
      {"type": "code", "label": "Step 2 · wifi_config.py (따로 저장)", "lang": "python", "file": "snippets/wifi_config.py"},
      {"type": "callout", "kind": "warn", "title": "두 줄 적을 때 주의",
       "html": "<b>따옴표 <code>\"</code> 는 그대로 두고 그 안의 글자만</b> 내 와이파이 이름·비밀번호로 바꾸세요(대소문자 정확히). 피코는 <b>2.4GHz</b> 와이파이만 됩니다 — 이름이 <code>…5G</code>로 끝나면 안 돼요."},
      {"type": "step_head", "html": "<b>Step 3.</b> 와이파이에 연결해 신호 세기를 1초마다 출력합니다. <b>편집기 칸에 붙여넣고 ▶ 실행</b>해 원리를 확인하세요. (셸에 RSSI 값이 1초마다 찍혀요.)"},
      {"type": "code", "label": "Step 3 · RSSI 읽기", "lang": "python", "file": "snippets/ch1_rssi.py"},
      {"type": "step_head", "html": "<b>Step 4.</b> 이제 이 값을 웹으로 봅니다. 이런 긴 코드는 손으로 치지 않아요 — AI에게 아래처럼 <b>상황과 목표를 설명</b>하면 대시보드 코드를 만들어 줍니다."},
      {"type": "prompt", "label": "① AI에게 이렇게 설명하세요 (그대로 복사)", "text":
"라즈베리파이 피코 2 W에서 돌아가는 마이크로파이썬(MicroPython) 코드를 만들어줘. 와이파이 신호 세기 실시간 대시보드야.\n- 지금 내 피코는 와이파이에 접속해 신호 세기(RSSI)를 1초마다 읽고 있어. 신호 세기는 dBm 단위의 음수이고, 0에 가까울수록 강해.\n- 와이파이 이름과 비밀번호는 따로 만들어 둔 설정 파일(wifi_config.py)에서 불러와.\n- 피코가 외부 라이브러리 설치 없이 작은 웹서버(80번 포트)가 되게 해줘.\n- 브라우저가 '/data' 주소에서 최신 신호 세기를 JSON으로 받아 1초마다 자동 갱신하고, Chart.js로 실시간 꺾은선 그래프를 그려줘.\n- 같은 와이파이에 있는 스마트폰에서 접속할 수 있게 하고, 복사해서 바로 돌아가는 완결형 main.py 전체를 한 번에 줘."},
      {"type": "step_head", "html": "직접 만들지 않아도, 아래 <b>완성본</b>을 복사해 main.py로 저장하면 바로 돕니다. 실행 후 셸에 찍힌 <code>http://...</code> 주소를 같은 와이파이의 스마트폰에서 열어 보세요."},
      {"type": "code", "label": "② 전체 코드 · RSSI 실시간 대시보드 (main.py)", "lang": "python", "file": "snippets/ch1_dashboard.py", "fold": True},
      {"type": "step_head", "html": "<b>Step 5.</b> 여기서 <b>바이브코딩으로 마무리</b>해 봐요. 숫자만 보여 주는 대신, 신호 세기에 따라 <b>재미있게 반응</b>하도록 AI에게 <b>이어서</b> 설명합니다. ①→② 흐름에 이어 붙이는 <b>③ 개선 프롬프트</b>예요."},
      {"type": "improve", "label": "③ 프롬프트 개선 — 신호 세기에 반응하는 화면 (이어서 복사)", "text":
"방금 만든 신호 세기 대시보드를 이어서 개선해줘. 신호 세기에 따라 화면이 재미있게 반응하면 좋겠어.\n- 강할 때(약 -60dBm 이상): 초록색 배경에 '신호 최고예요! 😄' 같은 축하 문구를 살짝 반짝이게.\n- 보통(-60 ~ -78dBm): 노란색에 '쓸 만해요'.\n- 약할 때(약 -78dBm 이하): 빨간색으로 '⚠️ 신호 약함, 끊길 수 있어요' 경고를 크게 띄우고 화면이 살짝 흔들리게.\n- 피코의 16번 핀에 열 칸짜리 LED 바(WS2813)가 연결돼 있다면 같은 상태를 LED 색으로도 보여줘. 강함=초록, 보통=노랑, 약함=빨강 깜빡임.\n- 이 LED는 만들 때 타이밍 값 네 개(280, 515, 515, 745)를 꼭 지정해야 색이 안 깨져. 이 값과 핀 번호는 그대로 유지해줘.\n- 복사해서 바로 돌아가는 완결형 main.py 전체를 한 번에 줘."},
      {"type": "callout", "kind": "tip", "title": "바이브코딩 팁",
       "html": "받은 코드를 올리기 전에 ① 신호 기준값(-60·-78 등)이 우리 환경에 맞는지 ② LED를 함께 쓴다면 <code>timing</code> 인자가 들어 있는지 확인하세요. (LED와 <code>timing</code>은 <b>2장</b>에서 자세히 배워요 — 지금은 화면만으로도 충분합니다.) 기준값은 직접 돌아다니며 ‘강한 곳/약한 곳’ RSSI를 보고 조정하면 더 정확해요."},
      {"type": "callout", "kind": "info", "title": "들고 다니려면 — 전원 준비",
       "html": "사각지대를 찾으려면 피코를 들고 돌아다녀야 해요. 노트북에 USB로 연결한 채 움직이거나, <b>보조배터리(파워뱅크)</b>에 USB로 연결하면 선 없이 교실 곳곳의 신호를 잴 수 있어요. 측정 위치를 바꿀 때마다 몇 초 기다렸다가 값을 읽으세요."},
    ]},
    {"title": "자주 하는 실수", "items": [
      {"type": "mistakes", "items": [
        {"sym": "계속 연결 중... 에서 멈춤", "cause": "5GHz 와이파이이거나 비밀번호 오타.", "fix": "피코는 <b>2.4GHz</b> 와이파이만 됩니다. 5GHz 전용이면 안 돼요. SSID/비번 대소문자도 정확히 확인하세요."},
        {"sym": "브라우저에서 주소가 안 열림", "cause": "스마트폰이 피코와 <b>다른 와이파이</b>에 있음.", "fix": "스마트폰을 피코와 <b>같은 와이파이</b>에 연결하세요. 학교망은 기기 간 통신이 막힌 경우도 있어, 휴대폰 핫스팟이 가장 확실합니다."},
        {"sym": "RSSI가 0 또는 이상한 값", "cause": "연결 전에 status를 읽음.", "fix": "<code>wlan.isconnected()</code>가 참이 된 뒤에 읽어야 합니다. (위 코드는 이미 연결 후 읽습니다)"},
      ]},
    ]},
    {"title": "스스로 점검하기", "items": [
      {"type": "check", "items": [
        {"q": "RSSI가 -50과 -80 중 어느 쪽이 더 좋은 신호인가요?", "a": "-50입니다. 0에 가까울수록 강한 신호예요."},
        {"q": "그래프는 피코가 그리나요, 브라우저가 그리나요?", "a": "브라우저가 그립니다. 피코는 <code>/data</code>로 숫자만 보내고, Chart.js가 화면에 그려요. 그래서 피코의 부담이 적습니다."},
        {"q": "wifi_config.py를 따로 두는 이유는?", "a": "비밀번호를 코드 본문과 분리해 관리하기 쉽고, 여러 코드가 같은 설정을 재사용할 수 있어서요."},
      ]},
    ]},
  ],
},
# ----------------------------------------------------------------- CH2
{
  "id": "ch2", "num": "02", "title": "LED로 내 감정 표현하기", "accent": "#1F9D63",
  "subtitle": "WS2813 LED 바(10개)를 색과 움직임으로 자유자재로 다뤄, 마지막엔 내 기분을 표현하는 ‘감정 무드등’을 만듭니다.",
  "goals": [
    "NeoPixel로 LED 한 칸·전체를 원하는 색으로 켤 수 있다",
    "WS2813에 꼭 필요한 timing 인자를 이해한다",
    "10칸에 무지개·게이지를 표현할 수 있다",
    "색과 움직임을 조합해 내 감정을 LED로 표현할 수 있다",
  ],
  "why": "LED는 ‘숫자·상태를 빛으로 바꾸는’ 가장 직관적인 출력 장치예요. 색과 움직임만으로도 기쁨·평온·화남 같은 <b>감정을 표현</b>할 수 있죠. 이 장에서 10칸을 다루는 법을 익히면, 뒤의 공기질·날씨 장에서 데이터를 색으로 보여 주는 데에도 똑같이 씁니다.",
  "sections": [
    {"title": "핵심 개념 — timing이 진짜 중요해요", "items": [
      {"type": "callout", "kind": "key", "title": "WS2813은 timing 인자가 필수",
       "html": "우리가 쓰는 LED는 <b>WS2813</b> 계열이라, MicroPython NeoPixel의 <b>기본 타이밍과 안 맞습니다.</b> 그대로 두면 색이 깨지거나 엉뚱한 칸이 켜져요. 그래서 반드시 이렇게 만듭니다:<br><br><code>TIMING = (280, 515, 515, 745)</code><br><code>np = NeoPixel(Pin(16), 10, timing=TIMING)</code><br><br>이 네 숫자는 0/1 신호의 길이(나노초)예요. 이번 연수의 모든 LED 코드 첫 줄에 들어갑니다."},
      {"type": "callout", "kind": "info", "title": "LED가 60개짜리로 왔다면?",
       "html": "바꿀 곳은 <b>딱 한 줄</b>이에요. 코드 위쪽의 <code>NUM = 10</code>을 <code>NUM = 60</code>으로 바꾸면 끝입니다. (timing·핀은 그대로) <code>fill</code>·무지개·게이지·감정 무드등 모두 <code>NUM</code>을 기준으로 돌아서 자동으로 60칸에 맞춰집니다. 단, 60칸을 밝게 켜면 전류를 많이 먹으니 밝기는 더 낮춰 주세요."},
      {"type": "concept", "items": [
        {"t": "NeoPixel", "d": "여러 개의 색 LED를 한 줄로 제어하는 도구. <code>np[i] = (r, g, b)</code>로 i번 칸 색을 정합니다."},
        {"t": "write()", "d": "색을 정한 뒤 <code>np.write()</code>를 호출해야 실제 LED에 반영됩니다. 깜빡 잊기 쉬워요."},
        {"t": "칸 번호 0~9", "d": "10개니까 <code>np[0]</code>부터 <code>np[9]</code>까지. 0부터 시작!"},
        {"t": "밝기는 낮게", "d": "(255,255,255)는 너무 밝고 전류도 많이 써요. (30,30,30) 정도면 충분히 보입니다."},
      ]},
      {"type": "dig", "title": "timing=(280, 515, 515, 745)의 정체 (1선 통신과 GRB)",
       "html": "WS2813 같은 LED는 칸이 10개여도 <b>데이터 선이 하나</b>뿐이에요. 그래서 0과 1을 <b>‘펄스(전기 신호)의 길이’</b>로 구분합니다. 이게 <b>1-wire(원-와이어) 프로토콜</b>이에요.<br><br>네 숫자는 <b>나노초(ns, 10억분의 1초)</b> 단위의 시간이고, 각각:<br>· <b>T0H</b>=280 — ‘0’을 보낼 때 켜 두는 시간<br>· <b>T0L</b>=515 — ‘0’을 보낼 때 꺼 두는 시간<br>· <b>T1H</b>=515 — ‘1’을 보낼 때 켜 두는 시간<br>· <b>T1L</b>=745 — ‘1’을 보낼 때 꺼 두는 시간<br><br>이 길이가 칩이 기대하는 값과 안 맞으면 0을 1로, 1을 0으로 잘못 읽어 <b>색이 깨집니다.</b> 칩 종류마다 기대 시간이 조금씩 달라, WS2813엔 이 네 값을 직접 지정해 주는 거예요.<br><br>또 하나, 사람은 색을 (빨강, 초록, 파랑) = RGB 순서로 생각하지만 이 LED는 내부적으로 <b>GRB(초록·빨강·파랑) 순서</b>로 데이터를 받습니다. 대부분의 펌웨어에서는 <code>(r, g, b)</code>로 쓰면 되지만, 혹시 빨강·초록이 바뀌어 보이면 순서를 조정하면 돼요."},
      {"type": "teacher", "kind": "err", "title": "예상 오류 — timing 누락이 이 장의 1순위",
       "html": "AI가 준 코드에 <b>timing 인자가 빠진 채</b> 오는 경우가 가장 많습니다. 색이 깨지거나 엉뚱한 칸이 켜지면 코드를 읽기 전에 먼저 <b>Ctrl+F로 ‘timing’을 검색</b>하게 하세요. 없으면 AI에게 “타이밍 값 네 개(280, 515, 515, 745)를 넣어줘”라고 다시 요청하면 됩니다. 이 ‘검색 → 재요청’ 한 동작을 이 장에서 전체가 몸에 익히면 4·5장의 LED 질문이 절반으로 줍니다."},
    ]},
    {"title": "따라하기", "items": [
      {"type": "step_head", "html": "<b>Step 1.</b> 한 칸만 켜 보기."},
      {"type": "code", "label": "Step 1 · 한 칸 켜기", "lang": "python", "file": "snippets/ch2_basic.py"},
      {"type": "step_head", "html": "<b>Step 2.</b> 전체를 한 색으로 — 반복문으로 모든 칸을 칠하는 <code>fill</code> 함수."},
      {"type": "code", "label": "Step 2 · 전체 한 색 (fill)", "lang": "python", "file": "snippets/ch2_fill.py"},
      {"type": "step_head", "html": "<b>Step 3.</b> 10칸에 무지개 펼치기 (HSV로 색상환 한 바퀴)."},
      {"type": "code", "label": "Step 3 · 무지개 10칸", "lang": "python", "file": "snippets/ch2_rainbow.py"},
      {"type": "step_head", "html": "<b>Step 4.</b> 켜진 칸 수로 양을 나타내는 <b>게이지</b> — 뒤 장(공기질·날씨)의 핵심 기법이에요."},
      {"type": "code", "label": "예제 · 게이지 차오르기", "lang": "python", "file": "snippets/ch2_gauge.py"},
    ]},
    {"title": "내 감정 표현하기 (이 장의 작품)", "items": [
      {"type": "text", "html": "이제 배운 걸 모아 <b>감정 무드등</b>을 만들어요. 색은 ‘무슨 감정인지’, 움직임(숨쉬기·깜빡임·반짝임)은 ‘감정의 느낌·세기’를 나타냅니다. 이런 코드는 손으로 치지 말고, AI에게 아래처럼 <b>설명</b>해 만들면 돼요."},
      {"type": "teacher", "kind": "ask", "title": "발문 — 색만으로 감정이 전달될까",
       "html": "“빨간불 하나만 보고 이 사람이 <b>화난 건지, 신난 건지</b> 알 수 있을까요? 움직임(느린 숨쉬기 vs 빠른 깜빡임)이 더해지면 뭐가 달라질까요?” — 답을 주지 말고, ‘같은 색·다른 움직임’ 두 가지를 직접 켜서 비교하게 하세요. 색=감정의 종류, 움직임=감정의 세기라는 이 장의 설계 원리를 학생이 스스로 발견하게 됩니다."},
      {"type": "prompt", "label": "① AI에게 이렇게 설명하세요 (그대로 복사)", "text":
"라즈베리파이 피코에서 돌아가는 마이크로파이썬(MicroPython) 코드를 만들어줘. 열 칸짜리 LED 바로 내 기분을 표현하는 '감정 무드등'이야.\n- LED 바(WS2813)는 16번 핀에 연결했어. LED를 만들 때 타이밍 값 네 개(280, 515, 515, 745)를 꼭 지정해줘. 없으면 색이 깨져.\n- 밝기는 눈이 부시지 않게 낮게(최대 60 정도).\n- 색과 움직임을 조합해 기쁨·평온·화남·신남 네 가지 감정을 표현해줘. 예: 기쁨=따뜻한 노랑이 두근두근 숨쉬기, 평온=파랑이 천천히 숨쉬기, 화남=빨강 깜빡임, 신남=청록이 아무 칸에나 반짝.\n- 버튼은 없으니 코드 맨 아래 변수 하나만 바꾸면 감정을 고를 수 있게 해줘.\n- 복사해서 바로 돌아가는 완결형 main.py 전체를 한 번에 줘."},
      {"type": "step_head", "html": "아래는 <b>완성본</b>이에요. 버튼이 없으니 코드 맨 아래 <code>MOOD</code> 한 줄만 바꿔 기분을 골라요."},
      {"type": "code", "label": "② 전체 코드 · 감정 무드등 (main.py)", "lang": "python", "file": "snippets/ch2_emotion.py", "fold": True},
      {"type": "step_head", "html": "나만의 감정을 추가해 봐요. 색(<code>(r,g,b)</code>)과 움직임(<code>pulse</code>/<code>blink</code>/<code>sparkle</code>)을 골라 함수 하나만 더 만들면 됩니다. 처음부터 다시 설명할 필요 없이, 같은 대화에서 <b>③ 개선 프롬프트</b>로 이어 가면 돼요."},
      {"type": "improve", "label": "③ 프롬프트 개선 — 감정 추가 (이어서 복사)", "text":
"방금 만든 감정 무드등을 이어서 개선해줘.\n- '슬픔'과 '설렘' 두 감정을 추가해줘. 슬픔은 파란색이 천천히 한 칸씩 흘러내리는 느낌, 설렘은 분홍색이 점점 빨라지며 반짝이는 느낌으로.\n- 밝기는 지금처럼 낮게 유지하고, LED 타이밍 값과 핀 번호도 그대로 둬.\n- 복사해서 바로 돌아가는 완결형 main.py 전체를 한 번에 줘."},
      {"type": "teacher", "kind": "say", "title": "진행 멘트 — 감정 맞히기 미니 갤러리 (5분)",
       "html": "“완성한 사람은 무드등을 켜 둔 채 자리를 옮겨, <b>옆 사람 무드등이 무슨 감정인지</b> 맞혀 보세요. 만든 사람은 정답을 바로 말하지 말고요.” — 5분이면 충분하고, 못 맞힌 작품이 오히려 좋은 토론거리입니다. “어떻게 바꾸면 전달될까?”를 이어 물으면 자연스럽게 ③ 개선 프롬프트로 넘어갑니다."},
    ]},
    {"title": "자주 하는 실수", "items": [
      {"type": "mistakes", "items": [
        {"sym": "색이 깨지거나 엉뚱한 칸이 켜짐", "cause": "<b>timing 인자 누락.</b>", "fix": "<code>NeoPixel(Pin(16), 10, timing=(280,515,515,745))</code> 처럼 timing을 꼭 넣으세요. 이번 연수 LED 문제의 1순위 원인입니다."},
        {"sym": "색을 정했는데 안 켜짐", "cause": "<code>np.write()</code>를 빠뜨림.", "fix": "색을 바꾼 뒤에는 항상 <code>np.write()</code>를 호출하세요."},
        {"sym": "10번째 칸에서 에러", "cause": "<code>np[10]</code>을 씀 (칸은 0~9).", "fix": "10개의 인덱스는 0부터 9까지입니다. 마지막 칸은 <code>np[9]</code>."},
        {"sym": "눈이 부시고 피코가 뜨거움", "cause": "밝기를 너무 높게 줌.", "fix": "(255,…) 대신 (30,…) 수준으로 낮추세요. 10칸을 풀 밝기로 켜면 전류도 많이 먹습니다."},
      ]},
    ]},
    {"title": "스스로 점검하기", "items": [
      {"type": "check", "items": [
        {"q": "WS2813 LED를 만들 때 꼭 넣어야 하는 인자는?", "a": "<code>timing=(280, 515, 515, 745)</code>. 없으면 색이 깨집니다."},
        {"q": "색을 바꾼 뒤 화면(LED)에 반영하려면?", "a": "<code>np.write()</code>를 호출합니다."},
        {"q": "10칸 중 다섯 칸만 켜서 ‘50%’를 표현하려면?", "a": "0~4번 칸을 색으로, 5~9번 칸을 (0,0,0)으로 두고 write. (게이지 방식)"},
      ]},
    ]},
  ],
},
# ----------------------------------------------------------------- CH3 (MQ-2 웹 대시보드)
{
  "id": "ch3", "num": "03", "title": "우리반 공기질 대시보드 (웹)", "accent": "#F59E0B",
  "subtitle": "MQ-2 센서로 우리반 공기 중 가스를 숫자로 읽고, 안전/주의/위험을 색과 그래프로 보여 주는 웹 대시보드(다크 테마)를 만듭니다.",
  "goals": [
    "ADC로 가스센서 값을 읽고 전압·비율로 바꿀 수 있다",
    "이동 평균으로 값을 안정시킬 수 있다",
    "임계값으로 안전/주의/위험 상태를 판단해 웹으로 보여 준다",
  ],
  "why": "공기질은 눈에 안 보이죠. MQ-2 센서로 측정해 <b>숫자 → 색 → 그래프</b>로 바꾸면, 환기 타이밍을 한눈에 알 수 있어요. 센서값을 ‘판단(임계값)’하고 피코가 웹서버가 되어 스마트폰·PC로 보여 줍니다. <b>다음 장에선 폰을 켜지 않고 LED만으로</b> 같은 공기질을 확인해 볼 거예요.",
  "sections": [
    {"title": "핵심 개념", "items": [
      {"type": "concept", "items": [
        {"t": "ADC (아날로그)", "d": "가스 농도 같은 ‘연속된 값’을 숫자로 바꿔 읽는 기능. 그로브 <b>A0 = GP26</b>. <code>ADC(Pin(26))</code>"},
        {"t": "read_u16()", "d": "0~65535 사이 값으로 읽습니다. 가스가 짙을수록 값이 커져요."},
        {"t": "이동 평균", "d": "여러 번 읽어 평균 내면 값이 출렁이지 않고 안정됩니다. <code>read_average()</code>"},
        {"t": "임계값", "d": "SAFE / WARNING / DANGER를 나누는 기준 숫자. 환경마다 달라 보정이 필요해요."},
      ]},
      {"type": "dig", "title": "ADC가 ‘전압’을 ‘숫자’로 바꾸는 원리 (볼트 변환)",
       "html": "센서는 가스 농도를 <b>전압(아날로그)</b>으로 내보냅니다. 0V~3.3V 사이의 ‘연속된’ 값이죠. 그런데 컴퓨터는 숫자만 다루니, 이 전압을 숫자로 바꿔야 합니다. 그 변환기가 <b>ADC(Analog-to-Digital Converter, 아날로그→디지털 변환기)</b>예요.<br><br>피코의 ADC는 실제로는 <b>12비트(4096단계)</b>로 재고, MicroPython의 <code>read_u16()</code>이 그 값을 <b>0 ~ 65535</b>(16비트 범위)로 늘려서 돌려줘요.<br>· 0V → 0<br>· 3.3V(최대) → 65535<br>· 그 사이는 비례. 따라서 숫자를 전압으로 되돌리면:<br><code>전압(V) = read_u16() / 65535 × 3.3</code><br><br>예) 읽은 값이 32768이면 → 32768/65535×3.3 ≈ <b>1.65V</b> (딱 절반).<br><br><b>주의:</b> MQ-2에서 ‘전압이 곧 가스 농도(ppm)’는 아닙니다. 정확한 ppm은 보정·계산이 필요해서, 수업에서는 <b>상대적인 변화(평소보다 높다/낮다)</b>를 보는 지표로 씁니다. 그래서 SAFE/WARNING/DANGER 임계값도 우리 교실에서 직접 보고 정합니다."},
      {"type": "teacher", "kind": "theory", "title": "이론 심화 — MQ-2 값이 ppm이 아닌 이유",
       "html": "MQ-2는 내부 저항이 가스 농도에 따라 변하는 <b>반도체식 센서</b>라, 출력 전압이 온도·습도·예열 상태·개체 차이에 함께 흔들립니다. 정확한 ppm을 얻으려면 기준 가스로 개체별 보정 곡선을 만들어야 해서 수업에서는 사실상 불가능하죠. 그래서 이 교재는 처음부터 <b>‘평소보다 높다/낮다’는 상대 지표</b>로만 씁니다. “이 값이 몇 ppm이에요?” 질문이 나오면 “그 질문이 정확히 핵심”이라고 받아 주고, 절대값이 아니라 <b>변화를 읽는 도구</b>라고 정리해 주세요. 덤 하나 — 이 쉴드의 아날로그 포트는 전원 스위치와 무관하게 <b>항상 3.3V</b>라, MQ-2가 공식 스펙(5V)보다 약하게 구동돼 절대값이 더 낮게 나옵니다. 상대 지표를 쓰는 이유가 하나 더 있는 셈이에요."},
      {"type": "callout", "kind": "info", "title": "센서는 예열이 필요해요",
       "html": "MQ-2는 전원을 넣고 <b>1~2분</b> 지나야 값이 안정됩니다. 처음 켜자마자 값이 크게 나와도 예열 전이라 그런 것이니 정상이에요."},
      {"type": "callout", "kind": "info", "title": "먼저 — 와이파이 정보 파일 만들기 (wifi_config.py)",
       "html": "대시보드 코드는 와이파이 정보를 <code>wifi_config.py</code>에서 불러옵니다. <b>main.py와 같은 위치</b>에 이 파일을 새로 만들고 두 줄만 적어 저장하세요.<br><br><code>WIFI_SSID = \"우리_와이파이_이름\"</code><br><code>WIFI_PASSWORD = \"비밀번호\"</code><br><br>(피코는 <b>2.4GHz</b> 와이파이만 됩니다.)"},
    ]},
    {"title": "따라하기", "items": [
      {"type": "step_head", "html": "<b>Step 1.</b> 값 한 번 읽기. (그로브 <b>A0</b> 포트 + 센서 쪽 <b>노란선이 AO</b>에 꽂혔는지 확인!)"},
      {"type": "code", "label": "Step 1 · 한 번 읽기", "lang": "python", "file": "snippets/ch3_01_read.py"},
      {"type": "step_head", "html": "<b>Step 2.</b> 반복해서 읽고, Thonny <b>플로터</b>로 그래프 보기. (셸 옆 ‘Plotter’ 켜기)"},
      {"type": "code", "label": "Step 2 · 반복 읽기 (플로터)", "lang": "python", "file": "snippets/ch3_02_loop.py"},
      {"type": "step_head", "html": "<b>Step 3.</b> 원시값을 전압·비율로 바꿔 의미를 부여합니다."},
      {"type": "code", "label": "Step 3 · 전압·비율 변환", "lang": "python", "file": "snippets/ch3_03_convert.py"},
      {"type": "step_head", "html": "<b>Step 4.</b> 이제 완성형 대시보드를 만들어요. 이런 긴 코드는 손으로 치지 않아요 — AI에게 아래처럼 <b>상황과 목표를 설명</b>하면 만들어 줍니다."},
      {"type": "prompt", "label": "① AI에게 이렇게 설명하세요 (그대로 복사)", "text":
"라즈베리파이 피코 2 W에서 돌아가는 마이크로파이썬(MicroPython) 코드를 만들어줘. 우리 반 공기질 실시간 대시보드야.\n- 가스센서(MQ-2)는 아날로그 입력인 26번 핀(그로브 A0 포트)에 연결했어. 읽으면 0~65535 사이 숫자가 나오고, 가스가 짙을수록 값이 커져.\n- 값이 출렁이지 않게 여러 번 읽어 평균(이동 평균)으로 안정시켜줘.\n- 와이파이 정보는 설정 파일(wifi_config.py)에서 불러와.\n- 피코가 외부 라이브러리 설치 없이 작은 웹서버(80번 포트)가 되게 하고, 브라우저가 '/data' 주소에서 JSON으로 최신 값을 받아 자동 갱신하며, Chart.js로 실시간 그래프를 그려줘.\n- 기준값(임계값)으로 안전/주의/위험 세 단계를 나눠 색으로 표시해줘. 기준값은 코드 위쪽에서 쉽게 바꿀 수 있게. 화면은 다크 테마로.\n- 같은 와이파이의 스마트폰에서 접속할 수 있게 하고, 복사해서 바로 돌아가는 완결형 main.py 전체를 한 번에 줘."},
      {"type": "step_head", "html": "직접 만들지 않아도, 아래 <b>완성본</b>을 복사해 main.py로 저장하면 이동 평균·임계값·다크 테마 그래프가 모두 들어간 모니터가 됩니다. (wifi_config.py 필요)"},
      {"type": "code", "label": "② 전체 코드 · MQ-2 실시간 대시보드 (main.py)", "lang": "python", "file": "snippets/ch3_dashboard.py", "fold": True},
      {"type": "teacher", "kind": "err", "title": "예상 오류 — 실행 직후 5분에 몰리는 두 가지",
       "html": "① 켜자마자 화면이 <b>‘위험’(빨강)</b>이라 놀라는 학생 — 예열 전이라 정상입니다. “켜고 <b>1~2분</b>은 그냥 두세요. 빨강이어도 고장이 아닙니다”를 실행 <b>전에</b> 먼저 말해 두면 질문이 안 나옵니다. ② <b>‘Wi-Fi 연결 실패’</b> — 열에 아홉은 <code>wifi_config.py</code>의 대소문자·따옴표 오타이거나 5GHz 망입니다. 칠판의 SSID·비밀번호와 <b>글자 단위로</b> 대조하게 하세요."},
      {"type": "step_head", "html": "돌아가는 걸 확인했다면, 같은 대화에서 <b>③ 개선 프롬프트</b>로 우리 반에 꼭 맞게 업그레이드해 봐요."},
      {"type": "improve", "label": "③ 프롬프트 개선 — 환기 알리미로 업그레이드 (이어서 복사)", "text":
"방금 만든 공기질 대시보드를 이어서 개선해줘.\n- '주의' 이상 상태가 3번 연속 측정되면 화면 맨 위에 '🌬️ 환기하세요!' 배너를 크게 띄우고, '안전'으로 돌아오면 배너를 내려줘.\n- 그래프 옆에 최근 10분의 최고값과 평균값도 함께 보여줘.\n- 센서 핀 번호, 기준값 변수, '/data' 응답 구조는 그대로 유지해줘.\n- 복사해서 바로 돌아가는 완결형 main.py 전체를 한 번에 줘."},
      {"type": "callout", "kind": "key", "title": "대시보드 열기 · 임계값 바꾸기",
       "html": "실행하면 Thonny <b>셸에 <code>http://...</code> 주소</b>가 찍혀요. 그 주소를 <b>같은 와이파이의 폰/PC 브라우저</b>에 입력하면 화면이 열립니다(<code>http://</code>로, https 아님).<br>안전·주의 기준을 바꾸려면 코드 <b>맨 위 <code>SAFE_MAX</code>·<code>WARN_MAX</code></b> 두 숫자만 고치세요 — 웹 화면 색도 함께 바뀝니다. (다음 장 LED도 <b>같은 숫자</b>를 씁니다.)"},
      {"type": "teacher", "kind": "ask", "title": "발문 — 임계값은 누가 정할까",
       "html": "“<code>SAFE_MAX</code>를 얼마로 두면 좋을까요? 그 숫자는 <b>누가, 무엇을 근거로</b> 정하죠?” — 정답을 주지 말고, 평소 값을 10분쯤 지켜본 뒤 알코올 솜을 가까이 대 보게 하세요. ‘우리 교실의 평소 값’과 ‘자극이 있을 때 값’ 사이 어딘가를 모둠마다 스스로 정하게 하는 게 이 장의 진짜 목표입니다. 기준은 주어지는 게 아니라 <b>데이터를 보고 정하는</b> 것이니까요. 모둠끼리 숫자가 달라도 틀린 게 아닙니다."},
    ]},
    {"title": "자주 하는 실수", "items": [
      {"type": "mistakes", "items": [
        {"sym": "값이 늘 0이거나 65535에 붙어 있음", "cause": "센서를 A0가 아닌 다른 포트에 꽂았거나, 노란선이 센서의 <b>DO</b>에 꽂힘.", "fix": "그로브 쪽이 <b>A0(=GP26)</b>인지, 센서 쪽 <b>노란선이 AO</b>(DO 아님!)인지 확인하세요. 빨강→VCC·검정→GND도 함께 점검."},
        {"sym": "켜자마자 ‘위험’으로 뜸", "cause": "예열 전이라 값이 큼.", "fix": "1~2분 기다리세요. 그래도 항상 위험이면 코드 맨 위 <code>SAFE_MAX</code>·<code>WARN_MAX</code> 숫자를 우리 환경에 맞게 올리세요."},
        {"sym": "‘❌ Wi-Fi 연결 실패’만 뜨고 멈춤", "cause": "SSID·비밀번호 오타 또는 5GHz 망.", "fix": "<code>wifi_config.py</code>의 따옴표 안 이름·비밀번호를 정확히(대소문자) 확인하고 <b>2.4GHz</b> 망인지 보세요. 고친 뒤 ⏹ 정지 → 다시 ▶ 실행."},
        {"sym": "ImportError: wifi_config", "cause": "<code>wifi_config.py</code>가 피코에 없음.", "fix": "main.py와 같은 위치에 <code>wifi_config.py</code> 파일을 새로 만들어 두 줄만 적으세요. <code>WIFI_SSID = \"와이파이이름\"</code> / <code>WIFI_PASSWORD = \"비밀번호\"</code> (위 핵심 개념의 안내 참고)."},
      ]},
    ]},
    {"title": "스스로 점검하기", "items": [
      {"type": "check", "items": [
        {"q": "MQ-2는 그로브의 어느 포트에 꽂나요?", "a": "A0 (= GP26 = ADC0). 아날로그 포트입니다. MQ-2는 핀헤더형이라 <b>그로브 암 점퍼 케이블</b>로 잇고, 센서 쪽은 <b>노랑→AO</b>(DO 아님)·빨강→VCC·검정→GND예요."},
        {"q": "값을 안정시키는 read_average는 무엇을 하나요?", "a": "여러 번(기본 10번) 읽어 평균을 냅니다. 출렁임이 줄어요."},
        {"q": "임계값은 어디서나 같은 숫자를 쓰면 되나요?", "a": "아니요. 센서·환경마다 기준이 달라, 우리 교실에서 직접 보고 보정해야 합니다."},
      ]},
    ]},
  ],
},
# ----------------------------------------------------------------- CH4 (MQ-2 × LED)
{
  "id": "ch4", "num": "04", "title": "우리반 공기질, 실시간으로 확인하기 (LED)", "accent": "#F59E0B",
  "subtitle": "폰을 켜지 않아도 책상 위 LED만 흘끗 보면 공기질을 알 수 있게 — 앞 장의 센서값을 10칸 LED 게이지로 바꿉니다.",
  "goals": [
    "센서값(ADC)을 LED 10칸 게이지로 표현할 수 있다",
    "안전/주의/위험을 색(초록·노랑·빨강)으로 나타낼 수 있다",
    "위험할 때 LED를 깜빡여 눈에 띄게 만들 수 있다",
  ],
  "why": "앞 장에선 공기질을 <b>폰(웹)</b>으로 봤어요. 그런데 매번 폰을 켜기는 번거롭죠. 같은 센서값을 <b>LED 색과 칸 수</b>로 바꾸면, 지나가다 흘끗 보기만 해도 ‘지금 환기해야겠다’를 알 수 있어요. <b>같은 데이터, 다른 출력</b> — 원격(웹)과 물리(LED)의 차이를 직접 비교해 보는 장입니다.",
  "sections": [
    {"title": "핵심 개념", "items": [
      {"type": "concept", "items": [
        {"t": "센서 → 게이지", "d": "센서값이 클수록 켜지는 칸을 늘립니다. 2장에서 만든 게이지 기법 그대로예요."},
        {"t": "색으로 상태 표시", "d": "안전=초록 · 주의=노랑 · 위험=빨강. 임계값(SAFE/WARN)은 앞 장과 같은 숫자를 씁니다."},
        {"t": "깜빡임 경고", "d": "위험 구간에서는 LED를 깜빡여, 멀리서도 바로 알아채게 합니다."},
        {"t": "이동 평균", "d": "여러 번 읽어 평균 내면 LED가 덜 깜빡거려 보기 편해요. (앞 장과 동일)"},
      ]},
      {"type": "teacher", "kind": "ask", "title": "발문 — 폰이 없어도 알 수 있게 하려면",
       "html": "“3장 대시보드는 폰을 켜야 보이죠. <b>폰이 없는 사람도, 지나가다가도</b> 공기질을 알게 하려면 어떻게 해야 할까요?” — 학생 입에서 ‘불빛으로’가 나오면 그대로 이 장이 시작됩니다. 답이 안 나오면 “신호등은 왜 글자가 아니라 색일까요?”를 이어서 물어보세요."},
      {"type": "callout", "kind": "key", "title": "LED는 timing 인자 필수 — 잊지 마세요",
       "html": "이 장도 LED를 쓰니 <code>NeoPixel(Pin(16), 10, timing=(280,515,515,745))</code>로 만듭니다. timing이 없으면 색이 깨져요. (2장 참고)"},
      {"type": "callout", "kind": "info", "title": "임계값은 우리 교실 기준으로",
       "html": "<code>SAFE_MAX</code>·<code>WARN_MAX</code>·<code>GAUGE_MAX</code> 숫자는 환경마다 달라요. 앞 장에서 본 ‘평소 값’을 참고해, 평소엔 초록·주의 상황(예: 알코올 솜·향)에 노랑/빨강이 되도록 조정하세요."},
    ]},
    {"title": "따라하기", "items": [
      {"type": "step_head", "html": "2장 <b>게이지</b>(켜진 칸 수로 양을 나타내기)를 떠올리며, 센서값을 칸 수와 색으로 바꿉니다. 이런 코드는 손으로 치지 말고, AI에게 아래처럼 <b>설명</b>해 만들면 돼요."},
      {"type": "prompt", "label": "① AI에게 이렇게 설명하세요 (그대로 복사)", "text":
"라즈베리파이 피코 2 W에서 돌아가는 마이크로파이썬(MicroPython) 코드를 만들어줘. 폰을 켜지 않아도 LED만 보면 공기질을 아는 장치야.\n- 가스센서(MQ-2)는 아날로그 입력인 26번 핀(그로브 A0 포트)으로 읽어. 값은 0~65535 사이 숫자이고 가스가 짙을수록 커져.\n- 열 칸짜리 LED 바(WS2813)는 16번 핀에 연결했어. LED를 만들 때 타이밍 값 네 개(280, 515, 515, 745)를 꼭 지정해줘. 없으면 색이 깨져. 밝기는 낮게.\n- 센서값을 여러 번 읽어 평균으로 안정시키고, 값이 클수록 켜지는 칸이 많아지는 10칸 게이지로 보여줘.\n- 안전=초록, 주의=노랑, 위험=빨강으로 색을 바꾸고, 위험일 땐 LED를 깜빡여줘.\n- 안전과 주의를 나누는 기준값은 코드 맨 위에서 바꿀 수 있게 해줘.\n- 와이파이는 필요 없어. 복사해서 바로 돌아가는 완결형 main.py 전체를 한 번에 줘."},
      {"type": "step_head", "html": "아래는 <b>완성본</b>이에요. (와이파이 불필요 · LED만 있으면 동작) 임계값은 우리 교실에 맞게 코드 위에서 조정하세요."},
      {"type": "code", "label": "② 전체 코드 · 공기질 LED 게이지 (main.py)", "lang": "python", "file": "snippets/ch4_led.py", "fold": True},
      {"type": "teacher", "kind": "say", "title": "진행 팁 — 3장과 나란히 비교 시연",
       "html": "강사 피코 두 대에 <b>3장 대시보드와 이 장 LED를 동시에</b> 돌려 두고 알코올 솜을 가까이 대 보세요. 같은 센서값에 웹 그래프와 LED 게이지가 함께 움직이는 걸 보여 주면 ‘<b>같은 데이터, 다른 출력</b>’이 말 없이도 전달됩니다. 피코가 한 대뿐이면 ③ 개선 프롬프트(웹+LED 합치기)의 결과물 하나로 시연해도 됩니다."},
      {"type": "step_head", "html": "앞 장(웹 대시보드)과 이 장(LED)을 <b>하나로 합치고</b> 싶다면, 아래 <b>③ 개선 프롬프트</b>를 이어서 붙여넣으세요."},
      {"type": "improve", "label": "③ 프롬프트 개선 — 웹 대시보드와 합치기 (이어서 복사)", "text":
"3장에서 만든 공기질 웹 대시보드에, 이 장의 LED 게이지를 합쳐줘.\n- 열 칸짜리 LED 바(WS2813)는 16번 핀에 있어. 만들 때 타이밍 값 네 개(280, 515, 515, 745)를 꼭 지정하고, 밝기는 낮게(최대 60).\n- 웹 화면과 LED가 같은 센서값, 같은 기준값을 쓰게 해줘. 안전=초록, 주의=노랑, 위험=빨강 깜빡임.\n- 복사해서 바로 돌아가는 완결형 main.py 전체를 한 번에 줘. 받은 코드에 타이밍 값이 들어 있는지 내가 확인할게."},
    ]},
    {"title": "자주 하는 실수", "items": [
      {"type": "mistakes", "items": [
        {"sym": "색이 깨지거나 엉뚱한 칸이 켜짐", "cause": "<b>timing 인자 누락.</b>", "fix": "<code>NeoPixel(Pin(16), 10, timing=(280,515,515,745))</code>로 만드세요. LED 문제의 1순위 원인입니다."},
        {"sym": "늘 빨강이거나 늘 초록", "cause": "임계값이 우리 환경과 안 맞음.", "fix": "앞 장에서 본 평소 값을 참고해 <code>SAFE_MAX</code>·<code>WARN_MAX</code>를 조정하고, 예열(1~2분)도 기다리세요."},
        {"sym": "LED가 너무 빨리 깜빡여 어지러움", "cause": "읽기·갱신 주기가 짧음.", "fix": "이동 평균 횟수를 늘리거나 <code>sleep</code> 시간을 늘리세요."},
      ]},
    ]},
    {"title": "스스로 점검하기", "items": [
      {"type": "check", "items": [
        {"q": "센서값을 LED 칸 수로 바꾸는 방법은?", "a": "값을 0~10 범위로 비례 변환해, 그 수만큼 칸을 켭니다. (게이지)"},
        {"q": "웹(3장)과 LED(4장)는 무엇이 같고 무엇이 다른가요?", "a": "같은 센서값을 쓰지만, 웹은 폰으로 ‘원격’ 확인, LED는 폰 없이 ‘물리적으로’ 흘끗 확인합니다."},
        {"q": "위험 상태를 더 눈에 띄게 하려면?", "a": "빨강으로 칠하고 깜빡이게 합니다. (멀리서도 알아챔)"},
      ]},
    ]},
  ],
},
# ----------------------------------------------------------------- CH5 (날씨 API × LED)
{
  "id": "ch5", "num": "05", "title": "강수확률 물리 대시보드 (API×LED)", "accent": "#3B82F6",
  "subtitle": "인터넷에서 오늘의 강수확률을 받아, 6시~23시를 10개 LED에 담는 ‘날씨 시계(물리 대시보드)’를 만들고, 같은 데이터를 보여 주는 웹 대시보드까지 완성합니다.",
  "goals": [
    "Open-Meteo에서 강수확률 데이터를 받아올 수 있다",
    "받은 데이터(JSON)에서 시간대별 강수확률을 꺼낼 수 있다",
    "6시~23시의 강수확률을 10개 LED의 색으로 표현할 수 있다",
    "LED와 똑같은 정보를 보여 주는 웹 대시보드(색 범례 포함)를 띄울 수 있다",
  ],
  "why": "앞에서는 <b>센서로 내 주변</b>을 봤어요. 이번엔 <b>인터넷 너머 바깥 세상의 데이터</b>를 다룹니다. 무료 날씨 API <b>Open-Meteo</b>에서 오늘의 강수확률을 받아, LED 바가 <b>아침부터 밤까지 비 올 시간을 색으로 알려 주는 시계</b>가 되고, 같은 데이터를 웹으로도 보여 줍니다. 나갈 때 LED만 보고 우산을 챙길 수 있죠.",
  "sections": [
    {"title": "핵심 개념", "items": [
      {"type": "concept", "items": [
        {"t": "Open-Meteo", "d": "무료·<b>API 키 불필요</b>한 날씨 서비스. 위도·경도만 넣으면 시간대별 강수확률을 줍니다."},
        {"t": "강수확률(precipitation_probability)", "d": "그 시각에 비가 올 가능성(%). 0시~23시까지 24개가 옵니다."},
        {"t": "HTTP 요청 (requests)", "d": "피코가 인터넷 주소에 접속해 데이터를 받아오는 도구. <code>requests.get(url)</code>"},
        {"t": "6~23 → 10칸 매핑", "d": "오전 6시~밤 11시(18시간)를 10칸으로 고르게 나눠 대표 시각 10개를 LED에 배치합니다."},
      ]},
      {"type": "dig", "title": "API가 대체 뭐예요? — 관공서에서 등본 떼기로 이해하기",
       "html": API_ANALOGY_SVG},
      {"type": "teacher", "kind": "say", "title": "진행 멘트 — 등본 애니메이션 시연 순서 (3분)",
       "html": "화면에 띄우고 “API가 뭔지 <b>동사무소에서 등본 떼기</b>로 봅시다”라며 <b>위 줄(비유)을 먼저 클릭</b>해 신청서→등본 흐름을 보여 주세요. 그다음 “피코도 똑같습니다”라며 <b>아래 줄(피코)</b>을 클릭 — 신청서가 위도·경도로, 등본이 강수확률로 바뀔 뿐 흐름이 같다는 걸 짚습니다. 마지막에 학생들도 각자 두 줄을 눌러 보게 하세요. 여기에 3분을 쓰면 뒤의 URL 파라미터 설명이 훨씬 빨라집니다."},
      {"type": "linkbtn", "href": "https://open-meteo.com", "label": "open-meteo.com — 무료 날씨 API (키 불필요)"},
      {"type": "callout", "kind": "info", "title": "설치 없이 바로 됩니다",
       "html": "이번 장 코드는 피코에 <b>기본 내장된 <code>socket</code> + <code>ssl</code></b>만 써서 인터넷에 접속해요. 그래서 <b>추가 설치가 필요 없습니다</b> — 복사해서 바로 실행하면 됩니다. (연수 현장에서 모두가 패키지를 설치하다 막히는 일을 피하려고 이렇게 했어요.)<br><br>혹시 코드를 더 짧게 쓰고 싶다면 <code>requests</code> 모듈을 설치하는 방법도 있는데, 그 버전은 Step 3 아래에 따로 실어 뒀습니다."},
      {"type": "callout", "kind": "info", "title": "먼저 — 와이파이 정보 파일 만들기 (wifi_config.py)",
       "html": "이 장의 코드는 와이파이 정보를 <code>wifi_config.py</code>에서 불러옵니다. <b>main.py와 같은 위치</b>에 이 파일을 새로 만들고 두 줄만 적어 저장하세요.<br><br><code>WIFI_SSID = \"우리_와이파이_이름\"</code><br><code>WIFI_PASSWORD = \"비밀번호\"</code><br><br>(피코는 <b>2.4GHz</b> 와이파이만 됩니다. 이름·비밀번호를 정확히.)"},
      {"type": "dig", "title": "HTTPS와 인증서 — 코드의 CERT_NONE은 무슨 뜻일까?",
       "html": "주소가 <code>https://</code>로 시작하면, 피코와 서버 사이 통신이 <b>암호화(TLS)</b>됩니다. 중간에서 누가 엿봐도 내용을 못 읽죠.<br><br>원래 인터넷 브라우저는 ‘이 서버가 진짜 open-meteo가 맞는지’를 <b>인증서</b>로 확인합니다. 이때 신뢰할 수 있는 기관(CA) 목록이 필요한데, <b>피코에는 그 목록이 기본으로 들어 있지 않아요.</b> 그래서 코드에서 <code>ssl.CERT_NONE</code>으로 ‘서버 신원 확인은 건너뛰고, 암호화만 쓰겠다’고 한 거예요.<br><br>교육용으로 공개 날씨 데이터를 받는 정도는 충분히 안전합니다. 다만 <b>로그인·비밀번호처럼 민감한 정보</b>를 주고받을 땐 신원 확인을 생략하면 안 되니, 그때는 인증서를 갖춘 환경에서 해야 합니다."},
    ]},
    {"title": "따라하기", "items": [
      {"type": "step_head", "html": "<b>Step 1.</b> 우리 지역 <b>위도·경도</b>를 정합니다. 코드 맨 위 <code>LAT</code>/<code>LON</code>을 바꾸면 돼요. (검색창에 ‘우리동네 위도 경도’를 쳐서 찾으세요. 서울시청은 37.5665 / 126.9780)"},
      {"type": "step_head", "html": "<b>Step 2.</b> 먼저 강수확률을 받아 셸에 출력해, <b>데이터가 어떻게 생겼는지</b> 확인해요. 인터넷 접속 함수(<code>http_get_json</code> 등)는 길어서 손코딩하지 않아요 — AI에게 아래처럼 <b>설명</b>해 만들면 됩니다."},
      {"type": "prompt", "label": "AI에게 이렇게 설명하세요 (그대로 복사)", "text":
"라즈베리파이 피코 2 W에서 돌아가는 마이크로파이썬(MicroPython) 코드를 만들어줘. 날씨 데이터가 어떻게 생겼는지 먼저 확인하려는 거야.\n- 무료 날씨 서비스 Open-Meteo(키 필요 없음)에서 우리 지역의 오늘 시간별 강수확률을 받아와.\n- 아침 6시부터 밤 11시까지를 'N시 강수확률: M%' 형식으로 셸에 출력해줘.\n- 외부 라이브러리는 설치하지 말고, 피코에 기본 내장된 인터넷 접속 기능(socket, ssl)만 써. 보안 인증서 확인은 건너뛰어도 돼.\n- 와이파이 정보는 설정 파일(wifi_config.py)에서 불러오고, 위도·경도는 코드 맨 위에 둬서 내가 바꿀 수 있게 해줘.\n- 복사해서 바로 돌아가는 코드 전체를 한 번에 줘."},
      {"type": "step_head", "html": "직접 만들지 않아도 아래 <b>완성본</b>을 복사해 실행하면 됩니다. (긴 <code>http_get_json</code>은 뒤 단계에서도 그대로 재사용해요.)"},
      {"type": "code", "label": "전체 코드 · 강수확률 받아오기", "lang": "python", "file": "snippets/ch5_fetch.py"},
      {"type": "teacher", "kind": "err", "title": "예상 오류 — 이 장의 통신 막힘 3종",
       "html": "① <b>연결 자체가 안 됨</b> — 5GHz 망입니다. 강사 핫스팟(2.4GHz)으로 옮기게 하세요. ② <b>바다 한가운데 날씨</b>가 나옴 — <code>LAT</code>·<code>LON</code>을 서로 바꿔 넣은 겁니다. “한국은 위도 33~38, 경도 124~132”를 칠판에 적어 두면 스스로 잡아냅니다. ③ 뒤의 대시보드 단계에서 <b>주소가 안 열림</b> — 폰 브라우저가 <code>https://</code>로 붙인 경우가 대부분이니, 주소창에 <code>http://</code>를 직접 쳐 넣게 하세요."},
      {"type": "callout", "kind": "info", "title": "코드가 여러 개죠? — 최종은 하나만",
       "html": "아래로 가면서 코드가 여러 번 나와요. <b>피코에 저장(main.py)할 최종 코드는 딱 하나</b>면 됩니다:<br>· Step 2(강수확률 출력) = <b>확인용</b>(잠깐 실행만)<br>· Step 3(날씨 시계) = LED만 버전<br>· <b>Step 5(LED + 웹) = 가장 완성본 ← 이거 하나면 충분</b><br>새 코드를 쓸 땐 <b>이전 코드를 지우고</b> 붙여넣으세요(피코는 한 번에 main.py 하나만 돌려요)."},
      {"type": "step_head", "html": "<b>Step 3.</b> 받은 값을 10개 LED의 색으로 바꿔 ‘날씨 시계’를 만들어요. 이런 긴 코드는 손으로 치지 않아요 — AI에게 아래처럼 <b>설명</b>하면 만들어 줍니다."},
      {"type": "prompt", "label": "① AI에게 이렇게 설명하세요 (그대로 복사)", "text":
"라즈베리파이 피코 2 W에서 돌아가는 마이크로파이썬(MicroPython) 코드를 만들어줘. 하루의 비 예보를 LED 색으로 보여주는 '날씨 시계'야.\n- 무료 날씨 서비스 Open-Meteo(키 필요 없음)에서 오늘 시간별 강수확률을 받아와. 인터넷 접속은 피코 기본 내장 기능(socket, ssl)만 쓰고 추가 설치는 하지 마.\n- 와이파이 정보는 설정 파일(wifi_config.py)에서 불러와.\n- 아침 6시~밤 11시(18시간)를 열 칸짜리 LED 바에 고르게 나눠, 각 시각의 강수확률을 색으로 표시해줘. 예: 맑음=초록, 흐림=노랑, 비 가능=파랑, 비 확실=보라. 구간별 색은 코드 위에서 바꿀 수 있게.\n- LED 바(WS2813)는 16번 핀에 연결했어. 만들 때 타이밍 값 네 개(280, 515, 515, 745)를 꼭 지정해줘. 없으면 색이 깨져. 밝기는 낮게.\n- 날씨는 10분에 한 번만 새로 받아와줘.\n- 위도·경도와 타이밍 값은 코드 맨 위에 두고, 복사해서 바로 돌아가는 완결형 main.py 전체를 한 번에 줘."},
      {"type": "step_head", "html": "직접 만들지 않아도, 아래 <b>완성본</b>을 복사하면 바로 돕니다. (추가 설치 없음 · 10분마다 새 예보로 갱신)"},
      {"type": "code", "label": "② 전체 코드 · 날씨 시계 (main.py) — 무설치", "lang": "python", "file": "snippets/ch5_full.py", "fold": True},
      {"type": "callout", "kind": "tip", "title": "더 짧게 쓰고 싶다면 — requests 버전 (설치 1회)",
       "html": "위 무설치 버전이 기본이에요. 만약 <code>requests</code>를 설치할 수 있는 환경이라면, HTTP 부분을 훨씬 짧게 쓸 수 있습니다. Thonny <b>도구 → 패키지 관리</b>에서 <code>requests</code>를 한 번 설치(피코가 와이파이 연결된 상태)한 뒤 아래 버전을 쓰세요. 동작은 똑같습니다."},
      {"type": "code", "label": "대안 · 날씨 시계 (requests 설치 버전)", "lang": "python", "file": "snippets/ch5_full_requests.py", "fold": True},
      {"type": "step_head", "html": "<b>Step 4.</b> 이번엔 여기에 <b>웹 대시보드를 더해</b> 봐요. ①→②에 이어 붙이는 <b>③ 개선 프롬프트</b>입니다. (교재를 모르는 AI도 바로 작업할 수 있게, 필요한 정보가 모두 들어 있어요.)"},
      {"type": "improve", "label": "③ 프롬프트 개선 — 웹 대시보드 더하기 (이어서 복사)", "text":
"방금 만든 날씨 시계에 웹 대시보드를 더해줘.\n- 피코가 외부 라이브러리 없이 작은 웹서버(80번 포트)가 되게 해줘.\n- 브라우저가 '/data' 주소에서 JSON을 주기적으로 받아 화면을 자동 갱신하게 해줘.\n- 같은 와이파이의 스마트폰에서 접속하면 6시~23시 강수확률을 막대그래프로 보여주고, 색의 의미(범례)도 함께 표시해줘.\n- LED와 웹이 같은 데이터를 쓰고, 날씨는 지금처럼 10분에 한 번만 새로 받아와줘. 피코가 버겁지 않게.\n- 위도·경도와 LED 타이밍 값은 그대로 코드 맨 위에 두고, 복사해서 바로 돌아가는 완결형 main.py 전체를 한 번에 줘."},
      {"type": "callout", "kind": "tip", "title": "바이브코딩의 핵심",
       "html": "AI가 준 코드를 <b>그대로 믿지 말고</b>, ① timing 인자가 들어 있는지 ② 내 위도·경도를 쓰는지 ③ 너무 자주 API를 부르지 않는지 확인하세요. ‘동작을 우리말로 설명 → 받은 코드를 내 기준으로 점검’이 바이브코딩의 리듬입니다."},
      {"type": "step_head", "html": "<b>Step 5.</b> 직접 설명하지 않아도, 아래 <b>완성형 대시보드</b>를 바로 써도 됩니다. LED를 켜면서 동시에 웹서버가 되어, 스마트폰/PC로 접속하면 <b>피코 10칸과 똑같은 색의 칸 · 색의 뜻(범례) · 시간별 강수확률 막대</b>를 보여 줍니다. (무설치 · main.py로 저장)"},
      {"type": "code", "label": "전체 코드 · 날씨 LED + 웹 대시보드 (main.py)", "lang": "python", "file": "snippets/ch5_dashboard.py", "fold": True},
      {"type": "callout", "kind": "key", "title": "대시보드 읽는 법 — 색이 곧 비 예보",
       "html": "화면의 10칸은 피코 LED와 1:1로 같아요. 칸 위 시각(6시·8시…)과 색을 보면 <b>‘이 시각에 비가 오는구나’</b>를 알 수 있습니다.<br>🟩 <b>맑음</b> 0–20% · 🟨 <b>흐림</b> 20–50% · 🟦 <b>비 가능</b> 50–80% · 🟪 <b>비 확실</b> 80–100%.<br>아래 막대그래프는 6시~23시 전체 흐름이라, 파랑·보라가 모이는 구간이 ‘비 오는 시간대’입니다. 임계값(20·50·80)이나 색은 코드 맨 위 <code>LEVELS</code>에서 바꾸면 LED·웹이 함께 바뀝니다."},
    ]},
    {"title": "자주 하는 실수", "items": [
      {"type": "mistakes", "items": [
        {"sym": "ImportError: no module named 'requests'", "cause": "<b>requests 설치 버전</b>을 쓰는데 모듈이 없음.", "fix": "기본(무설치) 버전을 쓰면 이 오류가 안 납니다. 굳이 requests 버전을 쓰려면 Thonny <b>도구 → 패키지 관리</b>에서 <code>requests</code>를 와이파이 연결 후 설치하세요."},
        {"sym": "ssl/연결 오류로 멈춤", "cause": "TLS 연결이 일시적으로 실패하거나 메모리 부족.", "fix": "다시 실행해 보세요. 코드는 매 요청 전 <code>gc.collect()</code>로 메모리를 정리하고, 인증서 검증은 생략(<code>CERT_NONE</code>)합니다. 자주 끊기면 갱신 간격을 늘리세요."},
        {"sym": "위도·경도를 바꿨는데 엉뚱한 지역", "cause": "위도(LAT)와 경도(LON)를 바꿔 넣음.", "fix": "한국 기준 위도는 33~38, 경도는 124~132 범위예요. 둘이 바뀌면 바다 한가운데가 됩니다."},
        {"sym": "메모리 오류로 멈춤", "cause": "HTTPS 응답이 큰데 자주 부름.", "fix": "필요한 항목(precipitation_probability)만 요청하고, 갱신 간격을 10분(600초) 이상으로 두세요. 위 코드는 이미 그렇게 했습니다."},
        {"sym": "대시보드 주소가 안 열림", "cause": "스마트폰이 피코와 다른 와이파이이거나 <code>https</code>로 접속.", "fix": "셸에 찍힌 주소를 <b><code>http://</code></b>(s 없이)로, 피코와 <b>같은 와이파이</b>에서 여세요. LED는 떠도 화면이 안 뜨면 갱신을 기다리거나 페이지를 새로고침하세요."},
      ]},
    ]},
    {"title": "스스로 점검하기", "items": [
      {"type": "check", "items": [
        {"q": "Open-Meteo는 API 키가 필요한가요?", "a": "아니요. 무료이고 키 없이 위도·경도만으로 씁니다."},
        {"q": "강수확률 24개 중 6시 값은 어떻게 꺼내나요?", "a": "<code>probs[6]</code>. 리스트 인덱스가 곧 시각(0~23시)입니다."},
        {"q": "왜 10분마다만 새로 받아오나요?", "a": "날씨는 자주 안 바뀌고, 너무 자주 요청하면 피코 메모리·네트워크에 부담이 되기 때문입니다."},
      ]},
    ]},
    {"title": "Open-Meteo 자세히 알기", "items": [
      {"type": "text", "html": "<b>Open-Meteo</b>는 독일의 비영리 프로젝트로, 여러 나라 기상청의 공개 수치예보 모델을 모아 누구나 쓰도록 공개합니다. <b>API 키도, 회원가입도 필요 없고</b>, 비상업·교육용은 자유롭게 쓸 수 있어요. 주소(URL) 하나에 ‘어디(위도·경도)·무엇(변수)·언제(기간)’를 적어 보내면, 그 자리에서 JSON으로 답을 줍니다."},
      {"type": "concept", "items": [
        {"t": "여러 종류의 API", "d": "<b>forecast</b>(예보) · <b>archive</b>(1940년~ 과거 데이터) · <b>air-quality</b>(대기질) · <b>marine</b>(파고·해양) · <b>elevation</b>(고도). 주소의 앞부분만 바꾸면 됩니다."},
        {"t": "고를 수 있는 변수", "d": "기온 <code>temperature_2m</code> · 습도 <code>relative_humidity_2m</code> · 강수확률 <code>precipitation_probability</code> · 풍속 <code>windspeed_10m</code> · 기압 <code>surface_pressure</code> · 자외선 <code>uv_index</code> · 일사량 <code>shortwave_radiation</code>"},
        {"t": "응답(JSON) 구조", "d": "<code>hourly.time</code>(시각 배열)과 <code>hourly.기온</code>(값 배열)이 <b>같은 순서로 짝</b>을 이룹니다. 그래서 <code>값[6]</code>이 곧 그 날 6시 값이에요."},
        {"t": "기간 고르기", "d": "<code>forecast_days=1</code>(오늘) · <code>past_days=7</code>(지난 일주일) · archive는 <code>start_date</code>/<code>end_date</code>로 특정 기간."},
      ]},
      {"type": "dig", "title": "‘강수확률 60%’가 실제로 뜻하는 것",
       "html": "강수확률(POP, Probability of Precipitation)은 <b>그 시간·그 지역에 0.1mm 이상의 비가 내릴 통계적 확률</b>입니다. 비의 ‘양’이나 ‘세기’가 아니라 ‘올지 안 올지의 가능성’이에요.<br><br>흔한 오해 두 가지:<br>· ‘60%’는 <b>‘하늘의 60%에 비가 온다’</b>는 뜻이 아니에요.<br>· ‘비가 60% 세기로 온다’는 뜻도 아니에요.<br><br>예보 모델이 같은 조건을 여러 번 시뮬레이션했을 때 <b>10번 중 6번꼴로 비가 내렸다</b>는 의미에 가깝습니다. 그래서 강수확률이 높아도 실제로 안 올 수 있고, 낮아도 소나기가 올 수 있어요. 수업에서 ‘확률’과 ‘실제 관측’의 차이를 이야기하기 좋은 소재입니다."},
      {"type": "teacher", "kind": "theory", "title": "이론 심화 — “60%인데 안 왔잖아요”에 답하기",
       "html": "강수확률 60%는 ‘같은 조건에서 10번 중 6번꼴로 비가 온다’는 뜻이라, <b>안 와도 예보가 틀린 게 아닙니다.</b> 토론으로 키우기 좋은 질문 두 개: “확률 60% 예보가 맞았는지는 <b>하루</b>로 판정할 수 있을까요, <b>100일</b>을 모아야 할까요?” “우산을 챙기는 기준은 몇 %가 합리적일까요 — 사람마다 달라도 될까요?” 수학의 확률·통계 단원과 바로 이어지는 소재입니다."},
      {"type": "callout", "kind": "tip", "title": "변수 바꾸는 법 — 주소의 hourly= 뒤만 고치면 끝",
       "html": "앞서 만든 코드에서 요청 주소의 <code>hourly=</code> 뒤만 바꾸면 다른 데이터를 받습니다.<br>· 기온: <code>...&hourly=temperature_2m</code><br>· 자외선 지수: <code>...&hourly=uv_index</code><br>· 일사량(태양광): <code>...&hourly=shortwave_radiation</code><br>여러 개를 쉼표로: <code>...&hourly=temperature_2m,relative_humidity_2m</code><br>과거 데이터는 주소를 <code>https://archive-api.open-meteo.com/v1/archive</code> 로 바꾸고 <code>&start_date=2015-06-01&end_date=2015-06-30</code> 처럼."},
      {"type": "ideas", "items": [
        {"t": "📈 하루 기온 곡선", "d": "기온을 받아 24시간 그래프 → 일교차·최고/최저 시각 찾기 (지구과학)"},
        {"t": "🌡️ 기후변화 비교", "d": "archive로 ‘10년 전 6월’과 ‘올해 6월’ 평균기온 비교 (환경·기후)"},
        {"t": "☀️ 자외선 경보등", "d": "uv_index가 높으면 LED 빨강 → 자외선 차단 알림 (보건·물리)"},
        {"t": "🔆 태양광 발전 추정", "d": "shortwave_radiation(일사량)으로 발전량 어림 (에너지·물리)"},
      ]},
      {"type": "linkbtn", "href": "https://open-meteo.com/en/docs", "label": "open-meteo.com/en/docs — 변수·파라미터 전체 문서"},
    ]},
    {"title": "과학 수업에 쓸 만한 다른 오픈 API", "items": [
      {"type": "text", "html": "Open-Meteo 말고도 <b>무료에 대부분 키가 필요 없는</b> 과학 데이터 API가 많아요 — 지진·ISS·일출몰·물질(화학)·생물 등. 과목별로 <b>어떤 데이터를 주고 무엇을 탐구할 수 있는지</b>를 <b>부록 A</b>에 한눈에 정리했고, 브라우저에서 바로 받아 그려 보는 <b>라이브 대시보드(지도·그래프)</b>로도 만들어 뒀습니다(국내 적용 여부도 표시). 키 없이 동작하는 것만 골랐고, 2026년 기준 응답을 확인했어요."},
      {"type": "linkbtn", "href": "dashboards/index.html", "label": "오픈 API 라이브 대시보드 갤러리 열기 (10종 · 5장 날씨 포함)"},
      {"type": "callout", "kind": "key", "title": "🇰🇷 국내 공식 데이터가 필요하면 — 공공데이터포털",
       "html": "‘우리나라 공식 수치’가 필요한 수업(국내 지진·미세먼지·동네예보)이라면 <a class=\"ilink\" href=\"https://www.data.go.kr\" target=\"_blank\" rel=\"noopener\"><b>공공데이터포털(data.go.kr)</b></a>에서 무료 인증키를 받아 쓰세요. 글로벌 API보다 국내 정확도가 높습니다.<br>· <b>기상청 동네예보·지진통보</b> (data.go.kr) — 국내 공식 기상·지진<br>· <a class=\"ilink\" href=\"https://www.airkorea.or.kr\" target=\"_blank\" rel=\"noopener\"><b>에어코리아(한국환경공단) 미세먼지</b></a> — 측정소별 실시간 PM2.5/PM10<br><span style='color:#a55'>※ 회원가입 + 서비스키 신청이 필요하고 응답 형식(XML/JSON)이 제각각이라, 초보 단계에선 키 없는 글로벌 API로 원리를 익힌 뒤 넘어오길 권합니다.</span>"},
      {"type": "callout", "kind": "info", "title": "피코로 가져올 때 한 가지",
       "html": "대부분 <b>https + JSON</b>이라, 이 장의 <code>http_get_json()</code>(소켓+ssl) 함수를 그대로 써서 받을 수 있어요. 다만 응답이 큰 API(지진 전체 목록, NASA 이미지 등)는 피코 메모리에 부담이 될 수 있으니, <b>필요한 항목만 요청</b>하거나 수업에서는 컴퓨터(파이썬·브라우저)로 보여 주는 방법도 좋습니다."},
    ]},
  ],
},
# ----------------------------------------------------------------- CH6 (센서 → 구글 시트 기록)
{
  "id": "ch6", "num": "06", "title": "우리반 공기질 기록 노트 (센서 → 구글 시트)", "accent": "#16A34A",
  "subtitle": "피코가 잰 공기질을 구글 시트에 1분마다 자동 기록합니다. 밤새 쌓인 데이터를 아침에 열어 보면 — 우리가 없는 동안의 교실이 보여요.",
  "goals": [
    "‘실시간으로 보는 것’과 ‘기록으로 남기는 것’의 차이를 설명할 수 있다",
    "Google Apps Script 웹앱을 만들고 ‘모든 사용자’로 배포할 수 있다",
    "피코에서 센서값을 HTTPS로 구글 시트에 자동 기록할 수 있다",
    "쌓인 데이터를 차트·조건부 서식으로 탐구하고 결론 한 줄을 쓸 수 있다",
  ],
  "why": "지난 장에서 피코는 인터넷에서 데이터를 <b>받아 왔죠</b>(Open-Meteo). 이번엔 방향을 뒤집어 <b>보냅니다</b>. 3·4장의 공기질은 화면을 보는 ‘그 순간’만 알 수 있었어요 — 그런데 <b>어젯밤 우리 교실 공기는 어땠을까요?</b> 아무도 모릅니다. 기록하지 않았으니까요. 이 장에서는 피코가 잰 값을 <b>구글 시트에 1분마다 한 줄씩</b> 자동으로 쌓습니다. 시트는 무료이고, <b>Apps Script 웹앱</b>을 거치면 피코가 로그인 없이 <b>URL 하나로</b> 기록할 수 있어요. 데이터가 시간과 만나면, 순간의 숫자가 <b>이야기</b>가 됩니다.",
  "sections": [
    {"title": "핵심 개념 — ‘보는 것’에서 ‘남기는 것’으로", "items": [
      {"type": "teacher", "kind": "ask", "title": "발문 — 개념을 질문으로 먼저",
       "html": "“어제 밤 11시, 우리 교실 공기질은 어땠을까요? 지금 알 수 있는 방법이 있나요?” — 없다는 답이 나오면 “왜 없을까요?”를 이어 물으세요. <b>‘기록하지 않았으니까’</b>라는 답이 나오는 순간, 이 장의 필요성이 학습자 입에서 나온 셈입니다. “여러분 휴대폰 걸음 수는 어떻게 ‘어제 것’을 보여줄까요?”로 로깅이 이미 일상에 있음을 연결해도 좋아요."},
      {"type": "concept", "items": [
        {"t": "로깅(logging)", "d": "측정값을 <b>시각과 함께</b> 차곡차곡 저장하는 것. 걸음 수 앱, 블랙박스, 관측소가 모두 로깅 장치예요."},
        {"t": "실시간 vs 기록", "d": "실시간(3·4장)은 <b>지금</b>을 알려주고, 기록은 <b>변화·패턴·비교</b>를 알려줍니다. ‘언제 나빠지나’는 기록만이 답할 수 있어요."},
        {"t": "웹 앱(Web App)", "d": "URL을 부르면 실행되는 작은 프로그램. 우리는 <b>Apps Script</b>로 ‘값을 받아 시트에 한 줄 쓰는’ 웹앱을 만듭니다."},
        {"t": "이번 장의 방향", "d": "1·3장: 피코가 <b>서버</b>(브라우저가 가지러 옴) → 5장: 피코가 <b>받아옴</b> → 이번 장: 피코가 <b>보냄</b>. 도구는 같고 <b>방향만 반대</b>예요."},
      ]},
      {"type": "callout", "kind": "key", "title": "왜 구글 시트에 ‘바로’ 못 쓰나요? — 우편함이 필요한 이유",
       "html": "구글 시트에 직접 쓰려면 <b>구글 로그인(인증)</b>이 필요한데, 작은 피코는 그 복잡한 절차를 감당하기 어려워요. 그래서 중간에 <b>Apps Script 웹앱</b>이라는 <b>우편함</b>을 세웁니다 — 웹앱은 내 계정 권한으로 시트에 쓸 수 있고, 피코는 <b>우편함 주소(URL)만 알면</b> 값을 던져 넣으면 돼요. ‘로그인은 웹앱이, 배달은 피코가’ — 이 분업이 이 장의 핵심 구조입니다."},
      {"type": "dig", "title": "리다이렉트 — 구글이 ‘저쪽 창구로 가세요’ 하는 것",
       "html": "피코가 웹앱 주소로 요청을 보내면, 구글은 종종 <b>302</b>라는 답과 함께 ‘진짜 처리는 <b>이 주소</b>에서 해요’라고 다른 주소를 알려줍니다. 은행에서 번호표를 뽑았더니 “이 업무는 3번 창구로 가세요” 하는 것과 같아요. 브라우저는 이걸 <b>자동으로</b> 따라가지만, 우리가 직접 만드는 피코 코드는 <b>Location(새 주소)을 읽어 한 번 더 요청</b>해야 합니다. 아래 완성 코드의 <code>send()</code> 함수가 정확히 그 일을 해요 — ‘실패’처럼 보이는 302가 사실은 <b>정상 절차</b>라는 것, 기억해 두세요."},
    ]},
    {"title": "그림으로 보기 — 데이터가 어떻게 쌓일까", "items": [
      {"type": "text", "html": "마치 <b>엽서</b>를 보내는 것과 같아요. 피코가 지금 잰 숫자를 엽서에 적어 ‘구글 시트’라는 <b>우편함</b>으로 보내면, 시트에 <b>새 줄이 하나씩</b> 차곡차곡 쌓입니다. 👇"},
      {"type": "raw", "html": SHEETS_FLOW_SVG},
    ]},
    {"title": "1단계 · 구글 쪽 준비 (한 번만 · 차근차근)", "items": [
      {"type": "text", "html": "이 단계는 <b>컴퓨터 브라우저에서만</b> 진행합니다(피코는 아직 책상 위에). 화면이 여러 번 바뀌지만 순서대로 하면 <b>5분</b>이면 끝나요. 구글 계정이 필요합니다."},
      {"type": "callout", "kind": "warn", "title": "⚠️ 개인 구글 계정으로 하세요 (학교 계정 ✗)",
       "html": "학교에서 발급한 계정(구글 워크스페이스)은 관리자 설정에 따라 <b>Apps Script가 막혀 있거나</b>, 배포할 때 액세스 권한에 <b>‘모든 사용자’ 선택지가 아예 안 뜰 수</b> 있어요(‘○○학교의 모든 사용자’까지만 나옴). 그러면 로그인을 못 하는 피코는 무조건 실패합니다. 뒤에서 ‘모든 사용자’가 목록에 안 보이면 십중팔구 이것 때문 — <b>개인 @gmail.com 계정</b>으로 다시 진행하세요."},
      {"type": "steps", "items": [
        {"t": "새 구글 시트 만들기", "d": "주소창에 <a class=\"ilink\" href=\"https://sheets.new\" target=\"_blank\" rel=\"noopener\"><code>sheets.new</code></a>를 입력하면 새 시트가 열려요. (로그인이 안 돼 있으면 <b>로그인 화면이 먼저</b> 뜹니다.) 왼쪽 위 제목을 <b>‘우리반 공기질’</b>처럼 바꾸고, 1행에 <b>시각</b>·<b>값</b>이라고 적어 둡니다."},
        {"t": "Apps Script 열기", "d": "시트 메뉴 <b>확장 프로그램 → Apps Script</b>를 누르면 코드 편집기가 <b>새 탭</b>으로 열려요. (‘확장 프로그램’ 메뉴가 안 보이면 화면이 좁은 거예요 — 창을 넓혀 보세요.)"},
        {"t": "코드 붙여넣기 → 저장", "d": "편집기에 이미 적힌 <code>function myFunction()…</code>을 <b>전부 선택(Ctrl+A · 맥은 ⌘A)해 지우고</b>, 아래 코드를 통째로 붙여넣으세요. 파일 이름은 <code>Code.gs</code> 그대로 두고 저장(💾)합니다."},
      ]},
      {"type": "code", "label": "Apps Script 코드 (Code.gs 에 붙여넣기)", "lang": "javascript", "code":
"function doGet(e) {\n  const sh = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];\n  sh.appendRow([new Date(), Number(e.parameter.value)]);   // [시각, 값] 한 줄 추가\n  return ContentService.createTextOutput(\"OK\");\n}"},
      {"type": "callout", "kind": "info", "title": "이 다섯 줄이 하는 일",
       "html": "<code>doGet</code>은 누군가 이 웹앱 주소를 <b>열 때마다</b> 실행되는 함수예요. 주소 뒤에 붙어 온 <code>value</code>를 꺼내(<code>e.parameter.value</code>) 시트 맨 아래에 <b>[지금 시각, 값]</b> 한 줄을 추가하고(<code>appendRow</code>), ‘OK’라고 답합니다. 우편함에 편지가 오면 도장 찍고 서랍에 넣는 일을 코드 다섯 줄이 하는 거죠. 가운데 <code>Number(…)</code>는 문자로 도착한 값을 <b>숫자로 바꿔서</b> 넣는 부분 — 이래야 나중에 평균·차트가 제대로 됩니다."},
      {"type": "steps", "items": [
        {"t": "시간대를 서울로", "d": "왼쪽 <b>프로젝트 설정(⚙️)</b> → 시간대 → <b>(GMT+09:00) 서울</b>로 바꿉니다. 안 바꾸면 기록 시각이 <b>미국 시간</b>으로 적혀서 나중에 그래프가 통째로 어긋나요. (그래도 시각이 이상하면 <b>시트로 돌아가 파일 → 설정 → 시간대</b>도 서울인지 확인하세요 — 표시 시간대는 시트 설정을 따릅니다.)"},
        {"t": "웹 앱으로 배포 시작", "d": "오른쪽 위 파란 <b>배포 → 새 배포</b>를 누르고, ‘유형 선택’ 옆 <b>톱니바퀴(⚙️)</b>를 눌러 <b>웹 앱</b>을 고릅니다. (처음이면 ‘프로젝트 이름을 입력하세요’ 창이 먼저 떠요 — ‘공기질기록’ 등 아무 이름이나 적고 넘어가면 됩니다.)"},
        {"t": "권한 설정 후 배포", "d": "실행: <b>나</b> · 액세스 권한: <b>모든 사용자</b>로 두고 <b>배포</b>를 누르세요. <b>(피코는 로그인을 못 하니 꼭 ‘모든 사용자’!)</b> 기본값(‘나만’)으로 두면 아무 오류 없이 조용히 실패합니다. ‘모든 사용자’가 목록에 없으면 학교 계정이에요 — 위 경고 콜아웃을 보세요."},
        {"t": "권한 승인 (처음 한 번만)", "d": "‘액세스 승인’ → 내 구글 <b>계정 선택</b> → <b>‘확인되지 않은 앱’ 경고</b>가 떠도 정상 → 왼쪽 아래 <b>고급</b> → <b>‘…(으)로 이동(안전하지 않음)’</b> → <b>허용</b>. (화면에 따라 ‘허용’ 대신 항목에 체크하고 <b>‘계속’</b>을 누르는 모양일 수 있어요 — 같은 뜻입니다.) 이 경고 화면에서 90%가 멈칫하는데, 아래 설명을 읽고 침착하게 통과하세요."},
        {"t": "웹 앱 주소 복사", "d": "마지막에 나오는 <b>‘웹 앱 URL’</b>(<code>/exec</code>로 끝나는 긴 주소)의 <b>복사</b>를 누르세요. (<b>디플로이 ID가 아니라 URL</b>이에요! 브라우저 주소창의 편집 화면 주소도 아닙니다.) 메모장에 붙여 두면 다음 단계가 편해요."},
      ]},
      {"type": "callout", "kind": "tip", "title": "겁먹지 마세요 — ‘확인되지 않은 앱’ 경고",
       "html": "빨간/노란 경고 화면은 ‘구글이 아직 검토하지 않은 앱’이라는 뜻일 뿐이에요. 남이 만든 수상한 앱이 아니라 <b>내가 방금 만든 스크립트</b>라 안전합니다. <b>왼쪽 아래 ‘고급’ → ‘…(으)로 이동(안전하지 않음)’ → ‘허용’</b> 순서로 넘어가면 됩니다."},
      {"type": "raw", "html": (
        '<div class="urlbox">'
        '<label>🔗 방금 복사한 ‘웹 앱 URL’(<span style="font-family:var(--mono)">/exec</span>)을 여기에 붙여넣어 보세요</label>'
        '<input type="url" placeholder="https://script.google.com/macros/s/…/exec" spellcheck="false" autocomplete="off">'
        '<div class="urlbox-msg"></div>'
        '<small>주소는 이 브라우저에만 저장되고 어디로도 전송되지 않아요. 붙여넣으면 아래 <b>2단계 완성 코드에 자동으로 들어가고</b>, 중간 점검용 테스트 링크도 만들어 줍니다.</small>'
        '</div>')},
      {"type": "step_head", "html": "<b>중간 점검 — 피코 없이 웹앱부터 시험!</b> 위 상자에 주소를 붙여넣으면 <b>🧪 테스트 링크</b>가 생겨요. 링크를 누르거나, 직접 주소 뒤에 <code>?value=99</code>를 붙여 새 탭에서 열어 보세요."},
      {"type": "check_list", "items": [
        "브라우저 화면에 <b>OK</b>라고 떴나요?",
        "시트 탭으로 돌아가면 <b>[방금 시각, 99]</b> 한 줄이 생겼나요?",
        "한 번 더 열면(새로고침) 줄이 <b>하나 더</b> 늘어나나요?",
      ]},
      {"type": "callout", "kind": "key", "title": "이 중간 점검이 반이에요",
       "html": "여기서 OK가 뜨면 <b>구글 쪽은 완성</b> — 이후 문제가 생겨도 범인은 피코 쪽(와이파이·주소 오타)으로 좁혀집니다. 반대로 여기서 안 되면 피코를 붙여도 절대 안 돼요. <b>‘한 번에 다 만들고 몰아서 시험’ 대신 ‘반 만들고 반 시험’</b> — 디버깅의 기본기입니다."},
      {"type": "callout", "kind": "info", "title": "나중에 코드를 고치면 — 새 버전으로 재배포",
       "html": "Apps Script 코드를 수정했다면 <b>배포 → 배포 관리 → 편집(연필) → 버전: 새 버전 → 배포</b>로 다시 배포해야 반영됩니다. (주소는 그대로예요.) 편집기에서 저장만 하면 <b>옛 코드가 계속 돕니다.</b>"},
      {"type": "teacher", "kind": "say", "title": "진행 멘트 — 이 단계는 ‘같이 천천히’ (15분)",
       "html": "이 장에서 시간을 잡아먹는 건 피코가 아니라 <b>구글 화면</b>입니다. 브라우저 화면을 스크린에 띄워 놓고 <b>한 단계씩 같이</b> 가세요. 특히 ① 배포 유형에서 톱니바퀴 → 웹 앱 ② 액세스 권한 ‘모든 사용자’ ③ 경고 화면의 ‘고급’ 위치, 이 세 화면에서 손이 올라옵니다. <b>중간 점검(?value=99)에서 전원 OK를 확인한 뒤</b> 다음으로 넘어가세요 — 여기만 통과하면 나머지는 순조롭습니다."},
      {"type": "teacher", "kind": "err", "title": "예상 오류 — 시트가 안 쌓이면 십중팔구 배포 설정",
       "html": "막힘의 최다 원인 두 가지. ① 액세스 권한을 <b>‘모든 사용자’</b>로 안 바꾸고 기본값(나만)으로 둠 — 피코는 로그인을 못 하니 아무 오류 없이 조용히 실패합니다. ② 코드를 고친 뒤 <b>‘새 버전’ 재배포를 안 함</b> — 저장만 하면 옛 코드가 계속 돕니다. “안 쌓여요” 손이 올라오면 피코 코드를 보기 전에 <b>배포 관리 화면부터</b> 함께 여세요. 셋째로 흔한 것: <b>/exec 주소가 아니라 편집기 주소</b>를 복사한 경우, 넷째: <b>학교 워크스페이스 계정</b>이라 ‘모든 사용자’ 옵션 자체가 없는 경우입니다."},
      {"type": "teacher", "kind": "theory", "title": "이론 심화 — ‘모든 사용자’의 진짜 뜻 (보안 이야기)",
       "html": "‘모든 사용자’ 배포는 <b>URL이 곧 열쇠</b>라는 뜻입니다 — 주소를 아는 사람은 누구나 이 웹앱을 호출해 줄을 추가할 수 있어요. 그래서 웹앱 URL을 공개 게시판에 올리지 않게 안내하세요. 단, 우리가 만든 웹앱은 <b>‘한 줄 추가’만</b> 할 수 있고 기존 데이터를 읽거나 지우지는 못합니다 — <b>권한을 필요한 만큼만 좁게 여는 설계</b>(최소 권한 원칙) 자체가 좋은 보안 수업 소재예요. “왜 읽기 기능은 안 만들었을까?”를 물어보면 토론이 됩니다."},
    ]},
    {"title": "2단계 · 피코 연결 — 1분마다 자동 기록", "items": [
      {"type": "callout", "kind": "info", "title": "먼저 — 와이파이 정보 파일 (wifi_config.py)",
       "html": "이 코드는 와이파이 정보를 <code>wifi_config.py</code>에서 불러옵니다. <b>1장에서 이미 만들었다면 그대로</b> 쓰면 돼요. 없다면 main.py와 같은 위치에 새로 만들어 두 줄만 적어 저장하세요.<br><br><code>WIFI_SSID = \"우리_와이파이_이름\"</code><br><code>WIFI_PASSWORD = \"비밀번호\"</code><br><br>(피코는 <b>2.4GHz</b> 와이파이만 됩니다.)"},
      {"type": "step_head", "html": "<b>Step 1.</b> AI에게 이렇게 설명해 보세요. 하드웨어(3장 그대로: MQ-2 → A0)는 바뀐 게 없고, ‘보내는 곳’만 새로 생겼어요."},
      {"type": "prompt", "label": "① AI에게 이렇게 설명하세요 (그대로 복사)", "text":
"라즈베리파이 피코 2 W에서 돌아가는 마이크로파이썬(MicroPython) 코드를 만들어줘. 센서값을 구글 시트에 자동 기록하는 장치야.\n- 가스센서(MQ-2)를 아날로그 입력인 26번 핀으로 읽어, 60초마다 구글 시트에 한 줄씩 기록하고 싶어.\n- 값이 출렁이지 않게 여러 번 읽어 평균을 낸 값을 보내줘.\n- 기록 방법: 구글 앱스 스크립트(Apps Script)로 배포한 웹 앱 주소('/exec'로 끝나는 전체 주소) 뒤에 '?value=측정값'을 붙여 요청을 보내는 방식이야.\n- 외부 라이브러리는 설치하지 말고 피코 기본 내장 기능(socket, ssl)만 써. 보안 인증서 확인은 건너뛰어도 되고, 구글이 다른 주소로 한 번 건너뛰게 하면(리다이렉트) 그것까지 따라가서 마무리해줘.\n- 와이파이 정보는 설정 파일(wifi_config.py)에서 불러오고, 웹 앱 주소와 보내는 주기는 코드 맨 위에 둬.\n- 복사해서 바로 돌아가는 완결형 main.py 전체를 한 번에 줘."},
      {"type": "step_head", "html": "<b>Step 2.</b> 직접 만들지 않아도, 아래 <b>완성본</b>을 쓰면 됩니다. 1단계의 <b>주소 상자에 붙여넣었다면 코드에 이미 내 주소가 들어가 있어요</b> — 펼쳐서 복사만 하면 끝! (상자를 안 썼다면 코드 위쪽 <code>WEB_APP_URL = \"…\"</code> 줄의 <b>따옴표 안 주소만</b> 직접 바꾸세요. 양쪽 따옴표 <code>\"</code>는 지우지 말고요.)"},
      {"type": "code", "label": "② 전체 코드 · 센서값 → 구글 시트 (main.py)", "lang": "python", "file": "snippets/ch6_sheets.py", "fold": True},
      {"type": "callout", "kind": "tip", "title": "잘 되는지 확인하는 법",
       "html": "코드를 실행한 채 <b>구글 시트를 열어 두세요.</b> 1분마다 줄이 하나씩 <b>스르륵 늘어나면</b> 성공! Thonny 아래 <b>셸(Shell) 칸</b>에 <code>시트로 보냄: 1234</code> 같은 메시지가 1분마다 찍혀도 잘 가는 거예요. 안 되면 아래 ‘자주 막히는 곳’으로."},
      {"type": "callout", "kind": "key", "title": "둘은 ‘value’라는 이름으로 짝이에요",
       "html": "피코는 주소 뒤에 <code>?value=1234</code>처럼 값을 붙여 보내고, Apps Script(1단계 코드)는 그 <code>value</code>를 꺼내 시트 ‘값’ 칸에 적습니다. <b>양쪽 이름이 같아서</b> 짝이 맞는 거예요. 나중에 온도 등 값을 하나 더 보내고 싶으면 양쪽에 같은 이름을 하나 더 늘리면 됩니다."},
      {"type": "callout", "kind": "info", "title": "왜 딱 60초마다 안 와요?",
       "html": "<code>INTERVAL</code>은 ‘<b>쉬는 시간</b>’만 정해요. 한 바퀴에는 <b>쉬는 시간 + 인터넷으로 보내는 시간</b>이 같이 들어가고, 전송 시간이 매번 조금씩 달라서 실제 간격은 설정값보다 <b>살짝 길고 들쭉날쭉</b>합니다. ‘정확한 초’보다 ‘꾸준히 기록’이 목적이라 괜찮아요."},
      {"type": "step_head", "html": "<b>Step 3.</b> 1분마다 줄이 쌓이는 걸 확인했다면, 같은 대화에서 <b>③으로 더 똑똑하게</b> 만들어 봐요."},
      {"type": "improve", "label": "③ 프롬프트 개선 — 기록을 더 똑똑하게 (이어서 복사)", "text":
"방금 만든 구글 시트 기록 코드를 이어서 개선해줘.\n- 평소에는 5분마다 보내다가, 직전 값보다 크게 튀면(예: 1.5배 이상) 즉시 보내게 해줘. 조용할 땐 데이터를 아끼고, 사건이 나면 놓치지 않게.\n- 16번 핀의 열 칸 LED 바(WS2813, 타이밍 값 네 개 280, 515, 515, 745 지정 필수)로 전송 순간에 초록 불이 한 번 반짝이게 해줘. 보내는 게 눈에 보이게.\n- 와이파이가 잠깐 끊겨도 프로그램이 죽지 않고, 다시 연결해서 계속 기록하게 해줘.\n- 복사해서 바로 돌아가는 완결형 main.py 전체를 한 번에 줘."},
    ]},
    {"title": "밤새 기록하기 — 시간이 데이터를 만든다", "items": [
      {"type": "text", "html": "이 장의 진짜 실험은 <b>수업이 끝난 뒤</b> 시작됩니다. 우리가 집에 간 사이에도 피코는 1분마다 꼬박꼬박 기록해요 — 내일 아침, <b>수백 줄의 데이터</b>가 우리를 기다립니다."},
      {"type": "steps", "items": [
        {"t": "main.py로 저장", "d": "코드를 피코에 <b>main.py</b> 이름으로 저장하세요(0장 참고). 그래야 컴퓨터 없이 <b>전원만 꽂아도</b> 자동 실행됩니다."},
        {"t": "전원 확보", "d": "USB 어댑터(휴대폰 충전기면 충분)를 교실 콘센트에 꽂고 피코를 연결합니다. 보조배터리도 되지만 밤새 버티는지는 용량에 달렸어요."},
        {"t": "떠나기 전 확인", "d": "시트에 줄이 늘어나는 걸 <b>확인하고</b> 자리를 떠나세요. ‘아마 되겠지’는 다음 날 아침 빈 시트로 돌아옵니다. 중간 점검 때 넣은 <b>테스트 줄(99)은 지우고</b> 시작하면 내일 통계가 깨끗해요."},
        {"t": "다음 날 아침", "d": "시트를 열어 밤새 쌓인 데이터를 확인! 이제 아래 ‘탐구하기’로 넘어갑니다."},
      ]},
      {"type": "callout", "kind": "warn", "title": "학교 와이파이가 밤에 꺼진다면",
       "html": "일부 학교는 야간에 와이파이를 끄거나 기기 간 통신을 차단해요. 그럴 땐 <b>대안 두 가지</b> — ① 수업 중 <b>점심시간 2~3시간</b>만 기록해도 탐구는 충분히 됩니다. ② 데이터 무제한 폰이 있다면 <b>핫스팟을 켜 둔 채</b> 두는 방법도 있어요(배터리·요금 확인!). 목적은 ‘밤샘’이 아니라 <b>‘내가 안 보는 시간의 데이터’</b>입니다."},
      {"type": "teacher", "kind": "say", "title": "진행 멘트 — 연수/수업 차시 배치 팁",
       "html": "이 장은 <b>하루의 마지막 차시</b>에 두는 게 가장 좋습니다. “피코는 밤새 일합니다. 내일 아침에 같이 열어 봐요”로 끝내고, <b>다음 날 첫 10분</b>을 ‘밤새 데이터 열어 보기’로 시작하세요 — 리캡이 복습이 아니라 <b>개봉식</b>이 됩니다. 교실 전원·야간 와이파이는 <b>전날 미리</b> 확인해 두시고, 안 되는 환경이면 점심시간 기록으로 계획을 바꿔 안내하세요."},
    ]},
    {"title": "쌓인 데이터로 탐구하기 — 이 장의 본체", "items": [
      {"type": "text", "html": "기록은 수단이고 <b>탐구가 목적</b>이에요. 시트에 쌓인 수백 줄은 그냥 보면 숫자 더미지만, 그래프로 바꾸는 순간 <b>이야기</b>가 됩니다."},
      {"type": "steps", "items": [
        {"t": "차트 그리기", "d": "시각·값 두 열을 드래그로 선택 → 메뉴 <b>삽입 → 차트</b>. 차트 종류를 <b>라인(선) 차트</b>로 바꾸면 시간에 따른 곡선이 나타나요."},
        {"t": "위험 구간 색칠", "d": "값 열을 선택 → <b>서식 → 조건부 서식</b> → ‘다음보다 큼’에 3장에서 정한 <b>WARNING 값</b>을 넣고 배경을 노랑으로. 위험 시간대가 시트에서 한눈에 보여요."},
        {"t": "통계 한 줄", "d": "빈 칸에 <code>=MAX(B2:B)</code>, <code>=MIN(B2:B)</code>, <code>=AVERAGE(B2:B)</code>를 넣어 밤새 최고·최저·평균을 구합니다."},
      ]},
      {"type": "ideas", "items": [
        {"t": "🌙 밤새 곡선 읽기", "d": "언제 가장 깨끗했나? 아무도 없는데 값이 <b>튄 시각</b>이 있다면 — 무슨 일이 있었을까? (난방 가동? 청소?)"},
        {"t": "🚪 등교 순간 찾기", "d": "아침 그래프에서 <b>사람이 들어온 시각</b>을 값의 변화만으로 추리해 보세요. 실제 등교 시간과 맞나요?"},
        {"t": "💨 환기 실험", "d": "창문을 10분 열었다 닫고, 그래프에서 <b>환기 전-중-후</b>를 비교하세요. 몇 분 만에 원래대로 돌아오나요?"},
        {"t": "🏫 자리 비교 (모둠)", "d": "피코 두 대를 <b>창가 vs 복도쪽</b>에 두고, <b>피코마다 시트를 하나씩</b> 새로 만들어(1단계 반복) 각자의 주소로 기록 → 두 그래프를 나란히 놓고 어느 자리가 공기가 좋은지 데이터로 판정."},
      ]},
      {"type": "callout", "kind": "key", "title": "마무리는 ‘결론 한 줄’로",
       "html": "탐구의 끝은 그래프가 아니라 <b>문장</b>입니다. “우리 교실은 <b>___시쯤</b> 공기가 가장 나쁘고, <b>___시에 환기</b>하는 게 좋다” — 데이터를 근거로 이 문장의 빈칸을 채워 보세요. 숫자가 <b>의사결정</b>으로 바뀌는 순간이에요."},
      {"type": "teacher", "kind": "ask", "title": "발문 — 그래프 앞에서",
       "html": "“이 그래프에서 <b>확실히 말할 수 있는 것</b>과 <b>추측인 것</b>을 나눠 볼까요?” — ‘새벽 3시에 값이 낮았다’(사실)와 ‘그건 아무도 없어서다’(추측)를 구분하는 훈련입니다. 이어서 “추측을 확인하려면 <b>다음엔 뭘 기록</b>해야 할까요?”를 물으면, 변인 통제와 추가 실험 설계로 자연스럽게 이어집니다."},
    ]},
    {"title": "자주 하는 실수", "items": [
      {"type": "mistakes", "items": [
        {"sym": "브라우저 테스트(?value=99)부터 안 됨", "cause": "배포 설정 문제 — 피코 이전 단계.", "fix": "1단계로 돌아가 액세스 권한 <b>‘모든 사용자’</b>, 주소가 <b>/exec</b>로 끝나는지부터 확인하세요. 여기가 안 되면 피코는 절대 안 됩니다."},
        {"sym": "브라우저는 OK인데 피코만 실패", "cause": "와이파이 문제이거나 주소를 잘못 붙여넣음.", "fix": "셸의 와이파이 메시지를 확인하고(2.4GHz만!), <code>WEB_APP_URL</code>에 <b>/exec 전체 주소</b>가 따옴표 안에 정확히 들어갔는지 보세요. 주소 앞뒤가 잘리는 실수가 흔해요."},
        {"sym": "시트에 아무것도 안 쌓임", "cause": "웹앱 액세스 권한이 ‘모든 사용자’가 아님.", "fix": "배포를 <b>모든 사용자</b>로 다시 하세요. 코드 수정 후엔 <b>배포 관리 → 편집 → 새 버전</b>으로 재배포해야 반영됩니다."},
        {"sym": "ImportError: no module named 'wifi_config'", "cause": "<code>wifi_config.py</code>가 피코에 없음.", "fix": "위 2단계 안내대로 <code>wifi_config.py</code>를 main.py와 같은 위치에 만들고 와이파이 두 줄을 적으세요."},
        {"sym": "셸에 ‘실패’라고 떠요", "cause": "잠깐 인터넷이 끊겼을 때 그래요.", "fix": "한두 번은 괜찮아요 — 다음 차례에 다시 보냅니다. 계속 그러면 <code>INTERVAL</code>을 늘려 보세요."},
        {"sym": "시각이 한국시간과 다름", "cause": "Apps Script 프로젝트 또는 시트의 시간대가 기본(미국).", "fix": "Apps Script <b>프로젝트 설정(⚙️) → 시간대 → 서울</b>, 그리고 시트 쪽 <b>파일 → 설정 → 시간대</b>도 서울인지 확인하세요. 이미 쌓인 줄의 시각은 안 바뀌니 초반에 확인!"},
        {"sym": "아침에 보니 기록이 중간에 끊김", "cause": "전원이 뽑혔거나 야간에 와이파이가 꺼짐.", "fix": "콘센트·어댑터를 확인하고, 학교망 야간 차단이면 ‘점심시간 기록’으로 바꾸세요. <b>끊긴 시각 자체도 데이터</b>예요 — 언제 끊겼는지 그래프로 찾아보세요."},
      ]},
    ]},
    {"title": "스스로 점검하기", "items": [
      {"type": "check", "items": [
        {"q": "피코가 구글 로그인 없이 시트에 쓸 수 있는 이유는?", "a": "Apps Script 웹앱을 <b>‘모든 사용자’로 배포</b>해, URL만 알면 누구나(피코도) 호출할 수 있게 했기 때문. 로그인은 웹앱이 대신 해 줍니다."},
        {"q": "이번 장에서 데이터가 흐르는 방향은 5장과 어떻게 다른가요?", "a": "5장은 피코가 인터넷에서 <b>받아 왔고</b>(Open-Meteo), 이번 장은 피코가 인터넷으로 <b>보냅니다</b>(시트). 둘 다 피코가 클라이언트인 건 같아요."},
        {"q": "피코를 붙이기 전에 웹앱만 따로 시험하는 방법은?", "a": "브라우저에서 <code>웹앱주소?value=99</code>를 열어 <b>OK</b>와 시트의 새 줄을 확인합니다. ‘반 만들고 반 시험’이 디버깅의 기본기예요."},
        {"q": "보내는 간격을 바꾸려면?", "a": "코드 맨 위 <code>INTERVAL</code> 숫자를 바꾸면 됩니다. 60이면 1분, 300이면 5분마다."},
        {"q": "‘실시간으로 보기’는 못 하고 ‘기록’만 할 수 있는 질문의 예는?", "a": "‘어젯밤 언제 가장 나빴나’, ‘환기하면 몇 분 만에 돌아오나’, ‘창가와 복도 중 어디가 좋나’ — 모두 <b>시간·비교</b>가 필요한 질문들입니다."},
      ]},
    ]},
  ],
},
# ----------------------------------------------------------------- CH7 (자유 프로젝트)
{
  "id": "ch7", "num": "07", "title": "자유 프로젝트", "accent": "#8B5CF6",
  "subtitle": "지금까지 배운 LED·센서·웹·날씨 API·시트 기록을 조합해, 나만의 작품을 바이브코딩으로 완성합니다.",
  "goals": [
    "여러 기능을 조합해 새 작품을 기획할 수 있다",
    "AI에게 명확하게 설명하고, 받은 코드를 점검할 수 있다",
  ],
  "why": "도구는 다 익혔어요. 이제 <b>‘무엇을 만들까’</b>가 남았습니다. 작은 아이디어 하나면 충분해요. 아래 아이디어와 프롬프트 틀을 출발점으로 삼아, 우리 교실·우리 집에 쓸모 있는 작품을 만들어 보세요.",
  "sections": [
    {"title": "아이디어 모음", "items": [
      {"type": "ideas", "items": [
        {"t": "🌧️ 우산 알리미", "d": "날씨 시계(5장)에서 오늘 강수확률이 60% 넘는 시간대가 있으면, 현관 LED를 파랑으로 깜빡여 ‘우산 챙겨!’"},
        {"t": "🌬️ 스마트 환기등", "d": "가스센서(3·4장) 값이 WARNING을 넘으면 LED를 노랑→빨강으로, 웹에 ‘환기하세요’ 알림."},
        {"t": "📶 와이파이 약한 자리 찾기", "d": "RSSI 대시보드(1장)를 들고 다니며 집에서 신호가 약한 곳을 LED 게이지로 탐색."},
        {"t": "🌡️ 오늘 날씨 무드등", "d": "강수확률 대신 기온을 받아(Open-Meteo) 더우면 빨강, 추우면 파랑으로 방 전체 분위기 표현."},
        {"t": "🔭 과학 데이터 작품", "d": "<b>부록 A</b> 갤러리에서 API 하나 골라(지진·낮 길이·CO₂…) 값을 10칸 LED 게이지로. 각 페이지에 ‘AI에게 설명’ 프롬프트가 있어요."},
        {"t": "📒 일주일 공기질 리포트", "d": "기록 노트(6장)를 일주일 돌려 요일별 패턴을 차트로 비교하고, 데이터를 근거로 ‘우리 반 환기 규칙’을 제안하는 탐구 보고서."},
      ]},
      {"type": "teacher", "kind": "say", "title": "진행 팁 — 주제 정하기에 10분 이상 쓰지 않기",
       "html": "자유 프로젝트에서 가장 오래 막히는 건 코딩이 아니라 <b>‘뭘 만들지’</b>입니다. 시작할 때 “<b>10분 안에</b> 주제를 정합니다. 못 정하면 위 아이디어 5개 중 하나를 골라 한 가지만 바꿔 보세요”라고 선을 그어 주세요. 시간 배분은 <b>기획 10분 · 제작 60분 · 발표 준비 10분</b>이 기본이고, 제작 30분쯤에 “지금 LED에 뭐라도 켜진 사람?”으로 한 번 점검하면 마지막에 몰리지 않습니다."},
    ]},
    {"title": "AI에게 잘 설명하는 틀", "items": [
      {"type": "text", "html": "막연히 ‘만들어 줘’보다, <b>① 지금 상태 → ② 추가할 동작 → ③ 제약(핀·timing·갱신주기)</b>을 함께 설명하면 훨씬 정확한 코드를 받습니다."},
      {"type": "prompt", "label": "AI에게 이렇게 설명하세요 — 틀 (복사해서 채우세요)", "text":
"[맥락] 내 피코는 지금 ____ 를 하고 있어. (예: 오늘 강수확률을 열 칸 LED에 색으로 표시)\n[하드웨어] 열 칸짜리 LED 바(WS2813)는 16번 핀, 만들 때 타이밍 값 네 개(280, 515, 515, 745) 지정 필요 / 가스센서(MQ-2)는 아날로그 26번 핀 / 와이파이 정보는 설정 파일(wifi_config.py)에서 불러옴.\n[작업] 여기에 ____ 기능을 더해줘. (예: 강수확률이 60%를 넘으면 LED 깜빡이기)\n[제약] 외부 라이브러리는 최소로, 데이터 갱신은 ____초마다.\n[출력] 복사해서 바로 돌아가는 완결형 main.py 전체를 한 번에 줘.\n받은 코드에서 핀 번호와 타이밍 값이 내 것과 같은지 확인할게."},
      {"type": "callout", "kind": "tip", "title": "점검 체크리스트",
       "html": "받은 코드를 올리기 전에: ① <code>timing=(280,515,515,745)</code> 있는지 ② 핀 번호(16 / 26)와 포트(D16 / A0) 맞는지 ③ 무한 반복 속 <code>sleep</code>으로 쉬어 주는지 ④ 와이파이/네트워크 요청이 과하지 않은지."},
    ]},
    {"title": "마무리", "items": [
      {"type": "teacher", "kind": "ask", "title": "발문 — 발표에서는 코드가 아니라 프롬프트를 묻기",
       "html": "발표 때 “코드를 설명해 보세요” 대신 <b>“AI에게 뭐라고 설명했나요? 왜 그렇게 말했나요?”</b>를 물어보세요. 프롬프트가 곧 설계도라서, 이 질문에 답하다 보면 핀 번호·timing·갱신 주기 같은 제약을 어떻게 챙겼는지가 저절로 드러납니다. “처음 받은 코드에서 뭘 고쳐 달라고 했나요?”를 이어 물으면 점검 습관까지 확인할 수 있어요."},
      {"type": "text", "html": "여기까지 왔다면, 여러분은 <b>센서로 데이터를 모으고 · 인터넷의 데이터를 주고받고 · LED와 웹으로 표현하고 · 기록으로 남겨 탐구하는</b> 데이터 기반 탐구의 한 사이클을 전부 경험한 거예요. 도구는 거들 뿐, 진짜 중요한 건 ‘무엇을, 왜 만드는가’입니다. 멋진 작품을 만들어 보세요! 🎉"},
    ]},
  ],
},
# ----------------------------------------------------------------- 부록 A
{
  "id": "apx", "num": "A", "title": "부록 · 오픈 API 한눈에 보기", "accent": "#0EA5A0",
  "subtitle": "프로젝트에 쓸 만한 과목별 오픈 API 카탈로그예요. 각 API가 어떤 데이터를 주고 무엇을 탐구할 수 있는지 보고, 바로 살아 있는 대시보드로 들어가 보세요.",
  "why": "5장에서 API로 데이터를 받아 표현하는 흐름을 익혔죠. 이 부록은 과목별 오픈 API를 <b>한눈에 정리한 카탈로그</b>예요 — 각 API가 <b>어떤 데이터</b>를 주고 <b>어떤 탐구</b>를 할 수 있는지, 그리고 <b>브라우저에서 바로 그려 보는 라이브 대시보드</b>로 연결됩니다. 피코로 직접 받아오려면 5장 ‘날씨 시계’에서 쓴 <code>socket</code>+<code>ssl</code> 방식을 그대로 응용하면 돼요. (API는 2026년 기준 응답 확인)",
  "sections": [
    {"title": "이 부록 쓰는 법", "items": [
      {"type": "callout", "kind": "key", "title": "🌐 라이브 대시보드로 데이터를 ‘직접’ 만나 보기",
       "html": "각 API 카드의 <b>‘라이브 대시보드 열기’</b>를 누르면, 브라우저에서 <b>지금 데이터를 받아 지도·그래프로 그려 주는 페이지</b>가 열려요(설치·피코 없이 클릭만). 위치·물질·종을 바꿔 가며 탐구하고, 페이지마다 ‘🔎 탐구 질문’도 있습니다."},
      {"type": "linkbtn", "href": "dashboards/index.html", "label": "오픈 API 라이브 대시보드 갤러리 열기 (10종 · 5장 날씨 포함)"},
      {"type": "callout", "kind": "info", "title": "국내 적용 여부 한눈에",
       "html": "🇰🇷 국내 OK(일출몰·생물) · 🌍 전 지구라 국내도 포함(대기질·ISS) · 🌐 국적 무관(화학·천문) · 🌎 해외 위주(지진은 국내 드묾 → 기상청 권장). 국내 공식 데이터는 공공데이터포털(키 필요)을 쓰세요."},
      {"type": "teacher", "kind": "say", "title": "진행 팁 — 교과 연계로 소개하기",
       "html": "갤러리 10종을 하나씩 다 보여 주기보다, “<b>내 과목과 닿는 API 하나</b>를 골라 10분 탐구해 보세요”라고 던지는 편이 낫습니다. 지구과학=지진·일출몰, 화학=PubChem, 생물=GBIF, 환경=대기질·CO₂, 물리·에너지=ISS·태양광 — 이렇게 과목별 짝을 한 줄씩만 안내하고, 마무리에 “이 데이터로 수업에서 뭘 시켜 보고 싶은지” 한 사람씩 말하게 하면 자기 수업과 연결된 채 끝납니다."},
    ]},
    {"title": "1) 미세먼지 (대기질) — 환경 🌍", "items": [
      {"type": "text", "html": "<b>📊 어떤 데이터</b> — PM2.5·PM10·오존 등 시간별 대기질(<a class=\"ilink\" href=\"https://open-meteo.com/en/docs/air-quality-api\" target=\"_blank\" rel=\"noopener\">Open-Meteo</a>, 키 불필요).<br><b>🔎 어떤 탐구</b> — 지금 등급(좋음~매우나쁨) 판정 · 하루 중 미세먼지가 높은 시간대 찾기 · 우리 동네와 다른 지역 공기질 비교."},
      {"type": "linkbtn", "href": "dashboards/airquality.html", "label": "이 API 라이브 대시보드 열기"},
    ]},
    {"title": "2) 전 세계 지진 — 지구과학 🌎", "items": [
      {"type": "text", "html": "<b>📊 어떤 데이터</b> — 실시간 지진의 규모·위치·깊이·시각(<a class=\"ilink\" href=\"https://earthquake.usgs.gov\" target=\"_blank\" rel=\"noopener\">USGS</a>, 키 불필요).<br><b>🔎 어떤 탐구</b> — 세계 지도에 찍어 ‘불의 고리’ 패턴 관찰 · 규모별 발생 수 세기 · 최대 규모 추적. (국내 지진은 드물어 기상청 권장)"},
      {"type": "linkbtn", "href": "dashboards/earthquake.html", "label": "이 API 라이브 대시보드 열기"},
    ]},
    {"title": "3) 국제우주정거장 ISS — 천문·물리 🌍", "items": [
      {"type": "text", "html": "<b>📊 어떤 데이터</b> — ISS의 실시간 위·경도·고도·속도(<a class=\"ilink\" href=\"https://wheretheiss.at\" target=\"_blank\" rel=\"noopener\">wheretheiss</a>, 키 불필요).<br><b>🔎 어떤 탐구</b> — 지금 어느 나라 상공인지 지도로 추적 · 내 위치와의 거리 · 궤도가 물결치는 이유(궤도 경사) 탐구."},
      {"type": "linkbtn", "href": "dashboards/iss.html", "label": "이 API 라이브 대시보드 열기"},
    ]},
    {"title": "4) 일출·일몰·낮 길이 — 천문·지구과학 🇰🇷", "items": [
      {"type": "text", "html": "<b>📊 어떤 데이터</b> — 일출·일몰·남중시각·낮 길이(<a class=\"ilink\" href=\"https://sunrise-sunset.org\" target=\"_blank\" rel=\"noopener\">sunrise-sunset</a>, 키 불필요).<br><b>🔎 어떤 탐구</b> — 계절별 낮 길이 변화 · 위도를 바꿔 적도 vs 극지방(백야·극야) 비교."},
      {"type": "linkbtn", "href": "dashboards/sunrise.html", "label": "이 API 라이브 대시보드 열기"},
    ]},
    {"title": "5) 물질 정보 — 화학 🌐", "items": [
      {"type": "text", "html": "<b>📊 어떤 데이터</b> — 물질 이름 → 화학식·분자량·2D/3D 구조(<a class=\"ilink\" href=\"https://pubchem.ncbi.nlm.nih.gov\" target=\"_blank\" rel=\"noopener\">PubChem</a>, 키 불필요).<br><b>🔎 어떤 탐구</b> — 여러 물질 분자량 비교 · 3D 구조를 돌려 보며 모양 이해 · 화학식만 보고 물질 맞히기."},
      {"type": "linkbtn", "href": "dashboards/pubchem.html", "label": "이 API 라이브 대시보드 열기"},
    ]},
    {"title": "6) 우리나라 생물 관찰 — 생물 🇰🇷", "items": [
      {"type": "text", "html": "<b>📊 어떤 데이터</b> — 생물 종별 관찰 기록·위치·날짜(<a class=\"ilink\" href=\"https://www.gbif.org\" target=\"_blank\" rel=\"noopener\">GBIF</a>, 한국 약 880만 건, 키 불필요).<br><b>🔎 어떤 탐구</b> — 관찰 지점을 지도에 찍어 분포(도시 vs 산) · 월별(계절) 분포 · 철새 vs 텃새 비교."},
      {"type": "linkbtn", "href": "dashboards/gbif.html", "label": "이 API 라이브 대시보드 열기"},
    ]},
    {"title": "7) NASA 우주 데이터 — 천문 🌐 (키 필요)", "items": [
      {"type": "text", "html": "<b>📊 어떤 데이터</b> — 오늘의 천문사진(APOD)과 오늘 지구 곁을 지나는 소행성(NeoWs, NASA).<br><b>🔎 어떤 탐구</b> — 매일 우주사진 감상 · 오늘 가까운 소행성의 거리(달까지 거리의 몇 배)·크기·위험 여부 비교.<br><span style='color:#a55'>※ NASA만 API 키가 필요해요. 대시보드는 공용 <code>DEMO_KEY</code>로 동작하고(횟수 제한), 막히면 <a class=\"ilink\" href=\"https://api.nasa.gov\" target=\"_blank\" rel=\"noopener\">api.nasa.gov</a>에서 무료 키를 받아 넣으면 돼요.</span>"},
      {"type": "linkbtn", "href": "dashboards/nasa.html", "label": "이 API 라이브 대시보드 열기"},
    ]},
    {"title": "8) 태양·바람 에너지 — 에너지·물리·지구 🌍", "items": [
      {"type": "text", "html": "<b>📊 어떤 데이터</b> — 지역별 월평균 일사량·풍속(<a class=\"ilink\" href=\"https://power.larc.nasa.gov\" target=\"_blank\" rel=\"noopener\">NASA POWER</a>, 키 불필요).<br><b>🔎 어떤 탐구</b> — 우리 지역 태양광 발전 잠재력 · 적도·사막·극지방 일사량 비교 · 계절(여름↑ 겨울↓) 차이."},
      {"type": "linkbtn", "href": "dashboards/energy.html", "label": "이 API 라이브 대시보드 열기"},
    ]},
    {"title": "10) 나라별 CO₂·에너지 — 환경·에너지 🌍", "items": [
      {"type": "text", "html": "<b>📊 어떤 데이터</b> — 나라별 1인당 CO₂ 배출·재생에너지 비중 등(<a class=\"ilink\" href=\"https://data.worldbank.org\" target=\"_blank\" rel=\"noopener\">World Bank</a>, 키 불필요).<br><b>🔎 어떤 탐구</b> — 한국 vs 주요국 비교 · 세계지도/버블로 대륙별 패턴 · 우리나라 순위 확인."},
      {"type": "linkbtn", "href": "dashboards/worldbank.html", "label": "이 API 라이브 대시보드 열기"},
    ]},
  ],
},
# ----------------------------------------------------------------- 부록 C (용어 사전)
{
  "id": "apxc", "num": "C", "title": "부록 · 용어 사전", "accent": "#9A8B6A",
  "subtitle": "프롬프트와 본문에서 만나는 용어를 한 줄씩 정리했어요. AI에게 설명할 때 이 낱말을 그대로 쓰면 훨씬 정확한 코드를 받습니다.",
  "why": "프롬프트에는 코드를 쓰지 않아요. 대신 <b>정확한 낱말</b>을 씁니다. ‘그거’ 대신 ‘타이밍 값’, ‘저장하는 파일’ 대신 ‘wifi_config.py’라고 말하면 AI가 헤매지 않아요. 뜻이 가물가물할 때 이 페이지로 돌아오세요.",
  "sections": [
    {"title": "기본 도구", "items": [
      {"type": "teacher", "kind": "say", "title": "활용 팁 — 수업 내내 옆 탭에 열어 두게 하기",
       "html": "이 페이지는 읽고 끝내는 자료가 아니라 <b>수업 내내 옆 탭에 띄워 두는 사전</b>입니다. 첫 시간에 “브라우저 탭 하나는 항상 용어 사전”을 규칙으로 정하고, 수업 중 ‘타이밍 값’·‘임계값’ 같은 낱말이 나올 때마다 “사전에서 찾아 옆 사람에게 한 줄로 설명해 보세요”를 시키세요. 프롬프트에 정확한 낱말을 쓰는 습관이 곧 바이브코딩 실력이 됩니다."},
      {"type": "concept", "items": [
        {"t": "마이크로파이썬 (MicroPython)", "d": "피코 같은 작은 컴퓨터에서 돌아가도록 만든 파이썬. 펌웨어를 한 번 설치하면 피코가 파이썬 코드를 알아듣습니다."},
        {"t": "펌웨어 (firmware)", "d": "기기를 켰을 때 가장 먼저 도는 기본 소프트웨어. 컴퓨터의 운영체제에 해당하는 피코의 속살."},
        {"t": "Thonny (토니)", "d": "코드를 쓰고 피코로 보내는 편집기. 아래쪽 셸 칸으로 피코와 대화합니다."},
        {"t": "셸 (Shell)", "d": "코드를 한 줄씩 바로 실행해 보고, 피코가 보낸 메시지를 보여 주는 대화창."},
        {"t": "main.py", "d": "피코에 이 이름으로 저장하면 전원만 넣어도 자동 실행되는 파일."},
        {"t": "wifi_config.py", "d": "와이파이 이름과 비밀번호를 따로 적어 두는 설정 파일. 여러 코드가 함께 씁니다."},
      ]},
    ]},
    {"title": "하드웨어", "items": [
      {"type": "concept", "items": [
        {"t": "핀 (GP 번호)", "d": "피코 다리 하나하나에 붙은 번호. ‘16번 핀’은 GP16을 말해요."},
        {"t": "그로브 포트 (D·A)", "d": "센서 케이블을 딸깍 꽂는 자리. D는 디지털(D16), A는 아날로그(A0)."},
        {"t": "디지털 / 아날로그", "d": "켜짐·꺼짐 두 가지로 나뉘는 신호(디지털)와, 밝기·농도처럼 연속으로 이어지는 신호(아날로그)."},
        {"t": "ADC", "d": "아날로그 신호를 0~65535 사이 숫자로 바꿔 읽어 주는 변환기. 가스센서를 읽을 때 씁니다."},
        {"t": "LED 바 (WS2813)", "d": "색 LED 열 칸이 한 줄로 붙은 부품. 칸마다 다른 색을 켤 수 있어요."},
        {"t": "타이밍 값", "d": "WS2813 LED에게 0과 1을 구분해 주는 신호 길이 네 개(280, 515, 515, 745). 빠뜨리면 색이 깨집니다."},
        {"t": "MQ-2", "d": "공기 중 가스를 감지하는 센서. 가스가 짙을수록 큰 값을 내보냅니다."},
        {"t": "이동 평균", "d": "여러 번 읽어 평균을 내서 값의 출렁임을 줄이는 방법."},
        {"t": "기준값 (임계값)", "d": "안전/주의/위험처럼 상태를 가르는 기준 숫자. 환경마다 달라서 직접 보고 정합니다."},
      ]},
    ]},
    {"title": "인터넷과 데이터", "items": [
      {"type": "concept", "items": [
        {"t": "와이파이 2.4GHz", "d": "피코가 붙을 수 있는 와이파이 종류. 이름이 ‘…5G’로 끝나는 5GHz 전용 망에는 못 붙어요."},
        {"t": "SSID", "d": "와이파이의 이름."},
        {"t": "RSSI · dBm", "d": "신호 세기와 그 단위. 항상 음수이고, 0에 가까울수록(-50) 강하고 멀수록(-85) 약해요."},
        {"t": "웹서버 · 포트", "d": "브라우저의 접속을 기다렸다 화면이나 데이터를 돌려주는 프로그램. 포트는 그 문 번호(웹은 보통 80번)."},
        {"t": "JSON", "d": "데이터를 주고받을 때 쓰는 글자 형식. {\"이름\": 값} 모양으로 생겼어요."},
        {"t": "API", "d": "정해진 양식으로 요청하면 정해진 형식으로 결과를 돌려주는 창구. 관공서 민원 창구와 같은 원리."},
        {"t": "socket · ssl", "d": "피코에 기본 내장된 인터넷 접속 기능과 암호화 기능. 추가 설치 없이 쓸 수 있어요."},
        {"t": "인증서", "d": "서버가 진짜인지 확인하는 신분증. 공개 데이터 수업에서는 확인을 건너뛰어도 안전합니다."},
        {"t": "리다이렉트", "d": "서버가 ‘다른 주소로 가 보세요’ 하고 안내하는 것. 구글 시트에 기록할 때(6장) 만나요."},
        {"t": "로깅", "d": "측정값을 시각과 함께 차곡차곡 저장하는 것(6장). 걸음 수 앱·블랙박스가 다 로깅 장치예요."},
        {"t": "Apps Script", "d": "구글 시트에 딸린 작은 프로그래밍 도구. 우리는 ‘값을 받아 시트에 한 줄 쓰는’ 웹앱을 만들 때 써요(6장)."},
        {"t": "웹 앱 · /exec 주소", "d": "URL을 부르면 실행되는 프로그램. Apps Script로 배포하면 /exec로 끝나는 주소가 생기고, 피코는 이 주소로 값을 보냅니다."},
        {"t": "Chart.js", "d": "브라우저에서 그래프를 그려 주는 도구. 피코는 숫자만 보내고 그림은 브라우저가 그립니다."},
        {"t": "Open-Meteo", "d": "키도 회원가입도 필요 없는 무료 날씨 서비스. 위도·경도만 보내면 예보를 돌려줍니다."},
        {"t": "위도 · 경도", "d": "지구 위 위치를 나타내는 두 숫자. 한국은 위도 33~38, 경도 124~132 범위."},
        {"t": "강수확률", "d": "그 시각·그 지역에 비가 내릴 통계적 가능성(%). 비의 양이 아니라 올지 안 올지의 가능성이에요."},
      ]},
    ]},
  ],
},
]
CHAPTERS[0]["extra"] = ""   # FW_CARD는 0.4 섹션 안에 배치

# ===================================================================
#  히어로 (허브 index.html 전용) — build_ml_site.py의 BRAND 치환이
#  이 문자열과 정확히 일치해야 하므로 내용은 수정 금지
# ===================================================================
HERO_HTML = r'''<header class="hero" id="top">
      <span class="eyebrow">라즈베리파이 피코 2 WH · MicroPython · 바이브코딩</span>
      <h1>데이터로 탐구하는<br>바이브 <span class="pk">피</span>지컬 <span class="pk">코</span>딩 🐣</h1>
      <div class="under"></div>
      <p>센서로 모은 데이터와 인터넷의 공개 데이터(API)를, <b><span class="pico-accent">피코</span></b>와 LED·웹으로 ‘보이게’ 만드는 <b>데이터 기반 탐구 프로젝트</b> 안내서예요. 준비(설치·조립)부터 와이파이·LED·날씨 API·가스센서, 그리고 과목별 오픈 API 부록까지 — 모든 코드를 <b>복사해 바로 실행</b>할 수 있습니다. 🌈</p>
      <div class="stats">
        <div class="stat"><b>/*NCH*/</b>개 챕터</div>
        <div class="stat"><b>/*NCODE*/</b>개 코드 블록</div>
        <div class="stat"><b>/*NPROMPT*/</b>개 AI 프롬프트</div>
      </div>
      <a class="ml-cta" href="ml_site/">
        <span class="ml-cta-emoji">🔊🧠</span>
        <span class="ml-cta-txt"><b>새 확장판 · 소리를 배우고 말하는 피코 (머신러닝)</b>
        <small>마이크로 소리를 모아 k-NN으로 분류하고, LED·MP3 음성으로 말하게 만들어요. 이 책을 끝낸 다음 단계예요.</small></span>
        <span class="ml-cta-go">확장판 열기 →</span>
      </a>
    </header>'''

# ===================================================================
#  렌더러
# ===================================================================
n_code = 0
n_prompt = 0
TEACHER = False   # True면 강사노트(type: teacher) 아이템도 렌더 (teacher.html 빌드용)

def render_item(it, accent):
    global n_code, n_prompt
    t = it["type"]
    if t == "teacher":
        # 강사 전용 노트 — 학생용 빌드에서는 통째로 생략된다.
        # kind: say(진행 멘트) / ask(발문) / theory(이론 심화) / err(예상 오류)
        if not TEACHER:
            return ""
        icons = {"say": "🎙️", "ask": "🙋", "theory": "📚", "err": "🧯"}
        ic = icons.get(it["kind"], "🎙️")
        return (f'<div class="callout {it["kind"]}"><div class="callout-head">{ic} '
                f'{esc(it["title"])}</div><div class="callout-body">{it["html"]}</div></div>')
    if t == "text":
        return f'<p class="prose">{it["html"]}</p>'
    if t == "raw":
        return it["html"]
    if t == "step_head":
        return f'<p class="step-head">{it["html"]}</p>'
    if t == "linkbtn":
        return (f'<a class="linkbtn" href="{esc(it["href"])}" target="_blank" rel="noopener">'
                f'🔗 {esc(it["label"])}</a>')
    if t == "figure_hw":
        return HW_FIGURE
    if t == "callout":
        icons = {"tip": "💡", "warn": "⚠️", "info": "ℹ️", "key": "🔑",
                 "mini": "🎯", "check": "✅"}
        ic = icons.get(it["kind"], "💡")
        return (f'<div class="callout {it["kind"]}"><div class="callout-head">{ic} '
                f'{esc(it["title"])}</div><div class="callout-body">{it["html"]}</div></div>')
    if t == "check_list":
        lis = "".join(f'<li>{g}</li>' for g in it["items"])
        return f'<ul class="check-list">{lis}</ul>'
    if t == "concept":
        rows = "".join(f'<div class="concept"><div class="concept-t">{esc(c["t"])}</div>'
                       f'<div class="concept-d">{c["d"]}</div></div>' for c in it["items"])
        return f'<div class="concept-grid">{rows}</div>'
    if t == "ideas":
        rows = "".join(f'<div class="idea"><div class="idea-t">{c["t"]}</div>'
                       f'<div class="idea-d">{c["d"]}</div></div>' for c in it["items"])
        return f'<div class="idea-grid">{rows}</div>'
    if t == "steps":
        lis = "".join(f'<li><b>{esc(s["t"])}</b><span>{s["d"]}</span></li>' for s in it["items"])
        return f'<ol class="steps">{lis}</ol>'
    if t == "mistakes":
        rows = ""
        for m in it["items"]:
            rows += (f'<div class="mistake"><div class="m-sym">❌ {esc(m["sym"])}</div>'
                     f'<div class="m-row"><span class="m-tag">원인</span>{m["cause"]}</div>'
                     f'<div class="m-row"><span class="m-tag fix">해결</span>{m["fix"]}</div></div>')
        return f'<div class="mistakes">{rows}</div>'
    if t == "check":
        rows = ""
        for c in it["items"]:
            rows += (f'<details class="qa"><summary>{c["q"]}</summary>'
                     f'<div class="qa-a">{c["a"]}</div></details>')
        return f'<div class="checks">{rows}</div>'
    if t == "dig":
        return (f'<details class="dig"><summary>🔬 더 알아보기 — {esc(it["title"])}</summary>'
                f'<div class="dig-body">{it["html"]}</div></details>')
    if t == "code":
        n_code += 1
        raw = it["code"] if "code" in it else load(it["file"])
        raw = raw.rstrip("\n")
        code = esc(raw)
        tag = it["lang"].upper()
        label = esc(it["label"]) if it.get("label") else "코드"
        block = (f'<div class="block code-block">'
                 f'<div class="block-head"><span class="block-label">{label}</span>'
                 f'<span class="lang-tag">{tag}</span>'
                 f'<button class="copy-btn" aria-label="복사">복사</button></div>'
                 f'<pre><code class="language-{it["lang"]}">{code}</code></pre></div>')
        if it.get("fold"):
            lines = raw.count("\n") + 1
            return (f'<details class="codefold"><summary>{label} '
                    f'<span class="fold-hint">· {lines}줄 · 펼쳐서 복사</span></summary>'
                    f'{block}</details>')
        return block
    if t == "prompt":
        n_prompt += 1
        return (f'<div class="block prompt-block">'
                f'<div class="block-head"><span class="prompt-ico">🤖</span>'
                f'<span class="block-label">{esc(it["label"])}</span>'
                f'<button class="copy-btn" aria-label="복사">복사</button></div>'
                f'<div class="prompt-body">{esc(it["text"])}</div></div>')
    if t == "improve":
        # ③ 프롬프트 개선 — ①프롬프트 → ②코드 → ③개선 3박자의 마무리
        n_prompt += 1
        label = esc(it.get("label", "③ 프롬프트 개선 (이어서 붙여넣기)"))
        return (f'<div class="block prompt-block improve-block">'
                f'<div class="block-head"><span class="prompt-ico">✨</span>'
                f'<span class="block-label">{label}</span>'
                f'<button class="copy-btn" aria-label="복사">복사</button></div>'
                f'<div class="prompt-body">{esc(it["text"])}</div></div>')
    return ""

def _plan_table(rows):
    """운영 계획 시간표 한 개 — rows: (시간, 내용, 비고)
       웹은 html을, 인쇄(docx) 빌더는 rows를 그대로 읽어 표로 만든다."""
    tr = "".join(f'<tr><td class="t">{t}</td><td>{c}</td><td class="note">{n}</td></tr>'
                 for t, c, n in rows)
    html = ('<div style="overflow-x:auto"><table class="plan-table">'
            '<tr><th>시간</th><th>내용</th><th>비고</th></tr>' + tr + '</table></div>')
    return {"type": "raw", "html": html, "rows": rows}

# 강사용 전용 페이지 — CHAPTERS에 넣지 않고 build(teacher=True)에서만 렌더한다.
PLAN_PAGE = {
  "id": "plan", "num": "🗓 운영", "title": "20시간 연수 운영 계획 (4일 × 5시간)", "accent": "#D97706",
  "subtitle": "본편 0~7장 + ML 확장판(소리·동작)을 4일 20시간에 담는 표준 진행안입니다. 하루 300분 기준이며, 블록 사이 10분 휴식을 끼워 운영하세요.",
  "goals": [
    "하루 단위 목표와 시간 배분을 한눈에 파악한다",
    "6장 ‘밤새 기록’을 차시 장치로 활용하는 법을 안다",
    "밀렸을 때 어디를 압축할지(버퍼) 미리 안다",
  ],
  "why": "전체 서사는 <b>출력(LED) → 입력(센서) → 인터넷(받기·보내기) → 머신러닝 → 종합</b>입니다. 설계의 축은 두 가지 — ① 매일 <b>클리프행어</b>로 끝낸다(2장 작품 예고, 6장 밤새 기록, IMU 예고), ② 6장 기록을 <b>2일차 마지막</b>에 두어 3일차 아침이 복습이 아니라 <b>‘데이터 개봉식’</b>이 되게 한다.",
  "sections": [
    {"title": "한눈에 보기", "items": [
      {"type": "concept", "items": [
        {"t": "1일차 · 첫 만남", "d": "세팅 → 첫 IoT(와이파이) → LED 기본기. <b>Ch0~Ch2 전반</b>"},
        {"t": "2일차 · 데이터", "d": "LED 작품 → 공기질(웹·LED) → 날씨 API → <b>시트 기록 시작하고 퇴근</b>. <b>Ch2 후반~Ch6</b>"},
        {"t": "3일차 · 머신러닝", "d": "<b>데이터 개봉식</b> → 소리 분류(INMP441) → 동작 인식(IMU) 전반"},
        {"t": "4일차 · 종합", "d": "동작 인식 완성 → 자유 프로젝트(기획·제작·발표)"},
      ]},
      {"type": "callout", "kind": "key", "title": "전날 미리 확인 — 6장 밤새 기록의 성패",
       "html": "2일차 전까지 <b>① 교실 콘센트·USB 어댑터</b>(휴대폰 충전기면 충분) <b>② 야간 와이파이 차단 여부</b>를 확인하세요. 야간에 막히는 학교라면 6장을 3일차 오전으로 옮기고 <b>‘점심 2~3시간 기록’</b>으로 계획을 바꿉니다 — 목적은 밤샘이 아니라 ‘내가 안 보는 시간의 데이터’입니다."},
    ]},
    {"title": "1일차 — 피코와 첫 만남 (300분)", "items": [
      _plan_table([
        ("30분", "OT + 준비물 점검", "<b>그로브 케이블(LED용) vs 암 점퍼 케이블(MQ-2용)</b> 구분을 여기서 확실히. 데이터용 여분 USB 케이블 3~4개 준비"),
        ("90분", "<b>Ch0 준비하기</b> — Thonny·조립·펌웨어·첫 코드", "MQ-2 노란선→AO 확인 · 전원 스위치 5V. 케이블 불량이 최다 막힘"),
        ("120분", "<b>Ch1 와이파이 사각지대 찾기</b>", "wifi_config.py 저장 습관 — 3·5·6장까지 계속 재사용. 강사 핫스팟이 가장 안전"),
        ("60분", "<b>Ch2 전반</b> — timing 개념 + 기본 점등·채우기·무지개", "‘timing 없으면 Ctrl+F 검색 → AI에 재요청’ 습관 심기"),
      ]),
      {"type": "callout", "kind": "tip", "title": "밀렸을 때",
       "html": "Ch0이 밀리면(가장 흔한 시나리오) <b>Ch2 전반을 통째로 2일차로</b> 미루세요. 2일차의 Ch4를 30분으로 압축하면 흡수됩니다."},
    ]},
    {"title": "2일차 — 데이터의 날: 측정 → 표현 → 인터넷 → 기록 (300분)", "items": [
      _plan_table([
        ("10분", "리캡 + 전날 미해결 트러블 일괄 정리", ""),
        ("50분", "<b>Ch2 후반</b> — 게이지 + 감정 무드등 작품·상호 공유", "첫 ‘내 작품’ 경험 — 공유 시간을 아끼지 말 것"),
        ("80분", "<b>Ch3 공기질 웹 대시보드</b>", "여기서 정한 WARNING 값을 6장 조건부 서식에서 재사용"),
        ("40분", "<b>Ch4 공기질 LED 게이지</b>", "결합 장이라 짧게 — ‘배운 걸 조합하면 새 작품’ 메시지"),
        ("75분", "<b>Ch5 강수확률 API×LED</b>", "‘인터넷에서 받기’ — 다음 블록(보내기)의 발판"),
        ("45분", "<b>Ch6 공기질 기록 노트</b> — 구글 설정 → 피코 연결 → <b>기록 시작하고 퇴근</b>", "URL 자동 반영 상자로 시간 단축. <b>시트에 줄이 쌓이는 걸 확인한 뒤</b> 전원 꽂아 두고 마침. ‘내일 아침에 같이 열어 봐요’로 클리프행어"),
      ]),
      {"type": "callout", "kind": "warn", "title": "6장 45분 운영의 관건 — 구글 화면",
       "html": "구글 쪽 설정(15분)은 <b>스크린에 띄워 한 단계씩 같이</b> 가세요. ‘모든 사용자’ 배포·경고 화면 ‘고급’·<b>개인 계정</b>(학교 워크스페이스 ✗) 세 지점에서 손이 올라옵니다. <b>중간 점검(?value=99) 전원 통과</b>를 확인한 뒤 피코 연결로 넘어가면 나머지는 순조롭습니다."},
    ]},
    {"title": "3일차 — 데이터 개봉식 + 머신러닝의 날 (300분)", "items": [
      _plan_table([
        ("30분", "<b>📊 데이터 개봉식</b> — 6장 ‘쌓인 데이터로 탐구하기’", "“어제 우리가 떠난 뒤 교실은?” — 차트·조건부 서식·MAX/MIN/AVERAGE → <b>결론 한 줄 쓰기</b>(‘우리 교실은 __시에 환기’)"),
        ("150분", "<b>ML1 소리를 배우는 피코</b> — INMP441 + k-NN 소리 분류", "확장판의 심장. 자기가 고른 소리로 데이터 수집하는 시간을 넉넉히. 정규화·k·확신도 개념"),
        ("120분", "<b>ML2 동작 인식 전반</b> — IMU 개념 + 6축 읽기 + 물통 플립 데이터 수집 시작", "수집한 데이터로 내일 예측 — 두 번째 클리프행어"),
      ]),
      {"type": "callout", "kind": "info", "title": "MP3(말하기) 챕터를 재개한다면",
       "html": "SD 카드가 준비되어 ML+ ‘피코가 말을 한다’를 살리는 경우, <b>ML2 전반 120분 → 60분으로 줄이고</b> 그 자리에 MP3 75분을 넣으세요(ML2 나머지는 4일차로). 듣기→생각→말하기 사이클이 완성되는 대신 4일차 자유 프로젝트가 20분쯤 줄어듭니다."},
    ]},
    {"title": "4일차 — 종합과 자유 프로젝트 (300분)", "items": [
      _plan_table([
        ("15분", "리캡", ""),
        ("75분", "<b>ML2 완성</b> — 물통 플립 학습 → 성공 예측", "성공/실패 데이터를 조별로 모으면 자연스러운 협력 활동"),
        ("40분", "<b>자유 프로젝트 기획</b> — 7장 아이디어 + 부록 A 카탈로그", "‘일주일 공기질 리포트’ 같은 <b>기록형 작품</b>(6장 응용)도 선택지로. 주제 결정에 10분 이상 쓰지 않기"),
        ("110분", "<b>제작</b> — 바이브코딩", "LED·센서·API·ML·시트 기록 조합 자유. 순회하며 프롬프트 개선 코칭. 중간 30분쯤 ‘LED에 뭐라도 켜진 사람?’ 점검"),
        ("60분", "<b>발표·공유 + 정리</b>", "발문: “AI에게 뭐라고 설명했나요?” — 프롬프트가 곧 설계도"),
      ]),
    ]},
    {"title": "설계 노트 (시간이 왜 이렇게 배분됐나)", "items": [
      {"type": "concept", "items": [
        {"t": "Ch6 45분의 출처", "d": "2일차에서 리캡 5분 + Ch2 10분 + Ch3 10분 + Ch4 5분 + Ch5 15분을 압축해 확보. Ch5·Ch6은 둘 다 ‘피코가 인터넷과 대화’라 연달아 배우면 인지 부하가 오히려 줄어요."},
        {"t": "MP3 보류의 여유", "d": "말하기 챕터 75분이 빠진 자리를 IMU 전반(3일차)에 배분 → 4일차 자유 프로젝트가 185분으로 늘었습니다."},
        {"t": "버퍼", "d": "매일의 리캡과 Ch4(40분)가 사실상 버퍼. 최악의 경우 개봉식을 15분으로, Ch4를 30분으로 압축."},
        {"t": "차시형(학교 수업) 변환", "d": "같은 내용을 정규 수업으로 옮기면 장당 2차시(100분)씩 한 학기 분량. 6장 밤새 기록은 ‘차시 사이 일주일’로 자연 확장되고, 7장 자유 프로젝트+기록 리포트는 수행평가와 연결됩니다."},
      ]},
    ]},
  ],
}

BASE_TITLE = "데이터로 탐구하는 피코 바이브 피지컬 코딩"

def nav_html():
    """드로어 목차 — 모든 페이지 공용. 챕터별 파일(ch0.html…)로 링크한다."""
    nav = []
    for c in CHAPTERS:
        nav.append(f'<div class="nav-ch"><a href="{c["id"]}.html" class="nav-ch-link" '
                   f'data-target="{c["id"]}"><span class="nav-dot"></span>'
                   f'{esc(c["num"])}. {esc(c["title"])}</a>'
                   f'<div class="nav-secs">')
        for si, s in enumerate(c["sections"]):
            sid = f'{c["id"]}-{si}'
            nav.append(f'<a href="{c["id"]}.html#{sid}" class="nav-sec" data-target="{sid}">{esc(s["title"])}</a>')
        nav.append('</div></div>')
    return "".join(nav)

def chapter_main(c):
    """한 챕터의 본문 HTML (챕터 페이지용)."""
    sec_html = []
    for si, s in enumerate(c["sections"]):
        sid = f'{c["id"]}-{si}'
        items_html = "".join(render_item(it, c.get("accent", "")) for it in s["items"])
        sec_html.append(f'<section class="sec" id="{sid}">'
                        f'<h3 class="sec-title">{esc(s["title"])}</h3>{items_html}</section>')
    goals = "".join(f'<li>{g}</li>' for g in c.get("goals", []))
    intro = ''
    if goals:
        intro += f'<div class="goals"><div class="goals-t">🎯 이 장을 마치면</div><ul>{goals}</ul></div>'
    if c.get("why"):
        intro += f'<div class="why"><div class="why-t">💡 왜 배우나요?</div><p>{c["why"]}</p></div>'
    return (f'<div class="chapter" id="{c["id"]}">'
            f'<div class="ch-head"><span class="ch-num">CHAPTER {c["num"]}</span>'
            f'<h2 class="ch-title"><span class="ch-bar"></span>{esc(c["title"])}</h2>'
            f'<p class="ch-sub">{esc(c["subtitle"])}</p></div>'
            f'{intro}{c.get("extra","")}{"".join(sec_html)}</div>')

def pager_html(idx):
    """챕터 하단 이전/다음 이동 카드."""
    prev = CHAPTERS[idx - 1] if idx > 0 else None
    nxt = CHAPTERS[idx + 1] if idx + 1 < len(CHAPTERS) else None
    def card(c, cls, direction):
        if not c:
            return (f'<a class="{cls}" href="index.html"><span class="dir">{direction}</span>'
                    f'<span class="tt">목차로</span></a>')
        return (f'<a class="{cls}" href="{c["id"]}.html"><span class="dir">{direction}</span>'
                f'<span class="tt">{esc(c["num"])}. {esc(c["title"])}</span></a>')
    return ('<nav class="pager">'
            + card(prev, "prev", "← 이전")
            + card(nxt, "next", "다음 →")
            + '</nav>')

def hub_main():
    """허브(index.html) 본문 — 히어로 + 챕터 링크카드 목차."""
    cards = []
    if TEACHER:
        cards.append('<a class="linkcard" href="plan.html">'
                     '<span class="n">🗓 운영</span>'
                     '<span class="tt">20시간 연수 운영 계획 (강사 전용)</span>'
                     '<span class="d">4일 × 5시간 표준 진행안 — 하루별 시간표, 6장 밤새 기록 운영법, 밀렸을 때 버퍼까지.</span></a>')
    for c in CHAPTERS:
        cards.append(f'<a class="linkcard" href="{c["id"]}.html">'
                     f'<span class="n">CHAPTER {esc(c["num"])}</span>'
                     f'<span class="tt">{esc(c["title"])}</span>'
                     f'<span class="d">{esc(c.get("subtitle", ""))}</span></a>')
    cards.append('<a class="linkcard" href="dashboards/index.html">'
                 '<span class="n">LIVE</span>'
                 '<span class="tt">🛰️ 오픈 API 라이브 대시보드</span>'
                 '<span class="d">피코 없이 브라우저에서 공개 데이터를 바로 받아 그려 보는 탐구실 11종 (지진·ISS·미세먼지…)</span></a>')
    cards.append('<a class="linkcard" href="gallery/index.html">'
                 '<span class="n">GALLERY</span>'
                 '<span class="tt">🖼️ 학생 작품 갤러리</span>'
                 '<span class="d">로그인 없이 닉네임만으로 내 작품을 올리고, 다른 선생님 작품에 좋아요·한 줄 피드백을 남겨보세요.</span></a>')
    return (f'<h2 style="font-size:1.35rem;font-weight:800;margin:6px 0 4px">📚 목차</h2>'
            f'<p style="color:var(--text-soft);font-size:14px;margin:0 0 10px">순서대로 따라가도 되고, 필요한 장만 골라 봐도 됩니다. '
            f'용어가 낯설면 <a class="ilink" href="apxc.html">부록 C · 용어 사전</a>부터 열어 두세요.</p>'
            f'<div class="linkgrid">{"".join(cards)}</div>')

def page(main, title, teacher=False, fname=None, hero=""):
    """TEMPLATE에 본문을 끼워 완성된 페이지 HTML을 돌려준다."""
    out = TEMPLATE
    out = out.replace("/*NAV*/", nav_html())
    out = out.replace("/*HERO*/", hero)
    out = out.replace("/*MAIN*/", main)
    out = out.replace(f'<title>{BASE_TITLE}</title>', f'<title>{title}</title>')
    if teacher:
        out = out.replace('<span class="badge">학생용</span>',
                          '<span class="badge teacher">강사용</span>')
        out = out.replace('<!--MODELINK-->',
                          f'<a class="home" href="../{fname}">학생용 ↗</a>')
        # teacher/ 하위 디렉터리 기준으로 자산·형제 사이트 경로 보정
        for pre in ("favicon.svg", "dashboards/", "ml_site/", "firmware/", "gallery/"):
            out = out.replace(f'href="{pre}', f'href="../{pre}')
    else:
        out = out.replace('<!--MODELINK-->',
                          '<a class="home" href="index.html">← 목차</a>' if fname != "index.html" else '')
    return out

def build(teacher=False):
    """학생용(루트) 또는 강사용(teacher/) 사이트 한 벌을 생성한다."""
    global n_code, n_prompt, TEACHER
    n_code, n_prompt, TEACHER = 0, 0, teacher
    outdir = os.path.join(BASE, "teacher") if teacher else BASE
    os.makedirs(outdir, exist_ok=True)
    who = "강사용" if teacher else "학생용"

    # 챕터 페이지 (렌더하며 코드/프롬프트 수를 함께 센다)
    for i, c in enumerate(CHAPTERS):
        title = f'{c["num"]}. {c["title"]} · {BASE_TITLE}' + (' (강사용)' if teacher else '')
        html_out = page(chapter_main(c) + pager_html(i), title,
                        teacher=teacher, fname=f'{c["id"]}.html')
        with open(os.path.join(outdir, f'{c["id"]}.html'), "w", encoding="utf-8") as f:
            f.write(html_out)

    # 강사 전용 — 연수 운영 계획 페이지 (CHAPTERS 밖이라 드로어 목차에는 없음, 허브 카드로 진입)
    if teacher:
        html_out = page(chapter_main(PLAN_PAGE),
                        f'연수 운영 계획 · {BASE_TITLE} (강사용)',
                        teacher=True, fname="index.html")  # '학생용 ↗'은 학생 허브로
        with open(os.path.join(outdir, "plan.html"), "w", encoding="utf-8") as f:
            f.write(html_out)

    # 옛 부록 B(apxb.html) → 본문 6장으로 승격됨. 배포된 옛 링크를 위한 리다이렉트 스텁.
    with open(os.path.join(outdir, "apxb.html"), "w", encoding="utf-8") as f:
        f.write('<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">'
                '<meta http-equiv="refresh" content="0; url=ch6.html">'
                '<link rel="canonical" href="ch6.html"><title>이동됨 · 6장 공기질 기록 노트</title></head>'
                '<body><p>이 내용은 본문 <a href="ch6.html">6장 · 우리반 공기질 기록 노트</a>로 옮겨졌어요. '
                '자동으로 이동합니다…</p></body></html>')

    # 허브 (히어로 + 링크카드 목차)
    hero = (HERO_HTML.replace("/*NCH*/", str(len(CHAPTERS)))
                     .replace("/*NCODE*/", str(n_code))
                     .replace("/*NPROMPT*/", str(n_prompt)))
    # 확장판(ml-cta) 배너는 본편 허브에서 노출하지 않는다.
    # (HERO_HTML 원본에는 남겨 둔다 — build_ml_site.py가 이 블록을 '본편 열기' 카드로 치환해 쓴다)
    _a = hero.find('<a class="ml-cta"')
    if _a != -1:
        _b = hero.find('</a>', _a) + 4
        hero = hero[:_a] + hero[_b:]
    hub_title = BASE_TITLE + (' (강사용)' if teacher else '')
    html_out = page(hub_main(), hub_title, teacher=teacher, fname="index.html", hero=hero)
    if teacher:
        html_out = html_out.replace('<a class="home" href="../index.html">학생용 ↗</a>',
                                    '<a class="home" href="../">학생용 ↗</a>')
    with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_out)
    print(f"생성 완료 ({who}) · 허브 + 챕터 {len(CHAPTERS)}페이지 · 코드 {n_code}개 · 프롬프트 {n_prompt}개"
          + (" · 강사노트 포함" if teacher else ""))

# ===================================================================
#  HTML 템플릿 (CSS는 그대로 — 토큰 치환 방식)
# ===================================================================
TEMPLATE = r'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<title>데이터로 탐구하는 피코 바이브 피지컬 코딩</title>
<meta name="description" content="라즈베리파이 피코 2 WH로 배우는 피지컬 컴퓨팅 연수 자료 — 설치부터 와이파이·LED·가스센서·날씨 API 대시보드까지, 복사해서 바로 쓰는 MicroPython 코드 모음.">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/atom-one-dark.min.css">
<style>
/* ============================================================
   피코 바이브 피지컬 코딩 · 웹 교재 스타일
   디자인 계열: 2026-snui 웹 교재 (따뜻한 크림·골드)
   ============================================================ */
:root{
  --gold:#f4b400; --accent:#e8930c;
  --bg:#fffdf7; --card:#fff6e0;
  --border:#f0e2bc; --border-soft:#f7edcf;
  --text:#3a2e1a; --text-soft:#6b5836; --muted:#9a8b6a;
  --blue:#4c8df6; --blue-ink:#2f6bd6; --blue-soft:#eef3ff;
  --green:#54a24b; --green-soft:#eef6e8;
  --red:#e45756; --red-soft:#fdeeee;
  --teal:#3ba6a0; --teal-ink:#2b7a75; --teal-soft:#e9f6f5;
  --violet:#b279a2; --violet-soft:#f8f0f5;
  --code-bg:#2a2318; --code-text:#f0e8d6;
  --radius:0.9rem; --radius-sm:0.7rem;
  --shadow:0 1px 4px rgba(180,140,20,.1);
  --shadow-lg:0 8px 24px rgba(180,140,20,.16);
  --maxw:960px;
  --font:-apple-system,BlinkMacSystemFont,'Apple SD Gothic Neo','Malgun Gothic','Segoe UI',Roboto,sans-serif;
  --mono:'SFMono-Regular','D2Coding',ui-monospace,Menlo,Consolas,monospace;
}
*{box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{margin:0;font-family:var(--font);color:var(--text);background:var(--bg);line-height:1.72;-webkit-font-smoothing:antialiased;font-size:15.5px;}
a{color:inherit;text-decoration:none;}
.ilink{color:var(--blue-ink);text-decoration:underline;text-underline-offset:2px;font-weight:600;}
.ilink:hover{color:var(--blue);}
/* ---------- 상단 바 ---------- */
.topbar{position:sticky;top:0;z-index:50;background:rgba(255,253,247,.9);
  backdrop-filter:saturate(180%) blur(8px);-webkit-backdrop-filter:saturate(180%) blur(8px);
  border-bottom:1px solid var(--border);}
.topbar .inner{max-width:var(--maxw);margin:0 auto;padding:10px 20px;display:flex;align-items:center;gap:12px;}
.menu-btn{display:inline-flex;align-items:center;gap:6px;font-family:var(--font);font-size:13px;font-weight:800;
  color:var(--text-soft);background:var(--card);border:1px solid var(--border);border-radius:999px;
  padding:5px 13px;cursor:pointer;transition:.15s;white-space:nowrap;}
.menu-btn:hover{border-color:var(--accent);color:var(--accent);}
.topbar .brand{font-weight:800;letter-spacing:-.02em;display:flex;align-items:center;gap:7px;font-size:15px;min-width:0;}
.topbar .brand .brand-emoji{font-size:17px;}
.topbar .spacer{flex:1;}
.topbar .badge{font-size:.72rem;font-weight:800;padding:3px 10px;border-radius:999px;
  border:1px solid var(--border);background:var(--card);color:var(--accent);white-space:nowrap;}
.topbar .badge.teacher{border-color:#cfe0ff;background:var(--blue-soft);color:var(--blue-ink);}
.topbar a.home{color:var(--muted);font-size:.83rem;font-weight:700;white-space:nowrap;}
.topbar a.home:hover{color:var(--text);}
/* ---------- 목차 드로어 ---------- */
.drawer{position:fixed;left:0;top:0;bottom:0;z-index:70;width:302px;overflow-y:auto;
  background:var(--bg);border-right:1px solid var(--border);padding:18px 14px 60px;
  transform:translateX(-100%);transition:transform .22s ease;}
.drawer.open{transform:none;box-shadow:0 0 44px rgba(120,90,10,.2);}
.drawer .brand{font-weight:800;font-size:14.5px;padding:4px 10px 12px;letter-spacing:-.02em;}
.drawer .brand small{display:block;font-weight:500;color:var(--muted);font-size:12px;margin-top:3px;}
.scrim{display:none;}
.scrim.show{display:block;position:fixed;inset:0;background:rgba(58,46,26,.32);z-index:65;}
.nav-ch{margin-top:8px;}
.nav-ch-link{display:flex;align-items:center;gap:8px;font-weight:700;font-size:13.5px;padding:7px 10px;border-radius:8px;}
.nav-ch-link:hover{background:var(--card);}
.nav-dot{width:9px;height:9px;border-radius:50%;flex:0 0 9px;background:linear-gradient(120deg,var(--gold),var(--accent));}
.nav-secs{display:flex;flex-direction:column;margin:2px 0 8px 18px;border-left:1px solid var(--border);}
.nav-sec{font-size:12.5px;color:var(--muted);padding:5px 10px;border-left:2px solid transparent;margin-left:-1px;}
.nav-sec:hover{color:var(--text);}
.nav-sec.active{color:var(--text);font-weight:700;border-left-color:var(--accent);}
/* ---------- 레이아웃 ---------- */
.wrap{max-width:var(--maxw);margin:0 auto;padding:26px 20px 96px;}
.main{background:#fff;border:1px solid var(--border);border-radius:var(--radius);
  padding:40px clamp(20px,5vw,52px) 48px;box-shadow:var(--shadow);}
/* ---------- 히어로 ---------- */
.hero{padding:10px 0 26px;border-bottom:1px solid var(--border);margin-bottom:14px;}
.eyebrow{font-size:.78rem;font-weight:800;text-transform:uppercase;letter-spacing:.08em;color:var(--accent);}
.hero h1{font-size:clamp(26px,4.5vw,36px);font-weight:800;letter-spacing:-.03em;margin:8px 0 0;line-height:1.28;}
.under{width:64px;height:4px;border-radius:999px;background:linear-gradient(90deg,var(--gold),#ffd766);margin:.6rem 0 1.1rem;}
.hero p{font-size:15px;color:var(--text-soft);margin:0 0 20px;max-width:680px;}
.stats{display:flex;gap:10px;flex-wrap:wrap;}
.stat{display:flex;align-items:baseline;gap:7px;background:var(--card);border:1px solid var(--border);
  border-radius:999px;padding:6px 15px;font-size:13px;color:var(--text-soft);}
.stat b{font-size:15px;color:var(--text);font-weight:800;}
.ml-cta{display:flex;align-items:center;gap:14px;margin:22px 0 2px;padding:16px 18px;border:1px solid var(--border);
  border-radius:var(--radius);background:linear-gradient(135deg,var(--card),var(--bg));box-shadow:var(--shadow);
  transition:border-color .15s,box-shadow .15s,transform .15s;}
.ml-cta:hover{border-color:var(--accent);box-shadow:var(--shadow-lg);transform:translateY(-2px);}
.ml-cta-emoji{font-size:30px;flex:0 0 auto;line-height:1;}
.ml-cta-txt{display:flex;flex-direction:column;gap:3px;flex:1;min-width:0;}
.ml-cta-txt b{font-size:15px;letter-spacing:-.01em;}
.ml-cta-txt small{color:var(--muted);font-size:12.5px;line-height:1.5;}
.ml-cta-go{flex:0 0 auto;font-weight:800;font-size:13px;color:var(--accent);white-space:nowrap;}
/* ---------- 링크 카드 (허브 목차) ---------- */
.linkgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px;margin:18px 0;}
.linkcard{display:block;border:1px solid var(--border);border-radius:var(--radius-sm);padding:16px;background:#fff;transition:border-color .15s,transform .15s,box-shadow .15s;}
.linkcard:hover{border-color:var(--accent);transform:translateY(-2px);box-shadow:var(--shadow-lg);}
.linkcard .n{display:block;font-size:.72rem;font-weight:800;color:var(--accent);letter-spacing:.06em;}
.linkcard .tt{display:block;font-weight:800;margin:4px 0 2px;}
.linkcard .d{display:block;font-size:.85rem;color:var(--text-soft);line-height:1.55;}
/* ---------- 하단 이동 (이전/다음) ---------- */
.pager{display:flex;justify-content:space-between;gap:12px;margin-top:46px;}
.pager a{flex:1;border:1px solid var(--border);border-radius:var(--radius-sm);padding:14px 16px;background:#fff;transition:border-color .15s,box-shadow .15s;}
.pager a:hover{border-color:var(--accent);box-shadow:var(--shadow);}
.pager .dir{display:block;font-size:.72rem;color:var(--muted);font-weight:800;}
.pager .tt{display:block;font-weight:800;}
.pager a.next{text-align:right;}
/* ---------- 챕터 / 섹션 ---------- */
.chapter{padding-top:24px;scroll-margin-top:70px;}
.ch-head{margin:34px 0 8px;}
.ch-num{font-size:.76rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);}
.ch-title{display:flex;align-items:center;gap:12px;font-size:26px;font-weight:800;letter-spacing:-.02em;margin:6px 0 8px;}
.ch-bar{width:5px;height:26px;border-radius:3px;flex:0 0 5px;background:linear-gradient(180deg,var(--gold),var(--accent));}
.ch-sub{color:var(--text-soft);font-size:14.5px;margin:0 0 6px;max-width:680px;}
.sec{padding-top:12px;scroll-margin-top:70px;}
.sec-title{font-size:17px;font-weight:800;margin:34px 0 12px;letter-spacing:-.01em;padding-top:16px;border-top:1px solid var(--border);}
.prose{font-size:14.5px;margin:12px 0;max-width:720px;}
.prose code,.callout-body code,.concept-d code,.steps code,.m-row code,.qa-a code,.idea-d code,.dig-body code{
  font-family:var(--mono);font-size:12.5px;background:var(--card);border:1px solid var(--border);
  border-radius:5px;padding:1px 6px;color:#7a5a1e;}
.step-head{font-size:14.5px;margin:22px 0 10px;max-width:720px;}
/* ---------- 챕터 인트로 (목표 / 왜 배우나요) ---------- */
.goals{background:linear-gradient(135deg,var(--card),var(--bg));border:1px solid var(--border);
  border-radius:var(--radius);padding:16px 20px;margin:14px 0;max-width:720px;box-shadow:var(--shadow);}
.goals-t{font-weight:800;font-size:14px;margin-bottom:8px;color:var(--accent);}
.goals ul{margin:0;padding-left:20px;}
.goals li{font-size:13.5px;margin:4px 0;}
.why{background:#fff;border:1px solid var(--border);border-left:4px solid var(--gold);
  border-radius:var(--radius-sm);padding:14px 18px;margin:14px 0;max-width:720px;}
.why-t{font-weight:800;font-size:14px;margin-bottom:6px;color:var(--text-soft);}
.why p{margin:0;font-size:14px;}
/* ---------- 콜아웃 (tip/warn/mini/say/theory/ask/check/err + info/key) ---------- */
.callout{border:1px solid var(--border);border-left:4px solid var(--muted);background:var(--card);
  border-radius:var(--radius-sm);padding:13px 16px;margin:16px 0;max-width:720px;}
.callout-head{font-weight:800;font-size:13.5px;margin-bottom:5px;}
.callout-body{font-size:13.5px;}
.callout.tip{border-left-color:var(--blue);background:var(--blue-soft);}
.callout.tip .callout-head{color:var(--blue-ink);}
.callout.info{border-left-color:var(--blue);background:var(--blue-soft);}
.callout.info .callout-head{color:var(--blue-ink);}
.callout.warn{border-left-color:var(--accent);background:var(--card);}
.callout.warn .callout-head{color:#b45309;}
.callout.key{border-left-color:var(--gold);background:linear-gradient(135deg,#fffaf0,#fff);}
.callout.key .callout-head{color:#a06a08;}
.callout.check{border-left-color:var(--green);background:var(--green-soft);}
.callout.check .callout-head{color:#3d7a37;}
.callout.mini{border-left-color:var(--teal);background:var(--teal-soft);}
.callout.mini .callout-head{color:var(--teal-ink);}
.callout.say{border-left-color:var(--blue);background:var(--blue-soft);}
.callout.say .callout-head{color:var(--blue-ink);}
.callout.ask{border-left-color:var(--teal);background:var(--teal-soft);}
.callout.ask .callout-head{color:var(--teal-ink);}
.callout.theory{border-left-color:var(--violet);background:var(--violet-soft);}
.callout.theory .callout-head{color:#8a5578;}
.callout.err{border-left-color:var(--red);background:var(--red-soft);}
.callout.err .callout-head{color:#c23b3a;}
/* ---------- 링크 버튼 ---------- */
.linkbtn{display:inline-flex;align-items:center;gap:6px;background:#fff;border:1px solid var(--border);
  border-radius:10px;padding:9px 16px;font-size:13.5px;font-weight:700;margin:8px 8px 8px 0;transition:.15s;color:var(--text-soft);}
.linkbtn:hover{border-color:var(--accent);color:var(--accent);box-shadow:var(--shadow);}
/* ---------- 체크리스트 (준비물) ---------- */
.check-list{list-style:none;padding:0;margin:12px 0;max-width:720px;}
.check-list li{font-size:14px;padding:7px 0 7px 30px;position:relative;border-bottom:1px solid var(--border-soft);}
.check-list li:before{content:"☐";position:absolute;left:4px;top:6px;font-size:16px;color:var(--accent);}
/* ---------- 핵심 개념 / 아이디어 그리드 ---------- */
.concept-grid,.idea-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;margin:14px 0;max-width:760px;}
.concept,.idea{background:var(--card);border:1px solid var(--border);border-radius:var(--radius-sm);padding:13px 15px;}
.concept-t,.idea-t{font-weight:800;font-size:13.5px;margin-bottom:5px;}
.concept-d,.idea-d{font-size:13px;color:var(--text-soft);}
.idea-d code,.concept-d code{word-break:break-all;}
.idea-d{line-height:1.7;}
/* ---------- 스텝 ---------- */
.steps{margin:14px 0;padding-left:0;counter-reset:s;list-style:none;max-width:720px;}
.steps li{position:relative;padding:3px 0 16px 44px;font-size:14px;}
.steps li:before{counter-increment:s;content:counter(s);position:absolute;left:0;top:2px;width:29px;height:29px;
  background:var(--accent);color:#fff;border-radius:50%;text-align:center;line-height:29px;font-size:13px;font-weight:800;
  box-shadow:var(--shadow);}
.steps li:not(:last-child):after{content:"";position:absolute;left:14px;top:35px;bottom:2px;width:2px;background:var(--border);}
.steps li>b{display:block;margin-bottom:2px;}
.steps li span{color:var(--text-soft);font-size:13.5px;}
/* ---------- 자주 하는 실수 ---------- */
.mistakes{margin:12px 0;max-width:720px;}
.mistake{border:1px solid var(--border);border-left:4px solid var(--red);border-radius:var(--radius-sm);
  padding:12px 15px;margin:10px 0;background:var(--red-soft);}
.m-sym{font-weight:800;font-size:13.5px;color:#c23b3a;margin-bottom:7px;}
.m-row{font-size:13px;margin:4px 0;padding-left:2px;}
.m-tag{display:inline-block;font-size:11px;font-weight:800;color:#fff;background:var(--muted);border-radius:5px;
  padding:1px 7px;margin-right:7px;}
.m-tag.fix{background:var(--green);}
/* ---------- 스스로 점검 ---------- */
.checks{margin:12px 0;max-width:720px;}
.qa{border:1px solid var(--border);border-radius:var(--radius-sm);margin:8px 0;background:#fff;}
.qa summary{cursor:pointer;padding:11px 15px;font-size:13.8px;font-weight:700;list-style:none;}
.qa summary::-webkit-details-marker{display:none;}
.qa summary:before{content:"❓ ";}
.qa[open] summary{border-bottom:1px solid var(--border);background:var(--green-soft);border-radius:var(--radius-sm) var(--radius-sm) 0 0;}
.qa-a{padding:11px 15px;font-size:13.5px;color:var(--text-soft);}
.qa-a:before{content:"✅ ";}
/* ---------- 더 알아보기 (이론 심화) ---------- */
.dig{border:1px solid var(--border);border-left:4px solid var(--violet);border-radius:var(--radius-sm);
  margin:16px 0;max-width:760px;background:var(--violet-soft);}
.dig summary{cursor:pointer;padding:12px 16px;font-weight:800;font-size:13.5px;color:#8a5578;list-style:none;}
.dig summary::-webkit-details-marker{display:none;}
.dig summary:after{content:"▾";float:right;color:var(--violet);transition:.2s;}
.dig[open] summary:after{transform:rotate(180deg);}
.dig[open] summary{border-bottom:1px solid #ecd9e6;}
.dig-body{padding:14px 16px;font-size:13.5px;line-height:1.8;color:var(--text-soft);background:#fff;
  border-radius:0 0 var(--radius-sm) var(--radius-sm);}
.dig-body b{color:#8a5578;}
/* ---------- 코드 접기 ---------- */
.codefold{margin:12px 0;max-width:840px;}
.codefold>summary{cursor:pointer;list-style:none;padding:11px 15px;border:1px dashed #e0cf9a;border-radius:var(--radius-sm);
  background:var(--card);font-size:13px;font-weight:800;color:var(--text-soft);}
.codefold>summary::-webkit-details-marker{display:none;}
.codefold>summary:before{content:"📄 ";}
.codefold>summary:after{content:"  ▾";color:var(--muted);}
.codefold[open]>summary:after{content:"  ▴";}
.codefold[open]>summary{border-style:solid;border-color:var(--border);border-bottom:none;
  border-radius:var(--radius-sm) var(--radius-sm) 0 0;}
.codefold .fold-hint{font-weight:500;color:var(--muted);}
.codefold .block{margin:0;border-radius:0 0 var(--radius-sm) var(--radius-sm);}
/* ---------- 브랜딩 강조 ---------- */
.pico-accent{background:linear-gradient(120deg,var(--gold),var(--accent));-webkit-background-clip:text;
  background-clip:text;color:transparent;font-weight:900;}
.brand-emoji{font-size:17px;}
/* '피지컬 코딩'의 [피][코] 글자 강조 — 피코 워드플레이 */
.pk{background:linear-gradient(120deg,var(--gold),var(--accent));color:#fff;font-weight:900;
  border-radius:7px;padding:0 .26em;margin:0 .02em;}
/* ---------- 하드웨어 다이어그램 ---------- */
.figure{margin:14px 0;max-width:760px;}
.diagram{font-family:var(--mono);font-size:12px;line-height:1.5;background:var(--card);
  border:1px solid var(--border);border-radius:var(--radius-sm);padding:16px;overflow-x:auto;white-space:pre;}
.hw-svg{width:100%;height:auto;background:#fff;border:1px solid var(--border);border-radius:12px;padding:12px;font-family:var(--font);}
.api-svg{width:100%;height:auto;background:#fffdf9;border:1px solid var(--border);border-radius:14px;padding:8px;font-family:var(--font);}
/* ---------- 코드 / 프롬프트 / 개선 블록 ---------- */
.block{border:1px solid var(--border);border-radius:var(--radius-sm);margin:12px 0;overflow:hidden;background:#fff;max-width:840px;}
.block-head{display:flex;align-items:center;gap:9px;padding:8px 13px;background:var(--card);border-bottom:1px solid var(--border);}
.block-label{font-size:12.5px;font-weight:800;color:var(--text-soft);flex:1;min-width:0;}
.lang-tag{font-family:var(--mono);font-size:10.5px;font-weight:700;color:var(--muted);
  background:#fff;border:1px solid var(--border);border-radius:5px;padding:1px 7px;letter-spacing:.04em;}
.plan-table{width:100%;border-collapse:collapse;margin:12px 0 6px;font-size:13.5px;line-height:1.62;min-width:520px;}
.plan-table th,.plan-table td{border:1px solid var(--border);padding:8px 12px;text-align:left;vertical-align:top;}
.plan-table th{background:var(--green-soft);font-weight:800;white-space:nowrap;}
.plan-table td.t{white-space:nowrap;font-weight:800;color:#b45309;}
.plan-table td.note{color:var(--text-soft);font-size:12.5px;}
.urlbox{margin:16px 0;padding:15px 17px;border:2px solid #86efac;border-radius:14px;background:#f0fdf4;}
.urlbox label{display:block;font-size:13.5px;font-weight:800;margin-bottom:8px;color:#166534;}
.urlbox input{width:100%;box-sizing:border-box;font-family:var(--mono);font-size:12.5px;padding:9px 12px;
  border:1.5px solid #bbf7d0;border-radius:9px;background:#fff;color:var(--text);}
.urlbox input:focus{outline:none;border-color:#16A34A;box-shadow:0 0 0 3px #bbf7d055;}
.urlbox-msg{margin-top:8px;font-size:12.5px;line-height:1.55;}
.urlbox-msg:empty{display:none;}
.ub-ok{color:#166534;} .ub-warn{color:#b45309;}
.ub-test{display:inline-block;margin-top:4px;font-weight:800;color:#166534;text-decoration:underline;}
.urlbox small{display:block;margin-top:7px;color:var(--muted);font-size:11.5px;line-height:1.5;}
.copy-btn{font-family:var(--font);font-size:11.5px;font-weight:800;color:var(--text-soft);cursor:pointer;
  background:#fff;border:1px solid var(--border);border-radius:6px;padding:4px 11px;transition:.15s;flex:0 0 auto;}
.copy-btn:hover{color:var(--accent);border-color:var(--accent);}
.copy-btn.done{color:#fff;border-color:var(--green);background:var(--green);}
/* 코드: 따뜻한 다크 (파트너 code-bg) */
.code-block pre{margin:0;padding:16px 18px;overflow-x:auto;background:var(--code-bg);}
.code-block code{font-family:var(--mono);font-size:13px;line-height:1.62;background:none;padding:0;color:var(--code-text);}
.code-block .block-head{background:#211b10;border-bottom-color:#3b3222;}
.code-block .block-label{color:#e8dcc0;}
.code-block .lang-tag{color:#c9b98c;background:#3b3222;border-color:#4d4230;}
.code-block .copy-btn{color:#e8dcc0;background:#3b3222;border-color:#4d4230;}
.code-block .copy-btn:hover{color:#fff;border-color:#7a6338;}
.code-block .copy-btn.done{color:#fff;border-color:var(--green);background:var(--green);}
/* 프롬프트: 파트너 teal 다크 */
.prompt-block{border-color:#cfe8e4;}
.prompt-block .block-head{background:var(--teal-soft);border-bottom-color:#cfe8e4;}
.prompt-block .block-label{color:var(--teal-ink);}
.prompt-ico{font-size:15px;}
.prompt-body{font-family:var(--mono);font-size:13px;line-height:1.7;color:#d7f0ea;
  white-space:pre-wrap;word-break:break-word;padding:15px 18px;background:#1c2b26;}
/* ③ 프롬프트 개선: 파트너 improve (따뜻한 다크 골드) */
.improve-block{border-color:#ecd9ae;}
.improve-block .block-head{background:linear-gradient(135deg,#fdf3dd,#fffaf0);border-bottom-color:#ecd9ae;}
.improve-block .block-label{color:#b45309;}
.improve-block .prompt-body{background:#2a2012;color:#f6e8cf;}
/* ---------- 펌웨어 카드 ---------- */
.fw-card{border:1px solid var(--border);border-radius:var(--radius);
  background:linear-gradient(180deg,var(--card),#fff);padding:22px 24px;margin:12px 0 18px;max-width:840px;box-shadow:var(--shadow);}
.fw-top{display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap;}
.fw-badge{display:inline-block;font-size:11.5px;font-weight:800;color:var(--accent);
  background:#fff;border:1px solid var(--border);border-radius:999px;padding:3px 12px;margin-bottom:9px;}
.fw-title{margin:0 0 5px;font-size:19px;font-weight:800;letter-spacing:-.01em;}
.fw-meta{margin:0;color:var(--muted);font-size:13px;}
.fw-meta b{color:var(--text);}
.dl-btn{display:inline-flex;align-items:center;background:var(--accent);color:#fff;font-weight:800;
  font-size:14.5px;border-radius:11px;padding:13px 22px;white-space:nowrap;
  box-shadow:0 5px 16px rgba(232,147,12,.35);transition:.15s;}
.dl-btn:hover{background:#d2830a;transform:translateY(-1px);}
.fw-steps-wrap{margin-top:18px;background:#fff;border:1px solid var(--border);border-radius:var(--radius-sm);padding:14px 18px 16px;}
.fw-steps-title{font-size:12.5px;font-weight:800;color:var(--accent);margin-bottom:6px;}
.fw-steps{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:7px;font-size:13.5px;color:var(--text);line-height:1.5;}
.fw-steps li{padding-left:3px;}
.fw-dim{color:var(--muted);}
.fw-steps code,.fw-note code{font-family:var(--mono);font-size:12px;background:var(--card);
  border:1px solid var(--border);border-radius:4px;padding:1px 6px;color:#7a5a1e;}
.fw-note{margin:14px 0 0;font-size:12.5px;color:var(--muted);line-height:1.55;}
.fw-note a{color:var(--blue-ink);text-decoration:underline;}
/* ---------- 푸터 ---------- */
footer{margin-top:56px;padding-top:22px;border-top:1px solid var(--border);color:var(--muted);font-size:12.5px;}
/* ---------- 반응형 ---------- */
@media(max-width:640px){
  body{font-size:15px;}
  .main{padding:26px 16px 36px;}
  .topbar .inner{padding:9px 12px;gap:8px;}
  .topbar .brand{font-size:13.5px;}
  .topbar a.home{display:none;}
  .hero h1{font-size:24px;}
  .ml-cta{flex-wrap:wrap;gap:10px;}
  .ml-cta-go{width:100%;}
}
</style>
</head>
<body>
<div class="topbar"><div class="inner">
  <button class="menu-btn" id="menuBtn" aria-label="목차 열기">☰ 목차</button>
  <a class="brand" href="index.html"><span class="brand-emoji">🐣🔌</span> 바이브 <span class="pk">피</span>지컬 <span class="pk">코</span>딩</a>
  <span class="spacer"></span>
  <!--MODELINK-->
  <span class="badge">학생용</span>
</div></div>
<div class="scrim" id="scrim"></div>
<aside class="drawer" id="sidebar">
  <div class="brand"><span class="brand-emoji">🐣🔌</span> 바이브 <span class="pk">피</span>지컬 <span class="pk">코</span>딩<small>데이터 기반 탐구 프로젝트 · <span class="pico-accent">피코</span>로 시작하기</small></div>
  /*NAV*/
</aside>
<div class="wrap">
<main class="main">
    /*HERO*/
    /*MAIN*/
    <footer>
      라즈베리파이 피코 2 WH · MicroPython · Thonny &nbsp;·&nbsp; 손 코딩 → 바이브 코딩<br>
      LED → 그로브 D16(GP16) · MQ-2 → 그로브 A0(GP26) &nbsp;·&nbsp; 이 자료의 코드와 프롬프트는 연수·수업에 자유롭게 활용할 수 있습니다.
    </footer>
</main>
</div>
<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js"></script>
<script>
// 코드 하이라이트 (실패해도 아래 복사 기능은 계속 동작하도록 보호)
try{
  if(window.hljs){ document.querySelectorAll('pre code').forEach(el=>{ try{hljs.highlightElement(el);}catch(e){} }); }
}catch(e){}
// 복사 — clipboard API → 실패 시 execCommand 폴백 (둘 다 처리)
function fallbackCopy(text){
  const ta=document.createElement('textarea');
  ta.value=text; ta.setAttribute('readonly','');
  ta.style.position='fixed'; ta.style.top='-9999px';
  document.body.appendChild(ta); ta.select(); ta.setSelectionRange(0, text.length);
  let ok=false; try{ ok=document.execCommand('copy'); }catch(e){}
  document.body.removeChild(ta); return ok;
}
function flash(btn, msg, good){
  btn.textContent=msg; if(good) btn.classList.add('done');
  setTimeout(()=>{ btn.textContent='복사'; btn.classList.remove('done'); }, 1400);
}
document.querySelectorAll('.block').forEach(block=>{
  const btn=block.querySelector('.copy-btn'); if(!btn) return;
  btn.addEventListener('click', async ()=>{
    const code=block.querySelector('code');
    const body=block.querySelector('.prompt-body');
    const text=code?code.textContent:(body?body.textContent:'');
    try{
      if(navigator.clipboard && window.isSecureContext){
        await navigator.clipboard.writeText(text); flash(btn,'복사됨',true);
      }else{
        const ok=fallbackCopy(text); flash(btn, ok?'복사됨':'복사 실패', ok);
      }
    }catch(e){
      const ok=fallbackCopy(text); flash(btn, ok?'복사됨':'복사 실패', ok);
    }
  });
});
// 웹 앱 주소 자동 반영 (6장 urlbox) — 붙여넣으면 페이지의 WEB_APP_URL 코드가 내 주소로 바뀐다
document.querySelectorAll('.urlbox').forEach(box=>{
  const input=box.querySelector('input'); const msg=box.querySelector('.urlbox-msg');
  const codes=[...document.querySelectorAll('pre code')].filter(c=>c.textContent.indexOf('WEB_APP_URL')!==-1);
  if(!input||!codes.length) return;
  codes.forEach(c=>{ if(!c.dataset.orig) c.dataset.orig=c.textContent; });
  function rehl(c){ try{ if(window.hljs){ c.removeAttribute('data-highlighted'); hljs.highlightElement(c); } }catch(e){} }
  function apply(){
    const url=input.value.trim();
    if(!url){
      codes.forEach(c=>{ c.textContent=c.dataset.orig; rehl(c); });
      msg.innerHTML=''; try{localStorage.removeItem('ch6_webapp_url');}catch(e){}
      return;
    }
    if(!/^https:\/\/script\.google\.com\/[A-Za-z0-9_\/.\-]+\/exec$/.test(url)){
      msg.innerHTML='<span class="ub-warn">⚠ 주소를 다시 확인하세요 — <b>https://script.google.com/…</b>으로 시작해 <b>/exec</b>로 끝나야 해요. (Apps Script 편집기 주소나 디플로이 ID가 아니에요!)</span>';
      return;
    }
    codes.forEach(c=>{
      c.textContent=c.dataset.orig.replace(/WEB_APP_URL = "[^"]*"/, 'WEB_APP_URL = "'+url+'"');
      rehl(c);
    });
    msg.innerHTML='<span class="ub-ok">✅ 아래 2단계 완성 코드에 주소가 자동으로 들어갔어요 — 이제 <b>복사</b> 버튼만 누르면 됩니다.</span><br>'
      +'<a class="ub-test" href="'+url+'?value=99" target="_blank" rel="noopener">🧪 브라우저 테스트 열기 (?value=99) — 시트에 줄이 생기면 성공!</a>';
    try{localStorage.setItem('ch6_webapp_url',url);}catch(e){}
  }
  input.addEventListener('input',apply);
  try{ const saved=localStorage.getItem('ch6_webapp_url'); if(saved){ input.value=saved; apply(); } }catch(e){}
});
// 목차 드로어 (모든 화면 폭에서 동일하게 동작)
const sb=document.getElementById('sidebar'),scrim=document.getElementById('scrim'),mb=document.getElementById('menuBtn');
function toggle(o){sb.classList.toggle('open',o);scrim.classList.toggle('show',o);}
mb.addEventListener('click',()=>toggle(!sb.classList.contains('open')));
scrim.addEventListener('click',()=>toggle(false));
sb.addEventListener('click',e=>{if(e.target.closest('a'))toggle(false);});
const secs=[...document.querySelectorAll('.sec, .chapter')];
const links=new Map();
document.querySelectorAll('.nav-sec,.nav-ch-link').forEach(a=>links.set(a.dataset.target,a));
const io=new IntersectionObserver(es=>{
  es.forEach(e=>{if(e.isIntersecting){
    document.querySelectorAll('.nav-sec.active').forEach(x=>x.classList.remove('active'));
    const l=links.get(e.target.id); if(l&&l.classList.contains('nav-sec'))l.classList.add('active');
  }});
},{rootMargin:'-10% 0px -80% 0px',threshold:0});
secs.forEach(s=>io.observe(s));
</script>
</body>
</html>'''

# === BUILD_MARKER: 이 아래는 파일 쓰기 — build_ml_site.py는 이 마커 앞까지만 라이브러리로 재사용 ===
build(teacher=False)
build(teacher=True)
