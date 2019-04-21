'''
```python
dir([obj]):

    调用这个方法将返回包含obj大多数属性名的列表（会有一些特殊的属性不包含在内）。obj的默认值是当前的模块对象。

hasattr(obj, attr):

    这个方法用于检查obj是否有一个名为attr的值的属性，返回一个布尔值。

getattr(obj, attr):

    调用这个方法将返回obj中名为attr值的属性的值，例如如果attr为’bar’，则返回obj.bar。

setattr(obj, attr, val):

    调用这个方法将给obj的名为attr的值的属性赋值为val。例如如果attr为’bar’，则相当于obj.bar = val。
	dir(cat)
    hasattr(cat, 'name'): #检查实例是否有这个属性
    setattr(cat, 'name', 'tiger') #same as: a.name = 'tiger'
    print getattr(cat, 'name') #same as: print a.name



isinstance(object, classinfo)
	检查object是不是classinfo中列举出的类型，返回布尔值。classinfo可以是一个具体的类型，也可以是多个类型的元组或列表。

1. 模块(module)


__doc__: 文档字符串。如果模块没有文档，这个值是None。
*__name__: 始终是定义时的模块名；即使你使用import .. as 为它取了别名，或是赋值给了另一个变量名。
*__dict__: 包含了模块里可用的属性名-属性的字典；也就是可以使用模块名.属性名访问的对象。
__file__: 包含了该模块的文件路径。需要注意的是内建的模块没有这个属性，访问它会抛出异常！
如：
import fnmatch as m

print m.__doc__.splitlines()[0]
print m.__name__
print m.__file__
print m.__dict__.items()[0]

2.类(class)
  __doc__: 文档字符串。如果类没有文档，这个值是None。
*__name__: 始终是定义时的类名。
*__dict__: 包含了类里可用的属性名-属性的字典；也就是可以使用类名.属性名访问的对象。
__module__: 包含该类的定义的模块名；需要注意，是字符串形式的模块名而不是模块对象。
*__bases__: 直接父类对象的元组；但不包含继承树更上层的其他类，比如父类的父类
如：
from a import *

print Cat.__doc__ #None Cat类没有doc
print Cat.__name__ #Cat
print Cat.__module__ # a 如果在自身的module中执行时__main__
print Cat.__bases__ #(<type 'object'>,)
print Cat.__dict__ # 一个属性、方法对象名值的字典

3.实例(instance)
*__dict__: 包含了可用的属性名-属性对象字典。
*__class__: 该实例的类对象。对于类Cat，cat.__class__ == Cat 为 True。
 如：
from a import *

print cat.__dict__ #{'name': 'Kitty'} 仅仅有属性，没有方法
print cat.__class__ #<class 'a.Cat'>
print cat.__class__ == Cat #True



```


'''