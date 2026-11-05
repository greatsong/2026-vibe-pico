-- ============================================================
-- 피코 갤러리 v3 — pico_apps_private 권한 축소 (적용 전 검토용. 아직 실행하지 않았습니다)
-- ------------------------------------------------------------
-- 이 표에는 학교·학번·이름·소감이 있습니다. 지금은 RLS에 select 정책이 없어서 막혀 있고,
-- 이 방어선은 정책 한 줄이 잘못 추가되면 바로 무너집니다. 표 권한도 회수해 두 겹으로 막습니다.
--
-- 앱과의 대조(gallery/app.js insertPrivateInfo):
--   .insert([...]) 뒤에 .select() 가 없어 PostgREST 가 return=minimal 로 보냅니다.
--   따라서 anon 에게 insert 권한만 있으면 동작하고 select 권한은 필요 없습니다.
--   이 표를 읽는 코드는 없습니다. 조회는 대시보드(서비스 롤)에서만 합니다.
--
-- 적용 뒤 확인: 작품을 하나 제출해 "비공개 정보 저장"이 성공하는지 봅니다.
-- 되돌리기: grant select, update, delete on public.pico_apps_private to anon, authenticated;
-- ============================================================

revoke select, update, delete, truncate, references, trigger
  on public.pico_apps_private from anon, authenticated;

grant insert on public.pico_apps_private to anon, authenticated;

notify pgrst, 'reload schema';
