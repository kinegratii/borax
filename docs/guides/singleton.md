# Singleton 模块

> 模块： `borax.patterns.singleton`

该模块定义了 `MetaSingleton` 类，以元类方式实现单例模式。

若需要实现类 `A` 为单例模式，只需将其元类属性设置为 `MetaSingleton` 即可。

```python
from borax.patterns.singleton import MetaSingleton

class SingletonM(metaclass=MetaSingleton):
    pass
```
`SingletonM` 类的实例对象都共享相同状态和数据。如：

```python
a = SingletonM()
b = SingletonM()
print(id(a) == id(b)) # True
```
