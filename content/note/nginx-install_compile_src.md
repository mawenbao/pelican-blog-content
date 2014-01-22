Title: 从源码安装nginx
Date: 2013-08-25 12:14
Tags: nginx, install, 教程

## 准备工作

安装必须的工具和库。
    apt-get install libpcre3-dev libssl-dev
## 编译参数

我使用如下的configure参数，按照提示安装缺少的库。这里使用的第三方库有nginx-accesskey-2.0.3，如果需要请修改nginx-accsskey的实际路径。

	./configure --prefix=/etc/nginx/ --sbin-path=/usr/sbin/nginx \
	            --conf-path=/etc/nginx/nginx.conf \
	            --error-log-path=/var/log/nginx/error.log \
	            --http-log-path=/var/log/nginx/access.log \
	            --pid-path=/var/run/nginx.pid \
	            --lock-path=/var/run/nginx.lock \ 
	            --http-client-body-temp-path=/var/cache/nginx/client_temp \
	            --http-proxy-temp-path=/var/cache/nginx/proxy_temp \
	            --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp \
	            --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp \
	            --http-scgi-temp-path=/var/cache/nginx/scgi_temp \
	            --user=nginx --group=nginx \
	            --with-http_ssl_module --with-http_realip_module \
	            --with-http_addition_module --with-http_sub_module \
	            --with-http_dav_module --with-http_flv_module \
	            --with-http_mp4_module --with-http_gzip_static_module \
	            --with-http_random_index_module --with-http_secure_link_module \
	            --with-http_stub_status_module --with-mail --with-mail_ssl_module \
	            --with-file-aio --with-ipv6 \
	            --add-module=/root/src/nginx/addons/nginx-accesskey-2.0.3

## 第三方模块

*  accesskey 防盗链
## 安装或运行错误

### client_temp failed
编译安装后，启动nginx时报错:

    nginx: [emerg] mkdir() "/var/cache/nginx/client_temp" failed (2: No such file or directory)

手动创建`/var/cache/nginx`即可。

## 阅读资料

*  [Websites with nginx on Debian 6 (Squeeze)](http://library.linode.com/web-servers/nginx/installation/debian-6-squeeze) from linode documentation
*  [Nginx third party modules](http://wiki.nginx.org/Nginx3rdPartyModules)

