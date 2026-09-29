# -*- coding: utf-8 -*-
# ML3장·부록 공통: 라즈베리파이 5 준비물 (모둠당 1세트). 2026-09-29 디바이스마트 조회(GPT-6-sol 11번 조회)
DM = "https://www.devicemart.co.kr/goods/view?no="

def _row(name, role, qty, no=None, note=""):
    link = f'<a href="{DM}{no}" target="_blank" rel="noopener">디바이스마트</a>' if no else ""
    return f"<tr><td>{name}</td><td>{role}</td><td style='text-align:center'>{qty}</td><td>{link}</td><td>{note}</td></tr>"

PI_BUY = ("<div style='overflow-x:auto'><table class='plan-table'>"
          "<tr><th>부품</th><th>역할</th><th>수량</th><th>구입</th><th>비고</th></tr>"
          + _row("라즈베리파이 5 (8GB) + 가이드북", "BirdNET 서버", 1, "15215449", note="4GB(15215450)는 조회 당시 재고 확보 중")
          + _row("공식 라즈베리파이 27W USB-C 어댑터", "전원 5.1V 5A", 1, "15502416", note="KC 인증. 다른 충전기는 전원 부족 경고가 나요")
          + _row("라즈베리파이 5 공식 케이스 (팬 포함)", "보호·냉각", 1, "15276234", note="팬 대신 Active Cooler(15276241)를 쓸 수도 있지만 둘을 함께 달지는 않아요")
          + _row("SanDisk Extreme microSDXC 64GB (SDSQXAH-064G-GN6MN)", "운영체제 카드", 1, "14825254", note="A2 규격. 공식 A2 64GB(15549242)는 조회 당시 품절")
          + _row("USB 3.0 카드 리더 (넥시 NX-U30CR)", "PC에서 Pi 카드 굽기", "모둠당 1", "15227464", note="ML2장의 카드 리더가 있으면 그대로 사용")
          + "<tr><td colspan='5' style='background:var(--card);font-weight:700'>이미 있는 것</td></tr>"
          + _row("ML2장 물까치 관측기 한 벌", "피코 1차 판정·녹음", 1, note="Wi-Fi 연결을 위해 wifi_config.py 필요(본 교재 1장)")
          + _row("PC(Windows 10/11 또는 macOS)", "Imager·SSH·브라우저", 1, note="Pi와 같은 공유기에 연결")
          + _row("교실 공유기(Wi-Fi)", "피코·Pi·PC를 한 네트워크로", "학급 1", note="'AP 격리'가 꺼져 있어야 해요(부록 참고)")
          + "</table></div>")
