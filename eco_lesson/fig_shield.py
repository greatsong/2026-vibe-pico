# -*- coding: utf-8 -*-
# 마이크 연결 그림 (ML2 그림 3). Seeed Grove Shield for Pi Pico v1.0 실물 배치 기준
# 위쪽 줄: 전원 스위치 · I2C0 · I2C1 · A0 · A1 · A2 / 아래쪽 줄: SPI0 · UART0 · UART1 · D16 · D18 · D20 / 피코 USB는 왼쪽
# Grove 커넥터는 세로로 서 있고 인쇄는 위에서부터 GND · VCC(3V3) · 둘째 신호 · 첫째 신호 → 선 색은 검정 · 빨강 · 흰색 · 노랑
ACC = "#b91c4a"
COL = {"노랑": "#e2b200", "흰색": "#fbfbf6", "빨강": "#d33a2f", "검정": "#1b1b1b"}
INK, SOFT, PCB, PCB_T = "#16201c", "#5a6762", "#1c5f43", "#e3f3ea"


def _t(x, y, s, size=12, color=INK, anchor="middle", weight="400"):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{s}</text>'


def _wire(d, color):
    under = '<path d="%s" fill="none" stroke="#8a8f8c" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>' % d if color == "흰색" else ""
    return under + f'<path d="{d}" fill="none" stroke="{COL[color]}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>'


def _ell(x0, y0, x1, y1, r=10):
    """가로로 가다가 세로로 꺾이는 선 (모서리 둥글게)"""
    sx = 1 if x1 > x0 else -1
    sy = 1 if y1 > y0 else -1
    return f"M{x0},{y0} H{x1 - sx * r} Q{x1},{y0} {x1},{y0 + sy * r} V{y1}"


def _cap(x, y, color):
    """꽂지 않고 둔 선 끝: 암 점퍼 하우징 (금속은 플라스틱 안에 있다)"""
    return f'<rect x="{x}" y="{y - 7}" width="22" height="14" rx="2" fill="#222"/><rect x="{x + 1}" y="{y - 2}" width="4" height="4" fill="#555"/>'


def _housing(x, y, h=112, colors=None, hl=False):
    """세로로 선 Grove 커넥터. colors가 있으면 핀마다 꽂힌 선 색을 점으로"""
    out = f'<rect x="{x}" y="{y}" width="32" height="{h}" rx="4" fill="#f4f1e8" stroke="{ACC if hl else "#b9b3a0"}" stroke-width="{3 if hl else 1.2}"/>'
    step = h / 4
    for i in range(4):
        cy = y + step * (i + .5)
        fill = COL[colors[i]] if colors else "#c9b27a"
        out += f'<circle cx="{x + 16}" cy="{cy}" r="{7 if colors else 3}" fill="{fill}" stroke="#555" stroke-width="{1 if colors else .6}"/>'
    return out


# ① 쉴드 위에서 본 모습 ------------------------------------------------------------
def _overview():
    o = _t(20, 26, "① 쉴드에서 자리 찾기", 15, INK, "start", "700")
    o += f'<rect x="20" y="50" width="430" height="410" rx="16" fill="{PCB}"/>'
    # 전원 스위치
    o += '<rect x="32" y="84" width="24" height="52" rx="4" fill="#d97706"/><rect x="37" y="90" width="14" height="16" rx="2" fill="#fff"/>'
    o += _t(44, 150, "5V", 10, PCB_T, weight="700")
    # 위쪽 줄 포트
    for cx, n in zip((110, 180, 250, 320, 390), ("I2C0", "I2C1", "A0", "A1", "A2")):
        o += _t(cx, 74, n, 12, PCB_T, weight="700") + _housing(cx - 16, 82, 56, hl=(n == "A2"))
    # 윗줄 헤더 (바깥 줄 + 안쪽 줄)
    o += '<rect x="40" y="158" width="392" height="30" rx="3" fill="#111"/>'
    o += "".join(f'<rect x="{45 + i * 19.4}" y="{162 + j * 13}" width="10" height="9" fill="#333"/>' for i in range(20) for j in range(2))
    # 아래 헤더
    o += '<rect x="40" y="314" width="392" height="30" rx="3" fill="#111"/>'
    o += "".join(f'<rect x="{45 + i * 19.4}" y="{318 + j * 13}" width="10" height="9" fill="#333"/>' for i in range(20) for j in range(2))
    # 피코 (안쪽 두 줄에 꽂힘)
    o += '<rect x="40" y="172" width="392" height="158" rx="8" fill="#2d7a45" stroke="#e3f3ea" stroke-opacity=".5"/>'
    o += '<rect x="24" y="232" width="30" height="38" rx="4" fill="#c9ccd1" stroke="#666"/>' + _t(39, 256, "USB", 9, "#333", weight="700")
    o += _t(245, 246, "Raspberry Pi Pico 2 WH", 15, PCB_T, weight="700") + _t(245, 268, "USB 단자가 왼쪽에 오게 놓아요", 12, PCB_T)
    # SPI0 헤더와 아래쪽 줄 포트
    o += '<rect x="30" y="362" width="44" height="30" rx="3" fill="#111"/>'
    o += "".join(f'<circle cx="{39 + i * 13}" cy="{370 + j * 14}" r="3.4" fill="#d9b44a"/>' for i in range(3) for j in range(2))
    o += _t(52, 410, "SPI0", 11, PCB_T, weight="700")
    for cx, n in zip((110, 180, 250, 320, 390), ("UART0", "UART1", "D16", "D18", "D20")):
        o += _housing(cx - 16, 360, 56, hl=(n == "D20")) + _t(cx, 434, n, 12, PCB_T, weight="700")
    # 케이블 표시
    o += f'<rect x="340" y="30" width="100" height="22" rx="11" fill="{ACC}"/>' + _t(390, 46, "케이블 B", 12, "#fff", weight="700")
    o += f'<rect x="340" y="468" width="100" height="22" rx="11" fill="{ACC}"/>' + _t(390, 484, "케이블 A", 12, "#fff", weight="700")
    o += _t(235, 518, "A2는 위쪽 줄 맨 오른쪽, D20은 아래쪽 줄 맨 오른쪽이에요.", 13, INK)
    o += _t(235, 540, "Grove 커넥터는 한 방향으로만 들어가요. 딸깍 소리가 날 때까지 밀어 넣어요.", 12, SOFT)
    return o


# ② 선을 마이크 핀에 ------------------------------------------------------------
def _pin(x, y, name, from_top):
    """마이크 핀에 꽂힌 암 점퍼 끝(검은 하우징)과 핀 이름"""
    hy = y - 14 if from_top else y - 10
    out = f'<rect x="{x - 8}" y="{hy}" width="16" height="24" rx="2" fill="#222"/>'
    out += f'<circle cx="{x}" cy="{y}" r="3" fill="#e8c35a"/>'
    ly = y + 28 if from_top else y - 22
    out += _t(x, ly, name, 13, "#fff", weight="700")
    return out


def _detail():
    o = f'<line x1="468" y1="20" x2="468" y2="580" stroke="#d4dcd8" stroke-dasharray="5 5"/>'
    o += _t(488, 26, "② 선을 마이크 핀에 꽂기", 15, INK, "start", "700")
    # 마이크 모듈 (흔한 배열을 180° 돌려 놓은 방향)
    o += '<circle cx="800" cy="300" r="100" fill="#6b3fa0"/>'
    o += _t(690, 292, "INMP441 마이크", 13, INK, "end", "700")
    o += _t(690, 312, "흔한 핀 배열로 그렸어요", 12, SOFT, "end")
    o += _t(690, 330, "모듈 인쇄를 보고 꽂아요", 12, SOFT, "end")
    # 케이블 B: A2 커넥터 확대 (오른쪽 위)
    o += _t(896, 50, "A2 포트 · 케이블 B", 12, ACC, weight="700")
    o += _housing(880, 60, 112, ["검정", "빨강", "흰색", "노랑"], hl=True)
    for i, s in enumerate(("GND", "3V3 (고정)", "A1 · GP27", "A2 · GP28")):
        o += _t(918, 79 + i * 28, s, 12, INK, "start")
    o += _wire(_ell(880, 74, 750, 250), "검정")
    o += _wire(_ell(880, 102, 800, 250), "빨강")
    o += _wire(_ell(880, 158, 850, 250), "노랑")
    o += _wire("M880,130 H866", "흰색") + _cap(844, 130, "흰색") + _t(855, 117, "꽂지 않음", 10, ACC, weight="700")
    o += _pin(750, 262, "GND", True) + _pin(800, 262, "VDD", True) + _pin(850, 262, "SD", True)
    # 케이블 A: D20 커넥터 확대 (왼쪽 아래)
    o += _t(576, 570, "D20 포트 · 케이블 A", 12, ACC, weight="700")
    o += _housing(560, 428, 112, ["검정", "빨강", "흰색", "노랑"], hl=True)
    for i, s in enumerate(("GND", "VCC", "D21 · GP21", "D20 · GP20")):
        o += _t(554, 447 + i * 28, s, 12, INK, "end")
    o += _wire(_ell(592, 442, 750, 350), "검정")
    o += _wire(_ell(592, 498, 800, 350), "흰색")
    o += _wire(_ell(592, 526, 850, 350), "노랑")
    o += _wire("M592,470 H606", "빨강") + _cap(606, 470, "빨강") + _t(634, 475, "빨강은 꽂지 않음 (5V가 흐를 수 있어요)", 12, ACC, "start", "700")
    o += _pin(750, 338, "L/R", False) + _pin(800, 338, "WS", False) + _pin(850, 338, "SCK", False)
    # 한 줄 요약
    o += _t(912, 262, "← 케이블 B", 11, SOFT, "start") + _t(912, 342, "← 케이블 A", 11, SOFT, "start")
    return o


FIG_MIC = (
    '<svg viewBox="0 0 1000 590" role="img" aria-label="그림 3. 마이크 연결. 피코의 USB가 왼쪽에 오게 놓으면 A2는 위쪽 줄 맨 오른쪽, D20은 아래쪽 줄 맨 오른쪽 포트다. '
    'A2에 꽂는 케이블 B는 검정을 GND, 빨강(3.3V 고정)을 VDD, 노랑(GP28)을 SD에 꽂고 흰색은 어디에도 꽂지 않는다. '
    'D20에 꽂는 케이블 A는 검정을 L/R, 흰색(GP21)을 WS, 노랑(GP20)을 SCK에 꽂고 빨강(5V가 흐를 수 있음)은 어디에도 꽂지 않는다. 마이크의 한 줄은 케이블 B, 다른 한 줄은 케이블 A가 맡는다.">'
    + _overview() + _detail() + '</svg>')
