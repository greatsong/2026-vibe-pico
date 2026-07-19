# -*- coding: utf-8 -*-
"""build_site.py의 CHAPTERS를 print/content.json으로 내보낸다 (docx 생성용).
   기본: 학생용(강사노트 제외).  `--teacher`: 강사노트 포함 + 운영 계획 페이지 추가.
   code 아이템의 file 참조는 실제 코드 텍스트로 치환한다.
"""
import os, json, sys

TEACHER = "--teacher" in sys.argv

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, "build_site.py"), encoding="utf-8").read()
src = src.split('# === BUILD_MARKER')[0]
ns = {"__file__": os.path.join(ROOT, "build_site.py"), "__name__": "build_site_lib"}
exec(compile(src, "build_site.py", "exec"), ns)

def resolve_items(items):
    out = []
    for it in items:
        t = it.get("type")
        if t == "teacher" and not TEACHER:
            continue                       # 학생용 인쇄본 — 강사노트 제외
        it = dict(it)
        if t == "code" and "file" in it:
            it["code"] = open(os.path.join(ROOT, it["file"]), encoding="utf-8").read().rstrip("\n")
        out.append(it)
    return out

source = list(ns["CHAPTERS"])
if TEACHER:
    source = [ns["PLAN_PAGE"]] + source      # 강사용은 운영 계획을 맨 앞에

chapters = []
for c in source:
    chapters.append({
        "id": c["id"], "num": c["num"], "title": c["title"], "accent": c.get("accent", "#B45309"),
        "subtitle": c.get("subtitle", ""), "goals": c.get("goals", []),
        "why": c.get("why", ""),
        "sections": [{"title": s["title"], "items": resolve_items(s["items"])}
                     for s in c["sections"]],
    })

out = os.path.join(ROOT, "print", "content_teacher.json" if TEACHER else "content.json")
json.dump(chapters, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("OK →", out, "· 챕터", len(chapters), "· 강사노트", "포함" if TEACHER else "제외")
