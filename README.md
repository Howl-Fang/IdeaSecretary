# IdeaSecretary (烂笔头) - AI 自动知识整理系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)]()
[![React: 18.2](https://img.shields.io/badge/React-18.2-61dafb.svg)]()

一个智能知识整理系统，帮助用户快速记录、组织和管理想法。通过 AI 的力量，自动整理用户输入的内容，并提供灵感建议和知识网络可视化。

## 🎯 核心功能

- **💬 智能输入**: 支持文本、语音、图片等多种输入方式
- **🤖 AI 整理**: 使用 OpenAI API 自动组织和增强想法
- **🌳 知识树**: 灵活的树形结构管理想法之间的关系
- **🔍 快速搜索**: 全文搜索和语义搜索支持
- **📚 多库管理**: 支持创建和管理多个独立的知识库
- **🌍 国际化**: 完整的中英文支持
- **🎨 主题切换**: 深色/浅色模式自适应
- **💾 自动备份**: 定期自动备份数据库
- **📤 数据导出**: 支持将库导出为 ZIP 格式

## 📋 项目结构

```
IdeaSecretary/
├── backend/                 # Flask 后端服务
│   ├── app/
│   │   ├── models/         # SQLAlchemy ORM 模型
│   │   ├── routes/         # API 路由和接口
│   │   └── utils/          # 工具函数和 AI 提示词
│   ├── tests/              # 单元测试
│   └── config.py           # 应用配置
├── frontend/               # React 前端应用
│   ├── src/
│   │   ├── pages/          # 页面组件
│   │   ├── components/     # 可复用组件
│   │   └── i18n.js         # 国际化配置
│   └── package.json        # NPM 依赖
├── data/                   # 数据存储目录
│   ├── backups/            # 数据库备份
│   ├── media/              # 媒体资源
│   └── media_trash/        # 媒体回收站
└── product_document/       # 产品文档
    ├── DEVELOPMENT_GUIDE.md
    ├── API_REFERENCE.md
    └── REQUIREMENTS_ANALYSIS.md
```

## 🚀 快速开始

### 前置要求

- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 后端设置

```bash
cd backend

# 运行设置脚本
chmod +x setup.sh
./setup.sh

# 激活虚拟环境
source .venv/bin/activate

# 启动服务器
python run.py
```

后端将在 `http://localhost:5000` 上运行。

### 前端设置

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm start
```

前端将在 `http://localhost:3000` 上运行。

## 🔧 配置

### 后端环境变量 (backend/.env)

```bash
# Flask 配置
FLASK_ENV=development
FLASK_APP=run.py
PORT=5000

# 数据库配置
DATABASE_URL=sqlite:////path/to/idea_secretary.db

# OpenAI 配置
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_API_BASE=https://api.openai.com/v1

# 安全配置
SECRET_KEY=your-secret-key-change-in-production
```

### 前端配置 (frontend/src/config.js)

```javascript
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
```

## 📚 API 文档

详见 [API_REFERENCE.md](./product_document/API_REFERENCE.md)

主要端点：
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET/POST /api/ideas/libraries` - 库管理
- `GET/POST/PUT/DELETE /api/ideas/<library_id>` - 想法管理
- `POST /api/ai/organize` - AI 整理想法
- `POST /api/ai/inspire` - 获取 AI 灵感

## 🗄️ 数据模型

### User (用户)
- 用户认证和偏好设置
- OpenAI API 密钥管理

### IdeaLibrary (知识库)
- 树形想法集合
- 统计信息维护

### Idea (想法)
- Markdown 格式内容
- 树形层级结构
- AI 增强信息

### MediaResource (媒体)
- 图片、附件等资源
- 回收站管理

### IndexRecord (索引)
- 快速搜索支持
- 定期重建优化

详见 [DEVELOPMENT_GUIDE.md](./product_document/DEVELOPMENT_GUIDE.md#数据模型设计)

## 🤖 AI 功能

系统使用 OpenAI API 提供以下 AI 功能：

1. **想法组织**: 自动结构化和改进输入的想法
2. **灵感生成**: 基于现有想法推荐新的角度和方向
3. **智能搜索**: 语义相似度搜索（可选）

提示词模板位于 `backend/app/utils/prompts.py`

## 📊 数据库

使用 SQLite 数据库，通过 SQLAlchemy ORM 管理。

### 自动化维护

- **备份**: 每 100 次操作自动备份
- **清理**: 定期清理 30+ 天前的回收站文件
- **索引重建**: 支持库的重新平衡和索引优化

## 🧪 测试

```bash
cd backend
pytest tests/
```

## 📖 文档

- [开发指南](./product_document/DEVELOPMENT_GUIDE.md) - 详细的开发说明
- [API 参考](./product_document/API_REFERENCE.md) - 完整的 API 文档
- [需求分析](./product_document/REQUIREMENTS_ANALYSIS.md) - 产品需求和改进建议
- [变更日志](./product_document/CHANGELOG.md) - 项目进度和版本历史

## 🎨 UI 特性

- ✅ 中英文完整支持 (i18next)
- ✅ 深色/浅色主题切换
- ✅ Material-UI 设计系统
- ✅ 响应式布局
- ✅ 平滑动画效果
- ⚠️ 语音输入集成 (开发中)
- ⚠️ 图片上传 (开发中)

## 🔮 路线图

### v0.2 (当前) - MVP
- [x] 基础框架搭建
- [x] 用户认证
- [x] CRUD 操作
- [x] AI 整理框架
- [ ] 前端 UI 完善
- [ ] 集成测试

### v0.3 - 核心功能增强
- [ ] 语音输入
- [ ] 图片上传
- [ ] URL 导入
- [ ] 高级搜索
- [ ] 数据导出

### v0.4+ - 高级特性
- [ ] JWT 认证增强
- [ ] 用户协作
- [ ] 高级 AI 功能
- [ ] 移动应用
- [ ] 浏览器扩展

## 💡 改进建议

详见 [REQUIREMENTS_ANALYSIS.md](./product_document/REQUIREMENTS_ANALYSIS.md#改进建议)

关键改进方向：
1. 安全性增强 (JWT 认证、密码强度)
2. 性能优化 (缓存、分页、虚拟列表)
3. 并发控制 (乐观锁机制)
4. 数据导入/导出 (多格式支持)
5. 高级 AI 功能 (问答、推荐、总结)

## 🤝 贡献

欢迎提交问题和改进建议！

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件

## 👨‍💻 作者

**Howl-Fang** - [GitHub](https://github.com/Howl-Fang)

## 🔗 相关链接

- [项目 GitHub](https://github.com/Howl-Fang/IdeaSecretary)
- [作者博客](https://howl-fang.github.io)

---

**项目版本**: 0.2.0  
**最后更新**: 2026年04月08日
