Title: 在CentOS上安装和配置Swatch
Date: 2013-08-25 12:14
Tags: centos, install, config, swatch, security


Swatch是一个日志监控工具，以下介绍在CentOS上的安装和配置方法。

## 安装Swatch

在[这里](http://sourceforge.net/projects/swatch/)下载源代码，解压后安装。
    perl Makefile.PL
    make
    make install

如果遇到类似`Can't locate Date/Manip`之类的错误，说明你缺少某些perl模块。通常需要安装以下软件包:

	
	yum install perl-TimeDate perl-Date-Calc perl-DateManip


## Swatch配置文件

可参考[这里](http://www.suretecsystems.com/our_docs/proxy-guide-en/swatch-cfg.html)和man swatch里的说明。
## 运行Swatch

    swatch -c $CONFIG -t $LOG

## 参考资料

*  [Swatch的安装和使用](http://fanqiang.chinaunix.net/a5/b6/20010810/1500001102.html)
*  [Linux Packages Search](http://pkgs.org/)
*  [swatch(1)](http://linux.die.net/man/1/swatch)
*  [Swatch installation and configuration](http://www.suretecsystems.com/our_docs/proxy-guide-en/swatch-intro.html)

