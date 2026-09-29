# eco_lib.py — 물까치 찾는 피코 공통 도구
# 피코에 이 이름(eco_lib.py) 그대로 한 번 저장해 두면, 이 챕터의 모든 코드가 이 파일을 불러 씁니다.
# 핀 배치: 마이크 D20(GP20·GP21) + A2(GP28) · microSD SPI0 헤더(GP2~GP5) · 시계 I2C0(GP9·GP8)
#          MP3 UART0(GP0·GP1) · LED D16 · 버튼 D18
from machine import I2S, SPI, I2C, UART, Pin
from neopixel import NeoPixel
from array import array
import sdcard, os, vfs, errno, struct, time, math, gc

RATE = 16000        # 1초에 16000번 소리를 재요. 특징 계산이 이 값에 맞춰져 있으니 바꾸지 않아요
IBUF = 64000        # 마이크 내부 버퍼. 16kHz에서 약 0.5초 분량이에요

np = NeoPixel(Pin(16), 10, timing=(280, 515, 515, 745))
btn = Pin(18, Pin.IN)
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100_000)


# ---------- LED · 버튼 ----------
def led(c, n=10):
    for i in range(10): np[i] = c if i < n else (0, 0, 0)
    np.write()

def error_blink(times=6):           # 전원만 연결해 실행할 때 문제가 생기면 빨간 불이 깜빡여요
    for _ in range(times):
        led((40, 0, 0)); time.sleep(0.25); led((0, 0, 0)); time.sleep(0.25)

_stop = [False]
def _pressed(pin):                  # 3초 듣기나 계산 중에 짧게 눌러도 놓치지 않게 기억해 둬요
    _stop[0] = True
btn.irq(trigger=Pin.IRQ_RISING, handler=_pressed)

def stop_reset():
    _stop[0] = False
def want_stop():                    # 버튼을 한 번이라도 누르면 '멈춤'을 계속 기억해요. 하던 기록은 마치고 끝나요
    if btn.value() == 1: _stop[0] = True
    return _stop[0]


# ---------- microSD ----------
def sd_mounted():
    for _, point in vfs.mount():
        if point == "/sd": return True
    return False

def sd_open():                      # SD 카드를 /sd에 연결하고 /sd/eco 폴더를 준비. 이번에 새로 연결했으면 True
    new = False
    try:
        if not sd_mounted():
            spi = SPI(0, baudrate=1_000_000, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
            card = sdcard.SDCard(spi, Pin(5, Pin.OUT), baudrate=10_000_000)
            vfs.mount(card, "/sd"); new = True
        try:
            os.mkdir("/sd/eco")
        except OSError as e:
            if e.args[0] != errno.EEXIST: raise
        return new
    except:
        if new: vfs.umount("/sd")
        raise

def remove_quiet(path):             # 파일이 있으면 지우고, 없으면 그냥 넘어가요
    try:
        os.remove(path)
    except OSError as e:
        if e.args[0] != errno.ENOENT: raise

def log(name, header, line):        # /sd/eco/name 에 한 줄 추가. 처음이면 제목 줄부터
    new = name not in os.listdir("/sd/eco")
    with open("/sd/eco/" + name, "a") as f:
        if new: f.write(header + "\n")
        f.write(line + "\n")


# ---------- 시계 DS3231 ----------
def _b2d(v):
    if (v & 15) > 9 or (v >> 4) > 9:
        raise ValueError("시계 값이 이상해요. ⓪ 부품 확인으로 시계를 다시 맞추세요")
    return (v >> 4) * 10 + (v & 15)

def _d2b(v):
    return ((v // 10) << 4) | (v % 10)

def clock_set_from_pico():          # Thonny가 맞춰 둔 피코 시각을 DS3231에 옮겨 적어요
    y, mo, d, h, mi, s, wd, _ = time.localtime()
    if not 2025 <= y <= 2099:
        raise ValueError("피코 시각이 맞춰져 있지 않아요. Thonny로 연결한 상태에서 실행하세요")
    i2c.writeto_mem(0x68, 0x00, bytes([_d2b(s), _d2b(mi), _d2b(h), _d2b(wd + 1), _d2b(d), _d2b(mo), _d2b(y - 2000)]))
    st = i2c.readfrom_mem(0x68, 0x0F, 1)[0]
    i2c.writeto_mem(0x68, 0x0F, bytes([st & 0x7F]))     # '시계가 멈춘 적 있음' 표시 지우기

def clock_now():                    # (년, 월, 일, 시, 분, 초)
    if i2c.readfrom_mem(0x68, 0x0F, 1)[0] & 0x80:
        raise ValueError("시계가 멈춘 적이 있어요. ⓪ 부품 확인으로 시계를 다시 맞추세요")
    r = i2c.readfrom_mem(0x68, 0x00, 7)
    if r[2] & 0x40:                                       # 12시간제로 설정된 시계
        h = _b2d(r[2] & 0x1F) % 12 + (12 if r[2] & 0x20 else 0)
    else:
        h = _b2d(r[2] & 0x3F)
    y = 2000 + _b2d(r[6]) + (100 if r[5] & 0x80 else 0)
    mo = _b2d(r[5] & 0x1F); d = _b2d(r[4]); mi = _b2d(r[1] & 0x7F); s = _b2d(r[0] & 0x7F)
    if not (2025 <= y <= 2099 and 1 <= mo <= 12 and 1 <= d <= 31 and 0 <= h <= 23 and 0 <= mi <= 59 and 0 <= s <= 59):
        raise ValueError("시계의 날짜나 시각이 이상해요. ⓪ 부품 확인으로 시계를 다시 맞추세요")
    return (y, mo, d, h, mi, s)

def stamp():                        # 파일 이름용 "20261001_071502"
    return "%04d%02d%02d_%02d%02d%02d" % clock_now()

def when():                         # 기록용 "2026-10-01 07:15:02"
    return "%04d-%02d-%02d %02d:%02d:%02d" % clock_now()


# ---------- 마이크 INMP441 ----------
def mic_open():
    return I2S(0, sck=Pin(20), ws=Pin(21), sd=Pin(28),
               mode=I2S.RX, bits=32, format=I2S.MONO, rate=RATE, ibuf=IBUF)

PIECE = 1600                        # 0.1초 조각
PIECES = 30                         # 3초 = 조각 30개
TOP = 8                             # 특징을 계산할 큰 소리 조각 수 (메모리를 아끼려고 8개만 남겨요)
_piece = bytearray(PIECE * 4); _pmv = memoryview(_piece)
small = bytearray(512 * 4)          # 소리 크기용 512개 = 약 0.03초

def _rms(buf, count):               # 앞쪽 count개로 소리 크기(RMS) 계산. 교재 소리 챕터와 같은 식
    v = struct.unpack("<%di" % count, buf[:count * 4])
    m = 0
    for x in v: m += x >> 16
    m /= count; s = 0.0
    for x in v:
        d = (x >> 16) - m; s += d * d
    return math.sqrt(s / count)

def level(audio):
    audio.readinto(small)
    return _rms(small, 512)

def baseline(audio):                # 조용할 때의 크기 (25번 잰 값의 중앙값)
    for _ in range(8): level(audio)                       # 켜진 직후 튀는 값은 버려요
    bg = sorted(level(audio) for _ in range(25))
    return bg[len(bg) // 2]

def drain(audio, seconds):          # 버튼을 보며 seconds초 기다려요. 그동안 쌓이는 소리는 읽어서 버려요
    t0 = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), t0) < seconds * 1000 and not want_stop():
        audio.readinto(_pmv)


# ---------- 3초 듣기 ----------
def wav_head(n):                    # 32비트 모노 16kHz WAV 머리말 (n = 소리 데이터 바이트 수)
    return (b"RIFF" + struct.pack("<I", 36 + n) + b"WAVE" + b"fmt " +
            struct.pack("<IHHIIHH", 16, 1, 1, RATE, RATE * 4, 4, 32) + b"data" + struct.pack("<I", n))

def listen3(audio, thresh, path=None, prefix=None):
    # 3초를 들어요. prefix에 소리를 감지한 조각(small)을 주면 그 조각부터 3초에 넣어요.
    # path를 주면 그 3초를 WAV로 저장해요. 중간에 실패하면 불완전한 파일을 지워요.
    # 돌려주는 값: (특징을 계산할 큰 소리 조각들의 바이트 목록, 소리가 기준보다 컸던 조각의 비율)
    top = []; loud = 0; f = None; done = False
    try:
        if path:
            f = open(path, "wb")
            if f.write(wav_head(0)) != 44: raise OSError("WAV 머리말을 쓰지 못했어요")
        for j in range(PIECES):
            if j == 0 and prefix is not None:
                _piece[:len(prefix)] = prefix
                n = audio.readinto(_pmv[len(prefix):]); want = len(_piece) - len(prefix)
            else:
                n = audio.readinto(_pmv); want = len(_piece)
            if n != want: raise OSError("마이크에서 소리를 다 읽지 못했어요")
            if f and f.write(_pmv) != len(_piece): raise OSError("SD 카드에 소리를 다 쓰지 못했어요")
            lv = _rms(_piece, 512)
            if lv > thresh: loud += 1
            if len(top) < TOP or lv > top[-1][0]:
                top.append((lv, bytes(_piece)))
                top.sort(key=lambda t: -t[0])
                if len(top) > TOP: top.pop()
        if f:
            f.seek(0)
            if f.write(wav_head(PIECE * 4 * PIECES)) != 44: raise OSError("WAV 머리말을 고쳐 쓰지 못했어요")
        done = True
    finally:
        if f: f.close()
        if path and not done: remove_quiet(path)
    keep = [b for lv, b in top if lv > thresh]
    if len(keep) < 2: keep = [b for lv, b in top[:2]]
    return keep, loud / PIECES


# ---------- 특징: 12개 주파수 대역의 에너지 모양 ----------
BANDS = [300, 404, 545, 734, 990, 1334, 1797, 2422, 3264, 4399, 5929, 7500]   # 대역 가운데 주파수(Hz)
LENS = [max(8, int(2 * RATE / max(120, int(c * 0.35)))) for c in BANDS]      # 대역 폭에 맞춘 블록 길이
WINS = [array("f", [0.5 - 0.5 * math.cos(2 * math.pi * (i + 0.5) / L) for i in range(L)]) for L in LENS]
KS = [2 * math.cos(2 * math.pi * f / RATE) for f in BANDS]

def _band(x, k, L, w):              # 짧게 끊어 Goertzel 계산을 반복하고 평균 → 대역 에너지
    p = 0.0; nb = 0
    for s in range(0, len(x) - L + 1, L):
        s1 = 0.0; s2 = 0.0
        for i in range(L):
            s0 = x[s + i] * w[i] + k * s1 - s2; s2 = s1; s1 = s0
        p += s1 * s1 + s2 * s2 - k * s1 * s2; nb += 1
    return p / (nb * L * L)

def shape12(raw):                   # 0.1초 조각 하나 → 소리 크기와 상관없는 스펙트럼 모양 12개
    v = struct.unpack("<%di" % PIECE, raw)
    m = 0
    for t in v: m += t >> 16
    m /= PIECE
    x = array("f", [(t >> 16) - m for t in v])
    e = [max(_band(x, k, L, w), 0.0) for k, L, w in zip(KS, LENS, WINS)]; tot = sum(e) + 1e-9
    return [math.log(ei / tot + 1e-6) for ei in e]

def features3(pieces, active):      # 3초 특징 25개 = 조각들의 모양 평균 12 + 흔들림 12 + 소리 난 비율 1
    fs = [shape12(b) for b in pieces]; n = len(fs)
    mu = [sum(f[i] for f in fs) / n for i in range(12)]
    sd = [math.sqrt(sum((f[i] - mu[i]) ** 2 for f in fs) / n) for i in range(12)]
    return array("f", mu + sd + [active])


def features3_timed(pieces, active):  # 특징 계산 시간과 남은 메모리를 함께 알려 줘요 (⓪ 부품 확인용)
    gc.collect(); t0 = time.ticks_ms()
    r = features3(pieces, active)
    ms = time.ticks_diff(time.ticks_ms(), t0); gc.collect()
    return r, ms, gc.mem_free()


# ---------- 예시와 k-NN ----------
EXAMPLES = "/sd/eco/examples.csv"
MAX_EXAMPLES = 300                  # 예시 수 상한 (피코 메모리 때문)
EX_HEADER = ",".join("f%d" % i for i in range(25)) + ",label"

def save_example(feat, label):
    log("examples.csv", EX_HEADER, ",".join("%.4f" % v for v in feat) + "," + label)

def knn_load(k):                    # 예시를 읽어, 가까운 예시 k개의 라벨별 표를 세는 함수를 돌려줘요
    rows = []; cnt = {}
    with open(EXAMPLES) as f:
        for ln in f:
            p = ln.strip().split(",")
            if len(p) == 26 and p[25] != "label":
                rows.append((array("f", [float(v) for v in p[:25]]), p[25]))
                cnt[p[25]] = cnt.get(p[25], 0) + 1
    if len(rows) > MAX_EXAMPLES:
        raise ValueError("예시가 %d개예요. 피코 메모리를 생각해 %d개 이하로 줄이세요" % (len(rows), MAX_EXAMPLES))
    if len(cnt) < 2 or min(cnt.values()) < 3 or len(rows) < k:
        raise ValueError("예시가 부족해요 %s. 두 종류 이상, 종류마다 3개 이상, 모두 %d개 이상 모으세요" % (cnt, k))
    lo = array("f", [min(r[0][i] for r in rows) for i in range(25)])
    sc = array("f", [1 / (max(r[0][i] for r in rows) - lo[i] + 1e-9) for i in range(25)])
    for f, _ in rows:
        for i in range(25): f[i] = (f[i] - lo[i]) * sc[i]
    gc.collect()
    def votes(feat):                # {라벨: 표 수}
        q = [(feat[i] - lo[i]) * sc[i] for i in range(25)]
        best = []
        for f, lab in rows:
            d = 0.0
            for i in range(25):
                t = f[i] - q[i]; d += t * t
            if len(best) < k or d < best[-1][0]:
                best.append((d, lab)); best.sort(key=lambda t: t[0])
                if len(best) > k: best.pop()
        v = {}
        for _, lab in best: v[lab] = v.get(lab, 0) + 1
        return v
    return votes, cnt


# ---------- MP3 말하기 (Grove MP3 v4.0 · UART0) ----------
_uart = [None]
def mp3_open(volume=22):            # 모듈이 켜질 시간을 1초 기다려요. 쉴드 전원 스위치는 5V여야 해요
    _uart[0] = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
    time.sleep(1.0)
    _uart[0].write(("AT+VOL=%d\r\n" % volume).encode()); time.sleep(0.1)

def say(audio, track, seconds=2.5): # track번 MP3를 틀고, 말하는 동안에는 귀를 닫아요(자기 목소리를 다시 듣지 않게)
    if _uart[0] is None: return
    _uart[0].write(("AT+PLAY=sd0,%d\r\n" % track).encode())
    drain(audio, seconds)


# ---------- 구글 시트로 보내기 (선택) ----------
def wifi_connect():                 # wifi_config.py의 이름·비밀번호로 연결 (교재 1장과 같은 파일)
    import network
    try:
        from wifi_config import WIFI_SSID, WIFI_PASSWORD
    except ImportError:
        print("wifi_config.py가 없어요. 교재 1장처럼 먼저 저장하세요"); return False
    w = network.WLAN(network.STA_IF); w.active(True)
    if not w.isconnected():
        w.connect(WIFI_SSID, WIFI_PASSWORD)
        for _ in range(40):
            if w.isconnected(): break
            time.sleep(0.5)
    return w.isconnected()

def _https_get(url):                # 교재 6장과 같은 방식 (설치할 것 없음)
    import socket, ssl
    host, _, path = url[8:].partition("/")
    gc.collect(); s = socket.socket()
    try:
        s.connect(socket.getaddrinfo(host, 443)[0][-1])
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT); ctx.verify_mode = ssl.CERT_NONE
        s = ctx.wrap_socket(s, server_hostname=host)
        s.write(("GET /%s HTTP/1.0\r\nHost: %s\r\nConnection: close\r\n\r\n" % (path, host)).encode())
        buf = b""
        while True:
            c = s.read(512)
            if not c: break
            buf += c
        return buf
    finally:
        s.close()

def _q(s):                          # 주소에 넣을 수 있게 바꾸기 (한글·공백 포함)
    out = ""
    for b in str(s).encode():
        if (48 <= b <= 57) or (65 <= b <= 90) or (97 <= b <= 122) or b in b"-_.~":
            out += chr(b)
        else:
            out += "%%%02X" % b
    return out

def sheet_send(url, **values):      # 구글 시트 웹 앱으로 한 줄 보내기. 실패해도 관측은 계속해요
    try:
        resp = _https_get(url + "?" + "&".join("%s=%s" % (k, _q(v)) for k, v in values.items()))
        head = resp.split(b"\r\n\r\n", 1)[0]
        if b" 302 " in head or b" 301 " in head:          # 구글이 다른 주소로 넘기면 따라가기
            for line in head.split(b"\r\n"):
                if line.lower().startswith(b"location:"):
                    _https_get(line.split(b":", 1)[1].strip().decode()); break
        return True
    except Exception as e:
        print("시트 전송 실패(관측은 계속):", e)
        return False


# ---------- 마무리 ----------
def finish(audio, mounted_here=True):  # 마이크 정리 → LED 끄기 → SD 분리. 하나가 실패해도 나머지는 꼭 해요
    try:
        if audio is not None: audio.deinit()
    finally:
        try:
            led((0, 0, 0))
        finally:
            if sd_mounted(): vfs.umount("/sd")     # 이전 실행에서 연결된 채 남아 있어도 분리해요
    print("안전하게 끝났어요. 이제 전원을 뽑아도 됩니다.")
