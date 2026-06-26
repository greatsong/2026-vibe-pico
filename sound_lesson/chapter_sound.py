# -*- coding: utf-8 -*-
# 신규 챕터(별도 보관) — build_site.py의 CHAPTERS 포맷 그대로.
# 실기검증 후 이 dict를 CHAPTERS 리스트에 끼워 넣으면 합쳐집니다.

CHAPTER_SOUND = {
  "id": "chml", "num": "ML", "title": "소리를 배우는 피코 — 머신러닝 첫걸음",
  "accent": "#0891B2",
  "subtitle": "마이크 + k-NN으로 ‘내가 가르친 소리’(휘파람·박수·말소리·문·발걸음…)를 알아맞히는 만능 소리 분류기.",
  "goals": [
    "마이크로 소리를 숫자(특징)로 읽는다",
    "콘솔에서 키를 눌러 ‘내가 고른 소리들’을 직접 라벨링한다",
    "k-NN으로 새 소리가 무엇인지 예측한다",
    "정규화·k·확신도·다중클래스 같은 머신러닝 핵심 개념을 이해한다",
    "ML이 잘 되는 소리와 헷갈리는 소리의 차이를 안다",
  ],
  "why": "음성비서·새 찾기 앱·Shazam은 소리를 어떻게 알아들을까요? 비밀은 <b>소리를 숫자로 바꿔, 닮은 것과 비교</b>하는 거예요. 지금까지 피코는 <code>if 값 &gt; 임계값</code>으로만 판단했지만, <b>소리는 규칙 한 줄로 못 가릅니다.</b> 그래서 오늘은 다르게 — 내가 보여준 <b>소리 예시</b>만 모으면 피코가 스스로 경계를 찾습니다. 이것이 <b>지도학습</b>이고, 가장 직관적인 <b>k-NN</b>으로 ‘내 손이 만든 미니 음성 AI’를 만듭니다.",
  "extra": "<div style='margin:18px 0 6px;padding:16px 18px;border:1px solid var(--line);border-radius:14px;background:var(--code-bg)'>"
           "<div style='font-size:14px;font-weight:800;margin-bottom:2px'>🗺️ 이 챕터 한눈에</div>"
           "<div style='font-size:12.5px;color:var(--muted);margin-bottom:13px'>듣고 → 배우고 → 맞히고 → 말하는 <b>AI 한 사이클</b>을 직접 만들어요.</div>"
           "<div style='display:flex;flex-wrap:wrap;gap:9px'>"
           "<div style='flex:1;min-width:118px;background:#fff;border:1px solid var(--line);border-radius:10px;padding:11px 8px;text-align:center'><div style='font-size:11px;font-weight:800;color:#0891B2'>1</div><div style='font-size:25px'>🎤</div><div style='font-size:12.5px;font-weight:800;margin-top:3px'>듣기</div><div style='font-size:10.5px;color:var(--muted)'>마이크로 소리를</div></div>"
           "<div style='flex:1;min-width:118px;background:#fff;border:1px solid var(--line);border-radius:10px;padding:11px 8px;text-align:center'><div style='font-size:11px;font-weight:800;color:#0891B2'>2</div><div style='font-size:25px'>📊</div><div style='font-size:12.5px;font-weight:800;margin-top:3px'>숫자로</div><div style='font-size:10.5px;color:var(--muted)'>크기·높낮이·들쭉</div></div>"
           "<div style='flex:1;min-width:118px;background:#fff;border:1px solid var(--line);border-radius:10px;padding:11px 8px;text-align:center'><div style='font-size:11px;font-weight:800;color:#0891B2'>3</div><div style='font-size:25px'>🧠</div><div style='font-size:12.5px;font-weight:800;margin-top:3px'>배우기</div><div style='font-size:10.5px;color:var(--muted)'>예시 모아 k-NN</div></div>"
           "<div style='flex:1;min-width:118px;background:#fff;border:1px solid var(--line);border-radius:10px;padding:11px 8px;text-align:center'><div style='font-size:11px;font-weight:800;color:#0891B2'>4</div><div style='font-size:25px'>🔮</div><div style='font-size:12.5px;font-weight:800;margin-top:3px'>맞히기</div><div style='font-size:10.5px;color:var(--muted)'>새 소리 예측</div></div>"
           "<div style='flex:1;min-width:118px;background:#fff;border:1px solid var(--line);border-radius:10px;padding:11px 8px;text-align:center'><div style='font-size:11px;font-weight:800;color:#0891B2'>5</div><div style='font-size:25px'>🔊</div><div style='font-size:12.5px;font-weight:800;margin-top:3px'>표현</div><div style='font-size:10.5px;color:var(--muted)'>LED·음성(MP3)</div></div>"
           "</div>"
           "<div style='margin-top:13px;padding:9px 13px;border-radius:10px;background:#fff7ed;border:1px solid #fed7aa;color:#c2410c;font-size:13px;font-weight:700'>⭐ 와우 — 안 가르친 소리도 맞히는 ‘일반화’의 순간</div>"
           "</div>",
  "sections": [
    {"title": "시작하기 전에 — 준비물과 순서", "items": [
      {"type": "text", "html": "완전 처음이어도 괜찮아요. 아래 준비물만 확인하고 <b>코드 ①→②→③→④ 순서</b>로 한 칸씩 따라오면 됩니다. 막히면 각 단계의 <b>‘예상 화면’</b>과 맨 끝 <b>‘자주 하는 실수’</b>를 보세요."},
      {"type": "concept", "items": [
        {"t": "준비물", "d": "피코 2 WH + 그로브 쉴드, <b>마이크</b>(아날로그 또는 INMP441), WS2813 LED(2장에서 쓰던 것), USB 케이블. <b>새로 살 건 마이크뿐</b>이에요."},
        {"t": "진행 순서", "d": "① 마이크 값 보기 → ② 특징 뽑기 → ③ 소리 모으기 → ④ 예측. <b>한 코드씩 ▶로 실행</b>합니다."},
        {"t": "걸리는 시간", "d": "데이터 모으기 2~3분 + 예측까지, 천천히 해도 넉넉해요."},
      ]},
      {"type": "callout", "kind": "tip", "title": "마이크는 둘 중 아무거나 — 처음이면 아날로그",
       "html": "<b>처음이면 그로브 아날로그 마이크</b>(A1 포트에 꽂기만)로 시작하길 권해요. 익숙해지면 INMP441(음질↑)로 바꾸면 됩니다. 연결법은 아래 <b>‘하드웨어 준비’</b> 섹션에 있어요."},
    ]},
    {"title": "핵심 개념 — 기계가 소리를 배운다는 것", "items": [
      {"type": "text", "html": "어려운 수학은 없어요. 오늘의 전부는 딱 한 문장 — <b>‘새 소리와 가장 닮은 이웃에게 물어본다’</b>입니다. 먼저 도구와 개념을 천천히 짚어요."},
      {"type": "concept", "items": [
        {"t": "지도학습", "d": "<b>정답(라벨)이 붙은 예시</b>로 배워, 새 데이터의 정답을 맞히는 것. 우리는 소리마다 <b>이름</b>(휘파람·박수…)을 알려줍니다."},
        {"t": "k-NN", "d": "새 소리와 <b>가장 닮은(가까운) 이웃 k개</b>의 다수결로 결정. <code>k</code>는 ‘몇 명에게 물어볼까’예요."},
        {"t": "‘학습’의 정체", "d": "k-NN은 훈련이 따로 없어요. <b>예시를 통째로 기억</b>해뒀다 비교할 뿐. 그래서 <b>모델 = 우리가 모은 데이터</b>입니다."},
        {"t": "특징(feature)", "d": "소리에서 뽑은 숫자 3개 — <b>크기(RMS)</b>=얼마나 큰가, <b>높낮이(ZCR)</b>=얼마나 높은가, <b>들쭉날쭉(crest)</b>=톡 치는 소리(박수·노크)인가 이어지는 소리(목소리)인가."},
      ]},
      {"type": "callout", "kind": "key", "title": "정규화 — 단위가 다르면 공평하지 않다",
       "html": "세 특징의 범위가 제각각이에요. 높낮이는 <b>0~수천</b>, 크기는 <b>0~수만</b>, 들쭉날쭉은 <b>1~수십</b>. 그냥 거리를 재면 숫자가 큰 <b>크기에만 휘둘립니다</b>. 그래서 <b>세 특징을 각각 0~1로</b> 다시 스케일해 공평하게 만들어요. 머신러닝에서 거의 항상 필요한 단계랍니다."},
      {"type": "dig", "title": "영교차(ZCR)가 어떻게 ‘높낮이’가 되나요?",
       "html": "소리는 0(가운데)을 중심으로 <b>위아래로 출렁이는 물결</b>이에요. <b>높은 소리</b>일수록 물결이 빨라서 <b>0을 더 자주 지나갑니다</b>. 그래서 ‘0을 몇 번 지났나(영교차수)’를 세면 음의 <b>높낮이</b>를 대신할 수 있어요. 휘파람은 영교차가 많고, 낮은 ‘우~’ 허밍은 적습니다. FFT 같은 어려운 수학 없이도 음높이를 잡는 똑똑한 꼼수예요."},
      {"type": "callout", "kind": "info", "title": "k 고르기 & 확신도",
       "html": "<b>k=1</b>은 이웃 하나에 휘둘려 과민(과적합), <b>너무 큰 k</b>는 경계가 흐려져요. 보통 <b>홀수 5</b>. <b>확신도</b>는 다수 비율 — 이웃 5 중 4가 ‘박수’면 ‘박수, 확신 80%’이고, 이걸 <b>LED 칸 수</b>로 보여줍니다."},
      {"type": "callout", "kind": "info", "title": "2가지에서 여러 가지로 — 다중클래스",
       "html": "성공/실패 같은 2개만이 아니라, <b>휘파람·박수·말소리·노크</b>처럼 <b>여러 종류</b>도 똑같이 됩니다. 이웃 k명의 <b>다수결</b>에서 가장 표를 많이 받은 이름이 답이에요. 소리 종류마다 <b>LED 색</b>을 다르게 켭니다."},
    ]},

    {"title": "하드웨어 준비 — 마이크 연결하기 (아주 자세히)", "items": [
      {"type": "text", "html": "마이크는 두 가지 중 <b>하나만</b> 쓰면 됩니다. 완전 처음이면 <b>경로 A(아날로그)</b>를 강력 추천 — 점퍼 없이 케이블만 꽂으면 되거든요. (둘 다 꽂아도 괜찮아요.) 결과를 보여줄 <b>LED(2장에서 쓰던 것)</b>도 함께 표시했어요 — <b>D16 포트</b>에 그로브 케이블로 꽂으면 됩니다. 아래 <b>인터랙티브 배선표</b>에서 포트·핀을 하나씩 체크하며 따라오세요."},
      {"type": "raw", "html": "<div class=\"wire\" data-ac=\"#0891B2\" data-parts=\"mic_a,inmp441,led\"></div>"},
      {"type": "step_head", "html": "🟢 <b>경로 A · 그로브 아날로그 마이크</b> — 케이블만 꽂으면 끝"},
      {"type": "steps", "items": [
        {"t": "쉴드 확인", "d": "피코가 그로브 쉴드 위에 잘 꽂혀 있는지 봅니다."},
        {"t": "케이블 한쪽", "d": "그로브 4핀 케이블 한쪽을 <b>마이크 모듈</b>에 ‘딸각’."},
        {"t": "케이블 다른쪽", "d": "다른쪽을 쉴드의 <b>A1 포트</b>에 ‘딸각’. <b>(A0은 가스센서가 쓰니 꼭 A1!)</b>"},
        {"t": "전원", "d": "피코를 USB로 컴퓨터에 연결."},
        {"t": "끝!", "d": "점퍼·납땜 없이 이게 전부예요."},
      ]},
      {"type": "step_head", "html": "🔵 <b>경로 B · INMP441</b> — 음질 업그레이드 (점퍼 6선 · 거의 나란히)"},
      {"type": "callout", "kind": "warn", "title": "먼저! VDD는 반드시 3.3V — 5V 금지",
       "html": "INMP441은 3.3V 소자라 <b>VDD를 5V에 꽂으면 망가집니다.</b> 쉴드가 피코 40핀을 모두 헤더로 뽑아주니, 그 헤더에 점퍼선(암-수)을 꽂으면 돼요. <b>요령</b>: 신호선 바로 양옆의 GND(<b>23·28번</b>)를 쓰면 <b>23~28번 한 군데</b>에 거의 다 모입니다. 7색 리본선이면 <b>가장자리 ‘흰’선은 안 꽂은 채로</b> 두고(자를 필요 없어요 — 재사용해요) 나머지를 순서대로 꽂으세요. 정작 중요한 건 색이 아니라 <b>신호↔핀</b> 짝이에요 — 다른 선이면 색이 달라도 됩니다.<br><br><b>⚠ 특히 — 리본선을 ‘통째로’ 연속 삽입하지 마세요.</b> 센서 보드는 한 줄이 아니라 <b>2열 6핀</b>이라, 핀 순서가 쉴드 23~28번과 1:1로 맞지 않아요. <b>VDD 한 선만 23~28 묶음과 떨어진 위쪽 36번(3V3)으로 따로</b> 올려야 합니다. 색 순서를 믿지 말고, 아래 핀맵처럼 <b>센서 글자(실크) → 피코 핀 번호</b>를 한 선씩 확인하세요."},
      {"type": "raw", "html": (
        '<div style="margin:8px 0 2px">'
        '<div style="font-weight:800;font-size:13.5px;color:#0f172a;margin-bottom:8px">📷 INMP441 센서 보드 핀맵 — 한 줄이 아니라 <span style="color:#b91c1c">2열 6핀</span> <span style="font-weight:600;color:#64748b">(보드 글자를 읽는 방향 기준)</span></div>'
        '<table style="border-collapse:separate;border-spacing:7px;width:100%;max-width:560px;font-size:12.5px;line-height:1.35">'
        '<tr>'
        '<td style="background:#eef2ff;border:1px solid #c7d2fe;border-radius:10px;padding:9px 8px;text-align:center"><b style="font-size:15px">SCK</b><br><span style="color:#475569">→ GP18 · 24번</span></td>'
        '<td style="background:#eef2ff;border:1px solid #c7d2fe;border-radius:10px;padding:9px 8px;text-align:center"><b style="font-size:15px">WS</b><br><span style="color:#475569">→ GP19 · 25번</span></td>'
        '<td style="background:#ecfdf5;border:1px solid #bbf7d0;border-radius:10px;padding:9px 8px;text-align:center"><b style="font-size:15px">L/R</b><br><span style="color:#475569">→ <b>GND</b> · 28번</span></td>'
        '</tr><tr>'
        '<td style="background:#eef2ff;border:1px solid #c7d2fe;border-radius:10px;padding:9px 8px;text-align:center"><b style="font-size:15px">SD</b><br><span style="color:#475569">→ GP20 · 26번</span></td>'
        '<td style="background:#fef2f2;border:2px solid #fca5a5;border-radius:10px;padding:9px 8px;text-align:center"><b style="font-size:15px;color:#b91c1c">VDD ⚠</b><br><span style="color:#b91c1c"><b>→ 3V3 · 36번</b> (5V 아님!)</span></td>'
        '<td style="background:#ecfdf5;border:1px solid #bbf7d0;border-radius:10px;padding:9px 8px;text-align:center"><b style="font-size:15px">GND</b><br><span style="color:#475569">→ <b>GND</b> · 23번</span></td>'
        '</tr></table>'
        '<div style="font-size:12px;color:#475569;margin-top:7px">위쪽 줄 <b>SCK · WS · L/R</b> / 아래쪽 줄 <b>SD · VDD · GND</b> — 서로 <b>다른 줄</b>이에요. '
        '<b style="color:#b91c1c">VDD만</b> 23~28 묶음에서 떨어진 <b>36번(3V3)</b>으로, <b>L/R은 신호가 아니라 GND</b>로 갑니다.</div>'
        '</div>'
      )},
      {"type": "steps", "items": [
        {"t": "GND → GND(23번)", "d": "<b>주</b> 점퍼 — SCK 바로 옆 GND"},
        {"t": "SCK → GP18(24번)", "d": "<b>노</b> 점퍼 — 클록"},
        {"t": "WS → GP19(25번)", "d": "<b>초</b> 점퍼 — <b>반드시 SCK 바로 다음 핀</b>"},
        {"t": "SD → GP20(26번)", "d": "<b>파</b> 점퍼 — 데이터"},
        {"t": "L/R → GND(28번)", "d": "<b>보</b> 점퍼 — SD 옆 GND(왼쪽 채널)"},
        {"t": "VDD → 3V3(36번)", "d": "<b>회</b> 점퍼 — <b>⚠ 5V 아님!</b> 23~28 묶음과 떨어진 <b>위쪽 36번</b>으로 따로"},
      ]},
      {"type": "callout", "kind": "warn", "title": "전원(USB) 켜기 전 — 이 3가지부터 확인",
       "html": "<b>① VDD → 3V3(36번)</b> 인가요? (5V면 즉시 손상) &nbsp; <b>② GND → GND</b> 인가요? &nbsp; <b>③ L/R → GND</b> 인가요? (신호 핀 아님!)<br>이 세 개만 맞으면 나머지 SCK·WS·SD는 GP18·19·20에 순서대로 꽂혀 있으면 됩니다. <b>리본 색이 아니라 센서 글자 라벨</b> 기준으로 한 선씩 짚어 보세요."},
      {"type": "callout", "kind": "tip", "title": "배선이 헷갈리면",
       "html": "‘배선 위젯/그림’의 핀맵을 보세요. INMP441은 그로브 포트가 아니라 <b>헤더 핀</b>에 점퍼로 꽂는다는 점만 기억하면 됩니다."},
      {"type": "step_head", "html": "이제 값을 읽어 ‘소리가 숫자가 되는’ 걸 봅니다"},
      {"type": "code", "label": "코드 ① · 마이크 값 읽기 (아날로그 A1)", "lang": "python", "file": "snippets/sound_read.py"},
      {"type": "callout", "kind": "tip", "title": "INMP441로 한다면",
       "html": "코드 이름 뒤에 <code>_i2s</code>가 붙은 버전을 쓰세요(예: <code>sound_read_i2s.py</code>). 나머지 흐름은 똑같아요. 4종은 맨 끝 ‘INMP441 버전 모음’에 접어 뒀어요."},
      {"type": "steps", "items": [
        {"t": "붙여넣기", "d": "Thonny 편집창에 코드 ①을 붙여넣어요."},
        {"t": "실행", "d": "▶(초록 실행) 버튼을 누릅니다."},
        {"t": "플로터 켜기", "d": "메뉴 <b>보기 → Plotter</b> 체크 → 숫자가 그래프로 보여요."},
        {"t": "소리 내기", "d": "휘파람·박수를 해보세요."},
      ]},
      {"type": "check_list", "items": [
        "콘솔/플로터에 <b>숫자가 흐르나요?</b> (안 나오면 ▶ 다시, 포트 확인)",
        "휘파람을 불면 그래프가 <b>출렁</b>이나요?",
        "가만히 있으면 값이 <b>작게(거의 0)</b> 유지되나요?",
        "박수를 치면 값이 <b>순간 확</b> 튀나요?",
      ]},
    ]},

    {"title": "따라하기 ① 소리를 잡아 특징 뽑기", "items": [
      {"type": "step_head", "html": "소리가 나면 한 덩어리(약 0.2초)로 잡아, <b>크기(RMS)·높낮이(ZCR)·들쭉날쭉(crest)</b> 세 숫자를 뽑습니다. 이 셋이 다음 단계 예측의 입력이에요."},
      {"type": "code", "label": "코드 ② · 소리 감지 + 특징 추출", "lang": "python", "file": "snippets/sound_detect.py"},
      {"type": "callout", "kind": "info", "title": "이렇게 뜨면 성공! (예상 화면)",
       "html": "휘파람을 불면 셸에 <code>소리 감지!  크기=320  높낮이=181  들쭉날쭉=3.2</code> 처럼 떠요. <b>박수·노크</b>는 들쭉날쭉이 <b>크고</b>, <b>목소리·허밍</b>은 <b>작게</b> 나옵니다. 소리마다 세 숫자가 달라지면 성공!"},
      {"type": "callout", "kind": "tip", "title": "감지가 안 되거나 너무 잦으면",
       "html": "코드가 시작할 때 <b>배경소음을 재서 임계값을 자동</b>으로 정해요. 그래도 안 맞으면 <code>THRESH</code> 식의 숫자(<code>*2</code>)를 조절하세요. 소리가 안 잡히면 ↓, 가만히 있어도 잡히면 ↑."},
    ]},

    {"title": "따라하기 ② 내 소리 직접 모으기 (혼자, 콘솔 키)", "items": [
      {"type": "text", "html": "데이터 모으기가 <b>이 책에서 제일 쉬워졌어요</b> — 와이파이도 짝도 필요 없습니다. Thonny <b>셸에 숫자 키</b>를 누르고 그 소리를 내면 자동 저장돼요."},
      {"type": "steps", "items": [
        {"t": "키 누르기", "d": "셸에 <code>1</code>(휘파람) 등 숫자를 입력 (LED 주황)"},
        {"t": "소리 내기", "d": "<b>3초 안에</b> 그 소리를 한 번 → 가장 또렷한 0.2초가 저장(LED 초록). <b>큰 소리 아니어도 OK!</b>"},
        {"t": "반복", "d": "소리마다 <b>10개씩</b> (또렷한 소리면 5개도 OK). 종류마다 <b>비슷한 수</b>로!"},
        {"t": "끝내기", "d": "<code>s</code> 입력 → <code>sounds.csv</code> 완성"},
      ]},
      {"type": "callout", "kind": "info", "title": "몇 개나 모아야 할까? — 학습곡선으로 본 정밀 가이드",
       "html": "실제로 표본 수를 늘려가며 정확도를 재봤어요. 필요한 개수는 <b>‘소리가 얼마나 비슷한가’</b>에 달렸습니다:<br>• <b>또렷이 다른 소리</b>(휘파람·박수처럼) → <b>각 3~5개</b>면 거의 100%.<br>• <b>조금 헷갈리는 소리</b> → <b>각 10개</b> 권장(여기서 정확도가 거의 평평해져요. 15~20개로 늘려도 +2~3%p뿐).<br>• <b>많이 헷갈리거나 종류가 5개 이상</b> → <b>20~30개+</b> 필요(또는 아래 <b>FFT 심화</b>로 특징 늘리기).<br><b>개수보다 ‘균형’이 더 중요</b>해요 — 한 소리만 30개·다른 건 3개면 30개짜리 쪽으로 쏠립니다. 소리마다 비슷한 수로!"},
      {"type": "callout", "kind": "key", "title": "조용한 곳에서! — 좋은 데이터의 조건",
       "html": "배경이 시끄러우면 ‘좋은 예시’가 안 모여요. <b>조용한 곳에서, 마이크에 비슷한 거리</b>로 소리를 내세요. ‘<b>좋은 데이터가 좋은 AI를 만든다</b>’ — 이게 오늘의 진짜 교훈이에요."},
      {"type": "code", "label": "코드 ③ · 소리 모으기 (콘솔 라벨링)", "lang": "python", "file": "snippets/sound_record.py"},
      {"type": "callout", "kind": "info", "title": "이렇게 뜨면 성공! (예상 화면)",
       "html": "숫자 키를 누르고 소리를 내면 <code>저장! 휘파람 (크기=320 높낮이=181 들쭉=3.2) | 현재: {'휘파람': 3}</code> 처럼 개수가 쌓여요. 종류마다 <b>10개+</b>가 되면 <code>s</code>로 끝내세요."},
      {"type": "callout", "kind": "tip", "title": "어떤 소리든 가르칠 수 있어요 — LABELS 한 줄만 바꾸기",
       "html": "코드 위쪽 <code>LABELS</code> 딕셔너리만 고치면 끝! 예) <code>{\"1\":\"사람목소리\", \"2\":\"노크\", \"3\":\"문여닫기\", \"4\":\"발걸음\"}</code>. 가르칠 소리를 <b>여러분이 정하세요.</b>"},
      {"type": "callout", "kind": "info", "title": "‘정적(조용함)’은 왜 안 가르치나요?",
       "html": "<b>예측</b>은 임계값을 넘는 소리에만 반응해요 — 피코는 <b>소리가 날 때만</b> 깨어나 ‘무슨 소리지?’를 판단합니다. 조용할 땐 아무 일도 안 일어나죠. 그게 ‘정적’이라, <b>정적은 따로 가르칠 필요가 없어요.</b> 비슷해서 ‘잘 모르겠는 소리’는 뒤에서 <b>확신도가 낮으면 침묵</b>으로 거릅니다."},
    ]},

    {"title": "따라하기 ③ 3D 산점도로 눈으로 보기 (Plotly)", "items": [
      {"type": "text", "html": "특징이 <b>3개</b>가 됐으니 평면(2D)이 아니라 <b>3차원</b>으로 봅니다. PC에서 <b>Plotly</b>로 그리면 마우스로 <b>빙글빙글 돌려가며</b> 무리가 갈리는지 볼 수 있어요."},
      {"type": "callout", "kind": "key", "title": "잠깐 — 이 코드는 ‘피코’가 아니라 ‘내 PC’에서 돌아요",
       "html": "앞의 코드(①~④)는 피코에 올려 ▶로 실행했죠. 하지만 <b>이 그래프 코드는 PC의 파이썬</b>으로 돌립니다. 그래서 <b><code>sounds.csv</code>와 <code>plot_sounds.py</code>를 PC의 <u>같은 폴더</u>에 두는 것</b>이 핵심이에요."},
      {"type": "steps", "items": [
        {"t": "1. 폴더 만들기", "d": "PC 바탕화면에 폴더 하나(예: <code>sound</code>)를 만들어요."},
        {"t": "2. CSV 내려받기", "d": "Thonny 왼쪽 ‘파일’ 창에서 <code>sounds.csv</code> 우클릭 → <b>Download</b> → 방금 만든 폴더에 저장."},
        {"t": "3. 코드 저장", "d": "아래 <code>plot_sounds.py</code>를 <b>같은 폴더</b>에 같은 이름으로 저장."},
        {"t": "4. 라이브러리 설치(처음 1번만)", "d": "Windows는 <b>명령 프롬프트</b>, Mac은 <b>터미널</b>을 열고 <code>pip install plotly pandas</code> 입력."},
        {"t": "5. 폴더로 이동 → 실행", "d": "<code>cd</code>로 그 폴더에 들어가 <code>python plot_sounds.py</code> 실행(안 되면 <code>python3</code>). → 브라우저에 3D 그래프가 떠요!"},
      ]},
      {"type": "code", "label": "그래프 코드 (PC에서 실행 · sounds.csv와 같은 폴더에)", "lang": "python", "file": "snippets/plot_sounds.py"},
      {"type": "callout", "kind": "tip", "title": "터미널이 어렵다면 — Thonny로 그냥 실행",
       "html": "PC에 깔린 <b>Thonny</b>로도 돼요(피코 켤 때 쓰던 그 프로그램!). ① <code>plot_sounds.py</code>를 Thonny로 열기 → ② 오른쪽 아래 인터프리터를 <b>‘이 컴퓨터의 Python’</b>으로 바꾸기 → ③ <code>sounds.csv</code>가 같은 폴더에 있는지 확인하고 ▶ 실행. (단, <code>plotly·pandas</code>는 <b>도구 → 패키지 관리</b>에서 한 번 설치해야 해요.)"},
      {"type": "prompt", "label": "AI에게 시켜도 돼요 (바이브코딩)",
       "text": "sounds.csv(열: rms, zcr, crest, label)를 plotly로 3D 산점도를 그려줘. label별로 색을 다르게 하고 마우스로 회전되게 해줘. 축 이름은 크기/높낮이/들쭉날쭉으로."},
      {"type": "callout", "kind": "key", "title": "무리가 갈리나요?",
       "html": "소리별 점들이 <b>다른 덩어리</b>로 모여 있으면 → 예측이 잘 될 신호. 두 소리가 <b>겹쳐</b> 있으면 → 헷갈리는 어려운 문제(특징을 더 넣을 차례 — 아래 <b>FFT 심화</b>)."},
    ]},

    {"title": "따라하기 ④ k-NN으로 예측 → LED로 표현", "items": [
      {"type": "text", "html": "이제 모은 데이터를 ‘모델’ 삼아 새 소리를 예측합니다. <b>소리마다 다른 색</b>으로, 확신도만큼 LED 칸이 켜져요. <code>k</code>를 1과 7로 바꿔 차이도 느껴보세요. 아래 <b>동작 흐름</b>에서 소리를 골라 ‘듣기→특징→정규화→k-NN→확신→출력’ 6단계를 눈으로 따라가 보세요."},
      {"type": "raw", "html": "<div class=\"flow\" data-ac=\"#0891B2\"></div>"},
      {"type": "code", "label": "코드 ④ · k-NN 예측 + LED", "lang": "python", "file": "snippets/sound_predict.py"},
      {"type": "callout", "kind": "info", "title": "이렇게 뜨면 성공! (예상 화면)",
       "html": "새 소리를 내면 <code>이건… 휘파람!  (확신 92%, 크기=318 높낮이=181 들쭉=3.2)</code> 가 뜨고, <b>LED가 그 소리의 색</b>으로 확신도만큼 켜집니다. 안 가르친 살짝 다른 소리도 맞히면 — 그게 바로 <b>일반화</b>예요!"},
      {"type": "callout", "kind": "info", "title": "왜 하필 k-NN? — 실제 데이터로 확인했어요",
       "html": "공개 음성 데이터(모음·음소 분류)로 여러 알고리즘을 직접 견줘봤더니, <b>피코에 넣을 수 있는 것 중 k-NN이 가장 정확</b>했어요(소리가 다양해질수록 격차가 더 커집니다). 게다가 코드에선 <b>‘가까운 이웃일수록 큰 표’를 주는 거리 가중</b>으로 한 단계 더 똑똑하게 만들었답니다."},
      {"type": "prompt", "label": "막히면 AI에게 (바이브코딩)",
       "text": "이 MicroPython k-NN 코드에서 k 값을 바꾸거나, 예측 결과를 더 보기 좋게 출력하도록 고쳐줘. sounds.csv는 rms,zcr,crest,label 형식이야."},
    ]},

    {"title": "★ 다양하게 실험해보기 — 무엇이든 가르쳐 보세요", "items": [
      {"type": "text", "html": "같은 코드로 <b>가르칠 소리만 바꾸면</b> 끝없이 실험할 수 있어요. 쉬운 것부터 도전까지, 난이도 순으로 골라보세요. (어려운 건 <b>INMP441 + 조용한 환경 + 마이크 가까이</b>를 권해요.)"},
      {"type": "concept", "items": [
        {"t": "🟢 쉬움 (깔끔히 갈림)", "d": "<b>휘파람 · 박수 · 노크</b>. 높낮이·크기·들쭉날쭉이 뚜렷이 달라서 거의 항상 잘 맞아요. <b>첫 성공 경험용으로 강력 추천.</b>"},
        {"t": "🟡 중간", "d": "<b>말소리(“아~”) · 노크 · 박수</b>. ‘지속되는 소리 vs 톡 치는 소리’가 섞여 재밌어요."},
        {"t": "🔵 도전", "d": "<b>문 여닫는 소리 · 복도 발걸음 · 누구 목소리</b>. 작고 비슷해서 잘 안 될 수 있어요 — 그래서 <b>가장 좋은 수업거리</b>예요."},
      ]},
      {"type": "callout", "kind": "info", "title": "발걸음·문소리가 잘 안 잡히면? — 그게 정상이고, 그게 핵심",
       "html": "발걸음은 <b>소리가 아주 작고</b>, 사람마다 비슷해요. 잘 안 맞는 건 버그가 아니라 <b>‘특징 안에 신호가 부족하다’</b>는 ML의 정직한 한계랍니다. 해결의 방향은 둘 — ① <b>마이크를 더 가까이</b>(바닥/문 근처)·INMP441 사용, ② <b>특징을 더 추가</b>(아래)."},
      {"type": "callout", "kind": "info", "title": "특징 공학 — 왜 ‘들쭉날쭉’을 기본에 넣었나 (데이터로 확인)",
       "html": "크기·높낮이 <b>2개만</b>으론 ‘톡 치는 소리(박수·노크)’와 ‘이어지는 소리(목소리·허밍)’가 잘 안 갈려요. 그래서 <b>들쭉날쭉(crest)=최댓값÷평균크기</b>을 기본 특징으로 넣었습니다. 실제 데이터로 재보니 정확도가 <b>0.73 → 0.96</b>으로 뛰었어요(음량이 변해도 안정적 — 비율이라). ‘더 좋은 특징 = 더 똑똑한 ML’ = <b>특징 공학</b>. 더 올리려면? 아래 <b>FFT 심화</b>로!"},
    ]},

    {"title": "INMP441(음질↑) 버전 코드 모음", "items": [
      {"type": "text", "html": "INMP441을 점퍼로 연결한 분은 아래 4종을 쓰세요. <b>특징·k-NN·LED는 위와 완전히 같고</b>, 마이크 읽는 부분만 다릅니다."},
      {"type": "code", "label": "I2S ① · 값 읽기", "lang": "python", "file": "snippets/sound_read_i2s.py", "fold": True},
      {"type": "code", "label": "I2S ② · 감지 + 특징", "lang": "python", "file": "snippets/sound_detect_i2s.py", "fold": True},
      {"type": "code", "label": "I2S ③ · 소리 모으기", "lang": "python", "file": "snippets/sound_record_i2s.py", "fold": True},
      {"type": "code", "label": "I2S ④ · k-NN 예측", "lang": "python", "file": "snippets/sound_predict_i2s.py", "fold": True},
    ]},

    {"title": "모의 테스트 — 하드웨어 없이 브라우저에서 체험", "items": [
      {"type": "text", "html": "피코가 없어도 괜찮아요. 아래에서 소리를 골라 누르면 같은 <b>3특징 k-NN</b>이 맞히고, <b>목소리로 말해줍니다</b>(MP3 출력 미리보기!). ‘내 마이크’ 탭에선 진짜 마이크로 직접 가르치고 테스트할 수도 있어요."},
      {"type": "raw", "html": "<div class=\"mocktest\" data-ac=\"#0891B2\"></div>"},
      {"type": "callout", "kind": "tip", "title": "마이크 모드는 https에서",
       "html": "‘내 마이크’ 탭은 브라우저 마이크 권한이 필요해, <b>배포된 https 사이트</b>에서 가장 잘 됩니다. 버튼 모드는 어디서나 동작해요."},
    ]},
    {"title": "INMP441 심화 — FFT 주파수밴드로 음색까지 (성능 끌어올리기)", "items": [
      {"type": "text", "html": "예측이 잘 돼야 재밌죠. 더 어려운 소리(휘파람 vs 쉬익, 모음 ‘아’ vs ‘이’처럼 <b>음색만 다른</b> 소리)까지 가르려면 특징을 더 풍부하게 — <b>8개 주파수 대역의 에너지</b>를 씁니다. 음성비서가 쓰는 방식의 축소판이에요. (INMP441 권장, ulab 없이 Goertzel로 계산.)"},
      {"type": "callout", "kind": "info", "title": "한 파일로 수집→예측까지",
       "html": "이 코드는 실행하면 <b>[수집]</b>(숫자키로 소리 모으기) → <code>go</code> 입력 → <b>[예측]</b> 순으로 한 번에 돌아갑니다. 음색이 다른 소리일수록 효과가 커요."},
      {"type": "code", "label": "코드 ⑤ · FFT 주파수밴드 + k-NN (INMP441 심화)", "lang": "python", "file": "snippets/sound_fft_i2s.py", "fold": True},
      {"type": "callout", "kind": "key", "title": "특징을 늘릴수록…",
       "html": "특징 2개(0.73) → 3개(0.96) → FFT 8밴드는 <b>음색이 비슷한 소리</b>까지 잡아냅니다. 단 계산이 무거워 <b>INMP441(깨끗한 16kHz)</b>에서 제일 잘 돼요. ‘성능 = 좋은 특징’임을 몸으로 확인하는 코너."},
    ]},
    {"title": "자주 하는 실수", "items": [
      {"type": "mistakes", "items": [
        {"sym": "데이터가 적거나 한 소리만 많음", "cause": "한 소리만 잔뜩 모으면 늘 그 소리로만 예측해요(불균형).", "fix": "소리마다 <b>비슷한 수로 10개씩</b>. 잘 안 맞으면 15~20개로 늘리거나 더 또렷한 소리로 바꾸세요."},
        {"sym": "높낮이·들쭉날쭉이 무시됨", "cause": "정규화를 빼먹어 큰 숫자(크기)에만 휘둘림.", "fix": "<b>세 특징을 0~1로 정규화</b>(코드의 <code>norm()</code>)하세요."},
        {"sym": "예측이 자꾸 이상", "cause": "<code>k</code>가 짝수라 동점.", "fix": "<b>홀수(5,7)</b>로 두세요."},
        {"sym": "어제는 됐는데 오늘 틀림", "cause": "배경소음·마이크 거리가 달라짐.", "fix": "<b>조용한 곳·같은 거리</b>로, 환경이 바뀌면 다시 모으세요."},
        {"sym": "비슷한 두 소리를 헷갈림", "cause": "특징 안에 구분 신호가 부족(버그 아님).", "fix": "<b>특징 추가</b>(들쭉날쭉)나 <b>INMP441</b>로 음질을 올리세요."},
      ]},
    ]},

    {"title": "스스로 점검하기", "items": [
      {"type": "check", "items": [
        {"q": "k-NN에서 ‘학습’은 무엇을 하나요?", "a": "훈련이 따로 없고, <b>예시를 기억</b>해뒀다 새 데이터와 비교합니다. 모델 = 데이터."},
        {"q": "정규화는 왜 필요할까요?", "a": "크기(0~수만)·높낮이(0~수천)·들쭉날쭉(1~수십)의 범위가 제각각이라, 안 하면 큰 숫자(크기)에만 휘둘려요. <b>세 특징을 0~1로</b> 맞춰 공평하게."},
        {"q": "영교차(ZCR)가 왜 ‘높낮이’인가요?", "a": "높은 소리일수록 물결이 빨라 <b>0을 더 자주 지나가</b>기 때문이에요."},
        {"q": "확신 80%는 무슨 뜻인가요?", "a": "가까운 이웃 5개 중 4개가 같은 답을 냈다는 뜻."},
        {"q": "발걸음이 잘 안 맞으면 버그인가요?", "a": "아니에요. <b>특징 안에 신호가 부족</b>한 ML의 정직한 한계. 특징을 더하거나 마이크를 가까이 하면 나아집니다."},
      ]},
    ]},

    {"title": "수업/학습 시나리오", "items": [
      {"type": "text", "html": "한 흐름(자기주도 학습 또는 한두 차시)과 ‘와우 포인트’입니다. 모든 무게는 <b>장면 4 — 안 가르친 소리를 맞히는 0.5초</b>에 싣습니다."},
      {"type": "dig", "title": "장면별 흐름과 와우 포인트",
       "html": "<b>① 훅</b> — “음성비서·Shazam은 어떻게 알아들을까?” 소리의 ‘모양’으로 판단함을 던진다.<br>"
               "<b>② 소리가 숫자가 된다</b> 🌟 — 플로터로 휘파람·박수를. 즉각성·신체성.<br>"
               "<b>③ 규칙으로 해보기 → 막힘</b> — <code>if</code>로 못 가름 → ML의 필요성.<br>"
               "<b>④ 첫 인식</b> ⭐ <b>메인 와우</b> — 모은 것과 살짝 다른 새 소리를 맞힘 = ‘일반화’. 일부러 다르게 해 증명.<br>"
               "<b>⑤ 일부러 깨뜨리기</b> 🌟 — 비슷한 소리·시끄러운 곳은 헷갈림 → 특징·과적합·정직한 한계.<br>"
               "<b>⑥ 내 소리 만들기</b> 🌟 — 가르칠 소리·의미를 학습자가 정함(주도성).<br>"
               "<b>⑦ 정리</b> — 음성비서·낙상 감지·새 식별 앱이 다 이 원리. 지도학습 개념 명명."},
      {"type": "callout", "kind": "info", "title": "정직한 한 방 (선택)",
       "html": "“쉬운 소리는 90% 넘게 맞히는데, 발걸음은 왜 어려울까?” → 특징을 더하거나(들쭉날쭉) 센서를 더 좋은 걸로(INMP441). <b>‘특징 안에 신호가 있어야 ML이 된다’</b>를 남기며 마무리."},
    ]},
  ],
}
