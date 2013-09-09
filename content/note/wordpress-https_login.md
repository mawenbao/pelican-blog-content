Title: 使用https协议登录并管理wordpress
Date: 2013-08-25 12:14
Tags: wordpress, ssl

介绍使用https协议登录并管理wordpress的配置方法，服务器为nginx1.2.5。
## 修改wp-config.php

添加如下两行:

	define('FORCE_SSL_ADMIN', true);
	define('FORCE_SSL_LOGIN', true);

## 服务器设置

### 生成ssl证书

	
	openssl req -new -x509 -days 365 -nodes -out /etc/ssl/localcerts/blog.atime.me.pem -keyout /etc/ssl/localcerts/blog.atime.me.key

### 添加重写规则

在80端口的server端添加如下代码，所有登录和管理操作将自动跳转到对应的https页面。

	
	location ~ /wp-(admin|login) {
	    rewrite ^ https://$host$request_uri redirect;
	}

添加443端口的server，非登陆和管理页面自动跳转到对应的http页面。代码如下:

	
	server {
	    listen 443 ssl;
	    server_name blog.atime.me;
	    root /home/wilbur/www/wordpress3;
	    index index.php;
	
	    # ssl
	    keepalive_timeout   70;
	    ssl_certificate     /etc/ssl/localcerts/blog.atime.me.pem;
	    ssl_certificate_key /etc/ssl/localcerts/blog.atime.me.key;
	    
	    location ~ /wp-(admin|login) {
	        location ~ \.php$ {
	            fastcgi_pass   127.0.0.1:9000;
	            fastcgi_index  index.php;
	            fastcgi_param  SCRIPT_FILENAME $document_root$fastcgi_script_name;
	            include        fastcgi_params;
	        }
	    }
	
	    location / {
	        rewrite ^ http://$host$request_uri redirect; 
	    }
	}
	

完整的配置文件如下所示(包含w3 total cache的配置):
    server {
        listen 80;
        server_name  blog.atime.me;
        root /home/wilbur/www/wordpress3;
    
        #charset koi8-r;
        access_log  /var/log/nginx/blog.access.log  main;
        error_log   /var/log/nginx/blog.error.log warn;
        
        # blog
        location ~ /wp-(admin|login) {
            rewrite ^ https://$host$request_uri redirect;
        }
    
        location / {
            index index.php;
            try_files $uri $uri/ /index.php;
        }
        
        #error_page  404              /404.html;
    
        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   /usr/share/nginx/html;
        }
    
        # BEGIN W3TC Browser Cache
        gzip on;
        gzip_types text/css application/x-javascript text/x-component text/richtext image/svg+xml text/plain text/xsd text/xsl text/xml image/x-icon;
        location ~ \.(css|js|htc)$ {
            add_header X-Powered-By "W3 Total Cache/0.9.2.4";
        }
        location ~ \.(html|htm|rtf|rtx|svg|svgz|txt|xsd|xsl|xml)$ {
            add_header X-Powered-By "W3 Total Cache/0.9.2.4";
        }
        location ~ \.(asf|asx|wax|wmv|wmx|avi|bmp|class|divx|doc|docx|eot|exe|gif|gz|gzip|ico|jpg|jpeg|jpe|mdb|mid|midi|mov|qt|mp3|m4a|mp4|m4v|mpeg|mpg|mpe|mpp|otf|odb|odc|odf|odg|odp|ods|odt|ogg|pdf|png|pot|pps|ppt|pptx|ra|ram|svg|svgz|swf|tar|tif|tiff|ttf|ttc|wav|wma|wri|xla|xls|xlsx|xlt|xlw|zip)$ {
            add_header X-Powered-By "W3 Total Cache/0.9.2.4";
        }
        # END W3TC Browser Cache
        # BEGIN W3TC Minify core
        rewrite ^/wp-content/w3tc/min/w3tc_rewrite_test$ /wp-content/w3tc/min/index.php?w3tc_rewrite_test=1 last;
        rewrite ^/wp-content/w3tc/min/(.+\.(css|js))$ /wp-content/w3tc/min/index.php?file=$1 last;
        # END W3TC Minify core
        
        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
        #
        location ~ \.php$ {
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
    
        # deny access to .htaccess files, if Apache's document root
        # concurs with nginx's one
        #
        location ~ /\.ht {
            deny all;
        }
    
    }

    server {
        listen 443 ssl;
        server_name blog.atime.me;
        root /home/wilbur/www/wordpress3;
        index index.php;

        # ssl
        keepalive_timeout   70;
        ssl_certificate     /etc/ssl/localcerts/blog.atime.me.pem;
        ssl_certificate_key /etc/ssl/localcerts/blog.atime.me.key;
        
        location ~ /wp-(admin|login) {
            location ~ \.php$ {
                fastcgi_pass   127.0.0.1:9000;
                fastcgi_index  index.php;
                fastcgi_param  SCRIPT_FILENAME $document_root$fastcgi_script_name;
                include        fastcgi_params;
            }
        }

        location / {
            rewrite ^ http://$host$request_uri redirect; 
        }
    }

## 参考资料

*  [How to Make a Self-Signed SSL Certificate](http://library.linode.com/security/ssl-certificates/self-signed)
*  [Nginx Rewrite Rules for WP Admin over SSL](https///www.tinywp.in/nginx-ssl-rewrites/)

