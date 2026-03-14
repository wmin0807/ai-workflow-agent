

# src/tools/report.py
import os
import asyncio
from datetime import datetime
from tools.base import BaseTool

class ReportTool(BaseTool):
    """报告生成工具"""
    
    @property
    def name(self) -> str:
        return "report_tool"
    
    @property
    def description(self) -> str:
        return "生成 Markdown 格式的舆情报告"
    
    async def execute(self, 
                     topic: str,
                     search_results: list,
                     summary: str = "",
                     output_path: str = None) -> Dict:
        """
        生成报告
        :param topic: 监控主题
        :param search_results: 搜索结果列表
        :param summary: 核心摘要
        :param output_path: 输出文件路径
        :return: 报告内容 + 文件路径
        """
        print(f"  📝 [报告] 生成'{topic}'舆情报告")
        
        # 生成 Markdown 内容
        report = f"""# 📊 {topic} 舆情日报

**生成时间**：{datetime.now().strftime("%Y-%m-%d %H:%M")}

## 🔍 核心摘要
{summary if summary else "暂无摘要"}

## 📰 关键新闻
"""
        
        # 添加新闻列表
        for i, item in enumerate(search_results[:5], 1):
            report += f"\n### {i}. {item.get('title', '无标题')}\n"
            report += f"- 来源：{item.get('source', '未知')}\n"
            report += f"- 链接：[{item.get('url', '#')}]({item.get('url', '#')})\n"
            report += f"- 摘要：{item.get('snippet', '')}\n"
        
        report += "\n---\n*本报告由 AI Workflow Agent 自动生成*\n"
        
        # 保存到文件
        file_path = None
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(report)
            file_path = os.path.abspath(output_path)
            print(f"  💾 报告已保存：{file_path}")
        
        return {
            "status": "success",
            "content": report,
            "file_path": file_path,
            "word_count": len(report)
        }

# 测试代码
if __name__ == "__main__":
    import asyncio
    
    async def test():
        tool = ReportTool()
        
        # 模拟搜索结果
        search_results = [
            {"title": "新闻 1", "url": "https://example.com/1", "snippet": "摘要 1", "source": "源 1"},
            {"title": "新闻 2", "url": "https://example.com/2", "snippet": "摘要 2", "source": "源 2"},
        ]
        
        result = await tool.execute(
            topic="特斯拉",
            search_results=search_results,
            summary="特斯拉近期舆情整体正面，主要关注新车型发布。",
            output_path="reports/test_report.md"
        )
        
        print(f"\n✅ 报告生成完成：{result['file_path']}")
        print(f"   字数：{result['word_count']}")
    
    asyncio.run(test())
