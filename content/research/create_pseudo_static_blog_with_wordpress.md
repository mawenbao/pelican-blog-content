Title: create a pseudo static blog with wordpress
Date: 2012-12-21 18:10:54
Tags: php, golang, wordpress, static_blog

[1]: http://blog.atime.me/2012/12/w3tc-test/ "W3 Total Cache简单测评与配置经验分享"
[2]: http://getpelican.com/ "Pelican"
[3]: http://ruhoh.com/ "Ruhoh"
[4]: http://wordpress.org/extend/plugins/markdown-on-save-improved/ "Markdown on Save Improved plugin"
[5]: http://patrickmylund.com/projects/ocp/ "Optimus Cache Prime(ocp)"
[6]: http://zh.wikipedia.org/wiki/Markdown "Markdown from wikipedia"
[7]: http://wowubuntu.com/markdown/ "Markdown 语法"
[8]: http://wordpress.org/extend/plugins/google-xml-sitemaps-v3-for-qtranslate/ "Google XML Sitemaps v3 for qTranslate plugin"
[9]: https://help.ubuntu.com/community/CronHowto "Cron howto from ubuntu wiki"
[10]: http://wordpress.org/extend/plugins/w3-total-cache/ "W3 totoal cache plugin"
[11]: https://github.com/wilbur-ma/wordpress-tweak/tree/master/google-xml-sitemaps-v3-for-qtranslate
[12]: https://github.com/wilbur-ma/ocp
[13]: http://wordpress.org/extend/plugins/disqus-comment-system/ "disqus社会化评论插件"
[14]: http://wordpress.org/extend/plugins/duoshuo/ "多说社会化评论插件"
[15]: http://wordpress.org/extend/plugins/denglu/ "灯鹭社会化评论插件"

# 使用w3tc，ocp和cron让wordpress成为一个伪静态博客

前一段时间折腾了一会[Pelican][2]和[Ruhoh][3]这些静态博客引擎，不过因为舍不得wordpress的众多优秀主题和插件，最终没有迁移到静态博客引擎上，我果然是一个懒人。使用过静态博客引擎的人肯定对其闪电般的页面加载速度(nginx+静态文件)印象深刻，相较之下wordpress这类动态博客便差强人意。好在wordpress有众多的缓存插件，适当的配置之后页面加载速度会有很大的提高。不过这还不够，我想要的效果是，既有动态博客的便利也要有静态博客的速度。所以，免不了又要折腾一翻。

要让wordpress成为一个“伪静态博客“，至少要实现如下的几个功能:

*  文章和页面必须被缓存，未注册用户访问时直接读取缓存的静态文件即可。这一点使用w3tc插件可以实现。
*  使用[Markdown][6]撰写文章，这一点可以使用[Markdown on Save Improved][4]插件实现。
*  社会化评论，可以使用[Disqus][13], [多说][14]或[灯鹭][15]等社会化评论服务提供的插件实现。

使用w3tc有一个缺点，当写完新的文章后，文章存档、文章分类和标签这些页面将无法及时更新。一个解决的方法是，在w3tc的page cache里，将Garbage collection interval(垃圾回收间隔)设置的小一些会有所帮助。不过垃圾回收后，所有的页面缓存都会失效，然而绝大多数的页面并未改变，所以每次都重新生成所有的页面缓存有点资源浪费。

对此，我的解决方案是使用[Optimus Cache Prime(ocp)][5]爬取网站的sitemap.xml(使用[Google XML Sitemaps v3 for qTranslate插件][8]自动生成)来自动更新文章存档、文章分类和标签的页面缓存(w3tc会自动删除新文章的页面缓存)。要达到这一目的必须对ocp和Google XML Sitemaps的代码做一些修改。

首先，让Google XML Sitemaps v3 for qTranslate插件能够输出分类目录(category)和标签(tag)页的最后修改时间(lastmod)，修改后的插件代码放在[这里][11]。注意在插件的配置页面，开启将分类目录(category)和tag(tag)加入sitemap内容中，并在高级设置里勾选“包含最后修改时间“。

然后，让ocp能够处理sitemap.xml的修改时间(lastmod)，修改后的ocp代码放在[这里][12]，请自行下载并用go编译。

需要说明的是，目前的解决方案存在两点不足:

1. 人为删除文章(post)和页面(page)后，ocp无法删除对应的页面缓存，也无法更新包含删除文章或页面的缓存(比如文章存档，月归档，标签和文章分类页面)等，此时需要手动删除对应的页面缓存。
2. 一些使用插件生成的页面，比如文章存档和网站地图等，每次更新缓存时需要提前删除缓存。

通常情况下(不考虑删除文章)，可以使用如下脚本update-wp-cache.sh来自动更新。

    :::sh
    purgeAllArg='purgeAll'
    localCacheDir=/var/www/wordpress3/wp-content/w3tc/pgcache
    sitemapPath=/var/www/wordpress3/sitemap.xml
    ocpPath=/root/bin/ocp 
    archiveDir=$localCacheDir/archives   # 使用插件的short code生成的archives页面必须手动删除，否则不会更新
    sitemapDir=$localCacheDir/sitemap    # 使用插件生成的sitemap页面必须手动删除，否则不会更新
    
    # remove archive page and sitemap page manually
    if [ $# -ge 1 ] && [ $1 = $purgeAllArg ]
    then 
        echo "Remove all the page cache..."
        rm -Rf $localCacheDir/*
    else
        echo "Remove archive page and sitemap page..."
        rm -Rf $archiveDir $sitemapDir
    fi
    # update cache with ocp
    echo "Update page cache with ocp..."
    $ocpPath -u -rl "_index.html,_index.html_gzip,page" -v -l $localCacheDir -ls _index.html $sitemapPath
    
最后配置crontab，使ocp自动进行爬取，cron job的周期可以根据博客更新的频率设定。在w3tc的page cache配置页面，将Garbage collection interval设置的尽量大一些，至少要大于cron job执行的周期。通常我几天才会写一篇文章，所以用cron每天更新一次页面缓存足够了。

下面是我的crontab设置，每天凌晨3点30分自动运行update-wp-cache.sh脚本，每周末凌晨3点30分清空所有页面缓存并更新。

    30 03 * * * /root/bin/update-wp-cache.sh
    30 03 * * 7 /root/bin/update-wp-cache.sh purgeAll

最后列出一些相关的资源:

*  [Optimus Cache Prime(ocp)][5]
*  [Google XML Sitemaps插件][8]
*  [W3 total cache插件][10]
*  [Markdown中文语法说明][7]
*  [Cron Howto][9]
