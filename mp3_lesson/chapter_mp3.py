# -*- coding: utf-8 -*-
# 심화 챕터(별도 보관) — build_site.py의 CHAPTERS 포맷 그대로.
# 소리 분류(chml) 챕터를 끝낸 다음에 붙이는 '출력' 편.
# 독학용: 처음부터 끝까지 순서대로 따라가면 되도록 상세화.
# 기본 끝낸 뒤 합칠지 결정. 합치려면 이 dict를 CHAPTERS 리스트에 끼워 넣으면 됩니다.

CHAPTER_MP3 = {
  "id": "chsay", "num": "ML+", "title": "피코가 말을 한다 — 소리의 주인공을 목소리로",
  "accent": "#7C3AED",
  "subtitle": "k-NN이 알아맞힌 소리에게 ‘이름’을 붙여 목소리로 말해주는 출력기. Grove MP3 v4로 듣기→생각→말하기 한 사이클을 완성합니다.",
  "goals": [
    "출력 모듈(Grove MP3 v4)에 UART로 ‘명령’을 보내 소리를 낸다",
    "분류 결과(이름표)를 음성 파일 번호로 잇는 <code>TRACK</code> 표를 이해한다",
    "‘자기 소리 되먹임’과 ‘모듈 부팅’ 같은 현실 문제를 코드로 다스린다",
    "확신이 낮으면 ‘모르겠어요’ 하고 침묵하는 규칙을 넣는다",
    "입력(마이크)→처리(k-NN)→출력(음성)의 AI 한 바퀴를 직접 잇는다",
  ],
  "why": "소리 분류 챕터에서 피코는 ‘이건 휘파람!’이라고 <b>속으로만</b> 알았어요(콘솔 글자·LED 색). 그런데 음성비서·새 찾기 앱은 거기서 한 발 더 나아가 <b>사람의 말로 대답</b>합니다. 오늘은 그 마지막 한 칸을 채워요. 분류 결과라는 <b>이름표</b>를, Grove MP3 v4를 통해 <b>들리는 목소리</b>로 되돌려줍니다. 그러면 ‘기계가 듣고·생각하고·말한다’는 AI의 한 사이클이 눈앞에서 완성돼요. <b>아래 순서대로 한 칸씩만 따라오면</b> 됩니다.",
  "extra": "",
  "sections": [

    {"title": "0단계 · 시작하기 전에 (준비물 점검)", "items": [
      {"type": "text", "html": "이 챕터는 <b>소리 분류 챕터의 ‘다음 편’</b>이에요. 시작 전에 아래 세 가지가 준비됐는지 먼저 확인하세요. 하나라도 비면 그 챕터를 먼저 끝내고 오면 됩니다."},
      {"type": "check_list", "items": [
        "소리 분류 챕터에서 만든 <b><code>sounds.csv</code></b>가 피코 안에 들어 있다 (이게 ‘모델’이에요)",
        "마이크가 연결돼 있고, 휘파람·박수가 <b>이미 잘 구분</b>됐다",
        "새로 준비한 <b>Grove MP3 v4.0 모듈</b>(스피커 포함, Grove 케이블), <b>FAT32로 포맷한 microSD</b>, PC에서 카드를 읽을 <b>카드 리더</b>가 있다",
      ]},
      {"type": "callout", "kind": "info", "title": "완성하면 이런 모습이에요 (미리 그려보기)",
       "html": "마이크에 대고 <b>휘파람</b>을 붑니다 → 피코가 0.5초 생각하더니 → 스피커에서 <b>“휘파람이에요!”</b> 하고 말합니다. 박수를 치면 <b>“박수네요!”</b>. 가르친 네 소리 어디에도 표가 모이지 않는 애매한 소리엔 <b>조용히</b> 있어요. 이 한 장면을 만드는 게 오늘의 목표예요."},
      {"type": "callout", "kind": "key", "title": "오늘 추가되는 건 ‘입’ 하나뿐",
       "html": "듣기(마이크)·생각하기(k-NN)는 <b>이미 다 만들었어요.</b> 오늘은 거기에 <b>말하는 입(MP3 모듈)</b>만 답니다. 그래서 새로 배우는 코드는 생각보다 적어요."},
    ]},

    {"title": "핵심 개념 — ‘출력기’가 마지막 한 칸을 채운다", "items": [
      {"type": "text", "html": "코드를 짜기 전에, 오늘 쓰는 부품과 개념을 하나씩 살펴봐요. 딱 네 가지만 이해하면 됩니다."},
      {"type": "concept", "items": [
        {"t": "입력 vs 출력", "d": "마이크는 소리를 <b>듣는</b> 입력, Grove MP3 v4는 소리를 <b>내는</b> 출력이에요. 방향이 정반대. 둘을 이으면 ‘듣고 대답하는 기계’가 됩니다."},
        {"t": "MP3 v4 = ‘똑똑한 부하 직원’", "d": "피코는 <b>“3번 곡 틀어”라는 명령만</b> 보내요. 파일 찾기·소리 키우기·스피커 울리기는 모듈이 알아서 해요. 피코는 소리를 직접 안 만듭니다."},
        {"t": "UART(시리얼)", "d": "두 기계가 <b>전선 한 줄로 글자를 주고받는</b> 약속이에요. 마치 두 사람이 실 전화기로 속닥이는 것. 피코의 <b>TX</b>(말하는 핀)와 모듈의 <b>RX</b>(듣는 핀)를 잇습니다."},
        {"t": "TRACK 표", "d": "소리 이름과 재생할 파일 번호를 짝지은 표예요. ‘휘파람’이면 1번, ‘박수’면 2번처럼요."},
      ]},
      {"type": "callout", "kind": "key", "title": "오늘의 한 문장 — ‘이름표를 목소리로 바꾸는 표’",
       "html": "k-NN이 내놓는 답은 <code>\"휘파람\"</code> 같은 <b>글자(이름표)</b>예요. 이걸 <code>TRACK = {\"휘파람\":1, \"박수\":2}</code>라는 <b>사전 한 줄</b>로 음성 트랙 번호에 연결합니다. 그게 전부예요."},
      {"type": "callout", "kind": "info", "title": "확신이 낮으면 — 침묵이 정답",
       "html": "분류가 흔들릴 때(이웃이 갈릴 때) 자신 있게 <b>틀린 답</b>을 말하면 더 나빠요. 그래서 <b>확신도가 기준(60%) 아래면 아무 말도 안 합니다.</b> ‘<b>모를 땐 모른다고 하는 것</b>’ — 좋은 AI의 태도이고, 한 줄(<code>if conf &gt;= CONF_MIN</code>)로 가르칠 수 있어요."},
    ]},

    {"title": "1단계 · 모듈 연결하기 (배선)", "items": [
      {"type": "step_head", "html": "Grove MP3 v4는 <b>그로브 4핀 케이블 하나</b>면 연결 끝이에요. 마이크는 앞 챕터 그대로 두고(VDD는 36번 3V3 그대로), MP3 모듈만 새로 답니다."},
      {"type": "callout", "kind": "warn", "title": "먼저 — USB를 뽑고 쉴드 스위치를 5V로",
       "html": "MP3 모듈은 <b>5V</b>에서 켜져요. USB를 뽑은 상태에서 쉴드 모서리 전원 스위치를 <b>5V</b>로 밀고, 배선을 모두 확인한 뒤 USB를 연결하세요. 마이크 VDD는 스위치와 상관없는 <b>36번(3V3)</b>에 꽂혀 있으니 그대로 두면 안전해요."},
      {"type": "steps", "items": [
        {"t": "MP3 모듈 꽂기", "d": "그로브 케이블로 쉴드의 <b>UART0 포트</b>에 ‘톡’ 꽂기 (피코 핀 TX=GP0, RX=GP1에 연결돼요. 쉴드에 UART 포트가 <b>두 개</b>인데 <b>UART1이 아니라 UART0</b>이에요!)"},
        {"t": "스피커 달기", "d": "모듈의 <b>스피커 단자</b>에 작은 스피커, 또는 <b>3.5mm 잭</b>에 이어폰을 꽂기"},
        {"t": "SD카드 꽂기", "d": "음성 MP3를 넣은 microSD를 모듈에 삽입 (만드는 법은 2단계)"},
      ]},
      {"type": "check_list", "items": [
        "MP3 모듈의 전원 LED에 <b>불이 들어오나요</b>?",
        "스피커(또는 이어폰)가 모듈에 <b>단단히</b> 꽂혔나요?",
        "SD카드가 <b>딸깍</b> 소리 나게 끝까지 들어갔나요?",
      ]},
    ]},

    {"title": "2단계 · 음성 파일 만들어 SD카드에 넣기", "items": [
      {"type": "step_head", "html": "소리 이름마다 한 마디 음성 파일을 SD 카드에 넣어요. 샘플 네 개를 받아 아래 순서대로 넣으면 돼요."},
      {"type": "callout", "kind": "info", "title": "샘플 음성 바로 받기 — 직접 안 만들어도 돼요",
       "html": "아래 4개(휘파람·박수·말소리·노크)를 받아 아래 순서대로 카드에 넣어요.<br><span style='display:inline-block;margin-top:8px'>"
               "<a href='samples/0001.mp3' download style='display:inline-block;margin:3px 5px 3px 0;padding:6px 12px;border:1px solid #7C3AED;border-radius:8px;color:#7C3AED;text-decoration:none;font-weight:700;font-size:13px'>⬇ 0001 휘파람</a>"
               "<a href='samples/0002.mp3' download style='display:inline-block;margin:3px 5px 3px 0;padding:6px 12px;border:1px solid #7C3AED;border-radius:8px;color:#7C3AED;text-decoration:none;font-weight:700;font-size:13px'>⬇ 0002 박수</a>"
               "<a href='samples/0003.mp3' download style='display:inline-block;margin:3px 5px 3px 0;padding:6px 12px;border:1px solid #7C3AED;border-radius:8px;color:#7C3AED;text-decoration:none;font-weight:700;font-size:13px'>⬇ 0003 말소리</a>"
               "<a href='samples/0004.mp3' download style='display:inline-block;margin:3px 5px 3px 0;padding:6px 12px;border:1px solid #7C3AED;border-radius:8px;color:#7C3AED;text-decoration:none;font-weight:700;font-size:13px'>⬇ 0004 노크</a>"
               "<a href='samples/sd_voice_samples.zip' download style='display:inline-block;margin:3px 5px 3px 0;padding:6px 12px;border:1px solid #7C3AED;background:#7C3AED;border-radius:8px;color:#fff;text-decoration:none;font-weight:700;font-size:13px'>⬇ 전체 ZIP</a>"
               "</span>"},
      {"type": "callout", "kind": "key", "title": "SD 카드 준비 (한 번만)",
       "html": "① 카드를 <b>FAT32</b>로 포맷해요. Windows는 카드 우클릭 → 포맷 → FAT32, Mac은 디스크 유틸리티 → 지우기 → MS-DOS(FAT)예요. 32GB 이하 카드가 편해요.<br>② 카드 <b>맨 위 폴더</b>에 <code>0001.mp3</code>부터 <b>한 개씩 순서대로</b> 복사해요. 이 모듈은 파일 이름이 아니라 복사한 순서로 번호를 매기는 경우가 많아서, 한꺼번에 끌어다 놓으면 순서가 섞일 수 있어요.<br>③ Mac에서 복사했다면 터미널에서 <code>dot_clean /Volumes/카드이름</code>을 실행해 숨김 파일을 지워요.<br>④ 3단계에서 1번·2번 음성이 맞게 나오는지 직접 들어 확인해요.<br>내 목소리로 바꾸고 싶으면 휴대폰 녹음 앱으로 MP3를 만들어 같은 번호 이름으로 넣으면 돼요."},
    ]},

    {"title": "3단계 · 모듈만 따로 테스트 (소리부터 확인!)", "items": [
      {"type": "step_head", "html": "분류와 합치기 <b>전에</b>, MP3 모듈이 혼자서도 소리를 잘 내는지부터 확인해요. 여기서 소리가 나야 다음 단계가 의미 있어요. <b>제일 먼저 넘어야 할 관문</b>이에요."},
      {"type": "code", "label": "코드 ① · MP3 모듈 단독 테스트 (1·2번 곡 재생)", "lang": "python", "file": "snippets/mp3_test.py"},
      {"type": "code", "label": "이렇게 나오면 성공! (셸 출력 + 스피커)", "lang": "text",
       "code": "> AT+VOL=22\n1번 곡(0001.mp3) 재생…\n> AT+PLAY=sd0,1\n  🔊 \"휘파람이에요\"\n2번 곡(0002.mp3) 재생…\n> AT+PLAY=sd0,2\n  🔊 \"박수네요\""},
      {"type": "callout", "kind": "tip", "title": "여기서 잠깐 🤔 — 코드가 하는 일",
       "html": "<b>Grove MP3 v4.0(WT2605CX)</b>은 <b>‘AT+’ 텍스트 명령</b>을 <b>115200 baud</b>로 받아요(v2.0의 <code>7E…EF</code> 바이너리와 완전 다름!). 맨 위에서 연결하고 모듈 <b>부팅을 1초 기다린 뒤</b>, <code>AT+VOL=22</code>로 <b>볼륨(0~31)</b>을, <code>AT+PLAY=sd0,1</code>로 <b>1번 곡</b>을 재생합니다. 명령 끝엔 항상 <code>\\r\\n</code>(줄바꿈)이 붙어요."},
      {"type": "callout", "kind": "warn", "title": "소리가 안 나면 — 이 순서로 점검",
       "html": "① 쉴드 모서리의 <b>전원 스위치가 5V</b>인가?(3V3면 모듈이 부팅을 못 해요) ② <b>UART0 포트</b>에 꽂았나?(UART1 아님) ③ <b>보드레이트 115200</b> 맞나?(v4.0 필수) ④ Grove 케이블이 <b>UART0 포트와 모듈에 끝까지</b> 꽂혔나? ⑤ 볼륨이 너무 작나?(<code>AT+VOL=22</code>→<code>28</code>) ⑥ SD가 <b>FAT32</b>이고 <code>0001.mp3</code>가 있나? ⑦ 부팅 대기(<code>1.0</code>→<code>2.0</code>초) 늘리기. 대부분 ①·②·④·⑥에서 해결돼요."},
      {"type": "check_list", "items": [
        "스피커에서 <b>1번 곡</b> 소리가 나나요?",
        "약 3초 뒤 <b>2번 곡</b>으로 바뀌나요?",
        "<code>AT+VOL=22</code>의 숫자를 5·31로 바꾸면 <b>음량</b>이 변하나요?",
      ]},
    ]},

    {"title": "4단계 · 분류 결과를 ‘목소리’로 (메인 완성)", "items": [
      {"type": "step_head", "html": "이제 마지막! 마이크로 들은 소리를 k-NN으로 알아맞히고, 그 <b>이름표에 맞는 음성 파일</b>을 재생합니다. 코드의 <code>TRACK</code> 표만 내 이름표에 맞추면 끝이에요."},
      {"type": "code", "label": "코드 ② · k-NN 예측 → 음성 출력 (+LED)", "lang": "python", "file": "snippets/mp3_say.py"},
      {"type": "code", "label": "이렇게 나오면 성공! (셸 출력 + 스피커)", "lang": "text",
       "code": "조용히… 배경소음 측정 중\n준비! 소리를 내면 누구인지 말해줄게요. (멈추려면 Ctrl+C)\n이건… 휘파람!  (확신 80%)\n  🔊 \"휘파람이에요\"\n이건… 박수!  (확신 100%)\n  🔊 \"박수네요\"\n음… 잘 모르겠어요 (확신 40%) — 조용히 있을게요"},
      {"type": "callout", "kind": "warn", "title": "여기가 핵심! 🔁 — 말하는 동안 들어온 소리는 버려요",
       "html": "스피커가 “휘파람이에요”라고 말하면 <b>그 소리를 마이크가 다시 듣고</b> 또 판단해버려요 → 끝없이 자기 말을 따라 하는 <b>무한 반복</b>! 그래서 <code>say()</code>는 ① 말하는 동안(<code>SPEAK_SEC</code>) 들어온 소리를 <b>계속 읽어서 버리고</b> ② 잔향이 0.3초 조용해질 때까지 기다립니다. 읽지 않고 쉬기만 하면 마이크 버퍼에 자기 목소리가 남아 다음 판단에 섞여요. 음성이 길어 끝까지 안 나오면 이 값을 늘리세요. <b>이게 이 챕터가 실제로 돌아가게 하는 장치예요.</b>"},
      {"type": "callout", "kind": "key", "title": "TRACK 표 = sounds.csv 이름표와 ‘글자까지’ 똑같이",
       "html": "<code>TRACK = {\"휘파람\":1, ...}</code>의 왼쪽 이름은 데이터를 모을 때 쓴 이름표와 <b>한 글자도 다르면 안 돼요.</b> ‘휘파람’과 ‘휘파람소리’는 다른 이름이라 음성이 안 나와요. 이름표를 바꿨다면 여기도 같이 고쳐요."},
      {"type": "callout", "kind": "tip", "title": "여기서 잠깐 🤔 — 침묵도 잘 되나요?",
       "html": "가르치지 않은 애매한 소리(헛기침 등)를 내 봐요. 네 종류를 가르쳤다면, 가장 많은 표를 받은 이름표가 다섯 표 중 두 표 이하(확신 60% 미만)일 때 “잘 모르겠어요”만 표시하고 <b>말하지 않아요</b>. 두 종류만 가르쳤다면 다섯 표 가운데 세 표 이상이 늘 한쪽에 모여서 항상 말해요."},
      {"type": "prompt", "label": "막히면 AI에게 (바이브코딩)",
       "text": "내 피코는 마이크로 들은 소리를 k-NN으로 분류한 뒤, MP3 모듈(Grove MP3 v4.0)로 소리 이름에 맞는 트랙을 재생해. 그런데 문제가 생겼어.\n- 소리가 안 나오거나 엉뚱한 곡이 나올 때 어디부터 점검해야 하는지 순서대로 알려줘.\n- 소리 이름표와 트랙 번호를 짝지어 둔 목록(TRACK)과 SD카드 파일 번호를 맞추는 방법도 정리해줘.\n- 스피커가 말하는 소리를 마이크가 다시 듣는 '되먹임'을 막으려고 둔 쉬는 시간(SPEAK_SEC)은 어떻게 조절하면 좋을지도 알려줘."},
    ]},

    {"title": "★ 생각해 보기 — 왜 목소리로 알려 줄까", "items": [
      {"type": "dig", "title": "LED 색과 목소리는 무엇이 다를까?",
       "html": "LED 색은 <b>약속을 외워야</b> 뜻을 알아요(‘초록=박수였지?’). 하지만 <b>목소리</b>는 약속이 필요 없어요 — 처음 보는 사람도 즉시 이해합니다. 분류 결과를 <b>사람의 언어로 되돌리는</b> 순간, AI가 ‘내 안의 숫자’에서 ‘남과 나누는 대화’로 바뀌어요. 이게 음성비서·낙상 알림·점자 안내기가 모두 ‘출력’에 공들이는 이유랍니다."},
      {"type": "callout", "kind": "info", "title": "교재 다른 부품과도 잇기",
       "html": "이 ‘출력 사고방식’은 어디든 통해요. <b>가스 센서 경보 → 안내 방송</b>, <b>밝기 임계값 → 안내 멘트</b>처럼, ‘판단 결과를 사람이 알아듣게 내보낸다’는 한 패턴입니다."},
    ]},

    {"title": "자주 하는 실수", "items": [
      {"type": "mistakes", "items": [
        {"sym": "아무 소리도 안 남", "cause": "쉴드 스위치가 3V3이거나, Grove 케이블이 UART0이 아닌 포트에 꽂힘.", "fix": "스위치를 <b>5V</b>로, 케이블을 <b>UART0</b>에 끝까지 꽂으세요."},
        {"sym": "첫 곡만 안 나옴", "cause": "모듈 부팅 전에 명령이 감.", "fix": "맨 위 <b>부팅 대기(1초)를 2초로</b> 늘려 보세요."},
        {"sym": "엉뚱한 곡이 나옴", "cause": "파일 복사 순서와 <code>TRACK</code> 값이 어긋남.", "fix": "SD카드를 포맷하고 <b>0001.mp3부터 순서대로</b> 다시 복사."},
        {"sym": "특정 이름표만 침묵", "cause": "<code>TRACK</code> 이름이 이름표와 글자가 다름.", "fix": "sounds.csv의 이름표와 <b>똑같이</b> 적으세요."},
        {"sym": "자기 말을 무한 반복", "cause": "스피커 소리를 마이크가 또 들음.", "fix": "<code>SPEAK_SEC</code>를 음성 길이만큼 <b>넉넉히</b>, 또는 스피커를 마이크에서 떼기."},
        {"sym": "맞혔는데 말을 안 함", "cause": "확신이 <code>CONF_MIN</code>보다 낮음.", "fix": "정상이에요. 데이터를 더 모으거나 기준값을 낮춰보세요."},
        {"sym": "소리가 너무 크거나 작음", "cause": "볼륨 설정값.", "fix": "<code>AT+VOL=22</code>의 숫자(0~31)를 조절하세요."},
      ]},
    ]},

    {"title": "스스로 점검하기", "items": [
      {"type": "text", "html": "다음 질문에 답할 수 있으면 이 장을 이해한 거예요. (먼저 스스로 답해보고 펼치세요)"},
      {"type": "check", "items": [
        {"q": "마이크와 MP3 모듈은 뭐가 다른가요?", "a": "마이크는 소리를 <b>듣는 입력</b>, MP3 v4는 소리를 <b>내는 출력</b>. 방향이 반대예요."},
        {"q": "피코가 MP3 모듈에 보내는 건 무엇인가요?", "a": "소리가 아니라 <b>“몇 번 곡 틀어”라는 명령</b>(UART). 재생은 모듈이 해요."},
        {"q": "TRACK 표는 무슨 일을 하나요?", "a": "분류 결과인 <b>이름표를 음성 파일 번호로</b> 이어 줍니다. 오늘의 핵심 한 줄."},
        {"q": "말하는 동안 마이크 입력을 왜 무시하나요?", "a": "스피커 소리를 마이크가 다시 듣고 <b>무한 반복</b>하는 ‘되먹임’을 막기 위해서예요."},
        {"q": "확신이 낮으면 왜 말을 안 하나요?", "a": "자신 있게 <b>틀린 답</b>을 하는 것보다 ‘모른다’가 낫기 때문. 좋은 AI의 태도예요."},
        {"q": "소리가 아예 안 날 때 1순위 점검은?", "a": "쉴드 스위치가 <b>5V</b>이고 케이블이 <b>UART0</b>에 꽂혔는지, 그리고 SD에 <code>0001.mp3</code>가 있는지."},
      ]},
    ]},

  ],
}
