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
  <text x="370" y="137" text-anchor="middle" font-size="11.5" fill="#8a8fb0">+ 그로브 베이스 쉴드</text>
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
  <text x="612" y="189" font-size="12.5" font-weight="700" fill="#2b2d3a">MQ-2 가스센서</text>
  <text x="612" y="207" font-size="10.5" fill="#8a8fa6">그로브 A0 = GP26 · ADC0</text>

  <!-- 범례 -->
  <text x="20" y="244" font-size="10.5" fill="#a7adc0">● 그로브 포트  ·  LED → D16(GP16, 디지털)  ·  MQ-2 → A0(GP26, 아날로그)</text>
</svg></div>'''

# API = 관공서 등본 발급 비유 (애니메이션 SVG)
API_ANALOGY_SVG = '''<p style="margin:0 0 12px">API는 <b>‘데이터를 가진 기관에 정해진 양식으로 신청하면, 정해진 형식으로 발급해 주는 창구’</b>예요. 동사무소에서 <b>등본</b> 떼는 것과 똑같죠 👇</p>
<svg class="api-svg" viewBox="0 0 760 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="API를 관공서 등본 발급에 빗댄 요청-응답 흐름도">
  <defs>
    <marker id="aR" markerWidth="10" markerHeight="10" refX="7" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#5B6CF0"/></marker>
    <marker id="aL" markerWidth="10" markerHeight="10" refX="7" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#E0568A"/></marker>
    <filter id="ds2" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#2a3568" flood-opacity="0.12"/></filter>
  </defs>

  <!-- 나(민원인) -->
  <g filter="url(#ds2)"><rect x="20" y="120" width="182" height="96" rx="18" fill="#ffffff" stroke="#e6e8f2"/></g>
  <text x="111" y="160" text-anchor="middle" font-size="34">🙋</text>
  <text x="111" y="187" text-anchor="middle" font-size="13" font-weight="800" fill="#2b2d3a">나 = 민원인</text>
  <text x="111" y="205" text-anchor="middle" font-size="11" fill="#8a8fa6">피코 · 브라우저</text>

  <!-- API 서버(관공서) -->
  <g filter="url(#ds2)"><rect x="558" y="120" width="182" height="96" rx="18" fill="#eef0ff" stroke="#c3c9f5"/></g>
  <text x="649" y="158" text-anchor="middle" font-size="32">🏛️</text>
  <text x="649" y="185" text-anchor="middle" font-size="12.5" font-weight="800" fill="#3b47c2">API = 관공서 창구</text>
  <text x="649" y="203" text-anchor="middle" font-size="11" fill="#8a8fb0">Open-Meteo · 기상청 …</text>

  <!-- 요청(위, 오른쪽으로) -->
  <line x1="204" y1="151" x2="554" y2="151" stroke="#c8cdf5" stroke-width="3" marker-end="url(#aR)"/>
  <rect x="292" y="121" width="178" height="27" rx="13" fill="#eef0ff" stroke="#c3c9f5"/>
  <text x="381" y="139" text-anchor="middle" font-size="12" font-weight="700" fill="#3b47c2">📝 요청 = 신청서(URL)</text>
  <circle r="6" cy="151" fill="#5B6CF0">
    <animate attributeName="cx" values="212;546" dur="2.6s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;1;1;0" dur="2.6s" repeatCount="indefinite"/>
  </circle>

  <!-- 응답(아래, 왼쪽으로) -->
  <line x1="554" y1="186" x2="204" y2="186" stroke="#f3cfe0" stroke-width="3" marker-end="url(#aL)"/>
  <rect x="286" y="189" width="190" height="27" rx="13" fill="#fff0f6" stroke="#f3cfe0"/>
  <text x="381" y="207" text-anchor="middle" font-size="12" font-weight="700" fill="#b83d72">📦 응답 = 발급 서류(JSON)</text>
  <circle r="6" cy="186" fill="#E0568A">
    <animate attributeName="cx" values="546;212" dur="2.6s" begin="1.3s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;1;1;0" dur="2.6s" begin="1.3s" repeatCount="indefinite"/>
  </circle>

  <!-- 보조 설명 -->
  <text x="381" y="244" text-anchor="middle" font-size="11" fill="#8a8fa6">🔑 일부 API(예: NASA)는 ‘신분증=키’가 있어야 발급</text>
  <text x="381" y="270" text-anchor="middle" font-size="11" fill="#7a7f95">신청서에 ‘무엇을(강수확률)·어디를(위도·경도)’ 적어 보내면 → 정해진 형식(JSON)으로 받아요</text>
</svg>
<p style="margin:12px 0 0;font-size:12.5px;color:#7a7f95">관공서=서버 · 신청서=요청(URL) · 서류=응답(JSON) · 양식=규칙 · 신분증=API 키. 우리 코드는 ‘피코가 <b>오늘 강수확률 등본</b>을 떼 오는 것’ — <b>정보과학</b>(요청→응답)과 <b>과학</b>(데이터 탐구)이 만나는 지점이에요.</p>'''

# ===================================================================
#  콘텐츠 정의
# ===================================================================
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
        "그로브(Grove) <b>베이스 쉴드</b>",
        "<b>WS2813 LED 바</b> (10개짜리) + 그로브 케이블",
        "<b>MQ-2 가스센서</b> 모듈 + 그로브 케이블",
        "데이터 전송이 되는 <b>USB 케이블</b> (충전 전용 케이블 ✗)",
        "Windows 또는 macOS 컴퓨터",
      ]},
      {"type": "callout", "kind": "warn", "title": "USB 케이블 주의",
       "html": "세상에는 ‘충전만 되는’ USB 케이블이 의외로 많아요. 피코가 컴퓨터에 인식되지 않으면, 가장 먼저 <b>다른 케이블</b>로 바꿔 보세요. 이게 연수 현장에서 제일 흔한 막힘 지점입니다."},
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
        {"sym": "설치 파일이 백신/보안 경고로 막힘", "cause": "다운로드 직후 일부 백신이 과민 반응합니다.", "fix": "공식 사이트(thonny.org)에서 받았다면 안전합니다. ‘허용’ 또는 ‘추가 정보 → 실행’을 선택하세요."},
      ]},
    ]},
    {"title": "0.3 · 하드웨어 조립", "items": [
      {"type": "text", "html": "그로브 베이스 쉴드는 피코 위에 ‘덮어 끼우는’ 확장 보드예요. 센서를 납땜 없이 케이블로 톡 꽂을 수 있게 해 줍니다. 아래 그림처럼 연결합니다."},
      {"type": "figure_hw"},
      {"type": "steps", "items": [
        {"t": "피코를 그로브 쉴드에 꽂기", "d": "핀 방향을 맞춰 피코를 쉴드에 끝까지 눌러 끼웁니다. <b>USB 단자가 쉴드 바깥쪽을 향하도록</b> 방향을 확인하세요. 한 줄이라도 핀이 어긋나면 안 됩니다."},
        {"t": "LED 바 → D16 포트", "d": "WS2813 LED 바의 그로브 케이블을 쉴드의 <b>D16</b> 포트에 꽂습니다. (코드에서는 GP16)"},
        {"t": "MQ-2 센서 → A0 포트", "d": "MQ-2 가스센서의 그로브 케이블을 쉴드의 <b>A0</b> 포트에 꽂습니다. (코드에서는 GP26 / ADC0)"},
        {"t": "USB로 컴퓨터에 연결", "d": "USB 케이블로 피코와 컴퓨터를 연결합니다. (펌웨어를 처음 설치할 때는 0.4의 BOOTSEL 순서를 따르세요)"},
      ]},
      {"type": "callout", "kind": "warn", "title": "꽂는 위치를 헷갈리지 마세요",
       "html": "D16(디지털)과 A0(아날로그)는 쓰임이 다릅니다. LED는 <b>D16</b>, 가스센서는 <b>A0</b>. 반대로 꽂으면 값이 이상하거나 LED가 안 켜져요."},
    ]},
    {"title": "0.4 · MicroPython 펌웨어 설치", "items": [
      {"type": "text", "html": "갓 산 피코에는 아직 파이썬을 실행할 ‘속살’이 없어요. <b>MicroPython 펌웨어</b>를 한 번 설치하면, 그때부터 피코가 파이썬 코드를 알아듣습니다. (처음 한 번만 하면 됩니다)"},
      {"type": "raw", "html": FW_CARD},
      {"type": "dig", "title": "펌웨어? MicroPython? BOOTSEL? — 용어 정리",
       "html": "<b>펌웨어(firmware)</b>는 어떤 기기를 켰을 때 가장 먼저 돌아가는 ‘기본 소프트웨어’예요. 컴퓨터의 운영체제(윈도우·macOS)에 해당하는, 피코의 속살이라고 보면 됩니다.<br><br><b>MicroPython</b>은 피코 같은 작은 컴퓨터(마이크로컨트롤러)에서 돌아가도록 만든 <b>파이썬</b>이에요. 이 펌웨어를 설치하면, 그때부터 피코가 우리가 쓴 파이썬 코드를 알아듣습니다. (C/C++로도 쓸 수 있지만, 파이썬이 가장 쉬워요.)<br><br><b>BOOTSEL 버튼</b>은 피코를 ‘펌웨어를 새로 받을 준비(부트로더) 모드’로 켜는 버튼이에요. 이 버튼을 누른 채 USB를 꽂으면 컴퓨터에 USB 드라이브처럼 나타나고, 거기에 <code>.uf2</code> 파일을 끌어다 놓으면 설치됩니다.<br><br><b>.uf2</b>는 이런 보드에 드래그&드롭으로 펌웨어를 넣도록 만든 파일 형식(USB Flashing Format)입니다."},
      {"type": "mistakes", "items": [
        {"sym": "RP2350 드라이브가 안 나타남", "cause": "BOOTSEL 버튼을 누르지 않고 꽂았거나, 충전 전용 케이블입니다.", "fix": "케이블을 뽑고 → <b>BOOTSEL 버튼을 누른 채</b> 다시 꽂으세요. 그래도 안 되면 데이터용 케이블로 교체합니다."},
      ]},
    ]},
    {"title": "0.5 · Thonny와 피코 연결 + 첫 코드", "items": [
      {"type": "steps", "items": [
        {"t": "인터프리터 선택", "d": "Thonny 오른쪽 <b>아래 구석</b>을 클릭 → <b>‘MicroPython (Raspberry Pi Pico)’</b>를 고릅니다. 포트는 보통 자동으로 잡혀요."},
        {"t": "셸에서 인사해 보기", "d": "아래 Shell 칸에 다음을 한 줄 입력하고 Enter."},
      ]},
      {"type": "code", "label": "셸에 직접 입력", "lang": "python", "file": "snippets/ch0_hello.py"},
      {"type": "text", "html": "<code>안녕, 피코!</code>가 셸에 찍히면, 컴퓨터와 피코가 <b>대화에 성공</b>한 거예요. 🎉 이제 보드 위 작은 LED를 깜빡여 봅시다."},
      {"type": "code", "label": "보드 LED 깜빡이기", "lang": "python", "file": "snippets/ch0_blink.py"},
      {"type": "callout", "kind": "tip", "title": "main.py로 저장하면 자동 실행",
       "html": "이 코드를 피코에 <b>main.py</b>라는 이름으로 저장하면(파일 → 저장 → Raspberry Pi Pico), 다음부터 전원만 넣어도 코드가 저절로 돌아갑니다. 멈추려면 Thonny에서 ⏹(정지) 또는 Ctrl+C."},
      {"type": "mistakes", "items": [
        {"sym": "포트/장치가 목록에 안 보임", "cause": "펌웨어 미설치, 또는 케이블 문제.", "fix": "0.4를 다시 확인하고, 케이블을 데이터용으로 바꾸세요. Thonny를 재시작하면 잡히기도 합니다."},
        {"sym": "코드를 멈출 수 없음 (무한 반복)", "cause": "<code>while True</code>는 일부러 무한 반복합니다.", "fix": "Thonny의 ⏹ 정지 버튼을 누르거나 셸에서 Ctrl+C."},
      ]},
      {"type": "check", "items": [
        {"q": "Thonny에서 셸(Shell) 칸은 무슨 역할을 하나요?", "a": "코드를 한 줄씩 바로 실행해 보고, 피코가 print로 보낸 메시지를 보여 주는 ‘대화창’입니다."},
        {"q": "펌웨어는 매번 설치해야 하나요?", "a": "아니요. 처음 한 번만 설치하면 계속 유지됩니다."},
        {"q": "보드 LED를 코드에서 어떻게 가리켰나요?", "a": "<code>Pin(\"LED\", Pin.OUT)</code> — 피코 보드에 내장된 LED를 출력 모드로 잡았습니다."},
      ]},
    ]},
  ],
},
# ----------------------------------------------------------------- CH1
{
  "id": "ch1", "num": "01", "title": "와이파이 센서 대시보드", "accent": "#E0568A",
  "subtitle": "피코를 와이파이에 연결하고, 신호 세기(RSSI)를 스마트폰 브라우저에서 실시간 그래프로 봅니다. 첫 IoT 작품이에요.",
  "goals": [
    "피코를 와이파이(STA 모드)에 연결할 수 있다",
    "신호 세기(RSSI)가 무엇이고 어떻게 읽는지 안다",
    "피코를 작은 웹서버로 만들어 브라우저에서 데이터를 본다",
    "‘피코는 /data로 값만 주고, 그래프는 브라우저가 그린다’는 구조를 이해한다",
  ],
  "why": "센서 값을 셸에서만 보면 나만 볼 수 있죠. 하지만 피코가 <b>웹서버</b>가 되면, 같은 와이파이에 있는 누구나 스마트폰으로 실시간 값을 볼 수 있어요. 이 장에서 익히는 <b>‘피코=서버, 브라우저=화면’</b> 구조는 뒤의 날씨·가스 대시보드에서도 똑같이 재사용됩니다.",
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
    ]},
    {"title": "따라하기", "items": [
      {"type": "step_head", "html": "<b>Step 1.</b> 주변에 어떤 와이파이가 있는지 스캔해 봅니다. (셸에서 실행)"},
      {"type": "code", "label": "Step 1 · 와이파이 스캔", "lang": "python", "file": "snippets/ch1_scan.py"},
      {"type": "step_head", "html": "<b>Step 2.</b> 와이파이 이름·비밀번호를 <b>wifi_config.py</b>라는 별도 파일로 저장합니다. (피코에 새 파일로 저장!) 와이파이를 쓰는 코드는 모두 이 파일을 함께 씁니다."},
      {"type": "code", "label": "Step 2 · wifi_config.py (따로 저장)", "lang": "python", "file": "snippets/wifi_config.py"},
      {"type": "step_head", "html": "<b>Step 3.</b> 와이파이에 연결하고 신호 세기를 1초마다 출력합니다. (손코딩으로 원리 확인)"},
      {"type": "code", "label": "Step 3 · RSSI 읽기", "lang": "python", "file": "snippets/ch1_rssi.py"},
      {"type": "step_head", "html": "<b>Step 4.</b> 이제 이 값을 웹으로 봅니다. 아래는 <b>복사해서 main.py로 저장하면 바로 도는</b> 완결형 대시보드예요. 실행 후 셸에 찍힌 <code>http://...</code> 주소를 같은 와이파이의 스마트폰에서 열어 보세요."},
      {"type": "code", "label": "전체 코드 · RSSI 실시간 대시보드 (main.py)", "lang": "python", "file": "snippets/ch1_dashboard.py", "fold": True},
      {"type": "step_head", "html": "<b>Step 5.</b> 여기서 <b>바이브코딩으로 마무리</b>해 봐요. 숫자만 보여 주는 대신, 신호 세기에 따라 <b>재미있게 반응</b>하도록 AI에게 부탁합니다. 아래 프롬프트를 그대로 복사해 AI 도구에 붙여넣으세요."},
      {"type": "prompt", "label": "AI에게 이렇게 부탁해 보세요 (그대로 복사)", "text":
"내 라즈베리파이 피코 2 W가 지금 와이파이 신호 세기(RSSI)를 측정해서 소켓 기반 웹서버로 보여주고 있어. RSSI는 dBm 단위의 음수이고 0에 가까울수록 강해(예: -50은 강함, -85는 약함). 와이파이 정보는 wifi_config.py(WIFI_SSID, WIFI_PASSWORD)에서 불러와.\n신호 세기에 따라 화면이 재미있게 반응하도록 바꿔 줘:\n- 강할 때(약 -60dBm 이상): 초록색 + ‘신호 최고예요! 😄’ 같은 축하 느낌(살짝 반짝).\n- 보통(-60 ~ -78dBm): 노란색 + ‘쓸 만해요’.\n- 약할 때(약 -78dBm 이하): 빨간색 + ‘⚠️ 신호 약함 — 끊길 수 있어요’ 경고를 크게 띄우고 화면이 살짝 흔들리는 애니메이션.\n그리고 WS2813 LED 10개(GP16, NeoPixel을 timing=(280,515,515,745)로 생성)가 연결돼 있다면, 같은 상태를 LED 색으로도 보여 줘(강함=초록, 보통=노랑, 약함=빨강 깜빡).\n복사해서 바로 도는 완결형 main.py로 주고, 핀·timing 설정은 그대로 유지해 줘."},
      {"type": "callout", "kind": "tip", "title": "바이브코딩 팁",
       "html": "받은 코드를 올리기 전에 ① 신호 기준값(-60·-78 등)이 우리 환경에 맞는지 ② LED를 쓴다면 <code>timing</code> 인자가 들어 있는지 확인하세요. 기준값은 직접 돌아다니며 ‘강한 곳/약한 곳’ RSSI를 보고 조정하면 더 정확해요."},
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
  "id": "ch2", "num": "02", "title": "LED 10개 다루기", "accent": "#1F9D63",
  "subtitle": "WS2813 LED 바(10개)를 색과 밝기로 자유롭게 제어합니다. 다음 장 ‘날씨 시계’의 준비 운동이에요.",
  "goals": [
    "NeoPixel로 LED 한 칸·전체를 원하는 색으로 켤 수 있다",
    "WS2813에 꼭 필요한 timing 인자를 이해한다",
    "10칸에 무지개·게이지를 표현할 수 있다",
  ],
  "why": "LED는 ‘숫자를 빛으로 바꾸는’ 가장 직관적인 출력 장치예요. 강수확률·가스 농도 같은 데이터를 색으로 보여 주면 한눈에 들어오죠. 이 장에서 10칸을 다루는 법을 익히면, 3장에서 ‘오늘의 비 예보’를 10칸 LED 시계로 만들 수 있어요.",
  "sections": [
    {"title": "핵심 개념 — timing이 진짜 중요해요", "items": [
      {"type": "callout", "kind": "key", "title": "WS2813은 timing 인자가 필수",
       "html": "우리가 쓰는 LED는 <b>WS2813</b> 계열이라, MicroPython NeoPixel의 <b>기본 타이밍과 안 맞습니다.</b> 그대로 두면 색이 깨지거나 엉뚱한 칸이 켜져요. 그래서 반드시 이렇게 만듭니다:<br><br><code>TIMING = (280, 515, 515, 745)</code><br><code>np = NeoPixel(Pin(16), 10, timing=TIMING)</code><br><br>이 네 숫자는 0/1 신호의 길이(나노초)예요. 이번 연수의 모든 LED 코드 첫 줄에 들어갑니다."},
      {"type": "callout", "kind": "info", "title": "LED가 60개짜리로 왔다면?",
       "html": "걱정 마세요. 바꿀 곳은 <b>딱 한 줄</b>이에요. 코드 위쪽의 <code>NUM = 10</code>을 <code>NUM = 60</code>으로 바꾸면 끝입니다. (timing·핀은 그대로) <code>fill</code>·무지개·게이지·날씨 시계 모두 <code>NUM</code>을 기준으로 돌아서 자동으로 60칸에 맞춰집니다. 단, 60칸을 밝게 켜면 전류를 많이 먹으니 밝기는 더 낮춰 주세요."},
      {"type": "concept", "items": [
        {"t": "NeoPixel", "d": "여러 개의 색 LED를 한 줄로 제어하는 도구. <code>np[i] = (r, g, b)</code>로 i번 칸 색을 정합니다."},
        {"t": "write()", "d": "색을 정한 뒤 <code>np.write()</code>를 호출해야 실제 LED에 반영됩니다. 깜빡 잊기 쉬워요."},
        {"t": "칸 번호 0~9", "d": "10개니까 <code>np[0]</code>부터 <code>np[9]</code>까지. 0부터 시작!"},
        {"t": "밝기는 낮게", "d": "(255,255,255)는 너무 밝고 전류도 많이 써요. (30,30,30) 정도면 충분히 보입니다."},
      ]},
      {"type": "dig", "title": "timing=(280, 515, 515, 745)의 정체 (1선 통신과 GRB)",
       "html": "WS2813 같은 LED는 칸이 10개여도 <b>데이터 선이 하나</b>뿐이에요. 그래서 0과 1을 <b>‘펄스(전기 신호)의 길이’</b>로 구분합니다. 이게 <b>1-wire(원-와이어) 프로토콜</b>이에요.<br><br>네 숫자는 <b>나노초(ns, 10억분의 1초)</b> 단위의 시간이고, 각각:<br>· <b>T0H</b>=280 — ‘0’을 보낼 때 켜 두는 시간<br>· <b>T0L</b>=515 — ‘0’을 보낼 때 꺼 두는 시간<br>· <b>T1H</b>=515 — ‘1’을 보낼 때 켜 두는 시간<br>· <b>T1L</b>=745 — ‘1’을 보낼 때 꺼 두는 시간<br><br>이 길이가 칩이 기대하는 값과 안 맞으면 0을 1로, 1을 0으로 잘못 읽어 <b>색이 깨집니다.</b> 칩 종류마다 기대 시간이 조금씩 달라, WS2813엔 이 네 값을 직접 지정해 주는 거예요.<br><br>또 하나, 사람은 색을 (빨강, 초록, 파랑) = RGB 순서로 생각하지만 이 LED는 내부적으로 <b>GRB(초록·빨강·파랑) 순서</b>로 데이터를 받습니다. 대부분의 펌웨어에서는 <code>(r, g, b)</code>로 쓰면 되지만, 혹시 빨강·초록이 바뀌어 보이면 순서를 조정하면 돼요."},
    ]},
    {"title": "따라하기", "items": [
      {"type": "step_head", "html": "<b>Step 1.</b> 한 칸만 켜 보기."},
      {"type": "code", "label": "Step 1 · 한 칸 켜기", "lang": "python", "file": "snippets/ch2_basic.py"},
      {"type": "step_head", "html": "<b>Step 2.</b> 전체를 한 색으로 — 반복문으로 모든 칸을 칠하는 <code>fill</code> 함수."},
      {"type": "code", "label": "Step 2 · 전체 한 색 (fill)", "lang": "python", "file": "snippets/ch2_fill.py"},
      {"type": "step_head", "html": "<b>Step 3.</b> 10칸에 무지개 펼치기 (HSV로 색상환 한 바퀴)."},
      {"type": "code", "label": "Step 3 · 무지개 10칸", "lang": "python", "file": "snippets/ch2_rainbow.py"},
      {"type": "step_head", "html": "<b>Step 4.</b> 켜진 칸 수로 양을 나타내는 <b>게이지</b> — 다음 장의 핵심 기법이에요."},
      {"type": "code", "label": "전체 코드 · 게이지 차오르기", "lang": "python", "file": "snippets/ch2_gauge.py"},
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
# ----------------------------------------------------------------- CH3
{
  "id": "ch3", "num": "03", "title": "날씨 비 예보 대시보드", "accent": "#3B82F6",
  "subtitle": "인터넷에서 오늘의 강수확률을 받아, 6시~23시를 10개 LED에 담는 ‘날씨 시계’를 만들고, 같은 데이터를 보여 주는 웹 대시보드까지 완성합니다.",
  "goals": [
    "Open-Meteo에서 강수확률 데이터를 받아올 수 있다",
    "받은 데이터(JSON)에서 시간대별 강수확률을 꺼낼 수 있다",
    "6시~23시의 강수확률을 10개 LED의 색으로 표현할 수 있다",
    "LED와 똑같은 정보를 보여 주는 웹 대시보드(색 범례 포함)를 띄울 수 있다",
  ],
  "why": "여기서부터 진짜 ‘세상의 데이터’를 다룹니다. 무료 날씨 API <b>Open-Meteo</b>에서 오늘의 강수확률을 받아, 거실의 LED 바가 <b>아침부터 밤까지 비 올 시간을 색으로 알려 주는 시계</b>가 됩니다. 출근 전 LED만 보고 우산을 챙길 수 있죠.",
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
      {"type": "step_head", "html": "<b>Step 2.</b> 강수확률을 받아 셸에 출력해 봅니다. (손코딩 — 데이터가 어떻게 생겼는지 확인)"},
      {"type": "code", "label": "Step 2 · 강수확률 받아오기", "lang": "python", "file": "snippets/ch3_fetch.py"},
      {"type": "step_head", "html": "<b>Step 3.</b> 받은 값을 10개 LED의 색으로 바꿉니다. 아래가 <b>복사하면 바로 도는</b> 완결형 ‘날씨 시계’예요. (추가 설치 없음 · 10분마다 새 예보로 갱신)"},
      {"type": "code", "label": "전체 코드 · 날씨 시계 (main.py) — 무설치", "lang": "python", "file": "snippets/ch3_full.py", "fold": True},
      {"type": "callout", "kind": "tip", "title": "더 짧게 쓰고 싶다면 — requests 버전 (설치 1회)",
       "html": "위 무설치 버전이 기본이에요. 만약 <code>requests</code>를 설치할 수 있는 환경이라면, HTTP 부분을 훨씬 짧게 쓸 수 있습니다. Thonny <b>도구 → 패키지 관리</b>에서 <code>requests</code>를 한 번 설치(피코가 와이파이 연결된 상태)한 뒤 아래 버전을 쓰세요. 동작은 똑같습니다."},
      {"type": "code", "label": "대안 · 날씨 시계 (requests 설치 버전)", "lang": "python", "file": "snippets/ch3_full_requests.py", "fold": True},
      {"type": "step_head", "html": "<b>Step 4.</b> 직접 만들어 보고 싶다면, 아래 프롬프트를 <b>그대로 복사해 AI 도구(Claude 등)에 붙여넣으세요.</b> 교재를 모르는 AI도 바로 작업할 수 있게, 필요한 정보가 모두 들어 있습니다."},
      {"type": "prompt", "label": "AI에게 이렇게 부탁해 보세요 (그대로 복사)", "text":
"라즈베리파이 피코 2 W에서 도는 MicroPython 코드를 만들어 줘.\n[지금 하는 일] Open-Meteo API에서 오늘의 시간별 강수확률을 받아, WS2813 LED 10개에 6시~23시를 색으로 표시하고 있어. LED는 GP16에 연결했고 NeoPixel을 timing=(280,515,515,745)로 만들어. 와이파이 정보는 wifi_config.py(WIFI_SSID, WIFI_PASSWORD)에서 불러와.\n[추가할 기능] 여기에 웹 대시보드를 더해 줘:\n- 피코가 직접 소켓 기반 웹서버가 되어 80번 포트에서 응답하게 해 줘(외부 라이브러리 없이).\n- 브라우저가 /data 주소에서 JSON을 주기적으로 받아 화면을 자동 갱신하게 해 줘.\n- 같은 와이파이의 스마트폰에서 접속하면 6시~23시 강수확률을 막대그래프로 보여 주고, 색의 의미(범례)도 함께 표시해 줘.\n- LED와 웹이 같은 데이터를 쓰고, 날씨 데이터는 10분에 한 번만 새로 받아와 줘(피코가 버겁지 않게).\n[조건] 복사해서 바로 실행되는 완결형 main.py로 주고, 위도/경도(LAT/LON)와 timing 값은 내가 바꿔 쓸 수 있게 코드 맨 위에 둬 줘."},
      {"type": "callout", "kind": "tip", "title": "바이브코딩의 핵심",
       "html": "AI가 준 코드를 <b>그대로 믿지 말고</b>, ① timing 인자가 들어 있는지 ② 내 위도·경도를 쓰는지 ③ 너무 자주 API를 부르지 않는지 확인하세요. ‘동작을 우리말로 부탁 → 받은 코드를 내 기준으로 점검’이 바이브코딩의 리듬입니다."},
      {"type": "step_head", "html": "<b>Step 5.</b> 직접 부탁하지 않아도, 아래 <b>완성형 대시보드</b>를 바로 써도 됩니다. LED를 켜면서 동시에 웹서버가 되어, 스마트폰/PC로 접속하면 <b>피코 10칸과 똑같은 색의 칸 · 색의 뜻(범례) · 시간별 강수확률 막대</b>를 보여 줍니다. (무설치 · main.py로 저장)"},
      {"type": "code", "label": "전체 코드 · 날씨 LED + 웹 대시보드 (main.py)", "lang": "python", "file": "snippets/ch3_dashboard.py", "fold": True},
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
      {"type": "text", "html": "<b>Open-Meteo</b>는 독일의 비영리 프로젝트로, 여러 나라 기상청의 공개 수치예보 모델을 모아 누구나 쓸 수 있게 제공합니다. <b>API 키도, 회원가입도 필요 없고</b>, 비상업·교육용은 자유롭게 쓸 수 있어요. 주소(URL) 하나에 ‘어디(위도·경도)·무엇(변수)·언제(기간)’를 적어 보내면, 그 자리에서 JSON으로 답을 줍니다."},
      {"type": "concept", "items": [
        {"t": "여러 종류의 API", "d": "<b>forecast</b>(예보) · <b>archive</b>(1940년~ 과거 데이터) · <b>air-quality</b>(대기질) · <b>marine</b>(파고·해양) · <b>elevation</b>(고도). 주소의 앞부분만 바꾸면 됩니다."},
        {"t": "고를 수 있는 변수", "d": "기온 <code>temperature_2m</code> · 습도 <code>relative_humidity_2m</code> · 강수확률 <code>precipitation_probability</code> · 풍속 <code>windspeed_10m</code> · 기압 <code>surface_pressure</code> · 자외선 <code>uv_index</code> · 일사량 <code>shortwave_radiation</code>"},
        {"t": "응답(JSON) 구조", "d": "<code>hourly.time</code>(시각 배열)과 <code>hourly.기온</code>(값 배열)이 <b>같은 순서로 짝</b>을 이룹니다. 그래서 <code>값[6]</code>이 곧 그 날 6시 값이에요."},
        {"t": "기간 고르기", "d": "<code>forecast_days=1</code>(오늘) · <code>past_days=7</code>(지난 일주일) · archive는 <code>start_date</code>/<code>end_date</code>로 특정 기간."},
      ]},
      {"type": "dig", "title": "‘강수확률 60%’가 실제로 뜻하는 것",
       "html": "강수확률(POP, Probability of Precipitation)은 <b>그 시간·그 지역에 0.1mm 이상의 비가 내릴 통계적 확률</b>입니다. 비의 ‘양’이나 ‘세기’가 아니라 ‘올지 안 올지의 가능성’이에요.<br><br>흔한 오해 두 가지:<br>· ‘60%’는 <b>‘하늘의 60%에 비가 온다’</b>는 뜻이 아니에요.<br>· ‘비가 60% 세기로 온다’는 뜻도 아니에요.<br><br>예보 모델이 같은 조건을 여러 번 시뮬레이션했을 때 <b>10번 중 6번꼴로 비가 내렸다</b>는 의미에 가깝습니다. 그래서 강수확률이 높아도 실제로 안 올 수 있고, 낮아도 소나기가 올 수 있어요. 수업에서 ‘확률’과 ‘실제 관측’의 차이를 이야기하기 좋은 소재입니다."},
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
      {"type": "text", "html": "Open-Meteo 말고도 <b>무료에 대부분 키가 필요 없는</b> 과학 데이터 API가 많아요 — 지진·ISS·일출몰·우주날씨·물질(화학)·생물 등. 과목별로 <b>어떤 데이터를 주고 무엇을 탐구할 수 있는지</b>를 <b>부록 A</b>에 한눈에 정리했고, 브라우저에서 바로 받아 그려 보는 <b>라이브 대시보드(지도·그래프)</b>로도 만들어 뒀습니다(국내 적용 여부도 표시). 키 없이 동작하는 것만 골랐고, 2026년 기준 응답을 확인했어요."},
      {"type": "linkbtn", "href": "dashboards/index.html", "label": "오픈 API 라이브 대시보드 갤러리 열기 (11종)"},
      {"type": "callout", "kind": "key", "title": "🇰🇷 국내 공식 데이터가 필요하면 — 공공데이터포털",
       "html": "‘우리나라 공식 수치’가 필요한 수업(국내 지진·미세먼지·동네예보)이라면 <b>공공데이터포털(data.go.kr)</b>에서 무료 인증키를 받아 쓰세요. 글로벌 API보다 국내 정확도가 높습니다.<br>· <b>기상청 동네예보·지진통보</b> (data.go.kr) — 국내 공식 기상·지진<br>· <b>에어코리아(한국환경공단) 미세먼지</b> — 측정소별 실시간 PM2.5/PM10<br><span style='color:#a55'>※ 회원가입 + 서비스키 신청이 필요하고 응답 형식(XML/JSON)이 제각각이라, 초보 단계에선 키 없는 글로벌 API로 원리를 익힌 뒤 넘어오길 권합니다.</span>"},
      {"type": "callout", "kind": "info", "title": "피코로 가져올 때 한 가지",
       "html": "대부분 <b>https + JSON</b>이라, 3장의 <code>http_get_json()</code>(소켓+ssl) 함수를 그대로 써서 받을 수 있어요. 다만 응답이 큰 API(지진 전체 목록, NASA 이미지 등)는 피코 메모리에 부담이 될 수 있으니, <b>필요한 항목만 요청</b>하거나 수업에서는 컴퓨터(파이썬·브라우저)로 보여 주는 방법도 좋습니다."},
    ]},
  ],
},
# ----------------------------------------------------------------- CH4
{
  "id": "ch4", "num": "04", "title": "MQ-2 가스센서 대시보드", "accent": "#F59E0B",
  "subtitle": "공기 중 가스를 숫자로 읽고, 안전/주의/위험을 색과 그래프로 보여 주는 다크 테마 대시보드를 만듭니다.",
  "goals": [
    "ADC로 가스센서 값을 읽고 전압·비율로 바꿀 수 있다",
    "이동 평균으로 값을 안정시킬 수 있다",
    "임계값으로 안전/주의/위험 상태를 판단해 웹으로 보여 준다",
  ],
  "why": "공기질은 눈에 안 보이죠. MQ-2 센서로 측정해 <b>숫자 → 색 → 그래프</b>로 바꾸면, 환기 타이밍을 한눈에 알 수 있어요. 센서값을 ‘판단(임계값)’하고 피코가 웹서버가 되어 ‘예쁜 화면’으로 보여 주는, 가장 완성도 높은 대시보드입니다.",
  "sections": [
    {"title": "핵심 개념", "items": [
      {"type": "concept", "items": [
        {"t": "ADC (아날로그)", "d": "가스 농도 같은 ‘연속된 값’을 숫자로 바꿔 읽는 기능. 그로브 <b>A0 = GP26</b>. <code>ADC(Pin(26))</code>"},
        {"t": "read_u16()", "d": "0~65535 사이 값으로 읽습니다. 가스가 짙을수록 값이 커져요."},
        {"t": "이동 평균", "d": "여러 번 읽어 평균 내면 값이 출렁이지 않고 안정됩니다. <code>read_average()</code>"},
        {"t": "임계값", "d": "SAFE / WARNING / DANGER를 나누는 기준 숫자. 환경마다 달라 보정이 필요해요."},
      ]},
      {"type": "dig", "title": "ADC가 ‘전압’을 ‘숫자’로 바꾸는 원리 (볼트 변환)",
       "html": "센서는 가스 농도를 <b>전압(아날로그)</b>으로 내보냅니다. 0V~3.3V 사이의 ‘연속된’ 값이죠. 그런데 컴퓨터는 숫자만 다루니, 이 전압을 숫자로 바꿔야 합니다. 그 변환기가 <b>ADC(Analog-to-Digital Converter, 아날로그→디지털 변환기)</b>예요.<br><br>피코의 ADC는 <b>16비트</b> 해상도로 읽습니다. 16비트 = 2¹⁶ = <b>65536단계</b>, 그래서 <code>read_u16()</code>은 <b>0 ~ 65535</b> 사이 숫자를 돌려줘요.<br>· 0V → 0<br>· 3.3V(최대) → 65535<br>· 그 사이는 비례. 따라서 숫자를 전압으로 되돌리면:<br><code>전압(V) = read_u16() / 65535 × 3.3</code><br><br>예) 읽은 값이 32768이면 → 32768/65535×3.3 ≈ <b>1.65V</b> (딱 절반).<br><br><b>주의:</b> MQ-2에서 ‘전압이 곧 가스 농도(ppm)’는 아닙니다. 정확한 ppm은 보정·계산이 필요해서, 수업에서는 <b>상대적인 변화(평소보다 높다/낮다)</b>를 보는 지표로 씁니다. 그래서 SAFE/WARNING/DANGER 임계값도 우리 교실에서 직접 보고 정합니다."},
      {"type": "callout", "kind": "info", "title": "센서는 예열이 필요해요",
       "html": "MQ-2는 전원을 넣고 <b>1~2분</b> 지나야 값이 안정됩니다. 처음 켜자마자 값이 크게 나와도 놀라지 마세요."},
      {"type": "callout", "kind": "info", "title": "먼저 — 와이파이 정보 파일 만들기 (wifi_config.py)",
       "html": "대시보드 코드는 와이파이 정보를 <code>wifi_config.py</code>에서 불러옵니다. <b>main.py와 같은 위치</b>에 이 파일을 새로 만들고 두 줄만 적어 저장하세요.<br><br><code>WIFI_SSID = \"우리_와이파이_이름\"</code><br><code>WIFI_PASSWORD = \"비밀번호\"</code><br><br>(피코는 <b>2.4GHz</b> 와이파이만 됩니다.)"},
    ]},
    {"title": "따라하기", "items": [
      {"type": "step_head", "html": "<b>Step 1.</b> 값 한 번 읽기. (그로브 A0에 센서를 꽂았는지 확인!)"},
      {"type": "code", "label": "Step 1 · 한 번 읽기", "lang": "python", "file": "snippets/ch4_01_read.py"},
      {"type": "step_head", "html": "<b>Step 2.</b> 반복해서 읽고, Thonny <b>플로터</b>로 그래프 보기. (셸 옆 ‘Plotter’ 켜기)"},
      {"type": "code", "label": "Step 2 · 반복 읽기 (플로터)", "lang": "python", "file": "snippets/ch4_02_loop.py"},
      {"type": "step_head", "html": "<b>Step 3.</b> 원시값을 전압·비율로 바꿔 의미를 부여합니다."},
      {"type": "code", "label": "Step 3 · 전압·비율 변환", "lang": "python", "file": "snippets/ch4_03_convert.py"},
      {"type": "step_head", "html": "<b>Step 4.</b> 완성형 대시보드. <b>복사해서 main.py로 저장</b>하면, 이동 평균·임계값·다크 테마 그래프가 모두 들어간 모니터가 됩니다. (wifi_config.py 필요)"},
      {"type": "code", "label": "전체 코드 · MQ-2 실시간 대시보드 (main.py)", "lang": "python", "file": "snippets/ch4_dashboard.py", "fold": True},
    ]},
    {"title": "자주 하는 실수", "items": [
      {"type": "mistakes", "items": [
        {"sym": "값이 늘 0이거나 65535에 붙어 있음", "cause": "센서를 A0가 아닌 다른 포트에 꽂음.", "fix": "그로브 <b>A0(=GP26)</b>에 꽂았는지 확인하세요. D포트에 꽂으면 아날로그 값을 못 읽습니다."},
        {"sym": "켜자마자 ‘위험’으로 뜸", "cause": "예열 전이라 값이 큼.", "fix": "1~2분 기다리세요. 그래도 항상 위험이면 임계값(SAFE/WARNING/DANGER 숫자)을 우리 환경에 맞게 올리세요."},
        {"sym": "ImportError: wifi_config", "cause": "<code>wifi_config.py</code>가 피코에 없음.", "fix": "main.py와 같은 위치에 <code>wifi_config.py</code> 파일을 새로 만들어 두 줄만 적으세요. <code>WIFI_SSID = \"와이파이이름\"</code> / <code>WIFI_PASSWORD = \"비밀번호\"</code> (위 핵심 개념의 안내 참고)."},
      ]},
    ]},
    {"title": "스스로 점검하기", "items": [
      {"type": "check", "items": [
        {"q": "MQ-2는 그로브의 어느 포트에 꽂나요?", "a": "A0 (= GP26 = ADC0). 아날로그 포트입니다."},
        {"q": "값을 안정시키는 read_average는 무엇을 하나요?", "a": "여러 번(기본 10번) 읽어 평균을 냅니다. 출렁임이 줄어요."},
        {"q": "임계값은 어디서나 같은 숫자를 쓰면 되나요?", "a": "아니요. 센서·환경마다 기준이 달라, 우리 교실에서 직접 보고 보정해야 합니다."},
      ]},
    ]},
  ],
},
# ----------------------------------------------------------------- CH5
{
  "id": "ch5", "num": "05", "title": "자유 프로젝트", "accent": "#8B5CF6",
  "subtitle": "지금까지 배운 LED·센서·웹·날씨 API를 조합해, 나만의 작품을 바이브코딩으로 완성합니다.",
  "goals": [
    "여러 기능을 조합해 새 작품을 기획할 수 있다",
    "AI에게 명확하게 부탁하고, 받은 코드를 점검할 수 있다",
  ],
  "why": "도구는 다 익혔어요. 이제 <b>‘무엇을 만들까’</b>가 남았습니다. 작은 아이디어 하나면 충분해요. 아래 아이디어와 프롬프트 틀을 출발점으로 삼아, 우리 교실·우리 집에 쓸모 있는 작품을 만들어 보세요.",
  "sections": [
    {"title": "아이디어 모음", "items": [
      {"type": "ideas", "items": [
        {"t": "🌧️ 우산 알리미", "d": "날씨 시계(3장)에서 오늘 강수확률이 60% 넘는 시간대가 있으면, 현관 LED를 파랑으로 깜빡여 ‘우산 챙겨!’"},
        {"t": "🌬️ 스마트 환기등", "d": "가스센서(4장) 값이 WARNING을 넘으면 LED를 노랑→빨강으로, 웹에 ‘환기하세요’ 알림."},
        {"t": "📶 와이파이 약한 자리 찾기", "d": "RSSI 대시보드(1장)를 들고 다니며 집에서 신호가 약한 곳을 LED 게이지로 탐색."},
        {"t": "🌡️ 오늘 날씨 무드등", "d": "강수확률 대신 기온을 받아(Open-Meteo) 더우면 빨강, 추우면 파랑으로 방 전체 분위기 표현."},
      ]},
    ]},
    {"title": "AI에게 잘 부탁하는 틀", "items": [
      {"type": "text", "html": "막연히 ‘만들어 줘’보다, <b>① 지금 상태 → ② 추가할 동작 → ③ 제약(핀·timing·갱신주기)</b>을 함께 주면 훨씬 정확한 코드를 받습니다."},
      {"type": "prompt", "label": "프롬프트 틀 (복사해서 채우세요)", "text":
"[지금 상태] 내 피코는 지금 ____ 를 하고 있어. (예: Open-Meteo 강수확률을 10개 LED에 표시)\n[하드웨어] WS2813 LED 10개는 Pin 16, timing=(280,515,515,745) / MQ-2는 ADC Pin 26 / 와이파이는 wifi_config.py 사용.\n[추가할 동작] 여기에 ____ 기능을 더해 줘. (예: 강수확률 60% 넘으면 LED 깜빡)\n[제약] 외부 라이브러리는 최소로, 갱신은 ____초마다, 복사해서 바로 도는 완결형 코드로 줘.\n받은 코드에서 핀 번호와 timing 설정이 내 것과 같은지 확인할게."},
      {"type": "callout", "kind": "tip", "title": "점검 체크리스트",
       "html": "받은 코드를 올리기 전에: ① <code>timing=(280,515,515,745)</code> 있는지 ② 핀 번호(16 / 26)와 포트(D16 / A0) 맞는지 ③ 무한 반복 속 <code>sleep</code>으로 쉬어 주는지 ④ 와이파이/네트워크 요청이 과하지 않은지."},
    ]},
    {"title": "마무리", "items": [
      {"type": "text", "html": "여기까지 왔다면, 여러분은 <b>센서로 데이터를 모으고 · 인터넷의 데이터를 가져오고 · LED와 웹으로 표현하는</b> 데이터 기반 탐구의 한 사이클을 전부 경험한 거예요. 도구는 거들 뿐, 진짜 중요한 건 ‘무엇을, 왜 만드는가’입니다. 멋진 작품을 만들어 보세요! 🎉"},
    ]},
  ],
},
# ----------------------------------------------------------------- 부록 A
{
  "id": "apx", "num": "A", "title": "부록 · 오픈 API 한눈에 보기", "accent": "#0EA5A0",
  "subtitle": "프로젝트에 쓸 만한 과목별 오픈 API 카탈로그예요. 각 API가 어떤 데이터를 주고 무엇을 탐구할 수 있는지 보고, 바로 살아 있는 대시보드로 들어가 보세요.",
  "why": "3장에서 API로 데이터를 받아 표현하는 흐름을 익혔죠. 이 부록은 과목별 오픈 API를 <b>한눈에 정리한 카탈로그</b>예요 — 각 API가 <b>어떤 데이터</b>를 주고 <b>어떤 탐구</b>를 할 수 있는지, 그리고 <b>브라우저에서 바로 그려 보는 라이브 대시보드</b>로 연결됩니다. 피코로 직접 받아오려면 3장 ‘날씨 시계’에서 쓴 <code>socket</code>+<code>ssl</code> 방식을 그대로 응용하면 돼요. (API는 2026년 기준 응답 확인)",
  "sections": [
    {"title": "이 부록 쓰는 법", "items": [
      {"type": "callout", "kind": "key", "title": "🌐 라이브 대시보드로 데이터를 ‘직접’ 만나 보기",
       "html": "각 API 카드의 <b>‘라이브 대시보드 열기’</b>를 누르면, 브라우저에서 <b>지금 데이터를 받아 지도·그래프로 그려 주는 페이지</b>가 열려요(설치·피코 없이 클릭만). 위치·물질·종을 바꿔 가며 탐구하고, 페이지마다 ‘🔎 탐구 질문’도 있습니다."},
      {"type": "linkbtn", "href": "dashboards/index.html", "label": "오픈 API 라이브 대시보드 갤러리 열기 (11종)"},
      {"type": "callout", "kind": "info", "title": "국내 적용 여부 한눈에",
       "html": "🇰🇷 국내 OK(일출몰·생물) · 🌍 전 지구라 국내도 포함(대기질·ISS·우주날씨) · 🌐 국적 무관(화학·천문) · 🌎 해외 위주(지진은 국내 드묾 → 기상청 권장). 국내 공식 데이터는 공공데이터포털(키 필요)을 쓰세요."},
    ]},
    {"title": "1) 미세먼지 (대기질) — 환경 🌍", "items": [
      {"type": "text", "html": "<b>📊 어떤 데이터</b> — PM2.5·PM10·오존 등 시간별 대기질(Open-Meteo, 키 불필요).<br><b>🔎 어떤 탐구</b> — 지금 등급(좋음~매우나쁨) 판정 · 하루 중 미세먼지가 높은 시간대 찾기 · 우리 동네와 다른 지역 공기질 비교."},
      {"type": "linkbtn", "href": "dashboards/airquality.html", "label": "이 API 라이브 대시보드 열기"},
    ]},
    {"title": "2) 전 세계 지진 — 지구과학 🌎", "items": [
      {"type": "text", "html": "<b>📊 어떤 데이터</b> — 실시간 지진의 규모·위치·깊이·시각(USGS, 키 불필요).<br><b>🔎 어떤 탐구</b> — 세계 지도에 찍어 ‘불의 고리’ 패턴 관찰 · 규모별 발생 수 세기 · 최대 규모 추적. (국내 지진은 드물어 기상청 권장)"},
      {"type": "linkbtn", "href": "dashboards/earthquake.html", "label": "이 API 라이브 대시보드 열기"},
    ]},
    {"title": "3) 국제우주정거장 ISS — 천문·물리 🌍", "items": [
      {"type": "text", "html": "<b>📊 어떤 데이터</b> — ISS의 실시간 위·경도·고도·속도(wheretheiss, 키 불필요).<br><b>🔎 어떤 탐구</b> — 지금 어느 나라 상공인지 지도로 추적 · 내 위치와의 거리 · 궤도가 물결치는 이유(궤도 경사) 탐구."},
      {"type": "linkbtn", "href": "dashboards/iss.html", "label": "이 API 라이브 대시보드 열기"},
    ]},
    {"title": "4) 일출·일몰·낮 길이 — 천문·지구과학 🇰🇷", "items": [
      {"type": "text", "html": "<b>📊 어떤 데이터</b> — 일출·일몰·남중시각·낮 길이(sunrise-sunset, 키 불필요).<br><b>🔎 어떤 탐구</b> — 계절별 낮 길이 변화 · 위도를 바꿔 적도 vs 극지방(백야·극야) 비교."},
      {"type": "linkbtn", "href": "dashboards/sunrise.html", "label": "이 API 라이브 대시보드 열기"},
    ]},
    {"title": "5) 우주날씨 Kp 지수 — 천문·지구과학 🌍", "items": [
      {"type": "text", "html": "<b>📊 어떤 데이터</b> — 지자기 폭풍 정도 Kp 지수(0~9, NOAA, 키 불필요).<br><b>🔎 어떤 탐구</b> — 최근 며칠 Kp 변화로 태양 활동 관찰 · 값이 높을 때 고위도 오로라 가능성 토론."},
      {"type": "linkbtn", "href": "dashboards/spaceweather.html", "label": "이 API 라이브 대시보드 열기"},
    ]},
    {"title": "6) 물질 정보 — 화학 🌐", "items": [
      {"type": "text", "html": "<b>📊 어떤 데이터</b> — 물질 이름 → 화학식·분자량·2D/3D 구조(PubChem, 키 불필요).<br><b>🔎 어떤 탐구</b> — 여러 물질 분자량 비교 · 3D 구조를 돌려 보며 모양 이해 · 화학식만 보고 물질 맞히기."},
      {"type": "linkbtn", "href": "dashboards/pubchem.html", "label": "이 API 라이브 대시보드 열기"},
    ]},
    {"title": "7) 우리나라 생물 관찰 — 생물 🇰🇷", "items": [
      {"type": "text", "html": "<b>📊 어떤 데이터</b> — 생물 종별 관찰 기록·위치·날짜(GBIF, 한국 약 880만 건, 키 불필요).<br><b>🔎 어떤 탐구</b> — 관찰 지점을 지도에 찍어 분포(도시 vs 산) · 월별(계절) 분포 · 철새 vs 텃새 비교."},
      {"type": "linkbtn", "href": "dashboards/gbif.html", "label": "이 API 라이브 대시보드 열기"},
    ]},
    {"title": "8) NASA 우주 데이터 — 천문 🌐 (키 필요)", "items": [
      {"type": "text", "html": "<b>📊 어떤 데이터</b> — 오늘의 천문사진(APOD)과 오늘 지구 곁을 지나는 소행성(NeoWs, NASA).<br><b>🔎 어떤 탐구</b> — 매일 우주사진 감상 · 오늘 가까운 소행성의 거리(달까지 거리의 몇 배)·크기·위험 여부 비교.<br><span style='color:#a55'>※ NASA만 API 키가 필요해요. 대시보드는 공용 <code>DEMO_KEY</code>로 동작하고(횟수 제한), 막히면 api.nasa.gov에서 무료 키를 받아 넣으면 돼요.</span>"},
      {"type": "linkbtn", "href": "dashboards/nasa.html", "label": "이 API 라이브 대시보드 열기"},
    ]},
  ],
},
]
CHAPTERS[0]["extra"] = ""   # FW_CARD는 0.4 섹션 안에 배치

# ===================================================================
#  렌더러
# ===================================================================
n_code = 0
n_prompt = 0

def render_item(it, accent):
    global n_code, n_prompt
    t = it["type"]
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
        icons = {"tip": "💡", "warn": "⚠️", "info": "ℹ️", "key": "🔑"}
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
        return (f'<div class="block prompt-block" style="--accent:{accent}">'
                f'<div class="block-head"><span class="prompt-ico">🤖</span>'
                f'<span class="block-label">{esc(it["label"])}</span>'
                f'<button class="copy-btn" aria-label="복사">복사</button></div>'
                f'<div class="prompt-body">{esc(it["text"])}</div></div>')
    return ""

def render():
    nav, main = [], []
    for c in CHAPTERS:
        nav.append(f'<div class="nav-ch"><a href="#{c["id"]}" class="nav-ch-link" '
                   f'data-target="{c["id"]}"><span class="nav-dot" '
                   f'style="background:{c["accent"]}"></span>{esc(c["num"])}. {esc(c["title"])}</a>'
                   f'<div class="nav-secs">')
        sec_html = []
        for si, s in enumerate(c["sections"]):
            sid = f'{c["id"]}-{si}'
            nav.append(f'<a href="#{sid}" class="nav-sec" data-target="{sid}">{esc(s["title"])}</a>')
            items_html = "".join(render_item(it, c["accent"]) for it in s["items"])
            sec_html.append(f'<section class="sec" id="{sid}">'
                            f'<h3 class="sec-title">{esc(s["title"])}</h3>{items_html}</section>')
        nav.append('</div></div>')

        # 챕터 인트로 (목표 + 왜 배우나요)
        goals = "".join(f'<li>{g}</li>' for g in c.get("goals", []))
        intro = ''
        if goals:
            intro += f'<div class="goals"><div class="goals-t">🎯 이 장을 마치면</div><ul>{goals}</ul></div>'
        if c.get("why"):
            intro += f'<div class="why"><div class="why-t">💡 왜 배우나요?</div><p>{c["why"]}</p></div>'

        main.append(
            f'<div class="chapter" id="{c["id"]}">'
            f'<div class="ch-head"><span class="ch-num" style="color:{c["accent"]}">CHAPTER {c["num"]}</span>'
            f'<h2 class="ch-title"><span class="ch-bar" style="background:{c["accent"]}"></span>{esc(c["title"])}</h2>'
            f'<p class="ch-sub">{esc(c["subtitle"])}</p></div>'
            f'{intro}{c.get("extra","")}{"".join(sec_html)}</div>')

    out = TEMPLATE
    out = out.replace("/*NAV*/", "".join(nav))
    out = out.replace("/*MAIN*/", "".join(main))
    out = out.replace("/*NCODE*/", str(n_code))
    out = out.replace("/*NPROMPT*/", str(n_prompt))
    out = out.replace("/*NCH*/", str(len(CHAPTERS)))
    return out

# ===================================================================
#  HTML 템플릿 (CSS는 그대로 — 토큰 치환 방식)
# ===================================================================
TEMPLATE = r'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>데이터로 탐구하는 피코 바이브 피지컬 코딩</title>
<meta name="description" content="라즈베리파이 피코 2 WH로 배우는 피지컬 컴퓨팅 연수 자료 — 설치부터 와이파이·LED·날씨 API·가스센서 대시보드까지, 복사해서 바로 쓰는 MicroPython 코드 모음.">
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/atom-one-dark.min.css">
<style>
:root{
  --bg:#ffffff; --fg:#37352f; --muted:#7b7872; --line:#ededec;
  --sidebar:#fbfbfa; --code-bg:#f7f6f3; --radius:10px;
  --font:'Pretendard',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  --mono:'SFMono-Regular',ui-monospace,Menlo,Consolas,'D2Coding',monospace;
}
*{box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{margin:0;font-family:var(--font);color:var(--fg);background:var(--bg);line-height:1.65;-webkit-font-smoothing:antialiased;}
a{color:inherit;text-decoration:none;}
.layout{display:flex;max-width:1180px;margin:0 auto;}
.sidebar{position:sticky;top:0;height:100vh;width:280px;flex:0 0 280px;overflow-y:auto;
  background:var(--sidebar);border-right:1px solid var(--line);padding:26px 16px 60px;}
.brand{font-weight:800;font-size:15px;padding:6px 10px 14px;letter-spacing:-.02em;}
.brand small{display:block;font-weight:500;color:var(--muted);font-size:12px;margin-top:3px;}
.nav-ch{margin-top:10px;}
.nav-ch-link{display:flex;align-items:center;gap:8px;font-weight:700;font-size:13.5px;padding:7px 10px;border-radius:7px;}
.nav-ch-link:hover{background:#efefee;}
.nav-dot{width:9px;height:9px;border-radius:50%;flex:0 0 9px;}
.nav-secs{display:flex;flex-direction:column;margin:2px 0 8px 18px;border-left:1px solid var(--line);}
.nav-sec{font-size:12.5px;color:var(--muted);padding:5px 10px;border-left:2px solid transparent;margin-left:-1px;}
.nav-sec:hover{color:var(--fg);}
.nav-sec.active{color:var(--fg);font-weight:600;border-left-color:var(--fg);}
.main{flex:1;min-width:0;padding:0 56px 120px;}
.hero{padding:64px 0 30px;border-bottom:1px solid var(--line);margin-bottom:18px;}
.hero h1{font-size:38px;font-weight:800;letter-spacing:-.03em;margin:0 0 14px;line-height:1.2;}
.hero p{font-size:15.5px;color:var(--muted);margin:0 0 22px;max-width:660px;}
.stats{display:flex;gap:10px;flex-wrap:wrap;}
.stat{display:flex;align-items:baseline;gap:7px;background:var(--code-bg);border:1px solid var(--line);
  border-radius:999px;padding:7px 15px;font-size:13px;color:var(--muted);}
.stat b{font-size:15px;color:var(--fg);font-weight:800;}
.chapter{padding-top:30px;}
.ch-head{margin:40px 0 8px;}
.ch-num{font-size:12px;font-weight:800;letter-spacing:.12em;}
.ch-title{display:flex;align-items:center;gap:12px;font-size:27px;font-weight:800;letter-spacing:-.02em;margin:6px 0 8px;}
.ch-bar{width:5px;height:26px;border-radius:3px;flex:0 0 5px;}
.ch-sub{color:var(--muted);font-size:14.5px;margin:0 0 6px;max-width:680px;}
.sec{padding-top:14px;}
.sec-title{font-size:16.5px;font-weight:700;margin:30px 0 12px;letter-spacing:-.01em;padding-bottom:7px;border-bottom:1px solid var(--line);}
.prose{font-size:14.5px;margin:12px 0;max-width:720px;}
.prose code,.callout-body code,.concept-d code,.steps code,.m-row code,.qa-a code,.idea-d code,.dig-body code{
  font-family:var(--mono);font-size:12.5px;background:var(--code-bg);border:1px solid var(--line);
  border-radius:4px;padding:1px 6px;}
.step-head{font-size:14.5px;margin:22px 0 10px;max-width:720px;}
/* 챕터 인트로 */
.goals{background:#f8f9ff;border:1px solid #e6e8fb;border-radius:12px;padding:16px 20px;margin:14px 0;max-width:720px;}
.goals-t{font-weight:800;font-size:14px;margin-bottom:8px;}
.goals ul{margin:0;padding-left:20px;}
.goals li{font-size:13.5px;margin:4px 0;}
.why{background:#fffdf5;border:1px solid #f1e9cf;border-radius:12px;padding:16px 20px;margin:14px 0;max-width:720px;}
.why-t{font-weight:800;font-size:14px;margin-bottom:6px;}
.why p{margin:0;font-size:14px;}
/* 콜아웃 */
.callout{border-radius:10px;padding:14px 18px;margin:14px 0;max-width:720px;border:1px solid var(--line);border-left-width:4px;}
.callout-head{font-weight:800;font-size:13.5px;margin-bottom:6px;}
.callout-body{font-size:13.5px;}
.callout.tip{background:#f0faf4;border-left-color:#22c55e;}
.callout.warn{background:#fff6f0;border-left-color:#f97316;}
.callout.info{background:#f0f7ff;border-left-color:#3b82f6;}
.callout.key{background:#f7f0ff;border-left-color:#8b5cf6;}
/* 링크 버튼 */
.linkbtn{display:inline-flex;align-items:center;gap:6px;background:#fff;border:1px solid #d6d5d2;
  border-radius:9px;padding:9px 16px;font-size:13.5px;font-weight:600;margin:8px 8px 8px 0;transition:.15s;}
.linkbtn:hover{border-color:#9b9b97;background:var(--code-bg);}
/* 체크리스트(준비물) */
.check-list{list-style:none;padding:0;margin:12px 0;max-width:720px;}
.check-list li{font-size:14px;padding:7px 0 7px 30px;position:relative;border-bottom:1px solid var(--line);}
.check-list li:before{content:"☐";position:absolute;left:6px;top:6px;font-size:16px;color:var(--muted);}
/* 핵심 개념 그리드 */
.concept-grid,.idea-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;margin:14px 0;max-width:760px;}
.concept,.idea{background:var(--code-bg);border:1px solid var(--line);border-radius:10px;padding:13px 15px;}
.concept-t,.idea-t{font-weight:800;font-size:13.5px;margin-bottom:5px;}
.concept-d,.idea-d{font-size:13px;color:#55524c;}
.idea-d code,.concept-d code{word-break:break-all;}
.idea-d{line-height:1.7;}
/* 스텝 */
.steps{margin:12px 0;padding-left:0;counter-reset:s;list-style:none;max-width:720px;}
.steps li{position:relative;padding:10px 0 10px 40px;border-bottom:1px solid var(--line);font-size:14px;}
.steps li:before{counter-increment:s;content:counter(s);position:absolute;left:0;top:9px;width:26px;height:26px;
  background:#37352f;color:#fff;border-radius:50%;text-align:center;line-height:26px;font-size:13px;font-weight:700;}
.steps li b{display:block;margin-bottom:2px;}
.steps li span{color:#55524c;font-size:13.5px;}
/* 자주 하는 실수 */
.mistakes{margin:12px 0;max-width:720px;}
.mistake{border:1px solid #f0d9d9;border-radius:10px;padding:12px 15px;margin:10px 0;background:#fffafa;}
.m-sym{font-weight:700;font-size:13.5px;color:#c0392b;margin-bottom:7px;}
.m-row{font-size:13px;margin:4px 0;padding-left:2px;}
.m-tag{display:inline-block;font-size:11px;font-weight:700;color:#fff;background:#bbb;border-radius:5px;
  padding:1px 7px;margin-right:7px;}
.m-tag.fix{background:#22a06b;}
/* 스스로 점검 */
.checks{margin:12px 0;max-width:720px;}
.qa{border:1px solid var(--line);border-radius:9px;margin:8px 0;background:#fff;}
.qa summary{cursor:pointer;padding:11px 15px;font-size:13.8px;font-weight:600;list-style:none;}
.qa summary:before{content:"❓ ";}
.qa[open] summary{border-bottom:1px solid var(--line);}
.qa-a{padding:11px 15px;font-size:13.5px;color:#55524c;}
.qa-a:before{content:"✅ ";}
/* 더 알아보기 (심화 이론) */
.dig{border:1px solid #dde2f2;border-left:4px solid #6b7cff;border-radius:10px;margin:14px 0;max-width:760px;
  background:linear-gradient(180deg,#fafbff,#fff);}
.dig summary{cursor:pointer;padding:12px 16px;font-weight:700;font-size:13.5px;color:#3a45a8;list-style:none;}
.dig summary::-webkit-details-marker{display:none;}
.dig summary:after{content:"▾";float:right;color:#9aa1cf;transition:.2s;}
.dig[open] summary:after{transform:rotate(180deg);}
.dig[open] summary{border-bottom:1px solid #e7eaf7;}
.dig-body{padding:14px 16px;font-size:13.5px;line-height:1.8;color:#44464f;}
.dig-body b{color:#2f3a96;}
/* 코드 접기 */
.codefold{margin:12px 0;max-width:840px;}
.codefold>summary{cursor:pointer;list-style:none;padding:11px 15px;border:1px dashed #cfd3e6;border-radius:10px;
  background:#f7f8fd;font-size:13px;font-weight:700;color:#4a4f74;}
.codefold>summary::-webkit-details-marker{display:none;}
.codefold>summary:before{content:"📄 ";}
.codefold>summary:after{content:"  ▾";color:#aab;}
.codefold[open]>summary:after{content:"  ▴";}
.codefold[open]>summary{border-style:solid;border-color:var(--line);border-bottom:none;
  border-radius:10px 10px 0 0;background:var(--code-bg);}
.codefold .fold-hint{font-weight:500;color:#9aa;}
.codefold .block{margin:0;border-radius:0 0 10px 10px;}
/* 귀여운 브랜딩 강조 */
.pico-accent{background:linear-gradient(120deg,#5B6CF0,#E0568A);-webkit-background-clip:text;
  background-clip:text;color:transparent;font-weight:900;}
.brand-emoji{font-size:17px;}
/* '피지컬 코딩'의 [피][코] 글자 강조 — 피코 워드플레이 */
.pk{background:linear-gradient(120deg,#5B6CF0,#E0568A);color:#fff;font-weight:900;
  border-radius:7px;padding:0 .26em;margin:0 .02em;}
/* 하드웨어 다이어그램 */
.figure{margin:14px 0;max-width:760px;}
.diagram{font-family:var(--mono);font-size:12px;line-height:1.5;background:var(--code-bg);
  border:1px solid var(--line);border-radius:10px;padding:16px;overflow-x:auto;white-space:pre;}
.hw-svg{width:100%;height:auto;background:#fff;border:1px solid var(--line);border-radius:12px;padding:12px;font-family:var(--font);}
.api-svg{width:100%;height:auto;background:#fbfcff;border:1px solid #e6e8f5;border-radius:14px;padding:8px;font-family:var(--font);}
/* 코드/프롬프트 블록 */
.block{border:1px solid var(--line);border-radius:var(--radius);margin:12px 0;overflow:hidden;background:#fff;max-width:840px;}
.block-head{display:flex;align-items:center;gap:9px;padding:9px 13px;background:var(--code-bg);border-bottom:1px solid var(--line);}
.block-label{font-size:12.5px;font-weight:600;color:#55524c;flex:1;min-width:0;}
.lang-tag{font-family:var(--mono);font-size:10.5px;font-weight:700;color:var(--muted);
  background:#fff;border:1px solid var(--line);border-radius:5px;padding:1px 7px;letter-spacing:.04em;}
.copy-btn{font-family:var(--font);font-size:11.5px;font-weight:600;color:var(--muted);cursor:pointer;
  background:#fff;border:1px solid var(--line);border-radius:6px;padding:4px 11px;transition:.15s;flex:0 0 auto;}
.copy-btn:hover{color:var(--fg);border-color:#d6d5d2;}
.copy-btn.done{color:#0a7f54;border-color:#9bd9bd;background:#f0faf5;}
.code-block pre{margin:0;padding:16px 18px;overflow-x:auto;background:#282c34;}
.code-block code{font-family:var(--mono);font-size:13px;line-height:1.62;background:none;padding:0;color:#abb2bf;}
.code-block .block-head{background:#21252b;border-bottom-color:#181b20;}
.code-block .block-label{color:#c7cdd6;}
.code-block .lang-tag{color:#9aa3b2;background:#2c313a;border-color:#3a4150;}
.code-block .copy-btn{color:#aeb6c2;background:#2c313a;border-color:#3a4150;}
.code-block .copy-btn:hover{color:#fff;border-color:#5a6275;}
.code-block .copy-btn.done{color:#79e3b4;border-color:#2f6b4f;background:#1f3a2c;}
.prompt-block{border-color:color-mix(in srgb,var(--accent) 30%,var(--line));}
.prompt-block .block-head{background:color-mix(in srgb,var(--accent) 8%,#fff);
  border-bottom-color:color-mix(in srgb,var(--accent) 18%,var(--line));}
.prompt-block .block-label{color:color-mix(in srgb,var(--accent) 55%,#37352f);}
.prompt-ico{font-size:15px;}
.prompt-body{font-family:var(--mono);font-size:13px;line-height:1.7;color:#3a3833;
  white-space:pre-wrap;word-break:break-word;padding:15px 18px;
  background:color-mix(in srgb,var(--accent) 4%,#fff);}
/* 펌웨어 카드 */
.fw-card{border:1px solid color-mix(in srgb,#5B6CF0 30%,var(--line));border-radius:14px;
  background:linear-gradient(180deg,color-mix(in srgb,#5B6CF0 7%,#fff),#ffffff);padding:22px 24px;margin:12px 0 18px;max-width:840px;}
.fw-top{display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap;}
.fw-badge{display:inline-block;font-size:11.5px;font-weight:700;color:#3B47C2;
  background:color-mix(in srgb,#5B6CF0 13%,#fff);border-radius:999px;padding:3px 12px;margin-bottom:9px;}
.fw-title{margin:0 0 5px;font-size:19px;font-weight:800;letter-spacing:-.01em;}
.fw-meta{margin:0;color:var(--muted);font-size:13px;}
.fw-meta b{color:var(--fg);}
.dl-btn{display:inline-flex;align-items:center;background:#5B6CF0;color:#fff;font-weight:700;
  font-size:14.5px;border-radius:11px;padding:13px 22px;white-space:nowrap;
  box-shadow:0 5px 16px color-mix(in srgb,#5B6CF0 38%,transparent);transition:.15s;}
.dl-btn:hover{background:#4a5ae0;transform:translateY(-1px);}
.fw-steps-wrap{margin-top:18px;background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 18px 16px;}
.fw-steps-title{font-size:12.5px;font-weight:700;color:#3B47C2;margin-bottom:6px;}
.fw-steps{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:7px;font-size:13.5px;color:var(--fg);line-height:1.5;}
.fw-steps li{padding-left:3px;}
.fw-dim{color:var(--muted);}
.fw-steps code,.fw-note code{font-family:var(--mono);font-size:12px;background:var(--code-bg);
  border:1px solid var(--line);border-radius:4px;padding:1px 6px;}
.fw-note{margin:14px 0 0;font-size:12.5px;color:var(--muted);line-height:1.55;}
.fw-note a{color:#3B47C2;text-decoration:underline;}
footer{margin-top:60px;padding-top:24px;border-top:1px solid var(--line);color:var(--muted);font-size:12.5px;}
.menu-btn{display:none;position:fixed;top:14px;left:14px;z-index:50;background:#fff;border:1px solid var(--line);
  border-radius:9px;width:42px;height:42px;font-size:18px;cursor:pointer;box-shadow:0 2px 10px rgba(0,0,0,.07);}
.scrim{display:none;}
@media(max-width:920px){
  .main{padding:0 22px 100px;}
  .hero{padding-top:74px;}
  .hero h1{font-size:30px;}
  .menu-btn{display:block;}
  .sidebar{position:fixed;left:0;top:0;z-index:45;transform:translateX(-100%);transition:.25s;box-shadow:0 0 40px rgba(0,0,0,.12);}
  .sidebar.open{transform:none;}
  .scrim.show{display:block;position:fixed;inset:0;background:rgba(0,0,0,.3);z-index:44;}
}
</style>
</head>
<body>
<button class="menu-btn" id="menuBtn" aria-label="메뉴">☰</button>
<div class="scrim" id="scrim"></div>
<div class="layout">
  <aside class="sidebar" id="sidebar">
    <div class="brand"><span class="brand-emoji">🐣🔌</span> 바이브 <span class="pk">피</span>지컬 <span class="pk">코</span>딩<small>데이터 기반 탐구 프로젝트 · <span class="pico-accent">피코</span>로 시작하기</small></div>
    /*NAV*/
  </aside>
  <main class="main">
    <header class="hero">
      <h1>데이터로 탐구하는<br>바이브 <span class="pk">피</span>지컬 <span class="pk">코</span>딩 🐣</h1>
      <p>센서로 모은 데이터와 인터넷의 공개 데이터(API)를, <b><span class="pico-accent">피코</span></b>와 LED·웹으로 ‘보이게’ 만드는 <b>데이터 기반 탐구 프로젝트</b> 안내서예요. 준비(설치·조립)부터 와이파이·LED·날씨 API·가스센서, 그리고 과목별 오픈 API 부록까지 — 모든 코드를 <b>복사해 바로 실행</b>할 수 있습니다. 🌈</p>
      <div class="stats">
        <div class="stat"><b>/*NCH*/</b>개 챕터</div>
        <div class="stat"><b>/*NCODE*/</b>개 코드 블록</div>
        <div class="stat"><b>/*NPROMPT*/</b>개 AI 프롬프트</div>
      </div>
    </header>
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
const sb=document.getElementById('sidebar'),scrim=document.getElementById('scrim'),mb=document.getElementById('menuBtn');
function toggle(o){sb.classList.toggle('open',o);scrim.classList.toggle('show',o);}
mb.addEventListener('click',()=>toggle(!sb.classList.contains('open')));
scrim.addEventListener('click',()=>toggle(false));
sb.addEventListener('click',e=>{if(e.target.closest('a')&&window.innerWidth<=920)toggle(false);});
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

with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
    f.write(render())
print(f"생성 완료 · 코드 {n_code}개 · 프롬프트 {n_prompt}개")
