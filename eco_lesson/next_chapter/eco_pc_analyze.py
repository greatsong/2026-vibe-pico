# 생태 관측기 ⑤ — PC에서 분석하고 채점하기 (피코가 아니라 컴퓨터의 파이썬으로 실행)
# 준비: pip install numpy matplotlib
# 사용: SD 카드의 eco 폴더를 컴퓨터로 복사한 뒤  python eco_pc_analyze.py eco
#  1) WAV마다 스펙트로그램 그림을 spectrograms 폴더에 만들어요. 새소리는 2~8kHz에 짧은 줄무늬로 보여요.
#  2) labels.csv에 파일 목록을 적어 줘요. 소리를 듣고 그림을 보며 bird 칸에 새소리가 있으면 1, 없으면 0을 적으세요.
#     (⑥ BirdNET 코드를 먼저 돌리면 bird 칸을 자동으로 채워 줘요. 그래도 꼭 직접 확인하세요.)
#  3) 정기 녹음기로 이어 녹음한 *_timed.wav에, 피코와 같은 규칙·AI 계산을 돌려 채점해요.
#     아래 설정값을 바꿔 다시 실행하면, 녹음을 다시 하지 않고도 설정에 따른 결과를 비교할 수 있어요.
import csv, math, os, sys, wave
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

K_RULE = 2.5        # 규칙 녹음기 기준 = 조용할 때 크기 × K_RULE + 25   (② 규칙 녹음기와 같게)
K_AI = 2.0          # AI 판단 시작 = 조용할 때 크기 × K_AI + 20         (④ AI 녹음기와 같게)
K_NN = 5
VOTE = 3
CONF = 0.6
LENGTH = 5          # 저장하면 이만큼(초) 녹음하고
COOLDOWN = 3        # 이만큼(초) 쉬었다가 다시 판단해요 (피코와 같은 흐름)

folder = sys.argv[1] if len(sys.argv) > 1 else "eco"
wavs = sorted(f for f in os.listdir(folder) if f.lower().endswith(".wav"))
print("WAV 파일 %d개" % len(wavs))

def read_wav(path):                  # 피코의 값과 같게: 32비트 값을 16비트 크기로 (x >> 16)
    with wave.open(path) as w:
        rate, width, n = w.getframerate(), w.getsampwidth(), w.getnframes()
        raw = w.readframes(n)
    if width == 4: x = np.frombuffer(raw, dtype="<i4") >> 16
    else: x = np.frombuffer(raw, dtype="<i2")
    return rate, x.astype(np.int64)

# ---------- 1) 스펙트로그램 ----------
out = os.path.join(folder, "spectrograms"); os.makedirs(out, exist_ok=True)
for fn in wavs:
    png = os.path.join(out, fn[:-4] + ".png")
    if os.path.exists(png): continue
    rate, x = read_wav(os.path.join(folder, fn))
    if len(x) < 512: continue
    plt.figure(figsize=(8, 3))
    plt.specgram(x - x.mean(), NFFT=512, Fs=rate, noverlap=256, cmap="magma")
    plt.ylim(0, rate / 2); plt.xlabel("time (s)"); plt.ylabel("Hz"); plt.title(fn)
    plt.tight_layout(); plt.savefig(png, dpi=90); plt.close()
print("스펙트로그램:", out)

# ---------- 2) 라벨 파일 ----------
lab_path = os.path.join(folder, "labels.csv")
if not os.path.exists(lab_path):
    with open(lab_path, "w", newline="", encoding="utf-8-sig") as f:
        csv.writer(f).writerow(["file", "bird", "memo"])
with open(lab_path, newline="", encoding="utf-8-sig") as f:
    known = {r["file"] for r in csv.DictReader(f)}
missing = [fn for fn in wavs if fn not in known]
if missing:
    with open(lab_path, "a", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        for fn in missing: wr.writerow([fn, "", ""])
    print("labels.csv에 새 파일 %d개를 적었어요. bird 칸을 채운 뒤 다시 실행하세요." % len(missing))
labels = {}
with open(lab_path, newline="", encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        if r["bird"].strip() in ("0", "1"): labels[r["file"]] = int(r["bird"])
print("bird 칸이 채워진 파일 %d개" % len(labels))

# ---------- 3) 피코와 같은 계산 ----------
BANDS = [200, 350, 600, 1000, 1700, 2800, 4500, 7000]
WIDTH = [150, 200, 300, 500, 800, 1200, 2000, 2500]
LENS = [max(8, int(2 * 16000 / w)) for w in WIDTH]
WINS = [[0.5 - 0.5 * math.cos(2 * math.pi * (i + 0.5) / L) for i in range(L)] for L in LENS]
def _band(x, f, L, w):
    k = 2 * math.cos(2 * math.pi * f / 16000); p = 0.0; nb = 0
    for s in range(0, len(x) - L + 1, L):
        s1 = 0.0; s2 = 0.0
        for v, wv in zip(x[s:s + L], w):
            s0 = v * wv + k * s1 - s2; s2 = s1; s1 = s0
        p += s1 * s1 + s2 * s2 - k * s1 * s2; nb += 1
    return p / (nb * L * L)
def features(x):
    m = sum(x) / len(x); x = [v - m for v in x]
    e = [max(_band(x, f, L, w), 0.0) for f, L, w in zip(BANDS, LENS, WINS)]; tot = sum(e) + 1e-9
    return [math.log(ei / tot + 1e-6) for ei in e]
def level(v):
    m = sum(v) / len(v); return math.sqrt(sum((x - m) ** 2 for x in v) / len(v))

ex_path = os.path.join(folder, "examples.csv")
timed = [fn for fn in wavs if fn.endswith("_timed.wav") and fn in labels]
if not timed or not os.path.exists(ex_path):
    print("채점하려면 bird 칸이 채워진 *_timed.wav와 examples.csv가 필요해요."); sys.exit()

rows = []
with open(ex_path, encoding="utf-8") as f:
    for r in csv.reader(f):
        if len(r) == 9 and r[8] != "label": rows.append(([float(v) for v in r[:8]], r[8]))
mins = [min(r[0][i] for r in rows) for i in range(8)]; maxs = [max(r[0][i] for r in rows) for i in range(8)]
norm = lambda f: [(f[i] - mins[i]) / (maxs[i] - mins[i] + 1e-9) for i in range(8)]
ex = [(norm(r[0]), r[1]) for r in rows]
def predict(f):
    q = norm(f)
    near = sorted((sum((e[0][i] - q[i]) ** 2 for i in range(8)), e[1]) for e in ex)[:K_NN]
    votes = {}; order = []
    for _, lab in near:
        if lab not in votes: votes[lab] = 0; order.append(lab)
        votes[lab] += 1
    top = max(votes.values()); return [l for l in order if votes[l] == top][0]
def vote(pieces):
    votes = {}; order = []
    for x in pieces:
        lab = predict(features(x))
        if lab not in votes: votes[lab] = 0; order.append(lab)
        votes[lab] += 1
    top = max(votes.values()); best = [l for l in order if votes[l] == top][0]
    return best, top / len(pieces)

# 조용할 때 크기: 모든 파일의 0.03초 조각 크기 가운데 하위 20%
lv_all = []
data = {}
for fn in timed:
    _, x = read_wav(os.path.join(folder, fn)); x = [int(v) for v in x]; data[fn] = x
    lv_all += [level(x[s:s + 512]) for s in range(0, len(x) - 512, 512)]
base = float(np.percentile(lv_all, 20))
T_RULE = base * K_RULE + 25; T_AI = base * K_AI + 20
print("조용할 때 크기 %.0f → 규칙 기준 %.0f, AI 판단 시작 %.0f" % (base, T_RULE, T_AI))

def simulate(x, method):             # 이 10초 동안 저장이 한 번이라도 일어났을까?
    s = 0; n = 1600
    while s + 512 <= len(x):
        lv = level(x[s:s + 512]); s += 512
        if method == "rule" and lv > T_RULE: return 1
        if method == "ai" and lv > T_AI:
            pieces = [x[s + j * n: s + (j + 1) * n] for j in range(VOTE)]
            if len(pieces[-1]) < n: return 0
            lab, share = vote(pieces); s += n * VOTE
            if lab == "새소리" and share >= CONF: return 1
            s += int(COOLDOWN * 16000)
    return 0

print("\n채점할 10초 파일 %d개 (새소리 있음 %d개)" % (len(timed), sum(labels[f] for f in timed)))
with open(os.path.join(folder, "score.csv"), "w", newline="", encoding="utf-8-sig") as f:
    wr = csv.writer(f); wr.writerow(["file", "bird", "rule", "ai"])
    res = {m: [] for m in ("rule", "ai")}
    for fn in timed:
        r = {m: simulate(data[fn], m) for m in res}
        for m in res: res[m].append((labels[fn], r[m]))
        wr.writerow([fn, labels[fn], r["rule"], r["ai"]])
for m, pairs in res.items():
    tp = sum(1 for b, s in pairs if b == 1 and s == 1); fp = sum(1 for b, s in pairs if b == 0 and s == 1)
    fn_ = sum(1 for b, s in pairs if b == 1 and s == 0); saved = tp + fp
    recall = tp / (tp + fn_) if tp + fn_ else float("nan"); precision = tp / saved if saved else float("nan")
    print("%-4s 저장 %3d개(%3.0f%%) · 재현율 %.2f · 정밀도 %.2f · 놓침 %d · 쓸데없는 저장 %d"
          % ({"rule": "규칙", "ai": "AI"}[m], saved, 100 * saved / len(pairs), recall, precision, fn_, fp))
print("재현율 = 새소리가 있는 파일 가운데 저장한 비율 · 정밀도 = 저장한 파일 가운데 새소리가 있는 비율")
print("파일별 결과: score.csv")
