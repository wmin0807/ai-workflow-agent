# src/day2_concurrent.py
import os
import asyncio
import time
import json
import re
from openai import AsyncOpenAI
from pydantic import BaseModel, Field, ConfigDict
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# ============ Pydantic 模型（灵活版） ============
class TaskStep(BaseModel):
    step_name: str = Field(description="步骤名称", default="未知步骤")
    tool_required: str = Field(description="所需工具", default="通用工具")
    reasoning: str = Field(description="执行理由", default="")

class WorkflowPlan(BaseModel):
    model_config = ConfigDict(extra='ignore')  # 忽略多余字段
    goal: str = Field(description="任务目标", default="")
    steps: list[TaskStep] = Field(description="执行步骤", default_factory=list)

# ============ 单个 API 调用 ============
async def generate_plan_single(goal: str) -> WorkflowPlan:
    """生成单个工作流计划（容错增强版）"""
    start = time.time()
    
    try:
        completion = await client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {
                    "role": "system",
                    "content": """你是一个工作流规划 API。
                    你必须严格按照以下 JSON Schema 输出：
                    {"goal": "任务目标", "steps": [{"step_name": "步骤", "tool_required": "工具", "reasoning": "理由"}]}
                    ⚠️ 只能输出 goal 和 steps 字段，不要其他字段，不要解释文字。"""
                },
                {
                    "role": "user",
                    "content": f"请为以下目标制定执行计划：{goal}"
                }
            ],
            max_tokens=800,
            temperature=0.3
        )
        
        content = completion.choices[0].message.content
        
        if not content or content.strip() == "":
            raise Exception("API 返回内容为空")
        
        # 提取 JSON 块
        json_match = re.search(r'\{[\s\S]*\}', content)
        json_str = json_match.group() if json_match else content.strip()
        
        plan_dict = json.loads(json_str)
        
        # 🔍 调试：打印返回字段
        print(f"  📦 返回字段：{list(plan_dict.keys())}")
        
        # 字段映射兼容
        if 'plan_name' in plan_dict and 'goal' not in plan_dict:
            plan_dict['goal'] = plan_dict.pop('plan_name')
        if 'phases' in plan_dict and 'steps' not in plan_dict:
            plan_dict['steps'] = plan_dict.pop('phases')
        
        # 格式化 steps
        if 'steps' in plan_dict:
            formatted_steps = []
            for step in plan_dict['steps']:
                if isinstance(step, dict):
                    formatted_steps.append(TaskStep(
                        step_name=step.get('step_name', step.get('phase', '未知步骤')),
                        tool_required=step.get('tool_required', '通用工具'),
                        reasoning=step.get('reasoning', step.get('time_allocation', ''))
                    ))
                else:
                    formatted_steps.append(TaskStep(step_name=str(step)))
            plan_dict['steps'] = formatted_steps
        
        plan = WorkflowPlan(**plan_dict)
        elapsed = time.time() - start
        print(f"  ✅ [{goal[:15]}...] 完成，耗时：{elapsed:.2f}秒")
        return plan
        
    except Exception as e:
        elapsed = time.time() - start
        print(f"  ❌ [{goal[:15]}...] 失败，耗时：{elapsed:.2f}秒，错误：{e}")
        raise

# ============ 串行调用 ============
async def run_serial(goals: list[str]) -> list[WorkflowPlan]:
    """串行执行"""
    print("\n🐢 开始串行执行...")
    start = time.time()
    plans = []
    for goal in goals:
        plan = await generate_plan_single(goal)
        plans.append(plan)
    total = time.time() - start
    print(f"🐢 串行总耗时：{total:.2f}秒\n")
    return plans

# ============ 并发调用 ============
async def run_concurrent(goals: list[str]) -> list[WorkflowPlan]:
    """并发执行"""
    print("\n🚀 开始并发执行...")
    start = time.time()
    tasks = [generate_plan_single(goal) for goal in goals]
    plans = await asyncio.gather(*tasks)
    total = time.time() - start
    print(f"🚀 并发总耗时：{total:.2f}秒\n")
    return plans

# ============ 主入口 ============
async def main():
    test_goals = [
        "帮我分析特斯拉近一周的舆情并生成报告",
        "帮我调研竞争对手的最新产品功能",
        "帮我整理本周的工作周报",
        "帮我制定下周的学习计划",
        "帮我总结最近读的三本书",
    ]
    
    print("=" * 60)
    print("🚀 Day 2: 异步并发调用性能对比测试")
    print("=" * 60)
    
    serial_plans = await run_serial(test_goals)
    concurrent_plans = await run_concurrent(test_goals)
    
    print("=" * 60)
    print("📈 性能对比总结")
    print("=" * 60)
    print(f"🐢 串行耗时：请查看上方输出")
    print(f"🚀 并发耗时：请查看上方输出")
    print(f"⚡ 加速比：串行/并发")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())