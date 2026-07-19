# 🔌 피코 바이브 코딩 연수 · 코드 & 가이드

라즈베리파이 **피코 2 WH** + 그로브 쉴드로 배우는 피지컬 컴퓨팅 연수 자료입니다.
설치·조립부터 와이파이·LED·가스센서·날씨 API 대시보드까지, 모든 MicroPython 코드를
**복사해 바로 실행**할 수 있게 정리한 웹 교재(학생 배포용)입니다.
허브 페이지에서 챕터를 고르면 챕터별 페이지로 이동하고, 각 페이지 하단의
이전/다음 버튼으로 순서대로 넘겨 볼 수 있습니다.

## 🌐 웹 페이지

👉 **https://greatsong.github.io/2026-vibe-pico/** (허브 — 챕터 목차)
👉 **https://greatsong.github.io/2026-vibe-pico/teacher/** (강사용 — 강사노트 포함)

- **Chapter 0 — 준비하기** (`ch0.html`): Thonny 설치 · 하드웨어 조립 · 펌웨어 설치 · 첫 코드
- **Chapter 1 — 와이파이 사각지대 찾기** (`ch1.html`): 신호 세기(RSSI) 실시간 웹 대시보드 · 사각지대 탐색
- **Chapter 2 — LED로 내 감정 표현하기** (`ch2.html`): WS2813 (timing 인자 필수) · 감정 무드등
- **Chapter 3 — 우리반 공기질 대시보드 (웹)** (`ch3.html`): MQ-2 · ADC · 이동평균 · 임계값 · 다크 테마
- **Chapter 4 — 우리반 공기질 실시간 확인 (LED)** (`ch4.html`): 센서값 → 10칸 LED 게이지 (물리 출력)
- **Chapter 5 — 강수확률 물리 대시보드 (API×LED)** (`ch5.html`): Open-Meteo 강수확률 → 10 LED + 웹 (바이브코딩)
- **Chapter 6 — 자유 프로젝트** (`ch6.html`): 조합 아이디어 + 프롬프트 틀
- **부록 A — 오픈 API 예제 모음** (`apx.html`): 과목별 10가지 API를 피코 10칸 LED로 (미세먼지·지진·ISS·낮길이·우주날씨·분자량·생물·천문사진·에너지·CO₂) · 갤러리는 날씨까지 11종
- **부록 B — 심화: 센서 데이터를 구글 시트에 쌓기** (`apxb.html`): Apps Script 웹앱 + 피코(무설치 socket+ssl)로 데이터 로깅
- **부록 C — 용어 사전** (`apxc.html`): 프롬프트·본문에서 쓰는 용어를 한 줄씩 정리 (프롬프트에는 코드 대신 정확한 낱말을 쓴다는 원칙)

각 코드/프롬프트 블록의 **복사** 버튼으로 바로 가져다 쓸 수 있습니다.

### 🛰️ 오픈 API 라이브 대시보드 (브라우저)

👉 **https://greatsong.github.io/2026-vibe-pico/dashboards/**

피코 없이 브라우저에서 공개 데이터를 직접 받아 그려 보는 탐구실(11종): 날씨·미세먼지·지진(세계지도)·ISS(실시간 지도)·일출몰·우주날씨·물질정보(2D/3D)·생물(지도·계절)·NASA(천문사진·소행성 애니메이션)·태양바람에너지·나라별 CO₂(세계지도·버블). 모두 무료(NASA만 키), CORS 허용 확인.

### 하드웨어 연결
- LED(WS2813 10칸) → 그로브 **D16** (= GP16) — 그로브 케이블
- MQ-2 가스센서(**핀헤더형 · 그로브 아님**) → 그로브 **A0** (= GP26 / ADC0) — **그로브 암 점퍼 케이블**: 노랑→AO · 빨강→VCC · 검정→GND (흰선·DO 미사용)
- INMP441 전방향 마이크(I2S · ML 확장판) → 헤더 핀 점퍼 6선: SCK→GP18 · WS→GP19 · SD→GP20 · L/R→GND · VDD→**3.3V(5V 금지)** · GND→GND
- LED 생성 시 **`timing=(280, 515, 515, 745)`** 필수 (없으면 색 깨짐)

## 📁 구성

| 경로 | 설명 |
|---|---|
| `index.html` | **허브 페이지 · 학생용** — 히어로 + 챕터 링크카드 목차 (GitHub Pages가 그대로 서빙) |
| `ch0.html` ~ `ch6.html` | 챕터별 페이지 (하단에 이전/다음 이동 버튼) |
| `apx.html` / `apxb.html` / `apxc.html` | 부록 A(오픈 API) / 부록 B(구글 시트) / 부록 C(용어 사전) |
| `teacher/` | **강사용 미러** — 허브(`teacher/index.html`) + 챕터 페이지, 강사노트(진행 멘트·발문·예상 오류) 포함 |
| `build_site.py` | 페이지 생성 스크립트 (콘텐츠 정의 + 렌더러 + 디자인 TEMPLATE, `snippets/` 읽음) |
| `build_ml_site.py` | ML 확장판(`ml_site/`) 빌더 — build_site.py의 TEMPLATE·렌더러 재사용 |
| `build_dashboards.py` | 대시보드 11종 + 갤러리 + **`dashboards/lab.css`** 생성 (lab.css도 자동 생성물!) |
| `snippets/*.py` | 복사해 바로 실행되는 완결형 MicroPython 코드 (검증본) |
| `firmware/*.uf2` | Pico 2 W용 MicroPython 펌웨어 |

### 🎨 디자인

따뜻한 **크림/골드** 팔레트(2026-snui 웹 교재와 같은 계열). 디자인 토큰과 콜아웃
클래스(`tip/warn/mini/say/theory/ask/check/err` + `info/key`)는 `build_site.py`의
TEMPLATE `<style>` 한 곳에서 관리하고, 대시보드는 `build_dashboards.py`의 `LAB_CSS`에서
같은 토큰을 씁니다. **HTML은 전부 생성물 — 직접 수정 금지.**

### ✍️ 콘텐츠 아이템 타입 메모

- `prompt`(① 샘플 프롬프트) → `code`(② 완성 코드) → **`improve`(③ 프롬프트 개선)** 3박자
- `teacher`(kind: `say`/`ask`/`theory`/`err`) — 강사노트. `teacher/` 페이지에만 렌더됨

## 🛠 로컬에서 보기 / 다시 빌드

```bash
python3 build_site.py        # snippets + 콘텐츠 → 허브 + 챕터 페이지 전체 (학생용 + teacher/ 강사용)
python3 build_ml_site.py     # → ml_site/index.html (TEMPLATE 공유 — build_site.py 수정만으로 반영)
python3 build_dashboards.py  # → dashboards/*.html + lab.css
python3 -m http.server 8000  # http://localhost:8000 접속
```

---
연수·수업 자료로 자유롭게 활용할 수 있습니다.
