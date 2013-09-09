Title: 使用https协议登录dokuwiki
Date: 2013-08-25 12:14
Tags: dokuwiki, ssl, nginx, config, note

介绍使用https协议登录dokuwiki的配置方法，服务器为nginx1.2.5。
## 生成ssl证书

    openssl req -new -x509 -days 365 -nodes -out /etc/ssl/localcerts/wiki.atime.me.pem -keyout /etc/ssl/localcerts/wiki.atime.me.key
## 禁用securecookie

首先需要禁用dokuwiki的securecookie，修改`$dokuwiki/conf/dokuwiki.conf`文件，将
    `$conf['securecookie'] = 1;`
改为
    `$conf['securecookie'] = 0;`

## nginx重写规则

将dokuwiki的配置分为两个文件:

*  `/etc/nginx/sites-available/dokuwiki.conf` 定义dokuwiki的通用重写规则
*  `/etc/nginx/sites-available/dokuwiki_https.conf` 定义http和https协议的服务器设置

### fastcgi设置

在`/etc/nginx/nginx.conf`文件的http上下文中使用map指令创建一个`php_https`变量:

    :::nginx
    http {
      ...  
      map $scheme $php_https { default off; https on; }
      ...
    }

在`/etc/nginx/fastcgi_params`中加入以下一行:
    fastcgi_param  HTTPS  $php_https;
### http和https重写规则

1. `/etc/nginx/sites-available/dokuwiki.conf`

        :::nginx
        access_log  /var/log/nginx/wiki.access.log  main;
        error_log   /var/log/nginx/wiki.error.log warn;
    
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
    
        #error_page  404              /404.html;
    
        # redirect server error pages to the static page /50x.html
    
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   /usr/share/nginx/html;
        }
    
        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
    
        #
        location ~ \.php$ {
            include        fastcgi_params;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_param  SCRIPT_FILENAME $document_root$fastcgi_script_name;
        }
    
        # deny access to .htaccess files, if Apache's document root
    
        # concurs with nginx's one
        #
    
        location ~ /\.ht {
            deny all;
        }

2. `/etc/nginx/sites-available/dokuwiki_https.conf`
    
        :::nginx
        server {
            server_name wiki.atime.me;
            root /home/wilbur/www/dokuwiki;
            index doku.php;
            listen 80;
            #Enforce https for logins, admin
            if ($args ~* do=(log|admin|profile)) {
                rewrite ^ https://$host$request_uri? redirect;
            }
            include sites-available/dokuwiki.conf;
        }
    
        server {
            server_name wiki.atime.me;
            root /home/wilbur/www/dokuwiki;
            index doku.php;
            listen 443 ssl;
            keepalive_requests    10;
            keepalive_timeout     60 60;
            ssl_certificate     /etc/ssl/localcerts/wiki.atime.me.pem;
            ssl_certificate_key /etc/ssl/localcerts/wiki.atime.me.key;
    
            #switch back to plain http for normal view
            if ($args ~* (do=show|^$)){
                rewrite ^ http://$host$request_uri? redirect;
            }
            include sites-available/dokuwiki.conf;
        }

## 参考资料

*  [doku>tips:httpslogin](doku>tips/httpslogin)
*  [Dokuwiki recipes](http://wiki.nginx.org/Dokuwiki) from nginx wiki
*  [How to Make a Self-Signed SSL Certificate](http://library.linode.com/security/ssl-certificates/self-signed)

