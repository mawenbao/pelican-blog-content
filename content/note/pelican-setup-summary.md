Title: Pelican静态博客搭建总结
Date: 2013-09-08 15:04
Update: 2014-02-08 14:58
Tags: pelican, setup, static_blog, 总结

介绍Pelican并总结在搭建Pelican博客过程中需要注意的问题等。

## Pelican介绍
[Pelican][1]是一个用Python语言编写的静态网站生成器，支持使用restructuredText和Markdown写文章，配置灵活，扩展性强。目前Pelican已发布3.2.2版本，有许多优秀的[主题][2]和[插件][3]可供使用。

## 配置文件介绍
以下内容以Pelican3.2.2的配置文件为标准，选择部分难设置的变量进行说明。

### 时区和时间设置
时间的具体显示样式取决于所使用的主题，需要查看对应的jinja2代码，时间的格式见[这里][4]。

    TIMEZONE = 'Asia/Shanghai'
    DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

### 其他有用的设置
使用目录名作为文章的分类名

    USE_FOLDER_AS_CATEGORY = True
    
使用文件名作为文章或页面的slug（url）

    FILENAME_METADATA = '(?P<slug>.*)'

页面的显示路径和保存路径，推荐下面的方式

    ARTICLE_URL = '{category}/{slug}.html'
    ARTICLE_SAVE_AS = ARTICLE_URL
    PAGE_URL = '{slug}.html'
    PAGE_SAVE_AS = PAGE_URL
    CATEGORY_URL = '{slug}/index.html'
    CATEGORY_SAVE_AS = CATEGORY_URL
    TAG_URL = 'tag/{slug}.html'
    TAG_SAVE_AS = TAG_URL
    TAGS_SAVE_AS = 'tag/index.html'
    
## 需要注意的问题

### 编码问题
对于使用python2.x的同学，如果遇到`ascii codec cannot decode ...`之类的问题，建议参照[这里][13]的方法将python的默认编码设置为UTF-8。

## 优秀主题推荐
官方主题仓库见[这里][2]，另外github上还有许多没有加入官方主题仓库的优秀pelican主题，请善用github的搜索功能。

### Elegant
[Elegant][6]是我见过的pelican主题里最优雅漂亮的一个了，功能也超齐全，[这里][7]有一篇作者写的介绍和配置文章。

![Elegant screenshoot][5]

### Niu-X2
接下来是毛遂自荐，Niu-X2是本人业余时间用bootstrap3创作的一个主题，<del>本站目前正在用</del>，功能比较齐全，不算漂亮但很对我自己的口味，代码和配置方法都在[这里][9]。官方主题仓库里的那个niu-x2版本比较老了，如果感兴趣请直接从我的仓库里拉取。

![niu-x2 screenshoot][8]

本博客目前在用的主题是Niu-X2的一个带侧边栏的分支，代码见[niu-x2-sidebar][15]。相对与Niu-X2，目前的主题添加了目录定位和目录自动滚动等功能，同时还完善了脚注(footnote)支持(示例见[这篇文章][16])。需要注意的是，添加侧边栏后，主题的自适应性不如Niu-X2。具体表现是，当可视区域比较窄的时候，侧边栏会被置于页面底部，目前还没有解决办法。 

## 优秀插件推荐
使用插件会延长pelican的编译时间，不过这不是什么问题。这里仅推荐我认为必备的插件，另外官方插件仓库见[这里][3]。

### sitemap
[sitemap][10]可以生成xml和txt格式的网站地图，配置见插件的readme。配置举例：

    SITEMAP = {
        'format': 'xml',
        'priorities': {
            'articles': 0.5,
            'indexes': 0.5,
            'pages': 0.5
            },
        'changefreqs': {
            'articles': 'weekly',
            'indexes': 'daily',
            'pages': 'monthly'
            }
        }

### gzip_cache
[gzip_cache][11]可以将所有的页面压缩为gz格式，有效加快页面的加载速度。

## 我的配置文件
下面贴一下我的配置文件，使用[niu-x2-sidebar][15]主题，sitemap，gzip_cache和[extract_headings][14]插件。（因为某些原因，我屏蔽了google analytics id等敏感数据，请替换所有的`你看不见我` :D）

最新的配置文件请访问[pelican-blog-content/pelicanconf.py][17]。

<script src="https://gist.github.com/mawenbao/8877732.js"></script>

## 阅读资料

*  [Pelican 3.2 官方文档][12]

[1]: https://github.com/getpelican/pelican "pelican"
[2]: https://github.com/getpelican/pelican-themes "pelican官方主题仓库"
[3]: https://github.com/getpelican/pelican-plugins "pelican官方插件仓库"
[4]: http://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior "python strftime 格式"
[5]: /static/images/pelican/pelican-elegant-home-page-screenshot.png "pelian-elegant theme screenshoot"
[6]: https://github.com/talha131/pelican-elegant "pelican-elegant主题"
[7]: http://oncrashreboot.com/pelican-elegant "pelican-elegant介绍和配置说明"
[8]: /static/images/pelican/pelican-niu-x2-screenshot.png "pelican niu-x2 theme screenshoot"
[9]: https://github.com/mawenbao/niu-x2 "niu-x2主题"
[10]: https://github.com/getpelican/pelican-plugins/tree/master/sitemap "pelican sitemap插件"
[11]: https://github.com/getpelican/pelican-plugins/tree/master/gzip_cache "pelican gzip_cache插件"
[12]: http://docs.getpelican.com/en/3.2/ "pelican3.2文档"
[13]: /note/python-notes.html#11d0f24533a5bf4819deb8f98b5375de "python2.x设置默认编码为UTF-8"
[14]: https://github.com/mawenbao/extract_headings "pelican extract_headings插件"
[15]: https://github.com/mawenbao/niu-x2-sidebar "niu-x2带侧边栏的主题"
[16]: http://blog.atime.me/note/golang-summary.html
[17]: https://github.com/mawenbao/pelican-blog-content/blob/master/pelicanconf.py

