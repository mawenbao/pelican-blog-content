Title: GO非官方Packages收集
Date: 2013-11-21 15:02
Tags: golang, package, resource

[1]: https://github.com/gorilla "gorilla"
[2]: https://github.com/gorilla/feeds "gorilla/feeds"
[3]: https://github.com/PuerkitoBio
[4]: https://github.com/PuerkitoBio/purell
[5]: https://github.com/PuerkitoBio/gocrawl
[6]: https://code.google.com/p/go/source/browse?repo=net
[7]: https://code.google.com/p/go/source/browse?repo=image
[8]: https://code.google.com/p/go/source/browse?repo=crypto
[9]: https://code.google.com/p/go/source/browse?repo=text

收集一些优秀的非官方GO Pacakges，官方标准库列表见[golang packages][6]。

## 尚在开发中的标准库
GO在google code的仓库里有很多尚未整合入标准库的Packages，多数可能有bug，需谨慎使用。

* [net][6] 包括html parser, ipv4, ipv6和proxy等
* [image][7] 图像处理相关的库
* [cryto][8] 包含众多加密算法的实现
* [text][9] 文本处理相关的库，包括转码等

## 网络相关

* [Gorilla Web Toolkit][1] 包含一些有用的网络开发工具
    * [feeds][2] Feed生成
* 由[PuerkitoBio][3]实现的网络库
    * [purell][4] purify url
    * [gocraw][5] 爬虫

