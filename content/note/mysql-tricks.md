Title: Mysql小技巧
Date: 2013-08-25 12:14
Tags: mysql, trick

收集关于Mysql的技巧。

##  禁用Innodb引擎 

Mysql5.5之后使用Innodb作为默认引擎，如果嫌其太耗内存，可以使用如下配置禁用Innodb并使用MyISAM作为默认引擎。在my.cnf的mysqld区块内添加如下两行:

    [mysqld]
    ...
    innodb=OFF
    default_storage_engine=MyISAM
    ...

然后重启mysql服务并登陆到mysql后使用如下命令查看引擎状况:

    SHOW VARIABLES LIKE '%storage_engine%';

## 忘记root密码

首先，修改mysql的配置文件/etc/mysql/my.cnf，在[mysqld]区域添加`skip-grant-tables`，之后重启mysql服务`service mysql restart`。

然后不用密码登陆mysql的root用户`mysql -uroot`，依次执行如下命令:

    use mysql; # 切换到mysql数据库
    update user set password=password('NEW_PASSWORD') where user = 'root'; # NEW_PASSWORD是你的新密码
    flush privileges; # 刷新系统权限

最后，修改配置文件/etc/mysql/my.cnf，将[mysqld]里刚刚添加的`skip-grant-tables`删除，重启mysql服务。

