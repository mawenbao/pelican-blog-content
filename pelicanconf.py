#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import datetime

AUTHOR = u'Ma Wenbao'
SITENAME = u'MWB日常笔记'
SITEURL = '//blog.atime.me'
#SITEURL = 'http://localhost:8000'

TIMEZONE = 'Asia/Shanghai'
DATE_FORMATS = {
        'zh_CN': '%Y-%m-%d %H:%M:%S',
}
DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DEFAULT_DATE = 'fs'  # use filesystem's mtime
LOCALE = ('zh_CN.utf8',)
DEFAULT_LANG = u'zh_CN'
FILENAME_METADATA = '(?P<slug>.*)'
#DISQUS_SITENAME = 'atime-me'
GOOGLE_ANALYTICS = 'UA-45005256-1'
# feed config
FEED_DOMAIN = SITEURL
FEED_ALL_RSS = 'feed.xml'
FEED_MAX_ITEMS = 20
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
# use directory name as category if not set
USE_FOLDER_AS_CATEGORY = True
DELETE_OUTPUT_DIRECTORY = True
DEFAULT_CATEGORY = 'uncategorized'
DEFAULT_PAGINATION = 7

READERS = {
        'html': None,
}

STATIC_PATHS = [
        'static',
        'extra',
]
EXTRA_PATH_METADATA = {
        'extra/CNAME': { 'path': 'CNAME' },
        'extra/.nojekyll': { 'path': '.nojekyll' },
        'extra/README': { 'path': 'README.md' },
        'extra/favicon.ico': { 'path': 'favicon.ico' },
        'extra/LICENSE.txt': { 'path': 'LICENSE.txt' },
        'extra/robots.txt': { 'path': 'robots.txt' },
        'extra/googlea4ca86ec98912b58.html': {'path': 'googlea4ca86ec98912b58.html' },
        'extra/BingSiteAuth.xml': {'path': 'BingSiteAuth.xml' },
}

ARTICLE_URL = '{category}/{slug}.html'
ARTICLE_SAVE_AS = ARTICLE_URL
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = PAGE_URL
CATEGORY_URL = '{slug}/index.html'
CATEGORY_SAVE_AS = CATEGORY_URL
TAG_URL = 'tag/{slug}.html'
TAG_SAVE_AS = TAG_URL
TAGS_SAVE_AS = 'tag/index.html'
# disable author pages
AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''

TEMPLATE_PAGES = {
        "404.html": "404.html",
        "archives_updatedate.html": "archives_updatedate.html",
        }
JINJA_EXTENSIONS = [
    'jinja2.ext.ExprStmtExtension',
]

# plugin config
PLUGIN_PATH = './plugins'
PLUGINS = [
    #'pandoc_reader',
    #'gzip_cache',
    'update_date',
    'extract_headings',
    'sitemap',
    'summary',
    'niux2_lazyload_helper',
    'niux2_hermit_player',
    'minify',
    ]
UPDATEDATE_MODE = 'metadata'

# extrac_headings plugin config
import md5
def my_slugify(value, sep):
    m = md5.new()
    m.update(value)
    return m.digest().encode('hex')
MY_SLUGIFY_FUNC = my_slugify
MY_HEADING_LIST_STYLE = 'ol'

from markdown.extensions import headerid, codehilite
MD_EXTENSIONS = ([
    'extra',
    'footnotes',
    'tables',
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
THEME = './themes/niu-x2-sidebar'
#THEME = '../niu-x2-sidebar'
NIUX2_DEBUG = False

# niu-x2 theme config
NIUX2_404_TITLE_TRANSL = '404错误 页面未找到!'
NIUX2_404_INFO_TRANSL = '请求页面未找到!'
NIUX2_TAG_TRANSL = '标签'
NIUX2_ARCHIVE_TRANSL = '存档'
NIUX2_ARCHIVE_PUBDATE_TRANSL = '存档 (按发布时间)'
NIUX2_ARCHIVE_UPDATEDATE_TRANSL = '存档 (按修改时间)'
NIUX2_CATEGORY_TRANSL = '分类'
NIUX2_TAG_CLEAR_TRANSL = '清空'
NIUX2_TAG_FILTER_TRANSL = '过滤标签'
NIUX2_HEADER_TOC_TRANSL = '目录'
NIUX2_SEARCH_TRANSL = '搜索'
NIUX2_SEARCH_PLACEHOLDER_TRANSL = '按回车开始搜索 ...'
NIUX2_COMMENTS_TRANSL = '评论'
NIUX2_PUBLISHED_TRANSL = '发布时间'
NIUX2_LASTMOD_TRANSL = '最后修改'
NIUX2_PAGE_TITLE_TRANSL = '页面'
NIUX2_RECENT_UPDATE_TRANSL = '最近修改'
NIUX2_HIDE_SIDEBAR_TRANSL = '隐藏侧边栏'
NIUX2_SHOW_SIDEBAR_TRANSL = '显示侧边栏'
NIUX2_REVISION_HISTORY_TRANSL = '修订历史'
NIUX2_VIEW_SOURCE_TRANSL = '查看源文件'

NIUX2_DUOSHUO_SHORTNAME = 'atime-me'
#DISQUS_SITENAME = 'blog-atime-me'
NIUX2_PYGMENTS_THEME = 'github'
NIUX2_PAGINATOR_LENGTH = 11
NIUX2_RECENT_UPDATE_NUM = 10
NIUX2_FAVICON_URL = '/favicon.ico'
NIUX2_GOOGLE_CSE_ID = '016368690064160370938:8u3wwjza9c4'
NIUX2_DISPLAY_TITLE = True
NIUX2_LAZY_LOAD = True
NIUX2_LAZY_LOAD_TEXT = '努力加载中'
NIUX2_TOOLBAR = True
NIUX2_GITHUB_REPO = 'mawenbao/pelican-blog-content'

#NIUX2_LIB_THEME = 'http://atime-me.qiniudn.com/niu-x2'
#NIUX2_LIB_BOOTSTRAP_JS = 'http://atime-me.qiniudn.com/niu-x2/js/bootstrap.min.js'
#NIUX2_LIB_FONTAWESOME = '//netdna.bootstrapcdn.com/font-awesome/4.0.3'
NIUX2_LIB_JQUERY = '//ajax.aspnetcdn.com/ajax/jQuery/jquery-1.11.0.min.js'

NIUX2_CATEGORY_MAP = {
        'code': ('代码', 'fa-code'),
        'collection': ('搜藏', 'fa-briefcase'),
        'essay': ('随笔', 'fa-leaf'),
        'life': ('日常', 'fa-coffee'),
        'note': ('笔记', 'fa-book'),
        'research': ('研究', 'fa-flask'),
        }
NIUX2_HEADER_SECTIONS = [
        ('关于', 'about me', '/about.html', 'fa-anchor'),
        ('使用协议', 'agreement', '/agreement.html', 'fa-info-circle'),
        ('项目', 'my projects', '/my_projects.html', 'fa-rocket'),
        ]
NIUX2_HEADER_DROPDOWN_SECTIONS = {
        ('社区', 'fa-user'): [
            ('留言板', 'guestbook', 'http://qa.atime.me', 'fa-comment'),
            (' Wiki', 'dokuwiki', 'http://wiki.atime.me', 'fa-puzzle-piece'),
            ],
        }
NIUX2_FOOTER_LINKS = [
        ('关于', 'about me', '/about.html', ''),
        ('协议', 'terms, license and privacy etc.', '/agreement.html', ''),
        ]

NIUX2_FOOTER_ICONS = [
        ('fa-key', 'my public key', '/my_gnupg.html'),
        ('fa-envelope-o', 'my email address', 'mailto: mawenbao@hotmail.com'),
        ('fa-github-alt', 'my github page', 'http://github.com/mawenbao'),
        ('fa-rss', 'subscribe my blog', '/feed.xml'),
        ]

