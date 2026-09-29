# 물까치 찾기 ③ — PC에서 채점하기 (피코가 아니라 컴퓨터의 파이썬으로 실행)
# 준비: Thonny 오른쪽 아래 인터프리터를 '이 컴퓨터의 Python'으로 바꾸고, 도구 → 패키지 관리에서 numpy 설치
# 사용: 이 파일을 아래 폴더들이 있는 곳에 저장하고 실행 (명령 창이라면 python eco_pc_score.py 폴더)
#   examples.csv                 ← 피코 SD의 eco/examples.csv를 복사 (피코에서 모은 예시로 채점)
#   시험/물까치/*.wav  시험/다른 새/*.wav …   ← 채점에 쓸 녹음 (예시로 쓰지 않은 녹음)
#   학습/물까치/*.wav  학습/다른 새/*.wav …   ← (선택) WAV로 예시를 만들어 비교하고 싶을 때
# 하는 일
#  1) examples.csv가 있으면 피코에서 모은 예시로, 학습 폴더가 있으면 WAV로 만든 예시(examples_pc.csv)로 채점해요.
#     examples_pc.csv를 SD 카드 eco 폴더에 examples.csv 이름으로 넣으면 피코가 그대로 씁니다.
#  2) 시험 녹음마다 피코처럼 소리가 난 3초를 판단하고, MIN_VOTES를 1~K_NN으로 바꿔 가며 재현율과 오판을 보여 줘요.
#     WAV 파일 이름은 자유이고 16kHz가 아니어도 돼요.
import os, sys, math
import numpy as np

TARGET = "물까치"; K_NN = 9; K = 2.0; PER_FILE = 3      # 학습 녹음 하나에서 뽑을 3초 구간 수
RATE = 16000; PIECE = 1600; PIECES = 30; TOP = 8
BANDS = [300, 404, 545, 734, 990, 1334, 1797, 2422, 3264, 4399, 5929, 7500]
LENS = [max(8, int(2 * RATE / max(120, int(c * 0.35)))) for c in BANDS]
WINS = [np.array([0.5 - 0.5 * math.cos(2 * math.pi * (i + 0.5) / L) for i in range(L)], dtype=np.float32) for L in LENS]
KS = [2 * math.cos(2 * math.pi * f / RATE) for f in BANDS]

def read16(path):                    # 어떤 WAV든(PCM 16·24·32비트, 실수형, 확장 형식) 16kHz 모노, 피코 값 크기(16비트)로
    data = open(path, "rb").read()
    if data[:4] != b"RIFF" or data[8:12] != b"WAVE": raise ValueError("WAV 파일이 아니에요: " + path)
    pos = 12; fmt = None; raw = None
    while pos + 8 <= len(data):
        cid = data[pos:pos + 4]; size = int.from_bytes(data[pos + 4:pos + 8], "little"); body = data[pos + 8:pos + 8 + size]
        if cid == b"fmt ": fmt = body
        if cid == b"data": raw = body
        pos += 8 + size + (size & 1)
    tag, ch, sr = int.from_bytes(fmt[0:2], "little"), int.from_bytes(fmt[2:4], "little"), int.from_bytes(fmt[4:8], "little")
    bits = int.from_bytes(fmt[14:16], "little")
    if tag == 0xFFFE: tag = int.from_bytes(fmt[24:26], "little")      # 확장 형식: 실제 형식은 뒤쪽에 적혀 있어요
    if tag == 3: x = np.rint(np.frombuffer(raw, dtype="<f4" if bits == 32 else "<f8").astype(np.float64) * 32768)
    elif bits == 16: x = np.frombuffer(raw[:len(raw) // 2 * 2], dtype="<i2").astype(np.int64)
    elif bits == 24:
        b = np.frombuffer(raw[:len(raw) // 3 * 3], dtype=np.uint8).reshape(-1, 3).astype(np.int32)
        x = ((b[:, 0] | (b[:, 1] << 8) | (b[:, 2] << 16)) << 8) >> 16      # 24비트 → 피코처럼 위 16비트
    elif bits == 32: x = np.right_shift(np.frombuffer(raw[:len(raw) // 4 * 4], dtype="<i4"), 16)   # 피코의 x >> 16과 같게
    else: raise ValueError("지원하지 않는 WAV 형식이에요: %s" % path)
    x = np.asarray(x)
    if ch > 1: x = x[:len(x) // ch * ch].reshape(-1, ch)[:, 0]              # 피코 MONO처럼 왼쪽 채널
    x = x.astype(np.float64)
    if sr != RATE:                                                           # 16kHz가 아니면 바꿔요(비교용 근사)
        n = (len(x) * RATE + sr - 1) // sr
        x = np.clip(np.rint(np.interp(np.arange(n) * sr / RATE, np.arange(len(x)), x)), -32768, 32767)
    need = PIECE * PIECES + 1024                     # 3초보다 짧으면 뒤를 조용한 소리로 채워요(피코는 늘 3초를 들어요)
    if len(x) < need: x = np.concatenate([x, np.rint(np.random.default_rng(0).normal(0, 30, need - len(x)))])
    return x

def rms(p): p = p[:512]; return float(np.sqrt(np.mean((p - p.mean()) ** 2)))
def band(x, k, L, w):                # 피코 eco_lib의 _band와 같은 계산
    p = 0.0; nb = 0
    for s in range(0, len(x) - L + 1, L):
        s1 = s2 = 0.0
        for v in (x[s:s + L] * w):
            s0 = v + k * s1 - s2; s2 = s1; s1 = s0
        p += s1 * s1 + s2 * s2 - k * s1 * s2; nb += 1
    return p / (nb * L * L)
def shape12(p):
    x = (p - p.mean()).astype(np.float32)
    e = [max(band(x, k, L, w), 0.0) for k, L, w in zip(KS, LENS, WINS)]; tot = sum(e) + 1e-9
    return [math.log(ei / tot + 1e-6) for ei in e]
def features3(seg, thresh):          # 피코 listen3 + features3와 같은 계산
    ps = [seg[j * PIECE:(j + 1) * PIECE] for j in range(PIECES)]
    lv = [rms(p) for p in ps]; active = sum(l > thresh for l in lv) / PIECES
    idx = sorted(range(PIECES), key=lambda j: -lv[j])[:TOP]
    keep = [j for j in idx if lv[j] > thresh]
    if len(keep) < 2: keep = idx[:2]
    fs = np.array([shape12(ps[j]) for j in keep])
    return list(fs.mean(axis=0)) + list(fs.std(axis=0)) + [active]

def quiet_level(x):                  # 조용할 때 크기: 0.03초 조각 크기의 하위 20%
    lv = [rms(x[s:s + 512]) for s in range(0, len(x) - 512, 512)]
    return float(np.percentile(lv, 20)) if lv else 30.0

def segments(x, thresh, limit):      # 피코처럼: 크기가 기준을 넘으면 그때부터 3초
    out = []; s = 0; L = PIECE * PIECES
    while s + 512 + L <= len(x) and len(out) < limit:
        if rms(x[s:s + 512]) > thresh: out.append(x[s:s + L]); s += L      # 피코처럼 감지 조각부터 3초
        else: s += 512
    return out

def loudest(x, thresh, k):           # 학습용: 소리가 큰 3초 구간 k개
    L = PIECE * PIECES; cand = []
    for s in range(0, max(1, len(x) - L + 1), RATE // 2):
        seg = x[s:s + L]
        if len(seg) != L: continue
        if not any(rms(seg[j:j + PIECE]) > thresh for j in range(0, L, PIECE)): continue   # 조용한 구간은 빼요
        cand.append((float(np.mean(seg ** 2)), s))
    cand.sort(reverse=True); out = []; used = []
    for e, s in cand:
        if all(abs(s - u) >= L for u in used): out.append(x[s:s + L]); used.append(s)
        if len(out) >= k: break
    return out

def wavs(d):
    return sorted(os.path.join(d, f) for f in os.listdir(d) if f.lower().endswith(".wav")) if os.path.isdir(d) else []

root = sys.argv[1] if len(sys.argv) > 1 else "."
tr_dir, te_dir = os.path.join(root, "학습"), os.path.join(root, "시험")
pico_csv = os.path.join(root, "examples.csv")

def read_examples(path):             # 피코와 같은 형식의 예시 파일 읽기
    ex = []
    with open(path, encoding="utf-8") as f:
        for ln in f:
            p = ln.strip().split(",")
            if len(p) == 26 and p[25] != "label": ex.append(([float(v) for v in p[:25]], p[25]))
    return ex

def build_from_wavs():               # 학습 폴더의 WAV에서 피코와 똑같은 계산으로 예시를 만들어 저장
    ex = []
    labels = sorted(d for d in os.listdir(tr_dir) if os.path.isdir(os.path.join(tr_dir, d)))
    with open(os.path.join(root, "examples_pc.csv"), "w", encoding="utf-8") as f:
        f.write(",".join("f%d" % i for i in range(25)) + ",label\n")
        for lab in labels:
            for p in wavs(os.path.join(tr_dir, lab)):
                x = read16(p); th = quiet_level(x) * K + 20
                for seg in loudest(x, th, PER_FILE):
                    ft = [float("%.4f" % v) for v in features3(seg, th)]     # 피코가 CSV로 읽는 값과 같게
                    ex.append((ft, lab)); f.write(",".join("%.4f" % v for v in ft) + "," + lab + "\n")
    print("examples_pc.csv 저장 (예시 %d개)" % len(ex))
    return ex

sets = []
if os.path.isfile(pico_csv): sets.append(("피코에서 모은 예시 (examples.csv)", read_examples(pico_csv)))
if os.path.isdir(tr_dir): sets.append(("학습 폴더로 만든 예시 (examples_pc.csv)", build_from_wavs()))
if not sets: sys.exit("예시가 없어요. 피코 SD의 eco/examples.csv를 이 폴더에 복사하거나 학습 폴더를 만드세요")
if not os.path.isdir(te_dir): sys.exit("시험 폴더가 없어요. 시험/물까치, 시험/다른 새 … 폴더에 WAV를 넣으세요")

tests = []                            # (정답 라벨, [녹음 속 3초 판단마다의 특징])
for lab in sorted(os.listdir(te_dir)):
    for p in wavs(os.path.join(te_dir, lab)):
        x = read16(p); th = quiet_level(x) * K + 20
        tests.append((lab, [np.array(features3(seg, th)) for seg in segments(x, th, 6)]))
nP = sum(l == TARGET for l, _ in tests)
print("시험 녹음: %s %d개, 그 밖의 소리 %d개" % (TARGET, nP, len(tests) - nP))

for name, ex in sets:
    counts = {}
    for _, lab in ex: counts[lab] = counts.get(lab, 0) + 1
    print("\n[%s] %s" % (name, counts))
    if len(ex) > 300: print("주의: 피코는 예시를 300개까지만 읽어요. 예시 수를 줄이세요")
    if TARGET not in counts or len(counts) < 2 or min(counts.values()) < 3 or len(ex) < K_NN:
        print("예시가 부족해 채점하지 않아요. 물까치와 다른 소리를 각각 3개 이상, 모두 %d개 이상 준비하세요" % K_NN); continue
    F = np.array([e[0] for e in ex]); lo = F.min(0); sc = 1 / (F.max(0) - lo + 1e-9); Fn = (F - lo) * sc
    labs = np.array([e[1] for e in ex])
    results = []                      # (정답 라벨, [판단마다 물까치 표 수])
    for lab, feats in tests:
        votes = []
        for ft in feats:
            near = np.argsort(((Fn - (ft - lo) * sc) ** 2).sum(1))[:K_NN]
            votes.append(int((labs[near] == TARGET).sum()))
        results.append((lab, votes))
    P = [v for l, v in results if l == TARGET]; N = [v for l, v in results if l != TARGET]
    print("MIN_VOTES | 재현율(물까치 녹음 가운데 찾은 비율) | 오판(다른 소리를 물까치라고 한 비율)")
    for m in range(1, K_NN + 1):
        rec = sum(any(x >= m for x in v) for v in P) / max(len(P), 1)
        fp = sum(any(x >= m for x in v) for v in N) / max(len(N), 1)
        print("    %d     |  %.2f  |  %.2f" % (m, rec, fp))
