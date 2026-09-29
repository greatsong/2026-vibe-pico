# 생태 관측기 ⑥ — BirdNET으로 새소리 찾기 (컴퓨터의 파이썬으로 실행)
# BirdNET은 코넬 조류학 연구소와 켐니츠 공대가 만든 새소리 인식 AI예요. 6,000종이 넘는 새를 알아봐요.
# 준비(처음 한 번): pip install birdnet    ← 파이썬 3.11 또는 3.12. 첫 실행 때 모델을 내려받아요(인터넷 필요)
# 사용: python eco_pc_birdnet.py eco
#  - WAV마다 BirdNET이 찾은 새 이름과 신뢰도를 birdnet.csv에 적어요.
#  - labels.csv의 bird 칸이 비어 있으면 BirdNET 결과로 채워요(신뢰도 THRESH 이상이면 1). 채운 칸은 memo에 "birdnet"이라고 표시해요.
#  - BirdNET도 틀려요. 자동으로 채운 칸은 소리를 듣고 스펙트로그램을 보며 꼭 확인하세요.
# 이용 조건: BirdNET 모델은 CC BY-NC-SA 4.0이에요. 교육·연구 목적 사용은 비상업적 이용으로 허용됩니다.
import csv, os, sys
import birdnet

THRESH = 0.5        # 이 신뢰도 이상이면 '새소리 있음'으로 봐요 (0.25로 낮추면 더 많이 찾지만 오답도 늘어요)
NOT_BIRD = ("Human vocal", "Human non-vocal", "Human whistle", "Dog", "Engine", "Environmental",
            "Fireworks", "Gun", "Noise", "Power tools", "Siren")

def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else "eco"
    wavs = sorted(f for f in os.listdir(folder) if f.lower().endswith(".wav"))
    if not wavs:
        print("WAV 파일이 없어요:", folder); return
    model = birdnet.load("acoustic", "2.4", "tf", library="litert")
    paths = [os.path.abspath(os.path.join(folder, f)) for f in wavs]
    df = model.predict(paths, n_workers=1, top_k=5, default_confidence_threshold=0.1).to_dataframe()
    df["file"] = df["input"].astype(str).map(os.path.basename)
    df["common"] = df["species_name"].str.split("_").str[-1]
    birds = df[~df["common"].isin(NOT_BIRD)]

    best = {}
    for fn in wavs:
        b = birds[birds["file"] == fn].sort_values("confidence", ascending=False)
        best[fn] = (float(b["confidence"].iloc[0]), b["species_name"].iloc[0]) if len(b) else (0.0, "")
    with open(os.path.join(folder, "birdnet.csv"), "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f); wr.writerow(["file", "confidence", "species"])
        for fn in wavs: wr.writerow([fn, "%.2f" % best[fn][0], best[fn][1]])
    print("birdnet.csv 저장 · 새를 찾은 파일 %d개 / 전체 %d개 (신뢰도 %.2f 이상)"
          % (sum(1 for fn in wavs if best[fn][0] >= THRESH), len(wavs), THRESH))

    lab_path = os.path.join(folder, "labels.csv")
    if not os.path.exists(lab_path):
        print("labels.csv가 없어요. ⑤ eco_pc_analyze.py를 먼저 실행하세요."); return
    with open(lab_path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    filled = 0
    for r in rows:
        if r["bird"].strip() == "" and r["file"] in best:
            r["bird"] = "1" if best[r["file"]][0] >= THRESH else "0"
            r["memo"] = ("birdnet %.2f %s" % (best[r["file"]][0], best[r["file"]][1])).strip()
            filled += 1
    with open(lab_path, "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.DictWriter(f, fieldnames=["file", "bird", "memo"]); wr.writeheader()
        for r in rows: wr.writerow({"file": r["file"], "bird": r["bird"], "memo": r.get("memo", "")})
    print("labels.csv의 빈칸 %d개를 BirdNET 결과로 채웠어요. 꼭 직접 확인하세요." % filled)

if __name__ == "__main__":          # BirdNET은 여러 프로세스를 쓰므로 이 줄이 꼭 필요해요
    main()
