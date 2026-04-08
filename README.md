# IdeaSecretary (MVP)

基于需求文档实现的 AI 自动知识整理系统 MVP，包含：
- FastAPI 后端（库管理、灵感整理、树结构、聊天、导出）
- SQLite + ORM 存储
- 媒体资源按 UUID 存储并支持回收站软删除
- 简单 Web UI（英语默认 / 中文切换，深浅色切换）

## Quick Start

1. 安装依赖

```bash
uv sync
```

2. 启动应用

```bash
uv run uvicorn app.main:app --reload
```

3. 打开浏览器访问

- `http://127.0.0.1:8000/`

## 环境变量（可选）

在仓库根目录创建 `.env`：

```bash
OPENAI_API_KEY=your_key_here
OPENAI_BASE_URL=
OPENAI_MODEL=gpt-4o-mini
BACKUP_EVERY_OPERATIONS=20
BACKUP_KEEP_LATEST=5
```

说明：
- 不配置 `OPENAI_API_KEY` 时，系统会采用本地 deterministic fallback。
- 支持通过 `OPENAI_BASE_URL` 指向自建 OpenAI 兼容接口。

## 目录说明

- `app/main.py`：应用入口
- `app/routers/`：API 路由
- `app/services/`：AI、索引、备份、导出、媒体管理
- `app/static/index.html`：介绍/仪表盘基础页面
- `data/`：SQLite、媒体、回收站、备份（运行时生成）

## Troubleshooting

- 如果出现依赖导入错误，请先执行 `uv sync` 重新同步环境。
- 如果 API 创建库返回 409，表示同名库已存在，可直接复用该库。
