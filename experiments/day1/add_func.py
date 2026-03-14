
def add(a: int, b:int) -> int:
    # 这是一个简单的加法函数
    """
    add 的 Docstring
    
    :param a: 说明
    :type a: int
    :param b: 说明
    :type b: int
    :return: 说明
    :rtype: int
    """ 
    return a + b

# 乘法
def multiply(a: float, b: float) -> float:
    return a * b


if __name__ == "__main__":
    assert add(2, 3) == 5, "正数相加失败"
    assert add(-3, 3) == 0, "负数相加失败"
    assert add(0, 0) == 0, "零相加失败"
    print("✅ 所有add 测试通过！")

    assert multiply(2, 1.1) == 2.2, "正数相乘失败"
    assert multiply(-3, 3) == -9, "负数相乘失败"
    assert multiply(0, 0) == 0, "零相乘失败"
    print("✅ 所有multiply 测试通过！")
