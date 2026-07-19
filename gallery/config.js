// ============================================================
// 피코 갤러리 설정 파일
// ------------------------------------------------------------
// SUPABASE_URL / SUPABASE_KEY 를 채우면 실제 Supabase와 연동됩니다.
// 비워두면(또는 이 파일이 없으면) 자동으로 "데모 모드"로 동작합니다.
//   - 데모 모드: 샘플 작품 6개로 브라우저 메모리에서만 동작 (새로고침 시 초기화)
//   - 실제 모드: 아래 두 값을 채우면 Supabase 프로젝트와 연동
//
// 이 프로젝트(upkakhnpvepqhsbwdyjb)는 당곡고 데이터 과학 팀 갤러리와
// 같은 Supabase 프로젝트를 재사용합니다. 이 갤러리는 별도 테이블
// (pico_apps / pico_feedback)을 쓰므로 서로 데이터가 섞이지 않습니다.
// 실제 갤러리로 쓰려면 gallery/pico_gallery_schema.sql을 먼저 실행하세요.
//
// ⚠️ 반드시 "publishable"(공개용 anon) 키만 넣으세요. secret 키는 절대 넣지 마세요.
// ============================================================
window.APP_CONFIG = {
  SUPABASE_URL: "https://upkakhnpvepqhsbwdyjb.supabase.co",
  SUPABASE_KEY: "sb_publishable_16HKdOESG_9U5OVNGZMeYQ_of--7oV1"
};
