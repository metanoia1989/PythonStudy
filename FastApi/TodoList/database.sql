--- 创建 users 表
DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT(11)  NOT NULL AUTO_INCREMENT, 
    `lname` VARCHAR(255) COMMENT 'last name',
    `fname` VARCHAR(255) COMMENT 'first name',
    `email` VARCHAR(255) NOT NULL COMMENT '邮箱',
    PRIMARY KEY (`id`),
    UNIQUE INDEX `email` (`email`)
)
ENGINE=InnoDB
COLLATE=utf8mb4_unicode_ci
COMMENT='用户表';

--- 创建 todo 表
DROP TABLE IF EXISTS `todos`;
CREATE TABLE IF NOT EXISTS `todos` (
    `id` INT(11)  NOT NULL AUTO_INCREMENT, 
    `text` VARCHAR(255) COMMENT '内容',
    `complated` TINYINT(1) UNSIGNED DEFAULT 0 COMMENT '是否完成',
    `owner_id` INT(11) NOT NULL COMMENT '创建者',
    PRIMARY KEY (`id`),
    CONSTRAINT FK_UserTodo FOREIGN KEY (`owner_id`) REFERENCES `users`(`id`)
)
ENGINE=InnoDB
COLLATE=utf8mb4_unicode_ci
COMMENT='待办事项表';