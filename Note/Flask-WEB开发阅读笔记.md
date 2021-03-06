[TOC]
# 资源链接
- [jinja模板引擎](http://jinja.pocoo.org/docs/2.10/)
- [flask 框架文档](http://flask.pocoo.org/docs/1.0/)

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

## current_user
current_user ，因为这个变量是上下文代理对象。真正的 User 对象要使用表达式 current_user._get_current_object() 获取。     


## cookie
set_cookie() 函数的前两个参数分别是 cookie 名和值。可选的 max_age 参数设置 cookie 的过期时间，单位为秒。如果不指定参数 max_age ，浏览器关闭后 cookie 就会过期。 

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

`url_for()` 方法接收的是视图方法名，不是 `app.route()` 的参数名

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

## 注释
```
变量  {{ ... }}
程序命令 {% ... %}
注释 {# ... #} 
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

Flask-Bootstrap 的 base.html 模板还定义了很多其他块，都可在衍生模板中使用。
```html
doc 整个 HTML 文档
html_attribs <html> 标签的属性
html <html> 标签中的内容
head <head> 标签中的内容
title <title> 标签中的内容
metas 一组 <meta> 标签
styles 层叠样式表定义
body_attribs <body> 标签的属性
body <body> 标签中的内容
navbar 用户定义的导航条
content 用户定义的页面内容
scripts 文档底部的 JavaScript 声明
```
很多块都是 Flask-Bootstrap 已经使用，里面有内容的，直接重定义可能会导致一些问题。例如，Bootstrap 所需的文件在 styles 和 scripts 块中声明。如果程序需要向已经有内容的块中添加新内容，必须使用 Jinja2 提供的 super() 函数，因为 Bootstrap 依赖的 js css 文件都在里面加载的。
```html
{% block scripts %}
    {{ super() }}
    <script type="text/javascript" src="my-script.js"></script>
{% endblock %}
```    

## 自定义错误页面
如果你在浏览器的地址栏中输入了不可用的路由，那么会显示一个状态码为 404 的错误页面。默认的404页面太简陋了，样式也与网站样式不一致。  
Flask 允许程序使用基于模板的自定义错误页面。最常见的错误代码有两个：404，客户端请求未知页面或路由时显示；500，有未处理的异常时显示。  
```python
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
```

## 链接
任何具有多个路由的程序都需要可以连接不同页面的链接，例如导航条。  
直接编写 URL 会对代码中定义的路由产生不必要的依赖关系。如果重新定义路由，模板中的链接可能会失效。  
Flask 提供了 `url_for()` 辅助函数，使用程序 URL 映射中保存的信息生成 URL。  
`url_for()` 函数最简单的用法是以视图函数名，作为参数，返回对应的 URL。  
`app.add_url_route()` 定义路由时使用的端点名作为参数，返回对应的 URL。
```python
url_for('index') 返回 /
url_for('index', _external=True)  返回  http://localhost:5000/
```
生成连接程序内不同路由的链接时，使用相对地址就足够了。如果要生成在浏览器之外使用的链接，则必须使用绝对地址。    
使用 `url_for()` 生成动态路由地址时，将动态部分作为关键字参数传入，
传入 `url_for()` 的关键字参数不仅限于动态路由中的参数。函数能将任何额外参数添加到查询字符串中。
```python
url_for('user', name='john', _external=True)  返回  http://localhost:5000/user/john
url_for('index', page=2) 的返回结果是 /?page=2
```

## 静态文件
对静态文件的引用被当成一个特殊的路由，即 `/static/<filename>`  
```python
调用 `url_for('static', filename='css/styles.css', _external=True)` 
得 到 的 结 果 是 `http://localhost:5000/static/css/styles.css`  
```

Flask 在程序根目录中名为 static 的子目录中寻找静态文件。如果需要，可在
static 文件夹中使用子文件夹存放文件。服务器收到前面那个 URL 后，会生成一个响应，
包含文件系统中 static/css/styles.css 文件的内容。

模板内插入网站图标，图标的声明会插入 head 块的末尾。注意如何使用 super() 保留基模板中定义的块的原始
内容。
```html
# templates/base.html：定义收藏夹图标
{% block head %}
    {{ super() }}
    <link rel="shortcut icon" href="{{ url_for('static', filename = 'favicon.ico') }}"
    type="image/x-icon">
    <link rel="icon" href="{{ url_for('static', filename = 'favicon.ico') }}"
    type="image/x-icon">
{% endblock %}
```

## Flask-Moment本地化日期和时间
如果 Web 程序的用户来自世界各地，那么处理日期和时间可不是一个简单的任务。  
服务器需要统一时间单位，这和用户所在的地理位置无关，所以一般使用协调世界时（Coordinated Universal Time，UTC）。  
在服务器上只使用 UTC 时间，而用户需要看到当地时间，而且采用当地惯用的格式。   
把时间单位发送给 Web 浏览器，转换成当地时间，然后渲染。Web 浏览器可以更好地完成这一任务，因为它能获取用户电脑中的时区和区域设置。   
前端的库  [moment.js](http://momentjs.com/) 可以在浏览器中渲染日期和时间。  
Flask-Moment 是一个 Flask 程序扩展，能把 moment.js 集成到 Jinja2 模板中。   
momentJs文档: <http://momentjs.com/docs/#/displaying/>    
Flask-Moment地址: <https://github.com/miguelgrinberg/Flask-Moment>    

安装 Flask-Moment: `$ pip install flask-moment`   
初始化 Flask-Moment:
```python
from flask_moment import Moment
moment = Moment(app)
```
除了 moment.js，Flask-Moment 还依赖 jquery.js。  
Bootstrap 已经引入了 jquery.js，因此只需引入 moment.js 即可。  
```html
# emplates/base.html
{% block scripts %}
    {{ super() }}
    {{ moment.include_jquery() }}
    {{ moment.include_moment() }}
    {{ moment.lang('zh-cn) }}
{% endblock %}
```
Flask-Monet 假定服务器端程序处理的时间戳是“纯正的” datetime 对象，且使用 UTC 表示。
Flask-Moment 渲染的时间戳可实现多种语言的本地化。语言可在模板中选择，把语言代码传给 `lang()` 函数即可: `{{ moment.lang('zh-cn') }}`

为了处理时间戳，Flask-Moment 向模板开放了 moment 类。
```python
# 把变量 current_time 传入模板进行渲染。
from datetime import datetime
@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())
```
**templates/index.html**
```html
<p>当前时间：{{ moment(current_time).format('LLL') }}</p>
<p>相对时间：{{ moment(current_time).fromNow(refresh=True) }}</p>
<!-- 当前时间：November 17, 2018 2:31 PM -->
<!-- 相对时间：in a few seconds -->
```
`format('LLL')` 根据客户端电脑中的时区和区域设置渲染日期和时间。参数决定了渲染的方式， 'L' 到 'LLLL' 分别对应不同的复杂度。   
`fromNow()` 渲染相对时间戳，而且会随着时间的推移自动刷新显示的时间。这个时间戳最开始显示为“a few seconds ago”，但指定 refresh 参数后，其内容会随着时间的推移而更新。如果一直待在这个页面，几分钟后，会看到显示的文本变成“a minute ago”“2 minutes ago”等。
好像 twitter, gitlab 都用了相对时间戳。  
Flask-Moment 实现了 moment.js 中的 `format()` 、 `fromNow()` 、 `fromTime()` 、 `calendar()` 、 `valueOf()` 和 `unix()` 方法。  


# Web 表单
请求对象包含客户端发出的所有请求信息， request.form 能获取 POST 请求中提交的表单数据。  
Flask 的请求对象提供的信息足够用于处理 Web 表单，包括生成表单的 HTML 代码和验证提交的表单数据。  
[Flask-WTF](http://pythonhosted.org/Flask-WTF/)扩展对独立的 [WTForms](http://wtforms.simplecodes.com)包进行了包装，方便集成到 Flask 程序中。  
安装 Flask-WTF: `$ pip install flask-wtf`  

## 跨站请求伪造保护
默认情况下，Flask-WTF 能保护所有表单免受跨站请求伪造（Cross-Site Request Forgery， CSRF）的攻击。恶意网站把请求发送到被攻击者已登录的其他网站时就会引发 CSRF 攻击。  
为了实现 CSRF 保护，Flask-WTF 需要程序设置一个密钥。Flask-WTF 使用这个密钥生成加密令牌，再用令牌验证请求中表单数据的真伪，即是否由本网站发送的。  
**设置 Flask-WTF 秘钥**
```python
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
```
app.config 字典可用来存储框架、扩展和程序本身的配置变量。使用标准的字典句法就能把配置值添加到 app.config 对象中。这个对象还提供了一些方法，可以从文件或环境中导入配置值。  
SECRET_KEY 配置变量是通用密钥，可在 Flask 和多个第三方扩展中使用。加密的强度取决于变量值的机密程度。不同的程序要使用不同的密钥，而且要保证其他人不知道你所用的字符串。  
为了增强安全性，密钥不应该直接写入代码，而要保存在环境变量中。  

## 表单类
使用 Flask-WTF 时，每个 Web 表单都由一个继承自 Form 的类表示。这个类定义表单中的一组字段，每个字段都用对象表示。字段对象可附属一个或多个验证函数。验证函数用来验证用户提交的输入值是否符合要求。  
> 感觉这样虽然很方便，但是有些过度封装的感觉，从头到脚都弄得清清楚楚，开发起来很快，不去看源代码，就不知道工作流程了。  

**定义表单类**
```python
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')
```
字段构造函数的第一个参数是把表单渲染成 HTML 时使用的标号。  
StringField 构造函数中的可选参数 validators 指定一个由验证函数组成的列表，在接受用户提交的数据之前验证数据。验证函数 Required() 确保提交的字段不为空。  
Form 基类由 Flask-WTF 扩展定义，所以从 flask_wtf 中导入。字段和验证函数却可以直接从 WTForms 包中导入。  
**WTForms 支持的 HTML 标准字段**: 
```python
StringField 文本字段
TextAreaField 多行文本字段
PasswordField 密码文本字段
HiddenField 隐藏文本字段
DateField 文本字段，值为 datetime.date 格式
DateTimeField 文本字段，值为 datetime.datetime 格式
IntegerField 文本字段，值为整数
DecimalField 文本字段，值为 decimal.Decimal
FloatField 文本字段，值为浮点数
BooleanField 复选框，值为 True 和 False
RadioField 一组单选框
SelectField 下拉列表
SelectMultipleField 下拉列表，可选择多个值
FileField 文件上传字段
SubmitField 表单提交按钮
FormField 把表单作为字段嵌入另一个表单
FieldList 一组指定类型的字段
```

**WTForms 内建的验证函数**  
```python
Email 验证电子邮件地址
EqualTo 比较两个字段的值；常用于要求输入两次密码进行确认的情况
IPAddress 验证 IPv4 网络地址
Length 验证输入字符串的长度
NumberRange 验证输入的值在数字范围内
Optional 无输入值时跳过其他验证函数
Required 确保字段中有数据
Regexp 使用正则表达式验证输入值
URL 验证 URL
AnyOf 确保输入值在可选值列表中
NoneOf 确保输入值不在可选值列表中
```

## 把表单渲染成HTML
表单字段是可调用的，在模板中调用后会渲染成 HTML。  
视图函数把一个 NameForm 实例通过参数 form 传入模板，在模板中可以生成一个简单的表单。  
改进表单的外观，可以把参数传入渲染字段的函数，传入的参数会被转换成字段的 HTML 属性。  
可以为字段指定 id 或 class 属性，然后定义 CSS 样式  
```html
<form method="POST">
    {{ form.hidden_tag() }}
    {{ form.name.label }} {{ form.name(id='my-text-field') }}
    {{ form.submit() }}
</form>
```
通过表单类渲染样式效率很低，Flask-Bootstrap 提供了一个非常高端的辅助函数，可以使用 Bootstrap 中预先定义好的表单样式渲染整个 Flask-WTF 表单，而这些操作只需一次调用即可完成。  
```html
{% import "bootstrap/wtf.html" as wtf %}
{{ wtf.quick_form(form) }}
```

## 在视图函数中处理表单
```python
@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name)
```
app.route 修饰器中添加的 methods 参数告诉 Flask 在 URL 映射中把这个视图函数注册为GET 和 POST 请求的处理程序。如果没指定 methods 参数，就只把视图函数注册为 GET 请求的处理程序。  
提交表单后，如果数据能被所有验证函数接受，那么 `validate_on_submit()` 方法的返回值为 True ，否则返回 False 。 这个函数的返回值决定是重新渲染表单还是处理表单提交的数据。  

## 重定向和用户会话
用户输入名字后提交表单，然后点击浏览器的刷新按钮，会看到一个莫名其妙的警告，要求在再次提交表单之前进行确认。之所以出现这种情况，是因为刷新页面时浏览器会重新发送之前已经发送过的最后一个请求。如果这个请求是一个包含表单数据的 POST 请求，刷新页面后会再次提交表单。   

使用重定向作为 POST 请求的响应，而不是使用常规响应。重定向是一种特殊的响应，响应内容是 URL，而不是包含 HTML 代码的字符串。浏览器收到这种响应时，会向重定向的 URL 发起 GET 请求，显示页面的内容。这个页面的加载可能要多花几微秒，因为要先把第二个请求发给服务器。  

最后一个请求是 GET 请求，所以刷新命令能像预期的那样正常使用了。这个技巧称为 Post/ 重定向 /Get 模式。  

程序处理 POST 请求时，使用 form.name.data 获取用户输入的名字，可是一旦这个请求结束，数据也就丢失了。因为这个 POST 请求使用重定向处理，所以程序需要保存输入的名字，这样重定向后的请求才能获得并使用这个名字，从而构建真正的响应。  

程序可以把数据存储在用户会话中，在请求之间“记住”数据。用户会话是一种私有存储，存在于每个连接到服务器的客户端中。  

用户会话，它是请求上下文中的变量，名为 session ，像标准的 Python 字典一样操作。  

redirect() 是个辅助函数， 用来生成 HTTP 重定向响应。 `redirect()` 函数的参数是重定向的 URL，这里使用的重定向 URL 是程序的根地址，因此重定向响应本可以写得更简单一些，写成 `redirect('/')` ，但却会使用 Flask 提供的 URL 生成函数 `url_for()` 。推荐使用 `url_for()` 生成 URL，因为这个函数使用 URL 映射生成 URL，从而保证 URL 和定义的路由兼容，而且修改路由名字后依然可用。   
```python
from flask import Flask, render_template, session, redirect, url_for
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data 
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))
```

## Flash消息
请求完成后，有时需要让用户知道状态发生了变化。这里可以使用确认消息、警告或者错误提醒。一个典型例子是，用户提交了有一项错误的登录表单后，服务器发回的响应重新渲染了登录表单，并在表单上面显示一个消息，提示用户用户名或密码错误。  
flash() 函数可实现这种效果。  

最好在基模板中渲染 Flash 消息，因为这样所有页面都能使用这些消息。Flask 把 `get_flashed_messages()` 函数开放给模板，用来获取并渲染消息  
```python
from flask import Flask, render_template, session, redirect, url_for, flash
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
    if old_name is not None and old_name != form.name.data:
        flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form = form, name = session.get('name'))
```
**templates/base.html 渲染模板消息**
```html
{% block content %}
<div class="container">
    {% for message in get_flashed_messages() %}
    <div class="alert alert-warning">
        <button type="button" class="close" data-dismiss="alert">&times;</button>
        {{ message }}
    </div>
    {% endfor %}
    {% block page_content %}{% endblock %}
</div>
{% endblock %}
```

# 数据库
数据库按照一定规则保存程序数据，程序再发起查询取回所需的数据。  
Web 程序最常用基于关系模型的数据库，这种数据库也称为 SQL 数据库，因为它们使用结构化查询语言。  
不过最近几年文档数据库和键值对数据库成了流行的替代选择，这两种数据库合称 NoSQL数据库。  

各种类型的数据库包:  MySQL、Postgres、SQLite、 Redis、MongoDB 或者 CouchDB。     
数据库抽象层代码包:   SQLAlchemy 和 MongoEngine。  
用这些抽象包直接处理高等级的 Python 对象，而不用处理如表、文档或查询语言此类的数据库实体。  

抽象层，也称为对象关系映射（Object-Relational Mapper，ORM）或对象文档映射（Object-Document Mapper，ODM），在用户不知觉的情况下把高层的面向对象操作转换成低层的数据库指令。  
ORM 和 ODM 把对象业务转换成数据库业务会有一定的损耗。大多数情况下，这种性能的降低微不足道，但也不一定都是如此。一般情况下，ORM 和 ODM 对生产率的提升远远超过了这一丁点儿的性能降低，所以性能降低这个理由不足以说服用户完全放弃 ORM 和 ODM。   
真正的关键点在于如何选择一个能直接操作低层数据库的抽象层，以防特定的操作需要直接使用数据库原生指令优化。  

[SQLAlchemy ORM](http://www.sqlalchemy.org/) 就是一个很好的例子，它支持很多关系型数据库引擎，包括流行的 MySQL、Postgres 和 SQLite。  
[Flask-SQLAlchemy](http://pythonhosted.org/Flask-SQLAlchemy/)  集成了 Flask 的框架可以简化配置和操作，节省你编写集成代码的时间。  


## noSQL
NoSQL 数据库一般使用集合代替表，使用文档代替记录。NoSQL 数据库采用的设计方式使联结变得困难，所以大多数数据库根本不支持这种操作。  
这是执行反规范化操作得到的结果，它减少了表的数量，却增加了数据重复量。这种结构的数据库要把角色名存储在每个用户中。如此一来，将角色重命名的操作就变得很耗时，可能需要更新大量文档。使用 NoSQL 数据库当然也有好处。数据重复可以提升查询速度。列出用户及其角色的操作很简单，因为无需联结。    

SQL 数据库擅于用高效且紧凑的形式存储结构化数据。这种数据库需要花费大量精力保证数据的一致性。NoSQL 数据库放宽了对这种一致性的要求，从而获得性能上的优势。对中小型程序来说，SQL 和 NoSQL 数据库都是很好的选择，而且性能相当。  


## Flask-SQLAlchemy 
Flask-SQLAlchemy 是一个 Flask 扩展，简化了在 Flask 程序中使用 SQLAlchemy 的操作。  
SQLAlchemy 是一个很强大的关系型数据库框架，支持多种数据库后台。SQLAlchemy 提供了高层 ORM，也提供了使用数据库原生 SQL 的低层功能。  
Flask-SQLAlchemy 也使用 pip 安装: `$ pip install flask-sqlalchemy`   
在 Flask-SQLAlchemy 中，数据库使用 URL 指定。
**FLask-SQLAlchemy数据库URL**
```python
MySQL mysql://username:password@hostname/database
Postgres postgresql://username:password@hostname/database
SQLite（Unix） sqlite:////absolute/path/to/database
SQLite（Windows） sqlite:///c:/absolute/path/to/database
```
hostname 表示 MySQL 服务所在的主机  
database 表示要使用的数据库名  
username 和 password 表示数据库用户密令  

SQLite 数据库不需要使用服务器，因此不用指定 hostname、username 和 password。URL 中的 database 是硬盘上文件的文件名。  

程序使用的数据库 URL 必须保存到 Flask 配置对象的 `SQLALCHEMY_DATABASE_URI` 键中。  
配置对象中还有一个很有用的选项，即 `SQLALCHEMY_COMMIT_ON_TEARDOWN` 键，将其设为 True 时，每次请求结束后都会自动提交数据库中的变动。
```python
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# db 对象是 SQLAlchemy 类的实例，表示程序使用的数据库，同时还获得了 Flask-SQLAlchemy 提供的所有功能。
db = SQLAlchemy(app)
```

## 定义模型
模型这个术语表示程序使用的持久化实体。在 ORM 中，模型一般是一个 Python 类，类中的属性对应数据库表中的列。  
Flask-SQLAlchemy 创建的数据库实例为模型提供了一个基类以及一系列辅助类和辅助函数，可用于定义模型的结构。  
Flask-SQLAlchemy 要求每个模型都要定义 主键 ，这一列经常命名为 id 。  
类变量 `__tablename__` 定义在数据库中使用的表名，其余的类变量都是该模型的属性，被定义为 db.Column 类的实例。  
db.Column 类构造函数的第一个参数是数据库列和模型属性的类型。  
两个模型都定义了 `__repr()__` 方法，返回一个具有可读性的字符串表示模型，可在调试和测试时使用。   
```python
class Role(db.Model):
    """ Role 表模型 """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    """ User表模型 """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<User %r>' % self.name
```
**最常用的SQLAlchemy列类型**
```python
Integer int 普通整数，一般是 32 位
SmallInteger int 取值范围小的整数，一般是 16 位
BigInteger int 或 long 不限制精度的整数
Float float 浮点数
Numeric decimal.Decimal 定点数
String str 变长字符串
Text str 变长字符串，对较长或不限长度的字符串做了优化
Unicode unicode 变长 Unicode 字符串
UnicodeText unicode 变长 Unicode 字符串，对较长或不限长度的字符串做了优化
Boolean bool 布尔值
Date datetime.date 日期
Time datetime.time 时间
DateTime datetime.datetime 日期和时间
Interval datetime.timedelta 时间间隔
Enum str 一组字符串
PickleType 任何 Python 对象 自动使用 Pickle 序列化
LargeBinary str 二进制文件
```
**db.Column 中其余的参数指定属性的配置选项**
```python
primary_key 如果设为 True ，这列就是表的主键
unique 如果设为 True ，这列不允许出现重复的值
index 如果设为 True ，为这列创建索引，提升查询效率
nullable 如果设为 True ，这列允许使用空值；如果设为 False ，这列不允许使用空值
default 为这列定义默认值
```

## 模型关联
关系型数据库使用关系把不同表中的行联系起来，如角色到用户的一对多关系，因为一个角色可属于多个用户，而每个用户都只能有一个角色。  
关系使用 users 表中的外键连接了两行。添加到 User 模型中的 `role_id` 列被定义为外键，就是这个外键建立起了关系。传给 `db.ForeignKey()` 的参数 'roles.id' 表明，这列的值是 roles 表中行的 id 值。   
`db.relationship()` 的第一个参数表明这个关系的另一端是哪个模型。 backref 参数向 User 模型中添加一个 role 属性，从而定义反向关系。这一属性可替代 role_id 访问 Role 模型，此时获取的是模型对象，而不是外键的值。

> 这种关联一般都是 ORM 的难点。

```python
class Role(db.Model):
    # ...
    users = db.relationship('User', backref='role')
class User(db.Model):
    # ...
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
```

**常用的SQLAlchemy关系选项**
```python
backref 在关系的另一个模型中添加反向引用
primaryjoin 明确指定两个模型之间使用的联结条件。只在模棱两可的关系中需要指定
lazy 指定如何加载相关记录。
> 可选值有 select （首次访问时按需加载）、 
> immediate （源对象加载后就加载）、 
> joined （加载记录，但使用联结）、 
> subquery （立即加载，但使用子查询）， 
> noload （永不加载）和 dynamic （不加载记录，但提供加载记录的查询）
uselist 如果设为 Fales ，不使用列表，而使用标量值
order_by 指定关系中记录的排序方式
secondary 指定多对多关系中关系表的名字
secondaryjoin SQLAlchemy 无法自行决定时，指定多对多关系中的二级联结条件
```

## 数据库操作
数据库会话也称为事务，通过数据库会话管理对数据库所做的改动，在 Flask-SQLAlchemy 中，会话由 db.session
表示。准备把对象写入数据库之前，先要将其添加到会话中。      
把对象添加到会话：db.session.add()      
添加多个对象到会话：db.session.add_all()        
提交会话：db.session.commit()       
回滚操作： db.session.rollback()

数据库会话能保证数据库的一致性。提交操作使用原子方式把会话中的对象全部写入数据库。如果在写入会话的过程中发生了错误，整个会话都会失效。如果你始终把相关改动放在会话中提交，就能避免因部分更新导致的数据库不一致性。  
数据库会话也可以回滚，回滚之后添加到数据库会话中的所有对象都会还原到它们在数据库时的状态。      

修改行：db.session.add() 方法 
删除行：db.seesion.delete() 方法
```python
# 更新
>>> admin_role.name = 'Administrator'
>>> db.session.add(admin_role)
>>> db.session.commit()
# 删除
>>> db.session.delete(mod_role)
>>> db.session.commit()
```

Flask-SQLAlchemy 为每个模型类都提供了 query 对象: `Role.query.all()`
使用过滤器可以配置 query 对象进行更精确的数据库查询: `User.query.filter_by(role=user_role).all()`
查看 SQLAlchemy 为查询生成的原生 SQL 查询语句，把 query 对象转换成字符串: `str(User.query.filter_by(role=user_role))`

**常用的SQLAlchemy查询过滤器**
```python
filter() 把过滤器添加到原查询上，返回一个新查询
filter_by() 把等值过滤器添加到原查询上，返回一个新查询
limit() 使用指定的值限制原查询返回的结果数量，返回一个新查询
offset() 偏移原查询返回的结果，返回一个新查询
order_by() 根据指定条件对原查询结果进行排序，返回一个新查询
group_by() 根据指定条件对原查询结果进行分组，返回一个新查询
```

**最常使用的SQLAlchemy查询执行函数**
```python
all() 以列表形式返回查询的所有结果
first() 返回查询的第一个结果，如果没有结果，则返回 None
first_or_404() 返回查询的第一个结果，如果没有结果，则终止请求，返回 404 错误响应
get() 返回指定主键对应的行，如果没有对应的行，则返回 None
get_or_404() 返回指定主键对应的行，如果没找到指定的主键，则终止请求，返回 404 错误响应
count() 返回查询结果的数量
paginate() 返回一个 Paginate 对象，它包含指定范围内的结果
```

## 集成Python shell
让 Flask-Script 的 shell 命令自动导入特定的对象，编程的乐趣就这里，一次编写，省很多事。     
若想把对象添加到导入列表中，为 shell 命令注册一个 `make_context` 回调函数   
```python
from flask_script import Shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
```
make_shell_context() 函数注册了程序、数据库实例以及模型，因此这些对象能直接导入 shell   

```python
In [1]: app                                                                                               
Out[1]: <Flask 'index'>
In [2]: db                                                                                                
Out[2]: <SQLAlchemy engine=sqlite:////home/smithadam/Code/python/Flask/data.sqlite>
In [3]: User                                                                                              
Out[3]: __main__.User
In [4]: Role                                                                                              
Out[4]: __main__.Role
```

## Flask-Migrate 数据库迁移
更新表的更好方法是使用数据库迁移框架。源码版本控制工具可以跟踪源码文件的变化，类似地，数据库迁移框架能跟踪数据库模式的变化，然后增量式的把变化应用到数据库中。  
SQLAlchemy 的主力开发人员编写了一个迁移框架，称为 [Alembic](https://alembic.readthedocs.org/en/latest/index.html)       
[Flask-Migrate](http://flask-migrate.readthedocs.org/en/latest/)扩展对 Alembic 做了轻量级包装，并集成到 Flask-Script 中，所有操作都通过 Flask-Script 命令完成。     

安装 Flask-Migrate: `$ pip install flask-migrate`
配置 Flask-Migrate 初始化:
```python
from flask_migrate import Migrate, MigrateCommand
# ...
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
```
为了导出数据库迁移命令，Flask-Migrate 提供了一个 MigrateCommand 类，可附加到 Flask-Script 的 manager 对象上。     

**迁移初始化**
初始化数据库迁移库：`$ python hello.py db init`     
这个命令会创建 migrations 文件夹，所有迁移脚本都存放其中，数据库迁移仓库中的文件要和程序的其他文件一起纳入版本控制。  
在 Alembic 中，数据库迁移用迁移脚本表示。脚本中有两个函数，分别是 upgrade() 和 downgrade() 。       
upgrade() 函数把迁移中的改动应用到数据库中， downgrade() 函数则将改动删除。     

Alembic 具有添加和删除改动的能力，因此数据库可重设到修改历史的任意一点。        

使用 revision 命令手动创建 Alembic 迁移，也可使用 migrate 命令自动创建。 手动创建的迁移只是一个骨架， upgrade() 和 downgrade() 函数都是空的，开发者要使用 Alembic 提供的 Operations 对象指令实现具体操作。自动创建的迁移会根据模型定义和数据库当前状态之间的差异生成 upgrade() 和 downgrade() 函数的内容。

migrate 子命令用来自动创建迁移脚本: `$ python hello.py db migrate -m "initial migration"`
使用 db upgrade 命令把迁移应用到数据库中: `$ python hello.py db upgrade`

# 电子邮件
很多类型的应用程序都需要在特定事件发生时提醒用户，而常用的通信方法是电子邮件。      
Python 标准库中的 smtplib 包可用在 Flask 程序中发送电子邮件，但包装了 smtplib 的 Flask-Mail 扩展能更好地和 Flask 集成。     

Flask-Mail 安装：`$ pip install flask-mail`     
Flask-Mail 连接到SMTP服务器，并把邮件交给这个服务器发送。如果不进行配置，Flask-Mail 会连接 localhost 上的端口 25，无需验证即可发送电子邮件。        
**Flask-Mail SMTP服务器的配置**
```python
MAIL_SERVER localhost 电子邮件服务器的主机名或 IP 地址
MAIL_PORT 25 电子邮件服务器的端口
MAIL_USE_TLS False 启用传输层安全（Transport Layer Security，TLS）协议
MAIL_USE_SSL False 启用安全套接层（Secure Sockets Layer，SSL）协议
MAIL_USERNAME None 邮件账户的用户名
MAIL_PASSWORD None 邮件账户的密码
```

配置 Flask-Mail 使用 Gmail
```python
import os
# ...
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
```
Flask-Mail扩展初始化:
```python
from flask.ext.mail import Mail
mail = Mail(app)
```
保存电子邮件服务器用户名和密码的两个环境变量要在环境中定义:
```sh
$ export MAIL_USERNAME=<Gmail username>
$ export MAIL_PASSWORD=<Gmail password>
```

# 大型程序结构
```
|-app/
    |-templates/
    |-static/
    |-main/
        |-__init__.py
        |-errors.py
        |-forms.py
        |-views.py
    |-__init__.py
    |-email.py
    |-models.py
|-migrations/
|-tests/
    |-__init__.py
    |-test*.py
|-venv/
|-requirements.txt
|-config.py
|-manage.py
```
Flask 程序一般都保存在名为 app 的包中；     
和之前一样，migrations 文件夹包含数据库迁移脚本；   
单元测试编写在 tests 包中；     
和之前一样，venv 文件夹包含 Python 虚拟环境。   
requirements.txt 列出了所有依赖包，便于在其他电脑中重新生成相同的虚拟环境；     
config.py 存储配置；    
manage.py 用于启动程序以及其他的程序任务。      

**配置**        
序经常需要设定多个配置，开发、测试和生产环境要使用不同的数据库，这样才不会彼此影响。    
基类 Config 中包含通用配置，子类分别定义专用的配置。如果需要，你还可添加其他配置类。    

**程序包**      
程序包用来保存程序的所有代码、模板和静态文件。我们可以把这个包直接称为 app（应用），如果有需求，也可使用一个程序专用名字。templates 和 static 文件夹是程序包的一部分，因此这两个文件夹被移到了 app 中。数据库模型和电子邮件支持函数也被移到了这个包中，分别保存为 app/models.py 和 app/email.py     

## 使用程序工厂函数       
构造文件导入了大多数正在使用的 Flask 扩展。由于尚未初始化所需的程序实例，所以没有初始化扩展，创建扩展类时没有向构造函数传入参数。 create_app() 函数就是程序的工厂函数，接受一个参数，是程序使用的配置名。   

配置类在 config.py 文件中定义，其中保存的配置可以使用 Flask app.config 配置对象提供的 from_object() 方法直接导入程序。至于配置对象，则可以通过名字从 config 字典中选择。程序创建并配置好后，就能初始化扩展了。在之前创建的扩展对象上调用 init_app() 可以完成初始化过程。        
```python
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
def create_db(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    # 附加路由定义和错误页面
    return app
```
现在工厂函数创建的程序还不完整，因为没有路由和自定义的错误页面处理程序。    

## 在蓝本中实现程序功能        
转换成程序工厂函数的操作让定义路由变复杂了。在单脚本程序中，程序实例存在于全局作用域中，路由可以直接使用 app.route 修饰器定义。但现在程序在运行时创建，只有调用 create_app() 之后才能使用 app.route 修饰器，这时定义路由就太晚了。和路由一样，自定义的错误页面处理程序也面临相同的困难，因为错误页面处理程序使用 app.errorhandler 修饰器定义。      
> 不是很懂这个过程，先抄下来吧  

蓝本和程序类似，也可以定义路由。不同的是，在蓝本中定义的路由处于休眠状态，直到蓝本注册到程序上后，路由才真正成为程序的一部分。使用位于全局作用域中的蓝本时，定义路由的方法几乎和单脚本程序一样。
> 所以说蓝本其实是一种另类的路由，blueprint 什么破名字！        

在蓝本中编写错误处理程序稍有不同，如果使用 errorhandler 修饰器，那么只有蓝本中的错误才能触发处理程序。要想注册程序全局的错误处理程序，必须使用 app_errorhandler 。  
```python
from flask import render_template
from . import main
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
```

在蓝本中就不一样了，Flask 会为蓝本中的全部端点加上一个命名空间，这样就可以在不同的蓝本中使用相同的端点名定义视图函数，而不会产生冲突。命名空间就是蓝本的名字（ Blueprint 构造函数的第一个参数），所以视图函数 index() 注册的端点名是 main.index ，其 URL 使用 url_for('main.index') 获取。      

url_for() 函数还支持一种简写的端点形式，在蓝本中可以省略蓝本名，例如 url_for('.index') 。在这种写法中，命名空间是当前请求所在的蓝本。这意味着同一蓝本中的重定向可以使用简写形式，但跨蓝本的重定向必须使用带有命名空间的端点名。     

蓝本其实就是flask的一种模块化编程的方式，什么命名空间、路由注册，都是为这个服务的。什么破名字，取得真是太烂了，直接跟别人说这个，打死也不会明白这是什么东西。   

## 单元测试
Python 标准库中的 unittest 包编写。 setUp() 和 tearDown() 方法分别在各测试前后运行，并且名字以 test_ 开头的函数都作为测试执行。     
```python
import unittest
from flask import current_app
from app import create_app, db

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
```

manager.command 修饰器让自定义命令变得简单。修饰函数名就是命令名，函数的文档字符串会显示在帮助消息中。  
添加自定义命令：
```python
@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
```

# 用户认证
大多数程序都要进行用户跟踪。用户连接程序时会进行身份认证，通过这一过程，让程序知道自己的身份。程序知道用户是谁后，就能提供有针对性的体验。      
最常用的认证方法要求用户提供一个身份证明（用户的电子邮件或用户名）和一个密码。  

Flask的认证扩展:
`Flask-Login`：管理已登录用户的用户会话       
`Werkzeug`：计算密码散列值并进行核对      
`itsdangerous`：生成并核对加密安全令牌    

生成安全密码散列值 - [Salted Password Hashing - Doing it Right](https://crackstation.net/hashing-security.htm)  
## Werkzeug实现密码散列    
`generate_password_hash(password, method= • pbkdf2:sha1, salt_length=8)`        
将原始密码作为输入，以字符串形式输出密码的散列值，输出的值可保存在用户数据库中。 
method 和 salt_length 的默认值就能满足大多数需求。      

`check_password_hash(hash, password)`       
函数的参数是从数据库中取回的密码散列值和用户输入的密码。返回值为 True 表明密码正确。    

## Flask-Login认证用户
使用 Flask-Login 扩展，程序的 User 模型必须实现几个方法
**Flask-Login要求实现的用户方法** 
```table
is_authenticated() 如果用户已经登录，必须返回 True ，否则返回 False
is_active() 如果允许用户登录，必须返回 True ，否则返回 False 。如果要禁用账户，可以返回 False
is_anonymous() 对普通用户必须返回 False
get_id() 必须返回用户的唯一标识符，使用 Unicode 编码字符串
```

这 4 个方法可以在模型类中作为方法直接实现，不过还有一种更简单的替代方案。Flask-Login 提供了一个 UserMixin 类，其中包含这些方法的默认实现，且能满足大多数需求，只需繼承就可以。  
```python
from flask.ext.login import UserMixin
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
```

> 在这个程序中，用户使用电子邮件地址登录，因为相对于用户名而言，用户更不容易忘记自己的电子邮件地址。（認同！）  

LoginManager 对象的 session_protection 属性可以设为 None 、 'basic' 或 'strong' ，以提供不同的安全等级防止用户会话遭篡改。设为 'strong' 时，Flask-Login 会记录客户端 IP 地址和浏览器的用户代理信息，如果发现异动就登出用户。 login_view 属性设置登录页面的端点。回忆一下，登录路由在蓝本中定义，因此要在前面加上蓝本的名字。        

为了保护路由只让认证用户访问，Flask-Login 提供了一个 login_required 修饰器。    
如果未认证的用户访问这个路由，Flask-Login 会拦截请求，把用户发往登录页面。  
```python
from flask.ext.login import login_required
@app.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'
```


变量 current_user 由 Flask-Login 定义，且在视图函数和模板中自动可用。   
这个变量的值是当前登录的用户，如果用户尚未登录，则是一个匿名用户代理对象。如果是匿名用户， is_authenticated 属性为 False 。

当请求类型是 GET 时，视图函数直接渲染模板，即显示表单。当表单在 POST 请求中提交时， Flask-WTF 中的 `validate_on_submit()` 函数会验证表单数据，然后尝试登入用户。    

视图函数首先使用表单中填写的 email 从数据库中加载用户。如果电子邮件地址对应的用户存在，再调用用户对象的 verify_password() 方法，其参数是表单中填写的密码。如果密码正确，则调用 Flask-Login 中的 login_user() 函数，在用户会话中把用户标记为已登录。 login_user() 函数的参数是要登录的用户，以及可选的“记住我”布尔值，“记住我”也在表单中填写。如果值为 False ，那么关闭浏览器后用户会话就过期了，所以下次用户访问时要重新登录。如果值为 True ，那么会在用户浏览器中写入一个长期有效的 cookie，使用这个 cookie 可以复现用户会话。         

cookie 的作用就在这里，可以保持长期的会话。     

### current_user.is_authenticated() TypeError: 'bool' object is not callable
- [if current_user.is_authenticated(): TypeError: 'bool' object is not callable](https://github.com/dpgaspar/Flask-AppBuilder/issues/235)

current_user.isauthenticated() 方法已被移除，改成属性了，难怪报错了。。。。晕倒。       
```python
{% if current_user.is_authenticated %}
  Hi {{ current_user.name }}!
{% endif %}
```

### AnonymousUser
定义了 AnonymousUser 类，并实现了 can() 方法和 is_administrator() 方法。这个对象继承自 Flask-Login 中的 AnonymousUserMixin 类，并将其设为用户未登录时 current_user 的值。这样程序不用先检查用户是否登录，就能自由调用 current_user.can() 和 current_user.is_administrator() 。      

如果你想让视图函数只对具有特定权限的用户开放，可以使用自定义的修饰器。      
下面实现两个修饰器，一个用来检查常规权限，一个专门用来检查管理员权限。  
```python
from functools import wraps
from flask import abort
from flask.ext.login import current_user
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)
```

### 模板权限
在模板中可能也需要检查权限，所以 Permission 类为所有位定义了常量以便于获取。为了避免每次调用 render_template() 时都多添加一个模板参数，可以使用上下文处理器。上下文处理器能让变量在所有模板中全局可访问。       

## itsdangerous 生成确认令牌
确认邮件中最简单的确认链接是 <http://www.example.com/auth/confirm/<id>> 这种形式的 URL，其中 id 是数据库分配给用户的数字 id 。用户点击链接后，处理这个路由的视图函数就将收到的用户 id 作为参数进行确认，然后将用户状态更新为已确认。但这种实现方式显然不是很安全，只要用户能判断确认链接的格式，就可以随便指定 URL中的数字，从而确认任意账户。解决方法是把 URL 中的 id 换成将相同信息安全加密后得到的令牌。     

Flask 使用加密的签名 cookie 保护用户会话，防止被篡改。这种安全的 cookie 使用 itsdangerous 包签名。同样的方法也可用于确认令牌上。        
```python
(venv) $ python manage.py shell
>>> from manage import app
>>> from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
用户认证 ｜ 91
>>> s = Serializer(app.config['SECRET_KEY'], expires_in = 3600)
>>> token = s.dumps({ 'confirm': 23 })
>>> token
'eyJhbGciOiJIUzI1NiIsImV4cCI6MTM4MTcxODU1OCwiaWF0IjoxMzgxNzE0OTU4fQ.ey ...'
>>> data = s.loads(token)
>>> data
{u'confirm': 23}
```
itsdangerous 提供了多种生成令牌的方法。其中， TimedJSONWebSignatureSerializer 类生成具有过期时间的 JSON Web 签名（JSON Web Signatures，JWS）。这个类的构造函数接收的参数是一个密钥，在 Flask 程序中可使用 SECRET_KEY 设置。     

dumps() 方法为指定的数据生成一个加密签名，然后再对数据和签名进行序列化，生成令牌字符串。 expires_in 参数设置令牌的过期时间，单位为秒。      

为了解码令牌，序列化对象提供了 loads() 方法，其唯一的参数是令牌字符串。这个方法会检验签名和过期时间，如果通过，返回原始数据。如果提供给 loads() 方法的令牌不正确或过期了，则抛出异常。      


## before_request before_app_request
对蓝本来说， before_request 钩子只能应用到属于蓝本的请求上。若想在蓝本中使用针对程序全局请求的钩子，必须使用 before_app_request 修饰器。        
如果 before_request 或 before_app_request 的回调返回响应或重定向，Flask 会直接将其发送至客户端，而不会调用请求的视图函数。因此，这些回调可在必要时拦截请求。    


## Gravatar 用户头像
Gravatar 是一个行业领先的头像服务，能把头像和电子邮件地址关联起来。用户先要到 http://gravatar.com 中注册账户，然后上传图片。生成头像的 URL 时，要计算电子邮件地址的 MD5 散列值，生 成 的 头 像 URL 是 在 http://www.gravatar.com/avatar/ 或 https://secure.gravatar.com/avatar/ 之后加上这个 MD5 散列值。   
python 生成md5值: `hashlib.md5(str.encode('utf-8')).hexdigest()`

如果这个电子邮件地址没有对应的头像，则会显示一个默认图片。头像 URL 的查询字符串中可以包含多个参数以配置头像图片的特征。 
Gravatar查询字符串参数
```
s 图片大小，单位为像素
r 图片级别。可选值有 "g" 、 "pg" 、 "r" 和 "x"
d 没有注册 Gravatar 服务的用户使用的默认图片生成方式。可选值有： "404" ，返回 404 错误；默
认图片的 URL；图片生成器 "mm" 、 "identicon" 、 "monsterid" 、 "wavatar" 、 "retro" 或 "blank"
之一
fd 强制使用默认头像
```

# forgerypy 创建虚拟数据
有多个 Python 包可用于生成虚拟信息，其中功能相对完善的是 ForgeryPy  

ForgeryPy 并不是这个程序的依赖，因为它只在开发过程中使用。为了区分生产环境的依赖和开发环境的依赖，我们可以把文件 requirements.txt 换成 requirements 文件夹，它们分别保存不同环境中的依赖。  

# Flask-SQLAlchemy
## 分页 
paginate() 方法的返回值是一个 Pagination 类对象，这个类在 Flask-SQLAlchemy 中定义。这个对象包含很多属性，用于在模板中生成分页链接，因此将其作为参数传入了模板。 
**Flask-SQLAlchemy分页对象的属性**
```python
items 当前页面中的记录
query 分页的源查询
page 当前页数
prev_num 上一页的页数
next_num 下一页的页数
has_next 如果有下一页，返回 True
has_prev 如果有上一页，返回 True
pages 查询得到的总页数
per_page 每页显示的记录数量
total 查询返回的记录总数
```
**在Flask-SQLAlchemy分页对象上可调用的方法**
```python
iter_pages (left_edge=2, left_current=2, right_current=5, right_edge=2)
一个迭代器，返回一个在分页导航中显示的页数列表。
这个列表的最左边显示 left_ edge 页，
当前页的左边显示 left_current 页，
当前页的右边显示 right_current 页，
最右边显示 right_edge 页。
例如，在一个 100 页的列表中，当前页为第 50 页，
使用 默认配置，这个方法会返回以下页数：
1、2、 None 、48、49、50、51、52、53、54、 55、 None 、99、100。 
None 表示页数之间的间隔
prev() 上一页的分页对象
next() 下一页的分页对象
```

app/templates/_macros.html：分页模板宏
```html
```

## 关联
数据库使用关系建立记录之间的联系。其中，一对多关系是最常用的关系类型，它把一个记录和一组相关的记录联系在一起。实现这种关系时，要在“多”这一侧加入一个外键，指向“一”这一侧联接的记录。    
大部分的其他关系类型都可以从一对多类型中衍生。多对一关系从“多”这一侧看，就是一对多关系。一对一关系类型是简化版的一对多关系，限制“多”这一侧最多只能有一个记录。唯一不能从一对多关系中简单演化出来的类型是多对多关系，这种关系的两侧都有多个记录。        

一对多关系、多对一关系和一对一关系至少都有一侧是单个实体，所以记录之间的联系通过外键实现，让外键指向这个实体。  
解决方法是添加第三张表，这个表称为关联表。现在，多对多关系可以分解成原表和关联表之间的两个一对多关系。  

多对多关系仍使用定义一对多关系的 db.relationship() 方法进行定义，但在多对多关系中，必须把 secondary 参数设为关联表。多对多关系可以在任何一个类中定义， backref 参数会处理好关系的另一侧。关联表就是一个简单的表，不是模型，SQLAlchemy 会自动接管这个表。    
```python
registrations = db.Table('registrations',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
    db.Column('class_id', db.Integer, db.ForeignKey('classes.id'))
)
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    classes = db.relationship('Class',
    secondary=registrations,
    backref=db.backref('students', lazy='dynamic'),
    lazy='dynamic')
class Class(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)

s.classes.append(c)
s.classes.remove(c)
db.session.add(s)
s.classes.all()
c.students.all()
```

**自引用关系**
多对多关系可用于实现用户之间的关注，但存在一个问题。在学生和课程的例子中，关联表联接的是两个明确的实体。但是，表示用户关注其他用户时，只有用户一个实体，没有第二个实体。    
如果关系中的两侧都在同一个表中，这种关系称为自引用关系。在关注中，关系的左侧是用户实体，可以称为“关注者”；关系的右侧也是用户实体，但这些是“被关注者”。  

**高级多对多关系**
使用多对多关系时，往往需要存储所联两个实体之间的额外信息。对用户之间的关注来说，可以存储用户关注另一个用户的日期，这样就能按照时间顺序列出所有关注者。这种信息只能存储在关联表中，但是在之前实现的学生和课程之间的关系中，关联表完全是由 SQLAlchemy 掌控的内部表。  
为了能在关系中处理自定义的数据，我们必须提升关联表的地位，使其变成程序可访问的模型。    



# Markdown Flask-PageDown 富文本
PageDown：使用 JavaScript 实现的客户端 Markdown 到 HTML 的转换程序。
Flask-PageDown：为 Flask 包装的 PageDown，把 PageDown 集成到 Flask-WTF 表单中。
Markdown：使用 Python 实现的服务器端 Markdown 到 HTML 的转换程序。
Bleach：使用 Python 实现的 HTML 清理器。


# 使用Flask-PageDown
Flask-PageDown 扩展定义了一个 PageDownField 类，这个类和 WTForms 中的 TextAreaField 接口一致。  
使用 PageDownField 字段之前，先要初始化扩展：
```python
from flask_pagedown import PageDown
# ...
pagedown = PageDown()
# ...
def create_app(config_name):
    # ...
    pagedown.init_app(app)
    # ...
```

更换表单对象的文本域控件：
```python
from flask_pagedown.fields import PageDownField
class PostForm(Form):
    body = PageDownField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')
```

Markdown 预览使用 PageDown 库生成，因此要在模板中修改。Flask-PageDown 简化了这个过程，提供了一个模板宏，从 CDN 中加载所需文件。     
```html
{% block scripts %}
{{ super() }}
{{ pagedown.include_pagedown() }}
{% endblock %}
```

## 服务器处理富文本的业务逻辑
提交表单后， POST 请求只会发送纯 Markdown 文本，页面中显示的 HTML 预览会被丢掉。和表单一起发送生成的 HTML 预览有安全隐患，因为攻击者轻易就能修改 HTML 代码，让其和 Markdown 源不匹配，然后再提交表单。  
只提交 Markdown 源文本，在
服务器上使用 Markdown（使用 Python 编写的 Markdown 到 HTML 转换程序）将其转换成 HTML。得到 HTML 后，再使用 Bleach 进行清理，确保其中只包含几个允许使用的 HTML 标签。    

把 Markdown 格式的博客文章转换成 HTML 的过程可以在 _posts.html 模板中完成，但这么做效率不高，因为每次渲染页面时都要转换一次。避免重复工作，可在创建博客文章时做一次性转换。转换后的博客文章 HTML 代码缓存在 Post 模型的一个新字段中，在模板中可以直接调用。文章的 Markdown 源文本还要保存在数据库中，以防需要编辑。     


# Flask-HTTPAuth 认证用户
REST Web 服务的特征之一是无状态，即服务器在两次请求之间不能“记住”客户端的任何信息。客户端必须在发出的请求中包含所有必要信息，因此所有请求都必须包含用户密令。   
REST 架构基于 HTTP 协议，所以发送密令的最佳方式是使用 HTTP 认证，基本认证和摘要认证都可以。在 HTTP 认证中，用户密令包含在请求的 Authorization 首部中。 

Flask-HTTPAuth 扩展提供了一个便利的包装，可以把协议的细节隐藏在修饰器之中，类似于 Flask-Login 提供的 login_required 修饰器。        

在将 HTTP 基本认证的扩展进行初始化之前，我们先要创建一个 HTTPBasicAuth 类对象。和 Flask-Login 一样，Flask-HTTPAuth 不对验证用户密令所需的步骤做任何假设，因此所需的信息在回调函数中提供。   

由于每次请求时都要传送用户密令，所以 API 路由最好通过安全的 HTTP 提供，加密所有的请求和响应。   
http是明文传输的，非常容易监听，传送密令非常不安全，最好用设置有效期的 token .

## 基于令牌的认证
每次请求时，客户端都要发送认证密令。为了避免总是发送敏感信息，可以提供一种基于令牌的认证方案。  
使用基于令牌的认证方案时，客户端要先把登录密令发送给一个特殊的 URL，从而生成认证令牌。一旦客户端获得令牌，就可用令牌代替登录密令认证请求。    
出于安全考虑，令牌有过期时间。令牌过期后，客户端必须重新发送登录密令以生成新令牌。  
令牌落入他人之手所带来的安全隐患受限于令牌的短暂使用期限。      
为了生成和验证认证令牌，我们要在 User 模型中定义两个新方法。    
