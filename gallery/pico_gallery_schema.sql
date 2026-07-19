-- ============================================================
-- 피코 바이브 코딩 수업 · 학생 작품 갤러리 (로그인 없는 버전) — Supabase 스키마
-- ------------------------------------------------------------
-- ▶ 실행 방법
--   1) Supabase 대시보드 → 해당 프로젝트(upkakhnpvepqhsbwdyjb) 접속
--   2) 왼쪽 메뉴 SQL Editor → New query
--   3) 이 파일 전체를 붙여넣고 Run
--   4) 성공하면 Table Editor에 pico_apps · pico_feedback 두 테이블이 보입니다.
--
-- ▶ 로그인 없는 버전의 한계 (수업용으로 감수한 부분)
--   - 닉네임 사칭: 로그인이 없으므로 "박쌤" 닉네임을 아무나 다시 쓸 수 있습니다.
--     가벼운 공유 갤러리 특성상 실사용 피해가 적어 감수합니다. 엄격한 운영으로
--     옮긴다면 danggok 갤러리처럼 학교 계정 로그인(Google OAuth)을 추가하세요.
--   - 중복 좋아요 방지는 브라우저 localStorage 수준입니다(gallery/app.js).
--     즉 "다른 기기/시크릿창/캐시 삭제" 후 다시 누르면 또 눌립니다.
--     서버가 막는 것은 "좋아요 수 위조"(아래 WITH CHECK)뿐이고,
--     "한 사람이 여러 번 누르는 것" 자체는 막지 않습니다.
--   - 좋아요 수 위조(누구나 insert 시 likes=999 같은 값을 직접 써넣는 공격)는
--     아래 pico_apps_public_insert 정책의 WITH CHECK로 서버에서 차단합니다.
--     (당곡고 팀 갤러리에서 실제로 있었던 공격 사례 — 처음엔 "공개 insert만
--     허용, likes는 신경 안 씀"으로 열어뒀다가, 등록 즉시 likes를 큰 수로
--     써넣는 위조 행이 들어와 이 방어를 추가했습니다.)
--
-- ▶ 테스트 데이터 정리
--   수업 중 만든 테스트 행은 SQL을 쓰지 않아도 Table Editor에서
--   pico_apps 행을 선택해 Delete하면 됩니다(ON DELETE CASCADE로
--   pico_feedback의 관련 피드백도 함께 삭제됩니다).
-- ============================================================

create extension if not exists pgcrypto;

-- ---------- 작품 (pico_apps) ----------
create table if not exists public.pico_apps (
  id           uuid primary key default gen_random_uuid(),
  created_at   timestamptz not null default now(),
  nickname     text not null check (char_length(nickname) between 1 and 20),
  category     text not null check (category in ('자유 프로젝트', '오픈 API', '수업 응용', '기타')),
  title        text not null check (char_length(title) between 1 and 40),
  url          text not null check (url ~ '^https://'),
  description  text not null check (char_length(description) between 1 and 80),
  likes        integer not null default 0 check (likes >= 0)
);

create index if not exists pico_apps_category_idx on public.pico_apps (category);

-- ---------- 한 줄 피드백 (pico_feedback) ----------
create table if not exists public.pico_feedback (
  id           uuid primary key default gen_random_uuid(),
  app_id       uuid not null references public.pico_apps (id) on delete cascade,
  created_at   timestamptz not null default now(),
  nickname     text not null check (char_length(nickname) between 1 and 16),
  content      text not null check (char_length(content) between 1 and 60)
);

create index if not exists pico_feedback_app_id_idx on public.pico_feedback (app_id);

-- ============================================================
-- RLS (Row Level Security)
-- 원칙: 누구나 읽고(select) 새로 쓸(insert) 수 있지만,
--       수정(update)·삭제(delete)는 정책을 만들지 않아 전면 차단.
--       좋아요 증가만 아래 RPC 함수를 통해서만 허용.
-- ============================================================

alter table public.pico_apps enable row level security;
alter table public.pico_feedback enable row level security;

-- pico_apps: 공개 조회 + 공개 등록.
-- ⚠️ 핵심 방어선 — WITH CHECK (likes = 0 또는 likes is null):
--   등록(insert) 시 클라이언트가 likes 컬럼에 어떤 값을 실어 보내든,
--   0 또는 NULL이 아니면 이 정책이 그 insert 자체를 거부합니다.
--   즉 "새 작품을 등록하면서 좋아요 수를 999로 위조해 끼워 넣기"가
--   데이터베이스 레벨에서 막힙니다. (update/delete 정책이 없어 등록 후
--   likes를 직접 고치는 것도 막혀 있으므로, 좋아요는 오직 아래
--   pico_increment_likes RPC로만 늘어납니다.)
create policy "pico_apps_public_select" on public.pico_apps
  for select using (true);

create policy "pico_apps_public_insert" on public.pico_apps
  for insert with check (likes = 0 or likes is null);

-- pico_feedback: 공개 조회 + 공개 등록만 허용 (update/delete 정책 없음 = 전면 차단)
create policy "pico_feedback_public_select" on public.pico_feedback
  for select using (true);

create policy "pico_feedback_public_insert" on public.pico_feedback
  for insert with check (true);

-- ============================================================
-- 좋아요 증가 RPC
-- - 원자적 UPDATE 한 줄로 처리 → 동시에 여러 명이 눌러도 카운트 안전
--   (레이스 컨디션 없음)
-- - SECURITY DEFINER: 이 함수를 만든 소유자 권한으로 실행되어
--   pico_apps에 update 정책이 없어도 likes 컬럼만 안전하게 증가시킬 수 있음
--   → 클라이언트는 이 함수 호출(rpc) 외에는 절대 likes를 직접 update할 수 없음
-- - 존재하지 않는 app_id로 호출되면(이미 삭제된 작품 등) 예외를 던지지
--   않고 조용히 무시하며 NULL을 반환한다 (요청 사양: "무시").
-- ============================================================

create or replace function public.pico_increment_likes(p_app_id uuid)
returns integer
language plpgsql
security definer
set search_path = public
as $$
declare
  new_likes integer;
begin
  update public.pico_apps
     set likes = likes + 1
   where id = p_app_id
  returning likes into new_likes;

  -- new_likes가 NULL이면 해당 id의 행이 없다는 뜻 — 예외 없이 그대로 NULL 반환(무시).
  return new_likes;
end;
$$;

-- anon(로그인 없는 방문자) 롤이 이 함수를 실행할 수 있어야 이 버전(로그인 없음)이 동작한다.
-- 테이블 직접 update는 여전히 불가 — 오직 이 함수를 통해서만 likes가 늘어난다.
revoke all on function public.pico_increment_likes(uuid) from public;
grant execute on function public.pico_increment_likes(uuid) to anon, authenticated;

-- ============================================================
-- (선택) 실시간 구독을 쓰고 싶다면 아래 주석 해제
-- ============================================================
-- alter publication supabase_realtime add table public.pico_apps;
-- alter publication supabase_realtime add table public.pico_feedback;
