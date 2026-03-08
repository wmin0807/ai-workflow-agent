# src/tools/base.py
import asyncio

# ============ 工具基类 ============
class BaseTool:
    name = "base"
    description = "基础工具"
    
    async def execute(self, **kwargs):
        return {"status": "not implemented"}

# ============ 搜索工具 ============
class SearchTool(BaseTool):
    name = "search_api"
    description = "搜索互联网信息"
    
    async def execute(self, query=""):
        print(f"  🔍 [搜索] {query}")
        await asyncio.sleep(0.5)
        return {"status": "success", "data": f"搜索结果：{query}"}

# ============ 邮件工具 ============
class EmailTool(BaseTool):
    name = "email_tool"
    description = "发送邮件"
    
    async def execute(self, to="", subject=""):
        print(f"  📧 [邮件] 发送给：{to}, 主题：{subject}")
        await asyncio.sleep(0.5)
        return {"status": "success"}

# ============ 文件工具 ============
class FileTool(BaseTool):
    name = "file_tool"
    description = "读写文件"
    
    async def execute(self, action="", path=""):
        print(f"  📁 [文件] {action} {path}")
        await asyncio.sleep(0.3)
        return {"status": "success"}

# ============ 工具注册表 ============
class ToolRegistry:
    def __init__(self):
        self.tools = {}
    
    def register(self, tool):
        self.tools[tool.name] = tool
    
    def get(self, name):
        if name not in self.tools:
            raise ValueError(f"工具不存在：{name}")
        return self.tools[name]

# 初始化全局注册表
tool_registry = ToolRegistry()
tool_registry.register(SearchTool())
tool_registry.register(EmailTool())
tool_registry.register(FileTool())