## 关于下划线定义的解释
| 命名方式 | 含义 | 访问性 |
| --- | --- | --- |
| `name` | 普通类变量 | 公开，随意访问 |
| `_name` | **保护变量**（约定俗成） | 可以访问，但暗示"内部使用，别乱动" |
| `__name` | **私有变量**（名称改写） | 外部访问被改写为 `_类名__name` |




```shell
class ToolRegistry:
    """ 工具注册表，管理所有可用工具的注册和获取 """

    public_var = "这是一个公共类变量"
    _protect_var = "这是一个受保护的类变量，只能在内部访问使用"
    __private_var = "这是一个私有类变量，外部无法访问"

    # 类变量，__这种开头方式，说明只是自己内部使用的类变量
    __instance = None
    
    def __init__(self):
        self.tools = {}

#obj = ToolRegistry()
print(ToolRegistry.public_var)  # 输出: 这是一个公共类变量
print(ToolRegistry._protect_var)  # 输出: 这是一个受保护的类变量，只能在内部访问使用
print(ToolRegistry.__dict__)  # 这行会报错，因为 __private_var 是私有变量，外部无法访问
print(ToolRegistry._ToolRegistry__private_var)
```

#### <font style="color:rgba(0, 0, 0, 0.9);">核心区别：</font>`<font style="color:rgba(0, 0, 0, 0.9);background-color:rgba(0, 0, 0, 0.03);">__</font>`<font style="color:rgba(0, 0, 0, 0.9);"> 到底做了什么？</font>
**<font style="color:rgba(0, 0, 0, 0.9);">目的</font>**<font style="color:rgba(0, 0, 0, 0.9);">：防止子类意外覆盖，实现</font>**<font style="color:rgba(0, 0, 0, 0.9);">伪私有</font>**<font style="color:rgba(0, 0, 0, 0.9);">（并非真正的安全机制）。</font>

## 关于 def __init__(self): 的解释
```shell
__init__ 是一个初始化函数，不是构造函数，在构造对象的时候，会被执行。
self 不是关键字，可以用其他的名字，但是强烈建议用这个
这个方法，没有返回值，不要设置返回值。
```

## 关于Python的命名方是
+ 使用的是PEP 8的标准，这个PEP8 是一个什么样的标准？
+ 简单总结就是：
    - 类名字使用驼峰命名法
    - 除了类名字外，使用下划线命名法
    - 常量使用：全大写下划线命名方式
    - 私有、保护：前面加_ 或者__ 
    - 模块，或者包：小写，无下划线，或者单下划线。

## 关于定义实例方法的方式
+ 实例方法的第一个参数是self，这个是必须得。虽然self不是Python的关键字，但是强烈建议使用这个名字，当然你可以更换。事实上，self已经是一个关键字了。
+ 通过该self，指向该实例对象本身。
+ 为什么要带self，原因是：Python的设计哲学所导致，也就是Python的：显示优于隐式
    - 本质上在调用实例方法的时候，其实Python内部会转成：类.methon(实例) 它会默认把实例作为第一个参数带给方法，如果你没有定义self，它就自然而然的报错了。
+ 在Python里面，其实是存在可以不带self的方法定义的，那就是@staticmethod 和 @classmethod 两个类型。

## 关于@staticmethod  @classmethod用法
+ `<font style="color:rgba(0, 0, 0, 0.9);background-color:rgba(0, 0, 0, 0.03);">cls</font>`**<font style="color:rgba(0, 0, 0, 0.9);">不是关键字，可以改</font>**<font style="color:rgba(0, 0, 0, 0.9);">，但 </font>`<font style="color:rgba(0, 0, 0, 0.9);background-color:rgba(0, 0, 0, 0.03);">@classmethod</font>`<font style="color:rgba(0, 0, 0, 0.9);"> 要求</font>**<font style="color:rgba(0, 0, 0, 0.9);">必须有第一个参数接收类</font>**<font style="color:rgba(0, 0, 0, 0.9);">；行业强制约定叫 </font>`<font style="color:rgba(0, 0, 0, 0.9);background-color:rgba(0, 0, 0, 0.03);">cls</font>`<font style="color:rgba(0, 0, 0, 0.9);">，和实例方法的 </font>`<font style="color:rgba(0, 0, 0, 0.9);background-color:rgba(0, 0, 0, 0.03);">self</font>`<font style="color:rgba(0, 0, 0, 0.9);"> 对应，</font>**<font style="color:rgba(0, 0, 0, 0.9);">永远不要改</font>**
+ **<font style="color:rgba(0, 0, 0, 0.9);">@classmethod 的返回值没有强制类型，你想返回什么就返回什么。</font>**

| **<font style="color:rgba(0, 0, 0, 0.9);">特性</font>** | `**<font style="color:rgba(0, 0, 0, 0.9);">@staticmethod</font>**` | `**<font style="color:rgba(0, 0, 0, 0.9);">@classmethod</font>**` |
| --- | --- | --- |
| **第一个参数** | **<font style="color:rgba(0, 0, 0, 0.9);">无</font>** | `**<font style="color:rgba(0, 0, 0, 0.9);">cls</font>**`**<font style="color:rgba(0, 0, 0, 0.9);">（类本身）</font>** |
| **能访问实例？** | ❌**<font style="color:rgba(0, 0, 0, 0.9);"> 不能</font>** | ❌**<font style="color:rgba(0, 0, 0, 0.9);"> 不能（但能用 </font>**`**<font style="color:rgba(0, 0, 0, 0.9);">cls</font>**`**<font style="color:rgba(0, 0, 0, 0.9);"> 创建实例）</font>** |
| **能访问类？** | ❌**<font style="color:rgba(0, 0, 0, 0.9);"> 不能直接</font>** | ✅**<font style="color:rgba(0, 0, 0, 0.9);"> 能，通过 </font>**`**<font style="color:rgba(0, 0, 0, 0.9);">cls</font>**` |
| **调用方式** | `**<font style="color:rgba(0, 0, 0, 0.9);">类.方法()</font>**`**<font style="color:rgba(0, 0, 0, 0.9);"> 或 </font>**`**<font style="color:rgba(0, 0, 0, 0.9);">实例.方法()</font>**` | `**<font style="color:rgba(0, 0, 0, 0.9);">类.方法()</font>**`**<font style="color:rgba(0, 0, 0, 0.9);"> 或 </font>**`**<font style="color:rgba(0, 0, 0, 0.9);">实例.方法()</font>**` |
| **典型用途** | **<font style="color:rgba(0, 0, 0, 0.9);">工具函数、组织相关功能</font>** | **<font style="color:rgba(0, 0, 0, 0.9);">工厂方法、替代构造函数</font>** |


**<font style="color:rgba(0, 0, 0, 0.9);"></font>**
