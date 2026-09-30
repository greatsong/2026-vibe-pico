# 물까치 찾기 ① — AI에게 가르칠 예시 모으기 (Thonny로 PC에 연결한 상태에서만 실행)
# 번호를 입력하면 피코가 3초 동안 들어요. 그 3초의 특징(숫자 25개)을 이름표와 함께 저장합니다.
# 소리 파일은 저장하지 않아요. 숫자만 남습니다.
# 물까치 소리는 우리 학교에서 직접 듣거나, 휴대폰으로 물까치 녹음을 틀어 모아요.
# 말소리는 녹음에 동의한 내 목소리로만 모아요.
import eco_lib as E

LABELS = {"1": "물까치", "2": "다른 새", "3": "말소리", "4": "배경", "5": "기타"}   # 기타 = 차·문·발걸음 같은 생활 소리

def counts():
    c = {}
    try:
        with open(E.EXAMPLES) as f:
            for ln in f:
                p = ln.strip().split(",")
                if len(p) == 26 and p[25] != "label": c[p[25]] = c.get(p[25], 0) + 1
    except OSError:
        pass
    return c

def main():
    E.stop_reset(); mounted = False; audio = None
    try:
        mounted = E.sd_open()
        audio = E.mic_open()
        quiet = E.baseline(audio); thresh = quiet * 2 + 20
        print("\n=== 예시 모으기 ===  (조용할 때 크기 %.0f)" % quiet)
        for k, v in LABELS.items(): print("  %s = %s" % (k, v))
        print("  s = 끝내기")
        while True:
            cmd = input("번호> ").strip()
            if cmd == "s": break
            name = LABELS.get(cmd)
            if not name:
                print("  ↑ 1~%d 또는 s" % len(LABELS)); continue
            if sum(counts().values()) >= E.MAX_EXAMPLES:
                print("  예시가 %d개로 가득 찼어요. 피코 메모리 때문에 더 저장하지 않아요" % E.MAX_EXAMPLES); continue
            E.drain(audio, 0.3)                                    # 엔터 소리가 섞이지 않게 잠깐 쉬어요
            print("  ▶ '%s' 소리를 들려주세요… (3초)" % name)
            E.led((40, 25, 0))
            pieces, active = E.listen3(audio, thresh)
            E.led((0, 0, 20)); print("  생각 중…")
            E.save_example(E.features3(pieces, active), name)
            E.led((0, 40, 0)); E.drain(audio, 0.3); E.led((0, 0, 0))
            print("  저장! 소리 난 비율 %d%% | 지금까지 %s" % (int(active * 100), counts()))
    finally:
        E.finish(audio, mounted)

try:
    main()
except KeyboardInterrupt:                   # Thonny의 정지 버튼으로 끝내도 오류 없이 끝나요
    pass
