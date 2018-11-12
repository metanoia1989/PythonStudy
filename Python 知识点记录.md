# pip python包管理器
在线包搜索：<https://pypi.org/>

## 安装
**通过 Linux 包管理器**
- CentOS: `sudo yum install python-pip`
- Debian: `sudo apt install python3-venv python3-pip`

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
- ~/.local/lib/python3.7/site-packages/ 包路径
- ~/.local/bin/pip 可执行文件路径

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

# Python 语句
## 多种赋值方式
**序列解包**
多个赋值操作可以同时进行: `x, y, z = 1, 2, 3`
序列解包(sequence unpacking)或递归解包，将多个值的序列解开，然后放到变量的序列中。
python3 星号运算符: `a, b, *rest = [1, 2, 3, 4]` 
使用星号的变量也可以放在第一个位置，这样它就总会包含一个列表。右侧的赋值语句可以是可迭代对象。

**链式赋值**
链式赋值(charned assignment)是将同一个值赋给多个变量的捷径。
```python
x = y = somefunction() # 和下面语句的效果是一样的：
y = somefunction()
x = y 
```
**增量赋值**
对于+、-、*、/、%等标准运算符都适用：`x += 2`, `x *= 2`, `"foo" += "bar"`

## 条件语句
会被解释器看做 false 的布尔表达式
```python
False    None    0    ""    ()    []    {}
```
事实上，True和False只不过是1和0的一种“华丽”的说法而已——看起来不同，但作用相同。
`bool()` 函数可以用来转换其他值为布尔值

```python
if num > 0: 
    print "The number is positive"
elif num < 0: 
    print "The number is negative"
else: 
    print "The number is zero"
```

**比较运算符**
```python
x == y
x != y　　　　　　　　　 x 不等于 y
x is y　　　　　　　　　 x 和 y 是同一个对象
x is not y　　　　　　　 x 和 y 是不同的对象
x in y　　　　　　　　　 x 是 y 容器(例如，序列)的成员
x not in y　　　　　　　 x 不是 y 容器(例如，序列)的成员
```

**断言**
确保程序中的某一个条件一定为真才能让程序正常工作的话，assert语句可以在程序中置入检查点。
```python
>>> age = -1
>>> assert 0 < age < 100, "The age must be realistic" 
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module> 
    AssertionError: The age must be realistic
```

## 循环
**while循环**
```python
x = 1
while x <= 100
    print x
    x += 1
name = ""
while while not name or name.isspace():
    name = raw_input("Please enter your name: ") 
    print "Hello, %s!" % name
```

**for循环**
內建的zip函数就可以用来进行并行迭代，可以把两个序列“压缩”在一起，然后返回一个元组的列表
zip可以处理不等长的序列，当最短的序列"用完"的时候就会停止
```python
words = ["this", "is", "an", "ex", "parrot"] 
for word in words: 
    print word 

for key, value in d.items(): 
    print key, "corrsponds", value

for name, age in zip(names, ages): 
    print name, "is", age, "years old"

# 按索引迭代
for index, string in enumerate(strings): 
    if "xxx" in string:
        strings[index] = "[censored]"
```

跳出循环：`break` `continue`

**循环中的else子句**
```python
from math import sqrt 
for n in range(99, 81, -1):
    root = sqrt(n) 
    if root == int(root): 
        print n break
else: 
    print "Didn't find it!"
```

`xrange([start,] stop[, step])`    创造xrange对象用于迭代。

**列表推导式——轻量级循环**
列表推导式(list comprehension)是利用其他列表创建新列表(类似于数学术语中的集合推导式)的一种方法。它的工作方式类似于for循环。
列表推导式可以添加 if 部分 和 for 部分。
使用普通的圆括号而不是方括号不会得到“元组推导式”，会得到一个生成器。
```python
>>> [x*x for x in range(10) if x % 3 == 0]
[0, 9, 36, 81] 
>>> [(x, y) for x in range(3) for y in range(3)]
[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)] 
```

## pass exec del 
pass语句 程序什么事情都不用做，在代码中做占位符使用。
del 删除那些不再使用的对象，在Python中是没有办法删除值的，del 只是删除名称，内存回收由python解释器负责。

exec() 执行一个字符串的语句，exec语句最有用的地方在于可以动态地创建代码字符串。
为了安全起见，可以增加一个字典，起到命名空间的作用。
命名空间的概念，或称为作用域(scope)，成保存变量的地方，类似于不可见的字典。
通过增加 `in <scope>` 来实现，其中`<scope>`就是起到放置代码字符串命名空间作用的字典。
```python
# 过exec赋值的变量sqrt只在它的作用域内有效。
>>> from math import sqrt 
>>> scope = {} 
>>> exec "sqrt = 1" in scope 
>>> sqrt(4) 2.0
>>> scope["sqrt"] 
1
```

eval() 类似于exec的內建函数，用于求值。
eval会计算_Python表达式_(以字符串形式书写)，并且返回结果值。
python计算器，好多语言里都有 `eval()`，js里也有，真的超方便的。
```python
>>> eval(raw_input("Enter an arithmetic expression: "))
Enter an arithmetic expression: 6 + 18 * 2
42
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
- str.find() 在一个较长的字符串中查找子串。它返回子串所在位置的最左端索引。如果没有找到则返回-1。
- str.join() 是split方法的逆方法，用来连接序列中的元素。
- str.split() 是join的逆方法，用来将字符串分隔成序列。
- str.lower() 返回字符串的小写字母版
- str.upper() 返回字符串的大写字母版
- str.replace() 返回某字符串的所有匹配项均被替换之后得到字符串。
- str.strip() 返回去除两侧(不包括内部)空格的字符串

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

- 索引：通过编号访问单个元素 `sep[index]`
- 分片：通过冒号隔开的两个索引访问一定范围内的元素 `tag[9:30]` `[0:10:2]`
- 序列相加：通过使用加运算符可以进行序列的连接操作 
- 乘法：用数字x乘以一个序列会生成新的序列，而在新的序列中，原来的序列将被重复x次。
- None、空列表和初始化：空列表可以简单地通过两个中括号进行表示([])
- 成员资格：为了检查一个值是否在序列中，可以使用in运算符
- 长度、最小值和最大值：`len`、`min` 和 `max`
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

## 列表元组操作及方法
**列表函数**
`list()` 将序列转化为列表，可以根据字符串创建列表。
`del` 删除列表中的元素。
`reversed()` 返回一个反向序列的迭代器

**列表方法**
- list.append() 在列表末尾追加新的对象
- list.insert() 将对象插入列表中
- list.pop() 移除列表中的一个元素(默认是最后一个)，并且返回该元素的值
- list.remove() 移除列表中某个值的第一个匹配项
- list.count() 统计某个元素在列表中出现的次数
- list.extend() 在列表的末尾一次性追加另一个序列中的多个值
- list.index() 从列表中找出某个值第一个匹配项的索引位置
- list.reverse() 将列表中的元素反向存放
- list.sort() 使用了固定的排序算法)对列表进行排序

**元组函数**
`tuple()` 以一个序列作为参数并把它转换为元组。

# 字典
列表这种数据结构适合于将值组织到一个结构中，并且通过编号对其进行引用。
通过名字来引用值的数据结构为_映射_(mapping)。字典是Python中唯一內建的映射类型。
字典中的值并没有特殊的顺序，但是都存储在一个特定的键(Key)下。键可以是数字、字符串甚至是元组。
不管是现实中的字典还是在Python中的字典，都是为了可以通过轻松查找某个特定的词语(键)，从而找到它的定义(值)。

> 电话号码(以及其他可能以0开头的数字)应该表示为数字字符串，而不是整数。

dict() 函数通过其他映射或者(键，值)对的序列建立字典，也可以通过关键字参数来创建字典
```python3
>>> d = dict(name="Gumby", age=42) 
>>> d
{'age': 42, 'name': 'Gumby'}
```
 
**字典基本操作** 
`del d[k]`删除键为k的项
`k in d`检查d中是否有含有键为k的项
> 在字典中检查键的成员资格比在列表中检查值的成员资格更高效，数据结构的规模越大，两者的效率差距越明显。

## 字典方法
- `dict.clear()` 清除字典中所有的项
- `dict.copy()` 返回一个具有相同键-值对的新字典，实现*浅复制*(shallow copy)
- `dict.fromKeys()` 使用给定的键建立新的字典，每个键都对应一个默认的值None。
- `dict.get()` 访问一个不存在的键时，没有任何异常，而得到了None值。还可以自定义“默认”值
- `dict.pop()` 获得对应于给定键的值，然后将这个键-值对从字典中移除
- `dict.popitem()` 弹出随机的项
- `dict.setdefault()` 获得与给定键相关联的值，当键不存在的时候，setdefault返回默认值并且相应地更新字典。
- `dict.update()` 利用一个字典项更新另外一个字典，提供的字典中的项会被添加到旧的字典中，若有相同的键则会进行覆盖。
- `dict.keys()` 将字典中的键以列表形式返回
- `dict.iterkeys()` 返回针对键的迭代器
- `dict.items()` 将字典所有的项以列表方式返回，列表中的每一项都表示为(键, 值)对的形式。
- `dict.iteritems()` 返回一个将字典所有的项以迭代器对象方式返回
- `dict.values()` 以列表的形式返回字典中的值
- `dict.itervalues()` 返回值的迭代器


> 浅复制 当在副本中替换值的时候，原始字典不受影响，但是，如果*删除*了某个值，原始的字典也会改变，因为同样的值也存储在原字典中。
> 深复制(deep copy)，复制其包含的所有值。可以使用copy模块的deepcopy函数来完成操作


 
## 字典排序
`sorted()` 排序任何可迭代的对象
```python
sorted(iterable,key,reverse)
iterable表示可以迭代的对象
key是一个函数，用来选取参与比较的元素
reverse则是用来指定排序是倒序还是顺序，True 倒序，False 正序，默认 False
```

**按key值对字典排序**
```python
d = { "lilee": 25, "wangyang": 21, "liqun": 32, "lidaming": 19 }
sorted(d.keys())
# ['lidaming', 'lilee', 'liqun', 'wangyang']
```

**按value值对字典排序**
```python
d = { "lilee": 25, "wangyang": 21, "liqun": 32, "lidaming": 19 }
sorted(d.items(), key=lambda item:item[1])
# [('lidaming', 19), ('wangyang', 21), ('lilee', 25), ('liqun', 32)]
```


## 统计文本的中文字符数
```python
from os import linesep
charBox = {}
filter = [linesep, ', '。', '；', '：', '“', "”"]
with open('./列子.txt', 'r') as f:
    while True:
        char = f.read(1)
        if not char:
            break
        if char in filter:
            continue
        if char not in charBox:
            charBox[char] = 1
        else:
            charBox[char] += 1
charBox = dict(sorted(charBox.items(), key = lambda item: item[1], reverse = True))
print(charBox)
```

# 抽象之函数
只需要告诉计算机下载网页并计算词频。这些操作的具体指令细节会在其他地方给出——在单独的函数定义中。
函数是可以调用的(可能带有参数，也就是放在圆括号中的值)，它执行某种行为并且返回一个值(并非所有Python函数都有返回值)。
`callable()` 可以用来判断函数是否可调用。
`hasattr(func, __call__)` 有python3
`help()` 获取函数的帮助信息
当不需要函数返回值的时候，就返回None。

**定义函数**
```python
def hello(name): 
    return "Hello, " + name + "!"
```

**文档字符串**
如果在函数的开头写下字符串，它就会作为函数的一部分进行存储，这成为文档字符串，用 `__doc__` 属性访问
```python
def square(x): 
    "Calculates the square of the number x."
    return x * x 
# 文档字符串可以按如下方式访问:
>>> square.__doc__
"Calculates the square of the number x."
```

## 函数参数
**关键字参数和默认值**
关键字参数可以在函数中给参数提供默认值，可以打乱传入顺序
```python
def hello_3(greeting="Hello", name="world"): 
    print "%s, %s!" % (greeting, name) 
```

**收集参数**
星号的意思就是"收集其余的位置参数"。
参数前的星号将所有值放置在同一个元组中。可以说是将这些值收集起来。
单星号不能处理关键字参数，双星号将参数放入字典。
```python
def print_params_2(title, *params): 
    print title 
    print params 

def print_params_3(**params): 
    print params 
# 至少解释器没有报错。调用一下看看:
>>> print_params_3(x=1, y=2, z=3)
{'y': 2, 'x': 1, 'z': 3} 
```

## 作用域
如果局部变量或者参数的名字和想要访问的去全局变量相同的话，就不能直接访问了。全局变量会被局部变量屏蔽。
可以使用`globals`函数获取全局变量值，该函数的近亲是`vars`，它可以返回全局变量的字典(locals返回局部变量的字典)。
Python的函数是可以嵌套的，也就是说可以将一个函数放在另一个里面，这样可以生成闭包和装饰器。
nonlocal关键字和global关键字的使用方法类似，可以让用户对外部作用域(但并非全局作用域)的变量进行赋值。

## 递归
**阶乘和幂**
在多数情况下，递归更加易读，有时会大大提高可读性，尤其当读程序的人懂得递归函数的定义的时候。
作为程序员来说还是要理解递归算法以及其他人写的递归程序，这也是最基本的。
```python
def factorial(n): 
    if n == 1: 
        return 1
    else: 
        return n * factorial(n-1)

def power(x, n): 
    if n == 0: 
        return 1
    else: 
        return x * power(x, n-1)
```

**二分法查找**
```python
def search(sequence, number, lower, upper): 
    if lower == upper: 
        assert number == sequence[upper] 
        return upper 
    else:
        middle = (lower + upper) // 2
        if number > sequence[middle]: 
            return search(sequence, number, middle+1, upper) 
        else: 
            return search(sequence, number, lower, middle)
```

## 函数式编程
到现在为止，函数的使用方法和其他对象(字符串、数值、序列，等等)基本上一样，它们可以分配给变量、作为参数传递以及从其他函数返回。有些编程语言(比如Scheme或者LISP)中使用函数几乎可以完成所有的事情。

Python在应对这类“函数式编程”方面有一些有用的函数：map、filter、reduce和apply函数
Python3.0中这些都被移至functools模块中。
`map()` 将序列中的元素全部传递给一个函数
`filter()` 可以基于一个返回布尔值的函数对元素进行过滤
`reduce()` 将序列的前两个元素与给定的函数联合使用，并且将它们的返回值和第3个元素继续联合使用，直到整个序列都处理完毕，并且得到一个最终结果。
`apply()` 调用函数，可以提供参数
```python
# map 
>>> map(str, range(10))  # Equivalent to [str(i) for i in range(10)]
['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# filter
>>> def func(x):
... return x.isalnum()
>>> seq = ["foo", "x41", "?!", "***"] 
>>> filter(func, seq)
['foo', 'x41']
# reduce

```

## lambda表达式
"lambda"来源于希腊字母，在数学中表示匿名函数
```python
>>> filter(lambda x: x.isalnum, seq)
['foo', 'x41']
```


# 文件和流
## 文件模式
open() 用来打开文件
```python
open(name[, mode[, buffering]])
```
open函数使用一个文件名作为唯一的强制参数，然后返回一个文件对象。
open函数的第3个参数(可选)控制着文件的缓冲。如果参数是0(或者是False)，I/O(输入/输出)就是无缓冲的(所有的读写操作都直接针对硬盘)；如果是1(或者True)，I/O就是有缓冲的(意味着Python使用内存来代替硬盘，让程序更快，只有使用flush或者close时才会更新硬盘上的数据，大于1的数字代表缓冲区的大小(单位是字节)，-1(或者是任何负数)代表使用默认的缓冲区大小。

**文件模式**
`+` 参数可以用到其他任何模式中，指明读和写都是允许的
```
'r'　　　　　　　　　　读模式
'w'　　　　　　　　　　写模式
'a'　　　　　　　　　　追加模式
'b'　　　　　　　　　　二进制模式(可添加到其他模式中使用)
'+'　　　　　　　　　　读/写模式(可添加到其他模式中使用)
```

一般来说，Python假定处理的是文本文件(包含字符)。通常这样做不会有任何问题。但是如果处理的是一些其他类型的文件(二进制文件)，比如声音剪辑或者图像，那么应该在模式中增加'b'。参数'rb'可以用来读取一个二进制文件。

Python在这里做了一些自动转换：当在Windows下用文本模式读取文件中的文本时，Python将\r\n转换成\n。相反地，当在Windows下用文本模式向文件写文本时，Python会把\n转换成\r\n(Macintosh系统上的处理也是如此，只是转换是在\r和\n之间进行)。

在使用二进制文件(比如声音剪辑)时可能会产生问题，因为文件中可能包含能被解释成前面提及的换行符的字符，而使用文本模式，Python能自动转换。但是这样会破坏二进制数据。因此为了避免这样的事发生，要使用二进制模式，这样就不会发生转换了。

## 文件对象和流
**类文件对象 流**
类文件对象是支持一些file类方法的对象，最重要的是支持read方法或者write方法，或者两者兼有。那些由urllib.urlopen返回的对象是一个很好的例子。它们支持的方法有read、readline和readlines。

**三种标准的流**
sys模块的三种流实际上是文件(或者是类文件对象)
数据输入的标准源是sys.stdin。当程序从标准输入读取数据时，你可以通过输入或者使用管道把它和其他程序的标准输出链接起来提供文本。
要打印的文本保存在sys.stdout内。input和raw_input函数的提示文字也是写入在sys.stdout中的。写入sys.stdout的数据一般是出现在屏幕上，但也能使用管道连接到其他程序的标准输入。
错误信息(如栈追踪)被写入sys.stderr。它和sys.stdout在很多方面都很像。


## 文件读写
f.write() 写入内容到文件
f.read() 读取文件内容，参数为要读取的长度
f.close() 完成对一个文件的操作
f.seek() 把当前进行读和写的位置移动到指定位置
f.tell() 返回当前文件的位置

f.readline() 读取一行，从当前位置开始直到一个换行符出现，也读取这个换行符。
f.readlines() 读取一个文件中的所有行并将其作为列表返回。
f.writelines() 传给它一个字符串的列表(实际上任何序列或者可迭代的对象都行)，它会把所有的字符串写入文件(或流)。注意，程序不会增加新行，需要自己添加换行符。

> 有os.linesep决定，在使用其他的符号作为换行符的平台上，用\r(Mac中)和\r\n(Windows中)代替\n

```python
# seek 原型
seek(offset[, whence])
Offset类是一个字节(字符)数，表示偏移量。
whence默认是0，表示偏移量是从文件开头开始计算的(偏移量必须是非负的)。
whence可能被设置为1(相对于当前位置的移动，此时偏移量`offset`可以是负的)或者2(相对于文件结尾的移动)。
```

with语句可以打开文件并且将其赋值到变量上(本例是somefile)。之后就可以将数据写入语句体中的文件(或许执行其他操作)。文件在语句结束后会被自动关闭，即使是处于异常引起的结束也是如此。
```python
with open("somefile.txt") as somefile:
    do_something(somefile)
```

## 文件内容迭代
处理文件内容一般都会进行迭代，这是少不了的，需要从中分拆数据。
python的语义化非常地高效，懂得语法、原理，编写代码来会轻松地多。

**按字节处理**
最常见的对文件内容进行迭代的方法是在while循环中使用read方法。
```python
def process(string): 
    print "Processing: ", string

f = open(filename) 
while True:
    char = f.read(1) 
    if not char: 
        break 
    process(char)
f.close
```

**按行操作**
当处理文本文件时，经常会对文件的行进行迭代而不是处理单个字符。处理行使用的方法和处理字符一样，即使用readline方法。
```python
f = open(filename) 
while True:
    line = f.readline() 
    if not line: 
        break 
    process(line)
f.close()
```

**读取所有内容**
如果文件不是很大，那么可以使用不带参数的read方法一次读取整个文件(把整个文件当做一个字符串来读取)，或者使用readlines方法(把文件读入一个字符串列表，在列表中每个字符串就是一行)。在读取后，就可以对字符串使用正则表达式操作，也可以将行列表存入一些数据结构中，以备将来使用。


# 上下文管理器 with
with语句实际上是很通用的结构，允许使用所谓的上下文管理器(context manager)。
上下文管理器是一种支持`__enter__`和`__exit__`这两个方法的对象。
`__enter__`方法不带参数，它在进入with语句块的时候被调用，返回值绑定到在as关键字之后的变量。
`__exit__`方法带有3个参数：异常类型、异常对象和异常回溯。在离开方法(通过带有参数提供的、可引发的异常)时这个函数被调用。
文件可以被用作上下文管理器。它们的`__enter__`方法返回文件对象本身，`__exit__`方法关闭文件。

# 正则表达式


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


# 数据库持久化
要自动序列化，这时可以选择shelve模块，pickle模块



# SQLite Python
PySQLite为SQLite数据库提供了一个标准的Python DBI API 2.0兼容接口。  
SQLite 原生支持的数据类型：NULL, INTEGER, REAL, TEXT, BLOB.  

Emoji表情符号为4个字节的字符，而 utf8 字符集只支持1-3个字节的字符，导致无法写入数据库。
修改MySQL数据库字符集， 把数据库字符集从utf8 修改为支持1-4 个字节字符的utf8mb4。
修改数据库字符集character-set-server=utf8mb4 重启数据库生效。
修改database 的字符集为utf8mb4: `alter database dbname character set utf8mb4`
修改表的字符集 为utf8mb4: `alter table character set=utf8mb4`

```python
Python  SQLite
None	NULL
int	    INTEGER
long	INTEGER
float	REAL
str(UTF8-encoded)	TEXT
unicode	TEXT
buffer	BLOB
```

**创建数据库**
`sqlite3.connect(db_filenam)` 返回一个 Connection 对象  
`Connection.cursor()` 返回游标对象，用来进行增删改查操作  
`Cursor.execute()` 执行SQL语句，第二参数是传入的值组成的元组  
`Cursor.fetchall()` 获取查询的数据集
`Connection.commit()` 提交改变  
`Connection.close()` 关闭连接  

`Cursor.lastrowid` 最后一条数据的id

如果将`:memory:`作为文件名传递给sqlite3模块的connect()函数，它将创建驻留在内存(RAM)中的新数据库，而不是磁盘上的数据库文件。  
执行SQL语句时，使用替代符（parameter substitution） `?`, `%s`, `:1`

```python
import sqlite3
conn = sqlite3.connection(filename) # 创建数据库
c = conn.cursor()
c.execute(create_table_sql) # 执行创建表的sql语句
c.close()
```

```python
conn = sqlite3.connection(dbfilename)
sql = '''DELETE FROM `tasks` WHERE id=?'''
cursor = conn.cursor()
cursor.execute(sql, (id,))
conn.close()
```

查看sqlite3数据库：
```bashk
$ sqlite3 dbname.db
sqlite> .tables
```