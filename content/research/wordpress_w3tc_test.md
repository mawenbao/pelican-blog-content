Title: wordpress plugin w3tc test
Date: 2012-12-11 14:00:29
Tags: test, wordpress, plugin, w3_total_cache

[1]: http://blog.tigertech.net/posts/use-wp-super-cache/
[2]: http://loadimpact.com
[3]: http://loadimpact.com/test/view/1251954
[4]: http://loadimpact.com/test/view/1251946
[7]: http://cd34.com/blog/scalability/wordpress-cache-plugin-benchmarks/
[8]: http://developer.yahoo.com/performance/rules.html

# Wordpress Cache Plugin W3TC Test
使用Wordpress一段时间后，开始关注其性能问题，自然就要用到缓存插件。Wordpress的缓存插件挺多的，我只用过WP Super Cache和W3 Total Cache(以下简称w3tc)，最终选择了w3tc，原因基于两点: 用apache bench简单测试过后发现w3tc略胜一筹; 另一点是w3tc集合了多种cache和minify功能，并且可配置性较高。

需要说明的是，本文重在展示w3tc的效果和分享使用经验，并不是一篇严肃和科学的测评，详细和专业的测评请移步[WordPress Cache Plugin Benchmarks][7]。之前在网上看到很多老外吐槽w3tc，说它配置麻烦且效果极差，甚至有人反映使用w3tc后网站性能比不用缓存插件还要差(-_-!)，如果你对这些吐槽感兴趣，不妨参观下这里的评论: [Use WP Super Cache for WordPress speed, not W3 Total Cache][1]。这说明，缓存插件的效果极可能因使用环境而异，因此找到最适合自己的插件才是最重要的。

先介绍下我的服务器环境:

*  服务器用的是Linode 512 Fremont机房，4核Intel Xeon Cpu，512M内存。
*  w3tc的Page Cache使用Disk:Enhanced模式，Minify、Database Cache和Object Cache均使用Opcode:APC模式。

用apache bench比较w3tc和wp super cache的结果就不再列出了，原因是差别不是特别明显，而且个人感觉可信度也不高。下面展示下用[loadimpact.com][2]测试裸奔(不用缓存插件)和使用w3tc的结果。

裸奔的测试结果可以在[这里][3]查看

w3tc的测试结果可以在[这里][4]查看

测试期间服务器的负载比较正常，并没有很出格的表现。从结果来看，使用w3tc优化后的效果还是很明显的，页面加载时间只有第一次比较长，之后便在1秒上下浮动。而裸奔的情况下，加载时间基本稳定在3秒左右。

w3tc的可配置性是优点也是麻烦，下面简单介绍一下配置w3tc的经验。对于w3tc的各种缓存使用的模式，个人推荐我在用的搭配，即Page Cache使用Disk:enhanced模式，其余的均使用Opcode:APC模式。

1.  对于Page Cache的设置，如果你的网站用户访问不是特别频繁的话，可以考虑将Garbage collection interval即回收间隔设置得稍微大一些。
2.  对于Minify，建议在General Settigns里面开启Mannual(手动)模式，这样的好处是你可以自定义需要minify的css和js，并自定义minify后的js位置。对于可以延迟加载的js代码，推荐放在Non Blocking的Embed before &lt;/body&gt;，这样可以提高页面加载速度。关于网站加载速度优化的更多内容可参考yahoo的神文[Best Practices for Speeding Up Your Web Site][8]。
3.  对于Database Cache和Object Cache，因为没有深入研究过，所以我用的都是默认设置。
4.  对于Browser Cache，记得勾选如下的选项:Set expires header，Set cache control header和Set entity tag (eTag)，这样可以促进浏览器对网页内容进行缓存。另外务必启用Enable HTTP (gzip) compression，使用gzip压缩可以加快页面内容的下载速度。最后记得按照w3tc的提示对你的服务器配置文件进行修改。

本人技术能力有限，再加上研究w3tc也不是很久，因此以上建议仅供参考。如果你决心要折腾一翻，**切记**要提前备份重要的数据。如果你有问题或建议，欢迎提出来一起研究。
