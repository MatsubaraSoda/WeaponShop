# GSA Weapons Bible

版本：v1.1  
组织：Galactic Sales Agency (GSA)  
生效范围：`ai_agencies/galactic_sales_agency/project`  
文档属性：GSA 内部最高执行规范（营销生产）

---

## 1. 权威基线与适用方式

本 Bible 已吸收并镜像以下规范中的 GSA 相关要求：

1. `docs/MASTER_SPEC.md`（产品与职责最高规范）。
2. `docs/schema/all.dbml`（字段与结构第二级规范）。

执行层原则：

1. GSA 运行时以本 Bible 作为直接操作手册。
2. 本 Bible 的字段契约必须与 `all.dbml` 保持一致。
3. 若后续上游规范更新，应优先修订本 Bible，再修订任务提示词。

---

## 2. GSA 组织使命与硬边界

### 2.1 唯一使命

将 CAS 的武器客观参数和 NLA 的宇宙语境转译为可销售、可审核、可被下游系统消费的商品营销数据。

### 2.2 硬边界（禁止越权）

GSA 不负责：

1. 入库（INSERT / UPDATE / migration / ETL）。
2. 支付、结算、履约、协议状态推进。
3. 改写武器客观事实或宇宙公理。
4. 视觉资产生成、前端渲染实现。
5. 上游 CAS/NLA 生产治理。

结论：**GSA 只负责“字段对齐的营销内容生产”，不负责入库执行。**

---

## 3. GSA 闭环输入资产

GSA 只依赖 `knowledge` 目录下三类输入：

1. `report.cas.md`：武器客观事实源。
2. `report.nla.md`：宇宙叙事语境源。
3. `GSA_Weapons_Bible.md`：规则与字段契约源。

---

## 4. all.dbml 字段对齐目标（核心）

> 目标：`output/report.md` 直接对准 `all.dbml` 所需业务字段，便于下游映射。  
> 声明：对准字段不等于执行入库。

### 4.1 对齐 `public.weapon_merchandising`（GSA 主责任）

GSA 必须输出以下字段（命名保持一致）：

1. `product_title`（varchar）
2. `short_description`（varchar）
3. `key_features`（jsonb，字符串数组）
4. `promo_copy`（text，可空）
5. `suggested_price_qc`（bigint，正整数）

### 4.2 对齐 `public.weapons`（GSA 提供可映射值，不宣称主数据权）

为保证 report 可被下游映射，GSA 需在每条记录携带以下“映射锚点”：

1. `sku_code`（唯一 SKU，字符串）
2. `native_universe_code`（用于映射 `public.universes.code`）
3. `list_price_qc`（整数，GSA 产出的“上架建议价”，供下游决策）

说明：

1. `list_price_qc` 是营销建议，不是结算系统行为。
2. `native_universe_id`、`weapon_id` 由下游根据映射关系生成/关联。
3. GSA 不生成数据库时间戳字段（`created_at`、`updated_at`）。

---

## 5. 字段级写作约束

### 5.1 `product_title`

1. 必须保留武器识别锚点（避免与 `armament_name` 失联）。
2. 允许商业化重命名，但不可脱离宇宙风格。
3. 建议 6-24 字。

### 5.2 `short_description`

1. 聚焦“谁在什么场景为何购买”。
2. 不得编造 CAS 未给出的硬参数。
3. 建议 30-80 字。

### 5.3 `key_features`

1. 固定 3 条。
2. 每条应可追溯到 CAS 字段。
3. 输出为 JSON 字符串数组语义（例如 `["x","y","z"]`）。

### 5.4 `promo_copy`

1. 可空；空值写 `N/A`。
2. 禁止承诺无法被事实支持的效果。
3. 与 `short_description` 职责分离：前者偏活动/促销，后者偏常设导购。

### 5.5 `suggested_price_qc` / `list_price_qc`

1. 必须是正整数。
2. 只输出数字，不带单位与货币名。
3. 两者关系默认：`list_price_qc = suggested_price_qc`，除非任务另行指定。

---

## 6. 生产 SOP（闭环）

### Step 1：事实抽取

从 `report.cas.md` 提取：

- `armament_name`
- `description`
- `physical_dimensions`
- `construction_feedstock`
- `usage_dependency`
- `operation_principle`
- 可选：`defects_and_risks`、`design_constraints`、`extended_spec`

### Step 2：宇宙映射

从 `report.nla.md` 为每个武器绑定宇宙代码与语境（至少输出 `native_universe_code`）。

### Step 3：字段生成

为每个武器生成第 4 章定义的全部输出字段。

### Step 4：门禁校验

1. **事实门禁**：不与 CAS 参数冲突。
2. **语境门禁**：符合该宇宙风格与禁忌。
3. **结构门禁**：字段齐全、命名准确。
4. **类型门禁**：`*_price_qc` 为整数；`key_features` 可被 JSON 数组解析。
5. **职责门禁**：输出中不得出现“已入库/已写库”等表述。

### Step 5：交付发布

输出到 `output/report.md`，供下游入库系统读取。

---

## 7. 定价策略（营销建议）

> 价格用于营销建议，不触发任何交易行为。

评分维度（1-5 分）：

1. 杀伤效率
2. 稀有度
3. 操作门槛
4. 战术覆盖
5. 风险惩罚（反向项）

公式：

`base_score = lethality + rarity + operation_complexity + tactical_coverage - risk_penalty`

`suggested_price_qc = max(1000, base_score * 5000)`

默认：

`list_price_qc = suggested_price_qc`

---

## 8. `report.md` 强制输出模板（字段对齐版）

每件武器必须按如下键输出：

```markdown
## item
- sku_code: <字符串，唯一>
- native_universe_code: <对应 universes.code>
- armament_name: <CAS 原名>
- list_price_qc: <整数>
- product_title: <字符串>
- short_description: <字符串>
- key_features: ["<卖点1>", "<卖点2>", "<卖点3>"]
- promo_copy: <字符串或 N/A>
- suggested_price_qc: <整数>
```

---

## 9. 异常处理

1. CAS 缺失关键字段：标记 `DATA_GAP`，该武器不产出正式条目。
2. NLA 无法映射宇宙：标记 `LORE_MISSING`，并要求补充 `native_universe_code`。
3. 价格无法确定：按公式给中位建议并标记 `PRICE_ESTIMATED`。
4. `sku_code` 冲突：后出现条目标记 `SKU_CONFLICT`，禁止覆盖。

---

## 10. 交付完成定义（DoD）

当且仅当满足以下条件，本轮 GSA 交付完成：

1. 每件武器均产出第 8 章模板字段。
2. 字段命名与 `all.dbml` 对齐。
3. 全部价格字段为整数。
4. 全流程无入库动作、无执行数据库写操作。

---

## 11. 执行口令

**“字段先对齐，再做文案；只交付 report，不触碰入库。”**