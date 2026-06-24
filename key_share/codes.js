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
    n: 2,
    title: "유튜브 인기 영상 TOP5 (Python)",
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
