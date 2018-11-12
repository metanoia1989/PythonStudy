-- create database python
CREATE DATABASE IF NOT EXISTS `python` DEFAULT CHARSET = utf8mb4 COLLATE utf8mb4_unicode_ci

-- create table study
CREATE TABLE IF NOT EXISTS `study` ( 
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(20) not null ,
    content TEXT,
    add_date VARCHAR(10)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci; 

CREATE TABLE employee ( 
    staff_number INTEGER PRIMARY KEY, 
    fname VARCHAR(20), 
    lname VARCHAR(30), 
    gender CHAR(1), 
    joining DATE,
    birth_date DATE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci; 

CREATE TABLE `tab_staff` (
  `id` int(11) DEFAULT NULL,
  `staffName` varchar(100) CHARACTER SET utf8mb4 DEFAULT NULL,
  `idCardNo` varchar(18) DEFAULT NULL
) CHARACTER SET utf8 collate utf8_general_ci;

SHOW VARIABLES WHERE Variable_name LIKE 'character_set_%' OR Variable_name LIKE 'collation%';

-- create user python
CREATE USER 'python'@'%' IDENTIFIED BY 'python';
GRANT ALL PRIVILEGES ON *.* TO 'python'@'%'
FLUSH PRIVILEGES;