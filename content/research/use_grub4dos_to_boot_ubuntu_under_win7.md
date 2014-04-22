Title: Win7系统下使用Grub4dos引导Ubuntu
Date: 2013-10-16 15:06:00
Update: 2014-04-22 14:31
Tags: win7, ubuntu, grub4dos, grub2

[1]: https://gna.org/projects/grub4dos "grub4dos project page"
[2]: http://download.gna.org/grub4dos/grub4dos-0.4.4-2009-06-20.zip "grub4dos download"
[3]: http://hi.baidu.com/pspio/item/1ff544a28e45c1218819d33b "Grub4dos引导Grub2"
[4]: http://diddy.boot-land.net/grub4dos/Grub4dos.htm "guide for grub4dos"
[5]: https://wiki.archlinux.org/index.php/GRUB#Backup_important_data

简要介绍在win7上使用grub4dos引导ubuntu的方法。以下假设win7系统的主分区为C盘，并且已经在同一硬盘上安装了ubuntu系统。

## 下载Grub4dos
Grub4dos的项目地址在[这里][1]，不过似乎很久没有更新了，[grub4dos-0.4.4-2009-06-20.zip][2]是我能找到的最新的一个版本。解压下载文件后将grldr.mbr和menu.lst文件放在C盘根目录下。其中，grldr.mbr是grub4dos的引导器，menu.lst是grub4dos引导项的配置文件。

## 修改win7的boot.ini

win7系统里已经不再使用boot.ini来配置启动项，不过`C:\boot.ini`文件里的启动项依然有效。

在boot.ini文件里添加如下内容:

    [boot loader]
    [operating systems]
    c:\grldr.mbr="Grub4dos"

## 查找并添加ubuntu的启动项

在开始之前必须要注意的是，不同的Ubuntu/Kubuntu发行版的core.img文件位置不同，因此以下的引导方法不适用于Ubuntu 14.04版本，Ubuntu/Kubuntu 14.04的引导方法可参考后面的内容。 

    Ubuntu 12.04    /boot/grub/core.img
    Ubuntu 12.10    /boot/grub/i386-pc/core.img
    Ubuntu 14.04    没有core.img文件

重启win7，在启动项里可以看到`Grub4dos`一项，选择后回车进入grub4dos的引导列表，此时按下`c`键切换到grub4dos的命令行界面。

然后，使用find命令查找ubuntu的grub2的位置。

	find /boot/grub/core.img

如果提示`file not found`之类的错误，再尝试执行

	find /grub/core.img

如果依然找不到，则ubuntu的安装可能有问题。记住查找命令的输出，这里假设为(hd0,7)且grub core image位于/grub/core.img。

重启回win7系统，修改C:\menu.list文件，为grub4dos加入如下的引导项。

	title Boot Ubuntu
	root (hd0,7)
	kernel /grub/core.img

日后，只需要使用grub4dos引导项里的`Boot Ubuntu`即可启动Ubuntu。

## Ubuntu/Kubuntu 14.04引导
上面提到过，Ubuntu/Kubuntu 14.04里没有了core.img文件，我尝试过用`grub-mkimage`命令生成core.img，但是grub4dos载入不了。下面介绍一个比较通用的引导方法，之前在逛Ubuntu中文论坛的时候看到的。

安装Ubuntu/Kubuntu 14.04的时候，在手动分区阶段，记得将引导记录安装到某个逻辑分区上，比如`/dev/sda7`。然后等安装完毕后不要急着重启，先将`/dev/sda7`上安装的引导记录备份到Windows的硬盘分区上（其实还额外备份了分区表[^1]），假设Windows的主分区C盘已经mount到了`/mnt/c`，则输入如下命令

    sudo dd if=/dev/sda7 of=/mnt/c/kubuntu.mbr bs=512 count=1

然后重启计算机进入Windows系统，修改`C:\boot.ini`文件，添加kubuntu.mbr的相应配置

    [boot loader]
    [operating systems]
    c:\kubuntu.mbr="Kubuntu 14.04"
    c:\grldr.mbr="Grub4dos"
    
然后重启后选择`Kubuntu 14.04`启动项即可进入Kubuntu 14.04系统。

## 阅读资料

*  [Grub4dos引导Grub2][3]
*  [Grub4dos Guide][4]

[^1]: Arch wiki: GRUB, [Backup important data][5]，引用于2014-04-22。

