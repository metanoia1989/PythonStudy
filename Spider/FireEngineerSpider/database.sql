
CREATE DATABASE `fire_engineer`;
USE `fire_engineer`; 
 
--- 章节分类表
CREATE TABLE `fire_chapter` (
    `id` INT(10) AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL COMMENT '章节名称', 
    `level` INT(10) NOT NULL COMMENT '级别 1 科目 2 试卷名',
    `pid` INT(10) NOT NULL DEFAULT 0 COMMENT '父章节 ID',
    `order` INT(10) NOT NULL DEFAULT 0 COMMENT '排序',
    `path` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '冗余字段，章节路径', 
    PRIMARY KEY (`id`),
    INDEX `path`(`path`)
)
DEFAULT CHARSET = utf8
ENGINE=InnoDB;

--- 题目表
CREATE TABLE `fire_questions` (
    `id` INT(10) AUTO_INCREMENT,
    `chapter_id` INT(10) NOT NULL COMMENT '题目所属章节',
    `title` VARCHAR(255) NOT NULL COMMENT '题目标题', 
    `questtype` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '题目类型', 
    `content` TEXT COMMENT '题目内容', 
    `select` TEXT COMMENT '选项', 
    `analyze` TEXT COMMENT '分析', 
    `answer` VARCHAR(20) COMMENT '答案', 
    `order` INT(10) NOT NULL DEFAULT 0 COMMENT '排序',
    `create_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    INDEX `chapter_id`(`chapter_id`)
)
DEFAULT CHARSET = utf8
ENGINE=InnoDB;