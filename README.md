# 零态军工终端（NSM）

**NullSpace Munitions（零态军工集团，NSM）** 的战术采购终端：在「多元宇宙黑市」设定下，将常规全栈能力（数据查询、状态与资产变更、任务型创建等）映射为军火交付与资产结算体验。

**产品公理与章节化 PRD 以 `docs/MASTER_SPEC.md` 为唯一权威**；实现与本文冲突时，以该文档为准并回溯修订。

---

## 项目概述

本项目以 **Chingu Solo Project（Tier 3）** 规模的全栈应用为交付形态，用一套可自洽的科幻业务语言包装需求：用户以 **跨界特工** 身份操作终端，在**校准宇宙**下浏览经 **物理可行性门禁** 过滤的 **商品目录（Catalog）**，使用 **量子信用点（Quantum Credit，QC）** 作为**唯一**结算单位，避免多币种与汇率逻辑。

业务侧与常见电商概念的对应关系（命名与协议划分对齐 PRD **公理 III / IV**）：

- **出向：虫洞（Wormhole）—「虫洞倾泻军火」**（对应任务型创建 / 军火运输）：用户配置目标宇宙、空间坐标与执行策略，开启**单向虫洞投送通道**，将订货自亚空间总账本定向送达前线，由后端 `wormhole_*` 协议栈承接；叙事上为**经虫洞向前线单向倾泻军火**，专责**武器运输**。
- **入向：黑洞（Black Hole）—「黑洞虹吸置换」**（对应余额侧资产增加 / 资产提取）：用户以指定宇宙坐标开启**单向黑洞吸入通道**，将远端实体物资**虹吸入账并折算为 QC**，由 `black_hole_intake_requests` 等栈承接；专责**资产提取**。虫洞与黑洞**职责对仗、管线不得串线**。
- **宇宙节点校准**（对应动态查询与目录过滤）：因 **本源法则排斥**（离开原生宇宙的实体武器在异宇宙会**亚原子级坍缩**），终端须按当前选定的**校准宇宙**对 SKU 做 **Catalog 级 `WHERE` 过滤**，只展示该宇宙法则下**可击发**的装备。

持久化与鉴权在 PRD 中归约为对**信息态亚空间**总账本的访问；具体技术栈与部署以本仓库实现为准（如前端、Supabase 等见下方徽章与代码结构）。

---

## 设定与内容管线（CrewAI）

设定与文案由仓库内 **CrewAI** 多智能体项目生成，**不**承担终端运行时；产出经产品验收后可进入策划与入库流程。与 `docs/MASTER_SPEC.md` 第 1.2–1.4 节一一对应：

| 目录 | 管线 | PRD 职责摘要 |
| --- | --- | --- |
| `ai_agencies/nexus_lore_agency` | **Nexus Lore Agency** | 多元宇宙设定稿（宏观冲突、战争形态、能量与武备体系等） |
| `ai_agencies/conceptual_armory_studio` | **CAS** | 各宇宙**武器客观设定**（参数、机理、风险等）；**不含**文生图 Prompt、画幅或视觉指令 |
| `ai_agencies/galactic_sales_agency` | **GSA** | 每把武器的**营销与上架向文案**；**建议性标价**不替代产品定价域真源 |

---

## 文档与数据

- **PRD / 公理：** [`docs/MASTER_SPEC.md`](docs/MASTER_SPEC.md)
- **库表结构（若使用）：** 见 `docs/schema/nsm_multiverse_catalog.dbml` 等

---

## 技术栈与状态（参考）

[![Chingu](https://img.shields.io/badge/Chingu-Solo_Project_Tier_3-blueviolet.svg)](#)
[![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)](#)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=flat&logo=typescript&logoColor=white)](#)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat&logo=tailwind-css&logoColor=white)](#)
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=flat&logo=supabase&logoColor=white)](#)

在线终端预览链接待部署后补充。
