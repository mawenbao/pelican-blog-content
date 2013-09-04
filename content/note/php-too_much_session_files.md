Title: php solution of too much session files
Date: 2013-08-25 12:14
Tags: php, problem

# Php Session文件过多

php session文件太多的解决办法.

## 设置session存储目录

使用php5-fpm的话, 修改`/etc/php5/fpm/php.ini`, 修改或添加下面一行:

	session.save_path = "path to your session dir"

然后重启fpm服务

	
	service php5-fpm restart

###  清除session的脚本 

    :::bash
    #!/bin/sh 

    # clear php session files

    find /tmp/php-session -cmin +24 -name "sess_*" -and -size 0 -delete > /dev/null 2>&1
    find /tmp/php-session -cmin +1440 -name "sess_*" -delete > /dev/null 2>&1
将以上脚本加入cron计划任务即可自动清除session文件.

## 参考资料

*  http://blog.longwin.com.tw/2008/10/php-too-more-session-file-set-2008/

