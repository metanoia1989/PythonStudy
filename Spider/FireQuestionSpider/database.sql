
CREATE DATABASE `fire_questions`;
USE `fire_questions`; 
 
--- 章节分类表
CREATE TABLE `tk_chapter` (
    `id` INT(10) AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL COMMENT '章节名称', 
    `level` INT(10) NOT NULL COMMENT '级别 1 科目 2 章节 3 知识点',
    `pid` INT(10) NOT NULL DEFAULT 0 COMMENT '父章节 ID',
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
    `create_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    INDEX `chapter_id`(`chapter_id`)
)
DEFAULT CHARSET = utf8
ENGINE=InnoDB;