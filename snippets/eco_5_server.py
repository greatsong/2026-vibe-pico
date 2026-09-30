# 물까치 찾기 ⑤ — 라즈베리파이에게 물어보기 (피코 k-NN + BirdNET)
# 소리가 나면 피코가 3초를 듣고 k-NN 표를 센 뒤, 그 WAV를 Wi-Fi로 라즈베리파이 5의 서버(bird_server.py)에 보내요.
# BirdNET이 새 이름과 신뢰도를 돌려주면, 그 새의 MP3를 틀고 server.csv에 피코 표 수와 함께 기록해요.
# server.csv로 '피코만 / BirdNET만 / 피코가 거른 뒤 BirdNET' 세 방식을 나중에 비교할 수 있어요.
# 서버가 응답하지 않으면 피코 판단만으로 계속 관측해요. Thonny의 정지 버튼을 누르면 안전하게 끝나요(USE_BUTTON = True면 버튼 D18로도 끝나요).
# 준비: Pi 5에서 bird_server.py 실행 → 화면에 나온 주소를 아래 SERVER에 적기, 피코에 wifi_config.py 저장
import eco_lib as E
import os, socket, time

SERVER = "http://192.168.0.23:8000"   # ← bird_server.py가 알려 준 주소로 바꾸세요
TARGET = "물까치"
K_NN = 9
MIN_VOTES = 3       # 피코 혼자 판단할 때의 기준(서버가 없을 때, SEND_ALL=False일 때 사용)
SEND_ALL = True     # True: 소리가 나면 모두 BirdNET에게 물어요. False: 피코가 MIN_VOTES 이상일 때만 물어요(보내는 횟수↓ 놓침↑)
K = 2.0
COOLDOWN = 2
TIMEOUT = 10        # 서버 응답을 기다리는 최대 시간(초)
TRACKS = {"물까치": 1, "까치": 2, "직박구리": 3, "참새": 4, "멧비둘기": 5, "박새": 6, "큰부리까마귀": 7}   # MP3 번호

def _send_all(s, data):             # 보낼 데이터를 끝까지 보내요
    mv = memoryview(data)
    while mv:
        n = s.send(mv)
        mv = mv[n:]

def _parse(server):                 # "http://192.168.0.23:8000" → ("192.168.0.23", 8000)
    if not server.startswith("http://"): raise ValueError("SERVER는 http://로 시작해야 해요")
    host, _, port = server[7:].rstrip("/").partition(":")
    return host, int(port or 80)

def _request(head, path=None):      # HTTP 요청을 보내고 (상태 코드, 본문 글자)를 돌려줘요
    host, port = _parse(SERVER)
    s = socket.socket()
    try:
        s.settimeout(TIMEOUT)
        s.connect(socket.getaddrinfo(host, port)[0][-1])
        _send_all(s, head.encode())
        if path:
            buf = bytearray(2048)
            with open(path, "rb") as f:
                while True:
                    n = f.readinto(buf)
                    if not n: break
                    _send_all(s, memoryview(buf)[:n])
        resp = b""
        while True:
            c = s.recv(512)
            if not c: break
            resp += c
    finally:
        s.close()
    first, _, rest = resp.partition(b"\r\n")
    body = rest.partition(b"\r\n\r\n")[2]
    code = int(first.split()[1]) if len(first.split()) > 1 else 0
    return code, body.decode().strip()

def server_ok():                    # 시작할 때 서버에 닿는지 확인
    host, port = _parse(SERVER)
    try:
        code, text = _request("GET /ping HTTP/1.0\r\nHost: %s\r\n\r\n" % host)
        return code == 200 and text == "ok"
    except Exception as e:
        print("서버 확인 실패:", e)
        return False

def ask(path, name):                # WAV를 보내고 (판정, 가장 높은 새, 신뢰도)를 받아요. 실패하면 None
    host, port = _parse(SERVER)
    size = os.stat(path)[6]
    head = ("POST /judge HTTP/1.0\r\nHost: %s\r\nContent-Type: audio/wav\r\nX-File: %s\r\n"
            "Content-Length: %d\r\n\r\n" % (host, name, size))
    try:
        code, text = _request(head, path)
        if code != 200: raise OSError("서버가 %d로 답했어요" % code)
        decision, best, conf = text.split(" ")
        return decision, best, float(conf)
    except Exception as e:
        print("  서버에 묻지 못했어요:", e)
        return None

def check(audio, tmp, t, n, online):   # 후보를 저장하고, 서버에 묻고, 답에 따라 말해요
    name = E.stamp() + ("_cand.wav" if n >= MIN_VOTES else "_check.wav")
    path = "/sd/eco/" + name
    os.rename(tmp, path)
    bird, best, conf = "서버 없음", "없음", 0.0
    if online:
        E.led((20, 0, 30))                                         # 보라 = 라즈베리파이에게 묻는 중
        r = ask(path, name)
        if r: bird, best, conf = r
        else: bird = "서버 오류"
    E.log("server.csv", "time,pico_votes,birdnet,best,confidence,file", "%s,%d,%s,%s,%.2f,%s" % (t, n, bird, best, conf, name))
    if bird in TRACKS:                                             # BirdNET이 아는 새라고 답했어요
        print("%s  %s인가 봐요! (피코 %d표 · BirdNET %.2f) → %s" % (t, bird, n, conf, name))
        E.led((0, 40, 20) if bird == TARGET else (30, 30, 30))
        E.say(audio, TRACKS[bird])
    elif bird in ("서버 없음", "서버 오류") and n >= MIN_VOTES:       # 서버가 없으면 피코 판단으로
        print("%s  물까치 후보 (피코 %d표 · %s) → %s" % (t, n, bird, name))
        E.led((0, 40, 20), n)
        E.say(audio, TRACKS[TARGET])
    else:
        print("%s  BirdNET: %s (가장 높은 새 %s %.2f) · 피코 %d표" % (t, bird, best, conf, n))
        E.remove_quiet(path)                                       # 새가 아니면 소리는 남기지 않아요

def main():
    if not (isinstance(MIN_VOTES, int) and 1 <= MIN_VOTES <= K_NN):
        raise ValueError("MIN_VOTES는 1 이상 K_NN 이하의 정수여야 해요")
    E.stop_reset(); mounted = False; audio = None
    try:
        mounted = E.sd_open()
        E.when()                                                   # 시각을 알 수 없으면 듣기 전에 바로 알려요
        votes, cnt = E.knn_load(K_NN)
        if TARGET not in cnt: raise ValueError("예시에 '%s'가 없어요. ① 예시 모으기를 먼저 하세요" % TARGET)
        print("예시를 불러왔어요:", cnt)
        online = E.wifi_connect() and server_ok()
        print("라즈베리파이 서버", "연결됨" if online else "연결 안 됨 → 피코 판단만 해요 (SERVER 주소와 Wi-Fi를 확인하세요)")
        E.mp3_open()
        audio = E.mic_open()
        quiet = E.baseline(audio); thresh = quiet * K + 20
        print("듣기 시작! (조용할 때 %.0f → 기준 %.0f) 끝내려면 %s." % (quiet, thresh, "버튼" if E.USE_BUTTON else "Thonny의 정지 버튼"))
        tmp = "/sd/eco/tmp.wav"; E.remove_quiet(tmp)
        E.led((0, 0, 3))
        while not E.want_stop():
            if E.level(audio) <= thresh: continue
            E.led((30, 20, 0))                                     # 노랑 = 듣는 중
            try:
                pieces, active = E.listen3(audio, thresh, tmp, E.small)
                E.led((0, 0, 20))                                  # 파랑 = 피코가 생각 중
                v = votes(E.features3(pieces, active)); n = v.get(TARGET, 0); t = E.when()
                if n >= MIN_VOTES or SEND_ALL:
                    check(audio, tmp, t, n, online)
                else:
                    print("%s  아니에요 (물까치 %d표)" % (t, n))
            finally:
                E.remove_quiet(tmp)
            E.drain(audio, COOLDOWN); E.led((0, 0, 3))
    finally:
        E.finish(audio, mounted)

try:
    main()
except KeyboardInterrupt:                                          # Thonny의 정지 버튼으로 끝내도 오류 없이 끝나요
    pass
except Exception as e:
    print("문제가 생겼어요:", e)
    E.error_blink(); E.led((40, 0, 0))
