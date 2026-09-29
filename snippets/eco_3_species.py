# 물까치 찾기 ③ — 여러 새 구분하기 (2단계 · 이 새는 누구일까)
# ① 예시 모으기의 LABELS에 새 이름을 더 넣고(예: "까치", "직박구리") 새마다 예시를 모은 뒤 실행하세요.
# 가까운 예시 K_NN개 가운데 가장 많은 표를 받은 새가 MIN_VOTES표 이상이면 그 새 이름을 MP3로 말해요.
import eco_lib as E
import os

BIRDS = {"물까치": 1, "까치": 2, "직박구리": 3}   # 새 이름 → MP3 파일 번호 (0001.mp3 = "물까치인가 봐요", 0002.mp3 = "까치인가 봐요" …)
K_NN = 9
MIN_VOTES = 4       # 가장 많은 표가 이보다 적으면 "잘 모르겠어요"로 넘어가요
K = 2.0
COOLDOWN = 2

def main():
    E.stop_reset(); mounted = False; audio = None
    try:
        mounted = E.sd_open()
        votes, cnt = E.knn_load(K_NN)
        missing = [b for b in BIRDS if b not in cnt]
        if missing: print("주의: 예시가 없는 새 %s → 이 새는 알아맞힐 수 없어요" % missing)
        print("예시:", cnt)
        E.mp3_open()
        audio = E.mic_open()
        quiet = E.baseline(audio); thresh = quiet * K + 20
        print("듣기 시작! 끝내려면 버튼.")
        tmp = "/sd/eco/tmp.wav"; E.remove_quiet(tmp)
        E.led((0, 0, 3))
        while not E.want_stop():
            if E.level(audio) <= thresh: continue
            E.led((30, 20, 0))
            try:
                pieces, active = E.listen3(audio, thresh, tmp, E.small)
                E.led((0, 0, 20))
                v = votes(E.features3(pieces, active))
                best = max(v, key=v.get); n = v[best]; t = E.when()
                if best in BIRDS and n >= MIN_VOTES:
                    name = "%s_%s.wav" % (E.stamp(), best)
                    os.rename(tmp, "/sd/eco/" + name)
                    E.log("species.csv", "time,label,votes,file", "%s,%s,%d,%s" % (t, best, n, name))
                    E.led((0, 40, 20), n)
                    print("%s  %s인가 봐요! (%d/%d표)" % (t, best, n, K_NN))
                    E.say(audio, BIRDS[best])
                else:
                    print("%s  잘 모르겠어요 (%s %d표)" % (t, best, n))
            finally:
                E.remove_quiet(tmp)
            E.drain(audio, COOLDOWN); E.led((0, 0, 3))
    finally:
        E.finish(audio, mounted)

try:
    main()
except Exception as e:
    print("문제가 생겼어요:", e)
    E.error_blink(); E.led((40, 0, 0))
