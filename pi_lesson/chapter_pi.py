# -*- coding: utf-8 -*-
# ML 확장판 ML3장 「물까치를 확인하는 라즈베리파이」 — build_site.py의 CHAPTERS 포맷
# 본문 문단(P)은 솔라 프로4 집필본(solar/solar_final.md). 코드·표·그림·단계 안내는 클로드 작성
import os, re, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
from parts import PI_BUY
from figs_pi import FIG_NET

_txt = open(os.path.join(_HERE, "solar", "solar_final.md"), encoding="utf-8").read()
P = {int(m.group(1)): m.group(2).strip() for m in re.finditer(r"### 블록 (\d+)\n(.*?)(?=\n### 블록 |\Z)", _txt, re.S)}

SITE = "https://greatsong.github.io/2026-vibe-pico"

def _fig(svg, cap):
    return {"type": "raw", "html": f"<div class='ecofig'>{svg}</div><p class='ecofig-cap'>{cap}</p>"}

def _out(text):                     # 예상 화면
    return {"type": "raw", "html": "<pre style='background:var(--code-bg);color:var(--code-text);border-radius:12px;padding:12px 14px;font-size:12.5px;overflow-x:auto'>" + text + "</pre>"}

_TABLE = ("<div style='overflow-x:auto'><table class='plan-table'>"
          "<tr><th>방식</th><th>물까치 재현율</th><th>다른 새를 물까치로</th><th>새 아닌 소리를 물까치로</th></tr>"
          "<tr><td>피코만 (3표 이상)</td><td>0.73</td><td>0.24</td><td>0.20</td></tr>"
          "<tr><td><b>BirdNET만</b> (신뢰도 0.25 이상)</td><td>0.46</td><td>0.01</td><td>0.00</td></tr>"
          "<tr><td>BirdNET만 (신뢰도 0.10 이상)</td><td>0.62</td><td>0.01</td><td>0.00</td></tr>"
          "<tr><td>피코 2표 이상 → BirdNET 0.25</td><td>0.35</td><td>0.01</td><td>0.00</td></tr>"
          "</table></div>"
          "<p class='ecofig-cap'>교재를 만들 때 공개 녹음(물까치 26개, 다른 새 119개, 새 아닌 소리 46개)을 피코와 같은 3초·16kHz 소리로 바꿔 시험한 결과예요. "
          "피코 예시는 시험과 다른 녹음으로 만들었어요. 녹음마다 3초 조각 두 개까지 판단하고, 하나라도 물까치라고 하면 그 녹음을 물까치라고 한 것으로 셌어요. 실물 라즈베리파이·피코에서 잰 값은 아니에요.</p>")

_AUDIO = ("<div style='display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 14px'>"
          + "".join(f"<a class='linkbtn' href='../pi_lesson/audio/{f}' download>🔊 {f} · {t}</a>"
                    for f, t in (("0004.mp3", "참새인가 봐요"), ("0005.mp3", "멧비둘기인가 봐요"), ("0006.mp3", "박새인가 봐요"), ("0007.mp3", "큰부리까마귀인가 봐요")))
          + "</div>")

_SERVER_RUN = """cd ~/bird
source venv/bin/activate
python bird_server.py"""

_SERVER_UPDATE = f"wget -O bird_server.py.new {SITE}/snippets/bird_server.py && mv bird_server.py.new bird_server.py"

CHAPTER_PI = {
  "id": "chpi", "num": "ML3", "title": "물까치를 확인하는 라즈베리파이 — BirdNET 판정 서버",
  "accent": "#B91C4A",
  "subtitle": "라즈베리파이 5를 BirdNET 서버로 만들어, 피코가 모은 소리를 다시 판정하고 실시간으로 새 이름을 알려 줘요.",
  "goals": [
    "라즈베리파이 5에서 BirdNET 판정 서버를 켜고 PC 브라우저로 접속한다",
    "피코가 저장한 물까치 후보 WAV를 BirdNET으로 다시 판정해 피코의 판단과 비교한다",
    "피코가 소리를 Wi-Fi로 보내 실시간으로 판정받고 새 이름을 말하게 한다",
    "피코만, BirdNET만, 둘을 이은 방식의 재현율과 오판을 비교해 관측 방식을 고른다",
  ],
  "why": P[1],
  "extra": "",
  "sections": [
    {"title": "시작하기 전에 — 흐름과 기대치", "items": [
      {"type": "text", "html": P[2]},
      _fig(FIG_NET, "그림 1. 실시간 판정(①②)과 2차 판정(③). 세 기기는 교실의 같은 공유기에 연결해요."),
      {"type": "step_head", "html": "얼마나 잘 맞힐까?"},
      {"type": "raw", "html": _TABLE},
      {"type": "callout", "kind": "info", "title": "표를 읽는 법", "html": P[3]},
    ]},
    {"title": "준비물", "items": [
      {"type": "raw", "html": PI_BUY},
      {"type": "text", "html": P[4]},
      {"type": "raw", "html": "<a class='linkbtn' href='#apxpi'>🔗 부록 · 라즈베리파이 5 세팅 A to Z</a>"},
    ]},
    {"title": "서버 켜기", "items": [
      {"type": "text", "html": P[5]},
      {"type": "steps", "items": [
        {"t": "부록 끝내기", "d": "부록 K까지 끝내면 <code>~/bird</code> 폴더에 가상환경, BirdNET, <code>bird_server.py</code>가 준비되어 있어요."},
        {"t": "자동 실행을 했다면", "d": "부록 L을 설정했다면 서버는 이미 켜져 있어요. 아래 명령은 건너뛰고 브라우저로 주소만 열어요."},
        {"t": "손으로 켜기", "d": "PC에서 <code>ssh 사용자이름@호스트이름.local</code>로 접속한 뒤 아래 명령 세 줄을 한 줄씩 붙여 넣어요. 첫 실행은 모델을 내려받느라 1~2분 걸려요."},
        {"t": "주소 확인", "d": "화면에 나온 <code>http://192.168.…:8000</code> 주소를 적어 두고, PC 브라우저에서 열어요."},
      ]},
      {"type": "code", "label": "라즈베리파이 SSH 창에서 (한 줄씩)", "lang": "bash", "code": _SERVER_RUN},
      {"type": "callout", "kind": "info", "title": "서버 파일을 교재의 새 버전으로 바꿀 때", "html": "<code>~/bird</code>에서 아래 한 줄을 실행해요. 내려받기에 실패하면 기존 파일은 그대로 남아요. 바이브코딩으로 고친 파일이 있다면 덮어써지니 먼저 다른 이름으로 복사해 둬요.<pre style='white-space:pre-wrap;margin:8px 0 0'>" + _SERVER_UPDATE + "</pre>"},
      {"type": "step_head", "html": "예상 화면"},
      _out("판정할 새 7종: 물까치, 까치, 직박구리, 참새, 멧비둘기, 박새, 큰부리까마귀\n브라우저에서 여세요 →  http://192.168.0.23:8000   (피코 코드의 SERVER에도 이 주소)\n * Serving Flask app 'bird_server'\n * Running on http://192.168.0.23:8000"),
      {"type": "callout", "kind": "tip", "title": "경고 문구는 괜찮아요", "html": "실행할 때 Flask의 개발용 서버라는 경고(WARNING: This is a development server)가 나올 수 있어요. 교실 공유기 안에서 쓰는 수업용이라 그대로 써도 돼요. 멈출 때는 <b>Ctrl+C</b>를 눌러요."},
      {"type": "code", "label": "bird_server.py (라즈베리파이에서 실행 · 위 wget으로 받는 파일과 같아요)", "lang": "python", "file": "snippets/bird_server.py", "fold": True},
    ]},
    {"title": "① 2차 판정 — 모아 둔 소리 다시 판정하기", "items": [
      {"type": "text", "html": P[6]},
      {"type": "steps", "items": [
        {"t": "카드 옮기기", "d": "피코 관측기에서 버튼을 눌러 끝내고, 녹음용 microSD를 카드 리더로 PC에 연결해 <code>eco</code> 폴더를 복사해요."},
        {"t": "올리기", "d": "판정 페이지에서 <b>파일 선택</b> → <code>_mulkkachi.wav</code>로 끝나는 파일을 여러 개 고르고 <b>올리고 판정하기</b>를 눌러요."},
        {"t": "표 보기", "d": "판정 · 가장 높은 새 · 신뢰도를 보고, 두 판정이 다른 파일은 ▶로 들어 봐요."},
        {"t": "세기", "d": "피코 후보 가운데 BirdNET도 물까치라고 한 파일 수를 세어 비율을 구해요. <b>판정 기록 CSV 내려받기</b>로 표를 저장해요."},
      ]},
    ]},
    {"title": "② 실시간 판정 — 피코가 묻고 라즈베리파이가 답하기", "items": [
      {"type": "text", "html": P[7]},
      {"type": "step_head", "html": "MP3 카드에 새 이름 4개 더 넣기"},
      {"type": "raw", "html": _AUDIO},
      {"type": "callout", "kind": "key", "title": "0003 다음에 차례로", "html": "MP3용 microSD에 이미 있는 0001~0003 뒤에 <code>0004.mp3</code> → <code>0005.mp3</code> → <code>0006.mp3</code> → <code>0007.mp3</code> 순서로 한 개씩 복사해요. Mac이라면 복사한 뒤 <code>dot_clean /Volumes/카드이름</code>을 실행해요. 번호가 섞였으면 카드를 포맷하고 0001부터 다시 복사해요."},
      {"type": "steps", "items": [
        {"t": "Wi-Fi 파일", "d": "피코에 <code>wifi_config.py</code>(본 교재 1장)가 있는지 확인해요. 교실 공유기의 이름과 비밀번호가 들어 있어야 해요."},
        {"t": "주소 적기", "d": "코드 ④의 <code>SERVER</code>에 우리 모둠 라즈베리파이 주소를 적어요. <code>http://</code>와 <code>:8000</code>까지 그대로 적어요."},
        {"t": "실행", "d": "라즈베리파이 서버가 켜진 상태에서 Thonny로 코드 ④를 실행해요. 판정 페이지 표에 피코가 보낸 줄이 생기는지 봐요."},
        {"t": "끝내기", "d": "버튼을 누르면 하던 판정을 마치고 안전하게 끝나요."},
      ]},
      {"type": "code", "label": "코드 ④ · 라즈베리파이에게 물어보는 탐지기 (피코에서 실행)", "lang": "python", "file": "snippets/eco_4_server.py"},
      {"type": "concept", "items": [
        {"t": "노랑", "d": "3초 듣는 중"},
        {"t": "파랑", "d": "피코가 표를 세는 중"},
        {"t": "보라", "d": "라즈베리파이에게 묻는 중"},
        {"t": "청록", "d": "BirdNET이 물까치라고 답함"},
        {"t": "흰색", "d": "BirdNET이 다른 새라고 답함"},
      ]},
      {"type": "step_head", "html": "예상 화면 (피코)"},
      _out("예시를 불러왔어요: {'물까치': 15, '다른 새': 12, '말소리': 10, '배경': 10, '기타': 10}\n라즈베리파이 서버 연결됨\n듣기 시작! (조용할 때 31 → 기준 82) 끝내려면 버튼.\n2026-10-01 07:21:40  BirdNET: 모르겠음 (가장 높은 새 없음 0.00) · 피코 1표\n2026-10-01 07:22:15  물까치인가 봐요! (피코 5표 · BirdNET 0.83) → 20261001_072215_cand.wav\n안전하게 끝났어요. 이제 전원을 뽑아도 됩니다."),
      {"type": "step_head", "html": "예상 화면 (라즈베리파이)"},
      _out("피코 → 20261001_072140_check.wav (지움)  모르겠음 (없음 0.00)\n피코 → 20261001_072215_cand.wav  물까치 (물까치 0.83)"),
      {"type": "callout", "kind": "info", "title": "SEND_ALL — 모두 물을까, 골라서 물을까", "html": P[8]},
    ]},
    {"title": "③ 세 방식 비교하기", "items": [
      {"type": "text", "html": P[9]},
      {"type": "steps", "items": [
        {"t": "틀어 주기", "d": "코드 ④를 켜 둔 채 휴대폰으로 물까치 녹음 5개 이상, 다른 새와 생활 소리 5개 이상을 하나씩 틀어요. 소리 사이에는 10초쯤 쉬어요."},
        {"t": "적어 두기", "d": "튼 순서와 시각을 종이에 적어요. 예) 07:31 물까치, 07:32 까치 …"},
        {"t": "정답 열 만들기", "d": "피코 SD의 <code>eco/server.csv</code>를 PC로 옮겨 스프레드시트로 열고, 맨 오른쪽에 <code>truth</code> 열을 만들어 물까치면 1, 아니면 0을 적은 뒤 CSV로 저장해요."},
        {"t": "비교 도구 실행", "d": "코드 ⑦을 <code>server.csv</code>와 같은 폴더에 저장하고, Thonny의 '이 컴퓨터의 Python'으로 실행해요. 설치할 것은 없어요."},
      ]},
      {"type": "code", "label": "코드 ⑦ · 세 방식 비교 도구 (PC에서 실행)", "lang": "python", "file": "snippets/eco_pc_compare.py", "fold": True},
      {"type": "step_head", "html": "예상 화면 (일부)"},
      _out("비교에 쓴 판정 18개 (물까치 6 · 다른 소리 12)\n\n방식                       | 재현율 | 오판\n피코만 MIN_VOTES 3          |  0.83  | 0.33\nBirdNET만 신뢰도 0.25       |  0.33  | 0.00\n피코 3표 → BirdNET 0.25    |  0.33  | 0.00\n(교재 제작 때 모의 시험의 18개 판정. 여러분의 기록으로 다시 계산하세요)"),
      {"type": "callout", "kind": "mini", "title": "탐구 과제", "html": P[10]},
      {"type": "prompt", "label": "바이브코딩 — 판정 페이지에 새별 막대그래프 (그대로 복사)", "text": "라즈베리파이의 Flask 서버 bird_server.py를 고쳐줘.\n- 첫 페이지(/)의 결과 표 위에, judged.csv에서 새 이름(species 열)별 판정 횟수를 막대그래프로 보여 줘.\n- 외부 라이브러리 없이 HTML과 CSS 막대(div 너비)로만 그려 줘.\n- '모르겠음'과 '읽기실패'는 그래프에서 빼 줘.\n- 기존의 /judge, /upload, /table 동작과 MIN_CONF, BIRDS 설정은 바꾸지 마."},
    ]},
    {"title": "현장에서 쓸 때", "items": [
      {"type": "text", "html": P[11]},
      {"type": "raw", "html": "<a class='linkbtn' href='#apxpi-10'>🔗 부록 L · 서버 자동 실행 설정</a>"},
    ]},
    {"title": "문제 해결과 확인", "items": [
      {"type": "mistakes", "items": [
        {"sym": "피코가 '연결 안 됨'이라고 해요", "cause": "SERVER 주소 오타, 다른 모둠의 주소, 서버가 꺼짐, 피코 Wi-Fi 실패", "fix": "먼저 PC 브라우저로 같은 주소가 열리는지 봐요. 열리면 피코의 <code>SERVER</code>와 <code>wifi_config.py</code>를, 안 열리면 라즈베리파이 서버를 확인해요. 고친 뒤에는 코드 ④를 다시 실행해요. 시작할 때 연결되지 않으면 끝날 때까지 BirdNET에 묻지 않아요."},
        {"sym": "PC 브라우저에서도 페이지가 안 열려요", "cause": "주소에 <code>:8000</code>이 빠짐, https로 입력, PC가 다른 Wi-Fi에 연결됨, 공유기의 AP 격리", "fix": "<code>http://주소:8000</code>으로 다시 입력하고, PC가 같은 공유기에 있는지 확인해요. 그래도 안 되면 부록의 'AP 격리' 항목을 봐요."},
        {"sym": "error: externally-managed-environment", "cause": "가상환경을 켜지 않고 pip를 실행함", "fix": "<code>cd ~/bird</code> 뒤 <code>source venv/bin/activate</code>를 먼저 실행해요. 줄 앞에 <code>(venv)</code>가 보여야 해요."},
        {"sym": "첫 실행에서 모델을 받다 멈춰요", "cause": "라즈베리파이가 인터넷에 연결되지 않음", "fix": "<code>ping -c 3 pypi.org</code>로 인터넷을 확인하고, 연결된 뒤 다시 실행해요. 한 번 받은 뒤에는 다시 받지 않아요."},
        {"sym": "엉뚱한 새 이름이 들려요", "cause": "MP3 카드의 복사 순서가 섞임", "fix": "카드를 포맷하고 0001부터 0007까지 한 개씩 차례로 복사해요."},
        {"sym": "거의 모두 '모르겠음'이에요", "cause": "소리가 작거나 멀어요. 피코 녹음은 8kHz까지만 담겨요", "fix": "휴대폰을 마이크에 더 가까이 두고 다시 틀어요. 탐구 1처럼 MIN_CONF를 낮춰 비교해 봐요."},
        {"sym": "SSH 창을 닫으면 서버가 꺼져요", "cause": "서버가 SSH 창 안에서 돌고 있음", "fix": "부록의 자동 실행(systemd)을 설정하면 창을 닫아도, 전원을 다시 켜도 서버가 돌아요."},
      ]},
      {"type": "check", "items": [
        {"q": "피코가 먼저 거른 뒤 BirdNET에 물으면 왜 놓치는 물까치가 늘어날까요?", "a": "피코가 물까치가 아니라고 걸러 낸 소리 가운데 BirdNET이라면 맞혔을 물까치가 있기 때문이에요. 두 판정이 놓치는 물까치가 서로 달라요."},
        {"q": "BirdNET이 '모르겠음'이라고 한 소리는 왜 지우나요?", "a": "새소리가 아닐 가능성이 높고, 사람 목소리가 들어 있을 수 있기 때문이에요."},
        {"q": "서버가 꺼지면 피코는 어떻게 하나요?", "a": "멈추지 않고 피코 판단만으로 관측을 이어 가요. server.csv에는 '서버 오류'로 남아요."},
        {"q": "재현율과 오판 가운데 무엇을 우선할지는 무엇으로 정하나요?", "a": "관측 목적으로 정해요. 물까치가 오는지 하나라도 알고 싶으면 재현율, 기록을 믿을 수 있어야 하면 오판을 먼저 봐요."},
      ]},
    ]},
    {"title": "정리", "items": [
      {"type": "text", "html": P[12]},
      {"type": "callout", "kind": "info", "title": "BirdNET 출처", "html": "BirdNET 모델과 라벨은 코넬 조류학 연구소(K. Lisa Yang Center for Conservation Bioacoustics)와 켐니츠 공과대학이 만들었어요. BirdNET 프로젝트는 모델 라이선스를 CC BY-NC-SA 4.0으로 안내해요. 수업과 연구 같은 비상업 용도로만 사용하고, 결과를 발표할 때는 BirdNET V2.4 모델과 만든 곳, 라이선스를 함께 밝혀요."},
    ]},
  ],
}
