Title: status.net
Date: 2013-08-25 12:14
Tags: cms, status.net

status.net是一个开源微博工具，前身是laconica。

## status.net fancy url 配置

for nginx 1.2.5. status.net安装文件位于/var/www/t（/var/www是网站根目录）。

首先修改nginx配置文件，添加以下内容，保存后重启nginx服务器。

	
	# status.net
	location /t {
	    index index.php;
	    try_files $uri $uri/ @status_net;
	}
	location @status_net {
	    rewrite ^/t/(.+)$ /t/index.php?p=$1 last;
	}

然后，修改status.net的配置文件/var/www/t/config.php，添加以下内容。

	
	$config['site']['fancy'] = true;

现在访问yourdomain.com/t即可使用status.net。

## 参考资料

