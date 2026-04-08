# IdeaSecretary 开发指南

## 项目概述

IdeaSecretary（烂笔头）是一个 AI 自动知识整理系统，帮助用户快速记录和组织想法，并通过 AI 进行智能整理和提示灵感。

## 项目结构

```
IdeaSecretary/
├── backend/              # Flask 后端
│   ├── app/
│   │   ├── models/      # 数据库模型（ORM）
│   │   ├── routes/      # API 路由
│   │   └── utils/       # 工具函数
│   ├── tests/           # 单元测试
│   ├── config.py        # 配置文件
│   ├── run.py           # 启动脚本
│   └── requirements.txt # 依赖管理
├── frontend/            # React 前端
│   ├── src/
│   │   ├── pages/       # 页面组件
│   │   ├── components/  # 可复用组件
│   │   ├── config.js    # 前端配置
│   │   └── i18n.js      # 国际化配置
│   └── package.json     # NPM 依赖
└── data/               # 数据存储
    ├── backups/        # 数据库备份
    ├── media/          # 媒体资源
    └── media_trash/    # 媒体回收站
```

## 技术栈

### 后端
- **框架**：Flask 3.0.0
- **数据库**：SQLite + SQLAlchemy ORM
- **AI 集成**：OpenAI API
- **认证**：Werkzeug security
- **CORS**：Flask-CORS

### 前端
- **框架**：React 18.2.0
- **路由**：React Router 6.0
- **UI 库**：Material-UI (MUI)
- **HTTP**：Axios
- **国际化**：i18next

## 开发步骤

### 1. 后端设置

```bash
cd backend
chmod +x setup.sh
./setup.sh
source .venv/bin/activate
python run.py
```

后端将在 `http://localhost:5000` 启动。

### 2. 前端设置

```bash
cd frontend
npm install
npm start
```

前端将在 `http://localhost:3000` 启动。

## 数据模型设计

### User（用户）
- id: 主键
- username: 用户名（唯一）
- email: 邮箱（唯一）
- password_hash: 密码哈希
- openai_api_key: 用户的 OpenAI API 密钥
- openai_api_base: 自建 API 地址
- language: 语言偏好（en/zh）
- theme: 主题偏好（light/dark）

### IdeaLibrary（想法库）
- id: UUID 主键
- user_id: 所有者
- name: 库名
- description: 描述
- is_default: 是否为默认库
- total_ideas: 想法总数
- total_words: 单词总数

### Idea（想法）
- id: UUID 主键
- library_id: 所属库
- parent_id: 父想法 ID（用于树形结构）
- title: 标题
- content: 内容（Markdown格式）
- ai_thoughts: AI 处理后的想法
- status: 状态（draft/organized/refined）
- word_count: 字数统计

### MediaResource（媒体资源）
- id: UUID 主键
- library_id: 所属库
- filename: 原始文件名
- file_path: 存储路径（UUID 命名）
- mime_type: 文件类型
- file_size: 文件大小
- status: 状态（active/trash）
- url: 外部资源 URL

### IndexRecord（索引记录）
- id: 主键
- library_id: 所属库
- idea_id: 关联想法
- search_text: 搜索文本
- is_stale: 是否过期

## API 端点

### 认证相关
- `POST /api/auth/register` - 注册用户
- `POST /api/auth/login` - 用户登录

### 想法库相关
- `GET /api/ideas/libraries` - 获取用户的所有库
- `POST /api/ideas/libraries` - 创建新库
- `GET /api/ideas/<library_id>` - 获取库内的想法
- `POST /api/ideas/<library_id>` - 添加新想法
- `PUT /api/ideas/<idea_id>` - 更新想法
- `DELETE /api/ideas/<idea_id>` - 删除想法

### AI 功能
- `POST /api/ai/organize` - 使用 AI 组织想法
- `POST /api/ai/inspire` - 获取 AI 灵感
- `GET /api/ai/search` - 搜索想法

### 账户相关
- `GET /api/account/profile/<user_id>` - 获取用户资料
- `PUT /api/account/profile/<user_id>` - 更新用户资料
- `GET /api/account/openai-config/<user_id>` - 获取 OpenAI 配置
- `PUT /api/account/openai-config/<user_id>` - 设置 OpenAI 配置

## AI 提示词策略

系统预设了多个场景下的 AI 提示词，位于 `backend/app/utils/prompts.py`：

1. **ORGANIZE_IDEA_SYSTEM_PROMPT** - 用于组织和增强想法
2. **INSPIRATION_SYSTEM_PROMPT** - 用于生成灵感
3. **SUMMARIZE_IDEAS_SYSTEM_PROMPT** - 用于总结多个想法
4. **CHAT_SYSTEM_PROMPT** - 用于一般聊天交互

## 维护和备份

### 自动备份
- 每隔 100 次操作自动备份数据库
- 备份文件保存在 `data/backups/` 目录
- 自动保留最近 10 个备份

### 清理回收站
- 定期清理回收站中超过 30 天的文件
- 执行时机：库重新平衡时

### 索引重建
- 支持库的重新平衡，优化搜索索引
- 标记过期的索引记录
- 重新生成所有想法的搜索文本

## 功能实现优先级

### 第一阶段（MVP）
- [x] 用户认证（注册/登录）
- [x] 创建/编辑想法
- [x] 基本的树形结构
- [x] AI 组织想法
- [ ] 前端完整 UI
- [ ] 数据库集成测试

### 第二阶段
- [ ] 语音输入
- [ ] 图片上传和识别
- [ ] 思维导图导出
- [ ] URL 内容提取
- [ ] 高级搜索
- [ ] 批量操作

### 第三阶段
- [ ] 用户分享和协作
- [ ] 多种知识库导入格式
- [ ] 高级 AI 功能（问答、推荐）
- [ ] 移动应用
- [ ] 浏览器扩展

## 开发建议

1. **代码质量**
   - 遵循 PEP 8（Python）和 ESLint（JavaScript）
   - 编写单元测试覆盖关键功能
   - 使用类型提示（Python）和 PropTypes（React）

2. **性能优化**
   - 实现数据库查询优化和缓存
   - 前端使用虚拟滚动处理大数据集
   - 异步加载和分页

3. **安全性**
   - 所有 API 端点需要身份验证
   - 验证和清理用户输入
   - 加密存储敏感信息
   - HTTPS 部署

4. **用户体验**
   - 保持 UI 简洁直观
   - 提供清晰的错误提示
   - 支持键盘快捷键
   - 确保响应式设计

5. **国际化**
   - 所有文本都使用 i18n
   - 提供中英文支持
   - 考虑其他语言的扩展

## 需求合理性分析

✅ **合理的需求**
- 想法快速输入和组织确实是必要的
- AI 辅助组织能提升效率
- 树形结构适合知识管理

⚠️ **可改进的地方**
1. **认证机制**：建议添加更强的身份验证（如 JWT token、刷新令牌）
2. **并发控制**：需要处理多用户同时编辑的冲突
3. **数据导入**：支持从其他应用导入（Notion、Obsidian 等）
4. **协作功能**：考虑添加多人编辑和评论功能
5. **版本控制**：记录想法的编辑历史

## 后续开发注意事项

- 完成前端所有页面的 UI 实现
- 实现完整的错误处理和验证
- 添加请求日志和监控
- 完善测试覆盖率
- 性能测试和优化
- 部署配置（Docker、CI/CD）
