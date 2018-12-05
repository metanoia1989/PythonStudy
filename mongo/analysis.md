# 感受
requests 只是获取源代码的工具，一旦获取过后就无需再请求。
requests 有各种辅助方式来获取源代码，发送、模拟各种请求方式。
http请求是需要耗费时间的，所以把获取的源代码保存下载，可以节省很多时间。
接下来是解析提取源代码，用正则表达式，用lxml解析，用pyquery解析等等。	
持久化可以让程序能够中断后恢复进度，记录爬取的数据，非常的重要。	


# 抓取流程以及首页分析

抓取目的：将html页面转换为pdf，提取内容制作 pdf
只保留主要的内容就够了，提取需要的内容，排除不需要的内容，简单的html就可以转换为 pdf页面，几乎不需要样式。
我想pdf最主要的是将 html的内容渲染成文本，并且去掉那些标签，样式基本需要重写，不过文章页面的样式都是通用的。
写好一个，其他都好了。	

首页目录的结构问题
[{
	title: "section-title-name", // 一级页面
	url: "http://xxxxxx.xxxx/xxxx",
	hash: '',
	child: [{
		title: "section-title-name", // 二级页面
		url: "http://xxxxxx.xxxx/xxxx",	
		hash: '',
	},{
		title: "section-title-name",
		url: "http://xxxxxx.xxxx/xxxx",		
		hash: ''
	}]
}]


解析首页，分析章节目录，组装数据，转换为json或picker持久化。
创建一个url池，将所有的url存入：
用url生成对应的hash值， 创建 url 和 html 的两个hash类型的值


urls {
	url_hash1: url1,
	url_hash2: url2
}

htmls {
	url_hash1: html1,
	url_hash2: html2
}

这样就完成数据的持久化

两个问题：hash 值生成，持久化的方式 picker 
用 json.dump() 生成 json字符串
用 json.loads() 反序列化为python对象
hash值生成 用 hashlib.md5('hello'.encode('utf-8')).hexdigest()

处理页面的节点关系，这方面 正则不适合，提取需要的内容，正则很适合。


