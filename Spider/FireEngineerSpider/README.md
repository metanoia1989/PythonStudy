
# 一级消防安全工程师题目数据抓取
用的是现代前端框架，需要用 Selenium 来渲染js。  

http://wx.anzhuoxfpx.com/member/

需要建两张表，一个分类表，一个题目表    

```php
获取课程列表 http://wx.anzhuoxfpx.com/BeegoEduApi/api/pc/getactivemajorcourse/1973420?keywords=
{
    "courseId": "H035001",
    "courseName": "安全生产法律法规",
    "umcId": 8400134,
},

获取章节列表 http://wx.anzhuoxfpx.com/BeegoEduApi/api/pc/getsimexamlist/8400134/H035001/1
"courseId": "H035001",
"examName": "中级安全工程师-安全生产法律法规2015年历年真题",
"simId": 11957,

获取试卷ID http://wx.anzhuoxfpx.com/BeegoEduApi/api/pc/gensimexamrecid/8400134/11957?courseId=H035001
获取试卷题目 http://wx.anzhuoxfpx.com/BeegoEduApi/api/pc/gensimexamreListBysrId/8400134/3782482/-2
simExamExerciseListPage
a: "犯罪既遂"
b: "犯罪预备"
c: "犯罪未遂"
d: "犯罪中止"
e: ""
f: ""
g: ""
h: ""
analyze: "犯罪的预备、未遂与中止，是故意犯罪行为发展中可能出现的几个不同的形`。"
keyType: "单选"
title: "为了犯罪，准备工具，制造条件的属于（&emsp;）。"
optNum: 4
rightKey: "ABDE"
```