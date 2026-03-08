# src/day3_agent.py
import os
import asyncio
import json
import re
from openai import AsyncOpenAI
from pydantic import BaseModel, ConfigDict
from dotenv import load_dotenv

from prompts import WORKFLOW_PLANNER_SYSTEM
from tools.base import tool_registry

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

class TaskStep(BaseModel):
    step_name: str = "未知步骤"
    tool_required: str = "other"
    reasoning: str = ""

class WorkflowPlan(BaseModel):
    model_config = ConfigDict(extra='ignore')
    goal: str = ""
    steps: list = []  # 保持为 list，手动处理

class WorkflowAgent:
    async def plan(self, user_goal):
        completion = await client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": WORKFLOW_PLANNER_SYSTEM},
                {"role": "user", "content": user_goal}
            ],
            max_tokens=1000,
            temperature=0.3
        )
        
        content = completion.choices[0].message.content
        json_match = re.search(r'\{[\s\S]*\}', content)
        json_str = json_match.group() if json_match else content
        
        return WorkflowPlan(**json.loads(json_str))
    
    async def execute_step(self, step):
        # ✅ 修复：先判断类型
        if isinstance(step, dict):
            tool_name = step.get("tool_required", "other")
            step_name = step.get("step_name", "未知步骤")
        else:
            tool_name = step.tool_required
            step_name = step.step_name
        
        print(f"\n⚙️  执行：{step_name}")
        print(f"   工具：{tool_name}")
        
        try:
            tool = tool_registry.get(tool_name)
            result = await tool.execute(query=step_name)
            print(f"   ✅ 成功")
            return result
        except Exception as e:
            print(f"   ⚠️  跳过：{e}")
            return {"status": "skipped"}
    
    async def run(self, user_goal):
        print("=" * 50)
        print(f"🎯 目标：{user_goal}")
        print("=" * 50)
        
        plan = await self.plan(user_goal)
        print(f"\n📋 计划生成：{len(plan.steps)} 个步骤")
        
        for i, step in enumerate(plan.steps, 1):
            print(f"\n--- 步骤 {i} ---")
            await self.execute_step(step)
        
        print("\n🎉 完成！")

async def main():
    agent = WorkflowAgent()
    await agent.run("帮我整理本周的工作周报")

if __name__ == "__main__":
    asyncio.run(main())