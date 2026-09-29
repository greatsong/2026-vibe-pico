# 생태 관측기 ④ — AI 녹음기: k-NN이 '새소리'라고 판단할 때만 녹음해요
# 소리가 기준보다 크면 0.1초 조각 3개를 읽어 조각마다 판단하고 다수결로 정해요.
# '새소리'가 아니면 소리를 저장하지 않고 기록에 '건너뜀'만 남겨요.
# 분류기는 틀릴 수 있어요. 사람이 대화하는 곳에는 설치하지 않습니다.
import eco_lib as E

K_NN = 5            # 가까운 예시 몇 개에게 물어볼까 (홀수)
VOTE = 3            # 조각 몇 개로 다수결을 할까
CONF = 0.6          # '새소리' 표가 이 비율 이상일 때만 저장
K = 2.0             # 판단을 시작할 크기 = 조용할 때 크기 × K + 20
LENGTH = 5
COOLDOWN = 3

def main():
    if not (isinstance(K_NN, int) and K_NN >= 1 and K_NN % 2 == 1 and isinstance(VOTE, int) and VOTE >= 1
            and 0 <= CONF <= 1 and isinstance(LENGTH, int) and LENGTH >= 1 and COOLDOWN >= 0):
        raise ValueError("K_NN은 홀수, VOTE와 LENGTH는 1 이상의 정수, CONF는 0~1 사이여야 해요")
    E.stop_reset(); mounted = False; audio = None
    try:
        mounted = E.sd_open(); E.eco_dir()
        predict, cnt = E.knn_load(K_NN)
        print("예시를 불러왔어요:", cnt)
        audio = E.mic_open()
        base = E.baseline(audio); thresh = base * K + 20
        print("기준 %.0f. 새소리로 판단하면 %d초 녹음해요. 끝내려면 버튼." % (thresh, LENGTH))
        saved = 0; skipped = 0; E.led((0, 0, 3))
        while not E.want_stop():
            lv = E.level(audio)
            if lv <= thresh: continue
            trig = bytes(E.small)                         # 기준을 넘은 조각
            pieces, blobs = E.grab_many(audio, VOTE)
            name, share = E.vote(predict, pieces)
            now = E.stamp()
            if name == "새소리" and share >= CONF:
                fn = now + "_ai.wav"; E.led((40, 0, 0))
                E.record(audio, "/sd/eco/" + fn, LENGTH, prefix=[trig] + blobs)
                saved += 1
                E.log("log_ai.csv", "time,decision,label,share,level,file", "%s,저장,%s,%.2f,%.0f,%s" % (now, name, share, lv, fn))
                print("저장 %d: %s (표 %d%%)" % (saved, fn, share * 100))
            else:
                skipped += 1                              # 소리는 저장하지 않아요
                E.log("log_ai.csv", "time,decision,label,share,level,file", "%s,건너뜀,%s,%.2f,%.0f," % (now, name, share, lv))
                E.led((20, 0, 20) if name == "말소리" else (0, 20, 0))
            E.drain(audio, COOLDOWN); E.led((0, 0, 3))
        print("저장 %d번, 건너뜀 %d번" % (saved, skipped))
    finally:
        E.finish(audio, mounted)

main()
