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