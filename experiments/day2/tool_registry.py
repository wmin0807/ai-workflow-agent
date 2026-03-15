
class ToolRegistry:
    """ 工具注册表，管理所有可用工具的注册和获取 """

    public_var = "这是一个公共类变量"
    _protect_var = "这是一个受保护的类变量，只能在内部访问使用"
    __private_var = "这是一个私有类变量，外部无法访问"

    # 类变量，__这种开头方式，说明只是自己内部使用的类变量
    __instance = None
    
    # 这是一个创建类时候的会被调用的初始化函数，self这个不是固定的，但是强烈建议使用这个名字。
    # 这个函数没有返回值
    def __init__(self):
        # self.tools = {}
        pass
    
    def register(self, name:str, tool:any) -> None:
        self.name = name
        pass

    def get_name(self) -> str:
        return self.name
    
    @classmethod
    def get_protected_var(cls):
        return cls._protect_var


print(ToolRegistry.public_var)  # 输出: 这是一个公共类变量
print(ToolRegistry._protect_var)  # 输出: 这是一个受保护的类变量，只能在内部访问使用
print(ToolRegistry.__dict__)  # 这行会报错，因为 __private_var 是私有变量，外部无法访问
print(ToolRegistry._ToolRegistry__private_var)

obj = ToolRegistry()
obj.register("search_api", "这是一个搜索工具")
print(obj.get_name()) 
