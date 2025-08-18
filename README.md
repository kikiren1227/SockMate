# 🧦 袜子个性化设计应用

一个基于 AI 的个性化袜子设计应用，通过分析用户照片的风格特征，生成独一无二的袜子设计。

## ✨ 功能特点

- 📷 照片上传和风格分析
- 🤖 AI 生成个性化袜子设计描述
- 🎨 DALL·E 自动生成袜子设计图
- 💫 现代化的用户界面
- 📱 响应式设计，支持移动端

## 🚀 快速开始

### 1. 环境要求

- Python 3.8+
- OpenAI API 密钥

### 2. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，添加您的 OpenAI API 密钥
# OPENAI_API_KEY=your_actual_api_key_here
```

### 4. 运行应用

```bash
python train.py
```

访问 http://127.0.0.1:5000 开始使用！

## 📁 项目结构

```
Kiki test/
├── train.py              # 主应用文件
├── requirements.txt       # Python 依赖
├── .env.example          # 环境变量模板
├── .gitignore           # Git 忽略文件
├── templates/           # HTML 模板
│   ├── upload.html      # 上传页面
│   └── result.html      # 结果页面
└── static/              # 静态文件
    └── css/
        └── style.css    # 样式文件
```

## 🔧 API 配置

### OpenAI API

本应用使用以下 OpenAI 服务：
- **GPT-3.5-turbo**: 生成袜子设计描述
- **DALL·E**: 生成袜子设计图

请确保您的 OpenAI 账户有足够的 API 调用额度。

## 📝 使用说明

1. **上传照片**: 在首页上传您的照片
2. **风格分析**: 系统会分析您的照片风格（目前使用模拟数据）
3. **生成设计**: AI 会根据风格特征生成袜子设计描述
4. **图像生成**: DALL·E 会根据描述生成袜子设计图
5. **查看结果**: 您可以查看设计说明并下载设计图

## 🔮 未来计划

- [ ] 集成真实的计算机视觉模型进行风格分析
- [ ] 添加更多设计风格选项
- [ ] 支持批量设计
- [ ] 添加用户账户系统
- [ ] 集成在线商店功能

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
