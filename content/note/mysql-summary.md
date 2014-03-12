Title: 关于MySQL的各种总结
Date: 2014-02-17 08:55
Update: 2014-03-11 16:50
Tags: mysql, database, 总结, 未完成

[1]: http://dev.mysql.com/doc/refman/5.5/en/mysql-tips.html#safe-updates "MySQL tips: safe updates"
[2]: http://www.happysysadm.com/2011/01/stopping-mysql-database-server-mysqld.html "Stopping MySQL database server : mysqld failed!"
[3]: http://dev.mysql.com/doc/refman/5.5/en/account-management-sql.html "MySQL Account Management SQL"
[4]: http://dev.mysql.com/doc/refman/5.5/en/date-and-time-types.html "MySQL Date and Time Types"
[5]: http://dev.mysql.com/doc/refman/5.5/en/date-and-time-functions.html "MySQL Date and Time Functions"

总结使用MySQL过程中遇到的各种问题和一些有用的资源，配置等等。将之前的若干篇零散的文章汇总到一起，备忘。

若无特别说明，文中的内容均基于Ubuntu 12.04和MySQL5.5。对于本文中出现的代码，`...`表示省略内容，`#`之后为代码注释。

## 配置
### 使用utf8编码
在MySQL的配置文件中做如下设置：

    [client]
    default-character-set = utf8

    [mysqld]
    character-set-server = utf8

然后重启MySQL服务，需要注意的是，已经创建的表不受影响。

### 启用查询日志

    [mysqld]
    ...
    general-log=1
    general-log-file = /var/log/mysql/general.log
    ...

### 禁用Innodb引擎
MySQL5.5之后使用Innodb作为默认引擎，如果嫌其太耗内存，可以使用如下配置禁用Innodb并使用MyISAM作为默认引擎。

在my.cnf的mysqld区块内添加如下两行:

    [mysqld]
    ...
    innodb=OFF
    default_storage_engine=MyISAM
    ...

然后重启mysql服务并登陆到mysql后使用如下命令查看引擎状况:

    mysql> SHOW VARIABLES LIKE '%storage_engine%';

## 技巧
### 忘记root密码
首先，修改mysql的配置文件/etc/mysql/my.cnf，在[mysqld]区域添加`skip-grant-tables`，之后重启mysql服务`service mysql restart`。

然后不用密码登陆mysql的root用户`mysql -uroot`，依次执行如下命令:

    mysql> use mysql;               # 切换到mysql数据库
    mysql> update user set password=password('NEW_PASSWORD') where user = 'root'; # NEW_PASSWORD是你的新密码
    mysql> flush privileges;        # 刷新系统权限

最后，修改配置文件/etc/mysql/my.cnf，将[mysqld]里刚刚添加的`skip-grant-tables`删除，重启mysql服务。

## 思考
### 日期用什么类型存储
在MySQL数据库中，日期可以使用多种类型进行存储，以下是我目前想到的各种类型的优缺点。

* [MySQL Date and Time Types][4]: MySQL内置的日期和时间类型，好处是MySQL有很多内置的[日期和时间函数][5]可供使用，缺点是可移植性很差。
* char或varchar: 暂时没想到什么优点。
* int: 优点是可移植性好，可以做一些基本的比较操作，缺点是和MySQL的内置日期时间类型比，可用函数很少；另外，int类型无法存储时区信息。

## 问题
### Error 1175 Safe Updtes Mode
错误提示如下:

> ERROR 1175: You are using safe update mode and you tried to update a table without a WHERE that uses a KEY column.

错误的原因是启用了MySQL的Safe Updtes Mode，它的作用是如果执行Update和Delete操作的时候，没有带键限制的where语句或limit语句，sql操作不会执行。详细的介绍可参考[MySQL Tips: safe-updates][1]。

可使用`SET sql_safe_updates=0;`来暂时禁用Safe Updates Mode。

### Stopping MySQL database server: mysqld failed

环境

*  OS: debian6 squeeze
*  Mysql: 5.1.63

使用`service mysql restart`命令时显示`Stopping MySQL database server: mysqld failed!`，导致无法重启mysql服务。

解决方法

问题是由mysql数据库的user表中debian-sys-maint用户的密码和/etc/mysql/debian.cnf中的密码不一致所引发的，参考[这篇文章][2]，即可解决。具体步骤如下。

1. 查看/etc/mysql/debian.cnf中的password，`cat /etc/mysql/debian.cnf`，有两个password，不过值是相同的。
2. 连接到mysql，`mysql -uroot -p`
3. 为`debian-sys-maint`用户修改密码。

    GRANT ALL PRIVILEGES ON *.* TO 'debian-sys-maint'@'localhost' IDENTIFIED BY `<password>` WITH GRANT OPTION;

问题原因

之前使用[backup脚本](/code/host_backup.html)迁移网站时，只迁移了/etc/mysql/debian.cnf，没有迁移mysql里的mysql数据库，导致mysql数据库中user表里的debian-sys-maint的密码和/etc/mysql/debian.cnf不一致。

## Snippets
以数据库db和表tb为例。

### 管理相关

显示所有的数据库

    mysql> show databases;

显示当前数据库的所有表

    mysql> show tables;

切换数据库

    mysql> use db

显示表的结构

    mysql> desc tb;

显示数据库的创建信息

    mysql> show create database db;

显示表的创建语句

    mysql> show create table tb;

### 表管理
修改表的字符集

    mysql> ALTER TABLE 'db'.'tb' CHARACTER SET utf8;

修改字段的字符集，参考[Column Character Set Conversion](http://dev.mysql.com/doc/refman/5.1/en/charset-conversion.html)。

### 权限相关
详细内容见[MySQL Account Management SQL][3]。

显示权限
    
    mysql> SHOW GRANTS FOR 'user_name'@'host';

分配权限

    mysql> GRANT ALL PRIVILEGES ON 'database'.'table' TO 'user_name'@'host' IDENTIFIED BY 'password';
    mysql> FLUSH PRIVILEGES;

解除权限

    mysql> REVOKE ALL PRIVILEGES ON 'database'.'table' FROM 'user_name'@'host';
    mysql> FLUSH PRIVILEGES;

### 批量删除表
批量删除有相同前缀的表，使用下面的sql语句会构造相应的drop语句，删除wordpress3数据库中前缀为`wp_`的表。

	SELECT CONCAT( 'DROP TABLE IF EXISTS wordpress3.', TABLE_NAME, ';' )
	FROM information_schema.tables
	WHERE TABLE_SCHEMA = 'wordpress3' AND TABLE_NAME LIKE 'wp_%';

删除步骤如下，首先生成删除命令并保存到drop.sql文件中。

	mysql -uroot -ANspe "SELECT CONCAT( 'DROP TABLE IF EXISTS wordpress3.', TABLE_NAME, ';' )
	                       FROM information_schema.tables
	                       WHERE TABLE_SCHEMA = 'wordpress3' AND TABLE_NAME LIKE 'wp_%';" > drop.sql

然后检查drop.sql文件中的语句是否正确，如果无误，最后执行如下命令即可。（**执行删除命令前务必提前备份相关的数据**）

    mysql -uroot -p -e "source drop.sql" 

## 资源列表
*  [Table Column-Count and Row-Size Limits](http://dev.mysql.com/doc/refman/5.1/en/column-count-limit.html) for MySQL 5.1

## 阅读资料

1. [MySQL Tips: safe-updates][1]
2. [Stopping MySQL database server : mysqld failed!][2]
3. [MySQL Account Management SQL][3]
4. [MySQL Date and Time Types][4]
5. [MySQL Date and Time Functions][5]

