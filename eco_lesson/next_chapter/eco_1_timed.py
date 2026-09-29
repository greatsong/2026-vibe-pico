# 생태 관측기 ① — 정기 녹음기: 정해진 간격마다 무조건 녹음해요
# EVERY와 LENGTH를 같게(예: 10과 10) 두면 쉬지 않고 10초씩 이어서 녹음해요.
# 이어 녹음한 파일은 ⑤ PC 분석에서 규칙 녹음기와 AI 녹음기를 같은 소리로 공정하게 비교하는 데 써요.
# 버튼(D18)을 누르면 파일을 닫고 안전하게 끝납니다. 끝났다는 글이 나온 뒤에 전원을 뽑으세요.
import eco_lib as E
import time

EVERY = 60          # 몇 초마다 녹음을 시작할까
LENGTH = 10         # 한 번에 몇 초 녹음할까 (EVERY보다 크면 안 돼요)

def main():
    if not (isinstance(EVERY, int) and isinstance(LENGTH, int) and 1 <= LENGTH <= EVERY):
        raise ValueError("EVERY와 LENGTH는 1 이상의 정수이고, LENGTH는 EVERY보다 크면 안 돼요")
    E.stop_reset(); mounted = False; audio = None
    try:
        mounted = E.sd_open(); E.eco_dir()
        audio = E.mic_open(); E.drain(audio, 1)           # 켜진 직후 튀는 소리는 버려요
        print("정기 녹음 시작: %d초마다 %d초씩. 끝내려면 버튼을 누르세요." % (EVERY, LENGTH))
        count = 0
        while not E.want_stop():
            t0 = time.ticks_ms(); name = E.stamp() + "_timed.wav"
            E.led((40, 0, 0))                             # 빨강 = 녹음 중
            got = E.record(audio, "/sd/eco/" + name, LENGTH)
            E.led((0, 0, 3))                              # 희미한 파랑 = 기다리는 중
            count += 1
            E.log("log_timed.csv", "file,seconds", "%s,%.2f" % (name, got / (E.RATE * 4)))
            print("%d번째 저장: %s" % (count, name))
            left = EVERY - time.ticks_diff(time.ticks_ms(), t0) / 1000
            if left > 0: E.drain(audio, left)
    finally:
        E.finish(audio, mounted)

main()
