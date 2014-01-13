Title: Python markdown模块
Date: 2013-08-25 12:14
Tags: python, package

介绍python markdown的命令行使用方法。

## 使用方法

直接运行markdown_py即可。

    markdown_py -f a.html a.md

注意设置输出文件，否则即使用`-e utf-8`选项设置utf-8编码也会出现`UnicodeEncodeError: ‘ascii’ codec can’t encode`错误。

## 技巧

当markdown文件里包含中文时，为防止生成的html文件出现乱码，可以为其添加meta标签。

    sed -i '1i\`<meta http-equiv="content-type" content="text/html; charset=UTF-8">` a.md

## 阅读资料

*  [如何在Linux下使用Markdown进行文档工作](http://www.ituring.com.cn/article/10044)
*  [Using Python-Markdown on the Command Line](http://packages.python.org/Markdown/cli.html) from python docs

