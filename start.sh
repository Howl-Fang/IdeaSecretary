#!/bin/bash

# IdeaSecretary 快速启动脚本

echo "🚀 IdeaSecretary - AI Knowledge Organization System"
echo "================================================="
echo ""

# 检查是否安装了 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 未安装。请先安装 Python 3.8 或以上版本。"
    exit 1
fi

# 检查是否安装了 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装。请先安装 Node.js 16 或以上版本。"
    exit 1
fi

echo "✅ 检查通过：Python 3 和 Node.js 已安装"
echo ""

# 启动后端
echo "📦 启动后端服务器..."
cd backend

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv .venv
fi

# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
if [ ! -f ".backend_setup_done" ]; then
    echo "安装后端依赖..."
    pip install --upgrade pip
    pip install -r requirements.txt
    touch .backend_setup_done
fi

# 启动 Flask 服务器
echo ""
echo "🔧 后端服务器启动中..."
python run.py &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 启动前端
echo ""
echo "📦 启动前端应用..."
cd ../frontend

# 检查 node_modules
if [ ! -d "node_modules" ]; then
    echo "安装前端依赖..."
    npm install
fi

echo ""
echo "🎨 前端应用启动中..."
echo ""
echo "================================================="
echo "✨ 启动完成！"
echo ""
echo "📱 前端: http://localhost:3000"
echo "🔧 后端: http://localhost:5000"
echo ""
echo "💡 建议："
echo "1. 后端首次运行需要配置 .env 文件 (OPENAI_API_KEY 等)"
echo "2. 登录页面可以注册新用户"
echo "3. 在 Account 设置中配置 OpenAI API"
echo ""
echo "📚 文档："
echo "- 开发指南: product_document/DEVELOPMENT_GUIDE.md"
echo "- API 文档: product_document/API_REFERENCE.md"
echo "- README: README.md"
echo ""
echo "📖 按 Ctrl+C 停止服务"
echo "================================================="
echo ""

npm start

# 清理
kill $BACKEND_PID
