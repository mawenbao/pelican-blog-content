Title: Win7系统下使用Grub4dos引导Ubuntu
Date: 2013-10-16 15:06:00
Tags: win7, ubuntu, grub4dos, grub2

[1]: https://gna.org/projects/grub4dos "grub4dos project page"
[2]: http://download.gna.org/grub4dos/grub4dos-0.4.4-2009-06-20.zip "grub4dos download"
[3]: http://hi.baidu.com/pspio/item/1ff544a28e45c1218819d33b "Grub4dos引导Grub2"
[4]: http://diddy.boot-land.net/grub4dos/Grub4dos.htm "guide for grub4dos"


简要介绍在win7上使用grub4dos引导ubuntu的方法。以下假设win7系统的主分区为C盘，并且已经在同一硬盘上安装了ubuntu系统。

## 下载Grub4dos
Grub4dos的项目地址在[这里][1]，不过似乎很久没有更新了，[grub4dos-0.4.4-2009-06-20.zip][2]是我能找到的最新的一个版本。解压下载文件后将grldr.mbr和menu.lst文件放在C盘根目录下。其中，grldr.mbr是grub4dos的引导器，menu.lst是grub4dos引导项的配置文件。

## 修改win7的boot.ini

win7系统里已经不再使用boot.ini来配置启动项，不过C盘根目录下的boot.ini文件里的启动项依然有效。

在boot.ini文件里添加如下内容:
<pre>
[boot loader]
[operating systems]
c:\grldr.mbr="Grub4dos"
</pre>

## 查找并添加ubuntu的启动项

接下来重启win7，在启动项里可以看到`Grub4dos`一项，选择后回车进入grub4dos的引导列表，此时按下`c`键切换到grub4dos的命令行界面。

然后，使用find命令查找ubuntu的grub2的位置。

	find /boot/grub/core.img

如果提示`file not found`之类的错误，再尝试执行

	find /grub/core.img

如果依然找不到，则ubuntu的安装可能有问题。记住查找命令的输出，这里假设为(hd0,7)且grub core img位于/grub/core.img。

重启回win7系统，修改C:\menu.list文件，为grub4dos加入如下的引导项。

	title Boot Ubuntu
	root (hd0,7)
	kernel /grub/core.img

日后，只需要使用grub4dos引导项里的`Boot Ubuntu`即可启动Ubuntu。

## 参考资料

*  [Grub4dos引导Grub2][3]
*  [Grub4dos Guide][4]

