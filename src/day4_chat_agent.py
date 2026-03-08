# src/day4_chat_agent.py
import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv

from prompts import WORKFLOW_PLANNER_SYSTEM
from memory import ConversationMemory

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

class ChatAgent:
    """带记忆功能的对话 Agent"""
    
    def __init__(self, max_history=10):
        self.memory = ConversationMemory(max_history)
        print(f"🧠 Agent 已初始化，记忆容量：{max_history} 轮")
    
    async def chat(self, user_input: str) -> str:
        """
        对话核心方法
        :param user_input: 用户输入
        :return: Agent 回复
        """
        # 1. 添加用户消息到记忆
        self.memory.add_message("user", user_input)
        
        # 2. 准备发送给模型的 messages（系统提示 + 历史对话）
        messages = [
            {"role": "system", "content": WORKFLOW_PLANNER_SYSTEM}
        ]
        # 添加历史对话
        messages.extend(self.memory.get_history())
        
        # 3. 调用千问 API
        try:
            completion = await client.chat.completions.create(
                model="qwen-plus",
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            assistant_reply = completion.choices[0].message.content
            
            # 4. 添加助手回复到记忆
            self.memory.add_message("assistant", assistant_reply)
            
            return assistant_reply
            
        except Exception as e:
            return f"❌ 出错了：{e}"
    
    def show_memory(self):
        """显示当前记忆状态（调试用）"""
        print("\n--- 🧠 当前记忆 ---")
        print(self.memory.get_summary())
        print("------------------\n")

# ============ 交互式命令行 ============
async def interactive_chat():
    """命令行交互模式"""
    agent = ChatAgent(max_history=10)
    
    print("=" * 50)
    print("🤖 AI Workflow Agent - 多轮对话模式")
    print("=" * 50)
    print("💡 提示：输入 'quit' 退出，输入 'memory' 查看记忆状态")
    print("=" * 50)
    
    while True:
        try:
            # 获取用户输入
            user_input = input("\n👤 你：").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'quit':
                print("👋 再见！")
                break
            
            if user_input.lower() == 'memory':
                agent.show_memory()
                continue
            
            # 获取 Agent 回复
            print("\n🤖 Agent 思考中...")
            reply = await agent.chat(user_input)
            print(f"\n🤖 Agent: {reply}")
            
        except KeyboardInterrupt:
            print("\n👋 强制退出")
            break
        except Exception as e:
            print(f"\n❌ 错误：{e}")

# ============ 测试脚本 ============
async def test_memory():
    """自动化测试记忆功能"""
    agent = ChatAgent(max_history=5)
    
    print("\n🧪 开始记忆测试...")
    
    # 第一轮
    reply1 = await agent.chat("帮我制定一个学习计划")
    print(f"1️⃣  回复：{reply1[:50]}...")
    
    # 第二轮（引用上一轮）
    reply2 = await agent.chat("把刚才的计划做成表格")
    print(f"2️⃣  回复：{reply2[:50]}...")
    
    # 第三轮（继续引用）
    reply3 = await agent.chat("导出为 Markdown 格式")
    print(f"3️⃣  回复：{reply3[:50]}...")
    
    # 查看记忆
    agent.show_memory()
    print("✅ 记忆测试完成！")

# ============ 主入口 ============
async def main():
    # 选项 1：交互式对话（推荐体验）
    await interactive_chat()
    
    # 选项 2：自动化测试（推荐演示）
    # await test_memory()

if __name__ == "__main__":
    asyncio.run(main())