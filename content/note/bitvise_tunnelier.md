Title: Bitvise Tunnelier
Date: 2013-08-25 12:14
Tags: proxy


有关Bitvise Tunnelier的东东。

## Unrecognized Proxy Protocol解决方案

使用ssh翻墙时，用Bitvise Tunnelier做代理，在chrome上用SwichySharp插件管理代理设置，访问使用https协议的网页一切正常，访问http的网页会返回"无数据"之类的错误。

查看Bitvise Tunnelier的日志显示unrecognized proxy protocol错误。Google了一番后，在[这里](http://0618.us/bitvise-tunnelier-under-http-proxy-with-socks-proxy-settings-tutorial/)找到了解决方案。Bitvise Tunnelier提供的是socks代理，不直接支持http。所以，在SwichySharp的配置界面，将http代理的ip和端口清空，只设置https代理、ftp代理和socks代理即可，如下图所示。

{{http://static.atime.me/images/dokuwiki/tools/bitvise-tunnelier/ssh_proxy_error-swichysharp.jpg?nolink}}

另外，参考[这里](http://www.appinn.com/bitvise-tunnelier/)vising的评论，这个问题还可以通过CCProxy或者是Proxy Forward将socks代理转发成http代理，不过未经测试。
## 参考资料

*  [Bitvise Tunnelier下，http代理與socks代理設置教程](http://0618.us/bitvise-tunnelier-under-http-proxy-with-socks-proxy-settings-tutorial/)

