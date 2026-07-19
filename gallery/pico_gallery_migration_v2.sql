-- ============================================================
-- 피코 학생 갤러리 v2 마이그레이션 — 세특 원천자료 수집 강화
-- ------------------------------------------------------------
-- ▶ 실행 방법
--   1) 이 파일은 gallery/pico_gallery_schema.sql(v1)을 먼저 실행해
--      pico_apps · pico_feedback 테이블이 이미 만들어져 있는 상태에서만
--      실행하세요. v1을 실행하지 않았다면 먼저 v1부터 실행할 것.
--   2) Supabase 대시보드 → 해당 프로젝트(upkakhnpvepqhsbwdyjb) 접속
--   3) 왼쪽 메뉴 SQL Editor → New query
--   4) 이 파일 전체를 붙여넣고 Run
--   5) 성공하면 Table Editor에 pico_apps_private 테이블이 새로 보입니다.
--      이 테이블은 "선생님 전용"입니다 — RLS에 select 정책을 아예 만들지
--      않았으므로 anon(공개) 롤로는 절대 조회가 안 되고, 오직 Supabase
--      대시보드의 Table Editor(서비스 롤로 접속)에서만 열람할 수 있습니다.
--
-- ▶ 이 마이그레이션이 하는 일
--   1) pico_apps.category CHECK 제약에 '머신러닝'을 추가 (ml_site 소리·
--      말하기·동작 인식 3챕터 작품 등록용).
--   2) pico_apps_private 테이블 신설 — 학교·학번·이름·"내가 주도적으로
--      한 일"·"배우고 느낀 점"을 담는 비공개 테이블. 세특(생활기록부)
--      작성 참고 자료로 선생님만 봅니다. 학생 화면(갤러리 카드)에는
--      이 테이블의 어떤 값도 절대 노출되지 않습니다 — 프라이버시의
--      본체는 "select 정책을 만들지 않는 것" 그 자체입니다.
-- ============================================================

-- ------------------------------------------------------------
-- 1) category CHECK 제약 교체: '머신러닝' 추가
-- ------------------------------------------------------------
-- pico_gallery_schema.sql(v1)의 category 컬럼은 테이블 생성 시 인라인으로
--   category text not null check (category in ('자유 프로젝트','오픈 API','수업 응용','기타'))
-- 라고만 썼고 별도 이름을 주지 않았습니다. 이 경우 PostgreSQL은
-- "<테이블명>_<컬럼명>_check" 규칙으로 자동 이름을 붙이므로 기대되는
-- 이름은 pico_apps_category_check 입니다. 실행 전 아래 조회로 실제
-- 제약 이름을 한 번 확인하는 것을 권장합니다(테이블을 직접 만들지 않고
-- 이 SQL 밖에서 이미 이름을 바꾼 적이 있다면 다를 수 있음):
--
--   select conname
--   from pg_constraint
--   where conrelid = 'public.pico_apps'::regclass
--     and contype = 'c'
--     and pg_get_constraintdef(oid) ilike '%category%';
--
-- 아래 DROP은 IF EXISTS로 안전하게 처리하되, 위 조회 결과가
-- pico_apps_category_check 와 다르다면 그 이름으로 바꿔서 실행하세요.

-- 제약 이름이 환경에 따라 다를 수 있어, 이름을 추정하지 않고 category 관련
-- CHECK 제약을 동적으로 찾아 제거합니다 (위 확인 쿼리는 참고용).
do $$
declare con_name text;
begin
  select conname into con_name
  from pg_constraint
  where conrelid = 'public.pico_apps'::regclass
    and contype = 'c'
    and pg_get_constraintdef(oid) ilike '%category%';
  if con_name is not null then
    execute format('alter table public.pico_apps drop constraint %I', con_name);
  end if;
end $$;

alter table public.pico_apps
  add constraint pico_apps_category_check
  check (category in ('자유 프로젝트', '오픈 API', '수업 응용', '기타', '머신러닝'));

-- ------------------------------------------------------------
-- 2) pico_apps_private — 세특 원천자료(비공개) 테이블
-- ------------------------------------------------------------
create table if not exists public.pico_apps_private (
  id            uuid primary key default gen_random_uuid(),
  app_id        uuid not null references public.pico_apps (id) on delete cascade,
  created_at    timestamptz not null default now(),
  school        text not null check (char_length(school) between 1 and 30),
  student_no    text not null check (char_length(student_no) between 1 and 10),
  student_name  text not null check (char_length(student_name) between 1 and 10),
  my_work       text not null check (char_length(my_work) between 1 and 250),
  learned       text not null check (char_length(learned) between 1 and 250)
);

create index if not exists pico_apps_private_app_id_idx on public.pico_apps_private (app_id);

-- ------------------------------------------------------------
-- 3) RLS — 프라이버시의 핵심
-- ------------------------------------------------------------
-- select 정책을 절대 만들지 않는다: 이것이 "학생 화면(익명/공개)에서
-- 절대 조회되지 않음"을 보장하는 유일하고 확실한 방법입니다. RLS가
-- 켜진 테이블에 select 정책이 하나도 없으면, anon/authenticated 롤은
-- 어떤 select 쿼리를 보내도 0행을 받습니다. 오직 Supabase 대시보드의
-- Table Editor(프로젝트 서비스 롤로 동작 — RLS를 우회함)에서만 열람
-- 가능합니다.
--
-- insert는 공개 허용하되(로그인 없는 버전이므로 제출 폼이 anon 롤로
-- insert함), WITH CHECK로 필수 필드가 비어있지 않은지 정도만 검증합니다.
-- update/delete 정책은 만들지 않아 전면 차단됩니다(v1과 동일한 원칙).

alter table public.pico_apps_private enable row level security;

create policy "pico_apps_private_public_insert" on public.pico_apps_private
  for insert with check (
    char_length(school) between 1 and 30
    and char_length(student_no) between 1 and 10
    and char_length(student_name) between 1 and 10
    and char_length(my_work) between 1 and 250
    and char_length(learned) between 1 and 250
  );

-- select 정책 없음 (의도적) — 아래는 "만들지 않는다"는 것을 명시하기 위한 주석입니다.
-- create policy "..." on public.pico_apps_private for select using (...);  <- 절대 추가하지 말 것

-- update/delete 정책 없음 (의도적, 전면 차단)
