# 🔌 피코 바이브 코딩 · 코드 & 프롬프트 모음

라즈베리파이 피코로 배우는 피지컬 컴퓨팅 교재의 **Chapter 1·2·3**에 쓰이는
모든 MicroPython 코드와 AI 샘플 프롬프트를 한곳에 모은 노션 스타일 웹 페이지입니다.

## 🌐 웹 페이지

👉 **https://greatsong.github.io/2026-vibe-pico/**

- **Chapter 1 — 피코와 첫 걸음**: 피코·MicroPython·Thonny 첫 만남부터 Wi-Fi 감도 웹 대시보드까지
- **Chapter 2 — 우리 집 와이파이 탐험대**: 와이파이 신호 세기(RSSI) 실시간 대시보드
- **Chapter 3 — 우리 교실 공기 지킴이**: 가스 센서 + LED 게이지 + 웹 대시보드

각 코드/프롬프트 블록의 **복사** 버튼으로 바로 가져다 쓸 수 있습니다.

## 📁 구성

| 파일 | 설명 |
|---|---|
| `index.html` | 완성된 단일 페이지 (GitHub Pages가 그대로 서빙) |
| `build_site.py` | 페이지 생성 스크립트 (Ch2·3 코드 인라인, Ch1은 원고에서 추출) |

## 🛠 로컬에서 보기

```bash
python3 -m http.server 8000
# http://localhost:8000 접속
```

---
수업 자료로 자유롭게 활용할 수 있습니다.
