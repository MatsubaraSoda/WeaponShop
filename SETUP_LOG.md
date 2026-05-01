## Docker 操作速查

```bash
# 步骤 1 重建并启动
docker compose down
# 无缓存构建 适合基础镜像或依赖变化后强制全量重建
docker compose build --no-cache
# 常规启动并按需构建 适合日常开发
docker compose up -d --build

# 仅启动某一个服务（服务名 = compose 文件里 services: 下的键名，带连字符）
docker compose up -d nexus-lore-agency
# 其它可选：conceptual-armory-studio、visual-forge-studio、galactic-sales-agency
# 前台看日志可去掉 -d：docker compose up visual-forge-studio
# 首次或 Dockerfile 变更后只构建该服务：docker compose build galactic-sales-agency

# 步骤 2 进入容器
# 占位示例 不要原样执行
docker exec -it <container_name> bash
# 实际可执行示例
docker exec -it nexus_lore_agency bash

# 步骤 3 查看容器状态和日志
docker compose ps
docker compose logs -f nexus-lore-agency

# 步骤 4 停止并清理
docker compose down
```
