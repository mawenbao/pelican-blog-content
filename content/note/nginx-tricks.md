Title: Nginx小技巧
Date: 2013-08-25 12:14
Update: 2013-12-24 16:49
Tags: nginx, trick

收集使用nginx过程中发现的小技巧。

## 配置技巧

这里记录一些nginx配置方面的技巧。
### 访问txt文件时提示下载

txt文件的MIME类型为text/plain，使用浏览器访问时默认行为是直接在浏览器中显示。如果需要将默认行为改为直接下载，可以在nginx配置文件中添加如下规则即可。

    location ~* \.(txt) {
      add_header Content-Disposition "attachment";
    }

对于某些特殊的文件，如果在访问时需要直接在浏览器上显示文件内容，则可使用如下规则，以gpg的asc加密文件为例。

    location ~* \.(asc) {
      default_type text/plain;
      add_header Content-Disposition "inline";
    }

### nginx负载平衡
配置实例如下

    :::nginx
    upstream wishome_backend {
        server atime.me:9001;
        server atime.me:9002;
    }

    server {
        server_name test.atime.me;

        location / {
            proxy_set_header X-Real-Ip $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_pass http://wishome_backend;
        }
    }

通过上面的配置，访问`test.atime.me`的请求将被平均分配到9001和9002两个端口。

proxy_set_header设置的两个http头X-Real-Ip和X-Forwarded-For用于记录访问者的原始ip地址，其中X-Real-Ip只是一个ip，而X-Forwarded-For是一系列逗号分割的ip列表，第一个是访问者的ip，其后都是转发服务器的ip地址。

## 阅读资料

*  [How can I make sure that Nginx serves plaintext files as a download, instead of inline?](http://serverfault.com/questions/364370/how-can-i-make-sure-that-nginx-serves-plaintext-files-as-a-download-instead-of)

