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
DISQUS_SITENAME = 'atime-me'
GOOGLE_ANALYTICS = 'UA-43647857-1'
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

# extrac_headings plugin configuration
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

THEME = './themes/niu-x2'
PLUGIN_PATH = './plugins'
PLUGINS = ['gzip_cache', 'extract_headings', 'sitemap']

# plugin config
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

# Blogroll
LINKS = ()

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),)

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

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

# niu-x2 theme custom variables
NIUX2_TAG_TRANSL = '标签'
NIUX2_ARCHIVE_TRANSL = '存档'
NIUX2_CATEGORY_TRANSL = '分类'
NIUX2_TAG_CLEAR_TRANSL = '清空'
NIUX2_TAG_FILTER_TRANSL = '过滤标签'
NIUX2_HEADER_TOC_TRANSL = '目录'
NIUX2_SEARCH_TRANSL = '搜索'
NIUX2_SEARCH_PLACEHOLDER_TRANSL = '按回车开始搜索 ...'

NIUX2_PYGMENTS_THEME = 'github'
NIUX2_PAGINATOR_LENGTH = 11
NIUX2_FAVICON_URL = '/favicon.ico'
NIUX2_GOOGLE_CSE_ID = '010036094435699263509:otu5mqpvchs'
NIUX2_DISPLAY_TITLE = False

NIUX2_CATEGORY_MAP = {
        'code': ('代码', 'icon-code'),
        'life': ('日常', 'icon-coffee'),
        'research': ('研究', 'icon-beaker'),
        'thought': ('思考', 'icon-question-sign'),
        'note': ('笔记', 'icon-book'),
        }
NIUX2_HEADER_SECTIONS = [
        ('关于', 'about', '/about.html', 'icon-anchor'),
        ('使用协议', 'agreement', '/agreement.html', 'icon-info-sign'),
        ('我的公钥', 'my gnupg', '/my-gnupg.html', 'icon-key'),
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

