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

把 sqlite3 封装成类，更易于使用
- [Python/16 Databases/sqlite3-class.py](https://github.com/hassanazimi/Python/blob/master/16%20Databases/sqlite3-class.py)
- [Python Sqlite3 wrapper](https://gist.github.com/goldsborough/c973d934f620e16678bf)
- [a small, expressive orm -- supports postgresql, mysql and sqlite](https://github.com/coleifer/peewee)

一些 python orm 封装类 Peewee, Storm, SQLObject, SQLAlchemy


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

