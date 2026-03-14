# src/day6_sentiment_monitor.py
import os
import asyncio
from datetime import datetime
from openai import AsyncOpenAI
from dotenv import load_dotenv

from prompts.system import WORKFLOW_PLANNER_SYSTEM
from tools.search import SearchTool
from tools.report import ReportTool

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

class SentimentMonitor:
    """舆情监控助手"""
    
    def __init__(self):
        self.search_tool = SearchTool()
        self.report_tool = ReportTool()
        print("🎯 舆情监控助手已初始化")
    
    async def analyze_sentiment(self, texts: list) -> str:
        """用千问模型做情感分析"""
        prompt = f"""分析以下文本的整体情感倾向，用 1 句话总结：
        
{' '.join(texts[:5])}

只输出总结，不要其他内容。"""
        
        try:
            resp = await client.chat.completions.create(
                model="qwen-plus",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200
            )
            return resp.choices[0].message.content
        except Exception as e:
            return f"分析失败：{e}"
    
    async def monitor(self, topic: str) -> dict:
        """执行完整的舆情监控流程"""
        print("\n" + "=" * 50)
        print(f"🎯 开始监控：{topic}")
        print("=" * 50)
        
        # Step 1: 搜索
        search_result = await self.search_tool.execute(f"{topic} 新闻", count=5)
        if search_result["status"] != "success":
            return {"error": "搜索失败"}
        
        # Step 2: 情感分析
        texts = [r["snippet"] for r in search_result["results"]]
        summary = await self.analyze_sentiment(texts)
        print(f"\n🧠 情感分析：{summary}")
        
        # Step 3: 生成报告
        report_path = f"reports/{topic}_{datetime.now().strftime('%Y%m%d')}.md"
        report_result = await self.report_tool.execute(
            topic=topic,
            search_results=search_result["results"],
            summary=summary,
            output_path=report_path
        )
        
        print("\n" + "=" * 50)
        print("✅ 监控完成！")
        print("=" * 50)
        
        return {
            "topic": topic,
            "search_count": search_result["count"],
            "summary": summary,
            "report_path": report_result["file_path"]
        }

async def main():
    monitor = SentimentMonitor()
    result = await monitor.monitor("特斯拉")
    print(f"\n📊 结果：{result}")

if __name__ == "__main__":
    asyncio.run(main())