// ============================================================
// 피코 바이브 코딩 수업 · 학생 작품 갤러리 — app.js
// 로그인 없는 버전. 빌드 없는 정적 SPA.
// config.js 에 SUPABASE_URL/KEY 가 비어 있으면 자동으로 데모 모드(메모리 내
// 샘플 데이터)로 동작하고, 값이 있어도 테이블이 아직 없으면(개강 전 배포
// 등) 자동으로 데모 모드로 폴백하며 안내 배너를 띄운다.
// ============================================================

(function () {
  "use strict";

  // ---------------------------------------------------------
  // 0. 금지어 필터 — 한국어 비속어 기본 목록 (당곡고 갤러리 목록 재사용)
  //    필요하면 아래 BANNED_WORDS 배열에 단어만 추가하면 된다.
  // ---------------------------------------------------------
  const BANNED_WORDS = [
    "시발", "씨발", "씨팔", "시팔", "쓰발", "ㅅㅂ", "ㅆㅂ",
    "개새끼", "개새", "새끼", "병신", "ㅄ", "지랄", "좆", "좃",
    "존나", "존나게", "졸라", "닥쳐", "미친놈", "미친년", "쳐죽",
    "죽어", "꺼져", "걸레", "창녀", "년아", "놈아", "fuck", "shit",
    "bitch", "asshole", "damn", "faggot", "니미", "느그", "애미",
    "애비", "썅", "씹", "좇", "간나", "빙신", "새꺄", "새키",
  ];

  function findBannedWord(text) {
    if (!text) return null;
    const normalized = String(text).toLowerCase().replace(/\s+/g, "");
    for (const word of BANNED_WORDS) {
      if (normalized.includes(word.toLowerCase())) return word;
    }
    return null;
  }

  // ---------------------------------------------------------
  // 1. 모드 판별 (데모 vs 실제)
  //    useSupabase는 나중에 "테이블 없음"을 만나면 false로 재조정될 수 있으므로
  //    const가 아니라 let으로 둔다 (아래 4.5 폴백 로직 참고).
  // ---------------------------------------------------------
  const cfg = window.APP_CONFIG || {};
  const hasRealConfig = !!(cfg.SUPABASE_URL && cfg.SUPABASE_KEY &&
    cfg.SUPABASE_URL.trim() && cfg.SUPABASE_KEY.trim());

  let supabaseClient = null;
  if (hasRealConfig) {
    try {
      supabaseClient = window.supabase.createClient(cfg.SUPABASE_URL, cfg.SUPABASE_KEY);
    } catch (e) {
      console.error("Supabase 클라이언트 생성 실패, 데모 모드로 대체:", e);
    }
  }
  let useSupabase = hasRealConfig && !!supabaseClient;
  let tableMissing = false; // 실제 모드로 시작했지만 테이블이 아직 없어 데모로 폴백한 경우

  // ---------------------------------------------------------
  // 2. 데모 데이터 (메모리 전용, 새로고침 시 초기화)
  // ---------------------------------------------------------
  let demoIdSeq = 1000;
  function nextDemoId() { return "demo-" + (demoIdSeq++); }

  const demoApps = [
    {
      id: nextDemoId(), nickname: "김쌤", category: "자유 프로젝트",
      title: "우리반 공기질 알림 무드등", url: "https://example.com/demo-pico-air-mood",
      description: "MQ-2 값에 따라 LED 색이 바뀌는 무드등을 만들었어요", likes: 5,
      feedback: [
        { nickname: "박쌤", content: "색이 부드럽게 바뀌어서 눈이 편해요!" },
        { nickname: "이코치", content: "임계값 설명이 이해하기 쉬웠어요" },
      ],
    },
    {
      id: nextDemoId(), nickname: "이코치", category: "오픈 API",
      title: "국제우주정거장(ISS) 위치 LED 시계", url: "https://example.com/demo-pico-iss-clock",
      description: "Open Notify API로 ISS 위치를 받아 LED로 표시했어요", likes: 8,
      feedback: [{ nickname: "정하늘", content: "부록A 예제에서 아이디어를 얻었어요" }],
    },
    {
      id: nextDemoId(), nickname: "정하늘", category: "수업 응용",
      title: "강수확률 물리 대시보드 개선판", url: "https://example.com/demo-pico-rain-dashboard",
      description: "5장 대시보드에 우산 이모지 알림을 추가했어요", likes: 3,
      feedback: [
        { nickname: "최멘토", content: "우산 알림 아이디어 좋아요" },
        { nickname: "한티처", content: "우리 반에도 적용해볼게요" },
      ],
    },
    {
      id: nextDemoId(), nickname: "최멘토", category: "기타",
      title: "와이파이 신호 세기 음악 반응기", url: "https://example.com/demo-pico-rssi-sound",
      description: "신호가 약해지면 경고음이 나는 스피커를 붙였어요", likes: 6,
      feedback: [],
    },
    {
      id: nextDemoId(), nickname: "한티처", category: "자유 프로젝트",
      title: "출석 체크 LED 게이지", url: "https://example.com/demo-pico-attendance",
      description: "교실 인원수를 세어 LED 게이지로 보여줘요", likes: 2,
      feedback: [{ nickname: "김쌤", content: "학급 운영에 바로 쓸 수 있겠어요" }],
    },
    {
      id: nextDemoId(), nickname: "박쌤", category: "오픈 API",
      title: "미세먼지 신호등", url: "https://example.com/demo-pico-dust-light",
      description: "에어코리아 데이터를 받아 신호등 색으로 표시했어요", likes: 9,
      feedback: [{ nickname: "이코치", content: "3장 대시보드랑 같이 쓰면 좋겠어요" }],
    },
  ];

  // ---------------------------------------------------------
  // 3. 데이터 레이어 (데모 / 실제 공통 인터페이스)
  // ---------------------------------------------------------
  let appsCache = []; // 실제 모드에서 feedback을 합쳐 캐싱

  async function loadAppsFromSupabase() {
    const { data: apps, error: appsErr } = await supabaseClient
      .from("pico_apps")
      .select("*")
      .order("created_at", { ascending: false });
    if (appsErr) throw appsErr;

    const { data: fbRows, error: fbErr } = await supabaseClient
      .from("pico_feedback")
      .select("*")
      .order("created_at", { ascending: true });
    if (fbErr) throw fbErr;

    const fbByApp = {};
    (fbRows || []).forEach((row) => {
      if (!fbByApp[row.app_id]) fbByApp[row.app_id] = [];
      fbByApp[row.app_id].push({ nickname: row.nickname, content: row.content });
    });

    return (apps || []).map((a) => ({ ...a, feedback: fbByApp[a.id] || [] }));
  }

  // 실제 모드 로딩 시도 → 실패하면(가장 흔한 원인: pico_gallery_schema.sql을
  // 아직 실행하지 않아 테이블이 없음) 데모 모드로 조용히 폴백하고 안내 배너를 띄운다.
  async function loadApps() {
    if (useSupabase) {
      try {
        appsCache = await loadAppsFromSupabase();
        return appsCache;
      } catch (e) {
        console.error("실제 갤러리 로딩 실패 → 데모 모드로 전환:", e);
        useSupabase = false;
        tableMissing = true;
      }
    }
    // 데모: 등록순(최신 데모 등록이 위로) 유지
    appsCache = demoApps;
    return demoApps;
  }

  async function insertApp(payload) {
    if (!useSupabase) {
      const newApp = {
        id: nextDemoId(),
        nickname: payload.nickname,
        category: payload.category,
        title: payload.title,
        url: payload.url,
        description: payload.description,
        likes: 0,
        feedback: [],
      };
      demoApps.unshift(newApp);
      return newApp;
    }
    const { data, error } = await supabaseClient
      .from("pico_apps")
      .insert([payload])
      .select()
      .single();
    if (error) throw error;
    data.feedback = [];
    appsCache.unshift(data);
    return data;
  }

  // 좋아요 증가: 데모 모드는 메모리+localStorage로, 실제 모드는
  // pico_increment_likes RPC로 처리한다. 두 모드 모두 "계정"이 없으므로
  // 중복 방지는 localStorage 수준(기기·브라우저별)에 머문다 — 한계는
  // pico_gallery_schema.sql 상단 주석과 아래 5번 절 참고.
  async function incrementLike(appId) {
    if (!useSupabase) {
      const app = demoApps.find((a) => a.id === appId);
      if (!app) throw new Error("app not found");
      app.likes += 1;
      return app.likes;
    }
    const { data, error } = await supabaseClient.rpc("pico_increment_likes", { p_app_id: appId });
    if (error) throw error;
    const app = appsCache.find((a) => a.id === appId);
    if (app && typeof data === "number") app.likes = data;
    return data;
  }

  async function insertFeedback(appId, nickname, content) {
    if (!useSupabase) {
      const app = demoApps.find((a) => a.id === appId);
      if (!app) throw new Error("app not found");
      app.feedback.push({ nickname, content });
      return;
    }
    const { error } = await supabaseClient
      .from("pico_feedback")
      .insert([{ app_id: appId, nickname, content }]);
    if (error) throw error;
    const app = appsCache.find((a) => a.id === appId);
    if (app) app.feedback.push({ nickname, content });
  }

  // ---------------------------------------------------------
  // 4. 좋아요 중복 방지 (localStorage 기반, 로그인 없는 버전의 한계)
  //    계정이 없으므로 "누가 눌렀는지"를 서버가 알 방법이 없다. 이 갤러리는
  //    브라우저의 localStorage에 "내가 누른 작품 id"만 저장해 같은
  //    브라우저에서는 중복 클릭을 막는다. 시크릿창·다른 기기·캐시 삭제
  //    후에는 다시 누를 수 있다 — 수업용으로 감수한 한계다.
  // ---------------------------------------------------------
  const LIKED_KEY = "pico_gallery_liked_ids";
  function getLikedSet() {
    try {
      return new Set(JSON.parse(localStorage.getItem(LIKED_KEY) || "[]"));
    } catch (e) {
      return new Set();
    }
  }
  function saveLikedLocal(id) {
    const s = getLikedSet();
    s.add(id);
    try { localStorage.setItem(LIKED_KEY, JSON.stringify([...s])); } catch (e) { /* noop */ }
  }
  let likedSet = getLikedSet();
  function isLiked(appId) { return likedSet.has(appId); }

  // ---------------------------------------------------------
  // 5. 상태 & 필터
  // ---------------------------------------------------------
  const CATEGORIES = ["자유 프로젝트", "오픈 API", "수업 응용", "기타"];
  let filterCategory = "all";

  // ---------------------------------------------------------
  // 6. DOM 유틸
  // ---------------------------------------------------------
  const $ = (sel, root) => (root || document).querySelector(sel);
  const $all = (sel, root) => Array.from((root || document).querySelectorAll(sel));

  function isHttpsUrl(str) {
    try {
      const u = new URL(str);
      return u.protocol === "https:";
    } catch (e) {
      return false;
    }
  }

  // ---------------------------------------------------------
  // 7. 렌더링
  // ---------------------------------------------------------
  const gridEl = $("#galleryGrid");
  const emptyEl = $("#galleryEmpty");
  const countEl = $("#galleryCount");
  const cardTemplate = $("#cardTemplate");

  function categoryClass(cat) {
    if (cat === "자유 프로젝트") return "cat-free";
    if (cat === "오픈 API") return "cat-api";
    if (cat === "수업 응용") return "cat-lesson";
    return "cat-etc";
  }

  function renderGallery() {
    const filtered = appsCache.filter((a) => {
      if (filterCategory !== "all" && a.category !== filterCategory) return false;
      return true;
    });

    gridEl.innerHTML = "";
    countEl.textContent = `총 ${filtered.length}개 작품`;
    emptyEl.hidden = filtered.length > 0;

    filtered.forEach((app) => {
      const node = cardTemplate.content.cloneNode(true);
      const catBadge = node.querySelector(".cat-badge");
      catBadge.textContent = app.category;
      catBadge.classList.add(categoryClass(app.category));

      node.querySelector(".card-title").textContent = app.title;
      node.querySelector(".card-by").textContent = "작성자: " + app.nickname;
      node.querySelector(".card-desc").textContent = app.description;

      const goBtn = node.querySelector(".btn-go");
      goBtn.href = app.url;

      const likeBtn = node.querySelector(".btn-like");
      const likeCountEl = node.querySelector(".like-count");
      likeCountEl.textContent = app.likes;
      const likedNow = isLiked(app.id);
      likeBtn.classList.toggle("liked", likedNow);
      likeBtn.setAttribute("aria-pressed", likedNow ? "true" : "false");
      likeBtn.addEventListener("click", async () => {
        if (likeBtn.disabled) return;
        likeBtn.disabled = true;
        try {
          const count = await incrementLike(app.id);
          likeCountEl.textContent = typeof count === "number" ? count : app.likes;
          likedSet.add(app.id);
          saveLikedLocal(app.id);
          likeBtn.classList.add("liked");
          likeBtn.setAttribute("aria-pressed", "true");
        } catch (e) {
          console.error(e);
          showToast("좋아요 처리 중 오류가 발생했어요. 잠시 후 다시 시도해주세요.", "error");
          likeBtn.disabled = false;
        }
      });

      const fbCountEl = node.querySelector(".fb-count");
      const fbListEl = node.querySelector(".fb-list");
      fbCountEl.textContent = `(${app.feedback.length})`;
      renderFeedbackList(fbListEl, app.feedback);

      const fbForm = node.querySelector(".fb-form");
      const fbMsg = node.querySelector(".fb-msg");
      fbForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const nickInput = fbForm.querySelector(".fb-nickname");
        const contentInput = fbForm.querySelector(".fb-content");
        const nickname = nickInput.value.trim();
        const content = contentInput.value.trim();

        fbMsg.hidden = true;
        fbMsg.className = "fb-msg";

        if (!nickname || !content) {
          showFbMsg(fbMsg, "닉네임과 피드백을 모두 입력해주세요.");
          return;
        }
        const banned = findBannedWord(nickname) || findBannedWord(content);
        if (banned) {
          showFbMsg(fbMsg, "부적절한 표현이 포함되어 있어 등록할 수 없어요.");
          return;
        }

        const submitBtn = fbForm.querySelector("button[type=submit]");
        submitBtn.disabled = true;
        try {
          await insertFeedback(app.id, nickname, content);
          fbCountEl.textContent = `(${app.feedback.length})`;
          renderFeedbackList(fbListEl, app.feedback);
          nickInput.value = "";
          contentInput.value = "";
          showFbMsg(fbMsg, "피드백을 남겼어요. 고마워요!", "ok");
        } catch (err) {
          console.error(err);
          showFbMsg(fbMsg, "등록 중 오류가 발생했어요. 잠시 후 다시 시도해주세요.");
        } finally {
          submitBtn.disabled = false;
        }
      });

      gridEl.appendChild(node);
    });
  }

  function showFbMsg(el, text, type) {
    el.textContent = text;
    el.hidden = false;
    el.className = "fb-msg " + (type === "ok" ? "ok" : "error");
  }

  function renderFeedbackList(listEl, feedback) {
    listEl.innerHTML = "";
    if (!feedback.length) {
      const li = document.createElement("li");
      li.className = "fb-empty";
      li.textContent = "아직 피드백이 없어요. 첫 피드백을 남겨보세요!";
      listEl.appendChild(li);
      return;
    }
    feedback.forEach((f) => {
      const li = document.createElement("li");
      const nickSpan = document.createElement("span");
      nickSpan.className = "fb-nick";
      nickSpan.textContent = f.nickname;
      li.appendChild(nickSpan);
      li.appendChild(document.createTextNode(f.content));
      listEl.appendChild(li);
    });
  }

  // ---------------------------------------------------------
  // 8. 토스트 배너 (네이티브 alert 대신)
  // ---------------------------------------------------------
  function showToast(text, type) {
    let el = document.getElementById("siteToast");
    if (!el) {
      el = document.createElement("div");
      el.id = "siteToast";
      el.className = "site-toast";
      el.setAttribute("role", "status");
      document.body.appendChild(el);
    }
    el.textContent = text;
    el.className = "site-toast show" + (type === "error" ? " error" : "");
    clearTimeout(el._t);
    el._t = setTimeout(() => { el.className = "site-toast"; }, 3500);
  }

  // ---------------------------------------------------------
  // 9. 탭 & 필터 이벤트
  // ---------------------------------------------------------
  function initTabs() {
    $all(".tab").forEach((btn) => {
      btn.addEventListener("click", () => {
        $all(".tab").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        const view = btn.dataset.view;
        $all(".view").forEach((v) => v.classList.remove("active"));
        $("#view-" + view).classList.add("active");
      });
    });
  }

  function initFilters() {
    $all("#categoryFilter .chip-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        $all("#categoryFilter .chip-btn").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        filterCategory = btn.dataset.category;
        renderGallery();
      });
    });
  }

  // ---------------------------------------------------------
  // 10. 제출 폼
  // ---------------------------------------------------------
  function initSubmitForm() {
    const form = $("#submitForm");

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const msgEl = $("#formMsg");
      msgEl.hidden = true;
      msgEl.className = "form-msg";

      const nickname = $("#f-nickname").value.trim();
      const category = $("#f-category").value;
      const title = $("#f-title").value.trim();
      const url = $("#f-url").value.trim();
      const description = $("#f-desc").value.trim();
      const consent = $("#f-consent").checked;

      if (!nickname || !category || !title || !url || !description) {
        return showFormMsg("모든 필수 항목(*)을 입력해주세요.");
      }
      if (!consent) {
        return showFormMsg("작품 공개 동의 체크가 필요해요.");
      }
      if (!isHttpsUrl(url)) {
        return showFormMsg("작품 URL은 https:// 로 시작하는 올바른 주소여야 해요.");
      }
      if (nickname.length > 20 || title.length > 40 || description.length > 80) {
        return showFormMsg("입력 길이가 너무 길어요. 조금 줄여주세요.");
      }

      const bannedHit = findBannedWord(nickname) || findBannedWord(title) || findBannedWord(description);
      if (bannedHit) {
        return showFormMsg("닉네임·제목·소개 중 부적절한 표현이 포함되어 있어요. 확인 후 다시 제출해주세요.");
      }

      const submitBtn = form.querySelector(".btn-primary");
      submitBtn.disabled = true;
      try {
        await insertApp({ nickname, category, title, url, description });
        form.reset();
        showFormMsg("게시 완료! 갤러리 탭에서 확인해보세요.", "ok");
        renderGallery();
      } catch (err) {
        console.error(err);
        showFormMsg("게시 중 오류가 발생했어요. 잠시 후 다시 시도해주세요.");
      } finally {
        submitBtn.disabled = false;
      }

      function showFormMsg(text, type) {
        msgEl.textContent = text;
        msgEl.hidden = false;
        msgEl.className = "form-msg " + (type === "ok" ? "ok" : "error");
      }
    });
  }

  // ---------------------------------------------------------
  // 11. 모드 배지 & 폴백 안내 배너
  // ---------------------------------------------------------
  function renderModeBadge() {
    // 학생 화면에는 기술 용어 배지를 표시하지 않는다 — 요소가 있으면(과거 버전) 조작하고 없으면 건너뜀.
    const badge = $("#modeBadge");
    if (badge) {
      if (useSupabase) {
        badge.textContent = "실제 모드 (Supabase 연동)";
        badge.classList.add("live");
      } else {
        badge.textContent = tableMissing ? "데모 모드 (테이블 준비 전)" : "데모 모드 (샘플 데이터)";
        badge.classList.add("demo");
      }
    }

    const notice = $("#fallbackNotice");
    if (notice) {
      if (tableMissing) {
        notice.hidden = false;
      } else {
        notice.hidden = true;
      }
    }
  }

  // ---------------------------------------------------------
  // 12. 시작
  // ---------------------------------------------------------
  async function init() {
    initTabs();
    initFilters();
    initSubmitForm();
    try {
      await loadApps();
    } catch (e) {
      console.error("데이터 로딩 실패:", e);
      countEl.textContent = "데이터를 불러오지 못했어요. 잠시 후 새로고침해주세요.";
    }
    renderModeBadge();
    renderGallery();
  }

  document.addEventListener("DOMContentLoaded", init);
})();

// ── 사용성 보강 ──
document.addEventListener("click", (e) => {
  const btn = e.target.closest("[data-go-submit]");
  if (!btn) return;
  const tab = [...document.querySelectorAll(".tab")].find((b) => (b.dataset.view || "") === "submit");
  if (tab) { tab.click(); window.scrollTo({ top: 0, behavior: "smooth" }); }
});
// 닉네임/제목이 최대 길이에 닿으면 조용히 잘리지 않게 안내
document.addEventListener("input", (e) => {
  const el = e.target;
  if (!el.maxLength || el.maxLength < 0 || el.tagName !== "INPUT") return;
  if (el.value.length >= el.maxLength) {
    let hint = el.parentElement.querySelector(".len-hint");
    if (!hint) {
      hint = document.createElement("span");
      hint.className = "len-hint";
      el.parentElement.appendChild(hint);
    }
    hint.textContent = `최대 ${el.maxLength}자까지 쓸 수 있어요.`;
  } else {
    const hint = el.parentElement.querySelector(".len-hint");
    if (hint) hint.remove();
  }
});
