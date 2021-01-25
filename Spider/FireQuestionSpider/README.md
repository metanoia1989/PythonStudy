# 中教安达题库抓取
题库地址：https://m10.bjzjxf.com/   

科目-章节-知识点，然后知识点对应着详细的题目，我就不搞那么麻烦了，直接用无限级分类好了。    

```sql
CREATE DATABASE `fire_questions`;
USE `fire_questions`; 
 
--- 章节分类表
CREATE TABLE `tk_chapter` (
    `id` INT(10) AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL COMMENT '章节名称', 
    `level` INT(10) NOT NULL COMMENT '级别 1 科目 2 章节 3 知识点',
    `pid` INT(10) NOT NULL DEFAULT 0 COMMENT '父章节 ID',
    `order` INT(10) NOT NULL DEFAULT 0 COMMENT '排序',
    `path` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '冗余字段，包含所有父级ID组成的字符串', 
    PRIMARY KEY (`id`),
    INDEX `path`(`path`)
)
DEFAULT CHARSET = utf8
ENGINE=InnoDB;

--- 题目表
CREATE TABLE `tk_questions` (
    `id` INT(10) AUTO_INCREMENT,
    `chapter_id` INT(10) NOT NULL COMMENT '题目所属章节',
    `title` VARCHAR(255) NOT NULL COMMENT '题目标题', 
    `content` TEXT COMMENT '题目内容', 
    `select` TEXT COMMENT '选项', 
    `answer` TEXT COMMENT '答案', 
    `order` INT(10) NOT NULL DEFAULT 0 COMMENT '排序',
    `create_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    INDEX `chapter_id`(`chapter_id`)
)
DEFAULT CHARSET = utf8
ENGINE=InnoDB;
```


初始入口地址 https://m10.bjzjxf.com/Home/Index/index