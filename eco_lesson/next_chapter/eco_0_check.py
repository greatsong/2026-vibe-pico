# 생태 관측기 ⓪ — 부품 확인과 시계 맞추기
# Thonny로 PC에 연결한 상태에서 실행하세요. 다섯 줄이 모두 OK면 다음 단계로 갑니다.
# 먼저 eco_lib.py가 피코에 저장되어 있어야 해요.
import eco_lib as E
import os, time

SET_CLOCK = True    # True면 컴퓨터 시각을 시계(DS3231)에 옮겨 적어요. 한 번 맞춘 뒤에는 False로 바꿔도 돼요

def main():
    E.stop_reset(); mounted = False; audio = None
    try:
        # ① SD 카드
        try:
            mounted = E.sd_open(); E.eco_dir()
            with open("/sd/eco/test.txt", "w") as f: f.write("hello eco")
            with open("/sd/eco/test.txt") as f: ok = f.read() == "hello eco"
            os.remove("/sd/eco/test.txt")
            st = os.statvfs("/sd")
            if ok: print("① SD 카드   OK  남은 공간 %.0f MB" % (st[1] * st[3] / 1048576))
            else:  print("① SD 카드   쓰고 읽은 내용이 달라요 → 카드를 다시 꽂아 보세요")
        except Exception as e:
            print("① SD 카드   실패:", e, "→ SPI0 헤더 6가닥, 카드 삽입, FAT32 포맷을 확인하세요")

        # ② 시계
        try:
            if 0x68 not in E.i2c.scan():
                print("② 시계      찾지 못함 → I2C0 포트와 Grove–STEMMA QT 케이블을 확인하세요")
            else:
                if SET_CLOCK: E.clock_set_from_pico()
                print("② 시계      OK  %04d-%02d-%02d %02d:%02d:%02d  ← 지금 시각과 같은지 확인하세요" % E.clock_now())
        except Exception as e:
            print("② 시계      실패:", e)

        # ③ 마이크
        audio = E.mic_open()
        quiet = E.baseline(audio)
        print("③ 마이크    조용할 때 크기 %.0f. 이제 3초 동안 박수를 쳐 보세요" % quiet)
        t0 = time.ticks_ms(); loud = 0.0
        while time.ticks_diff(time.ticks_ms(), t0) < 3000:
            loud = max(loud, E.level(audio))
        if loud > quiet * 3 + 30: print("③ 마이크    OK  박수 크기 %.0f" % loud)
        else: print("③ 마이크    소리가 작아요(%.0f) → D20·A2 케이블과 L/R 선을 확인하세요" % loud)
        audio.deinit(); audio = None

        # ④ 버튼
        print("④ 버튼      5초 안에 버튼을 한 번 누르세요")
        t0 = time.ticks_ms(); pressed = False
        while time.ticks_diff(time.ticks_ms(), t0) < 5000:
            if E.btn.value() == 1: pressed = True; break
            time.sleep(0.01)
        print("④ 버튼      OK" if pressed else "④ 버튼      눌림을 못 느꼈어요 → D18 포트를 확인하세요")

        # ⑤ LED
        for c in ((40, 0, 0), (0, 40, 0), (0, 0, 40)):
            E.led(c); time.sleep(0.4)
        print("⑤ LED       빨강 → 초록 → 파랑으로 켜졌다면 OK")
    finally:
        E.finish(audio, mounted)

main()
