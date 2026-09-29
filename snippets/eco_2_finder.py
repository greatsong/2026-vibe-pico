# 물까치 찾기 ② — 물까치 탐지기 (1단계 · 물까치인가, 아닌가)
# 소리가 나면 3초를 듣고, 모아 둔 예시와 비교해요. 가까운 예시 K_NN개 가운데 물까치가 MIN_VOTES개 이상이면
# MP3로 "물까치인가 봐요"라고 말하고, 그 3초를 WAV로, 시각을 CSV로 남깁니다.
# 물까치가 아니면 소리는 지우고 시각과 판단만 기록해요.
# 버튼(D18)을 누르면 안전하게 끝납니다. main.py로 저장하면 전원만 연결해도 자동으로 시작해요.
import eco_lib as E
import os

TARGET = "물까치"
K_NN = 9            # 가까운 예시 몇 개에게 물어볼까
MIN_VOTES = 3       # 그중 몇 표 이상이면 물까치라고 할까 (↑ 오판이 줄고 놓치는 게 늘어요, ↓ 반대)
K = 2.0             # 듣기 시작하는 크기 = 조용할 때 크기 × K + 20
COOLDOWN = 2        # 한 번 판단한 뒤 몇 초 쉴까
SAY_TRACK = 1       # MP3 모듈 SD 카드의 0001.mp3 = "물까치인가 봐요"
SHEET_URL = ""      # 구글 시트 웹 앱 주소(.../exec). 비워 두면 보내지 않아요 (⑤ 참고)

def main():
    if not (isinstance(K_NN, int) and K_NN >= 1 and isinstance(MIN_VOTES, int) and 1 <= MIN_VOTES <= K_NN):
        raise ValueError("K_NN은 1 이상, MIN_VOTES는 1 이상 K_NN 이하의 정수여야 해요")
    E.stop_reset(); mounted = False; audio = None
    try:
        mounted = E.sd_open()
        votes, cnt = E.knn_load(K_NN)
        if TARGET not in cnt: raise ValueError("예시에 '%s'가 없어요. ① 예시 모으기를 먼저 하세요" % TARGET)
        print("예시를 불러왔어요:", cnt)
        online = bool(SHEET_URL) and E.wifi_connect()
        if SHEET_URL: print("구글 시트 전송", "켜짐" if online else "꺼짐(Wi-Fi 연결 실패)")
        E.mp3_open()
        audio = E.mic_open()
        quiet = E.baseline(audio); thresh = quiet * K + 20
        print("듣기 시작! (조용할 때 %.0f → 기준 %.0f) 끝내려면 버튼." % (quiet, thresh))
        tmp = "/sd/eco/tmp.wav"; E.remove_quiet(tmp)                # 지난번에 남은 임시 파일 정리
        found = 0; E.led((0, 0, 3))
        while not E.want_stop():
            if E.level(audio) <= thresh: continue
            E.led((30, 20, 0))                                     # 노랑 = 듣는 중
            try:
                pieces, active = E.listen3(audio, thresh, tmp, E.small)   # 소리를 감지한 조각부터 3초
                E.led((0, 0, 20))                                  # 파랑 = 생각 중
                v = votes(E.features3(pieces, active)); n = v.get(TARGET, 0)
                top = max(v, key=v.get); t = E.when()
                if n >= MIN_VOTES:
                    found += 1
                    name = E.stamp() + "_mulkkachi.wav"
                    os.rename(tmp, "/sd/eco/" + name)
                    E.log("found.csv", "time,votes,active,file", "%s,%d,%.2f,%s" % (t, n, active, name))
                    E.led((0, 40, 20), n)                          # 청록 = 물까치 후보 (켜진 칸 수 = 표 수)
                    print("%s  물까치인가 봐요! (%d/%d표) → %s" % (t, n, K_NN, name))
                    E.say(audio, SAY_TRACK)
                    if online: E.sheet_send(SHEET_URL, time=t, label=TARGET, votes=n)
                else:
                    print("%s  아니에요 (물까치 %d표, 가장 많은 표: %s)" % (t, n, top))
                E.log("decisions.csv", "time,target_votes,top_label,active", "%s,%d,%s,%.2f" % (t, n, top, active))
            finally:
                E.remove_quiet(tmp)                                # 물까치가 아니면 소리는 남기지 않아요
            E.drain(audio, COOLDOWN); E.led((0, 0, 3))
        print("물까치 후보 %d번 찾았어요." % found)
    finally:
        E.finish(audio, mounted)

try:
    main()
except Exception as e:                                             # 전원만 연결했을 때도 알 수 있게 빨간 불을 켜 둬요
    print("문제가 생겼어요:", e)
    E.error_blink(); E.led((40, 0, 0))
