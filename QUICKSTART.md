# 快速开始指南

## 🎯 5 分钟快速启动

### 方案 1：使用自动启动脚本 (推荐)

```bash
# 进入项目目录
cd /Users/lihaofang/Documents/IdeaSecretary

# 给脚本执行权限
chmod +x start.sh

# 运行启动脚本
./start.sh
```

脚本会自动：
- ✅ 检查 Python 和 Node.js
- ✅ 创建虚拟环境
- ✅ 安装所有依赖
- ✅ 启动后端服务器 (localhost:5000)
- ✅ 启动前端应用 (localhost:3000)

### 方案 2：手动启动

**终端 1 - 后端**
```bash
cd backend

# 首次运行
chmod +x setup.sh
./setup.sh

# 后续启动
source .venv/bin/activate
python run.py
```

后端将在 `http://localhost:5000` 上运行

**终端 2 - 前端**
```bash
cd frontend

# 首次运行
npm install

# 后续启动
npm start
```

前端将在 `http://localhost:3000` 上运行

## ⚙️ 初始配置

### 1. 配置 OpenAI API

编辑 `backend/.env`:

```bash
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_API_BASE=https://api.openai.com/v1
```

### 2. 创建初始数据库

后端首次运行时会自动创建数据库，位置：
```
/Users/lihaofang/Documents/IdeaSecretary/data/idea_secretary.db
```

### 3. 媒体文件夹

自动创建以下目录：
- `data/media/` - 存储媒体文件
- `data/media_trash/` - 回收站
- `data/backups/` - 数据库备份

## 📱 使用流程

1. **访问应用**
   - 打开浏览器: http://localhost:3000

2. **注册账户**
   - 点击 "Register"
   - 填写用户名、邮箱、密码
   - 点击 "Register"

3. **登录**
   - 使用注册的账户登录

4. **配置 OpenAI**
   - 进入 Settings
   - 输入 OpenAI API Key
   - (可选) 输入自建 API 地址

5. **开始记录想法**
   - 进入 Treasury
   - 输入想法内容
   - 点击 Submit 提交
   - AI 会自动组织你的想法

## 🔧 常见问题

### Q1: 后端无法启动
**错误信息**: `ModuleNotFoundError: No module named 'flask'`

**解决方案**:
```bash
cd backend
source .venv/bin/activate
pip install -r requirements.txt
```

### Q2: 前端无法启动
**错误信息**: `command not found: npm`

**解决方案**: 安装 Node.js
```bash
# macOS
brew install node

# 或访问 https://nodejs.org/ 下载安装
```

### Q3: OpenAI API 调用失败
**错误信息**: `Invalid API Key`

**解决方案**:
1. 确保 API Key 正确
2. 检查 API 额度是否充足
3. 在 Account 设置中重新配置

### Q4: 数据库错误
**错误信息**: `database is locked`

**解决方案**:
1. 确保只有一个后端实例运行
2. 删除 `data/idea_secretary.db-wal` 和 `data/idea_secretary.db-shm` 文件
3. 重启后端

## 📊 验证启动成功

### 后端检查
```bash
curl http://localhost:5000/api/auth/login -X POST
# 应该返回 400 (缺少参数，但说明后端在运行)
```

### 前端检查
- 访问 http://localhost:3000
- 应该看到登录页面

## 🛠️ 开发工具

### 查看日志
```bash
# 后端日志已打印到终端

# 前端日志在浏览器开发者工具 (F12) 中
```

### 数据库检查
```bash
# 使用 SQLite 浏览器
sqlite3 data/idea_secretary.db

# 查看表
.tables

# 查看用户
SELECT * FROM users;

# 退出
.exit
```

### API 测试
```bash
# 注册用户
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"123456"}'

# 登录
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"123456"}'
```

## 📚 下一步

- 📖 阅读 [DEVELOPMENT_GUIDE.md](./product_document/DEVELOPMENT_GUIDE.md)
- 🔌 查看 [API_REFERENCE.md](./product_document/API_REFERENCE.md)
- 💡 了解 [REQUIREMENTS_ANALYSIS.md](./product_document/REQUIREMENTS_ANALYSIS.md)

## ⚠️ 注意事项

1. **开发模式**：当前配置为开发模式，生产部署需要修改配置
2. **数据安全**：更改 `SECRET_KEY` 在生产环境中
3. **CORS**：前端跨域已启用，生产环境需要配置具体域名
4. **数据库**：使用 SQLite，大规模使用建议迁移到 PostgreSQL

## 🆘 需要帮助

- 📧 提交 Issue
- 📖 查看项目文档
- 💬 参考 API 文档

---

**最后更新**: 2026年04月08日
