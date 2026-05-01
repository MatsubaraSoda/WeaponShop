-- 赋予最高特权角色 (你的 DHS 脚本) 所有增删改查权限
GRANT ALL ON TABLE public.weapons TO service_role;

-- 提前为未来的前端用户 (未登录) 赋予所有权限
-- (注意：在真实的生产环境中，anon 通常只给 SELECT 权限，但 MVP 阶段我们先全开防止踩坑)
GRANT ALL ON TABLE public.weapons TO anon;

-- 提前为未来的前端用户 (已登录) 赋予所有权限
GRANT ALL ON TABLE public.weapons TO authenticated;
