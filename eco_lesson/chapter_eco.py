# -*- coding: utf-8 -*-
# ML 확장판 3장 「물까치를 찾는 피코」 — build_site.py의 CHAPTERS 포맷
# 본문 문단(P)은 솔라 프로4 집필본(solar/solar_final.md). 코드·표·배선도·짧은 안내는 클로드 작성
import os, re
from figs import FIG_STYLE, FIG_ALL, FIG_MIC, FIG_SD

_HERE = os.path.dirname(os.path.abspath(__file__))
_txt = open(os.path.join(_HERE, "solar", "solar_final.md"), encoding="utf-8").read()
P = {int(m.group(1)): m.group(2).strip() for m in re.finditer(r"### 블록 (\d+)\n(.*?)(?=\n### 블록 |\Z)", _txt, re.S)}

DM = "https://www.devicemart.co.kr/goods/view?no="
def _row(name, role, qty, no=None, ext=None, note=""):
    link = f'<a href="{DM}{no}" target="_blank" rel="noopener">디바이스마트</a>' if no else (
        f'<a href="{ext}" target="_blank" rel="noopener">제조사</a>' if ext else "")
    return f"<tr><td>{name}</td><td>{role}</td><td style='text-align:center'>{qty}</td><td>{link}</td><td>{note}</td></tr>"

_BUY = ("<div style='overflow-x:auto'><table class='plan-table'>"
        "<tr><th>부품</th><th>역할</th><th>수량</th><th>구입</th><th>비고</th></tr>"
        + _row("라즈베리파이 피코 2 WH", "두뇌", 1, "15774532", note="앞 장 것 사용 가능")
        + _row("Grove Shield for Pi Pico v1.0", "부품 연결판", 1, "13960283", note="앞 장 것 사용 가능")
        + _row("INMP441 전방향 마이크 모듈(납땜)", "소리 듣기", 1, "15366646", note="핀헤더가 납땜되어 나오는 제품. 앞 장 것 사용 가능")
        + _row("Grove 4핀 암 점퍼 변환 케이블(5개입)", "마이크 연결", 1, "1153481", note="2개 사용")
        + _row("Digilent Pmod MicroSD", "녹음·기록 저장", 1, "15707182", note="학교구매전용 상품. 3.3V 전용")
        + _row("암-암 점퍼 케이블 10cm", "SD 모듈 연결", "6가닥", "1328410")
        + _row("microSDHC 32GB", "녹음용 카드", 1, "14051370", note="FAT32")
        + _row("Adafruit DS3231 RTC (STEMMA QT)", "시계", 1, "14440939")
        + _row("Grove to STEMMA QT 케이블", "시계 연결", 1, "14600579")
        + _row("CR1220 동전 전지", "시계 전원 유지", 1, "2930")
        + _row("Grove Button(P)", "관측 끝내기", 1, "1066473", note="누르면 HIGH")
        + _row("USB-A to Micro-B 데이터 케이블", "PC 연결·전원", 1, "15601492", note="PC가 USB-C면 15601504")
        + _row("microSD 카드 리더", "PC에서 카드 읽고 쓰기", "모둠당 1", "1384235", note="포맷·MP3 복사·녹음 회수")
        + "<tr><td colspan='5' style='background:var(--card);font-weight:700'>앞 장에서 쓰던 것</td></tr>"
        + _row("WS2813 LED 바 10칸 · Grove 케이블", "상태 표시", "각 1", note="본 교재 기본 부품")
        + _row("Grove MP3 v4.0 + 스피커 + MP3용 microSD", "말하기", "각 1", "15784279", note="말하기 장(ML+)에서 쓰던 것. 없으면 링크에서 구입(스피커 포함, 해외 재고 1주일)")
        + "<tr><td colspan='5' style='background:var(--card);font-weight:700'>현장 설치 (참고 추천)</td></tr>"
        + _row("Always On 보조배터리 (예: Voltaic V25)", "밖에서 전원", 1, ext="https://voltaicsystems.com/v25/", note="저전류에서 꺼지지 않는 제품")
        + _row("방수 케이스 (예: Coms BD983, IP65)", "비·먼지 막기", 1, "15813675", note="구멍을 내면 방수 등급이 유지되지 않아요")
        + "</table></div>")

_FLOW = ("<div style='margin:14px 0 6px;padding:14px 16px;border:1px solid var(--line);border-radius:14px;background:var(--code-bg)'>"
         "<div style='font-size:14px;font-weight:800;margin-bottom:10px;color:#f0e8d6'>이 챕터 한눈에</div>"
         "<div style='display:flex;flex-wrap:wrap;gap:8px'>"
         + "".join(f"<div style='flex:1;min-width:112px;background:#fff;border:1px solid var(--line);border-radius:10px;padding:9px 8px;text-align:center'>"
                   f"<div style='font-size:11px;font-weight:800;color:#0F766E'>{n}</div><div style='font-size:13px;font-weight:700'>{t}</div></div>"
                   for n, t in (("준비", "조립·확인"), ("①", "예시 모으기"), ("②", "물까치 탐지기"), ("③", "채점·기준 정하기"), ("④", "여러 새 구분"), ("⑤⑥", "현장·시간 그래프")))
         + "</div></div>")

_HERO = ("<figure style='margin:0 0 10px'><img src='../eco_lesson/img/hero_mulkkachi.jpg' alt='학교 화단 벤치 위의 관측기와 나뭇가지의 물까치 두 마리' "
         "style='width:100%;border-radius:14px;border:1px solid var(--line)'>"
         "<figcaption class='ecofig-cap'>장면 삽화(GPT 생성). 실제 배선은 아래 배선도를 따르세요.</figcaption></figure>")

def _fig(svg, cap):
    return {"type": "raw", "html": f"<div class='ecofig'>{svg}</div><p class='ecofig-cap'>{cap}</p>"}

def _out(text):                     # 예상 화면
    return {"type": "raw", "html": "<pre style='background:var(--code-bg);color:var(--code-text);border-radius:12px;padding:12px 14px;font-size:12.5px;overflow-x:auto'>" + text + "</pre>"}

_AUDIO = ("<div style='display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 14px'>"
          + "".join(f"<a class='linkbtn' href='../eco_lesson/audio/{f}' download>🔊 {f} · {t}</a>"
                    for f, t in (("0001.mp3", "물까치인가 봐요"), ("0002.mp3", "까치인가 봐요"), ("0003.mp3", "직박구리인가 봐요")))
          + "</div>")

_APPS = '''function doGet(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  sheet.appendRow([new Date(), e.parameter.time, e.parameter.label, e.parameter.votes]);
  return ContentService.createTextOutput("ok");
}'''

CHAPTER_ECO = {
  "id": "chbird", "num": "ML3", "title": "물까치를 찾는 피코 — 소리로 새를 알아보는 관측기",
  "accent": "#0F766E",
  "subtitle": "3초 동안 소리를 듣고 직접 모은 예시와 비교해 물까치 후보를 찾는 관측기. 찾으면 말하고, 녹음하고, 시각을 남겨요.",
  "goals": [
    "마이크·microSD·시계·MP3를 쉴드에 꽂아 관측기를 조립한다",
    "3초 동안 들은 소리를 숫자 25개(특징)로 바꾼다",
    "물까치와 헷갈릴 만한 소리의 예시를 모아 k-NN으로 물까치 후보를 찾는다",
    "예시로 쓰지 않은 녹음으로 재현율과 오판을 채점하고 기준을 정한다",
    "관측 기록으로 물까치가 나타난 시간을 그래프로 본다",
  ],
  "why": P[1],
  "extra": FIG_STYLE + _HERO + _FLOW,
  "sections": [
    {"title": "시작하기 전에 — 흐름과 기대치", "items": [
      {"type": "text", "html": P[2]},
      {"type": "callout", "kind": "info", "title": "얼마나 잘 맞힐까?", "html": P[3]},
    ]},
    {"title": "준비물", "items": [
      {"type": "raw", "html": _BUY},
      {"type": "text", "html": P[4]},
    ]},
    {"title": "조립 전에 전체 모습 보기", "items": [
      _fig(FIG_ALL, "그림 1. 전체 연결. I2C1·A0·A1·UART1은 비워 두어요. UART1은 SPI0 헤더와 핀을 함께 써요."),
      {"type": "callout", "kind": "warn", "title": "USB를 뽑고 조립해요", "html": "PC와 보조배터리의 USB 케이블을 모두 뽑은 상태에서 선을 꽂아요. 조립과 확인이 모두 끝난 뒤 마지막에 PC USB를 연결해요."},
    ]},
    {"title": "조립 ① 쉴드 스위치와 microSD", "items": [
      {"type": "text", "html": P[5]},
      _fig(FIG_SD, "그림 2. SPI0 헤더 → Pmod MicroSD 신호 연결. J1은 2줄 12핀이에요. 1번 표시가 있는 줄의 1~6번만 쓰고 7~12번 줄은 비워요. 선 색은 제품마다 다를 수 있으니 양 끝의 이름으로 확인해요."),
      {"type": "steps", "items": [
        {"t": "USB 분리", "d": "PC·보조배터리 USB 케이블이 모두 빠져 있는지 확인해요."},
        {"t": "스위치 5V", "d": "쉴드 모서리 스위치를 <b>5V</b> 쪽으로 밀어요."},
        {"t": "SCK → SCK(4번)", "d": "헤더 윗줄 왼쪽"},
        {"t": "TX → MOSI(2번)", "d": "헤더 윗줄 가운데"},
        {"t": "RX → MISO(3번)", "d": "헤더 윗줄 오른쪽"},
        {"t": "CS → ~CS(1번)", "d": "헤더 아랫줄 오른쪽"},
        {"t": "3V3 → VCC(6번)", "d": "헤더 아랫줄 가운데"},
        {"t": "GND → GND(5번)", "d": "헤더 아랫줄 왼쪽"},
      ]},
      {"type": "callout", "kind": "warn", "title": "카드는 FAT32로", "html": "녹음용 microSD는 PC에서 <b>FAT32</b>로 포맷해요. 64GB 이상 카드는 보통 exFAT로 나와서 다시 포맷해야 해요."},
    ]},
    {"title": "조립 ② 마이크", "items": [
      {"type": "callout", "kind": "warn", "title": "소리·말하기 장의 마이크 점퍼는 먼저 빼요", "html": "앞 장에서는 마이크를 피코 헤더(GP18·GP19·GP20, 36번 3V3)에 점퍼로 꽂았어요. 이 장은 D20·A2 포트로 다시 연결하고, 버튼을 D18(GP18)에 꽂아요. USB를 뽑은 상태에서 헤더에 꽂힌 마이크 점퍼 6가닥을 모두 뺀 뒤 아래대로 연결해요."},
      {"type": "text", "html": P[6]},
      _fig(FIG_MIC, "그림 3. D20·A2 → INMP441 신호 연결. 모듈의 핀 순서는 제품마다 다를 수 있으니 모듈에 인쇄된 이름을 보고 꽂아요. 케이블 A의 빨강, 케이블 B의 흰색은 절연하고 어디에도 꽂지 않아요."),
    ]},
    {"title": "조립 ③ 시계·MP3·LED·버튼", "items": [
      {"type": "text", "html": P[7]},
      {"type": "raw", "html": _AUDIO},
      {"type": "callout", "kind": "key", "title": "MP3용 microSD 준비", "html": "말하기 장에서 쓰던 카드에는 휘파람·박수 음성이 들어 있어요. 그대로 두면 번호가 섞이니 <b>포맷부터</b> 해요.<br>① 카드를 <b>FAT32</b>로 포맷해요. Windows는 카드 우클릭 → 포맷 → FAT32, Mac은 디스크 유틸리티 → 지우기 → MS-DOS(FAT)예요. 32GB 이하 카드가 편해요.<br>② 위 세 파일을 카드 <b>맨 위 폴더</b>에 <code>0001.mp3</code> → <code>0002.mp3</code> → <code>0003.mp3</code> 순서로 <b>한 개씩</b> 복사해요. 이 모듈은 파일 이름이 아니라 복사한 순서로 번호를 매기는 경우가 많아요.<br>③ Mac에서 복사했다면 터미널에서 <code>dot_clean /Volumes/카드이름</code>을 실행해 숨김 파일을 지워요. 숨김 파일이 있으면 번호가 한 칸씩 밀려요.<br>④ 엉뚱한 음성이 나오면 카드를 다시 포맷하고 ②부터 다시 해요."},
      {"type": "steps", "items": [
        {"t": "시계", "d": "DS3231 → <b>I2C0</b> (Grove–STEMMA QT 케이블), 뒷면에 CR1220"},
        {"t": "MP3", "d": "Grove MP3 v4.0 → <b>UART0</b>(말하기 장과 같아요). 스피커는 모듈의 스피커 단자에 꽂고, 위에서 준비한 microSD를 넣어요. 녹음용 카드와 다른 카드예요."},
        {"t": "LED", "d": "WS2813 → <b>D16</b>"},
        {"t": "버튼", "d": "Grove 버튼 → <b>D18</b>"},
      ]},
    ]},
    {"title": "전체 연결 확인", "items": [
      {"type": "step_head", "html": "그림 1과 비교하며 확인해요"},
      {"type": "check_list", "items": [
        "쉴드 스위치가 5V에 있다",
        "SPI0 헤더 6가닥이 SD 모듈 1~6번 핀과 이름대로 맞다",
        "마이크 케이블 A는 D20, B는 A2에 꽂혀 있고, 쓰지 않는 두 선이 절연되어 있다",
        "시계 I2C0, MP3 UART0, LED D16, 버튼 D18",
        "녹음용 SD와 MP3용 SD가 각각 꽂혀 있다",
        "모두 확인한 뒤 마지막에 PC USB를 연결했다",
      ]},
    ]},
    {"title": "프로그램 준비", "items": [
      {"type": "text", "html": P[8]},
      {"type": "callout", "kind": "tip", "title": "처음 연결한다면", "html": "피코에 MicroPython v1.28.0(Pico 2 W용 <code>RPI_PICO2_W</code>)이 설치되어 있어야 해요. Thonny 오른쪽 아래에서 <b>MicroPython (Raspberry Pi Pico)</b>를 고르고, 셸에 <code>&gt;&gt;&gt;</code>가 표시되면 연결된 거예요. 설치 방법은 0장에 있어요."},
      {"type": "linkbtn", "href": "../ch0.html", "label": "0장 · 펌웨어 설치와 Thonny 연결"},
      {"type": "code", "label": "sdcard.py (micropython-lib, MIT 라이선스) · 피코에 이 이름으로 저장", "lang": "python", "file": "snippets/sdcard.py", "fold": True},
      {"type": "code", "label": "eco_lib.py · 피코에 이 이름으로 저장", "lang": "python", "file": "snippets/eco_lib.py", "fold": True},
    ]},
    {"title": "⓪ 부품 확인", "items": [
      {"type": "text", "html": P[9]},
      {"type": "code", "label": "코드 ⓪ · 부품 확인과 시계 맞추기", "lang": "python", "file": "snippets/eco_0_check.py"},
      {"type": "step_head", "html": "예상 화면"},
      _out("① SD 카드   OK  남은 공간 29810 MB\n② 시계      OK  2026-10-01 07:15:03  ← 지금 시각과 같은지 확인하세요\n③ 마이크    조용할 때 크기 31. 이제 3초 동안 박수를 쳐 보세요\n③ 마이크    OK  박수 크기 2140\n④ MP3       1번 파일을 틀어요. '물까치인가 봐요'가 들리면 OK\n⑤ 버튼      5초 안에 버튼을 한 번 누르세요\n⑤ 버튼      OK\n⑥ LED       빨강 → 초록 → 파랑으로 켜졌다면 OK\n⑦ 판단 속도 3초 동안 아무 소리나 들려주세요\n⑦ 판단 속도 특징 계산 ○○○ ms · 남은 메모리 ○○○ KB · 조각 8개\n안전하게 끝났어요. 이제 전원을 뽑아도 됩니다."),
      {"type": "callout", "kind": "warn", "title": "④와 ⑥은 직접 확인해요", "html": "④와 ⑥은 코드가 판정하지 않고 늘 같은 안내를 표시해요. ④는 스피커에서 '물까치인가 봐요'가 들리는지, ⑥은 LED가 빨강·초록·파랑으로 켜지는지 직접 보고 확인해요."},
      {"type": "callout", "kind": "tip", "title": "⑦의 두 숫자를 적어 두세요", "html": "특징 계산 시간은 3초 녹음이 끝난 뒤 숫자 25개를 계산하는 데 걸린 시간이에요. SD 저장, 예시 비교, MP3 재생 시간은 들어 있지 않아요. 남은 메모리는 예시를 불러오기 전에 측정한 값이라, 탐지기에서는 예시가 차지하는 만큼 더 줄어요. 교재를 만들 때는 실물 피코에서 측정하지 못한 값이에요."},
    ]},
    {"title": "① 물까치 예시 모으기", "items": [
      {"type": "text", "html": P[10]},
      {"type": "concept", "items": [
        {"t": "물까치", "d": "학교에서 들은 물까치, 또는 휴대폰으로 튼 물까치 녹음"},
        {"t": "다른 새", "d": "까치·참새·직박구리·비둘기 등"},
        {"t": "말소리", "d": "녹음에 동의한 내 목소리"},
        {"t": "배경", "d": "바람·빗소리·조용한 교정"},
        {"t": "기타", "d": "자동차·문·발걸음 같은 생활 소리"},
      ]},
      {"type": "linkbtn", "href": "https://www.inaturalist.org/observations?taxon_name=Cyanopica%20cyanus&sounds=true&quality_grade=research", "label": "iNaturalist — 물까치 녹음 모음 (녹음마다 라이선스 확인)"},
      {"type": "code", "label": "코드 ① · 예시 모으기 (Thonny에서 실행)", "lang": "python", "file": "snippets/eco_1_collect.py"},
      {"type": "callout", "kind": "tip", "title": "끝낼 때와 저장 위치", "html": "셸에 <code>s</code>를 입력하면 끝나요. 저장할 때마다 셸에 이름표별 개수가 표시돼요. 예시는 녹음용 SD의 <code>eco/examples.csv</code>에 쌓이고, 피코 메모리 때문에 모두 <b>300개</b>까지만 저장해요."},
      {"type": "dig", "title": "숫자 25개는 무엇일까?", "html": P[11]},
    ]},
    {"title": "② 물까치 탐지기", "items": [
      {"type": "text", "html": P[12]},
      {"type": "code", "label": "코드 ② · 물까치 탐지기", "lang": "python", "file": "snippets/eco_2_finder.py"},
      {"type": "concept", "items": [
        {"t": "희미한 파랑", "d": "기다리는 중"},
        {"t": "노랑", "d": "3초 듣는 중"},
        {"t": "파랑", "d": "생각하는 중"},
        {"t": "청록", "d": "물까치 후보. 켜진 칸 수 = 물까치 표 수"},
        {"t": "빨강 깜빡임", "d": "문제가 생김 (Thonny로 연결해 메시지 확인)"},
      ]},
      {"type": "step_head", "html": "예상 화면"},
      _out("예시를 불러왔어요: {'물까치': 15, '다른 새': 12, '말소리': 10, '배경': 10, '기타': 10}\n듣기 시작! (조용할 때 31 → 기준 82) 끝내려면 버튼.\n2026-10-01 07:21:40  아니에요 (물까치 1표, 가장 많은 표: 말소리)\n2026-10-01 07:22:15  물까치인가 봐요! (5/9표) → 20261001_072215_mulkkachi.wav\n물까치 후보 1번 찾았어요.\n안전하게 끝났어요. 이제 전원을 뽑아도 됩니다."),
      {"type": "prompt", "label": "① 바이브코딩 — 오늘 찾은 횟수를 LED로 (그대로 복사)", "text": "라즈베리파이 피코 2 WH MicroPython 코드 eco_2_finder.py를 고쳐줘.\n- 물까치 후보를 찾을 때마다 그날 찾은 횟수를 세어, 기다리는 동안 LED 10칸에 그 횟수만큼 희미한 청록을 켜 줘(10번 넘으면 10칸).\n- eco_lib.py의 함수(E.led 등)는 그대로 쓰고, 판단 방식(K_NN, MIN_VOTES)은 바꾸지 마.\n- 버튼을 누르면 안전하게 끝나는 흐름은 유지해."},
    ]},
    {"title": "③ 채점하고 기준 정하기", "items": [
      {"type": "text", "html": P[13]},
      {"type": "steps", "items": [
        {"t": "녹음 모으기", "d": "탐지기가 저장한 WAV, 휴대폰 녹음, 공개 녹음 가운데 <b>예시로 쓰지 않은 녹음</b>을 모아요."},
        {"t": "채점 폴더 만들기", "d": "PC에 폴더 하나를 만들고 그 안에 <code>시험/물까치</code>, <code>시험/다른 새</code>, <code>시험/말소리</code> … 폴더를 만들어 WAV를 나눠 넣어요."},
        {"t": "피코 예시 복사", "d": "녹음용 SD의 <code>eco/examples.csv</code>를 카드 리더로 꺼내 그 폴더에 복사해요."},
        {"t": "PC 준비", "d": "코드 ③은 피코가 아니라 PC에서 실행해요. Thonny 오른쪽 아래 인터프리터를 <b>'이 컴퓨터의 Python'</b>으로 바꾸고, <b>도구 → 패키지 관리</b>에서 <code>numpy</code>를 한 번 설치해요."},
        {"t": "채점 실행", "d": "코드 ③을 그 폴더에 <code>eco_pc_score.py</code>로 저장하고 실행해요. 명령 창을 쓴다면 <code>python eco_pc_score.py 폴더이름</code>(안 되면 <code>python3</code>)이에요."},
        {"t": "기준 정하기", "d": "표를 보고 MIN_VOTES를 고른 뒤 탐지기 코드에 적어요."},
        {"t": "(선택) WAV로 만든 예시와 비교", "d": "같은 폴더에 <code>학습/물까치</code>, <code>학습/다른 새</code> … 폴더를 만들어 WAV를 넣으면 그 녹음으로 만든 예시(<code>examples_pc.csv</code>)도 함께 채점해요. 이쪽이 더 좋으면 SD의 <code>examples.csv</code>를 <code>examples_pico.csv</code>로 이름을 바꿔 보관하고 <code>examples_pc.csv</code>를 <code>examples.csv</code> 이름으로 넣어요."},
      ]},
      {"type": "code", "label": "코드 ③ · PC 채점 도구 (PC에서 실행 · numpy 필요)", "lang": "python", "file": "snippets/eco_pc_score.py", "fold": True},
      _out("시험 녹음: 물까치 10개, 그 밖의 소리 27개\n\n[피코에서 모은 예시 (examples.csv)] {'물까치': 12, '다른 새': 12, '말소리': 8, '배경': 8, '기타': 8}\nMIN_VOTES | 재현율(물까치 녹음 가운데 찾은 비율) | 오판(다른 소리를 물까치라고 한 비율)\n    1     |  0.90  |  0.67\n    2     |  0.80  |  0.37\n    3     |  0.70  |  0.30\n    4     |  0.70  |  0.15\n    5     |  0.60  |  0.07\n    6     |  0.30  |  0.00\n    7     |  0.00  |  0.00\n    8     |  0.00  |  0.00\n    9     |  0.00  |  0.00"),
      {"type": "callout", "kind": "info", "title": "이 표는 어떤 조건의 결과일까", "html": "교재를 만들 때 모의 피코에 공개 녹음(새소리·생활 소리)과 합성 말소리를 들려주어 예시 48개를 모으고, 예시에 쓰지 않은 녹음으로 코드 ③을 실행한 결과예요. 시험 녹음은 물까치 10개와 그 밖의 소리 27개였어요. 녹음이 적어서 한 개만 달라져도 재현율이 0.10씩 바뀌어요. 앞의 '얼마나 잘 맞힐까?'에 나온 오판 13%는 같은 녹음을 나눠 쓴 조건이라 이 표보다 낮아요. 우리 학교에서 모은 녹음으로 다시 채점하면 결과가 달라져요."},
      {"type": "callout", "kind": "mini", "title": "탐구 과제", "html": P[14]},
    ]},
    {"title": "④ 여러 새 구분하기 (2단계)", "items": [
      {"type": "text", "html": P[15]},
      {"type": "code", "label": "코드 ④ · 여러 새 구분", "lang": "python", "file": "snippets/eco_3_species.py"},
    ]},
    {"title": "⑤ 현장으로 — 배터리와 자동 시작", "items": [
      {"type": "text", "html": P[16]},
      {"type": "steps", "items": [
        {"t": "main.py로 저장", "d": "코드 ②를 Thonny에서 <code>main.py</code>라는 이름으로 피코에 저장"},
        {"t": "PC에서 한 번 확인", "d": "USB를 뽑았다 꽂아 LED가 희미한 파랑으로 켜지는지 봐요"},
        {"t": "배터리로 바꾸기", "d": "USB 케이블을 보조배터리에 연결"},
        {"t": "설치", "d": "사람이 대화하지 않는 곳, 비를 피하는 곳. 설치 사실을 알림"},
        {"t": "끝내기", "d": "버튼 → LED가 꺼지면 전원 분리 → SD 카드 회수"},
        {"t": "다시 실험하려면", "d": "PC에 연결하고 Thonny의 <b>정지</b> 버튼을 누르면 탐지기가 멈추고 다른 코드를 실행할 수 있어요. 현장 관측을 마치고 자동 시작을 없애려면 피코의 <code>main.py</code>를 지우거나 <code>finder_saved.py</code>로 이름을 바꿔요."},
      ]},
      {"type": "callout", "kind": "warn", "title": "사람 목소리가 저장될 수 있어요", "html": "탐지기는 소리가 날 때마다 3초를 SD 카드에 녹음하고, 물까치 후보가 아니면 지워요. 그래서 대화가 들리는 곳에 두면 판단 결과와 상관없이 대화가 잠시 녹음되고, 잘못 판단하면 파일로 남아요. 설치 사실을 알렸다고 대화 녹음이 허용되는 것은 아니므로 대화가 들리지 않는 곳에 설치해요. 사람 목소리가 든 파일은 공유하지 않고 바로 지워요."},
    ]},
    {"title": "⑥ 물까치는 언제 나타났을까", "items": [
      {"type": "text", "html": P[17]},
      {"type": "steps", "items": [
        {"t": "안전하게 끝내기", "d": "버튼을 눌러 LED가 꺼지면 USB 전원을 뽑아요."},
        {"t": "카드 옮기기", "d": "Pmod에서 녹음용 microSD를 빼 카드 리더로 PC에 연결하고, 카드의 <code>eco</code> 폴더를 PC에 복사해요."},
        {"t": "그래프 그리기", "d": "코드 ⑤를 복사한 <code>eco</code> 폴더 옆에 <code>eco_pc_timeline.py</code>로 저장하고, Thonny의 '이 컴퓨터의 Python'으로 실행해요. <code>matplotlib</code>는 도구 → 패키지 관리에서 설치해요. 그래프는 <code>eco/timeline_hour.png</code>에 저장돼요."},
      ]},
      {"type": "code", "label": "코드 ⑤ · 시간 그래프 (PC에서 실행 · matplotlib 필요)", "lang": "python", "file": "snippets/eco_pc_timeline.py", "fold": True},
      {"type": "callout", "kind": "info", "title": "구글 시트로 보내기 (선택)", "html": P[18]},
      {"type": "code", "label": "Apps Script (구글 시트 → 확장 프로그램 → Apps Script에 붙여 넣고 웹 앱으로 배포)", "lang": "javascript", "code": _APPS},
    ]},
    {"title": "문제 해결과 확인", "items": [
      {"type": "mistakes", "items": [
        {"sym": "① SD 카드 실패", "cause": "SPI0 헤더 선이 바뀌었거나, 카드가 exFAT", "fix": "그림 2를 보고 양 끝 이름을 다시 맞추고, 카드를 <b>FAT32</b>로 포맷해요."},
        {"sym": "③ 마이크 소리가 작음", "cause": "D20·A2 케이블이 바뀌었거나 L/R 선이 빠짐", "fix": "그림 3대로 다시 꽂고 L/R이 GND에 연결됐는지 확인해요."},
        {"sym": "MP3가 조용함", "cause": "쉴드 스위치가 3.3V, 또는 MP3용 SD에 파일이 없음", "fix": "스위치를 <b>5V</b>로, 모듈용 SD에 0001.mp3를 넣어요."},
        {"sym": "시계가 멈춘 적이 있어요", "cause": "CR1220 전지가 없거나 시계를 맞춘 적이 없음", "fix": "전지를 넣고 Thonny로 연결해 코드 ⓪을 다시 실행해요."},
        {"sym": "예시가 부족해요", "cause": "이름표가 하나뿐이거나 이름표마다 3개 미만", "fix": "코드 ①로 이름표마다 10개 이상 모아요."},
        {"sym": "아무 소리에나 물까치라고 함", "cause": "물까치 예시만 많고 헷갈릴 만한 소리 예시가 적음", "fix": "다른 새·배경·기타 예시를 늘리고, 채점해서 MIN_VOTES를 올려요."},
        {"sym": "배터리로 돌리다 저절로 꺼짐", "cause": "보조배터리가 전기를 적게 쓰는 기기를 끊음", "fix": "Always On 기능이 있는 배터리를 써요."},
      ]},
      {"type": "check", "items": [
        {"q": "물까치 예시만 모으면 안 되는 이유는?", "a": "가까운 예시가 모두 물까치뿐이라, 어떤 소리를 들려줘도 물까치라고 답하게 돼요."},
        {"q": "MIN_VOTES를 올리면 무엇이 달라지나요?", "a": "오판은 줄고, 놓치는 물까치는 늘어요."},
        {"q": "채점은 왜 예시로 쓰지 않은 녹음으로 하나요?", "a": "예시로 쓴 녹음은 피코가 거의 같은 예시를 이미 가지고 있어서, 점수가 실제보다 높게 나와요."},
        {"q": "후보 횟수가 물까치 수와 같나요?", "a": "아니에요. 같은 무리가 여러 번 울 수 있고, 잘못 판단한 것도 섞여 있어요."},
      ]},
    ]},
    {"title": "다음 장 미리 보기", "items": [
      {"type": "text", "html": P[19]},
    ]},
  ],
}
