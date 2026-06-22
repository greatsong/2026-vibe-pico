# 🔌 피코 바이브 코딩 연수 · 코드 & 가이드

라즈베리파이 **피코 2 WH** + 그로브 쉴드로 배우는 피지컬 컴퓨팅 연수 자료입니다.
설치·조립부터 와이파이·LED·날씨 API·가스센서 대시보드까지, 모든 MicroPython 코드를
**복사해 바로 실행**할 수 있게 모은 단일 페이지(연수생 배포용)입니다.

## 🌐 웹 페이지

👉 **https://greatsong.github.io/2026-vibe-pico/**

- **Chapter 0 — 준비하기**: Thonny 설치 · 하드웨어 조립 · 펌웨어 설치 · 첫 코드
- **Chapter 1 — 와이파이 센서 대시보드**: 신호 세기(RSSI) 실시간 웹 대시보드
- **Chapter 2 — LED 10개 다루기**: WS2813 (timing 인자 필수)
- **Chapter 3 — 날씨 비 예보 대시보드**: Open-Meteo 강수확률 → 10 LED (바이브코딩)
- **Chapter 4 — MQ-2 가스센서 대시보드**: ADC · 이동평균 · 임계값 · 다크 테마
- **Chapter 5 — 자유 프로젝트**: 조합 아이디어 + 프롬프트 틀

각 코드/프롬프트 블록의 **복사** 버튼으로 바로 가져다 쓸 수 있습니다.

### 하드웨어 연결
- LED(WS2813) → 그로브 **D16** (= GP16)
- MQ-2 가스센서 → 그로브 **A0** (= GP26 / ADC0)
- LED 생성 시 **`timing=(280, 515, 515, 745)`** 필수 (없으면 색 깨짐)

## 📁 구성

| 경로 | 설명 |
|---|---|
| `index.html` | 완성된 단일 페이지 (GitHub Pages가 그대로 서빙) |
| `build_site.py` | 페이지 생성 스크립트 (콘텐츠 정의 + 렌더러, `snippets/` 읽음) |
| `snippets/*.py` | 복사해 바로 실행되는 완결형 MicroPython 코드 (검증본) |
| `firmware/*.uf2` | Pico 2 W용 MicroPython 펌웨어 |

## 🛠 로컬에서 보기 / 다시 빌드

```bash
python3 build_site.py        # snippets + 콘텐츠 → index.html 재생성
python3 -m http.server 8000  # http://localhost:8000 접속
```

---
연수·수업 자료로 자유롭게 활용할 수 있습니다.
