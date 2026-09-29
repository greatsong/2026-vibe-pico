# -*- coding: utf-8 -*-
# 준비물 표의 부품 사진(썸네일) 도우미
# 사진 파일은 이 폴더에 <키>.jpg 또는 <키>.svg로 두고, 출처는 meta.json에 적어요.
# 실물 사진으로 바꿀 때는 같은 키의 .jpg를 덮어쓰고 meta.json의 출처를 "직접 촬영"으로 고치면 돼요.
import json, os
_HERE = os.path.dirname(os.path.abspath(__file__))
try:
    META = json.load(open(os.path.join(_HERE, "meta.json"), encoding="utf-8"))
except FileNotFoundError:
    META = {}

def _file(key):
    for ext in (".jpg", ".png", ".svg"):
        if os.path.exists(os.path.join(_HERE, key + ext)):
            return key + ext
    return None

def thumb(key, alt=""):
    """표 칸에 넣을 작은 사진 HTML. 사진이 없으면 빈 문자열."""
    f = _file(key) if key else None
    if not f:
        return ""
    m = META.get(key, {})
    title = m.get("credit", "")
    return (f"<img src='../parts_img/{f}' alt='{alt}' title='{title}' loading='lazy' "
            f"style='width:72px;height:54px;object-fit:contain;background:#fff;border:1px solid var(--line);border-radius:8px;display:block'>")

def credits(keys):
    """표 아래에 붙일 '사진 출처' 접힌 목록. 출처가 있는 사진만."""
    rows = []
    for k in keys:
        m = META.get(k)
        if not m or not _file(k):
            continue
        src = f"<a href='{m['page']}' target='_blank' rel='noopener'>{m.get('title', k)}</a>" if m.get("page") else m.get("title", k)
        lic = f"<a href='{m['license_url']}' target='_blank' rel='noopener'>{m['license']}</a>" if m.get("license_url") else m.get("license", "")
        rows.append(f"<li>{src} · {m.get('author', '')} · {lic}{' · ' + m['note'] if m.get('note') else ''}</li>")
    if not rows:
        return ""
    return ("<details style='margin:6px 0 14px;font-size:12.5px;color:var(--text-soft)'><summary>사진 출처</summary><ul style='margin:6px 0 0 18px'>"
            + "".join(rows) + "</ul></details>")
