# -*- coding: utf-8 -*-
# 소리·말하기 장 마이크 점퍼 그림. Grove Shield for Pi Pico v1.0 윗줄 헤더를 보드 인쇄 그대로 그린다
# 윗줄 헤더 인쇄(왼쪽→오른쪽) = 피코 40번 → 21번. 피코는 안쪽 줄에 꽂히고, 점퍼는 인쇄 글자 바로 아래 바깥쪽 줄에 꽂는다
PCB, PCB_T, INK, SOFT, WARN = "#1c5f43", "#e3f3ea", "#16201c", "#5a6762", "#ffb3b3"
LABELS = ["5V", "VSYS", "GND", "3V3 EN", "3V3", "ADC VREF", "GP28", "GND", "GP27", "GP26",
          "RUN", "GP22", "GND", "GP21", "GP20", "GP19", "GP18", "GND", "GP17", "GP16"]
# 칸 번호: (마이크 핀, 점퍼 색 이름, 색, 글자색) — 색은 본문 단계 목록(주·노·초·파·보·회)과 같다
PLUGS = {4: ("VDD", "회", "#8a8f8c", "#fff"), 12: ("L/R", "보", "#8a4fd0", "#fff"), 14: ("SD", "파", "#2f6fd6", "#fff"),
         15: ("WS", "초", "#2f9e4f", "#fff"), 16: ("SCK", "노", "#e2b200", INK), 17: ("GND", "주", "#e8792a", "#fff")}


def _t(x, y, s, size=12, color=INK, anchor="middle", weight="400", extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}" {extra}>{s}</text>'


def _cx(i):
    return 82 + 44 * i


def _board():
    o = f'<rect x="20" y="36" width="960" height="314" rx="14" fill="{PCB}"/>'
    # 피코 핀 번호 (보드에는 인쇄돼 있지 않음)
    o += "".join(_t(_cx(i), 60, 40 - i, 11, "#9cc5ae") for i in range(20))
    # 인쇄 글자 (세로)
    for i, s in enumerate(LABELS):
        hot = i in PLUGS
        bad = i in (0, 3)
        col = "#fff" if hot else (WARN if bad else PCB_T)
        o += _t(_cx(i) + 5, 146, s, 14, col, "start", "700" if hot or bad else "400", f'transform="rotate(-90 {_cx(i) + 5} 146)"')
    # 헤더 두 줄
    o += '<rect x="58" y="154" width="884" height="66" rx="3" fill="#111"/>'
    o += "".join(f'<rect x="{_cx(i) - 11}" y="{160 + j * 30}" width="22" height="22" fill="#2e2e2e"/>' for i in range(20) for j in range(2))
    # 피코 (안쪽 줄을 덮음)
    o += '<rect x="44" y="188" width="912" height="150" rx="8" fill="#2d7a45" stroke="#e3f3ea" stroke-opacity=".5"/>'
    o += "".join(f'<circle cx="{_cx(i)}" cy="196" r="4" fill="#d9b44a"/>' for i in range(20))
    o += '<rect x="24" y="242" width="30" height="46" rx="4" fill="#c9ccd1" stroke="#666"/>' + _t(39, 269, "USB", 9, "#333", weight="700")
    o += _t(300, 262, "Raspberry Pi Pico 2 WH", 16, PCB_T, weight="700")
    o += _t(300, 286, "피코는 안쪽 줄에 꽂혀 있어요", 13, PCB_T)
    o += _t(300, 308, "점퍼는 인쇄 글자 바로 아래 바깥쪽 줄에 꽂아요", 13, "#fff", weight="700")
    # 꽂지 않는 칸
    for i in (0, 3):
        x, y = _cx(i), 171
        o += f'<path d="M{x - 7},{y - 7} L{x + 7},{y + 7} M{x + 7},{y - 7} L{x - 7},{y + 7}" stroke="#ff6b6b" stroke-width="3" stroke-linecap="round"/>'
    o += _t(_cx(13), 176, "비움", 11, "#b9c4bf")
    # 점퍼 끝
    for i, (pin, cname, fill, ink) in PLUGS.items():
        x = _cx(i)
        o += f'<rect x="{x - 17}" y="150" width="34" height="44" rx="5" fill="{fill}" stroke="#111" stroke-width="1.2"/>'
        o += _t(x, 170, pin, 12, ink, weight="700") + _t(x, 187, cname, 11, ink)
    # 안내
    o += _t(66, 234, "✕ 5V · 3V3 EN에는 꽂지 않아요", 13, WARN, "start", "700")
    o += _t(944, 326, "맨 위 숫자는 피코 핀 번호예요. 보드에는 인쇄돼 있지 않아요", 12, "#9cc5ae", "end")
    return o


def _mic():
    o = _t(560, 380, "마이크 쪽 핀", 14, INK, "end", "700")
    o += _t(560, 400, "같은 색 점퍼의 반대쪽 끝을 꽂아요", 12, SOFT, "end")
    o += _t(560, 418, "흔한 핀 배열 예 · 모듈 인쇄를 보고 꽂아요", 12, SOFT, "end")
    o += '<rect x="580" y="362" width="270" height="72" rx="14" fill="#6b3fa0"/>'
    rows = (("SCK", "WS", "L/R"), ("SD", "VDD", "GND"))
    byname = {v[0]: v for v in PLUGS.values()}
    for r, names in enumerate(rows):
        for c, n in enumerate(names):
            x, y = 604 + c * 84, 382 + r * 32
            _, cname, fill, ink = byname[n]
            o += f'<rect x="{x}" y="{y - 9}" width="26" height="18" rx="3" fill="{fill}" stroke="#111"/>' + _t(x + 13, y + 4, cname, 10, ink, weight="700")
            o += _t(x + 32, y + 5, n, 13, "#fff", "start", "700")
    return o


FIG_HDR = (
    '<svg viewBox="0 26 1000 420" width="100%" style="display:block;min-width:760px;height:auto;background:#fff;border:1px solid #e6e8f5;border-radius:14px" role="img" '
    'aria-label="쉴드 윗줄 헤더와 마이크 점퍼. 피코 USB를 왼쪽에 두면 윗줄 헤더에는 왼쪽부터 5V, VSYS, GND, 3V3 EN, 3V3, ADC VREF, GP28, GND, GP27, GP26, RUN, GP22, GND, GP21, GP20, GP19, GP18, GND, GP17, GP16이 인쇄돼 있다. '
    '피코는 안쪽 줄에 꽂히고 점퍼는 글자 바로 아래 바깥쪽 줄에 꽂는다. 마이크 VDD는 왼쪽에서 다섯째 칸 3V3, L/R은 GP21 왼쪽 GND, SD는 GP20, WS는 GP19, SCK는 GP18, GND는 GP18 오른쪽 GND에 꽂는다. GP21은 비우고, 5V와 3V3 EN에는 꽂지 않는다.">'
    + _board() + _mic() + '</svg>')
