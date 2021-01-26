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


