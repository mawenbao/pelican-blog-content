Title: Linux网站搭建手册
Date: 2013-08-08 12:14
Update: 2013-11-04 10:38
Tags: linux_server, tutorial, install

本手册的内容主要包括需要安装的软件及其配置，和常见问题及其解决方案。

*  OS    : debian6 squeeze
*  Php   : php5
*  Wiki  : dokuwiki
*  CMS   : wordpress3
*  Server: nginx 1.2.4
*  DB    : mysql 5.1
*  DB-UI : phpmyadmin
## debian5 lenny

有些vps服务商（比如diahosting）只支持debian5，下面是一些常见的问题和升级到debian6的步骤。
### 软件源问题

如果在使用apt-get update命令的时候出现404错误，可能是因为debian5的软件仓库已被转移到archive.debian.org，而默认的软件源列表依然使用ftp.debian.org。因此正常使用之前需要先修改/etc/apt/sources.list，可参考下面的软件源列表。

    # debian5 lenny

    deb http://archive.debian.org/debian/ lenny main contrib non-free
    deb-src http://archive.debian.org/debian/ lenny main contrib non-free

    deb http://archive.debian.org/debian-security lenny/updates main contrib non-free
    deb-src http://archive.debian.org/debian-security lenny/updates main contrib non-free

    deb http://archive.debian.org/debian-volatile lenny/volatile main contrib non-free
    deb-src http://archive.debian.org/debian-volatile lenny/volatile main contrib non-free

修改sources.list之后需要安装archive.debian.org的key。

	
	apt-get install debian-archive-keyring

最后，运行`apt-get update`更新列表。
### 升级到debian6

debian支持无缝升级，因此从debian5升级到debian6很方便。按照[这里](http://leven.co/blog/view/133)的教程执行相关的步骤即可。
#### 1. 修改本机的hostname

hostname保存于`/etc/hostname`，修改后运行`hostname -F /etc/hostname`设置域名。
#### 2. 更新软件源

将软件源列表修改为debian6的软件源，可参考下面的sources.list文件。

    # debian6 squeeze

    deb http://ftp.debian.org/debian/ squeeze main
    deb-src http://ftp.debian.org/debian/ squeeze main

    deb http://security.debian.org/ squeeze/updates main
    deb-src http://security.debian.org/ squeeze/updates main

    # dotdeb key: http://www.dotdeb.org/dotdeb.gpg

    deb http://packages.dotdeb.org stable all 
    deb-src http://packages.dotdeb.org stable all

    # varnish

    # deb http://repo.varnish-cache.org/debian/ squeeze varnish-3.0

修改sources.list后记得运行`apt-get update`更新软件列表。
#### 3. 开始升级

到这里，升级前的准备工作基本都已完成。如果是通过ssh远程连接到服务器进行升级的话，为了防止网络异常等问题导致升级失败，可以使用screen辅助升级，screen可以保证在ssh断开的情况下继续在服务器上运行升级程序，针对screen的详细介绍可参考[这里](http://www.9usb.net/201002/linux-screen-mingling.html)。
首先使用`apt-get install screen`安装screen程序，然后运行`screen -S debian-upgrade`开启一个名为`debian-upgrade`的screen会话。之后即可运行`apt-get dist-upgrade`升级系统。升级期间ssh如果断开，则重新连接后运行`screen -r debian-upgrade`便可恢复到之前的screen会话。
## debian6 squeeze

### 常用软件
常用软件列表可参考[这里](/tools/debian/software)。
### 邮件设置

#### exim4 安装和配置
安装exim4。
`apt-get install exim4`
参考[这篇文章](http://zww.me/archives/25688)配置exim4。

	
	dpkg-reconfigure exim4-config

第一个页面选择`internet site`，之后的默认即可。
重启exim4

	
	service exim4 restart

修改配置文件以允许发送超过50M的文件。在/etc/exim4/update-exim4.conf.conf的末尾添加如下一行。

	
	MESSAGE_SIZE_LIMIT=1000m

然后运行`update-exim4.conf`更新配置文件即可。
#### mutt安装和使用

安装mutt
`apt-get install mutt`

设置mutt，mutt的默认配置文件在`~/.muttrc`，如果不存在，则从例子里拷贝并修改之，详细的配置说明可参考mutt的相关[文档](http://dev.mutt.org/trac/wiki/MuttGuide)和archlinux wiki的[mutt](https://wiki.archlinux.org/index.php/mutt)。

    :::bash
    cp /usr/share/doc/mutt/examples/sample.muttrc.gz ~
    gzip -d ~/sample.muttrc.gz
    mv ~/sample.muttrc ~/.muttrc

下面的命令将发送一份邮件给a@hotmail.com和a@qq.com，邮件的主题是host backup，邮件内容是host backup on wishome.name，附件是file_a。注意不要漏掉命令中的'--'，在-a选项后添加邮件地址时这是必须的。

	echo 'host backup from wishome.name' | mutt -a 'file_a' -s 'host backup' -- a@hotmail.com a@qq.com

### 常用系统配置

1. 设置常用编辑器。
	
	update-alternatives --config editor

## 安装和配置php

### FastCgi
PHP-FPM (FastCGI Process Manager)是一种常用的fastcgi的实现方式。使用如下命令安装:
`apt-get install php5-fpm`{bash}
日后使用service php5-fpm start/stop/restart进行管理即可。

另外，若不想使用php-fpm，可参考[这里](http://library.linode.com/web-servers/nginx/php-fastcgi/debian-6-squeeze#sph_tcp-sockets-configuration-example)的教程自己编写fastcgi的实现。
## 安装和配置nginx

### 安装nginx
为了安装最新的nginx，在软件源`/etc/apt/sources.list`中添加以下两条记录

	
	deb http://nginx.org/packages/debian/ squeeze nginx
	deb-src http://nginx.org/packages/debian/ squeeze nginx

然后，获取nginx源的key并添加到apt的key列表中，记得更新软件源列表。

	
	wget http://nginx.org/keys/nginx_signing.key -O - | apt-key add -
	apt-get update
	apt-get install nginx

## dokuwiki rewrite配置

已测试nginx版本: 1.2.4, 1.2.5

为了让dokuwiki支持类似`domain.com/wiki/syntax`的简洁url，需要分两步进行设置。
### 1. dokuwiki设置

进入dokuwiki配置界面，并定位到`高级设置`。将userewrite修改为`.htaccess`。
### 2. 服务器rewrite设置

如果经过以下设置后重写依然失败，可以尝试清空浏览器缓存和dokuwiki的缓存`rm -Rf %dokuwiki_home%/data/cache/*`后再重试。
#### 2.1 nginx1.2.4设置

参考[doku>rewrite](doku>rewrite)，为nginx添加重写规则，这里修改的文件是/etc/nginx/conf.d/default.conf。我的dokuwiki主目录位于/var/www/kb，使用`atime.me/wiki/`访问wiki, 相关设置如下所示。

    root /var/www;
    # dokuwiki

    location /kb {
        index doku.php;
        try_files $uri $uri/ @dokuwiki;
    }

    location @dokuwiki {
        rewrite ^/kb/_media/(.*) /kb/lib/exe/fetch.php?media=$1 last;
        rewrite ^/kb/_detail/(.*) /kb/lib/exe/detail.php?media=$1 last;
        rewrite ^/kb/_export/([^/]+)/(.*) /kb/doku.php?do=export_$1&id=$2 last;
        rewrite ^/kb/(.*) /kb/doku.php?id=$1 last;
    }

    location ~ /(data|conf|bin|inc)/ {
        deny all;
    }

设置完成后运行`service nginx restart`重启nginx服务器即可。

该重写规则完全参考了[doku>rewrite](doku>rewrite)中的`For NGINX 0.7.65 or later`版本，只是根据dokuwiki的实际所在位置，在规则前添加/kb目录前缀。如果出现`no input files specialfied`错误，则表明php-fastcgi无法找到文件，尝试修改规则的目录前缀。如果设置无效，请尝试清空浏览器缓存和dokuwiki的缓存后再重试。

倘若使用`wiki.atime.me`访问dokuwiki, 应当使用以下重写规则:

	
	location / {
	    index doku.php;
	    try_files $uri $uri/ @dokuwiki;
	}
	
	location @dokuwiki {
	    rewrite ^/_media/(.*) /lib/exe/fetch.php?media=$1 last;
	    rewrite ^/_detail/(.*) /lib/exe/detail.php?media=$1 last;
	    rewrite ^/_export/([^/]+)/(.*) /doku.php?do=export_$1&id=$2 last;
	    rewrite ^/(.*) /doku.php?id=$1 last;
	}
	
	location ~ /(data|conf|bin|inc)/ {
	    deny all;
	}

#### 2.2 apache2.2.16设置

首先运行`a2enmod rewrite`启用rewrite模块。为了允许使用.htaccess文件，修改`/etc/apache2/sites-enabled/000default`中相关Directory的AllowOverride属性为`AllowOverride All`。如下即可。

    DocumentRoot /var/www
    `<Directory /var/www/>`
        AllowOverride All
        ...

设置好后运行`service apache2 restart`重启apache服务器。
之后进入dokuwiki的主目录，将.htaccess.dist拷贝为.htaccess文件，并去掉以下各行前的注释符`#`。

    RewriteEngine on
    RewriteRule ^_media/(.*)              lib/exe/fetch.php?media=$1  [QSA,L]
    RewriteRule ^_detail/(.*)             lib/exe/detail.php?media=$1  [QSA,L]
    RewriteRule ^_export/([^/]+)/(.*)     doku.php?do=export_$1&id=$2  [QSA,L]
    RewriteRule ^$                        doku.php  [L]
    RewriteCond %{REQUEST_FILENAME}       !-f
    RewriteCond %{REQUEST_FILENAME}       !-d
    RewriteRule (.*)                      doku.php?id=$1  [QSA,L]
    RewriteRule ^index.php$               doku.php

如果以上设置无效，请尝试清空浏览器缓存和dokuwiki的缓存。

## phpmyadmin

### Sohusin问题
当使用apache2服务器并安装了Suhosin模块时，使用phpmyadmin时可能会在页面下方看到类似`链接表的额外特性尚未激活。要查出原因，请点击此处。`或`Server running with Suhosin. Please refer to documentation for possible issues`的错误提示。
参考[这里](http://www.webhostingtalk.com/archive/index.php/t-1144204.html)，我的解决方案分为如下两步。
#### 1. 为phpmyadmin禁用Suhosin

修改php.ini，添加以下项。假设phpmyadmin安装于/usr/share/phpmyadmin。

	
	[PATH=/usr/share/phpmyadmin]
	suhosin.simulation = On

#### 2. 关闭Suhosin警告

修改`/etc/phpmyadmin/config.inc.php`，添加如下项。

	
	$cfg['SuhosinDisableWarning']='true';

## 备份设置

使用python脚本进行备份和恢复，可以通过配置文件自定义备份选项。备份后的数据可以发送到多个邮件地址，在邮件服务器上设置邮件收信规则即可自动管理数据备份。

*  [backup-config.ini](/codes/projects/host_backup#backup-config.ini) 备份和恢复的配置文件
*  host-admin.py 用于备份和恢复
*  aes.py aes加密和解密，取自[slowaes工程](http://code.google.com/p/slowaes/)
## 计划任务cron

[这里](http://www.thegeekstuff.com/2009/06/15-practical-crontab-examples/)有详细的介绍，还有很多例子，推荐阅读。
下面是我的计划任务，使用[这个备份脚本](/codes/projects/host_backup)在每天凌晨备份一下dokuwiki的数据和wordpress的数据库，备份的数据都会被发送到邮箱里。

	
	00 01 * * * /root/bin/host-admin/host-admin.py -c /root/bin/host-admin/daily-backup.ini -b

需要注意的是，如果使用`/etc/cron.*`来放置任务脚本，脚本名(或软链接名)中不能包含点号`.`，否则任务将无法执行且没有任何提示信息，详细信息可参考[Ubuntu CronHowto wiki](https://help.ubuntu.com/community/CronHowto)。

## 参考资料

*  [debian5软件源列表](http://serverfault.com/questions/374651/apt-get-update-getting-404-on-debian-lenny)
*  [debian archive keyring](http://serverfault.com/questions/337278/debian-how-can-i-securely-get-debian-archive-keyring-so-that-i-can-do-an-apt-g)
*  [debian5升级到debian6](http://leven.co/blog/view/133)
*  [apt工具集合介绍](http://www.thegeekstuff.com/2009/10/debian-ubuntu-install-upgrade-remove-packages-using-apt-get-apt-cache-apt-file-dpkg/)
*  [screen介绍](http://www.9usb.net/201002/linux-screen-mingling.html)
*  [debian下配置exim4发送邮件](http://zww.me/archives/25688)
*  [exim4文档](http://www.exim.org/exim-html-4.20/doc/html/)
*  [exim4发送大文件](http://techteam.wordpress.com/2009/05/13/how-to-attach-large-files-to-command-line-email/)
*  [mutt文档](http://dev.mutt.org/trac/wiki/MuttGuide)
*  [archlinux mutt wiki](https://wiki.archlinux.org/index.php/mutt)
*  [Setting Up Mutt on Ubuntu 12.04](http://openswitch.org/blog/setting-up-mutt-on-ubuntu-12-dot-04/)
*  [使用mutt发送邮件](http://www.iamist.com/2011/08/linux-101-using-mutt-to-send-email.html)
*  [dokuwiki rewrite手册](doku>rewrite)
*  [debian6 nginx fastcgi配置](http://library.linode.com/web-servers/nginx/php-fastcgi/debian-6-squeeze)
*  [phpmyadmin suhosin问题](http://www.webhostingtalk.com/archive/index.php/t-1144204.html)
*  [debian6 perl fastcgi](http://library.linode.com/web-servers/nginx/perl-fastcgi/debian-6-squeeze)
*  [crontab例子](http://www.thegeekstuff.com/2009/06/15-practical-crontab-examples/)
*  [Cron Howto](https://help.ubuntu.com/community/CronHowto) from Ubuntu wiki

