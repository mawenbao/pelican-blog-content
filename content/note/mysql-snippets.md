Title: mysql sql snippets
Date: 2013-08-25 12:14
Tags: mysql, snippet

# SQL Snippets

收集一些常用的sql语句。

## 数据定义语言 DDL

### 批量删除表
批量删除有相同前缀的表，使用下面的sql语句会构造相应的drop语句，删除wordpress3数据库中前缀为`wp_`的表。

	SELECT CONCAT( 'DROP TABLE IF EXISTS wordpress3.', TABLE_NAME, ';' )
	FROM information_schema.tables
	WHERE TABLE_SCHEMA = 'wordpress3' AND TABLE_NAME LIKE 'wp_%';

删除步骤如下，首先生成删除命令并保存到drop.sql文件中。

	
	mysql -uroot -ANspe "SELECT CONCAT( 'DROP TABLE IF EXISTS wordpress3.', TABLE_NAME, ';' )
	                       FROM information_schema.tables
	                       WHERE TABLE_SCHEMA = 'wordpress3' AND TABLE_NAME LIKE 'wp_%';" > drop.sql

然后检查drop.sql文件中的语句是否正确，如果无误，最后执行如下命令即可。

执行删除命令前务必提前备份相关的数据
    mysql -uroot -p -e "source drop.sql" 
## 数据管理语言 DML

## 数据控制语言 DCL

