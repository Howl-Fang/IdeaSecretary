# IdeaSecretary - 快速开始指南

## 环境要求
- Python 3.8+
- Node.js 16+
- npm 或 yarn
- WSL/Linux/macOS 或 Windows PowerShell

---

## 快速启动 (3 分钟)

### 方式 1: 在 WSL/Linux 上启动

**终端 1 - 启动后端:**
```bash
cd /Projects/IdeaSecretary/backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 创建测试数据
python create_test_data.py

# 启动后端 (端口 5000)
python app.py
```

**终端 2 - 启动前端:**
```bash
cd /Projects/IdeaSecretary/frontend

# 安装依赖 (已安装可跳过)
npm install

# 启动前端 (端口 3000)
npm start
```

✅ 访问: http://localhost:3000

---

### 方式 2: Docker (推荐)

```bash
cd /Projects/IdeaSecretary

# 启动完整栈
docker-compose up

# 打开浏览器
# 前端: http://localhost:3000
# 后端: http://localhost:5000/api/health
```

停止: `Ctrl+C` 或 `docker-compose down`

---

## 测试账户

```
账户 1:
用户名: demo
密码: demo123456
邮箱: demo@ideasecretary.local

账户 2:
用户名: alice
密码: alice123456
邮箱: alice@ideasecretary.local
```

---

## 常见问题

### Q: 前端启动失败，显示 PowerShell 错误?
A: ✅ 已修复! 使用 `BROWSER=none npm start` 或直接 `npm start`

### Q: 后端显示 "ModuleNotFoundError"?
A: 需要安装依赖:
```bash
cd backend
pip install -r requirements.txt
```

### Q: 端口被占用?
```bash
# 查找占用端口的进程
lsof -i :5000   # 后端
lsof -i :3000   # 前端

# 杀死进程
kill -9 <PID>
```

### Q: 数据库错误?
```bash
# 重置数据库
cd backend
rm ideasecretary.db
python create_test_data.py
```

---

## 项目结构

```
IdeaSecretary/
├── backend/          # Flask Python 后端 ✅ 准备就绪
├── frontend/         # React JavaScript 前端 ✅ 已修复
├── docker-compose.yml ✅ Docker 部署
├── README.md         ✅ 完整文档
└── DEVELOPMENT.md    ✅ 详细指南
```

---

## 功能一览

### 后端 API (Python Flask)
✅ 用户认证 (JWT + bcrypt)  
✅ 想法管理 (树形结构)  
✅ 媒体管理 (上传/下载/删除)  
✅ OpenAI AI 集成  
✅ 自动备份系统  
✅ 全文搜索  
✅ 20+ REST 端点  

### 前端 UI (React)
✅ 登录/注册页面  
✅ Treasury (创建想法)  
✅ My Idea Base (浏览想法)  
✅ Account Settings (API 配置)  
✅ 深色/浅色模式  
✅ 中英文支持  
✅ 响应式设计  

### AI 功能
✅ 想法组织建议  
✅ 灵感生成  
✅ 想法总结  

---

## 下一步

### 本地开发
1. 启动后端和前端 (上面的步骤)
2. 打开 http://localhost:3000
3. 用 demo 账户登录
4. 开始创建想法!

### 生产部署
1. 查看 DEVELOPMENT.md 的部署章节
2. 或使用 Docker: `docker-compose up`

### 修改 API 地址
前端默认连接 `http://localhost:5000/api`

如需修改，编辑 `frontend/.env.local`:
```
REACT_APP_API_URL=https://your-api-url/api
```

---

## 更多文档

- **README.md** - 项目概览
- **DEVELOPMENT.md** - 详细开发指南
- **API 文档** - 见 backend/routes/

---

## 问题反馈

如遇到问题:
1. 查看上面的"常见问题"
2. 检查终端错误消息
3. 参考 DEVELOPMENT.md 的故障排除章节

---

**祝您使用愉快! 🚀**
