# 물까치 찾기 ⓪ — 부품 확인과 시계 맞추기
# Thonny로 PC에 연결한 상태에서 실행하세요. ①~⑥이 모두 OK면 다음 단계로 갑니다(버튼을 사용하지 않으면 ⑤는 건너뛰어요).
# ⑦은 이 피코가 3초를 판단하는 데 걸리는 시간과 남은 메모리를 알려 줘요(기록해 두세요).
# 먼저 sdcard.py와 eco_lib.py가 피코에 저장되어 있어야 해요.
import eco_lib as E
import os, time

SET_CLOCK = True    # True면 컴퓨터 시각을 시계(DS3231)에 옮겨 적어요. 한 번 맞춘 뒤에는 False로 바꿔도 돼요

def main():
    E.stop_reset(); mounted = False; audio = None
    try:
        # ① SD 카드
        try:
            mounted = E.sd_open()
            with open("/sd/eco/test.txt", "w") as f: f.write("hello eco")
            with open("/sd/eco/test.txt") as f: ok = f.read() == "hello eco"
            os.remove("/sd/eco/test.txt")
            st = os.statvfs("/sd")
            if ok: print("① SD 카드   OK  남은 공간 %.0f MB" % (st[1] * st[3] / 1048576))
            else:  print("① SD 카드   쓰고 읽은 내용이 달라요 → 카드를 다시 꽂아 보세요")
        except Exception as e:
            print("① SD 카드   실패:", e, "→ SPI0 헤더 6가닥, 카드 삽입, FAT32 포맷을 확인하세요")

        # ② 시계 (전원만 연결해 현장에 둘 때 필요해요. 없으면 피코 시각을 사용해요)
        try:
            if not E.HAS_CLOCK:
                print("② 시계      OK  %s  ← 시계(DS3231) 없이 피코 시각을 사용해요" % E.when())
                print("            시계는 현장 설치에만 필요해요. 꽂았다면 I2C0 포트와 Grove–STEMMA QT 케이블을 확인하세요")
            else:
                if SET_CLOCK: E.clock_set_from_pico()
                print("② 시계      OK  %s  ← 지금 시각과 같은지 확인하세요" % E.when())
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

        # ④ MP3
        E.mp3_open()
        print("④ MP3       1번 파일을 틀어요. '물까치인가 봐요'가 들리면 OK")
        E.say(audio, 1, 3)

        # ⑤ 버튼
        if not E.USE_BUTTON:
            print("⑤ 버튼      건너뛰어요 (USE_BUTTON = False). 끝낼 때는 Thonny의 정지 버튼을 눌러요")
        else:
            print("⑤ 버튼      5초 안에 버튼을 한 번 누르세요")
            t0 = time.ticks_ms(); pressed = False
            while time.ticks_diff(time.ticks_ms(), t0) < 5000:
                if E.btn.value() == 1: pressed = True; break
                time.sleep(0.01)
            print("⑤ 버튼      OK" if pressed else "⑤ 버튼      눌림을 못 느꼈어요 → D18 포트를 확인하세요. 버튼이 없으면 eco_lib.py의 USE_BUTTON을 False로 바꿔요")

        # ⑥ LED
        for c in ((40, 0, 0), (0, 40, 0), (0, 0, 40)):
            E.led(c); time.sleep(0.4)
        print("⑥ LED       빨강 → 초록 → 파랑으로 켜졌다면 OK")

        # ⑦ 판단 속도·메모리 (3초 듣고 특징 계산)
        print("⑦ 판단 속도 3초 동안 아무 소리나 들려주세요")
        pieces, active = E.listen3(audio, quiet * 2 + 20)
        feat, ms, free = E.features3_timed(pieces, active)
        print("⑦ 판단 속도 특징 계산 %d ms · 남은 메모리 %d KB · 조각 %d개" % (ms, free // 1024, len(pieces)))
    finally:
        E.finish(audio, mounted)

try:
    main()
except KeyboardInterrupt:                   # Thonny의 정지 버튼으로 끝내도 오류 없이 끝나요
    pass
