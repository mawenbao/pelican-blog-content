Title: 搬家至DigitalOcean
Date: 2014-03-13 09:35
Update: 2014-03-20 13:49
Tags: digitalocean, linode, vps

[1]: /life/thinking-about-moving-away-from-linode.html
[2]: /static/plain/digitalocean-512m-unixbench-report-20140313.txt
[3]: /static/plain/linode-1g-unixbench-report-20140126.txt

因为一些[很恶心的原因][1]，这几天将vps搬到了DigitalOcean。事实再次证明，盲信权威和无脑随大流是不可取的，我不会再迷信Linode了。

用的是DigitalOcean最便宜的一款plan，每月只要30元RMB。虽然内存只有512M，但已然够用了，其他资源根本用不完的说。系统用的是Debian 7，奇怪的是没有自动创建交换空间，只好参考[How To Add Swap on Ubuntu 12.04](https://www.digitalocean.com/community/articles/how-to-add-swap-on-ubuntu-12-04)自己创建Swap Space。

已经试用了一天，就目前看来，除了有时候网络延迟偏高之外，其他的一切都还不错。现在编译博客只要5秒左右，四分之一的价格，四分之一的时间[^1]。用UnixBench 5.1.3测了一下，得分1374.6，应该算比较正常，完整报告在[这里][2]。之前我那台Linode 1g的测试结果在[这里][3]，有兴趣的话可以围观一下。

## 2014-03-18 更新
用的是DigitalOcean的旧金山机房，ping一下，rtt基本在350ms左右，偶尔会飙到500ms，甚至1000ms+，这就是便宜的代价了。

用traceroute测了下，发现延迟主要在中国骨干网到美国这一段上，也不知道时间是花在穿越海底光缆上还是花在撞墙上了。

分别ping了下旧金山机房和新加坡机房，结果如下：

旧金山机房

    --- speedtest-sfo1.digitalocean.com ping statistics ---
    132 packets transmitted, 127 received, 3% packet loss, time 745077ms
    rtt min/avg/max/mdev = 193.340/403.047/1632.058/197.717 ms, pipe 2

新加坡机房

    --- speedtest-sgp1.digitalocean.com ping statistics ---
    148 packets transmitted, 127 received, 14% packet loss, time 730138ms
    rtt min/avg/max/mdev = 212.559/261.530/518.302/49.652 ms

从测试结果看，新加坡机房的rtt小一些，但丢包率有点吓人，先迁移过去试几天。

迁到新加坡机房后，感觉网速半斤八两，暂时就这样了。

## 2014-03-20 更新
今天抽空又ping了下sfo1和sgp1两个机房，得到的结果和前天的正好相反，具体结果也懒得贴了。用在线的[tracert服务](http://www.webkaka.com/Tracert.aspx)测了下两个机房，发现从中国访问新加坡机房，不管是走电信还是联通的网络，都得先从美国绕一圈。

正在考虑迁回sfo1机房，X，就不能省点儿心。说起来还是怪自己，功课没做好就下了手，太草率了。


[^1]: 吐槽见[此][1]

