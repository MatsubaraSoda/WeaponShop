进入容器

```bash
docker exec -it conceptual_armory_studio bash
```

### Knowledge / Embedding（503、`text-embedding-3-small` 不可用）

CrewAI 默认用 OpenAI 兼容的 **`text-embedding-3-small`** 做向量入库；若聚合网关（如 gemini 特价线路）**不提供该 embedding**，会报 `Failed to upsert documents` / `model_not_found`。

**任选其一：**

1. **换成本网关支持的 embedding 模型名**（在 `.env` 中）：  
   `CREWAI_EMBEDDING_MODEL=…`（或 `OPENAI_EMBEDDING_MODEL=…`），须与 `OPENAI_BASE_URL` 实际路由一致。  
   若走 **Gemini embedding**，可设：`CREWAI_EMBEDDING_PROVIDER=google-generativeai`，并配置对应 `CREWAI_EMBEDDING_MODEL`（如 `gemini-embedding-001`），且需具备 Google 侧密钥/环境。

2. **不做向量 Knowledge**（容器内避免调用 embedding API）：  
   `CREWAI_USE_FILE_KNOWLEDGE=false`  
   此时不从 `knowledge/` 建向量索引；`CAS_Weapons_Bible.md` 全文由 `main.py` 注入到任务变量 **`cas_weapons_bible`**（见 `forge_specific_weapons_task`）。`world_lore` 仍从 `knowledge/report.md` 读取。

