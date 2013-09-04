Title: wordpress weibo live-blogging
Date: 2013-08-25 12:14
Tags: wordpress, plugin

# 为wordpress添加本地微博

使用[Live Blogging插件](http://wordpress.org/extend/plugins/live-blogging/)为wordpress3添加微博功能。
## twitter同步支持

为了启用Live Blogging的twitter同步功能，需要安装php curl库，下面以debian为例介绍安装步骤。
首先安装软件包

	
	apt-get install curl libcurl3 libcurl3-dev php5-curl

重启用到php的程序，包括服务器、php-fastcgi等。

	
	service php-fastcgi stop
	service php-fastcgi start

## 日期格式

参考[php日期函数](http://uk3.php.net/manual/en/function.date.php)，定义为`Y.m.d H:s`，显示样式为`2012.11.13 10:22`
## 参考资料

*  linux下给php安装curl, gd（ubuntu）[http://www.cnblogs.com/macula7/.../1977580.html](http://www.cnblogs.com/macula7/archive/2011/03/08/1977580.html)
*  nginx and cURL http://forum.linode.com/viewtopic.php?t=6542
*  php日期函数 http://uk3.php.net/manual/en/function.date.php

