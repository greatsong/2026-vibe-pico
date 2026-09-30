# -*- coding: utf-8 -*-
# ML3장 그림: 피코·공유기·라즈베리파이·PC 사이에 무엇이 오가는지 (ML2의 FIG_STYLE .ecofig 클래스 재사용)

_ARROW = ('<defs><marker id="pa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
          '<path d="M0,0 L10,5 L0,10 z" fill="#16201c"/></marker>'
          '<marker id="pb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
          '<path d="M0,0 L10,5 L0,10 z" fill="#b91c4a"/></marker></defs>')

FIG_NET = ('<svg viewBox="0 0 1000 470" role="img" aria-label="그림 1. 실시간 판정과 2차 판정의 흐름. 피코는 3초 WAV를 교실 공유기를 거쳐 라즈베리파이 5의 bird_server.py에 보내고, '
           '판정 · 가장 높은 새 · 신뢰도 세 칸의 답을 받아 MP3로 말한다. PC 브라우저는 같은 주소의 판정 페이지에서 WAV를 올리고 결과 표를 본다. 피코의 녹음용 microSD는 카드 리더로 PC에 옮긴다.">'
           + _ARROW +
           # 피코 관측기
           '<rect class="mod" x="20" y="60" width="230" height="150" rx="12"/>'
           '<text class="tb" x="135" y="90" text-anchor="middle">피코 관측기 (ML2)</text>'
           '<text class="ts" x="135" y="114" text-anchor="middle">마이크 · microSD · MP3 · LED</text>'
           '<text class="t" x="135" y="142" text-anchor="middle">3초 듣기 → k-NN 표 세기</text>'
           '<text class="tm" x="135" y="168" text-anchor="middle">eco_5_server.py</text>'
           '<text class="ts" x="135" y="192" text-anchor="middle">LED 보라 = Pi에게 묻는 중</text>'
           # 공유기
           '<rect class="mod" x="385" y="80" width="200" height="110" rx="12"/>'
           '<text class="tb" x="485" y="112" text-anchor="middle">교실 공유기 (Wi-Fi)</text>'
           '<text class="ts" x="485" y="136" text-anchor="middle">세 기기가 같은 네트워크</text>'
           '<text class="ts" x="485" y="158" text-anchor="middle">AP 격리는 꺼 둬요</text>'
           # 라즈베리파이
           '<rect x="720" y="50" width="260" height="170" rx="12" fill="#fdecef" stroke="#b91c4a" stroke-width="1.6"/>'
           '<text class="tb" x="850" y="82" text-anchor="middle">라즈베리파이 5</text>'
           '<text class="tm" x="850" y="108" text-anchor="middle">bird_server.py</text>'
           '<text class="t" x="850" y="136" text-anchor="middle">BirdNET · 7종 목록</text>'
           '<text class="ts" x="850" y="160" text-anchor="middle">judged.csv · received/</text>'
           '<text class="tm" x="850" y="186" text-anchor="middle">http://Pi주소:8000</text>'
           '<text class="ts" x="850" y="208" text-anchor="middle">모니터 없이 PC에서 SSH</text>'
           # 피코 ↔ 공유기 ↔ Pi (실시간)
           '<line x1="252" y1="112" x2="382" y2="112" stroke="#16201c" stroke-width="2.2" marker-end="url(#pa)"/>'
           '<line x1="588" y1="112" x2="717" y2="112" stroke="#16201c" stroke-width="2.2" marker-end="url(#pa)"/>'
           '<text class="t" x="317" y="100" text-anchor="middle">① 3초 WAV</text>'
           '<text class="ts" x="652" y="100" text-anchor="middle">POST /judge</text>'
           '<line x1="717" y1="160" x2="588" y2="160" stroke="#b91c4a" stroke-width="2.2" marker-end="url(#pb)"/>'
           '<line x1="382" y1="160" x2="252" y2="160" stroke="#b91c4a" stroke-width="2.2" marker-end="url(#pb)"/>'
           '<text class="t" x="317" y="182" text-anchor="middle" fill="#b91c4a">② 답 세 칸</text>'
           '<text class="tm" x="652" y="182" text-anchor="middle">물까치 물까치 0.83</text>'
           # PC
           '<rect class="mod" x="385" y="300" width="200" height="120" rx="12"/>'
           '<text class="tb" x="485" y="330" text-anchor="middle">PC (브라우저 · SSH)</text>'
           '<text class="ts" x="485" y="354" text-anchor="middle">판정 페이지 열기</text>'
           '<text class="ts" x="485" y="376" text-anchor="middle">WAV 올리기 · 표 · 듣기</text>'
           '<text class="ts" x="485" y="398" text-anchor="middle">judged.csv 내려받기</text>'
           '<line x1="485" y1="297" x2="485" y2="193" stroke="#16201c" stroke-width="2.2" marker-start="url(#pa)" marker-end="url(#pa)"/>'
           '<text class="ts" x="495" y="250">③ 2차 판정·결과 보기</text>'
           # SD 카드 경로
           '<path d="M135,212 L135,360 L382,360" class="c-jump"/>'
           '<text class="t" x="145" y="300">녹음용 microSD</text>'
           '<text class="ts" x="145" y="320">카드 리더로 PC에 옮기기</text>'
           '<text class="ts" x="145" y="340">(2차 판정할 WAV)</text>'
           # 범례
           '<line x1="620" y1="330" x2="660" y2="330" stroke="#16201c" stroke-width="2.2" marker-end="url(#pa)"/><text class="ts" x="668" y="334">보내는 것</text>'
           '<line x1="620" y1="360" x2="660" y2="360" stroke="#b91c4a" stroke-width="2.2" marker-end="url(#pb)"/><text class="ts" x="668" y="364">돌려받는 것</text>'
           '<line x1="620" y1="390" x2="660" y2="390" class="c-jump"/><text class="ts" x="668" y="394">손으로 옮기는 카드</text>'
           '</svg>')

# 부록 G: SSH 명령 풀어 보기
_K = '#b91c4a'
def _chip(x, w, txt, mono=True, fill='#fff7f9'):
    cls = 'tm' if mono else 't'
    return (f'<rect x="{x}" y="40" width="{w}" height="46" rx="8" fill="{fill}" stroke="{_K}" stroke-width="1.4"/>'
            f'<text class="{cls}" x="{x + w / 2}" y="69" text-anchor="middle" style="font-size:18px">{txt}</text>')
def _note(x, y, lines):
    return "".join(f'<text class="ts" x="{x}" y="{y + 18 * i}" text-anchor="middle">{t}</text>' for i, t in enumerate(lines))
def _tick(x):
    return f'<line x1="{x}" y1="88" x2="{x}" y2="112" stroke="{_K}" stroke-width="1.4"/>'

FIG_SSH_CMD = ('<svg viewBox="0 0 1000 250" role="img" aria-label="그림. SSH 접속 명령 풀어 보기. ssh는 접속 명령, 띄어쓰기 한 칸, student는 D 단계에서 정한 사용자 이름, @는 붙여 쓰는 기호, bird-3은 D 단계에서 정한 호스트 이름, .local은 같은 공유기 안에서 찾으라는 뜻이다. bird-3.local 대신 IP 주소를 써도 된다.">'
               + _chip(40, 90, 'ssh') + _chip(180, 150, 'student') + _chip(340, 50, '@') + _chip(400, 150, 'bird-3') + _chip(560, 120, '.local')
               + '<text class="ts" x="155" y="69" text-anchor="middle">한 칸</text>'
               + _tick(85) + _tick(255) + _tick(365) + _tick(475) + _tick(620)
               + _note(85, 132, ['접속 명령', '(늘 같아요)']) + _note(255, 132, ['사용자 이름', 'D 단계에서 정한 것'])
               + _note(365, 132, ['붙여 써요', '띄어쓰기 없음']) + _note(475, 132, ['호스트 이름', 'D 단계에서 정한 것'])
               + _note(620, 132, ['같은 공유기', '안에서 찾기'])
               + '<rect x="720" y="40" width="250" height="120" rx="10" fill="#f4f1e8" stroke="#b9b3a0"/>'
               + '<text class="tb" x="845" y="66" text-anchor="middle">.local이 안 되면</text>'
               + '<text class="tm" x="845" y="96" text-anchor="middle">ssh student@192.168.0.23</text>'
               + '<text class="ts" x="845" y="122" text-anchor="middle">F 단계에서 찾은 IP 주소를</text>'
               + '<text class="ts" x="845" y="140" text-anchor="middle">호스트 이름 자리에 써요</text>'
               + '<text class="ts" x="40" y="215">예시의 student와 bird-3은 우리 모둠이 정한 사용자 이름과 호스트 이름으로 바꿔요.</text>'
               + '</svg>')

# 부록 G: 프롬프트 읽기 (PC일 때와 라즈베리파이일 때)
def _line(y, parts):
    x = 40; out = []
    for txt, col in parts:
        w = 11.2 * len(txt)
        out.append(f'<text x="{x}" y="{y}" style="font-family:ui-monospace,Menlo,monospace;font-size:18px;fill:{col}">{txt}</text>')
        x += w
    return "".join(out)
FIG_PROMPT = ('<svg viewBox="0 0 1000 330" role="img" aria-label="그림. 프롬프트 읽기. PC의 PowerShell은 PS C:\\Users\\이름> 처럼 보이고, 접속 뒤에는 student@bird-3:~ $ 처럼 바뀐다. student는 사용자 이름, bird-3은 라즈베리파이 이름, 물결표는 내 홈 폴더, 달러 기호는 명령을 기다린다는 뜻이다. 가상환경을 켜면 앞에 (venv)가 붙고 ~/bird는 지금 있는 폴더다.">'
              '<rect x="20" y="20" width="960" height="290" rx="12" fill="#1b2420"/>'
              '<text x="40" y="52" style="font-size:13px;fill:#9fb3aa">접속 전 (PC · Windows PowerShell)</text>'
              + _line(80, [('PS C:\\Users\\hong> ', '#e8e3d3'), ('ssh student@bird-3.local', '#ffd479')]) +
              '<text x="40" y="124" style="font-size:13px;fill:#9fb3aa">접속 뒤 (라즈베리파이)</text>'
              + _line(152, [('student', '#7fd1ff'), ('@', '#e8e3d3'), ('bird-3', '#ff9fb8'), (':', '#e8e3d3'), ('~', '#b7f59a'), (' $ ', '#e8e3d3')]) +
              '<text x="330" y="152" style="font-size:13px;fill:#7fd1ff">student = 사용자 이름</text>'
              '<text x="330" y="172" style="font-size:13px;fill:#ff9fb8">bird-3 = 라즈베리파이 이름 (여기서 명령이 실행돼요)</text>'
              '<text x="330" y="192" style="font-size:13px;fill:#b7f59a">~ = 지금 있는 폴더 (내 홈 폴더)   $ = 명령을 기다려요</text>'
              '<text x="40" y="232" style="font-size:13px;fill:#9fb3aa">가상환경을 켜고 bird 폴더로 옮긴 뒤</text>'
              + _line(262, [('(venv) ', '#ffd479'), ('student', '#7fd1ff'), ('@', '#e8e3d3'), ('bird-3', '#ff9fb8'), (':', '#e8e3d3'), ('~/bird', '#b7f59a'), (' $ ', '#e8e3d3')]) +
              '<text x="470" y="262" style="font-size:13px;fill:#ffd479">(venv) = 가상환경이 켜져 있어요</text>'
              '<text x="470" y="284" style="font-size:13px;fill:#b7f59a">~/bird = 지금 bird 폴더에 있어요</text>'
              '</svg>')
