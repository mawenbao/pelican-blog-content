#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import datetime

AUTHOR = u'Ma Wenbao'
SITENAME = u'baozi'
SITEURL = 'http://blog.atime.me'
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

STATIC_PATHS = [
        'static',
        'extra',
]
EXTRA_PATH_METADATA = {
        'extra/CNAME': { 'path': 'CNAME' },
        'extra/.nojekyll': { 'path': '.nojekyll' },
        'extra/README': { 'path': 'README.md' },
        'extra/favicon.ico': { 'path': 'favicon.ico' },
        'extra/CODE_LICENSE.txt': { 'path': 'CODE_LICENSE.txt' },
        'extra/robots.txt': { 'path': 'robots.txt' },
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

TEMPLATE_PAGES = {
        "404.html": "404.html",
        }
JINJA_EXTENSIONS = ['jinja2.ext.ExprStmtExtension',]

# plugin config
PLUGIN_PATH = './plugins'
PLUGINS = [
    #'gzip_cache',
    'update_date',
    'extract_headings',
    'sitemap',
    'summary'
    ]
UPDATEDATE_MODE = 'metadata'

# extrac_headings plugin config
import md5
def my_slugify(value, sep):
    m = md5.new()
    m.update(value)
    return m.digest().encode('hex')
MY_SLUGIFY_FUNC = my_slugify
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
THEME = './themes/niu-x2'
#THEME = '../niu-x2'

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
NIUX2_COMMENTS_TRANSL = '评论'
NIUX2_LASTMOD_TRANSL = '最后修改于:'

NIUX2_DUOSHUO_SHORTNAME = 'atime-me'
NIUX2_PYGMENTS_THEME = 'github'
NIUX2_PAGINATOR_LENGTH = 11
NIUX2_FAVICON_URL = '/favicon.ico'
NIUX2_GOOGLE_CSE_ID = '016368690064160370938:8u3wwjza9c4'
NIUX2_DISPLAY_TITLE = True

#NIUX2_LIB_THEME = '/theme'
#NIUX2_LIB_THEME = 'http://atime-me.qiniudn.com/niu-x2'
#NIUX2_LIB_BOOTSTRAP_JS = 'http://atime-me.qiniudn.com/niu-x2/js/bootstrap.min.js'
#NIUX2_LIB_FONTAWESOME = 'http://atime-me.qiniudn.com/niu-x2/css/font-awesome/css/font-awesome.min.css'
#NIUX2_LIB_JQUERY = 'http://atime-me.qiniudn.com/niu-x2/js/jquery-1.10.2.min.js'

NIUX2_CATEGORY_MAP = {
        'code': ('代码', 'icon-code'),
        'collection': ('搜藏', 'icon-briefcase'),
        'essay': ('随笔', 'icon-leaf'),
        'life': ('日常', 'icon-coffee'),
        'note': ('笔记', 'icon-book'),
        'research': ('研究', 'icon-beaker'),
        }
NIUX2_HEADER_SECTIONS = [
        ('关于', 'about me', '/about.html', 'icon-anchor'),
        ('使用协议', 'agreement', '/agreement.html', 'icon-info-sign'),
        ('项目', 'my projects', '/my_projects.html', 'icon-rocket'),
        ('存档', 'blog archives', '/archives.html', 'icon-archive'),
        ('标签', 'blog tags', '/tag/', 'icon-tag'),
        ]
NIUX2_HEADER_DROPDOWN_SECTIONS = {}
NIUX2_FOOTER_LINKS = [
        ('About', 'about me', '/about.html', ''),
        ('Agreement', 'terms, license and privacy etc.', '/agreement.html', ''),
        ]

NIUX2_FOOTER_ICONS = [
        ('icon-key', 'my public key', '/my_gnupg.html'),
        ('icon-envelope-alt', 'my email address', 'mailto: wilbur.ma@foxmail.com'),
        ('icon-github-alt', 'my github page', 'http://github.com/wilbur-ma'),
        ('icon-rss', 'subscribe my blog via rss2', '/feed.xml'),
        ]

