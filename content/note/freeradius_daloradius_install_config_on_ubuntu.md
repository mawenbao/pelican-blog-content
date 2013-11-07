Title: Ubuntu上安装和配置FreeRadius和DaloRadius
Date: 2013-11-07 17:50
Update: 2013-11-07 21:44
Tags: radius, vpn, ubuntu, tutorial, note

[1]: /note/pptpd.html "blog.atime.me/note/pptpd.html" 
[2]: /note/l2tp_ipsec_installation_on_ubuntu.html "blog.atime.me/note/l2tp_ipsec_installation_on_ubuntu.html"
[3]: #8fa2585857c5677442ed9b23e727fb04 "添加client"
[4]: http://wangyan.org/blog/freeradius-pptp-l2tp-html.html
[5]: http://blog.dayanjia.com/2011/03/configure-freeradius-and-daloradius-on-pptp-vpn-server/
[6]: http://poptop.sourceforge.net/dox/skwok/poptop_ads_howto_a5.htm "http://poptop.sourceforge.net/dox/skwok/poptop_ads_howto_a5.htm"
[7]: https://help.ubuntu.com/community/CategoryNetworking/daloRADIUS "https://help.ubuntu.com/community/CategoryNetworking/daloRADIUS"
[8]: http://sourceforge.net/projects/daloradius/ "http://sourceforge.net/projects/daloradius/"

总结我在Ubuntu上安装FreeRadius和DaloRadius的步骤及遇到的问题，以供日后查询，系统为Ubuntu 12.04.3 X86_64，本文的FreeRadius配置使用MySQL作为后端存储相关数据。

FreeRadius可以为pptp和l2tp提供验证和统计等功能，DaloRadius为FreeRadius提供一个网页界面。阅读本文前确保已经正确安装了pptpd或xl2tpd服务器。相关安装配置教程可参考[使用pptpd搭建VPN][1]和[在Ubuntu12.04上安装l2tp/ipsec VPN服务器][2]。

## 安装必要的软件

    sudo apt-get install freeradius freeradius-mysql radiusclient1 php5 php5-mysql php5-gd php5-cgi php5-fpm php-pear php-db mysql-server-5.5

## 配置FreeRadius 
FreeRadius的配置文件位于`/etc/freeradius`目录。

### 添加client
修改`/etc/freeradius/clients.conf`，添加如下内容，注意将`IP_ADDRESS`和`SHARED_SECRET`换为你的服务器IP和你的共享密钥。

    client IP_ADDRESS {
        ipaddr = IP_ADDRESS
        secret = SHARED_SECRET
        require_message_authenticator = no
    }

### 启用MySQL支持
#### /etc/freeradius/radiusd.conf
取消如下一行的注释来包含FreeRadius的sql配置文件`/etc/freeradius/sql.conf`。

    $INCLUDE sql.conf

#### /etc/freeradius/sql.conf
修改`/etc/freeradius/sql.conf`，设置MySQL数据库的端口，radius数据库的用户名密码等内容。取消如下一行的注释，使FreeRadius从数据库读取客户端信息。

    readclients = yes

`/etc/freeradius/sql/mysql`文件夹下的众多sql脚本文件用于构建FreeRadius的数据库，首先在admin.sql里修改数据库名称，用户名和密码等内容，这些内容必须和`/etc/freeradius/sql.conf`的设置相同。

#### /etc/freeradius/sql/mysql/dialup.conf
修改`/etc/freeradius/sql/mysql/dialup.conf`，取消如下几行的注释来提供在线人数统计功能。

    simul_verify_query  = "SELECT radacctid, acctsessionid, username, \
                           nasipaddress, nasportid, framedipaddress, \
                           callingstationid, framedprotocol \
                           FROM ${acct_table1} \
                           WHERE username = '%{SQL-User-Name}' \
                           AND acctstoptime IS NULL"

#### 创建FreeRadius数据库radius

登录mysql

    cd /etc/freeradius/sql/mysql
    mysql -u root -p

输入以下命令

    create database radius;

    source admin.sql;
    source cui.sql;
    source ippool.sql;
    source nas.sql;
    source schema.sql;
    source wimax.sql;

#### /etc/freeradius/sites-enabled
对`/etc/freeradius/sites-enabled/default`做如下修改

> 找到authorize {}模块，注释掉files，去掉sql前的#号

> 找到accounting {}模块，注释掉radutmp,注释掉去掉sql前面的#号。

> 找到session {}模块，注释掉radutmp，去掉sql前面的#号。

> 找到post-auth {}模块，去掉sql前的#号，去掉sql前的#号（Post-Auth-Type REJECT内）。

对`/etc/freeradius/sites-enabled/inner-tunnel`做如下修改

> 找到authorize {}模块，注释掉files，去掉sql前的#号。

> 找到session {}模块，注释掉radutmp，去掉sql前面的#号。

> 找到post-auth {}模块，去掉sql前的#号，去掉sql前的#号（Post-Auth-Type REJECT内）。

## 配置RadiusClient
RadiusClient用于将pptpd和xl2tpd的radius插件的验证请求发送给FreeRadius服务器，其配置文件位于`/etc/radiusclient`内。

### 添加字典
RadiusClient的字典主要负责请求参数的映射，默认配置没有包含dictionary.microsoft，因此无法处理使用mschapv2加密的请求头。下载dictionary.microsoft并包含到主dictonary文件中。

    cd /etc/radiusclient
    sudo wget http://blog.atime.me/static/resource/dictionary.microsoft

在`/etc/radiusclient/dictionary`文件的最后添加如下一行以包含dictionary.microsoft

    INCLUDE /etc/radiusclient/dictionary.microsoft

### 设置共享密钥
修改'/etc/radiusclient/servers'文件，添加如下一行，注意SHARED_SECRET必须和你在`/etc/freeradius/clients.conf`里设置的[共享密钥][3]相同。

    localhost   SHARED_SECRET

## 配置VPN服务器
为pptpd和xl2tpd启用radius插件，首先查找插件的位置。

    sudo updatedb
    locate radius.so

插件通常位于`/usr/lib/pppd/2.4.5/radius.so`。

### 配置pptpd
查看`/etc/pptpd.conf`，获取pptpd的ppp配置文件位置

    option /etc/ppp/pptpd-options

修改`/etc/ppp/pptpd-options`文件，在最后添加如下两行，注意修改插件的具体位置。

    plugin /usr/lib/pppd/2.4.5/radius.so
    radius-config-file /etc/radiusclient/radiusclient.conf

重启pptpd

    sudo service pptpd restart

### 配置xl2tpd
查看`/etc/xl2tpd/xl2tpd.conf`，获取xl2tpd的ppp配置文件位置

    pppoptfile = /etc/ppp/xl2tpd-options

修改`/etc/ppp/xl2tpd-options`，在最后添加如下两行，注意修改插件的具体位置。

    plugin  /usr/lib/pppd/2.4.5/radius.so
    radius-config-file /etc/radiusclient/radiusclient.conf

重启xl2tpd

    sudo service xl2tpd restart

## 配置DaloRadius
### 下载并配置daloRadius
daloRadius的项目托管在[sourceforge][8]上，下载并解压。

    :::bash
    # 下载并解压
    cd /tmp
    sudo wget http://sourceforge.net/projects/daloradius/files/daloradius/daloradius0.9-9/daloradius-0.9-9.tar.gz
    cd /var/www
    sudo tar -xvf /tmp/daloradius-0.9-9.tar.gz
    sudo mv daloradius-0.0.9 daloradius

    # 修改权限
    sudo chown -R www-data:www-data daloradius
    sudo chmod 644 daloradius/library/daloradius.conf.php

修改`/var/www/daloradius/library/daloradius.conf.php`，设置关于FreeRadius数据库的各个变量，注意和`/etc/freeradius/sql.conf`的配置相同。

    $configValues['FREERADIUS_VERSION'] = '2';
    $configValues['CONFIG_DB_ENGINE'] = 'mysql';
    $configValues['CONFIG_DB_HOST'] = 'localhost';
    $configValues['CONFIG_DB_PORT'] = '3306';
    $configValues['CONFIG_DB_USER'] = 'radius';
    $configValues['CONFIG_DB_PASS'] = 'raduser';

    $configValues['CONFIG_PATH_DALO_VARIABLE_DATA'] = '/var/www/daloradius/var';

### 为daloRadius创建MySQL数据表
由于之前已经为FreeRadius创建了相应的表结构，这里只需要为daloRadius创建表即可

    cd /var/www/daloradius/contrib/db/
    mysql -u root -p radius < mysql-daloradius.sql

由于daloRadius向FreeRadius的数据库`radius`添加了若干新表，我们需要为FreeRadius的数据库用户添加这几张表的访问权限。 FreeRadius的数据库名称和用户可查看`/etc/freeradius/sql.conf`，这里使用默认数据库radius和默认用户radius。

登录MySQL数据库

    mysql -u root -p

输入如下命令

    revoke all privileges on *.* from 'radius'@'localhost';
    grant all privileges on radius.* to 'radius'@'localhost';
    flush privileges;
    exit

### 配置nginx
首先在dns服务商添加一条新的A记录`daloradius`，然后添加新的nginx配置文件`/etc/nginx/sites-available/daloradius.conf`，确定已正确安装并启动了php5-fpm。

注意将server_name中的`your.domain`改为你自己的域名。

    :::nginx
    server {
        listen 80;
        server_name  daloradius.your.domain;
        root /home/wilbur/www/daloradius;

        access_log  /var/log/nginx/daloradius.access.log main;
        error_log   /var/log/nginx/daloradius.error.log warn;

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

        location ~ /\.ht {
            deny all;
        }
    }

链接到`/etc/nginx/sites-enabled/`目录后重启相关服务程序。

    cd /etc/nginx/sites-enabled/
    sudo ln -s ../sites-available/daloradius.conf .

    #sudo service php5-fpm restart
    sudo service nginx restart
    sudo service freeradius restart

dns更改生效后，访问http://daloradius.your.domain即可配置FreeRadius，默认的用户名是administrator，密码是radius。

### daloRadius界面指南
daloRadius的管理账户存储在MySQL的`radius.operators`表中，密码使用明文存储。

    Management => Users 管理VPN用户，注意添加新用户时，应选择Cleartext-Password（默认）密码类型

    Config => Operators 管理daloRadius的登录账户，包括修改密码和权限设置等
    Config => Interface Settings => Enable Password Hiding 设为yes可以将界面上的明文密码改为点号隐藏

## 排查错误
### 使用调试模式启动FreeRadius

    freeradius -X

### 使用radtest
radtest可以向freeradius服务器发送请求，不过目前不支持mschapv2加密模式，详情见`man radtest`。

    radtest user password localhost 0 shared_secret

## 参考资料
1. [PPTP/L2TP + FreeRADIUS + MySQL 安装与配置][4]
2. [在PPTP VPN服务器上配置FreeRADIUS+daloRADIUS实现用户跟踪管理][5]
3. [RadiusClient配置][6]
4. [daloRADIUS Ubuntu help][7]

