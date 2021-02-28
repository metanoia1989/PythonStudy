# 新闻聚合爬虫  
龙的天空 http://www.lkong.net/      
看雪论坛 https://bbs.pediy.com/     
吾爱破解论坛 https://www.52pojie.cn/    
v2ex https://v2ex.com/  
水木清华 https://www.newsmth.net/nForum/#!mainpage  
北大未名 https://bbs.pku.edu.cn/v2/home.php     


数据模型设计        
新闻站点表 projects
id 站点ID
name 名 
order 排序

文章分类表  thread
id 分类ID       
project_id 所属项目
name 分类名             
order 排序      
status 状态     
pid 父类ID      

文章表      
id 文章ID       
thread_id 分类ID      
title 标题      
author 作者     
date 日期       
content 内容            
order 排序  


文章评论表  之所以独立，是因为要做增量更新，嵌在文章里面的话不好查了    
id 评论ID   
author 作者     
content 内容    
date 日期       

# 初始化先插入Project
```json
{
    "id" : 1,
    "name" : "龙的天空",
    "url" : "http://www.lkong.net/forum.php"
},
{
    "id" : 2,
    "name" : "看雪论坛",
    "url" : "https://bbs.pediy.com"
},
{
    "id" : 3,
    "name" : "吾爱破解",
    "url" : "https://www.52pojie.cn"    
},
{
    "id" : 4,
    "name" : "v2ex",
    "url" : "https://v2ex.com"
},
{
    "id" : 5,
    "name" : "水木清华",
    "url" : "https://www.newsmth.net/nForum/#!mainpage"
},
{
    "id" : 6,
    "name" : "北大未名",
    "url" : "https://bbs.pku.edu.cn/v2/home.php"
}
```

# 龙的天空 
```python
all_a = response.css(".today+div,.todaynew+div").css("h2 a")
[ (x.attrib['href'], x.css('::text').get()) for x in all_a ]
[('http://www.lkong.net/forum-8-1.html', '原创评论 '),
 ('http://www.lkong.net/forum-60-1.html', '推书试读 '),
 ('http://www.lkong.net/forum-15-1.html', '网文江湖 '),
 ('http://www.lkong.net/forum-10-1.html', '女频小说 '),
 ('http://www.lkong.net/forum-2349-1.html', '业界招聘 '),
 ('http://www.lkong.net/forum-49-1.html', '动漫游戏 '),
 ('http://www.lkong.net/forum-16-1.html', '风花雪月 '),
 ('http://www.lkong.net/forum-48-1.html', '影视评谈 '),
 ('http://www.lkong.net/forum-19-1.html', '体育竞技 '),
 ('http://www.lkong.net/forum-33-1.html', '数码科技 '),
 ('http://www.lkong.net/forum-13-1.html', '财富经济 '),
 ('http://www.lkong.net/forum-20-1.html', '黑市置换 ')]
```