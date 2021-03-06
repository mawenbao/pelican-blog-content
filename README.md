[0]: http://blog.atime.me
[1]: https://github.com/mawenbao/niu-x2-sidebar
[2]: https://github.com/mawenbao/extract_headings
[3]: https://github.com/mawenbao/niux2_hermit_player
[4]: https://github.com/mawenbao/niux2_lazyload_helper
[5]: https://github.com/mawenbao/pelican-update-date
[6]: https://github.com/mawenbao/pelican-blog-content/tree/master/plugins/summary
[7]: https://github.com/mawenbao/pelican-blog-content/tree/master/plugins/sitemap

# MWB日常笔记
本仓库用于存放pelican博客demo的源文件和配置等。

## 依赖
### 初始化插件
如果clone的时候没有使用`--recursive`参数，则需要：

    git submodule init
    git submodule update
    
### 系统依赖
* jpegoptim 用于`make optimize`，压缩jpg图片。

    安装(debian/ubuntu):

        sudo apt-get install jpegoptim

* 生成zh_CN.UTF-8 locale
    
        sudo locale-gen zh_CN.UTF-8

### pelican依赖
* [niu-x2-sidebar][1]主题
* [extract_headings][2]插件: 从html文件里提取h1~h6标题并生成目录列表
* [niux2_hermit_player][3]插件: 音频播放器
* [niux2_lazyload_helper][4]插件: 延迟加载图片
* [pelican-update-date][5]插件: 提取文章内的修改时间
* [sitemap][6]插件: 生成sitemap
* [summary][7]插件: 提取第一句话作为摘要

### python依赖
上面的主题或插件的额外依赖

* pelican-minify: 压缩html文件
* beautifulsoup4: 解析html文件
* Pillow: PIL

使用pip安装

    sudo pip install pelican-minify beautifulsoup4 Pillow

