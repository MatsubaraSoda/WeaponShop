进入容器

```bash
docker exec -it crewai-nexus_lore_agency bash
```

先下载全局的 `crewai`

```bash
pip install crewai
```

然后使用 `crewai` 指令创建项目

```bash
crewai create crew project
```

进入项目并初始化 `uv`

```bash
cd project
uv sync
```

跑一次官方的测试命令

```bash
uv run crewai test -n 1 -m gemini-3.1-pro-preview
```