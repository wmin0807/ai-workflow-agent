# src/memory.py

class ConversationMemory:
    """对话记忆管理类"""
    
    def __init__(self, max_history=10):
        """
        初始化记忆
        :param max_history: 最大保留多少轮对话（防止超出 Token 限制）
        """
        self.history = []
        self.max_history = max_history
    
    def add_message(self, role: str, content: str):
        """添加一条消息到记忆"""
        self.history.append({
            "role": role,
            "content": content
        })
        
        # 如果超过最大长度，移除最早的对话（FIFO）
        if len(self.history) > self.max_history:
            self.history.pop(0)
    
    def get_history(self) -> list:
        """获取完整对话历史"""
        return self.history
    
    def clear(self):
        """清空记忆"""
        self.history = []
    
    def get_summary(self) -> str:
        """获取记忆摘要（用于调试）"""
        if not self.history:
            return "无历史记录"
        return f"共 {len(self.history)} 条消息，最近一条：{self.history[-1]['content'][:30]}..."