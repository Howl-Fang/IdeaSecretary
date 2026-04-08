# IdeaSecretary MVP 产品文档（根据 NEED.md 生成）

更新日期：2026-04-08

## 1. 目标

构建一个可运行的单机版前后端分离 MVP，让用户可输入文本/链接/图片线索并自动整理为知识节点，支持问答、树结构浏览、导出与基础备份。

## 2. 范围

### In Scope（本次已实现）
- 多库管理（默认可创建一个或多个库）
- Idea 入库：标题 + 内容 + 来源类型
- AI 整理（有 key 走 OpenAI；无 key 走本地 fallback）
- 索引维护（入库后更新索引文本）
- 树结构 API
- 媒体资源 UUID 命名 + 回收站软删除
- 导出 zip + 导出 mindmap 文本
- 操作计数触发数据库备份
- UI：英语默认，支持中英切换 + 深浅色

### Out of Scope（后续迭代建议）
- 真正的多模态识别（OCR/图像理解）
- 语音输入与实时转写
- 完整认证系统（登录/注册）
- 复杂推荐与统计可视化

## 3. 技术方案

- Backend：FastAPI + SQLAlchemy + SQLite
- Frontend：静态 HTML/CSS/JS（后续可升级为 React/Vue）
- AI：OpenAI Responses API（官方/自建兼容）
- Storage：`data/` 下统一管理数据库、媒体、备份

## 4. 关键数据结构

- `libraries`：知识库
- `ideas`：知识节点（含 parent_id）
- `idea_index`：检索索引
- `media_assets`：媒体索引
- `operation_counter`：操作计数/备份触发

## 5. 边界与改进建议

1. **需求合理性**：当前需求方向完整，但首次版本建议先稳定“文本流”能力，再逐步上多模态。
2. **Prompt 稳定性**：已加入 JSON 解析失败回退；后续建议加入严格 schema 验证与重试策略。
3. **检索能力**：当前为 SQL LIKE，后续可升级 FTS5 / 向量检索。
4. **产品一致性**：当前 UI 为 MVP 线框实现，后续建议用组件库统一视觉。

## 6. 后续开发指导意见

- 优先级 P0：鉴权、数据迁移策略、异常监控
- 优先级 P1：OCR/语音、灵感推荐、统计模块
- 优先级 P2：多端同步、协作编辑

## 7. 需求确认问题（建议你确认）

1. 登录/注册优先采用邮箱密码，还是 OAuth（GitHub/Google）？
2. 你期望的“思维导图导出”格式是 Mermaid、XMind 还是 FreeMind？
3. 是否需要默认把 AI 输出强制成双语（中英同时）？
