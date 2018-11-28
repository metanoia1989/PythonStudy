# HTML to PDF
爬取在线的文档，然后转换成pdf，这样就可以在本地看文档了，非常方便学习。 
标准库里应该有专门处理 pdf 的，也有第三方库。   

weasyprint 使用 gtk库  [在线文档](https://weasyprint.readthedocs.io/en/latest/tutorial.html)
xhtml2pdf  使用 ReportLab 之前看人做文档pdf的就是用这个 [在线文档](https://xhtml2pdf.readthedocs.io/en/latest/)
pypdf2 
pdfkit 封装 wkhtmltopdf [README](https://pypi.org/project/pdfkit/)

windows 终端工具 
ConEmu

# 相关资料
- [Python PDF Series](https://www.blog.pythonlibrary.org/tag/python-pdf-series/)
- [How to Generate PDF Files in Python with Xhtml2pdf, WeasyPrint or Unoconv](https://gearheart.io/blog/how-generate-pdf-files-python-xhtml2pdf-weasyprint-or-unoconv/)


# python 知识点
Python3中也有urllib和urllib3两个库，其中urllib几乎是Python2中urllib和urllib2两个模块的集合，所以我们最常用的urllib模块，而urllib3则作为一个拓展模块使用。   
url 编码 urllib.parse.urlencode(values)

dir()用来寻找一个对象的所有属性，包括`__dict__`中的属性，`__dict__`是dir()的子集；  

因为要用到 html，爬虫是必不可少的，复杂的爬虫，会涉及到监控的问题。

- [快来学习怎么可视化监控你的爬虫](https://cuiqingcai.com/6217.html)

**http 客户端**
[requests](http://docs.python-requests.org/en/master/) 第三方请求库的事实标准     
httpie 命令行 api 调试工具      
[urllib3](https://urllib3.readthedocs.io/) 支持线程安全的连接池，requests的底层库

<http://httpbin.org/> HTTP Request & Response Service, written in Python + Flask。   
源代码可以作为api开发的参考，我可以在网上找相关的flask api的源码，快速学习掌握怎么api开发的规范。   

**yaml解析库**  
- [PyYAML is a YAML parser and emitter for Python.](https://pyyaml.org/wiki/PyYAMLDocumentation)

# 抓取网页设计到的库和工具
## 相关库
网页抓取：urllib, requests, aiohttp, Selenium, Splash   
网页解析：re, lxml, Beautiful Soup, pyquery     
数据存储：JSON, XML, CSV, MySQL, MongoDB, Redis     
Web组件: Flask, Tornado     
反爬虫: Tesserocr, ProxyPool, CookiesPool       
App抓取：Charles, mitmproxy, mitmdump, Appium       
爬虫框架：pyspider, Scrapy, Scrapy-Redis, Scrapy-Splash         
管理部署: Docker, Scrapyd, Scrapyd-API, Gerapy  

在互联网时代，获取整理网络资源，爬虫必不可少。  
- [你需要这些：Python3.x爬虫学习资料整理](https://zhuanlan.zhihu.com/p/24358829)

## 书籍推荐    
Python3网络爬虫开发实战 崔庆才  
Python网络数据采集      



# sqlite3 class
把 sqlite3 封装成类，更易于使用
- [Python/16 Databases/sqlite3-class.py](https://github.com/hassanazimi/Python/blob/master/16%20Databases/sqlite3-class.py)
- [Python Sqlite3 wrapper](https://gist.github.com/goldsborough/c973d934f620e16678bf)
- [a small, expressive orm -- supports postgresql, mysql and sqlite](https://github.com/coleifer/peewee)
- [A thorough guide to SQLite database operations in Python](https://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html)
- [Peewee中文文档【二】：快速开始](https://blog.csdn.net/amoscn/article/details/74529133)
- [python中sqlite3对数据库的增删改查](https://blog.csdn.net/liuyanlin610/article/details/76021959)


一些 python orm 封装类 Peewee, Storm, SQLObject, SQLAlchemy

一般的数据库类不会动表，因为表都是实现创建好的，封装的话，一般都是用原生的sql语句。 
而那些 orm 数据库对象映射，也是基于表已经创建的情况。   
= = 被打脸了，设置好模型之后，peewee 有 create_table 的方法

我先用我那简单的封装就好，一个完善的orm类，会有连接池、并发各种设计，==，基础太薄弱，简单地封装，能用就行。 

# mysql 数据库操作类
Python和MySQL交互的模块有 MySQLdb 和 PyMySQL，MySQLdb是基于C 语言编写的，包名叫做 `MySQL-python`。
PyMySQL是一个纯Python写的MySQL客户端，它的目标是替代MySQLdb，可以在CPython、PyPy、IronPython和Jython环境下运行,PyMySQL在MIT许可下发布。  

- [【Python】基于pymysql的数据库操作类](http://www.liuhaihua.cn/archives/494969.html)
- [Python 常见数据库操作技巧](https://www.jb51.net/Special/681.htm)
- [Python中使用Flask、MongoDB搭建简易图片服务器](https://www.jb51.net/article/60738.htm)


# @property 属性方法
- [子类中扩展property](https://python3-cookbook.readthedocs.io/zh_CN/latest/c08/p08_extending_property_in_subclass.html)
- [How does the @property decorator work?](https://stackoverflow.com/questions/17330160/how-does-the-property-decorator-work)

利用属性方法，可以实现设置属性时检测参数，获取属性时检测权限等等    
@property装饰器就是负责把一个方法变成属性调用的，可以将逻辑放到里面。   
把一个getter方法变成属性，只需要加上@property就可以了，@property本身又创建了另一个装饰器@name.setter，负责把一个setter方法变成属性赋值。       
定义只读属性，只定义getter方法，不定义setter方法  
一个property其实是 getter、setter 和 deleter 方法的集合，而不是单个方法。   

```python
class Person:
    def __init__(self, name):
        self.name = name

    # Getter function
    @property
    def name(self):
        return self._name

    # Setter function
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._name = value

    # Deleter function
    @name.deleter
    def name(self):
        raise AttributeError("Can't delete attribute")
```

Remember, that the @decorator syntax is just syntactic sugar; the syntax:
```python
@property
def foo(self): return self._foo
```
really means the same thing as
```python
def foo(self): return self._foo
foo = property(foo)
```

Python 为了语法的简洁，真的是丧尽天良   





# pipenv 现代的依赖管理
pip 其实比起 npm composer 有过时的感觉，依赖竟然用txt文本存储，并且每个项目都要创建一个virtualvenv，实在太蠢了  
pipenv 使用 Pipfile 和 Pipfile.lock 解决依赖包记录的问题，漂亮！果然是一个有活力的社区。    

文档地址: <https://pipenv.readthedocs.io/en/latest/>    

创建虚拟环境: `$ pipenv --python 3.7`   or `$ pipenv install`
激活虚拟环境：`$ pipenv shell`  
输出依赖：`$ pipenv graph`  
运行虚拟环境的程序：`$ pipenv run pip freeze`   
安装包作为开发依赖：`$ pipenv install package --dev`   
安装系统依赖： `$ pipenv install --system`
卸载: `$ pipenv uninstall` `--all` `--all-dev`   
生成 requirements.txt 文件输出： `$ pipenv lock -r`
生成 dev-packages 的 requirements.txt 的文件输出：`$ pipenv lock -r -d`
从 requirements.txt 文件中安装依赖：`$ pipenv install -r` 
生成 Lockfile 文件: `$ pipenv lock`

设置镜像，直接修改Pipfile文件，或者设置环境变量 `PIPENV_PYPI_MIRROR`    

示例 Pipenv 文件
```ini
[[source]]
url = "https://pypi.python.org/simple"
verify_ssl = true
name = "pypi"

[packages]
requests = "*"

[dev-packages]
pytest = "*"
```

私有的pypi，pipenv 会自动展开环境变量。
```python
[[source]]
url = "https://$USERNAME:${PASSWORD}@mypypi.example.com/simple"
verify_ssl = true
name = "pypi"
```

**自动加载环境变量.env**
如果项目根目录下有.env文件，`$ pipenv shell` 和`$ pipenv run`会自动加载它。  

# urllib3
```python
import urllib3
# 创建连接池实例
http = urllib3.PoolManager()
# 发起 get 请求
res = http.request('GET', 'http://httpbin.org/robots.txt')
# 发起 post 请求
res = http.request( 'POST', 'http://httpbin.org/post', fields={'hello': 'world'})
```
**响应对象的内容**      
HTTPResponse.status     
HTTPResponse.header     
HTTPResponse.data   

**请求参数**        
headers 设置 header 头      
fields 设置请求数据     
timeout 设置请求超时时间      
retries 设置发起重复请求数量
redirect 设置是否接受重定向     

**扩展的对象**      
urllib3.Timeout(connect=1.0, read=2.0)  
urllib3.Retry(3, redirect=2)

**解码序列化 json响应数据**     
```python
import json
res = http.request('GET', 'htpp://httpbin.org/ip')
data = json.loads(res.data.decode('utf-8))
# {'origin': '127.0.0.1'}
```

**编码请求参数**        
```python
from urllib.parse import urlencode
encoded_args = urlencode({'arg': 'value'})
url = 'http://httpbin.org/post?' + encoded_args
```

**发起 json编码数据的 get 请求**        
```python
import json
data = {'attribute': 'value'}
encoded_data = json.dumps(data).encode('utf-8')
r = http.request(
    'POST',
    'http://httpbin.org/post',
    body=encoded_data,
    headers={'Content-Type': 'application/json'})
json.loads(r.data.decode('utf-8'))['json']
# {'attribute': 'value'}
```

**处理大型响应 Streaming IO**       
```python
import urllib3
http = urllib3.PoolManager()
res = http.request(
    'GET',
    'http://httpbin.org/bytes/1024',
    preload_content=False)
for chunk in res.stream(32):
    print(chunk)
res.release_conn() # 释放连接
```

**设置代理  ProxyManager**      
```python
# http 代理
import urllib3
proxy = urllib3.ProxyManager('http://localhost:3128/')
proxy.request('GET', 'http://google.com/')

# socks5 代理
from urllib3.contrib.socks import SOCKSProxyManager
proxy = SOCKSProxyManager('socks5://localhost:8889/')
proxy.request('GET', 'http://google.com/')
```

使用 SOCKSProxyManager 需要安装 `PySocks` 或者 安装 `urllib3[socks]`

# requests 库


# weasyprint
weasyprint, 好像是做单页的，导出单个网页，没有看到有做书签的功能。  

WeasyPrint 是一个 Python 的虚拟 HTML 和 CSS 渲染引擎，可以用来将网页转成 PDF 文档。旨在支持 Web 标准的打印。但它不是基于特定的渲染引擎，比如Gecko或Webkit。CSS 布局引擎使用 Python 编写，支持分页。   
Furthermore, WeasyPrint supports attachments, bookmarks, and hyperlinks.    
此外，WeasyPrint支持附件、书签和超链接。    

指定 url网址以及css样式，导出pdf
```python
from weasyprint import HTML, CSS
HTML('http://weasyprint.org/').write_pdf('/tmp/weasyprint-website.pdf',
    stylesheets=[CSS(string='body { font-family: serif !important }')])
```

或者直接实例化css对象
```python
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration

font_config = FontConfiguration()
html = HTML(string='<h1>The title</h1>')
css = CSS(string='''
    @font-face {
        font-family: Gentium;
        src: url(http://example.com/fonts/Gentium.otf);
    }
    h1 { font-family: Gentium }''', font_config=font_config)
html.write_pdf(
    '/tmp/example.pdf', stylesheets=[css],
    font_config=font_config)
```

实例化 HTML 对象的几个方法
```python
from weasyprint import HTML
HTML('../foo.html')  # Same as …
HTML(filename='../foo.html')

HTML('http://weasyprint.org')  # Same as …
HTML(url='http://weasyprint.org')

HTML(sys.stdin)  # Same as …
HTML(file_obj=sys.stdin)

# HTML('<h1>foo') would be filename
HTML(string='''
    <h1>The title</h1>
    <p>Content goes here
''')
```

渲染HTML对象返回 document 对象: `HTML-Object.render()`
渲染HTML对象为单文件: `write_pdf()`, `write_png()`  
制作书签：`make_bookmark_tree()`    
添加超链接：`add_hyperlinks()`  


# pdfkit
Python 2 and 3 wrapper for wkhtmltopdf utility to convert HTML to PDF using Webkit. 

