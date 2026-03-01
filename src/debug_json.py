import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

async def test():
    completion = await client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {"role": "system", "content": "只输出 JSON，不要任何文字"},
            {"role": "user", "content": "请为'写周报'制定计划"}
        ],
        max_tokens=500
    )
    
    content = completion.choices[0].message.content
    print("=" * 60)
    print("📝 完整原始回复:")
    print("=" * 60)
    print(content)
    print("=" * 60)

asyncio.run(test())
