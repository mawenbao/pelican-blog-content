Title: Vanilla论坛安装和配置总结
Date: 2014-02-08 17:35
Tags: vanilla, install, config, 总结

总结在Ubuntu服务器上搭建Vanilla论坛的过程和遇到的问题，以下内容均基于Vanilla 2.2.5。

## 安装
### 下载Vanilla
我用的是Vanilla的最新代码，直接从github上clone即可。

    git clone https://github.com/vanillaforums/Garden

默认检出的是master分支，按照官方的说法，master分支始终包含最新的生产(release)代码。安装后得知，实际版本号是2.2.5。

### 安装必要的软件
php，网页服务器和数据库都是必要的软件，不再赘述。

### 创建数据库表
创建一个名为vanilla的数据库，并为其创建一个名为'vanilla'的用户，密码也是vanilla。该用户仅能从本地访问vanilla数据库。

以mysql为例，执行如下命令。

    mysql -u root -p

    mysql> create database vanilla;
    mysql> grant all privileges on vanilla.* to 'vanilla'@'localhost' identified by 'vanilla';
    mysql> flush privileges;

### 配置网页服务器
配置网页服务器，以nginx配合php5-fpm为例，`/etc/nginx/sites-enabled/vanilla.conf`文件如下：

    :::nginx
    server {
        listen 80;
        server_name talk.atime.me;
        root /var/www/vanilla;

        location / {
            index index.php;
            try_files $uri $uri/ /index.php;
        }

        location ~ \.php$ {
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
    }

然后运行`sudo service nginx reload`来重新加载配置文件。

### 5分钟安装
以上面的nginx配置文件为例，访问`talk.atime.me`（vanilla论坛的域名）即可开始安装，安装过程非常简单。

## 问题
### 总是跳转到最新的回复
用户登录之后，点击帖子的链接总是会跳转到最新的回复(#latest)，我的解决方法是直接修改代码。

将`applications/vanilla/views/discussions/table_functions.php`文件里的相关代码注释掉，如下所示：

    :::php
    /*
    if ($Session->UserID)
        $DiscussionUrl .= '#latest';
    */

## 阅读资料
1. [Vanilla Github Repository](https://github.com/vanillaforums/Garden)
2. [Vanilla Installation](http://vanillaforums.org/docs/installation)

