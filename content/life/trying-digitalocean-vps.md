Title: 搬家至DigitalOcean
Date: 2014-03-13 09:35
Tags: digitalocean, linode, vps

[1]: /life/thinking-about-moving-away-from-linode.html
[2]: /static/plain/digitalocean-512m-unixbench-report-20140313.txt
[3]: /static/plain/linode-1g-unixbench-report-20140126.txt

因为一些[很恶心的原因][1]，这几天将vps搬到了DigitalOcean。事实再次证明，盲信权威和无脑随大流是不可取的，我不会再迷信Linode了。

用的是DigitalOcean最便宜的一款plan，每月只要30元RMB。虽然内存只有512M，但已然够用了，其他资源根本用不完的说。系统用的是Debian 7，奇怪的是没有自动创建交换空间，只好参考[How To Add Swap on Ubuntu 12.04](https://www.digitalocean.com/community/articles/how-to-add-swap-on-ubuntu-12-04)自己创建Swap Space。

已经试用了一天，就目前看来，除了有时候网络延迟偏高之外，其他的一切都还不错。现在编译博客只要5秒左右，四分之一的价格，四分之一的时间[^1]。用UnixBench 5.1.3测了一下，得分1374.6，应该算比较正常，完整报告在[这里][2]。之前我那台Linode 1g的测试结果在[这里][3]，有兴趣的话可以围观一下。

[^1]: 吐槽见[此][1]

