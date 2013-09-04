Title: wordpress problems
Date: 2013-08-25 12:14
Tags: wordpress, problem

# Wordpress3问题和解决方法收集

收集在使用wordpress的过程中遇到的问题及其解决方法。

## 无法在线安装插件或主题

在线安装插件或主题时，显示以下错误信息:
    发生了未知错误。有可能是因为 WordPress.org 工作不正常，或本地配置有误。如果问题持续存在，请浏览中文支持论坛。
应该是dns解析错误，参考[这里](http://www.oukan.net/201207741.html)，解决方法为修改`/etc/resolv.conf`:

    search localdomain
    nameserver 8.8.8.8
    nameserver 8.8.4.4

## 参考资料

*  [wordpress无法在线安装插件](http://www.oukan.net/201207741.html)

