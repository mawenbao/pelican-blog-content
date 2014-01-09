Title: Mysql错误收集
Date: 2013-08-25 12:14
Update: 2014-01-09 12:47
Tags: mysql, database, problem

[1]: http://dev.mysql.com/doc/refman/5.5/en/mysql-tips.html#safe-updates "mysql tips: safe updates"
[2]: http://www.happysysadm.com/2011/01/stopping-mysql-database-server-mysqld.html "Stopping MySQL database server : mysqld failed!"

收集使用Mysql时遇到的错误和解决方法。

## Error 1175 Safe Updtes Mode
错误提示如下:

> ERROR 1175: You are using safe update mode and you tried to update a table without a WHERE that uses a KEY column.

错误的原因是启用了MySQL的Safe Updtes Mode，它的作用是如果执行Update和Delete操作的时候，没有带键限制的where语句或limit语句，sql操作不会执行。详细的介绍可参考[MySQL Tips: safe-updates][1]。

可使用`SET sql_safe_updates=0;`来暂时禁用Safe Updates Mode。

## Stopping MySQL database server: mysqld failed

环境

*  OS: debian6 squeeze
*  Mysql: 5.1.63

使用`service mysql restart`命令时显示`Stopping MySQL database server: mysqld failed!`，导致无法重启mysql服务。

### 解决方法

问题是由mysql数据库的user表中debian-sys-maint用户的密码和/etc/mysql/debian.cnf中的密码不一致所引发的，参考[这篇文章][2]，即可解决。具体步骤如下。

1.  查看/etc/mysql/debian.cnf中的password，`cat /etc/mysql/debian.cnf`，有两个password，不过值是相同的。
2.  连接到mysql，`mysql -uroot -p`
3.  为`debian-sys-maint`用户修改密码。

        GRANT ALL PRIVILEGES ON *.* TO 'debian-sys-maint'@'localhost' IDENTIFIED BY `<password>` WITH GRANT OPTION;

### 问题原因

之前使用[backup脚本](/codes/projects/host_backup)迁移网站时，只迁移了/etc/mysql/debian.cnf，没有迁移mysql里的mysql数据库，导致mysql数据库中user表里的debian-sys-maint的密码和/etc/mysql/debian.cnf不一致。

## 参考资料

1. [MySQL Tips: safe-updates][1]
2. [Stopping MySQL database server : mysqld failed!][2]

