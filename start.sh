#!/bin/bash

# 袜子个性化设计系统启动脚本

echo "🚀 启动袜子个性化设计系统..."

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "❌ 错误: 虚拟环境不存在，请先创建虚拟环境"
    exit 1
fi

# 激活虚拟环境
echo "📦 激活虚拟环境..."
source venv/bin/activate

# 检查Python是否可用
if ! command -v python &> /dev/null; then
    echo "❌ 错误: Python命令不可用"
    exit 1
fi

echo "✅ Python版本: $(python --version)"

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "⚠️  警告: 未找到.env文件"
    echo "请创建.env文件并设置DOUBAO_API_TOKEN"
fi

# 启动应用
echo "🌐 启动Flask应用..."
python train.py

