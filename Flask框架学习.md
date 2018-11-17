# Flask程序基本结构
所有 Flask 程序都必须创建一个程序实例。Web 服务器使用一种名为 Web 服务器网关接口 （Web Server Gateway Interface，WSGI）的协议，把接收自客户端的所有请求都转交给这个对象处理。  
程序实例是 Flask 类的对象，Flask 类的构造函数只有一个必须指定的参数，即程序主模块或包的名字。在大多数程序
中，Python 的 `__name__` 变量就是所需的值。
```python
from flask import Flask
app = Flask(__name__)
```

客户端（例如 Web 浏览器）把请求发送给 Web 服务器，Web 服务器再把请求发送给 Flask 程序实例。程序实例需要知道对每个 URL 请求运行哪些代码，所以保存了一个 URL 到 Python 函数的映射关系。处理 URL 和函数之间关系的程序称为路由。  
在 Flask 程序中定义路由的最简便方式，是使用程序实例提供的 app.route 修饰器，把修饰的函数注册为路由。  
调用视图函数时，Flask 会将动态部分作为参数传入函数。  
路由中的动态部分默认使用字符串，不过也可使用类型定义。例如，路由 `/user/<int:id>` 只会匹配动态片段 id 为整数的 URL。  
Flask 支持在路由中使用 int、float 和 path 类型。path 类型也是字符串，但不把斜线视作分隔符，而将其当作动态片段的一部分。   
```python
@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/user/<name>')
def user(name):
 return '<h1>Hello, %s!</h1>' % name
```
> 修饰器是 Python 语言的标准特性，可以使用不同的方式修改函数的行为。惯常用法是使用修饰器把函数注册为事件的处理程序。

程序实例用 run 方法启动 Flask 集成的开发 Web 服务器。    
服务器启动后，会进入轮询，等待并处理请求。轮询会一直运行，直到程序停止，比如按 Ctrl-C 键。  
```python
if __name__ == '__main__':
    app.run(debug=True)
```

## 程序和请求上下文
Flask 从客户端收到请求时，要让视图函数能访问一些对象，这样才能处理请求。请求对象就是一个很好的例子，它封装了客户端发送的 HTTP 请求。  
在 Flask 中有两种上下文：程序上下文和请求上下文。
```txt
current_app 程序上下文 当前激活程序的程序实例
g 程序上下文 处理请求时用作临时存储的对象。每次请求都会重设这个变量
request 请求上下文 请求对象，封装了客户端发出的 HTTP 请求中的内容
session 请求上下文 用户会话，用于存储请求之间需要“记住”的值的词典
```
**在请求上下文中使用 request 获取 headers 头**
```python
@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>' % user_agent
```

Flask 在分发请求之前激活（或推送）程序和请求上下文，请求处理完成后再将其删除。程序上下文被推送后，就可以在线程中使用 current_app 和 g 变量。类似地，请求上下文被 推送后，就可以使用 request 和 session 变量。如果使用这些变量时我们没有激活程序上下文或请求上下文，就会导致错误。  

```python
>>> from hello import app
>>> from flask import current_app
>>> current_app.name
程序的基本结构 ｜ 13
Traceback (most recent call last):
...
RuntimeError: working outside of application context
>>> app_ctx = app.app_context()
>>> app_ctx.push()
>>> current_app.name
'hello'
>>> app_ctx.pop()
```

## 请求调度
程序收到客户端发来的请求时，要找到处理该请求的视图函数，Flask 会在程序的 URL 映射中查找请求的 URL。  
Flask 使用 `app.route` 修饰器或者非修饰器形式的 `app.add_url_rule()` 生成映射。  
```python
(venv) $ python
>>> from hello import app
>>> app.url_map
Map([<Rule '/' (HEAD, OPTIONS, GET) -> index>,
<Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>,
<Rule '/user/<name>' (HEAD, OPTIONS, GET) -> user>])
```

## 请求钩子
在处理请求之前或之后执行代码。在请求开始时，我们可能需要创建数据库连接或者认证发起请求的用户。  
Flask 提供了注册通用函数的功能，注册的函数可在请求被分发到视图函数之前或之后调用。  
请求钩子使用修饰器实现: 

- `before_first_request`: 注册一个函数，在处理第一个请求之前运行。
- `before_request`: 注册一个函数，在每次请求之前运行。
- `after_request`: 注册一个函数，如果没有未处理的异常抛出，在每次请求之后运行。
- `teardown_request`: 注册一个函数，即使有未处理的异常抛出，也在每次请求之后运行。

在请求钩子函数和视图函数之间共享数据一般使用上下文全局变量 `g` 。例如， `before_ request` 处理程序可以从数据库中加载已登录用户，并将其保存到 `g.user` 中。随后调用视图函数时，视图函数再使用 `g.user` 获取用户。  

## 响应
Flask 调用视图函数后，会将其返回值作为响应的内容。大多数情况下，响应就是一个简单的字符串，作为 HTML 页面回送客户端。   
HTTP 协议需要的不仅是作为请求响应的字符串。HTTP 响应中一个很重要的部分是状态码，Flask 默认设为 200，这个代码表明请求已经被成功处理。  
如果视图函数返回的响应需要使用不同的状态码，那么可以把数字代码作为第二个返回值，添加到响应文本之后。  
视图函数返回的响应还可接受第三个参数，这是一个由首部（header）组成的字典，可以添加到 HTTP 响应中。
```python
# 返回一个 400 状态码，表示请求无效
@app.route('/400')
def 400():
    return '<h1>Bad Request</h1>', 400
```

如果不想返回由 1 个、2 个或 3 个值组成的元组，Flask 视图函数还可以返回 `Response` 对象。 `make_response()` 函数可接受 1 个、2 个或 3 个参数（和视图函数的返回值一样），并返回一个 `Response` 对象。有时我们需要在视图函数中进行这种转换，然后在响应对象上调用各种方法，进一步设置响应。  
```python
def index():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response
```

**重定向响应** 没有页面文档，只告诉浏览器一个新地址用以加载新页面。重定向经常在 Web 表单中使用.  
重定向经常使用 `302` 状态码表示，指向的地址由 `Location` 首部提供。重定向响应可以使用 3 个值形式的返回值生成，也可在 `Response` 对象中设定。不过，由于使用频繁，Flask 提供了 `redirect()` 辅助函数，用于生成这种响应  

代码敲上去居然报错: TypeError: redirect() takes 0 positional arguments but 1 was given  
下面这段代码我一直没有看出什么，redirect() 调用的是正确的啊，没问题啊，难道是没在服务器上，所以这样？  
最后看到函数名，才知道，麻蛋把外部导入的包给覆盖掉了，结果最后调用的是自己，无语了我简直。
```python
@app.route('/redirect')
def redirect():
    return redirect('/400', 302)
```

**错误处理响应** 由 abort 函数生成，abort 不会把控制权交还给调用它的函数，而是抛出异常把控制权交给 Web 服务器。  
```python
from flask import abort
@app.route('/user/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return '<h1>Hello, %s</h1>' % user.name
```

## Flask-Script支持命令行
Flask 的开发 Web 服务器支持很多启动设置选项，但只能在脚本中作为参数传给 app.run() 函数。  
Flask-Script 是一个 Flask 扩展，为 Flask 程序添加了一个命令行解析器。Flask-Script 自带了一组常用选项，而且还支持自定义命令。  
```sh
$ pip install flask-script
```
然后将 app 对象注入 Manager 对象中
```python
from flask_script import Manager
manager = Manager(app)
# ...
if __name__ == '__main__':
manager.run()
```
把程序实例作为参数传给构造函数，初始化主类的实例。创建的对象可以在各个扩展中使用。在这里，服务器由 manager.run() 启 动，启动后就能解析命令行了。  

```sh
$ python hello.py
usage: hello.py [-h] {shell,runserver} ...

positional arguments:
    {shell,runserver}
        shell 在 Flask 应用上下文中运行 Python shell
        runserver 运行 Flask 开发服务器：app.run()
optional arguments:
    -h, --help 显示帮助信息并退出
```
shell 命令用于在程序的上下文中启动 Python shell 会话。你可以使用这个会话中运行维护任务或测试，还可调试异常。
runserver 命令用来启动 Web 服务器。运行 python hello.py runserver 将以调试模式启动 Web 服务器
```sh
optional arguments:
  -?, --help            show this help message and exit
  -h HOST, --host HOST
  -p PORT, --port PORT
  --threaded
  --processes PROCESSES
  --passthrough-errors
  -d, --debug           enable the Werkzeug debugger (DO NOT use in production
                        code)
  -D, --no-debug        disable the Werkzeug debugger
  -r, --reload          monitor Python files for changes (not 100% safe for
                        production use)
  -R, --no-reload       do not monitor Python files for changes
```
运行服务器: `$ python3 hello.py runserver --host 0.0.0.0 --port 8888 --debug`


# Jinja2模板引擎
业务逻辑和表现逻辑，把业务逻辑和表现逻辑混在一起会导致代码难以理解和维护。假设要为一个大型表格构建 HTML 代码，表格中的数据由数据库中读取的数据以及必要的 HTML 字符串连接在一起。把表现逻辑移到模板中能够提升程序的可维护性。   
模板是一个包含响应文本的文件，其中包含用占位变量表示的动态部分，其具体值只在请求的上下文中才能知道。使用真实值替换变量，再返回最终得到的响应字符串，这一过程称为渲染。   

Flask 提供的 `render_template` 函数把 Jinja2 模板引擎集成到了程序中。 `render_template` 函数的第一个参数是模板的文件名。随后的参数都是键值对，表示模板中变量对应的真实值。

```html
# templates/index.html
<h1>Hello World!</h1>
# templates/user.html
<h1>Hello, {{ name }}!</h1>
```
```python
from flask import Flask, render_template
# ...
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
```

## 变量
在模板中使用的 `{{ name }}` 结构表示一个变量，它是一种特殊的占位符，告诉模板引擎这个位置的值从渲染模板时使用的数据中获取。  
jinja2 能识别所有类型的变量，甚至是一些复杂的类型，例如列表、字典和对象。  
还可以使用过滤器修改变量，过滤器名添加在变量名之后，中间使用竖线分隔。
```html
<p>A value from a dictionary: {{ mydict['key'] }}.</p>
<p>A value from a list: {{ mylist[3] }}.</p>
<p>A value from a list, with a variable index: {{ mylist[myintvar] }}.</p>
<p>A value from an object's method: {{ myobj.somemethod() }}.</p>
<!-- 过滤器 -->
Hello, {{ name|capitalize }}
```
Jinja2 变量过滤器
```table
safe 渲染值时不转义
capitalize 把值的首字母转换成大写，其他字母转换成小写
lower 把值转换成小写形式
upper 把值转换成大写形式
title 把值中每个单词的首字母都转换成大写
trim 把值的首尾空格去掉
striptags 渲染之前把值中所有的 HTML 标签都删掉
```
出于安全考虑，Jinja2 会转义所有变量，使用 safe 过滤器将不会转义直接输出

## 控制结构
Jinja2 提供了多种控制结构，可用来改变模板的渲染流程  
**条件控制语句**
```html
{% if user   %}
    Hello, {{ user }}!
{% else %}
    Hello, Stranger!
{% endif %}
```

**for循环**
```html
<ul>
    {% for comment in comments %}
        <li>{{ comment }}</li>
    {% endfor %}
</ul>
```

**宏支持 - 类似函数**
```html
{% macro render_comment(comment) %}
    <li>{{ comment }}</li>
{% endmacro %}

<ul>
    {% for comment in comments %}
        {{ render_comment(comment) }}
    {% endfor %}
</ul>
```
可以把宏单独保存到文件中：
```html
{% import 'macros.html' as macros %}
<ul>
    {% for comment in comments %}
        {{ macros.render_comment(comment) }}
    {% endfor %}
</ul>
```

**文件引入**
```html
{% include 'common.html' %}
```

**模板继承**
```html
<!--  base.html -->
<html>
<head>
    {% block head %}
        <title>{% block title %}{% endblock %} - My Application</title>
    {% endblock %}
</head>
<body>
    {% block body %}
    {% endblock %}
</body>
</html>
```
继承模板文件后直接写内容到 block 即可
```html
{% extends "base.html" %}
{% block title %}Index{% endblock %}
{% block head %}
    {{ super() }}
    <style>
    </style>
{% endblock %}
{% block body %}
<h1>Hello, World!</h1>
{% endblock %}
```
extends 指令声明模板继承，注意新定义的 head 块，在基模板中其内容不是空的，所以使用 `super()` 获取原来的内容。

## Flask-Bootstrap
Bootstrap 是客户端框架，因此不会直接涉及服务器。服务器需要做的只是提供引用了 Bootstrap 层 叠 样 式 表（CSS） 和 JavaScript 文 件 的 HTML 响 应， 并 在 HTML、CSS 和 JavaScript 代码中实例化所需组件。这些操作最理想的执行场所就是模板。

安装  Flask-Bootstrap 的 Flask 扩展 无需修改模板: `pip install flask-bootstrap`
Flask 扩展一般都在创建程序实例时初始化，初始化 Flask-Bootstrap 之后，就可以在程序中使用一个包含所有 Bootstrap 文件的基模板。
```python
from flask_bootstrap import Bootstrap
# ...
bootstrap = Bootstrap(app)
```


# 资源链接
- [jinja模板引擎](http://jinja.pocoo.org/docs/2.10/)
- [flask 框架文档](http://flask.pocoo.org/docs/1.0/)
