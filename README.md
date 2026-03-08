# AI Workflow Agent 🤖

一个基于通义千问大模型的自动化工作流 Agent。能够理解用户目标、自动规划执行步骤、调用工具完成任务。

## 功能特性

- 自然语言目标解析
- 自动工作流规划
- 工具调用执行（搜索/邮件/文件）
- 异步并发调用，性能提升 2-3 倍
- 对话记忆管理

## 技术栈

- **语言**: Python 3.14
- **大模型**: 通义千问 (Qwen-Max/Plus)
- **SDK**: OpenAI 兼容接口
- **数据验证**: Pydantic
- **包管理**: uv
- **异步框架**: asyncio

## 快速开始

### 前置要求

- Python 3.10+
- uv 包管理工具
- 阿里云 DashScope API Key

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/YOUR_USERNAME/ai-workflow-agent.git
cd ai-workflow-agent

# 2. 安装 uv（如未安装）
pip install uv

# 3. 安装项目依赖
uv sync

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 DASHSCOPE_API_KEY

# 5. 运行测试
uv run python src/day3_agent.py
