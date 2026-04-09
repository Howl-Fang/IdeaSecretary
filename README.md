# IdeaSecretary - AI-Powered Knowledge Organization System

一个使用 AI 自动整理和组织用户想法的知识管理系统。用户可以通过文本、图片、链接等多种方式输入内容，系统自动进行分类、整理，并提供灵感建议。

## 🌟 核心特性

- **多源输入**：支持文本、语音、图片、链接输入
- **AI 知识整理**：基于 OpenAI API，自动分类和组织想法
- **知识库管理**：树形结构、思维导图展示、手动编辑
- **多库支持**：用户可创建多个独立知识库
- **智能建议**：根据现有想法生成创意灵感
- **数据导出**：支持 ZIP、思维导图等多种格式
- **国际化**：英文主体，中文适配
- **深浅色模式**：自动适配系统主题

## 🏗️ 项目结构

```
IdeaSecretary/
├── frontend/              # React + TypeScript 前端
│   ├── src/
│   │   ├── pages/        # 页面组件
│   │   ├── components/   # 可复用组件
│   │   ├── hooks/        # 自定义 Hook
│   │   ├── stores/       # Zustand 状态管理
│   │   ├── locales/      # 国际化文件
│   │   └── utils/        # 工具函数
│   └── vite.config.ts    # Vite 配置
├── backend/               # Node.js + Express 后端
│   ├── src/
│   │   ├── routes/       # API 路由
│   │   ├── models/       # 数据模型（待实现）
│   │   ├── middleware/   # 中间件
│   │   ├── config/       # 配置
│   │   └── utils/        # 工具函数
│   ├── db.ts             # 数据库初始化
│   └── index.ts          # 服务器入口
├── shared/                # 共享代码（待完善）
└── package.json           # 工作区根配置
```

## 🚀 快速开始

### 前置要求

- Node.js 18+
- npm 9+

### 安装依赖

```bash
npm install
```

### 环境配置

**后端**（`.env`）：
```bash
cp backend/.env.example backend/.env
# 编辑 backend/.env，填入 OpenAI API 密钥等
```

**前端**（`.env.local`）：
```bash
cp frontend/.env.example frontend/.env.local
```

### 开发模式

```bash
# 开发：启动前后端服务
npm run dev

# 前端（默认 http://localhost:5173）
cd frontend && npm run dev

# 后端（默认 http://localhost:3001）
cd backend && npm run dev
```

### 构建生产版本

```bash
npm run build
```

## 📋 API 文档

### 认证模块

#### 注册
```
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password",
  "name": "User Name"
}

Response: {
  "token": "jwt_token",
  "user": { "id": "uuid", "email": "...", "name": "..." }
}
```

#### 登录
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password"
}

Response: {
  "token": "jwt_token",
  "user": { "id": "uuid", "email": "...", "name": "..." }
}
```

### 认证头

所有受保护的 API 需要在请求头中包含 JWT：
```
Authorization: Bearer <jwt_token>
```

## 💾 数据库

SQLite 数据库包括以下表：

- **users** - 用户信息和认证
- **knowledge_bases** - 知识库管理
- **ideas** - 想法/笔记（树形结构）
- **media_resources** - 媒体资源管理
- **search_index** - 全文搜索索引

## 🔧 技术栈

### 前端
- **React 18** - UI 框架
- **TypeScript** - 类型安全
- **Vite** - 构建工具
- **Tailwind CSS** - 样式框架
- **React Router** - 路由管理
- **Zustand** - 状态管理
- **i18next** - 国际化
- **Axios** - HTTP 客户端

### 后端
- **Express** - Web 框架
- **SQLite** - 数据库
- **JWT** - 身份认证
- **bcryptjs** - 密码加密
- **OpenAI API** - AI 功能
- **express-validator** - 数据验证

## 📖 开发指南

### 代码风格

- 使用 TypeScript 进行类型安全开发
- 遵循 ES2020+ 语法
- 仅在必要时添加代码注释
- 使用有意义的变量和函数名

### 提交规范

提交信息遵循以下格式：
```
type: 简短描述

详细说明（可选）

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

Type 包括：
- `feat` - 新功能
- `fix` - 修复 bug
- `docs` - 文档
- `style` - 代码风格调整
- `refactor` - 代码重构
- `test` - 测试
- `chore` - 工程化相关

## 🗓️ 项目进度

### Phase 1：项目初始化与架构搭建 ✅
- [x] 初始化前端项目
- [x] 初始化后端项目
- [x] 配置项目结构和依赖

### Phase 2：身份认证系统（进行中）
- [x] 用户注册/登录功能
- [x] JWT 认证实现
- [ ] 用户会话管理
- [ ] 密码重置功能

### Phase 3+：待实现
详见项目计划文档

## 📝 相关文档

- [需求文档](./Documents/NEED.md) - 产品需求和功能规划
- [项目计划](../session-state/0771694a-cd63-42ce-bb4b-4b1e322c4f20/plan.md) - 详细实现计划

## 🔗 链接

- [GitHub Repository](https://github.com/Howl-Fang/IdeaSecretary)
- [Author Website](https://howl-fang.github.io)

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE)

## 💡 问题和建议

如有任何问题或建议，欢迎提交 Issue 或 Pull Request。
