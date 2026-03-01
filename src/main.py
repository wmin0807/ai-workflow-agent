# src/main.py
import os
import asyncio
from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

# 加载 .env 环境变量
load_dotenv()

# ============ 配置千问客户端 ============
client = AsyncOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# ============ 定义 Pydantic 数据模型 ============
class TaskStep(BaseModel):
    """工作流中的单个步骤"""
    step_name: str = Field(description="步骤名称，如'搜索信息'")
    tool_required: str = Field(description="需要使用的工具，如'google_search'")
    reasoning: str = Field(description="为什么需要这一步")

class WorkflowPlan(BaseModel):
    """完整的工作流计划"""
    goal: str = Field(description="任务目标")
    steps: List[TaskStep] = Field(description="执行步骤列表")

async def generate_plan(user_goal: str) -> WorkflowPlan:
    """调用千问生成工作流计划（增强版）"""
    try:
        completion = await client.chat.completions.create(
            model="qwen-max",
            messages=[
                {
                    "role": "system",
                    "content": """你是一个 JSON 输出机器。
                    你只能输出纯 JSON，不能有任何其他文字。
                    不要输出"好的"、"以下是"等任何解释性文字。
                    JSON 格式必须严格符合以下 Schema：
                    {
                        "goal": "任务目标",
                        "steps": [
                            {"step_name": "步骤名", "tool_required": "工具名", "reasoning": "理由"}
                        ]
                    }"""
                },
                {
                    "role": "user",
                    "content": f"请为以下目标制定执行计划：{user_goal}"
                }
            ],
            temperature=0.3,  # 降低随机性，让输出更稳定
            max_tokens=1000
        )
        
        # 🔍 关键：先检查响应结构
        if not completion.choices or len(completion.choices) == 0:
            raise Exception("API 返回为空，没有 choices")
        
        content = completion.choices[0].message.content
        
        # 🔍 打印原始内容，方便调试
        print(f"🔍 千问原始回复 ({len(content) if content else 0} 字符):")
        print("-" * 40)
        print(content if content else "[CONTENT IS EMPTY]")
        print("-" * 40)
        
        # 🔍 检查 content 是否为空
        if not content or content.strip() == "":
            raise Exception("千问返回的 content 为空，可能是 API 调用失败")
        
        # 🔍 尝试提取 JSON（处理模型可能包裹文字的情况）
        import json
        import re
        
        # 尝试直接解析
        try:
            plan_dict = json.loads(content)
        except json.JSONDecodeError:
            # 如果失败，尝试用正则提取 JSON 块
            print("⚠️ 直接解析失败，尝试提取 JSON 块...")
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                json_str = json_match.group()
                print(f"📦 提取到 JSON: {json_str[:100]}...")
                plan_dict = json.loads(json_str)
            else:
                raise Exception(f"无法从回复中提取 JSON，原始内容：{content[:200]}")
        
        # 用 Pydantic 验证并转换
        plan = WorkflowPlan(**plan_dict)
        return plan
        
    except Exception as e:
        print(f"❌ 调用失败：{e}")
        print(f"🔍 完整响应：{completion if 'completion' in locals() else 'N/A'}")
        raise

# ============ 主入口 ============
async def main():
    print("=" * 60)
    print("🚀 AI Workflow Agent - Day 1 环境验证")
    print("=" * 60)
    
    # 测试目标
    test_goal = "帮我分析特斯拉近一周的舆情并生成报告"
    print(f"\n🎯 测试目标：{test_goal}\n")
    
    # 调用千问生成计划
    print("⏳ 正在调用千问 API 生成计划...\n")
    plan = await generate_plan(test_goal)
    
    # 打印结构化结果
    print("=" * 60)
    print("✅ 成功生成工作流计划!")
    print("=" * 60)
    print(f"📌 目标：{plan.goal}")
    print(f"📋 步骤数量：{len(plan.steps)}")
    print("\n📝 详细步骤:")
    for i, step in enumerate(plan.steps, 1):
        print(f"  {i}. [{step.tool_required}] {step.step_name}")
        print(f"     理由：{step.reasoning}")
    print("=" * 60)
    print("🎉 Day 1 环境验证完成!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())