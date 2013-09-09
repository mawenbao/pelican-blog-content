Title: 使用Grub Rescue恢复Ubuntu引导
Date: 2013-08-25 12:14
Tags: ubuntu, grub, boot_loader


装了Ubuntu和Window双系统的电脑，通常会使用Ubuntu的Grub2进行引导。Grub2会在MBR写入引导记录，并将引导文件放在/boot/grub，破坏任意一项都会导致系统无法正常启动。当系统因引导失败而无法正常启动时，可以使用Windows的安装光盘或Grub Rescue恢复引导。

## 1. 使用Win7安装盘修复MBR

使用Win7安装盘启动后，用以下命令恢复MBR。BootRec命令详细介绍可参考[这里](/tools/windows/BootRec)。

	
	BootRec.exe /fixmbr

## 2. 使用Grub Rescue修复MBR

如果想继续使用Ubuntu，可以使用Grub Rescue进行引导恢复。Rescue模式下可使用的命令有：set，ls，insmod，root和prefix，详细介绍可参考[这里](/tools/linux/GrubRescue)。
### a) MBR被破坏

如果是MBR的引导记录被破坏，可按如下操作进行恢复。

1. 使用ls命令查看当前的分区情况。假设输出如下:

	
	(hd0, 1) (hd0, 2) (hd0, 3) (hd0, 4) (hd0, 5)

2. 使用ls命令查找引导文件/boot/grub的位置。

假设/boot被单独挂载于(hd0, 5)分区，则使用如下命令确认。

	
	ls (hd0, 5)/grub

否则使用如下命令。

	
	ls (hd0, 5)/boot/grub

使用上述命令后，如果在输出的文件列表中看到grub.cfg即可，否则继续在其他分区尝试以上命令。

3. 找到/boot/grub后，执行以下命令即可找回丢失的Grub2引导菜单，如果/boot单独挂载于(hd0, 5)分区，则执行如下命令:

	
	set root=(hd0, 5)
	set prefix=(hd0, 5)/grub
	insmod normal
	normal

否则，执行如下命令:

	
	set root=(hd0, 5)
	set prefix=(hd0, 5)/boot/grub
	insmod /boot/grub/normal.mod
	normal

4. 进入Ubuntu后，使用如下命令重新安装Grub2。这里的/dev/sda是你要安装MBR的硬盘。

	
	sudo update-grub
	sudo grub-install /dev/sda

### b) /boot/grub引导文件丢失

如果/boot/grub文件已丢失，或通过上面的方法无法找到/boot/grub，则可以通过手动引导进入Ubuntu。

首先使用ls命令查找Linux核心文件vmlinuz所在的分区，假设在(hd0, 4)分区发现了类似vmlinuz-*-generic的文件(*应该是一串数字表示的版本号)。然后使用LiveCD启动后执行如下命令:

	
	sudo mount /dev/sda4 /mnt
	sudo grub-install --boot-directory=/mnt/boot /dev/sda

最后重启即可。
## 参考资料

*  [Grub Rescue修复方法](http://www.2cto.com/os/201111/112327.html)
*  [grub rescue模式下修复](http://www.douban.com/note/66041888/)
*  [Recovering from 'grub rescue>' crash](http://askubuntu.com/questions/197833/recovering-from-grub-rescue-crash)

