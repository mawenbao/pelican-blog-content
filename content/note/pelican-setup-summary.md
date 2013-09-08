Title: pelican setup summary
Date: 2013-09-08 15:04
Tags: pelican, setup, summary, static_blog

# Pelican静态博客搭建总结
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
![Elegant screenshoot][5]

[Elegant][6]是我见过的pelican主题里最优雅漂亮的一个了，功能也超齐全，[这里][7]有一篇作者写的介绍和配置文章。

### Niu-X2
![Niu-X2 screenshoot][8]

接下来是毛遂自荐，Niu-X2是本人业余时间用bootstrap3创作的一个主题，本站目前正在用，功能比较齐全，不算漂亮但很对我自己的口味，代码和配置方法都在[这里][9]。官方主题仓库里的那个niu-x2版本比较老了，如果感兴趣请直接从我的仓库里拉取。

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
下面贴一下我的配置文件，使用[Niu-X2][9]主题，sitemap，gzip_cache和[extract_headings][14]插件。（因为某些原因，我屏蔽了google analytics id等敏感数据，请替换所有的`你看不见我` :D）

    :::python
    #!/usr/bin/env python
    # -*- coding: utf-8 -*- #
    from __future__ import unicode_literals
    import datetime

    AUTHOR = u'Ma Wenbao'
    SITENAME = u'baozi-x'
    SITEURL = 'http://atime.me'

    TIMEZONE = 'Asia/Shanghai'
    DATE_FORMATS = {
            'zh_CN': '%Y-%m-%d %H:%M:%S',
    }
    DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    DEFAULT_DATE = 'fs'  # use filesystem's mtime
    LOCALE = ('zh_CN.utf8',)
    DEFAULT_LANG = u'zh_CN'
    DEFAULT_PAGINATION = 10
    FILENAME_METADATA = '(?P<slug>.*)'
    GOOGLE_ANALYTICS = '你看不见我'
    # feed config
    FEED_DOMAIN = SITEURL
    FEED_ALL_RSS = 'feed.xml'
    FEED_MAX_ITEMS = 100
    FEED_ALL_ATOM = None
    CATEGORY_FEED_ATOM = None
    TRANSLATION_FEED_ATOM = None
    # use directory name as category if not set
    USE_FOLDER_AS_CATEGORY = True
    DELETE_OUTPUT_DIRECTORY = True
    DEFAULT_CATEGORY = 'uncategorized'

    FILES_TO_COPY = (
            ('extra/CNAME', 'CNAME'),
            ('extra/.nojekyll', '.nojekyll'),
            ('extra/README', 'README.md'),
            ('extra/favicon.ico', 'favicon.ico'),
            ('extra/CODE_LICENSE.txt', 'CODE_LICENSE.txt'),
            ('extra/robots.txt', 'robots.txt'),
    )

    ARTICLE_URL = '{category}/{slug}.html'
    ARTICLE_SAVE_AS = ARTICLE_URL
    PAGE_URL = '{slug}.html'
    PAGE_SAVE_AS = PAGE_URL
    CATEGORY_URL = '{slug}/index.html'
    CATEGORY_SAVE_AS = CATEGORY_URL
    TAG_URL = 'tag/{slug}.html'
    TAG_SAVE_AS = TAG_URL
    TAGS_SAVE_AS = 'tag/index.html'

    TEMPLATE_PAGES = {
            "404.html": "404.html",
            }
    STATIC_PATHS = ['images',]

    # plugin config
    PLUGIN_PATH = './plugins'
    PLUGINS = ['gzip_cache', 'extract_headings', 'sitemap']

    # extrac_headings plugin config
    import md5
    def my_slugify(value, sep):
        m = md5.new()
        m.update(value)
        return m.digest().encode('hex')
    MY_SLUGIFY_FUNC = my_slugify
    MY_TOC_CLASS = 'dropdown-menu'
    from markdown.extensions import headerid, codehilite
    MD_EXTENSIONS = ([
        'extra',
        codehilite.CodeHiliteExtension(configs=[('linenums', False), ('guess_lang', False)]),
        headerid.HeaderIdExtension(configs=[('slugify', my_slugify)]),
        ])

    # sitemap plugin config
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

    # theme config
    THEME = './themes/niu-x2'

    # niu-x2 theme config
    NIUX2_404_TITLE_TRANSL = '404错误 页面未找到!'
    NIUX2_404_INFO_TRANSL = '请求页面未找到!'
    NIUX2_TAG_TRANSL = '标签'
    NIUX2_ARCHIVE_TRANSL = '存档'
    NIUX2_CATEGORY_TRANSL = '分类'
    NIUX2_TAG_CLEAR_TRANSL = '清空'
    NIUX2_TAG_FILTER_TRANSL = '过滤标签'
    NIUX2_HEADER_TOC_TRANSL = '目录'
    NIUX2_SEARCH_TRANSL = '搜索'
    NIUX2_SEARCH_PLACEHOLDER_TRANSL = '按回车开始搜索 ...'

    NIUX2_DUOSHUO_SHORTNAME = '你看不见我'
    NIUX2_PYGMENTS_THEME = 'github'
    NIUX2_PAGINATOR_LENGTH = 11
    NIUX2_FAVICON_URL = '/favicon.ico'
    NIUX2_GOOGLE_CSE_ID = '你看不见我'
    NIUX2_DISPLAY_TITLE = False

    NIUX2_CATEGORY_MAP = {
            'research': ('研究', 'icon-beaker'),
            'code': ('代码', 'icon-code'),
            'thought': ('思考', 'icon-question-sign'),
            'note': ('笔记', 'icon-book'),
            'life': ('日常', 'icon-coffee'),
            'collection': ('搜藏', 'icon-briefcase'),
            }
    NIUX2_HEADER_SECTIONS = [
            ('关于', 'about', '/about.html', 'icon-anchor'),
            ('使用协议', 'agreement', '/agreement.html', 'icon-info-sign'),
            ('我的公钥', 'my gnupg', '/my_gnupg.html', 'icon-key'),
            ('存档', 'archives', '/archives.html', 'icon-archive'),
            ('标签', 'tags', '/tag/', 'icon-tag'),
            ]
    NIUX2_HEADER_DROPDOWN_SECTIONS = {}
    NIUX2_FOOTER_LINKS = [
            ('About', 'about me', '/about.html', ''),
            ('Agreement', 'terms, license and privacy etc.', '/agreement.html', ''),
            ]

    NIUX2_FOOTER_ICONS = [
            ('icon-envelope-alt', 'my email address', 'mailto: wilbur.ma@foxmail.com'),
            ('icon-weibo', 'my sina weibo page', 'http://weibo.com/baozi2x'),
            ('icon-github-alt', 'my github page', 'http://github.com/wilbur-ma'),
            ('icon-rss', 'subscribe my blog via rss2', 'http://atime.me/feed.xml'),
            ]

## 参考资料

*  [Pelican 3.2 官方文档][12]

[1]: https://github.com/getpelican/pelican "pelican"
[2]: https://github.com/getpelican/pelican-themes "pelican官方主题仓库"
[3]: https://github.com/getpelican/pelican-plugins "pelican官方插件仓库"
[4]: http://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior "python strftime 格式"
[5]: /static/images/pelican/pelican-elegant-home-page-screenshot.png "pelian-elegant theme screenshoot"
[6]: https://github.com/talha131/pelican-elegant "pelican-elegant主题"
[7]: http://oncrashreboot.com/pelican-elegant "pelican-elegant介绍和配置说明"
[8]: /static/images/pelican/pelican-niu-x2-screenshot.png "pelican niu-x2 theme screenshoot"
[9]: https://github.com/wilbur-ma/niu-x2 "niu-x2主题"
[10]: https://github.com/getpelican/pelican-plugins/tree/master/sitemap "pelican sitemap插件"
[11]: https://github.com/getpelican/pelican-plugins/tree/master/gzip_cache "pelican gzip_cache插件"
[12]: http://docs.getpelican.com/en/3.2/ "pelican3.2文档"
[13]: /note/python-notes.html#11d0f24533a5bf4819deb8f98b5375de "python2.x设置默认编码为UTF-8"
[14]: https://github.com/wilbur-ma/extract_headings "pelican extract_headings插件"
