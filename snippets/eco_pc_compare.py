# 물까치 찾기 ⑦ — 세 가지 판정 방식 비교하기 (PC에서 실행 · 설치할 것 없음)
# ④ 실시간 판정(SEND_ALL = True)이 피코 SD에 남긴 server.csv에 'truth' 열을 더해, 틀어 준 소리가 물까치였으면 1, 아니면 0을 적으세요.
# 사용: server.csv를 이 파일과 같은 폴더에 두고 실행 (명령 창이라면 python eco_pc_compare.py server.csv)
# 보여 주는 것: ① 피코만 ② BirdNET만 ③ 피코가 거른 뒤 BirdNET — 기준을 바꿔 가며 재현율과 오판
import csv, sys

path = sys.argv[1] if len(sys.argv) > 1 else "server.csv"
rows = []
with open(path, encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        t = (r.get("truth") or "").strip()
        if t not in ("0", "1") or r.get("birdnet") in ("서버 없음", "서버 오류"):
            continue                                          # 정답을 안 적었거나 서버에 묻지 못한 줄은 빼요
        rows.append((t == "1", int(r["pico_votes"]), r["best"], float(r["confidence"])))
P = sum(1 for t, *_ in rows if t); N = len(rows) - P
print("비교에 쓴 판정 %d개 (물까치 %d · 다른 소리 %d)" % (len(rows), P, N))
if P == 0 or N == 0:
    sys.exit("물까치(1)와 다른 소리(0)가 모두 있어야 비교할 수 있어요")

def score(rule):                                              # (재현율, 오판)
    hit = sum(1 for t, v, b, c in rows if t and rule(v, b, c))
    fp = sum(1 for t, v, b, c in rows if not t and rule(v, b, c))
    return hit / P, fp / N

print("\n방식                       | 재현율 | 오판")
for m in (2, 3, 4, 5):
    print("피코만 MIN_VOTES %d          |  %.2f  | %.2f" % ((m,) + score(lambda v, b, c, m=m: v >= m)))
for th in (0.10, 0.25, 0.50):
    print("BirdNET만 신뢰도 %.2f       |  %.2f  | %.2f" % ((th,) + score(lambda v, b, c, th=th: b == "물까치" and c >= th)))
    for m in (2, 3):
        print("피코 %d표 → BirdNET %.2f    |  %.2f  | %.2f" % ((m, th) + score(lambda v, b, c, m=m, th=th: v >= m and b == "물까치" and c >= th)))
print("\n재현율 = 물까치 소리 가운데 물까치라고 한 비율 · 오판 = 다른 소리를 물까치라고 한 비율")
