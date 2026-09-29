# 물까치 찾기 ⑤ — 물까치가 언제 나타났을까? (컴퓨터의 파이썬으로 실행)
# 준비: pip install matplotlib   ·   사용: python eco_pc_timeline.py eco   (SD 카드의 eco 폴더를 복사해 온 것)
# found.csv(물까치 후보 기록)와 decisions.csv(모든 판단 기록)를 읽어 시간대별 그래프를 그려요.
import csv, os, sys
from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

folder = sys.argv[1] if len(sys.argv) > 1 else "eco"
def read_rows(name):                # 파일이 없으면(아직 한 번도 안 찾았으면) 빈 목록
    path = os.path.join(folder, name)
    if not os.path.exists(path): return []
    with open(path, newline="", encoding="utf-8") as f: return list(csv.DictReader(f))
found = read_rows("found.csv"); allx = read_rows("decisions.csv")
print("물까치 후보 %d번 / 전체 판단 %d번" % (len(found), len(allx)))

hour = lambda r: int(r["time"][11:13])
day = lambda r: r["time"][:10]
hf = Counter(hour(r) for r in found); ha = Counter(hour(r) for r in allx)
hours = list(range(24))
from matplotlib import font_manager
_have = {f.name for f in font_manager.fontManager.ttflist}
plt.rcParams["font.family"] = [f for f in ("AppleGothic", "Malgun Gothic", "NanumGothic") if f in _have][:1] or ["sans-serif"]
plt.figure(figsize=(9, 4))
plt.bar(hours, [ha[h] for h in hours], color="#cfd8dc", label="모든 판단")
plt.bar(hours, [hf[h] for h in hours], color="#0e7490", label="물까치 후보")
plt.xticks(hours); plt.xlabel("시"); plt.ylabel("횟수"); plt.legend(); plt.title("시간대별 물까치 후보")
plt.tight_layout(); plt.savefig(os.path.join(folder, "timeline_hour.png"), dpi=120); plt.close()

for d, n in sorted(Counter(day(r) for r in found).items()):
    print("  %s  %d번" % (d, n))
print("그래프 저장:", os.path.join(folder, "timeline_hour.png"))
print("주의: 후보 횟수는 새의 수가 아니에요. 같은 새가 여러 번 울 수 있고, 오판도 섞여 있어요.")
