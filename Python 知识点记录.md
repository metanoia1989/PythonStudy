# pip python包管理器
## 安装
**通过 Linux 包管理器**
CentOS: `sudo yum install python-pip`
Debian: `sudo apt install python3-venv python3-pip`

**通过 get-pip.py**
```sh
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ python get-pip.py
# options
$ python get-pip.py --proxy="http://[user:passwd@]proxy.server:port"
$ python get-pip.py --prefix <dir>
$ python get-pip.py --user # 安装到用户目录 ~/.local  %APPDATA%Python
$ python get-pip.py --target # 安装包到目录
```
指定 PYTHONPATH 设置包目录

**升级pip**
```
$ pip install -U pip
```

使用 --user 安装，相关路径
~/.local/lib/python3.7/site-packages/ 包路径
~/.local/bin/pip 可执行文件路径

## 换源
国内的几个pip源
```url
http://topmanopensource.iteye.com/blog/2004853
http://pypi.douban.com/ 豆瓣
http://pypi.hustunique.com/ 华中理工大学
http://pypi.sdutlinux.org/ 山东理工大学
http://pypi.mirrors.ustc.edu.cn/ 中国科学技术大学
```
直接修改 pip 配置文件即可
linux的文件在`~/.pip/pip.conf`，windows在 `%HOMEPATH%\pip\pip.ini`
```ini
[global]
index-url = http://pypi.douban.com/simple
```

## 用法
```sh
$ pip3 install <package>
$ pip3 install --user <package> # user-level installs
```

## 报错
Python3: ImportError: No module named '_ctypes' 
```sh
$ sudo yum install libffi-devel
$ ./configure
$ make
$ make install
```

# 协程
协程是一种比进程和线程更加轻量级的解决方案，也通过yield实现了协程，但最大的疑问是没有提供像进程或线程类的任务调度，没有体现出协程的优势。

- [协程与多任务调度](https://www.hitoy.org/coroutine-multitasking-schedule.html)


# 异常
- [Python Standard Exceptions](http://www.tutorialspoint.com/python/standard_exceptions.htm)
- [总结：Python中的异常处理](https://segmentfault.com/a/1190000007736783)

异常(exceptions)是Python中一种非常重要的类型，它和语法错误不同，是在程序运行期间引发的错误。

> 从软件方面来说，错误是语法或是逻辑上的。错误是语法或是逻辑上的。
语法错误指示软件的结构上有错误，导致不能被解释器解释或编译器无法编译。这些些错误必须在程序执行前纠正。
当程序的语法正确后，剩下的就是逻辑错误了。逻辑错误可能是由于不完整或是不合法的输入所致；
在其它情况下，还可能是逻辑无法生成、计算、或是输出结果需要的过程无法执行。这些错误通常分别被称为域错误和范围错误。
当python检测到一个错误时，python解释器就会指出当前流已经无法继续执行下去。这时候就出现了异常。

内置异常：IOError,NameError,KeyboardInterrupt

Python的异常可以通过try语句来检查，任何在try语句块里的代码都会被监测，检查有无异常产生，except会根据输入检查异常的类型，并执行except内的代码。

## 异常处理语句 
try...excpet...else...finally
except后面的两个参数: 错误的类型, Exception的实例.
else 如果没有捕获异常 就会执行
finally 无论是否捕获异常 都会执行

1. except语句可以有多个，Python会按except语句的顺序依次匹配你指定的异常，如果异常已经处理就不会再进入后面的except语句。
2. except语句可以以元组形式同时指定多个异常
3. except语句后面如果不指定异常类型，则默认捕获所有异常，此时需要通过logging或者sys模块获取当前异常。
4. 尽量使用内置的异常处理语句来替换try/except语句，比如with语句，getattr()方法。这样让代码更优雅，我不觉得一个文件一堆异常处理有多好。
5. 避免在catch语句块中干一些没意义的事情，捕获异常也是需要成本的。
6. 不要使用异常来控制流程，那样你的程序会无比难懂和难维护。
7. 如果有需要，切记使用finally来释放资源。
8. 如果有需要，请不要忘记在处理异常后做清理工作或者回滚操作。

## 抛出异常
手动抛出异常一个异常，可以使用raise关键字。
raise关键字后面可以指定你要抛出的异常实例，一般来说抛出的异常越详细越好。
Python在exceptions模块内建了很多的异常类型，通过使用dir()函数来查看exceptions中的异常类型

```python
raise NameError("bad name!") # 抛出异常
import exceptions
print(dir(exceptions)) # 获取所有内置异常
# ['ArithmeticError', 'AssertionError'...]
```


## 自定义异常
自定义异常，所有异常必须直接或者间接的继承自Exception类。
```python
#!/usr/bin/env python
class MyError(Exception):
    def __init__(self,*args):
        self.value=args[0]
    def __str__(self):
        return repr(self.value)
def showname(*args):
    if args:
        print args
    else:
        raise MyError('Error: need 1 arguments at last, 0 Input')
```

## except Exception as e和 except Exception, e
```python
try:
    do_something()
except NameError as e:  # should
    pass
except KeyError, e:  # should not
    pass
```
在Python2的时代，你可以使用以上两种写法中的任意一种。在Python3中你只能使用第一种写法，第二种写法已经不再支持。

## 使用内置的语法范式代替try/except
Python 本身提供了很多的语法范式简化了异常的处理。
for语句就处理了的StopIteration异常，让你很流畅地写出一个循环。
with语句在打开文件后会自动调用finally并关闭文件。

打开文件 
```python
# should not
try:
    f = open(a_file)
    do_something(f)
finally:
    f.close()

# should 
with open(a_file) as f:
    do_something(f)
```

访问一个不确定的属性
```python3
try:
    test = Test()
    name = test.name  # not sure if we can get its name
except AttributeError:
    name = 'default'

ame = getattr(test, 'name', 'default')
```

# 字符串
```python
int(object)                        将字符串和数字转换为整数
long(object)                       将字符串和数字转换为长整型数
str(object)                        将值转换为字符串
```

## 字符串方法
字符串从string模块中“继承”了很多方法。
获取一个模块的文件位置：`print(string.__file__)`

**字符串模块的常量**
```python
string.digits：包含数字0~9的字符串
string.whitespace： 所有ascii空白字符
string.ascii_lowercase：所有ascii小写字母的字符串
string.ascii_uppercase：所有ascii大写字母的字符串
string.ascii_letters：所有ascii字母的字符串
string.hexdigits：包含十六进制数字0-F的字符串
string.punctuation：包含所有标点的字符串
string.printable包含所有可打印字符的字符串
```

**字符串方法**
str.find() 在一个较长的字符串中查找子串。它返回子串所在位置的最左端索引。如果没有找到则返回-1。
str.join() 是split方法的逆方法，用来连接序列中的元素。
str.split() 是join的逆方法，用来将字符串分隔成序列。
str.lower() 返回字符串的小写字母版
str.upper() 返回字符串的大写字母版
str.replace() 返回某字符串的所有匹配项均被替换之后得到字符串。
str.strip() 返回去除两侧(不包括内部)空格的字符串

```python3
>>> "/".join(["", "usr", "bin", "env"])
'/usr/bin/env'
>>> "/usr/bin/env".split("/")
['', 'usr', 'bin', 'env']"1+2+3+4+5".split("+")
>>> "This is a test".replace("is", "eez")
'Theez eez a test'
```

## str 和 repr
Python打印值的时候会保持该值在Python代码中的状态，而不是你希望用户所看到的状态。
```python
>>> "Hello, world!"
'Hello, world!'
>>> 1000000L
1000000L
>>> print "Hello, world!"
Hello, world!
>>> print 1000000L
1000000
```

str函数，它会把值转换为合理形式的字符串，最终输出的格式
repr函数，它会创建一个字符串，标准Python表达式，包含换行符等等，数值类型

##  input和raw_input的比较
input会假设用户输入的是合法的Python表达式，与repr函数相反的。用户的输入若是字符串必须带引号。
raw_input函数，它会把所有的输入当做原始数据(raw data)，然后将其放入字符串中。无论用户输入什么，都返回字符串。

python3中raw_input()和input()进行了整合，去除了raw_input()，仅保留了input()函数，其接收任意任性输入，将所有输入默认为字符串处理，并返回字符串类型。

## 长字符串、原始字符串和Unicode
**1. 长字符串**
写一个需要跨多行的长字符串，可以使用三个引号代替普通引号。可以在字符串之中同时使用单引号和双引号，而不需要使用反斜线进行转义。
普通字符串也可以跨行。如果一行之中最后一个字符是反斜线，那么，换行符本身就“转义”了，也就是被忽略了。

```python
longStr = '''This is a very long string.
It continues here.
And it's not over yet.
"Hello, world!"
Still here.'''
generalStr = "Hello, \
... world!"
```

**2. 原始字符串**
原始字符串_对于反斜线并不会特殊对待。在原始字符串中输入的每个字符都会与书写的方式保持一致。
在书写正则表达式时候，反斜线无需转义，直接用原始字符串，更容易理解。
以在原始字符串中同时使用单双引号，甚至三引号字符串也可以。
```python
r"This is illegal\"
```

**3. Unicode 字符串**
在Python 3.0中，所有字符串都是Unicode字符串。Python2中的普通字符串在内部是以18位的ASCII码形成存储的，而Unicode字符串则存储为16位的Unicode字符，这样就能够表示更多的字符集了，包括世界上大多数语言的特殊字符。
```python
>>> u"Hello, world!"
u'Hello, world!'
```

## 字符串格式化
字符串格式化使用字符串格式化操作符即百分号%来实现。

**格式化字符串**
在%的左侧放置一个字符串(格式化字符串)，而右侧则放置希望被格式化的值。可以使用一个值，如一个字符串或者数字，也可以使用多个值的元组或者字典。
如果使用列表或者其他序列代替元组，那么序列会被解释为一个值。只有元组和字典可以格式化一个以上的值。
格式化字符串的%s部分称为_转换说明符_(conversion specifier)，它们标记了需要插入转换值的位置。
如果要在格式化字符串里面包括百分号，那么必须使用%%，这样Python就不会将百分号误认为是转换说明符了。

```python
>>> format = "Hello, %s. %s enough for ya?"
>>> values = ("world", "Hot")
>>> print(format % values)
Hello, world. Hot enough for ya?
```

转换说明符
```python
%字符：标记转换说明符的开始
- 表示左对齐
+ 表示在转换值之前要加上正负号
" "  (空白字符)表示整数之前保留空格
0  表示转换值若位数不够则用0填充
最小字段宽度 转换后的字符串至少应该具有该值指定的宽度 
点(.)后跟精度值 如果转化的是实数，精度值就表示出现在小数点后的位数。如果转换的是字符串，那么该数字就表示_最大字段宽度
使用*(星号)作为字段宽度或者精度(或者两者都是用*)，此时数值会从元组参数中读出
```

字符串格式化转换类型
```python
d， i　　　　　　带符号的十进制整数
o　　　　　　　　不带符号的八进制
u　　　　　　　　不带符号的十进制
x　　　　　　　　不带符号的十六进制(小写)
X　　　　　　　　不带符号的十六进制(大写)
e　　　　　　　　科学计数法表示的浮点数(小写)
E　　　　　　　　科学计数法表示的浮点数(大写)
f， F　　　　　　十进制浮点数
g　　　　　　　　如果指数大于-4或者小于精度值则和e相同，其他情况与f相同
G　　　　　　　　如果指数大于-4或者小于精度值则和E相同，其他情况与F相同
C　　　　　　　　单字符(接受整数或者单字符字符串)
r　　　　　　　　字符串(使用repr转换任意Python对象)
s　　　　　　　　字符串(使用str转换任意Python对象)
```

```python3
# 使用给定宽度打印格式化后的价格列表
width = int(input("Please enter width: "))
price_width = 10
item_width = width - price_width
header_format = "%-*s%*s"
format = "%-*s%*.2f"

print("=" * width)
print(header_format % (item_width, "Item", price_width, "Price"))
print("-" * width)
print(format % (item_width, "Apples", price_width, 0.4))
print(format % (item_width, "Pears", price_width, 0.5))
print(format % (item_width, "Cantaloupes", price_width, 1.92))
print(format % (item_width, "Dried Apricots (16 oz.)", price_width, 8))
print(format % (item_width, "Prunes (16 oz.)", price_width, 12))
print("=" * width)
```
输出结果，格式化字符串好强大，像MySQL的查询结果，很多都是这个样子的，很漂亮
```output
Please enter width: 35
===================================
Item                          Price
-----------------------------------
Apples                         0.40
Pears                          0.50
Cantaloupes                    1.92
Dried Apricots (16 oz.)        8.00
Prunes (16 oz.)               12.00
===================================
```

**模板字符串**
string模块提供另外一种格式化值的方法：模板字符串。类似于很多UNIX Shell里的变量替换。substitute 模板方法会用传递进来的关键字参数foo替换字符串中的$foo。
如果替换字段是单词的一部分，那么参数名就必须用括号括起来，从而准确指明结尾。
如果模板字符串中要插入`$`可以使用`$$`插入美元符号。
```python
>>> s = Template("Make $$ selling $x!")
>>> s.substitute(x="slurm") 'Make $ selling slurm!'
```

# 列表和元组
数据结构是通过某种方式(例如对元素进行编号)组织在一起的数据元素的集合，这些数据元素可以是数字或者字符，甚至可以是其他数据结构。在Python中，最基本的数据结构是_序列_(sequence)，序列中的每个元素被分配一个序号——即元素的位置，也称为_索引_。第一个索引是0，第二个则是1，以此类推。

Python包含6中內建的序列，列表 和 元组 Unicode字符串、buffer对象和xrange对象。

列表和元组的主要却别在于：列表可以修改，元组则不能。也就是说如果要根据要求来添加元素，那么列表可能会更好用；而处于某些原因，序列不能修改的时候，使用元组则更为合适。

Python之中还有一种名为容器(container)的数据结构。容器基本上是包含到其他对象的任意对象。序列(例如列表和元组)和映射(例如字典)是两类主要的容器。序列中的每个元素都有自己的编号，而映射中的每个元素则有一个名字(也称为键)。至于既不是序列也不是映射的容器类型，集合(set)就是一个例子。

## 通用序列操作
所有序列类型都可以进行某些特定的操作。这些操作包括：索引(indexing)、分片(slicing)、加(adding)、乘(multiplying)以及检查某个元素是否属于序列的成员(成员资格)。除此之外，Python还有计算序列长度、找出最大元素和最小元素的內建函数。
还有迭代(iteration)。对序列进行迭代的意思是：依次对序列中的每个元素重复执行某些操作。

索引：通过编号访问单个元素 `sep[index]`
分片：通过冒号隔开的两个索引访问一定范围内的元素 `tag[9:30]` `[0:10:2]`
序列相加：通过使用加运算符可以进行序列的连接操作 
乘法：用数字x乘以一个序列会生成新的序列，而在新的序列中，原来的序列将被重复x次。
None、空列表和初始化：空列表可以简单地通过两个中括号进行表示([])
成员资格：为了检查一个值是否在序列中，可以使用in运算符
长度、最小值和最大值：`len`、`min` 和 `max`
```python3
# 相加
>>> [1, 2, 3] + [4, 5, 6]
[1, 2, 3, 4, 5, 6] 
>>> "Hello, " + "world!"
'Hello, world!'

# 乘法
>>> "Python" * 5
'PythonPythonPythonPythonPython'
>>> [19] * 10 
[19, 19, 19, 19, 19, 19, 19, 19, 19, 19]

# 初始化一个长度为10的列表
>>> [None] * 10
[None, None, None, None, None, None, None, None, None, None]
```


