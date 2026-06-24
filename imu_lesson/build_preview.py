# -*- coding: utf-8 -*-
"""별도 미리보기 빌더 — 기존 build_site.py를 '수정 없이' 재사용해
   IMU 머신러닝 챕터만 단독 HTML(imu_preview.html)로 렌더한다.
   build_site.py·index.html은 전혀 건드리지 않는다.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                      # 저장소 루트

# build_site.py 소스에서 '마지막 index.html 쓰기' 블록만 떼고 실행 → 부작용 없음
src = open(os.path.join(ROOT, "build_site.py"), encoding="utf-8").read()
src = src.split('\nwith open(os.path.join(BASE, "index.html")')[0]
ns = {"__file__": os.path.join(ROOT, "build_site.py"), "__name__": "build_site_lib"}
exec(compile(src, os.path.join(ROOT, "build_site.py"), "exec"), ns)

render_item, esc, TEMPLATE = ns["render_item"], ns["esc"], ns["TEMPLATE"]

import sys
sys.path.insert(0, HERE)
from chapter_imu import CHAPTER_IMU as c

# render() 의 한 챕터 조립 로직을 그대로 재현
nav = [f'<div class="nav-ch"><a href="#{c["id"]}" class="nav-ch-link" data-target="{c["id"]}">'
       f'<span class="nav-dot" style="background:{c["accent"]}"></span>'
       f'{esc(c["num"])}. {esc(c["title"])}</a><div class="nav-secs">']
sec_html = []
for si, s in enumerate(c["sections"]):
    sid = f'{c["id"]}-{si}'
    nav.append(f'<a href="#{sid}" class="nav-sec" data-target="{sid}">{esc(s["title"])}</a>')
    items_html = "".join(render_item(it, c["accent"]) for it in s["items"])
    sec_html.append(f'<section class="sec" id="{sid}">'
                    f'<h3 class="sec-title">{esc(s["title"])}</h3>{items_html}</section>')
nav.append('</div></div>')

goals = "".join(f'<li>{g}</li>' for g in c.get("goals", []))
intro = ''
if goals:
    intro += f'<div class="goals"><div class="goals-t">🎯 이 장을 마치면</div><ul>{goals}</ul></div>'
if c.get("why"):
    intro += f'<div class="why"><div class="why-t">💡 왜 배우나요?</div><p>{c["why"]}</p></div>'

main = (f'<div class="chapter" id="{c["id"]}">'
        f'<div class="ch-head"><span class="ch-num" style="color:{c["accent"]}">CHAPTER {c["num"]}</span>'
        f'<h2 class="ch-title"><span class="ch-bar" style="background:{c["accent"]}"></span>'
        f'{esc(c["title"])}</h2><p class="ch-sub">{esc(c["subtitle"])}</p></div>'
        f'{intro}{c.get("extra","")}{"".join(sec_html)}</div>')

out = (TEMPLATE.replace("/*NAV*/", "".join(nav)).replace("/*MAIN*/", main)
       .replace("/*NCODE*/", "4").replace("/*NPROMPT*/", "1").replace("/*NCH*/", "1"))
open(os.path.join(HERE, "imu_preview.html"), "w", encoding="utf-8").write(out)
print("OK → imu_lesson/imu_preview.html (%d bytes)" % len(out))
