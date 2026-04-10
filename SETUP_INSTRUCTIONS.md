# IdeaSecretary 完整安装指南

## 系统要求

### 最小配置
- CPU: 2核+
- 内存: 2GB+
- 存储: 1GB+

### 软件要求
- Python 3.8 或更高版本
- Node.js 16 或更高版本  
- npm 8 或更高版本
- Git

### 操作系统支持
- ✅ Linux (Ubuntu, Debian, CentOS 等)
- ✅ macOS
- ✅ Windows (WSL2 推荐)

---

## 安装步骤

### 1. 克隆项目

```bash
# 如果尚未克隆
git clone https://github.com/your-repo/IdeaSecretary.git
cd IdeaSecretary
```

### 2. 后端设置

```bash
cd backend

# 创建 Python 虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Linux/macOS:
source venv/bin/activate

# Windows (PowerShell):
venv\Scripts\Activate.ps1

# Windows (cmd):
venv\Scripts\activate.bat
```

### 3. 安装 Python 依赖

```bash
# 确保虚拟环境已激活
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
# 复制示例文件
cp .env.example .env

# 编辑 .env 文件 (可选,默认值已可用)
nano .env
```

示例 `.env`:
```
FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///ideasecretary.db
JWT_SECRET_KEY=your-jwt-secret-key-here
```

### 5. 创建数据库和测试数据

```bash
# 使用 Python 脚本创建数据库和示例数据
python create_test_data.py

# 或手动创建空数据库:
python -c "from app import create_app; app = create_app(); print('Database initialized!')"
```

### 6. 启动后端服务器

```bash
# 开发模式
python app.py

# 生产模式 (使用 gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

✅ 后端运行在: http://localhost:5000

---

### 7. 前端设置

在新的终端窗口中:

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm start
```

✅ 前端运行在: http://localhost:3000

---

## 验证安装

### 1. 检查后端

```bash
curl http://localhost:5000/api/health
```

预期响应:
```json
{
  "status": "healthy",
  "timestamp": "2026-04-10T10:00:00.000000"
}
```

### 2. 检查前端

在浏览器中打开: http://localhost:3000

应该看到登录页面。

### 3. 测试登录

使用以下凭据:
- 用户名: `demo`
- 密码: `demo123456`

---

## Docker 安装 (可选)

### 先决条件
- Docker 20.10+
- Docker Compose 1.29+

### 安装步骤

```bash
cd /path/to/IdeaSecretary

# 构建并启动服务
docker-compose up --build

# 后台运行
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

✅ 访问:
- 前端: http://localhost:3000
- 后端: http://localhost:5000

---

## 故障排除

### 问题 1: Python 不找到

```bash
# 检查 Python 版本
python --version

# 如果不存在,使用 python3
python3 --version
```

### 问题 2: pip 命令不找到

```bash
# 尝试
python -m pip install -r requirements.txt

# 或升级 pip
python -m pip install --upgrade pip
```

### 问题 3: Node 模块安装失败

```bash
# 清理缓存
npm cache clean --force

# 删除已有的模块
rm -rf node_modules package-lock.json

# 重新安装
npm install
```

### 问题 4: 端口被占用

```bash
# Linux/macOS - 查找占用进程
lsof -i :5000
lsof -i :3000

# Windows - 查找占用进程
netstat -ano | findstr :5000

# 杀死进程 (Linux/macOS)
kill -9 <PID>

# 杀死进程 (Windows PowerShell)
Stop-Process -Id <PID> -Force
```

### 问题 5: 数据库错误

```bash
# 重置数据库
cd backend
rm ideasecretary.db
rm ideasecretary.db-journal

# 重新初始化
python create_test_data.py
```

### 问题 6: WSL 上的前端错误

✅ 已修复! 使用:
```bash
npm start
# 或显式设置
BROWSER=none npm start
```

---

## 配置 API 连接

### 前端连接到不同的后端

编辑 `frontend/.env.local`:

```
REACT_APP_API_URL=http://your-backend-url:5000/api
```

重启前端服务器使更改生效。

---

## 生产部署检查清单

- [ ] 更改 `FLASK_ENV` 为 `production`
- [ ] 更新 `SECRET_KEY` 和 `JWT_SECRET_KEY` (强随机字符串)
- [ ] 配置数据库 (PostgreSQL 推荐)
- [ ] 设置 HTTPS/TLS
- [ ] 配置反向代理 (nginx 推荐)
- [ ] 启用 CORS 白名单
- [ ] 配置日志记录
- [ ] 设置监控和告警
- [ ] 备份策略
- [ ] 性能优化

详见 DEVELOPMENT.md

---

## 开发工具

### 推荐的 IDE
- **VS Code** (推荐)
- PyCharm (Python)
- WebStorm (JavaScript)

### VS Code 扩展
- Python
- ES7+ React/Redux/React-Native snippets
- Prettier - Code formatter
- REST Client
- SQLite
- Tailwind CSS IntelliSense

### 有用的命令

```bash
# 查看日志
npm start --verbose

# 运行测试
npm test

# 构建生产版本
npm run build

# 代码格式化
npm run format

# 代码检查
npm run lint
```

---

## 常见命令速查

```bash
# 后端
cd backend
source venv/bin/activate          # 激活虚拟环境
python app.py                     # 启动开发服务器
python create_test_data.py        # 创建测试数据
pytest                            # 运行测试

# 前端
cd frontend
npm install                       # 安装依赖
npm start                         # 启动开发服务器
npm build                         # 构建生产版本
npm test                          # 运行测试

# Docker
docker-compose up                 # 启动服务
docker-compose down               # 停止服务
docker-compose logs -f            # 查看日志
```

---

## 下一步

1. 📖 阅读 README.md 了解项目概览
2. 📚 查看 DEVELOPMENT.md 获取详细指南
3. 🚀 按照 QUICKSTART.md 快速开始
4. 💡 在 Treasury 创建你的第一个想法!

---

**安装成功! 享受使用 IdeaSecretary! 🎉**
