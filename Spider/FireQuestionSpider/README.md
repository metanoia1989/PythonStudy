# 中教安达题库抓取
题库地址：https://m10.bjzjxf.com/   

科目-章节-知识点，然后知识点对应着详细的题目，我就不搞那么麻烦了，直接用无限级分类好了。    


导入数据库文件 `database.sql`，然后复制 `.env.example` 为 `.env` 文件。 


# 科目章节分析

所有科目入口 https://m10.bjzjxf.com/Home/Index/index        
章节 新版基础知识 https://m10.bjzjxf.com/Index/one/1824      
知识点 https://m10.bjzjxf.com/Home/Index/one/id/2750

截断数据表：
```sql
TRUNCATE TABLE tk_chapter;
```