# 소리 ML 종합 컨트롤 대시보드 (INMP441 · I2S판) — 피코 2 WH = 웹서버, 폰/PC 브라우저 = 화면
#  한 화면에서: 🔊 라이브 소리 듣기 + 녹음(+즉시 분류) + 실시간 3D 산점도 + 예측 + k조절 + 지우기.
#  마이크=INMP441(I2S, SCK=GP18·WS=GP19·SD=GP20).  sounds.csv(rms,zcr,crest,label) 호환.  (와이파이 필요)
#  ⚠ 아날로그판과 숫자 크기(스케일)가 달라요 — 마이크를 바꿨다면 [전체 지우기]로 데이터를 새로 모으세요!
import network, socket, time, math, gc, struct
from machine import I2S, Pin
from neopixel import NeoPixel
from wifi_config import WIFI_SSID, WIFI_PASSWORD     # 1·3·5장에서 만든 그 파일

audio = I2S(0, sck=Pin(18), ws=Pin(19), sd=Pin(20),
            mode=I2S.RX, bits=32, format=I2S.MONO, rate=16000, ibuf=40000)
N = 2400; raw = bytearray(N * 4)
def grab():
    audio.readinto(raw)
    return [x >> 16 for x in struct.unpack("<%di" % N, raw)]
def features(buf):
    n = len(buf); m = sum(buf) / n; ss = 0.0; zc = 0; peak = 0.0; prev = buf[0] - m
    for v in buf:
        d = v - m; ad = d if d >= 0 else -d; ss += d * d
        if ad > peak: peak = ad
        if (d >= 0) != (prev >= 0): zc += 1
        prev = d
    r = math.sqrt(ss / n); return r, zc, peak / (r + 1e-9)
small = bytearray(512 * 4)
def level():                               # 빠른 '소리 크기'(라이브 미터용)
    audio.readinto(small); v = [x >> 16 for x in struct.unpack("<512i", small)]; m = sum(v) / 512
    return math.sqrt(sum((x - m) ** 2 for x in v) / 512)
def capture(sec=1.5):                      # sec초 중 '가장 또렷한' 0.15초(임계값 없음)
    best = None; bestr = -1.0; t0 = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), t0) < int(sec * 1000):
        f = features(grab())
        if f[0] > bestr: bestr = f[0]; best = f
    return best

LABELS = ["휘파람", "박수", "말소리", "노크"]
COLORS = ["#1D9E75", "#D85A30", "#378ADD", "#7F77DD"]

TIMING = (280, 515, 515, 745); NUM = 10
np = NeoPixel(Pin(16), NUM, timing=TIMING)
def show(ci, lv):
    c = [(40, 0, 0), (0, 40, 0), (0, 0, 40), (40, 40, 0)][ci % 4]
    for i in range(NUM): np[i] = c if i < lv else (0, 0, 0)
    np.write()

rows = []
try:
    for ln in open("sounds.csv"):
        ln = ln.strip()
        if ln == "" or ln.startswith("rms"): continue
        r, z, c, nm = ln.split(","); rows.append((float(r), float(z), float(c), nm))
except OSError:
    pass
def save_csv():
    f = open("sounds.csv", "w"); f.write("rms,zcr,crest,label\n")
    for r in rows: f.write("%.0f,%d,%.2f,%s\n" % (r[0], r[1], r[2], r[3]))
    f.close()

def predict(feat, k=5):
    if len(rows) < 2: return None, 0.0
    mins = [min(r[i] for r in rows) for i in range(3)]
    maxs = [max(r[i] for r in rows) for i in range(3)]
    def nz(v, i): return (v - mins[i]) / (maxs[i] - mins[i] + 1e-9)
    q = [nz(feat[i], i) for i in range(3)]
    def d2(r): return sum((nz(r[i], i) - q[i]) ** 2 for i in range(3))
    near = sorted(rows, key=d2)[:k]; vote = {}
    for r in near: vote[r[3]] = vote.get(r[3], 0) + 1.0 / (d2(r) + 1e-6)
    b = max(vote, key=vote.get); return b, vote[b] / sum(vote.values())

wlan = network.WLAN(network.STA_IF); wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)
for _ in range(30):
    if wlan.isconnected(): break
    time.sleep(0.5)
print("브라우저에서 여세요 →  http://%s" % wlan.ifconfig()[0])

PAGE = """<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>소리 ML 컨트롤 센터</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>body{font-family:sans-serif;max-width:760px;margin:0 auto;padding:16px;color:#222}
h2{margin:.2em 0}.sec{border:1px solid #e5e5e5;border-radius:12px;padding:12px 14px;margin:12px 0}
.sec b.t{font-size:14px}button{font-size:15px;padding:9px 13px;margin:4px;border:1px solid #999;border-radius:10px;background:#fff;cursor:pointer}
#meter{height:16px;border-radius:9px;background:#eee;overflow:hidden;margin:8px 0}#meter>i{display:block;height:100%;width:0%;background:#0891B2;transition:width .12s}
#plot{height:420px}#out{font-size:20px;font-weight:700;margin:8px 0}#rec{font-size:13px;color:#555;min-height:18px}
.muted{color:#777;font-size:13px}input[type=range]{vertical-align:middle}</style></head><body>
<h2>🎛️ 소리 ML 컨트롤 센터 <span class="muted">· INMP441</span></h2>
<div class="sec"><b class="t">🔊 라이브 — 지금 들리는 소리</b><div id="meter"><i></i></div><div class="muted" id="mtxt">마이크가 듣고 있어요…</div></div>
<div class="sec"><b class="t">① 데이터 만들기</b> <span class="muted">(버튼 누르고 1~2초 안에 소리)</span>
<div id="btns"></div><div id="rec"></div><div class="muted" id="cnt"></div></div>
<div class="sec"><b class="t">② 한눈에 — 모은 소리 3D 지도</b><div id="plot"></div></div>
<div class="sec"><b class="t">② 테스트 — 새 소리 분류</b>
<div><button onclick="pred()">🔮 예측 한 번</button>
이웃 k= <input type="range" id="k" min="1" max="9" step="2" value="5" oninput="kv.textContent=this.value"><b id="kv">5</b>
<button onclick="clr()">전체 지우기</button></div><div id="out">소리를 모은 뒤 예측해 보세요</div></div>
<script>
const LAB=__LABELS__, COL=__COLORS__; let maxL=1, busy=false;
let bh=''; LAB.forEach((n,i)=>bh+=`<button onclick="rec(${i})">${n}</button>`);
document.getElementById('btns').innerHTML=bh;
function setMeter(p){document.getElementById('meter').firstChild.style.width=Math.min(100,p*100)+'%';}
async function poll(){
  if(!busy){ try{ let r=await (await fetch('/level')).json(); maxL=Math.max(maxL,r.l,1); setMeter(r.l/maxL);
    document.getElementById('mtxt').textContent = r.l>maxL*0.35?'소리가 들려요! 🔊':'조용… (마이크 대기 중)'; }catch(e){} }
  setTimeout(poll,250);
}
poll();
async function rec(i){ busy=true; document.getElementById('rec').textContent='녹음 중… "'+LAB[i]+'" 소리를 내세요';
  let r=await (await fetch('/rec?i='+i)).json(); busy=false;
  let pv = (r.pred&&r.pred!=='-') ? ('현재 모델 판단: '+r.pred+' '+r.conf+'% '+(r.pred===r.saved?'✓ 잘 맞아요':'— 더 모아보세요')) : '(아직 예시가 적어요)';
  document.getElementById('rec').textContent='저장됨: '+r.saved+'  ·  '+pv; draw();
}
async function pred(){ busy=true; document.getElementById('out').textContent='예측 중… 소리를 내세요';
  let k=document.getElementById('k').value;
  let r=await (await fetch('/predict?k='+k)).json(); busy=false;
  document.getElementById('out').textContent = r.conf>=60 ? '이건… '+r.label+'! (확신 '+r.conf+'%)' : '음… 잘 모르겠어요 (확신 '+r.conf+'%)';
  draw(r);
}
async function clr(){ busy=true; await fetch('/clear'); busy=false; document.getElementById('out').textContent='지웠어요'; draw(); }
async function draw(pred){
  let d=await (await fetch('/data')).json(), cnt={};
  d.forEach(p=>cnt[p.label]=(cnt[p.label]||0)+1);
  document.getElementById('cnt').textContent='모은 개수 — '+LAB.map(n=>n+' '+(cnt[n]||0)).join(' · ');
  let tr=LAB.map((n,i)=>({type:'scatter3d',mode:'markers',name:n,
    x:d.filter(p=>p.label==n).map(p=>p.rms),y:d.filter(p=>p.label==n).map(p=>p.zcr),z:d.filter(p=>p.label==n).map(p=>p.crest),
    marker:{size:4,color:COL[i]}}));
  if(pred&&pred.feat) tr.push({type:'scatter3d',mode:'markers',name:'방금',
    x:[pred.feat[0]],y:[pred.feat[1]],z:[pred.feat[2]],marker:{size:9,color:'#000',symbol:'diamond'}});
  Plotly.react('plot',tr,{margin:{l:0,r:0,t:0,b:0},
    scene:{xaxis:{title:'크기'},yaxis:{title:'높낮이'},zaxis:{title:'들쭉날쭉'}}},{displayModeBar:false});
}
draw();
</script></body></html>"""

def send(cl, body, ctype="text/html"):
    if not isinstance(body, bytes): body = body.encode()
    hdr = ("HTTP/1.0 200 OK\r\nContent-Type: %s; charset=utf-8\r\nConnection: close\r\nContent-Length: %d\r\n\r\n" % (ctype, len(body))).encode()
    mv = memoryview(hdr + body)
    while mv:
        try:
            sent = cl.send(mv); mv = mv[sent:]
        except OSError:
            time.sleep(0.005)

srv = socket.socket(); srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("0.0.0.0", 80)); srv.listen(1); srv.setblocking(False)
show(0, 0)
while True:
    try: cl, _ = srv.accept()
    except OSError: cl = None
    if cl:
        try:
            gc.collect()                          # 녹음/응답마다 큰 리스트가 쌓여 단편화 방지(5장 패턴)
            cl.settimeout(5)
            path = cl.recv(1024).split(b" ")[1]
            if path.startswith(b"/level"):
                send(cl, '{"l":%.0f}' % level(), "application/json")
            elif path.startswith(b"/rec?i="):
                i = int(path.split(b"=")[1]); show(i, NUM)
                f = capture()
                pn, pc = predict(f)                       # 추가 '전' 현재 모델로 분류해 보기
                rows.append((f[0], f[1], f[2], LABELS[i])); save_csv(); show(0, 0)
                pj = '"-"' if pn is None else '"%s"' % pn
                send(cl, '{"saved":"%s","pred":%s,"conf":%d}' % (LABELS[i], pj, int((pc or 0) * 100)), "application/json")
            elif path.startswith(b"/predict"):
                k = 5
                if b"k=" in path:
                    try: k = int(path.split(b"k=")[1].split(b"&")[0].split(b" ")[0])
                    except Exception: k = 5
                f = capture(); name, conf = predict(f, k)
                if name is None:
                    send(cl, '{"label":"-","conf":0,"feat":[%.0f,%d,%.2f]}' % (f[0], f[1], f[2]), "application/json")
                else:
                    ci = LABELS.index(name) if name in LABELS else 0
                    show(ci, max(1, int(conf * NUM)))
                    send(cl, '{"label":"%s","conf":%d,"feat":[%.0f,%d,%.2f]}' % (name, int(conf * 100), f[0], f[1], f[2]), "application/json")
                    time.sleep(0.4); show(0, 0)
            elif path.startswith(b"/data"):
                pts = ",".join('{"rms":%.0f,"zcr":%d,"crest":%.2f,"label":"%s"}' % (r[0], r[1], r[2], r[3]) for r in rows)
                send(cl, ("[" + pts + "]").encode(), "application/json")
            elif path.startswith(b"/clear"):
                del rows[:]; save_csv(); send(cl, '{"ok":1}', "application/json")
            else:
                send(cl, PAGE.replace("__LABELS__", str(LABELS)).replace("__COLORS__", str(COLORS)))
        except Exception:
            pass
        cl.close()
    time.sleep(0.01)
