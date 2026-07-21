# -*- coding: utf-8 -*-
"""별도 'ML 확장 사이트' 빌더 — 메인 build_site.py를 '수정 없이' 재사용해
   소리 분류(CHAPTER_SOUND) + MP3 출력(CHAPTER_MP3) + 동작 인식(CHAPTER_IMU)
   세 챕터를 한 사이트로 묶어 ml_site/index.html 로 렌더한다.
   메인 index.html·build_site.py는 전혀 건드리지 않는다.
   챕터가 바뀌면 이 파일만 다시 실행하면 됩니다.
"""
import os, shutil, sys

ROOT = os.path.dirname(os.path.abspath(__file__))

# build_site.py 소스에서 '파일 쓰기' 블록(BUILD_MARKER 이하)만 떼고 실행 → 부작용 없음
src = open(os.path.join(ROOT, "build_site.py"), encoding="utf-8").read()
src = src.split('# === BUILD_MARKER')[0]
ns = {"__file__": os.path.join(ROOT, "build_site.py"), "__name__": "build_site_lib"}
exec(compile(src, os.path.join(ROOT, "build_site.py"), "exec"), ns)
render_item, esc, TEMPLATE = ns["render_item"], ns["esc"], ns["TEMPLATE"]
HERO_HTML = ns["HERO_HTML"]

sys.path.insert(0, os.path.join(ROOT, "sound_lesson"))
sys.path.insert(0, os.path.join(ROOT, "mp3_lesson"))
sys.path.insert(0, os.path.join(ROOT, "imu_lesson"))
from chapter_sound import CHAPTER_SOUND
from chapter_imu import CHAPTER_IMU

# MP3(말하기) 챕터는 SD 카드 준비 전까지 보류 — 소리는 LED로 표현하는 구성.
# 재개하려면: from chapter_mp3 import CHAPTER_MP3 후 CHS 가운데에 끼우면 됩니다.
CHS = [CHAPTER_SOUND, CHAPTER_IMU]  # 소리 → 동작

nav_all, main_all = [], []
for c in CHS:
    nav = [f'<div class="nav-ch"><a href="#{c["id"]}" class="nav-ch-link" data-target="{c["id"]}">'
           f'<span class="nav-dot"></span>'
           f'{esc(c["num"])}. {esc(c["title"])}</a><div class="nav-secs">']
    sec_html = []
    for si, s in enumerate(c["sections"]):
        sid = f'{c["id"]}-{si}'
        nav.append(f'<a href="#{sid}" class="nav-sec" data-target="{sid}">{esc(s["title"])}</a>')
        items_html = "".join(render_item(it, c["accent"]) for it in s["items"])
        sec_html.append(f'<section class="sec" id="{sid}">'
                        f'<h3 class="sec-title">{esc(s["title"])}</h3>{items_html}</section>')
    nav.append('</div></div>')
    nav_all.append("".join(nav))

    goals = "".join(f'<li>{g}</li>' for g in c.get("goals", []))
    intro = ''
    if goals:
        intro += f'<div class="goals"><div class="goals-t">🎯 이 장을 마치면</div><ul>{goals}</ul></div>'
    if c.get("why"):
        intro += f'<div class="why"><div class="why-t">💡 왜 배우나요?</div><p>{c["why"]}</p></div>'
    main_all.append(
        f'<div class="chapter" id="{c["id"]}">'
        f'<div class="ch-head"><span class="ch-num">CHAPTER {c["num"]}</span>'
        f'<h2 class="ch-title"><span class="ch-bar"></span>'
        f'{esc(c["title"])}</h2><p class="ch-sub">{esc(c["subtitle"])}</p></div>'
        f'{intro}{c.get("extra","")}{"".join(sec_html)}</div>')

ncode = sum(1 for c in CHS for s in c["sections"] for it in s["items"] if it.get("type") == "code")
nprompt = sum(1 for c in CHS for s in c["sections"] for it in s["items"] if it.get("type") == "prompt")

# 히어로를 먼저 주입한 뒤 NCH/NCODE/NPROMPT를 치환해야 히어로 안 플레이스홀더까지 채워진다
out = (TEMPLATE.replace("/*NAV*/", "".join(nav_all))
       .replace("/*HERO*/", HERO_HTML)
       .replace("/*MAIN*/", "".join(main_all)))
out = (out.replace("/*NCODE*/", str(ncode)).replace("/*NPROMPT*/", str(nprompt)).replace("/*NCH*/", str(len(CHS))))

# ── ML 확장판 브랜딩 (메인 책 표지/제목을 별도 사이트용으로 교체) ──
BRAND = [
  ("라즈베리파이 피코 2 WH로 배우는 피지컬 컴퓨팅 학습 자료 — 설치부터 와이파이·LED·가스센서·날씨 API 대시보드까지, 복사해서 바로 쓰는 MicroPython 코드 모음.",
   "라즈베리파이 피코 2 WH로 마이크 소리와 IMU 동작 데이터를 모아 k-NN으로 분류하고 LED 빛으로 표현하는 머신러닝 확장판 — 소리 분류·동작 인식까지 복붙 MicroPython 코드 모음."),
  ("<title>데이터로 탐구하는 피코 바이브 피지컬 코딩</title>",
   "<title>소리와 동작을 배우는 피코 · 바이브 피지컬 코딩 ML 확장판</title>"),
  # 드로어 브랜드 (TEMPLATE의 .drawer 안)
  ('<div class="brand"><span class="brand-emoji">🐣🔌</span> 바이브 <span class="pk">피</span>지컬 <span class="pk">코</span>딩<small>데이터 기반 탐구 프로젝트 · <span class="pico-accent">피코</span>로 시작하기</small></div>',
   '<div class="brand"><span class="brand-emoji">🐣🔊</span> 바이브 <span class="pk">피</span>지컬 <span class="pk">코</span>딩<small>머신러닝 확장판 · 소리·동작편</small></div>'),
  # 상단바 브랜드 이모지 (본편 🐣🔌 → 확장판 🐣🔊) — href는 ml_site 자기 자신이라 그대로 둔다
  ('<a class="brand" href="index.html"><span class="brand-emoji">🐣🔌</span>',
   '<a class="brand" href="index.html"><span class="brand-emoji">🐣🔊</span>'),
  # 상단바 모드 링크 자리 → 본편으로 가는 링크
  ('<!--MODELINK-->',
   '<a class="home" href="../">본편 ↗</a>'),
  # 히어로의 확장판 CTA → ml_site 안에서는 '본편으로 돌아가기' 카드로 교체
  ('''<a class="ml-cta" href="ml_site/">
        <span class="ml-cta-emoji">🔊🧠</span>
        <span class="ml-cta-txt"><b>새 확장판 · 소리를 배우고 말하는 피코 (머신러닝)</b>
        <small>마이크로 소리를 모아 k-NN으로 분류하고, LED·MP3 음성으로 말하게 만들어요. 이 책을 끝낸 다음 단계예요.</small></span>
        <span class="ml-cta-go">확장판 열기 →</span>
      </a>''',
   '''<a class="ml-cta" href="../">
        <span class="ml-cta-emoji">🐣🔌</span>
        <span class="ml-cta-txt"><b>본편 · 데이터로 탐구하는 바이브 피지컬 코딩</b>
        <small>설치·와이파이·LED·가스센서·날씨 API — 이 확장판의 바탕이 되는 본편 교재예요.</small></span>
        <span class="ml-cta-go">본편 열기 →</span>
      </a>'''),
  ('<h1>데이터로 탐구하는<br>바이브 <span class="pk">피</span>지컬 <span class="pk">코</span>딩 🐣</h1>',
   '<h1>소리와 동작을 배우는 <span class="pk">피</span><span class="pk">코</span> 🔊🤸<br>머신러닝 확장판</h1>'),
  ('<p>센서로 모은 데이터와 인터넷의 공개 데이터(API)를, <b><span class="pico-accent">피코</span></b>와 LED·웹으로 ‘보이게’ 만드는 <b>데이터 기반 탐구 프로젝트</b> 안내서예요. 준비(설치·조립)부터 와이파이·LED·날씨 API·가스센서, 그리고 과목별 오픈 API 부록까지 — 모든 코드를 <b>복사해 바로 실행</b>할 수 있습니다. 🌈</p>',
   '<p><b><span class="pico-accent">피코</span></b>로 소리를 <b>듣고</b>(INMP441 마이크) → 무슨 소리인지 <b>배우고</b>(k-NN 분류) → <b>LED 빛으로 표현하고</b> → 몸의 <b>동작</b>(IMU)까지 알아맞히는 <b>머신러닝 확장판</b>이에요. <code>2026-vibe-pico</code> 본편을 끝낸 뒤, 같은 키트로 <b>AI의 듣기·생각·표현·동작 인식</b>을 완성합니다. 모든 코드는 <b>복사해 바로 실행</b>. 🔊🧠💡🤸</p>'),
]
for _a, _b in BRAND:
    out = out.replace(_a, _b)

# ── 인터랙티브 위젯(배선·흐름) 자산을 '페이지당 1회' 주입 ──
# 두 위젯 스크립트는 최상위 const(esc 등)를 쓰고 .wire/.flow를 파싱 시점에 스캔하므로,
# 각 스크립트를 IIFE로 감싸 전역 충돌을 막고, 모든 컨테이너 뒤(=</body> 앞)에 1회만 둔다.
import re as _re
def _strip_scaffold(css):  # 미리보기용 전역 규칙(:root/body/h1/.demo-label) 제거 → 책 :root 그대로 사용
    for sel in (r":root", r"body", r"h1", r"\.demo-label"):
        css = _re.sub(r"(?m)^\s*" + sel + r"\s*\{[^}]*\}", "", css, count=1)
    return css
def _widget_assets(relpath):
    s = open(os.path.join(ROOT, relpath), encoding="utf-8").read()
    a = s.find("<style>") + len("<style>"); b = s.find("</style>", a)
    style = "<style>" + _strip_scaffold(s[a:b]) + "</style>"
    c = s.find("<script>", b) + len("<script>"); d = s.find("</script>", c)  # </style> 뒤에서 찾기(주석 오인 방지)
    return style, "<script>(function(){\n" + s[c:d] + "\n})();</script>"
try:
    _W = [_widget_assets("widgets/" + n) for n in
          ("wiring_preview.html", "flow_preview.html", "mocktest_preview.html", "recorder_preview.html")]
    _assets = "".join(a for a, _ in _W) + "".join(b for _, b in _W)
    out = out.replace("</body>", _assets + "\n</body>")
    print("위젯 자산 주입: 배선+흐름+모의테스트 (스캐폴드 제거·IIFE 격리·페이지당 1회)")
except FileNotFoundError:
    print("⚠ widgets/ 일부 없음 — 해당 위젯은 빈 칸으로 렌더됩니다.")

os.makedirs(os.path.join(ROOT, "ml_site"), exist_ok=True)
open(os.path.join(ROOT, "ml_site", "index.html"), "w", encoding="utf-8").write(out)
try:
    shutil.copy(os.path.join(ROOT, "favicon.svg"), os.path.join(ROOT, "ml_site", "favicon.svg"))
except Exception:
    pass

# 샘플 음성 파일을 사이트에 포함 (웹에서 다운로드용) + 전체 ZIP — MP3 챕터가 있을 때만
import glob, zipfile
_sdir = os.path.join(ROOT, "ml_site", "samples")
if any(c["id"] == "chsay" for c in CHS):
    os.makedirs(_sdir, exist_ok=True)
    _mp3s = sorted(glob.glob(os.path.join(ROOT, "mp3_lesson", "sample_sd", "*.mp3")))
    for _m in _mp3s:
        shutil.copy(_m, _sdir)
    if _mp3s:
        with zipfile.ZipFile(os.path.join(_sdir, "sd_voice_samples.zip"), "w") as _z:
            for _m in _mp3s:
                _z.write(_m, os.path.basename(_m))
        print("샘플 음성 %d개 + ZIP → ml_site/samples/" % len(_mp3s))
elif os.path.isdir(_sdir):
    shutil.rmtree(_sdir)
    print("MP3 챕터 보류 중 — ml_site/samples/ 제거")

print("OK → ml_site/index.html (%d bytes · %d챕터 · %d코드 · %d프롬프트)" % (len(out), len(CHS), ncode, nprompt))
