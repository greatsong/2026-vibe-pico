# 물까치 찾기 ③ — 채점하고 기준 정하기 (PC에서 실행 · 설치할 것 없음)
# 피코 SD의 eco/decisions.csv(ML2 탐지기) 또는 eco/server.csv(ML3)를 이 파일과 같은 폴더에 두고,
# 스프레드시트로 열어 맨 오른쪽에 truth 열을 만들어요. 적어 둔 시각과 CSV의 time을 맞춰, 물까치를 튼 줄은 1, 나머지는 0을 적고 CSV로 저장해요.
# 틀어 준 소리가 탐지기에 아예 감지되지 않아 줄이 없을 수도 있어요. 아래 두 값에 실제로 틀어 준 횟수를 적으면
# 줄이 없는 물까치는 '놓친 물까치'로, 줄이 없는 다른 소리는 '물까치라고 하지 않은 소리'로 세요. (0이면 기록된 줄만으로 계산)
# 사용: Thonny의 '이 컴퓨터의 Python'으로 실행 (명령 창이라면 python eco_pc_compare.py decisions.csv)
import csv, os, sys

MAGPIE_PLAYED = 0   # 틀어 준 물까치 수
OTHER_PLAYED = 0    # 틀어 준 다른 소리 수

path = sys.argv[1] if len(sys.argv) > 1 else ("server.csv" if os.path.exists("server.csv") else "decisions.csv")
rows = []
with open(path, encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        t = (r.get("truth") or "").strip()
        if t not in ("0", "1") or r.get("birdnet") in ("서버 없음", "서버 오류"):
            continue                                          # 정답을 안 적었거나 서버에 묻지 못한 줄은 빼요
        votes = int(r.get("target_votes") or r.get("pico_votes") or 0)
        rows.append((t == "1", votes, r.get("best", ""), float(r.get("confidence") or 0)))
detected = sum(1 for t, *_ in rows if t)
P = max(detected, MAGPIE_PLAYED); N = max(len(rows) - detected, OTHER_PLAYED)
print("%s: 판정 %d줄 (물까치 %d · 다른 소리 %d)" % (os.path.basename(path), len(rows), detected, len(rows) - detected))
if P > detected or N > len(rows) - detected:
    print("줄이 없는 재생 포함: 물까치 %d번 중 %d번, 다른 소리 %d번 중 %d번이 감지되지 않았어요" % (P, P - detected, N, N - (len(rows) - detected)))
if P == 0 or N == 0:
    sys.exit("물까치(1)와 다른 소리(0)가 모두 있어야 비교할 수 있어요")

def score(rule):                                              # (재현율, 오판)
    hit = sum(1 for t, v, b, c in rows if t and rule(v, b, c))
    fp = sum(1 for t, v, b, c in rows if not t and rule(v, b, c))
    return hit / P, fp / N

print("\n방식                       | 재현율 | 오판")
for m in range(1, 10):
    print("피코만 MIN_VOTES %d          |  %.2f  | %.2f" % ((m,) + score(lambda v, b, c, m=m: v >= m)))
if any(b for t, v, b, c in rows):                             # server.csv라면 BirdNET 방식도
    for th in (0.10, 0.25, 0.50):
        print("BirdNET만 신뢰도 %.2f       |  %.2f  | %.2f" % ((th,) + score(lambda v, b, c, th=th: b == "물까치" and c >= th)))
        print("피코 3표 → BirdNET %.2f    |  %.2f  | %.2f" % ((th,) + score(lambda v, b, c, th=th: v >= 3 and b == "물까치" and c >= th)))
print("\n재현율 = 물까치 가운데 물까치라고 한 비율 · 오판 = 다른 소리를 물까치라고 한 비율")
