Title: Search Engine Optimization
Date: 2013-08-25 12:14
Tags: dokuwiki, config, seo

针对SEO对dokuwiki进行优化。
## 优化

介绍配置简单且常见的优化方法。
### url rewrite

参考[这里](/tips/build_linux_host#dokuwiki_rewrite配置)的设置。
### 禁用index delay

在配置管理界面，定位到`反垃圾邮件/评论设置`，将indexdelay项修改为0即可禁用index delay。默认会自动在wiki页面上加入以下标签。

	<meta name="robots" content="noindex,nofollow" /> 

### 外部链接

要想对外部链接使用 rel="nofollow" 标签，在配置管理界面，定位到`反垃圾邮件/评论设置`，勾选`relnofollow`即可。
### 对不存在的页面返回404

在配置管理界面，定位到`高级设置`，勾选`send 404`即可。
### Sitemap

在配置管理界面，定位到`聚合设置`，修改`sitemap`的生成天数即可。sitemap地址是'http://your_domin/path_to_dokuwiki/doku.php?do=sitemap'。以本站为例，sitemap的地址为http://wishome.name/kb/doku.php?do=sitemap。可以参考[doku>sitemap](doku>sitemap)文档。
### 关键字

使用dokuwiki的[keywords](doku>plugin/keywords)插件，为wiki页面添加关键字。
### 简介

使用dokuwiki的[description](doku>plugin/description)插件，为wiki页面天剑简要介绍。

## 参考资料

*  How to optimize Dokuwiki for SEO http://docs.oseems.com/general/web/dokuwiki/optimize-for-seo
*  Dokuwiki don't like google http://www.stefanoforenza.com/doku-wiki-dont-like-google/
*  Dokuwiki Sitemap [doku>sitemap](doku>sitemap)
*  Dokuwiki SEO [doku>seo](doku>seo)

