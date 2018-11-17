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