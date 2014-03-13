Title: 考虑撤离Linode
Date: 2014-01-26 10:01
Update: 2014-03-13 09:31
Tags: linode, digitalocean, VPS

[1]: https://code.google.com/p/byte-unixbench/
[2]: http://serverbear.com/

最近我的linode好慢。

买vps主要是为了跑自己的个人博客，当时在网上看到Linode的口碑评价甚好，虽然价格比其他的服务商要高一些，但也没有太过计较，记得当初还专门为此办了一张双币信用卡。

之后因为博客暂停更新，暂停使用Linode一段时间，后来重新开始写博客后，第一时间选的还是Linode。这里不得不说一下Linode的诸多优点：

1. 客服响应及时，态度友好。一般发帖后10分钟之内必有回复，这已是众所周知的事了。
2. 稳定性良好。除了偶尔的系统维护之外，我还没遇到过意外宕机的情况。
3. 有众多的机房可供选择，其中Tokyo机房和Fremont机房，在国内访问通常十分顺畅。
4. 系统管理界面美观易用，用户体验十分友好。
5. 可以无缝迁移和升级，换机房和升级Plan时非常方便。
6. 开放API和移动端app，我没用过，不作评论，也算一个加分点。
7. 10年VPS服务，公司信誉良好。
8. 与时俱进，包括不断最硬件设备和开发软件服务等。

额外说明一下，本文并非是一篇软文，本人也不是Linode的脑残粉，以上的赞美之辞均是实际使用后有感而发。

不过我最近正打算撤离Linode。

前面说过，我买vps主要是为了运行这个用pelican搭建的静态博客。每当我写完一篇文章后，要将markdown文件“编译”（严格的说应该叫“转换”来着）为html文件。而目前pelican这个东东每次在编译的时候都要“从头再来”一次，就是说每次都要编译全部文章，不管你是写了N篇新文章还是只改了某篇旧文章里的一个标点，它都要“从头再来”一次。

在我工作的台式机上（大概是10年左右的顶级配置，现在早已落伍了），编译130篇文章5个页面，这个过程大概要5秒左右（实际过程可能受插件和主题影响），还可以接受的说。而在我的linode 1g上，整个过程要20秒左右，有时竟要50秒。

前几天我专门为此开了个ticket，客服人员也没有发现问题所在，只是帮我把linode换上了最新的硬件（前段时间他们一直在做硬件升级，如果你的linode硬件比较老，可以考虑开个ticket让他们帮你换成最新的。另外，上面的测试都是在换成最新硬件之后进行的）。换了新硬件之后，性能是好了一些，但是pelican的编译过程依然漫长。每次运行`make html`编译文章的时候，总有种“路漫漫其修远兮”的淡淡忧伤。

我觉得原因基本不在我这里，我的linode系统负载常年维持在零点零几，月流量连百分之一都用不完，可以说大部分时间系统都很闲。今天我在linode上用[UnixBench][1]做了下测试，最后得分是513.9（完整报告在[这里](/static/plain/linode-1g-unixbench-report-20140126.txt)，我瞬间就无语凝噎了。网上看到linode 1g的平均得分应该在1300左右，看来有必要再开一个ticket了。

话说天涯何处无芳草，正赶上digital ocean在搞促销，前几天收到一个10刀的促销码，可惜今天恰好过期了（感觉有点背的说）。在网上的性能测试文章（不知道是不是软文）里，digital ocean的表现比linode好不少，另外d家的vps价格比l家几乎要便宜1倍，真心很划算啊。 性价比什么的，我等屌丝最喜欢了。准备抽时间试用一下d家的产品，如果还不错的话，估计就要和linode说88了。

未完待续。

## 2014.01.27 更新
昨天发的linode太慢的ticket，经过一番沟通后，客服回复如下：

> Thanks for getting that for us. Those results do show you are experiencing a small amount of CPU steal but nothing major. Are you seeing any particular performance issues in your actual web application or services? I understand that a benchmark score might be lower than you expected, but that is always going to be a moving target on a virtualized platform where many users are sharing resources.

> That said, we have made some adjustments to the host that hopefully will help you see better performance, however they may take about 48 hours to fully implement. If the major problem is you aren't happy with that benchmark number, would you mind checking again in 48 hours? We can leave this ticket open until then.

大意就是同一台母鸡上的其他linode占用了我linode的一些cpu资源(估计是我的日常cpu使用率太低的原因)，然后他们帮我重新调整了下资源配置，但是完全生效需要48个小时。

今天重新跑了一遍[UnixBench][1]，最后评分提高到了800多，博客的编译时间也降到了10秒左右，基本还能接受。所以暂时先呆在Linode算了，临近年关也没那么多时间折腾。

最后提醒一下购买VPS的同学们，用[UnixBench][1]等工具测试下VPS的系统性能，再将结果和[ServerBear][2]上的平均值比较一下，如果差距太大，最好及时投诉。

## 2014.03.11 更新
最近linode又慢的像蜗牛一样，肯定是资源又被人"抢走了"，花了钱却享受不到应得的服务，实在让人愤怒，这次我是铁了心离开了。

## 2014.03.13 更新
搬家已基本完成，这次使用的是Digitalocean最便宜的一款plan，价格只有linode 1g的四分之一，感觉性能反而更好一些，后记在[此](/life/trying-digitalocean-vps.html)。

## 相关资源列表
*  [UnixBench][1] 系统性能测试工具
*  [ServerBear][2] 一个VPS比较网站，上面有很多VPS的配置信息和性能测试结果，十分有用。

