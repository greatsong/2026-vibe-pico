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
           '<text class="ts" x="135" y="114" text-anchor="middle">마이크 · microSD · MP3 · 버튼</text>'
           '<text class="t" x="135" y="142" text-anchor="middle">3초 듣기 → k-NN 표 세기</text>'
           '<text class="tm" x="135" y="168" text-anchor="middle">eco_4_server.py</text>'
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
