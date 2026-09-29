# bird_server.py — 라즈베리파이 5에서 실행하는 새소리 판정 서버 (BirdNET)
# 부록 R의 설치를 마친 뒤, 가상환경을 켠 상태에서:  python bird_server.py
# 하는 일
#  1) 브라우저 페이지(http://Pi주소:8000)에서 WAV 파일을 올리면 BirdNET으로 다시 판정해요 (2차 판정)
#  2) 피코가 3초 WAV를 보내면(/judge) 판정해서 "판정 가장높은새 신뢰도"를 돌려줘요 (실시간 판정)
#     예) "물까치 물까치 0.83", "모르겠음 까치 0.12"(기준보다 낮음), "모르겠음 없음 0.00"
#  3) 모든 결과를 judged.csv에 쌓고, 페이지에서 표로 보고 소리를 다시 들을 수 있어요
# BirdNET V2.4 모델·라벨: BirdNET 프로젝트가 CC BY-NC-SA 4.0으로 안내 (코넬 조류학 연구소 · 켐니츠 공과대학). 수업·연구 같은 비상업 용도로만 사용해요.
import csv, datetime, html, os, socket, subprocess, threading
from urllib.parse import quote
from flask import Flask, Response, redirect, request, send_from_directory
import birdnet

PORT = 8000
MIN_CONF = 0.25          # 이 신뢰도보다 낮으면 "모르겠음"으로 답해요 (올리면 오판↓ 놓침↑)
BIRDS = {                # 한국어 이름: BirdNET 학명 후보 (목록에 있는 것만 판정해요)
    "물까치": ["Cyanopica cyanus"],
    "까치": ["Pica serica", "Pica pica"],
    "직박구리": ["Hypsipetes amaurotis"],
    "참새": ["Passer montanus"],
    "멧비둘기": ["Streptopelia orientalis"],
    "박새": ["Parus minor"],
    "큰부리까마귀": ["Corvus macrorhynchos"],
}

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(HERE, "received")          # 받은 소리 파일
CSV_PATH = os.path.join(HERE, "judged.csv")         # 판정 기록
HEADER = ["time", "source", "file", "species", "best", "confidence"]
os.makedirs(AUDIO_DIR, exist_ok=True)

app = Flask(__name__)
model = None
session = None           # 판정 준비를 한 번만 해 두는 세션 (서버가 켜져 있는 동안 계속 사용)
labels = {}              # BirdNET 라벨 → 한국어 이름
lock = threading.Lock()     # 판정은 한 번에 하나씩
io_lock = threading.Lock()  # 파일 이름 고르기·저장, 기록 쓰기·읽기도 한 번에 하나씩


def load_model():
    global model
    model = birdnet.load("acoustic", "2.4", "tf", library="litert")   # 첫 실행 때 모델을 내려받아요(인터넷 필요)
    names = list(model.species_list)
    for ko, candidates in BIRDS.items():
        for sci in candidates:
            hit = [n for n in names if n.startswith(sci + "_")]
            if hit:
                labels[hit[0]] = ko
                break
        else:
            print("주의: BirdNET 목록에서 찾지 못한 새 →", ko)
    print("판정할 새 %d종: %s" % (len(labels), ", ".join(labels.values())))


def judge(path):
    """WAV 하나를 판정해 (판정, 가장 높은 새, 신뢰도)를 돌려줘요. 신뢰도가 MIN_CONF보다 낮으면 판정은 '모르겠음'."""
    with lock:
        result = session.run([path]).to_dataframe()
    best, conf = "없음", 0.0
    for _, row in result.iterrows():
        c = float(row["confidence"])
        if row["species_name"] in labels and c > conf:
            best, conf = labels[row["species_name"]], c
    return (best if conf >= MIN_CONF else "모르겠음"), best, conf


def record(source, fname, name, best, conf):
    with io_lock:
        new = not os.path.exists(CSV_PATH)
        with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if new:
                w.writerow(HEADER)
            w.writerow([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), source, fname, name, best, "%.2f" % conf])


def safe_name(name):     # 경로 문자를 없애고, 같은 이름이 있으면 번호를 붙여요 (io_lock 안에서 불러요)
    base = os.path.basename(name.replace("\\", "/")).strip() or "sound.wav"
    if not base.lower().endswith(".wav"):
        base += ".wav"
    stem, n, out = base[:-4], 1, base
    while os.path.exists(os.path.join(AUDIO_DIR, out)):
        n += 1
        out = "%s_%d.wav" % (stem, n)
    return out


def read_rows():
    with io_lock:
        if not os.path.exists(CSV_PATH):
            return []
        with open(CSV_PATH, encoding="utf-8") as f:
            return list(csv.DictReader(f))


@app.get("/ping")       # 피코가 시작할 때 서버가 켜져 있는지 확인하는 곳
def ping():
    return Response("ok", mimetype="text/plain")


@app.post("/judge")      # 피코가 3초 WAV를 보내는 곳
def judge_from_pico():
    if request.content_length is None or request.content_length > 256 * 1024:   # 3초 WAV는 약 192KB
        return Response("오류 없음 0.00", status=413, mimetype="text/plain; charset=utf-8")
    data = request.get_data()
    if len(data) < 44 or data[:4] != b"RIFF":
        return Response("오류 없음 0.00", status=400, mimetype="text/plain; charset=utf-8")
    with io_lock:
        fname = safe_name(request.headers.get("X-File", datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_pico.wav"))
        path = os.path.join(AUDIO_DIR, fname)
        with open(path, "wb") as f:
            f.write(data)
    name, best, conf = judge(path)
    if name == "모르겠음":               # 새가 아니면 소리는 남기지 않아요(사람 목소리일 수 있어요)
        os.remove(path)
        fname += " (지움)"
    record("pico", fname, name, best, conf)
    print("피코 → %s  %s (%s %.2f)" % (fname, name, best, conf))
    return Response("%s %s %.2f" % (name, best, conf), mimetype="text/plain; charset=utf-8")


@app.post("/upload")     # 브라우저에서 여러 WAV를 한꺼번에 올리는 곳
def upload():
    for item in request.files.getlist("wavs"):
        if not item.filename.lower().endswith(".wav"):
            continue
        with io_lock:
            fname = safe_name(item.filename)
            path = os.path.join(AUDIO_DIR, fname)
            item.save(path)
        try:
            name, best, conf = judge(path)
        except Exception as e:                          # 망가진 파일은 건너뛰고 기록에 남겨요
            name, best, conf = "읽기실패", "없음", 0.0
            print("판정 실패:", fname, e)
        record("upload", fname, name, best, conf)
    return redirect("/")


@app.get("/audio/<path:fname>")
def audio(fname):
    return send_from_directory(AUDIO_DIR, fname)


@app.get("/judged.csv")
def download_csv():
    if not os.path.exists(CSV_PATH):
        return Response(",".join(HEADER) + "\n", mimetype="text/csv")
    return send_from_directory(HERE, "judged.csv", as_attachment=True)


@app.get("/table")       # 결과 표만 (페이지가 5초마다 새로 불러요)
def table():
    rows = read_rows()
    counts = {}
    for r in rows:
        counts[r["species"]] = counts.get(r["species"], 0) + 1
    out = ["<p>모두 %d개 · %s</p>" % (len(rows), " · ".join("%s %d" % (html.escape(k), v) for k, v in sorted(counts.items(), key=lambda t: -t[1])))]
    out.append("<div class='wrap'><table><tr><th>시각</th><th>판정</th><th>가장 높은 새 · 신뢰도</th><th>듣기</th><th>보낸 곳</th><th>파일</th></tr>")
    for r in reversed(rows[-100:]):
        f = html.escape(r["file"])
        play = "" if r["file"].endswith("(지움)") else (
            "<audio controls preload='none' src='/audio/%s'></audio>" % html.escape(quote(r["file"], safe=""), quote=True))
        out.append("<tr><td>%s</td><td><b>%s</b></td><td>%s %s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
                   % (html.escape(r["time"][5:]), html.escape(r["species"]), html.escape(r.get("best", "")),
                      html.escape(r["confidence"]), play, html.escape(r["source"]), f))
    out.append("</table></div>")
    return "".join(out)


PAGE = """<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>새소리 판정 서버</title>
<style>body{font-family:sans-serif;max-width:900px;margin:0 auto;padding:16px}
.wrap{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:14px}
td,th{border-bottom:1px solid #ddd;padding:4px 6px;text-align:left;white-space:nowrap}
audio{height:28px}form{padding:12px;background:#f3f7f6;border-radius:10px;margin:12px 0}</style></head><body>
<h2>새소리 판정 서버 (BirdNET)</h2>
<p>판정하는 새: {BIRDS} · 기준 신뢰도 {MIN_CONF}</p>
<form action="/upload" method="post" enctype="multipart/form-data">
<b>2차 판정</b>: 피코 SD 카드의 WAV 파일을 골라 올리세요(여러 개 가능)<br>
<input type="file" name="wavs" accept=".wav" multiple> <button>올리고 판정하기</button></form>
<p><a href="/judged.csv">판정 기록 CSV 내려받기</a></p>
<div id="t">불러오는 중…</div>
<script>
function load(){fetch('/table').then(r=>r.text()).then(h=>{document.getElementById('t').innerHTML=h});}
load(); setInterval(load, 5000);
</script></body></html>"""


@app.get("/")
def index():
    # PAGE 안의 CSS에 %가 있어서 % 서식 대신 자리 표시를 바꿔 넣어요
    return PAGE.replace("{BIRDS}", ", ".join(html.escape(v) for v in labels.values())).replace("{MIN_CONF}", "%.2f" % MIN_CONF)


def my_addresses():      # 이 Pi의 IP 주소(피코와 브라우저에 적을 주소)
    try:
        return subprocess.check_output(["hostname", "-I"], text=True, stderr=subprocess.DEVNULL).split()
    except Exception:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("10.255.255.255", 1))
            ip = s.getsockname()[0]
            s.close()
            return [ip]
        except Exception:
            return ["127.0.0.1"]


if __name__ == "__main__":
    load_model()
    with model.predict_session(top_k=3, n_workers=1, default_confidence_threshold=0.05,
                               custom_species_list=list(labels)) as session:
        for ip in my_addresses():
            if ":" not in ip:                           # IPv6 주소는 건너뛰어요
                print("브라우저에서 여세요 →  http://%s:%d   (피코 코드의 SERVER에도 이 주소)" % (ip, PORT))
        app.run(host="0.0.0.0", port=PORT, threaded=True)
