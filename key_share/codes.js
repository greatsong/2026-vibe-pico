/* ============================================================
   코드 라이브러리 데이터
   ------------------------------------------------------------
   새 코드를 배포하려면: 아래 배열 맨 위에 한 칸 추가하고 git push.
     - n    : 코드 번호 (가장 큰 n 이 '최신 🆕' 으로 표시됨)
     - title: 제목
     - lang : 'python' | 'bash' | 'text' 등 (표시용)
     - date : 'YYYY-MM-DD'
     - code : 코드 본문 (백틱 ` ` 사이에 그대로. {{API_KEY}}는 학생 키로 자동 치환)
   ============================================================ */
window.CODES = [
  {
    n: 4,
    title: "유튜브 검색 — Pico / MicroPython (secrets.py)",
    lang: "micropython",
    date: "2026-06-24",
    code:
`# ── 1) 키를 secrets.py 에 저장 (코드에 직접 쓰지 않기!) ──
#   Thonny 에서  secrets.py  파일을 새로 만들어 Pico 에 저장:
#
#       WIFI_SSID = "와이파이_이름"
#       WIFI_PASSWORD = "와이파이_비밀번호"
#       YOUTUBE_API_KEY = "{{API_KEY}}"
#
#   ※ secrets.py 는 공유/업로드 금지
# ───────────────────────────────────────────────

import network, time, urequests
import secrets                       # ← 위 secrets.py 를 불러옴

# 1) 와이파이 연결
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
while not wlan.isconnected():
    time.sleep(0.5)
print("WiFi 연결됨:", wlan.ifconfig()[0])

# 2) 유튜브 검색 (Pico 는 urequests, URL 에 키를 붙여 보냄)
url = ("https://www.googleapis.com/youtube/v3/search"
       "?part=snippet&maxResults=5&q=cat"
       "&key=" + secrets.YOUTUBE_API_KEY)
res = urequests.get(url)
for item in res.json()["items"]:
    print(item["snippet"]["title"])
res.close()`,
  },

  {
    n: 3,
    title: "유튜브 검색 — Streamlit (st.secrets)",
    lang: "python",
    date: "2026-06-24",
    code:
`# ── 1) 키를 secrets 에 저장 (코드에 직접 쓰지 않기!) ──
#   프로젝트 폴더에  .streamlit/secrets.toml  파일을 만들고:
#
#       YOUTUBE_API_KEY = "{{API_KEY}}"
#
#   ※ secrets.toml 은 깃허브에 올리지 말 것 (.gitignore 에 추가)
#   ※ Streamlit Cloud 배포 시: 앱 Settings → Secrets 에 같은 내용 붙여넣기
# ───────────────────────────────────────────────

import streamlit as st
import requests

API_KEY = st.secrets["YOUTUBE_API_KEY"]   # ← secrets 에서 읽어옴

url = "https://www.googleapis.com/youtube/v3/search"
params = {"key": API_KEY, "q": "고양이", "part": "snippet", "maxResults": 5}
res = requests.get(url, params=params).json()

for item in res["items"]:
    st.write(item["snippet"]["title"])`,
  },

  {
    n: 2,
    title: "유튜브 인기 영상 TOP5 (Python · 빠른 테스트용)",
    lang: "python",
    date: "2026-06-24",
    code:
`import requests

API_KEY = "{{API_KEY}}"
url = "https://www.googleapis.com/youtube/v3/videos"
params = {
    "key": API_KEY,
    "part": "snippet",
    "chart": "mostPopular",
    "regionCode": "KR",
    "maxResults": 5,
}

r = requests.get(url, params=params)
for i, item in enumerate(r.json()["items"], 1):
    print(i, item["snippet"]["title"])`,
  },

  {
    n: 1,
    title: "유튜브 검색 (Python)",
    lang: "python",
    date: "2026-06-24",
    code:
`import requests

API_KEY = "{{API_KEY}}"
url = "https://www.googleapis.com/youtube/v3/search"
params = {
    "key": API_KEY,
    "q": "고양이",
    "part": "snippet",
    "maxResults": 5,
}

r = requests.get(url, params=params)
for item in r.json()["items"]:
    print(item["snippet"]["title"])`,
  },

  // ▼▼▼ 다음 코드는 이 윗줄(배열 맨 위)에 추가하세요. n 을 하나 올리면 자동으로 '최신'이 됩니다. ▼▼▼
];
