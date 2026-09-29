# 생태 관측기 ② — 규칙 녹음기: 소리가 기준보다 클 때만 녹음해요
# 기준을 어떻게 정할지가 이 단계의 탐구 주제예요.
# 너무 낮으면 바람·자동차 소리까지 저장하고, 너무 높으면 작은 새소리를 놓쳐요.
import eco_lib as E

K = 2.5             # 기준 = 조용할 때 크기 × K + 25  (놓치는 소리가 많으면 ↓, 쓸데없는 저장이 많으면 ↑)
LENGTH = 5          # 한 번에 몇 초 녹음할까
COOLDOWN = 3        # 저장한 뒤 몇 초 쉴까 (같은 소리를 여러 번 저장하지 않게)

def main():
    if not (isinstance(LENGTH, int) and LENGTH >= 1 and COOLDOWN >= 0 and K > 0):
        raise ValueError("LENGTH는 1 이상의 정수, COOLDOWN은 0 이상, K는 0보다 커야 해요")
    E.stop_reset(); mounted = False; audio = None
    try:
        mounted = E.sd_open(); E.eco_dir()
        audio = E.mic_open()
        print("조용히… 배경 소리 크기를 재는 중")
        base = E.baseline(audio); thresh = base * K + 25
        print("조용할 때 %.0f → 기준 %.0f. 기준보다 큰 소리가 나면 %d초 녹음해요. 끝내려면 버튼." % (base, thresh, LENGTH))
        count = 0; E.led((0, 0, 3))
        while not E.want_stop():
            lv = E.level(audio)
            if lv <= thresh: continue
            name = E.stamp() + "_rule.wav"
            E.led((40, 0, 0))
            E.record(audio, "/sd/eco/" + name, LENGTH, prefix=(E.small,))   # 기준을 넘은 조각부터 저장
            count += 1
            E.log("log_rule.csv", "file,level,thresh", "%s,%.0f,%.0f" % (name, lv, thresh))
            print("%d번째 저장: %s (크기 %.0f)" % (count, name, lv))
            E.led((0, 0, 3)); E.drain(audio, COOLDOWN)
    finally:
        E.finish(audio, mounted)

main()
