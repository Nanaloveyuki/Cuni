# 语言

## Python

Cunimi 语言规范

> Lint1级别: 在测试(tests)和开发(dev)环境中允许适量报错,但在生产(prod)环境中必须将**Pyright** & **Ruff**等语法规范工具开到最大后,**一个报错&警告都不能有**

适合高度团队化和高风险行业,如金融和医疗,高并发服务项目.又例如标准库项目.

- 全部代码必须遵守全部规范([L1],[L2],[L3])

---

> Lint2级别: 在测试(tests)和开发(dev)环境中允许适量报错,但在生产(prod)环境中必须将**Pyright** & **Ruff**等语法规范工具开到最大后,**不能存在任何报错,但可以存在适量的警告**

适合普通团队,如初创公司,小团队,或对代码质量有一定要求但是组织规模不是特别大的项目,又或是一些对代码质量要求不是特别高但是需要有一定代码规范的项目.又例如算法项目.

- 全部代码必须遵守[L2]及[L3]

---

> Lint3级别: 在测试(tests)和开发(dev)环境中允许报错,可以运行即可,但在生产(prod)环境中必须将**Pyright** & **Ruff**等语法规范工具开到最大后,**可以存在适量报错和警告,只要不影响程序运行即可**

适合新手和一次性项目,如个人项目,小项目,或一些对代码质量要求不是特别高但是需要有一定代码规范的项目.又例如练手项目.

- 全部代码必须遵守[L3]

### 函数

[L1]必须保持**单函数单功能原则**

- [L2]每个函数只负责一个功能,不要在单个函数中塞下两个以上的功能;

- [L2]每个函数推荐行数20行以内,最大行数50行,超过50行的函数必须拆分成多个函数;

- [L2]每个函数在Python版本条件允许下,必须使用显式输出和显式类型注解:

```python

def func_name(param1: int, param2: list) -> result_type:
    """
    函数功能描述
    Args:
        param1 (param1_type): 参数1描述
        param2 (param2_type): 参数2描述
    Returns:
        result_type: 返回值描述
    """
    # 函数体
    return result
```

- [L2]每个函数的输入参数必须使用类型注解,如果存在默认值,则默认值也必须使用类型注解;

```python

def func_name(param1: int, param2: list = []) -> result_type:
    """
    函数功能描述
    Args:
        param1 (param1_type): 参数1描述
        param2 (param2_type): 参数2描述
    Returns:
        result_type: 返回值描述
    """
    # 函数体
    return result
```

- [L2]每个函数的函数命名必须包含以下因素:
    - [L3]函数名非必要情况(除非项目特别说明函数规范)下必须使用小写和下划线命名
    - [L3]私有函数以下划线开头: `_priv_func`
    - [L2]对外接口函数以g开头: `g_func_name`
    - 函数名必须要足够简洁明了,例如:
        - `get_user_id` 普通函数;
        - [L2]`g_add_user` 全局/接口函数;
        - `_set_color` 私有函数;
    - 函数名必须包含功能描述,例如:
        - `get_user_id` 获取用户ID;
        - [L2]`g_add_user` 添加用户;
        - `_set_color` 设置颜色;

- [L2]函数参数行只要有超过四个参数或其字符长度大于79个字符就必须换行:
```python
def func_name(arg1: int,
    arg2: int,
    arg3: int) -> int:
```

### 类

[L2]必须保持**最简类单元**

- [L2]非必要情况下(例如类中只有一个实现函数)不建议使用类;

- [L3]必要情况下(如自定义Exception)必须使用类且说明情况;
```python
class MyException(Exception):
    """
    自定义异常类,用于在程序中抛出xxx异常
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
```

- [L2]每个类必须包含类注释,类注释中必须包含类功能描述和所有公开的内部方法;

- [L3]非最初父类的类继承必须使用显式继承,例如:
```python
class MyClass(User):
    """
    自定义类,继承自User
    """
    def __init__(self, param1: int, param2: list = []):
        self.param1 = param1
        self.param2 = param2
        super().__init__(self.param1, self.param2)
```

- [L2]禁止继承的类必须使用`@final`装饰器说明

- [L3]每个类的类命名必须包含以下因素:
    - 类名非必要情况(除非项目特别说明类规范)下必须使用大写驼峰命名
    - 类名必须要足够简洁明了,例如:
        - `MyClass` 普通类;
        - `MyException` 异常类;
    - 类名必须包含功能描述,例如:
        - `MyClass` 自定义类;
        - `MyException` 自定义异常类;

- [L2]特殊类,如数据类,必须使用`dataclass`等装饰器,例如:
```python
from dataclasses import dataclass

@dataclass
class MyDataClass:
    """
    自定义数据类,用于存储xxx数据
    """
    param1: int
    param2: list = field(default_factory=list)
```
- [L3]对于只读数据类推荐以支持线程安全和哈希: `@dataclass(frozen=True)`

- [L2]类空行规范:
    - 类的内类与另一类的内类/函数/类数据之间空两行:
    ```python
    class MyClass:
        """
        自定义类,继承自BaseClass
        """
        def __init__(self, param1: int, param2: list = []):
            self.param1 = param1
            self.param2 = param2
            super().__init__(self.param1, self.param2)
            # 第一行
            #第二行
        class MyClassSubClass(User):
            """
            自定义子类类,继承自User
            """
            def __init__(self, param1: int, param2: list = []):
                self.param1 = param1
                self.param2 = param2
                super().__init__(self.param1, self.param2)
    ```
    - 类与外部类之间空两行
    ```python
    class MyFristClass:
        """
        自定义类,继承自BaseClass
        """
        def __init__(self, param1: int, param2: list = []):
            self.param1 = param1
            self.param2 = param2
            super().__init__(self.param1, self.param2)
        # 第一行
        # 第二行
    class MySecondClass:
        """
        自定义类,继承自BaseClass
        """
        def __init__(self, param1: int, param2: list = []):
            self.param1 = param1
            self.param2 = param2
            super().__init__(self.param1, self.param2)
    ```
    - 类的内函数与类的内函数之间空一行
    ```python
    class MyClass:
        """
        自定义类,继承自BaseClass
        """
        def __init__(self, param1: int, param2: list = []):
            self.param1 = param1
            self.param2 = param2
            super().__init__(self.param1, self.param2)
        # 一行
        def func_name(self, param1: int, param2: list = []) -> result_type:
            """
            函数功能描述
            Args:
                param1 (param1_type): 参数1描述
                param2 (param2_type): 参数2描述
            Returns:
                result_type: 返回值描述
            """
            # 函数体
            return result
    ```
    - 类的内函数里逻辑代码尽量不空行;

- [L2]类的内函数保护级别:
    - 公开函数: 常见,可以直接调用,例如: `func_name` & `g_func_name`
    - 保护函数: 常见,仅在类内调用,例如: `_func_name`
    - 私有函数: 仅限于避免子类覆盖时,仅在类内调用,例如: `__func_name`

- [L2]实例的类属性:
    - 公开属性: 常见,可以直接访问,例如: `self.param1`
    - 保护属性: 常见,仅在类内访问,例如: `self._param1`
    - 私有属性: 仅限于避免子类覆盖时,仅在类内访问,例如: `self.__param1`

- [L2]非特殊情况(例如数据类),实例的属性声明必须要在`__init__`函数中完成,避免运行时新增属性导致维护艰难;

- [L2]没有动态属性的类建议使用`__slots__`来优化内存占用;

- [L2]类参数行宽度必须小于等于79字符,避免参数列表过长导致阅读困难, 过长的必须分行;
```python
class MyClass(xxx,
    aaa,
    ccc):
```

### Code Review & Git Flow

根据具体项目选择L1~L3三个等级的代码规范,建议在项目开始时就确定,并在项目运行过程中保持一致;

遇到非项目预定规范的 PR/Commit 时,需要根据具体情况判断是否需要修改或拒绝并打回,如果修改,需要在 PR/Commit 中说明修改原因,并在项目中记录下修改,如果拒绝并打回,需要详细说明哪里的规范存在问题以好让提出 PR/Commit 的人了解具体情况避免团队争议;

允许适当使用 AI 作为辅助性工具,但是一定要 Review AI 写的代码,不能直接接受 AI 写的代码;

单人写的代码在本地 Commit 到远程仓库时一定要仔细查看, 不能直接提交;

Pyright等Lint出现警告或报错时,如果是特殊情况,例如误判或当前无法解决的困境,则需要在PR/Commit信息中详细说明,并在项目中记录下修改,如果是项目预定规范的问题,则需要在PR/Commit信息中说明并在项目中记录下修改,之后才可使用`# noqa: xxx`;

L1级`pyproject.toml`示例:
```toml
[tool.ruff]
target-version = "py311"
line-length = 79
select = ["ALL"]
ignore = [
    "D203", "D212",  # 与 Google 风格 docstring 冲突，可关
    "T201",          # 允许 print 在调试阶段
]
unfixable = ["F841"]  # 禁止自动删除未使用变量，避免调试被误杀

[tool.ruff.per-file-ignores]
"tests/*" = ["S101", "D"]  # 测试文件允许 assert 与无 docstring

[tool.pyright]
typeCheckingMode = "strict"
reportMissingTypeStubs = false   # 第三方库无 stubs 时豁免
reportIncompatibleMethodOverride = true
reportPrivateUsage = true

[tool.slotscheck]
strict-imports = true
```

一键L1级别:
```bash
pip install ruff pyright slotscheck pre-commit && pre-commit install
```

尽量使用本地pre-commit集成各Lint以阻断可能出现的规范问题;
