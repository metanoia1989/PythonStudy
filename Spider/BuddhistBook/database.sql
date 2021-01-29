
CREATE DATABASE `buddhism_book`;
USE `buddhism_book`; 
 
--- 章节表
CREATE TABLE `book_chapter` (
    `id` INT(10) AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL COMMENT '章节名称', 
    `order` INT(10) NOT NULL DEFAULT 0 COMMENT '排序',
    PRIMARY KEY (`id`)
)
DEFAULT CHARSET = utf8
ENGINE=InnoDB;

--- 文章表
CREATE TABLE `book_article` (
    `id` INT(10) AUTO_INCREMENT,
    `chapter_id` INT(10) NOT NULL COMMENT '题目所属章节',
    `title` VARCHAR(255) NOT NULL COMMENT '题目标题', 
    `order` VARCHAR(10) NOT NULL DEFAULT '' COMMENT '排序',
    `content` TEXT COMMENT '题目内容', 
    PRIMARY KEY (`id`),
    INDEX `chapter_id`(`chapter_id`)
)
DEFAULT CHARSET = utf8
ENGINE=InnoDB;