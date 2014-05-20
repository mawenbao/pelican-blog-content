Title: 计划将博客迁回国内
Date: 2014-05-20 11:28
Tags: 备案, VPS

[1]: https://library.linode.com/upgrading/upgrade-to-debian-7-wheezy
[2]: https://www.digitalocean.com/community/articles/how-to-add-swap-on-ubuntu-12-04

基于种种靠谱的不靠谱的考虑，近期计划将博客迁到国内的阿里云主机，目前正在筹备备案的事情。。。

最近一段时间，博客访问可能不太稳定，也可能暂时停止对外访问，抱歉，我承认我在瞎折腾。

## 阿里云服务器配置
依然使用最便宜的服务器，1核心512M内存，每月55RMB。阿里云只提供已经被淘汰的debian6系统，参考linode上的一篇[文章][1]升级到debian7，然后参考digitalocean上的一篇[文章][2]创建交换空间。

创建交换空间的时候发现磁盘写入速度只有40M/s左右，应该是机械硬盘，digitalocean上大概是150M/s，速度差距很大的说。不过网速还可以的说，系统升级不用10分钟就结束了。CPU和digitalocean的差距应该不大，编译博客的时间和原来一样。

