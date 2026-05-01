你是一个资深的前端架构师。我们的 Vite + React + TS 项目已经初始化完成，现在我们需要打通连接 Supabase 后端数据库的“数据骨架”。

请按照以下步骤为我生成代码并执行：

1. **安装依赖**：请帮我安装 `@supabase/supabase-js`。
2. **环境变量**：提醒我或帮我创建 `.env.local` 文件，包含 `VITE_SUPABASE_URL` 和 `VITE_SUPABASE_ANON_KEY`（占位符即可，我自己填入真实秘钥）。
3. **初始化客户端**：创建 `src/lib/supabase.ts`，导出配置好的 supabase 实例。
4. **定义类型与 Hook**：根据我下方提供的 SQL 表结构，在 `src/hooks/useWeapons.ts` 中：
   - 精准定义 `Weapon` 的 TypeScript Interface。
   - 编写并导出一个 custom hook `useWeapons`，负责从 `weapons` 表中 `select('*')` 全量抓取数据。
   - 必须包含严谨的 `data`、`isLoading` 和 `error` 状态管理。
5. **极简测试渲染**：修改 `src/App.tsx`，调用 `useWeapons`。如果正在加载，显示 Loading；如果有报错，显示 Error；如果成功，请**不需要写任何复杂样式**，直接用 `<pre>{JSON.stringify(data, null, 2)}</pre>` 或者一个最简陋的 `<ul>` 列表把拉取到的真实数据展示在页面上，用来验证端到端的数据连通性。

这是后端的表结构，请据此生成 TypeScript 类型：
```sql
CREATE TABLE weapons (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    world_shell TEXT NOT NULL,
    title TEXT NOT NULL,
    short_description TEXT,
    price_value INTEGER NOT NULL,
    currency_type TEXT NOT NULL,
    features JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```
@ai_agencies/data_harmonization_system/supabase/01_init_weapons_table.sql 

目前 .env 为空，后端是 supabase。请你顺被设置 .env 的内容填什么，不要直接查看 .env，而是给我一个 .env.example。