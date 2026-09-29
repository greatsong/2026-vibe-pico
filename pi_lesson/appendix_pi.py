# -*- coding: utf-8 -*-
# ML 확장판 부록 「라즈베리파이 5 세팅 A to Z」 — 모니터 없이 PC에서 SSH로
# 본문 문단(P)은 솔라 프로4 집필본(solar/solar_apx_final.md). 명령어·단계·예상 화면은 클로드 작성
# 근거: etc/ai-kit-research/reference/12-rpi5-setup.md (2026-09-15 Raspberry Pi OS trixie, Imager 2.0.11.1)
import os, re, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
from parts import PI_BUY

_txt = open(os.path.join(_HERE, "solar", "solar_apx_final.md"), encoding="utf-8").read()
P = {int(m.group(1)): m.group(2).strip() for m in re.finditer(r"### 블록 (\d+)\n(.*?)(?=\n### 블록 |\Z)", _txt, re.S)}

SITE = "https://greatsong.github.io/2026-vibe-pico"

def _out(text):
    return {"type": "raw", "html": "<pre style='background:var(--code-bg);color:var(--code-text);border-radius:12px;padding:12px 14px;font-size:12.5px;overflow-x:auto'>" + text + "</pre>"}

_SERVICE = """sudo tee /etc/systemd/system/bird.service > /dev/null <<EOF
[Unit]
Description=BirdNET bird sound server
Wants=network-online.target
After=network-online.target

[Service]
Type=exec
User=$USER
WorkingDirectory=$HOME/bird
ExecStart=$HOME/bird/venv/bin/python -u $HOME/bird/bird_server.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF"""

CHAPTER_APXPI = {
  "id": "apxpi", "num": "부록", "title": "라즈베리파이 5 세팅 A to Z — 모니터 없이 PC에서",
  "accent": "#B91C4A",
  "subtitle": "부품 준비부터 운영체제 설치, SSH 접속, BirdNET 설치, 전원만 켜면 서버가 시작되는 설정까지 차례로 따라가요.",
  "goals": [
    "Raspberry Pi Imager로 microSD에 운영체제를 굽고 사용자·Wi-Fi·SSH를 미리 설정한다",
    "PC에서 SSH로 라즈베리파이에 접속해 명령을 실행한다",
    "가상환경에 BirdNET과 Flask를 설치하고 판정 서버를 실행한다",
    "서버가 부팅할 때 저절로 시작되게 하고, 주소 고정·안전한 종료를 익힌다",
  ],
  "why": P[1],
  "extra": "",
  "sections": [
    {"title": "A. 준비물", "items": [
      {"type": "text", "html": P[2]},
      {"type": "raw", "html": PI_BUY},
      {"type": "check_list", "items": [
        "PC가 Windows 10 이상 또는 macOS 13 이상이다",
        "교실 공유기의 Wi-Fi 이름과 비밀번호를 안다 (아이디 로그인 방식이 아니다)",
        "모둠 번호를 정했다 (호스트 이름에 써요. 예: bird-3)",
        "교실 공유기의 AP 격리(무선 격리)가 꺼져 있는지 관리자에게 확인했다 (켜져 있으면 PC에서 라즈베리파이에 접속할 수 없어요)",
      ]},
    ]},
    {"title": "B. 조립", "items": [
      {"type": "text", "html": P[3]},
      {"type": "steps", "items": [
        {"t": "팬 연결", "d": "케이스의 팬 선을 보드의 <b>FAN</b> 단자(4핀)에 꽂아요."},
        {"t": "케이스 닫기", "d": "보드를 케이스에 넣고 뚜껑을 닫아요."},
        {"t": "전원은 아직", "d": "microSD를 굽고 넣은 뒤(E 단계) 마지막에 전원을 연결해요."},
      ]},
    ]},
    {"title": "C. PC에 Raspberry Pi Imager 설치", "items": [
      {"type": "linkbtn", "href": "https://www.raspberrypi.com/software/", "label": "Raspberry Pi Imager 내려받기 (공식)"},
      {"type": "steps", "items": [
        {"t": "Windows", "d": "<code>.exe</code> 설치 파일을 받아 실행해요."},
        {"t": "macOS", "d": "<code>.dmg</code> 파일을 열고 Imager를 응용 프로그램 폴더로 끌어 넣어요."},
      ]},
    ]},
    {"title": "D. microSD에 운영체제 굽기", "items": [
      {"type": "text", "html": P[4]},
      {"type": "steps", "items": [
        {"t": "장치(Device)", "d": "<b>Raspberry Pi 5</b>를 골라요."},
        {"t": "운영체제(OS)", "d": "<b>Raspberry Pi OS (other)</b> → <b>Raspberry Pi OS Lite (64-bit)</b>를 골라요."},
        {"t": "저장장치(Storage)", "d": "카드 리더에 꽂은 microSD를 골라요. <b>시스템 드라이브 제외(Exclude system drives)</b>는 켜 둬요. PC의 하드디스크를 고르면 지워져요."},
        {"t": "호스트 이름", "d": "<code>bird-모둠번호</code> (예: <code>bird-3</code>). 영문 소문자·숫자·하이픈만 써요."},
        {"t": "지역(Localisation)", "d": "수도를 <b>Seoul</b>로 골라요. 시간대 Asia/Seoul, 키보드 kr이 함께 채워져요."},
        {"t": "사용자(User)", "d": "사용자 이름(영문 소문자)과 비밀번호를 정하고 <b>종이에 적어 둬요</b>. sudo를 쓸 때도 이 비밀번호를 입력해요."},
        {"t": "Wi-Fi", "d": "교실 공유기의 Wi-Fi 이름(SSID)과 비밀번호를 입력해요."},
        {"t": "원격 접속(Remote Access)", "d": "<b>Enable SSH</b>를 켜고 <b>Use password authentication</b>을 골라요."},
        {"t": "쓰기(Write)", "d": "쓰기와 검증(verify)이 끝날 때까지 기다린 뒤 카드를 꺼내요."},
      ]},
      {"type": "callout", "kind": "warn", "title": "사용자 지정을 건너뛰지 마세요", "html": "사용자 지정(Customisation)을 건너뛰면 첫 부팅 때 모니터 화면으로만 설정을 물어요. 모니터 없이는 접속할 수 없으니 호스트 이름, 사용자, Wi-Fi, SSH를 모두 넣어요."},
    ]},
    {"title": "E·F. 첫 부팅과 주소 찾기", "items": [
      {"type": "text", "html": P[5]},
      {"type": "steps", "items": [
        {"t": "켜기", "d": "microSD를 라즈베리파이에 넣고 27W 전원을 연결해요. 초록 LED가 깜빡이면 부팅 중이에요."},
        {"t": "기다리기", "d": "첫 부팅은 몇 분 걸려요. 3분쯤 기다려요."},
        {"t": "응답 확인", "d": "PC의 명령 창(Windows는 PowerShell, macOS는 터미널)에서 아래 명령으로 응답을 확인해요."},
      ]},
      {"type": "code", "label": "PC에서 (bird-3은 우리 모둠 호스트 이름으로)", "lang": "bash", "code": "ping bird-3.local"},
      {"type": "step_head", "html": "예상 화면 (Windows는 4번, macOS는 멈출 때까지 반복돼요. macOS는 Ctrl+C로 멈춰요)"},
      _out("Reply from 192.168.0.23: bytes=32 time=6ms TTL=64\n(macOS) 64 bytes from 192.168.0.23: icmp_seq=0 ttl=64 time=6.1 ms"),
      {"type": "callout", "kind": "tip", "title": "응답이 없으면", "html": "공유기 관리 페이지(보통 공유기 아래 라벨에 주소가 있어요)의 연결 기기 목록에서 <code>bird-3</code>을 찾거나, 휴대폰 네트워크 검색 앱(예: Fing)에서 제조사가 Raspberry Pi인 기기를 찾아 IP 주소를 적어요. 그다음부터는 <code>bird-3.local</code> 대신 그 IP 주소를 써요."},
    ]},
    {"title": "G. PC에서 SSH로 접속하기", "items": [
      {"type": "text", "html": P[6]},
      {"type": "code", "label": "PC에서 (사용자이름과 bird-3을 바꿔서)", "lang": "bash", "code": "ssh 사용자이름@bird-3.local"},
      {"type": "step_head", "html": "처음 접속할 때"},
      _out("The authenticity of host 'bird-3.local (192.168.0.23)' can't be established.\nED25519 key fingerprint is SHA256:…\nAre you sure you want to continue connecting (yes/no/[fingerprint])? yes\n사용자이름@bird-3.local's password:        ← 입력해도 보이지 않아요\n사용자이름@bird-3:~ $"),
      {"type": "callout", "kind": "tip", "title": "Windows에서 ssh를 찾을 수 없다고 나오면", "html": "PowerShell에서 <code>ssh -V</code>를 입력해 버전이 나오는지 봐요. 안 나오면 <b>설정 → 시스템 → 선택적 기능 → 기능 추가</b>에서 <b>OpenSSH 클라이언트</b>를 설치하고 PowerShell을 다시 열어요."},
    ]},
    {"title": "H. 업데이트", "items": [
      {"type": "text", "html": P[7]},
      {"type": "code", "label": "라즈베리파이 SSH 창에서 (한 줄씩)", "lang": "bash", "code": "sudo apt update\nsudo apt full-upgrade -y\nsudo reboot"},
      {"type": "callout", "kind": "info", "title": "다시 접속하기", "html": "<code>sudo reboot</code>를 하면 SSH 연결이 끊겨요. 1분쯤 뒤 G 단계의 <code>ssh</code> 명령으로 다시 접속해요."},
    ]},
    {"title": "I. 작업 폴더와 가상환경", "items": [
      {"type": "text", "html": P[8]},
      {"type": "code", "label": "라즈베리파이 SSH 창에서 (한 줄씩)", "lang": "bash", "code": "mkdir -p ~/bird\ncd ~/bird\npython3 -m venv venv\nsource venv/bin/activate"},
      {"type": "step_head", "html": "예상 화면"},
      _out("(venv) 사용자이름@bird-3:~/bird $"),
      {"type": "callout", "kind": "key", "title": "새로 접속할 때마다", "html": "SSH로 다시 접속하면 <code>cd ~/bird</code>와 <code>source venv/bin/activate</code>를 먼저 입력해요. 줄 앞에 <code>(venv)</code>가 없으면 설치한 패키지를 찾지 못해요."},
    ]},
    {"title": "J. BirdNET과 Flask 설치", "items": [
      {"type": "text", "html": P[9]},
      {"type": "code", "label": "(venv)가 보이는 상태에서", "lang": "bash", "code": "pip install \"birdnet==1.1.1\" flask\npython -c \"import birdnet, flask; print('설치 완료')\""},
      {"type": "step_head", "html": "예상 화면 (마지막 줄)"},
      _out("설치 완료"),
    ]},
    {"title": "K. 서버 받고 첫 실행", "items": [
      {"type": "text", "html": P[10]},
      {"type": "code", "label": "(venv)가 보이는 상태에서, ~/bird 폴더에서", "lang": "bash", "code": f"wget -O bird_server.py.new {SITE}/snippets/bird_server.py && mv bird_server.py.new bird_server.py\npython bird_server.py"},
      {"type": "step_head", "html": "예상 화면"},
      _out("판정할 새 7종: 물까치, 까치, 직박구리, 참새, 멧비둘기, 박새, 큰부리까마귀\n브라우저에서 여세요 →  http://192.168.0.23:8000   (피코 코드의 SERVER에도 이 주소)\n * Running on http://192.168.0.23:8000"),
      {"type": "callout", "kind": "tip", "title": "확인", "html": "PC 브라우저에서 <code>http://192.168.0.23:8000</code>(화면에 나온 주소)을 열어 '새소리 판정 서버' 페이지가 보이면 성공이에요. 서버를 멈출 때는 SSH 창에서 <b>Ctrl+C</b>를 눌러요."},
    ]},
    {"title": "L. 전원만 켜면 서버가 시작되게 (자동 실행)", "items": [
      {"type": "text", "html": P[11]},
      {"type": "steps", "items": [
        {"t": "손으로 켠 서버 끄기", "d": "K 단계의 서버가 돌고 있으면 <b>Ctrl+C</b>로 멈춰요."},
        {"t": "서비스 파일 만들기", "d": "아래 명령을 <b>통째로</b> 붙여 넣어요. <code>$USER</code>와 <code>$HOME</code>은 내 사용자 이름과 폴더로 저절로 바뀌어요."},
        {"t": "등록하고 시작", "d": "그다음 명령 세 줄을 한 줄씩 입력해요. 상태에 <b>active (running)</b>이 보이면 <code>journalctl -u bird -f</code>로 '브라우저에서 여세요' 줄이 나올 때까지 기다린 뒤 Ctrl+C로 나와요. PC 브라우저에서 그 주소가 열리면 성공이에요."},
      ]},
      {"type": "code", "label": "① 서비스 파일 만들기 (통째로 붙여 넣기)", "lang": "bash", "code": _SERVICE},
      {"type": "code", "label": "② 등록·시작·확인 (한 줄씩)", "lang": "bash", "code": "sudo systemctl daemon-reload\nsudo systemctl enable --now bird\nsystemctl status bird --no-pager"},
      {"type": "step_head", "html": "예상 화면 (일부)"},
      _out("● bird.service - BirdNET bird sound server\n     Loaded: loaded (/etc/systemd/system/bird.service; enabled; preset: enabled)\n     Active: active (running) since …"),
      {"type": "code", "label": "자주 쓰는 명령", "lang": "bash", "code": "journalctl -u bird -f          # 서버가 쓰는 글 보기 (Ctrl+C로 나와도 서버는 계속 돌아요)\nsudo systemctl restart bird    # bird_server.py를 고친 뒤 다시 시작\nsudo systemctl stop bird       # 멈추기\nsudo systemctl disable bird    # 자동 실행 없애기"},
      {"type": "callout", "kind": "warn", "title": "active (running)이 아니면", "html": "<code>cat /etc/systemd/system/bird.service</code>로 파일을 열어 <code>User=</code>와 경로에 내 사용자 이름이 들어갔는지 봐요. <code>journalctl -u bird -n 30</code>으로 오류 메시지를 확인해요."},
    ]},
    {"title": "M. 주소 고정과 AP 격리", "items": [
      {"type": "text", "html": P[12]},
      {"type": "code", "label": "라즈베리파이에서: 내 IP와 Wi-Fi MAC 주소 보기", "lang": "bash", "code": "hostname -I\nnmcli device show wlan0 | grep -E 'HWADDR|IP4.ADDRESS'"},
      {"type": "steps", "items": [
        {"t": "주소 예약", "d": "공유기 관리 페이지의 DHCP 설정에서 '주소 예약', '고정 할당' 같은 메뉴를 찾아, 위의 MAC 주소(HWADDR)에 지금 IP를 등록해요. 메뉴 이름은 공유기마다 달라요."},
        {"t": "AP 격리 확인", "d": "PC에서 <code>ping 라즈베리파이IP</code>를 했을 때 응답이 없는데 공유기 목록에는 보이면, 공유기의 AP 격리(무선 격리)를 꺼 달라고 관리자에게 요청하거나 수업용 공유기를 따로 써요."},
      ]},
    ]},
    {"title": "N. 온도·전원 확인과 안전하게 끄기", "items": [
      {"type": "text", "html": P[13]},
      {"type": "code", "label": "라즈베리파이에서", "lang": "bash", "code": "vcgencmd measure_temp\nvcgencmd get_throttled\nsudo poweroff"},
      _out("temp=48.3'C\nthrottled=0x0          ← 0x0이면 전원 부족·과열 기록이 없어요"),
      {"type": "callout", "kind": "info", "title": "다시 켜기", "html": "LED가 빨간색이 된 뒤 전원을 뽑아요. 전원을 다시 꽂으면 켜지고, 전원이 꽂힌 채 꺼져 있을 때는 보드의 전원 버튼을 눌러 켜요. 자동 실행(L)을 설정했다면 서버도 저절로 시작돼요."},
    ]},
    {"title": "O·P. 이럴 때는", "items": [
      {"type": "text", "html": P[14]},
      {"type": "code", "label": "PC에서: 운영체제를 다시 구운 뒤 접속 경고가 나올 때", "lang": "bash", "code": "ssh-keygen -R bird-3.local"},
      {"type": "mistakes", "items": [
        {"sym": "ping bird-3.local에 응답이 없어요", "cause": "첫 부팅 중, Wi-Fi 이름·비밀번호 오타, 지역 설정 잘못, AP 격리", "fix": "3분 더 기다린 뒤 다시 해요. 공유기 목록에도 없으면 D 단계부터 다시 구워요. 목록에는 있는데 응답이 없으면 M 단계의 AP 격리를 봐요."},
        {"sym": "Permission denied (password)", "cause": "사용자 이름이나 비밀번호가 D 단계와 다름", "fix": "적어 둔 사용자 이름을 확인하고, 비밀번호는 보이지 않아도 그대로 입력해요."},
        {"sym": "WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED", "cause": "microSD를 다시 구워 라즈베리파이의 신분 정보가 바뀜", "fix": "PC에서 <code>ssh-keygen -R bird-3.local</code>을 실행하고 다시 접속해요."},
        {"sym": "error: externally-managed-environment", "cause": "가상환경을 켜지 않고 pip를 실행함", "fix": "<code>cd ~/bird</code>, <code>source venv/bin/activate</code> 뒤 다시 설치해요."},
        {"sym": "Address already in use", "cause": "자동 실행 서버가 이미 8000번을 쓰는데 손으로 또 켬", "fix": "손으로 켤 필요가 없어요. 고친 뒤에는 <code>sudo systemctl restart bird</code>를 써요."},
        {"sym": "번개 표시·느려짐, throttled가 0x0이 아님", "cause": "전원 부족이나 과열", "fix": "공식 27W 어댑터와 팬 케이스를 쓰고, 팬 선이 꽂혔는지 봐요."},
      ]},
    ]},
  ],
}
