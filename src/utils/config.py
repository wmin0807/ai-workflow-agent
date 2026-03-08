# src/utils/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """全局配置类"""
    
    # 千问 API
    DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
    DASHSCOPE_BASE_URL = os.getenv("DASHSCOPE_BASE_URL", 
                                   "https://dashscope.aliyuncs.com/compatible-mode/v1")
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "qwen-plus")
    
    # Agent 配置
    MAX_HISTORY = int(os.getenv("MAX_HISTORY", "10"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1000"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    
    # 验证必要配置
    @classmethod
    def validate(cls):
        if not cls.DASHSCOPE_API_KEY:
            raise ValueError("DASHSCOPE_API_KEY 未配置，请检查 .env 文件")
        return True