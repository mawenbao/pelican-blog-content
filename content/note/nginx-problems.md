Title: Nginx错误收集和解决
Date: 2013-08-25 12:14
Tags: nginx, problem


记录使用nginx时遇见的错误及其解决方法。

## 配置错误

### nginx gzip duplicate MIME type "text/html"
在配置文件中开启gzip，重启nginx时，提示:

    nginx gzip duplicate MIME type "text/html"

gzip配置如下:

    gzip_vary   on;
    gzip_min_length  1000;
    gzip_buffers     4 8k;
    gzip_types       text/plain application/x-javascript text/css text/html application/xml

在新版本的nginx中，开启gzip后会默认压缩text/html，所以不需要手动配置。因此去掉gzip_types中的text/html即可。

## 参考资料

