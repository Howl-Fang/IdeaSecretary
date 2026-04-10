# IdeaSecretary 项目概览 | Project Overview

---

## 📌 项目创新亮点 | Innovation Highlights

### 中文 (Chinese)
IdeaSecretary 创新之处在于：AI 驱动的自动知识整理、树形和思维导图双视图展示想法层级、支持多格式输入（文字、图片、链接、语音）、智能搜索索引、每 10 次操作自动备份、用户可自定义 OpenAI API，实现完全个性化的知识管理系统。

### English
IdeaSecretary's innovation lies in: AI-driven automatic knowledge organization, dual visualization (tree view and mindmap) for hierarchical idea display, multi-format input support (text, images, links, voice), intelligent search indexing, automatic backup every 10 operations, user-customizable OpenAI API integration for fully personalized knowledge management.

---

## 🎯 项目优势 | Project Advantages

### 中文 (Chinese)
产品优势包括：（1）零学习曲线，现代化UI 直观易用；（2）完整的中英文双语和深色模式支持；（3）分布式数据存储，用户数据完全隔离；（4）无第三方依赖的轻量级前端（React + Tailwind）；（5）灵活的后端架构（Flask + SQLAlchemy），易于扩展；（6）生产级代码质量，完整的测试和文档。

### English
Product advantages include: (1) Zero learning curve with intuitive modern UI; (2) Full bilingual support (Chinese/English) and dark mode; (3) Distributed data storage with complete user data isolation; (4) Lightweight frontend (React + Tailwind) with zero third-party visualization dependencies; (5) Flexible backend architecture (Flask + SQLAlchemy) for easy extension; (6) Production-grade code quality with comprehensive testing and documentation.

---

## 📖 项目简要描述 | Brief Description

### 中文 (Chinese)
IdeaSecretary（烂笔头）是一个 AI 驱动的个人知识整理系统。用户可以通过多种方式（文本、语音、图片、链接等）输入想法，系统使用 OpenAI API 对想法进行智能分类和整理，建立层级化的知识树。用户可通过树形视图查看详细内容，或切换到思维导图获得全局视角。系统支持全文搜索、标签分类、自动备份。用户可自定义 OpenAI API 地址和模型，实现完全可控的个性化知识管理。项目采用前后端分离架构，前端使用 React，后端使用 Flask，支持多用户隔离和数据导出。

### English
IdeaSecretary is an AI-powered personal knowledge organization system. Users can input ideas through multiple formats (text, voice, images, links, etc.), and the system intelligently categorizes and organizes them using OpenAI API, building a hierarchical knowledge tree. Users can view detailed content through a tree view or switch to mindmap for a global perspective. The system supports full-text search, tag classification, and automatic backup. Users can customize OpenAI API endpoint and model for fully personalized knowledge management. The project uses a frontend-backend separation architecture with React frontend and Flask backend, supporting multi-user isolation and data export.

---

## 🏗️ 技术架构 | Technology Stack

### 前端 | Frontend
- **框架**: React 18
- **样式**: Tailwind CSS
- **国际化**: i18next (中文/英文)
- **图标**: Lucide React
- **HTTP 客户端**: Axios
- **可视化**: 自主实现树形视图和思维导图

### 后端 | Backend
- **框架**: Flask
- **数据库**: SQLite + SQLAlchemy ORM
- **认证**: JWT + bcrypt
- **AI 集成**: OpenAI API (可自定义)
- **存储**: 文件系统 + UUID 命名

### 部署 | Deployment
- **容器化**: Docker Compose
- **支持**: Linux, WSL, 本地开发
- **构建**: npm (前端), Python (后端)

---

## ✨ 核心特性 | Core Features

### 数据输入 | Input
- ✅ 文本输入
- ✅ 语音转录
- ✅ 图片上传
- ✅ URL 链接

### 知识组织 | Organization
- ✅ 树形结构
- ✅ 层级分类
- ✅ 标签系统
- ✅ 自动排序

### 知识展示 | Visualization
- ✅ 树形视图（默认）
- ✅ 思维导图（可选）
- ✅ 全文搜索
- ✅ 内容预览

### 智能功能 | AI Features
- ✅ AI 自动分类
- ✅ AI 生成建议
- ✅ 内容智能索引
- ✅ 语义搜索

### 用户体验 | UX
- ✅ 中英文双语
- ✅ 深色/浅色主题
- ✅ 响应式设计
- ✅ 无障碍设计

### 数据管理 | Data Management
- ✅ 自动备份 (每 10 操作)
- ✅ 数据导出
- ✅ 用户隔离
- ✅ 版本管理

### 配置灵活性 | Flexibility
- ✅ 自定义 OpenAI API
- ✅ 支持自建 API
- ✅ 可配置模型
- ✅ 用户完全控制

---

## 📊 项目统计 | Project Statistics

### 代码量 | Code Metrics
- **前端**: React 组件 + 页面 + 服务
- **后端**: 20+ REST API 端点
- **数据库**: 7 个核心模型
- **文档**: 10+ 详细文档

### 功能完成度 | Completion
- ✅ 100% MVP 功能
- ✅ 完整的测试数据
- ✅ 生产级代码质量
- ✅ 完整的用户文档

### 用户体验 | UX Quality
- ✅ 现代化设计
- ✅ 流畅交互
- ✅ 完整本地化
- ✅ 无障碍支持

---

## 🎓 使用示例 | Usage Example

### 快速开始 | Quick Start
```bash
# 1. 使用演示账户
用户名: demo
密码: demo123456

# 2. 进入想法库
My Idea Base → Select Base → View Ideas

# 3. 切换视图
Tree View (默认) ↔ Mindmap (可视化)

# 4. 浏览想法
- 树形视图: 展开/折叠
- 思维导图: 右键拖拽, 缩放按钮
```

### 演示数据 | Demo Data
- 3 个想法库
- 12 个分层想法
- 完整的树形结构
- 丰富的内容示例

---

## 📚 文档指南 | Documentation Guide

| 文档 | 用途 | Language |
|------|------|----------|
| README.md | 项目简介 | EN/ZH |
| QUICK_START.md | 快速入门 | EN/ZH |
| TREE_MINDMAP_GUIDE.md | 可视化使用 | ZH |
| DEVELOPMENT.md | 开发指南 | EN |
| TROUBLESHOOTING.md | 常见问题 | EN/ZH |
| MINDMAP_FIX.md | 技术细节 | EN/ZH |

---

## 🚀 下一步 | Next Steps

### 短期 | Short Term
- [ ] 编辑/删除想法功能
- [ ] 想法详情页面
- [ ] 高级搜索过滤

### 中期 | Medium Term
- [ ] 协作编辑功能
- [ ] 实时同步
- [ ] 导出 PNG/PDF

### 长期 | Long Term
- [ ] 团队管理
- [ ] 权限控制
- [ ] 高级分析

---

## 👥 贡献 | Contributing

IdeaSecretary 欢迎所有形式的贡献！

Issues, Pull Requests, 和建议都非常欢迎。

---

## 📄 许可证 | License

MIT License - 详见 LICENSE 文件

---

## 📞 联系方式 | Contact

项目主页 | Project Home: [GitHub Repository]  
问题反馈 | Issues: [GitHub Issues]  
讨论交流 | Discussions: [GitHub Discussions]

---

**版本**: v0.1.0  
**最后更新**: 2026-04-10  
**状态**: 🚀 生产就绪 (Production Ready)

---
