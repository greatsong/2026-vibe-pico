# 생태 관측기 ③ — AI에게 가르칠 예시 모으기 (Thonny로 PC에 연결한 상태에서만 실행)
# 숫자를 입력한 뒤 3초 안에 그 소리를 들려주면, 가장 또렷한 0.1초 조각 3개의 특징을 저장해요.
# 소리 파일이 아니라 숫자 8개씩만 저장합니다.
# 새소리는 컴퓨터·휴대폰 스피커로 새소리 녹음을 틀어 모아요. 말소리는 녹음에 동의한 내 목소리로만 모아요.
import eco_lib as E

LABELS = {"1": "새소리", "2": "말소리", "3": "배경", "4": "기타"}   # 기타 = 차·문·발걸음 같은 생활 소리
PIECES = 3          # 한 번에 저장할 조각 수

def counts():
    c = {}
    try:
        with open(E.EXAMPLES) as f:
            for ln in f:
                p = ln.strip().split(",")
                if len(p) == 9 and p[8] != "label": c[p[8]] = c.get(p[8], 0) + 1
    except OSError:
        pass
    return c

def main():
    E.stop_reset(); mounted = False; audio = None
    try:
        mounted = E.sd_open(); E.eco_dir()
        audio = E.mic_open(); E.drain(audio, 1)
        print("\n=== 예시 모으기 ===")
        for k, v in LABELS.items(): print("  %s = %s" % (k, v))
        print("  s = 끝내기")
        while True:
            cmd = input("라벨> ").strip()
            if cmd == "s": break
            name = LABELS.get(cmd)
            if not name:
                print("  ↑ 1~4 또는 s"); continue
            print("  ▶ '%s' 소리를 지금 들려주세요… (3초)" % name)
            E.led((40, 25, 0))
            for x in E.best_pieces(audio, 3, PIECES):
                E.log("examples.csv", E.EX_HEADER, ",".join("%.3f" % v for v in E.features(x)) + "," + name)
            E.led((0, 40, 0)); E.drain(audio, 0.2); E.led((0, 0, 0))
            print("  저장! 지금까지 %s" % counts())
    finally:
        E.finish(audio, mounted)

main()
