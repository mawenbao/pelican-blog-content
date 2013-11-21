Title: Debian/Ubuntu系统小技巧收集
Date: 2013-08-25 12:14
Update: 2013-11-20 15:23
Tags: debian, ubuntu, trick

整理一些Debian/Ubuntu上的小技巧，包括系统管理、系统美化和娱乐等方面。

## 系统管理

### 手动添加locale
查看当前已安装的locale

    locale -a

安装`zh_CN`

    sudo /usr/share/locales/install-language-pack zh_CN

修改默认locale

    sudo cat > /etc/default/locale << EOF
    LANG="zh_CN.UTF-8"
    LANGUAGE="zh_CN"

    source /etc/default/locale

### 设置默认UMASK
umask影响新创建的文件的默认权限，详细的介绍可参考[这篇文章](http://www.cyberciti.biz/tips/understanding-linux-unix-umask-value-usage.html)。设置系统的默认UMASK，首先在`/etc/pam.d/common-session`里添加（可能已存在）如下一行

    session optional pam_umask.so

然后修改`/etc/login.defs`的UMASK值即可。如果只需要改某个用户的UMASK，只要在`~/.bashrc`或`~/.profile`里加入如下一行，注意将00002改为你想要的UMASK。

    umask 0002

### 使用SetGid和umask继承父目录组权限
用一个例子说明，首先创建两个临时用户temp和temp2并设置密码。

    sudo useradd temp
    sudo passwd temp

    sudo useradd temp2
    sudo passwd temp2

创建一个临时组temp-group并将两个临时用户加入临时组里。

    sudo groupadd temp-group
    sudo usermod -a -G temp-group temp
    sudo usermod -a -G temp-group temp2

用temp用户创建一个新的文件夹`/tmp/test`
    
    cd /tmp
    sudo -u temp mkdir test

    ls -ld test
    # drwxr-xr-x 2 temp temp 4096 Nov 10 10:35 test

将`/tmp/test`文件夹的组改为temp-group，并为其添加组的写权限

    sudo chgrp temp-group test
    ls -ld test
    # drwxr-xr-x 2 temp temp-group 4096 Nov 10 10:35 test

    sudo chmod g+w test
    ls -ld test
    # drwxrwxr-x 2 temp temp-group 4096 Nov 10 10:35 test

设置`/tmp/test`文件夹的SetGid权限

    sudo chmod g+s test
    ls -ld test
    # drwxrwsr-x 2 temp temp-group 4096 Nov 10 10:35 test

这样以来，在`/tmp/test`里用temp-group组的用户创建的文件，都会集成父目录`/tmp/test`的组。常见的一个用处就是，temp用户创建的文件，temp2用户也可以直接访问和修改。

`umask 0002`会使新创建文件和文件夹的组用户拥有写权限。

    cd test
    sudo -u temp bash -c 'umask 0002 && mkdir test-sub-dir'
    sudo -u temp2 bash -c 'umask 0002 && touch test-file'

    ls -ld test-dir test-file
    # drwxrwsr-x 2 temp  temp-group 4096 Nov 10 10:45 test-dir
    # -rw-rw-r-- 1 temp2 temp-group    0 Nov 10 10:45 test-file

### 同步系统时间

    ntpdate time.nist.gov

### 设置时区

    dpkg-reconfigure tzdata

### crontab默认编辑器
在Debian/Ubuntu上，运行`crontab -e`命令默认使用nano编辑器，如果想使用vim，可在`~/.bashrc`里加入如下一行:

    export EDITOR=vi
然后使用source命令重新载入`~/.bashrc`即可。

    source ~/.bashrc

###  kubuntu开启和关闭笔记本的触摸板 
使用如下命令开启或关闭触摸板。

    synclient touchpadoff=1 # 关闭触摸板
    synclient touchpadoff=0 # 打开触摸板
    syndaemon -i 3 -d       # 打字时关闭触摸板，3秒打字结束后触摸板关闭的时间

### 使用chkconfig管理系统服务

参考[这篇文章](http://www.aboutlinux.info/2006/04/enabling-and-disabling-services-during_01.html)，使用chkconfig可以方便的启用和禁用`/etc/rcX.d`下的服务，常用的命令有:

*  'chkconfig --list' 查看所有服务的启动状态。
*  'chkconfig apache2 on --level 2,3,5' 使apache2服务在2,3,5运行级别上自动启动。
*  'chkconfig apache2 --add' 添加apache2服务。
*  `chkconfig apache2 off` 在所有运行级别上禁止apache2服务自启动。

Linux系统运行等级简介:

*  0 开机
*  1 单人 文字界面
*  2 多人 无网络功能
*  3 多人 文字界面
*  4 保留
*  5 多人 图形界面
*  6 重启

### 管理多个ssh key文件

生成key:

    ssh-keygen -t rsa -f ~/.ssh/id_rsa.home -C "home key"
    ssh-keygen -t rsa -f ~/.ssh/id_rsa.work -C "work key"  

修改~/.ssh/config，管理key:
	
	Host home
	Hostname home.example.com
	IdentityFile ~/.ssh/id_rsa.home
	User `<your home account>`
	
	Host work
	Hostname work.example.com
	IdentityFile ~/.ssh/id_rsa.work
	User `<your work account>`

更多内容可参考`man ssh_config`

### 为不同的用户使用单独的sshd配置
在`/etc/ssh/sshd_config`文件中，使用Match块可以为某些用户启用单独的配置，这些配置将覆盖全局配置，详情可参考`man sshd_config`.

### 为debian启用单独的Cron日志

Debian上cron的日志默认和其他系统日志记录在一起，查看起来十分不方便，参考[这篇文章](http://pc-freak.net/blog/enable-rsyslog-and-syslog-cron-events-logging-in-varlogcron-log-on-debian-lenny/)，为debian6的cron启用单独的日志。

1. 修改配置文件/etc/rsyslog.conf，

    去掉`#cron.* /var/log/cron.log`这一行的注释符`#`。将`*.*;auth,authpriv.none -/var/log/syslog`改为`*.*;auth,authpriv.none,cron.none  -/var/log/syslog`，如下

        *.*;auth,authpriv.none,cron.none  -/var/log/syslog
        cron.* /var/log/cron.log

2. 重启rsyslogd
	
	    service rsyslog restart

### 自动挂载windows分区

对于ntfs分区，安装如下的软件包，并运行`ntfs-config`配置挂载点。

	sudo apt-get install ntfs-config ntfs-3g

对于fat32分区，可参考[Mounting Windows Partitions](https://help.ubuntu.com/community/MountingWindowsPartitions#FAT32)。
### 修改系统的时区

	tzselect

或

	dpkg-reconfigure tzdata

### 生成ssh key

	ssh-keygen -t rsa -C "wilbur.ma@hotmail.com"

### nohup and screen

nohup帮助程序在后台运行，即使终端关闭也不会有影响。

	nohup ./test.sh &

标准输出会被写入nohup.out，如果当前目录无法正常写入，会写在`~/nohup.out`。

当使用远程连接(ssh)进行系统升级时，screen很有用，即便期间连接断开，也不会影响升级过程，重新连接后还可以方便的恢复到之前的会话。可参考[这里](/tips/build_linux_host#开始升级)。

### 编译po文件
编译gettext的po文件需要安装`translate-toolkit`工具，安装好后运行如下命令即可。

    pocompile zh_CN.po -o zh_CN.mo

或使用msgfmt

    msgfmt -cvo zh_CN.mo zh_CN.po

##  系统美化 

### VLC中文字幕乱码
修改两项配置:

1.  视频>字幕／OSD>文本渲染器>字体 选择一个中文字体。
2.  输入／编码解码器>字幕编解码器>字幕文本编码 选择GB18030，然后去掉"UTF－8字幕"和"格式化字幕"前面的勾。
### 字体
可以考虑使用微软雅黑字体C:\Windows\Fonts\msyh.ttf和C:\Windows\Fonts\msyhbd.ttf，效果会好很多。

### ibus输入法
	
	sudo apt-get install ibus gnome-icon-theme

如果安装ibus后，无法显示系统托盘图标和候选词框，安装gnome-icon-theme即可。如果安装后依然有问题，可执行如下命令。

    ibus-daemon -x -r -d

设置ibus-pinyin的候选词个数:

   /usr/lib/ibus-pinyin/ibus-setup-pinyin

## 娱乐

### 1. MP3标签中文乱码
尚需完善
#### a) 图形界面转码工具
easytag
#### b) mutagen
	
	sudo apt-get install convmv iconv python-mutagen
	find . -iname "*.mp3" -execdir mid3iconv -e GBK {} \;

## 参考资料

*  [Linux 技巧：让进程在后台可靠运行的几种方法](http://www.ibm.com/developerworks/cn/linux/l-cn-nohup/)
*  [Enable Rsyslog and Syslog cron events logging in /var/log/cron.log on Debian Lenny](http://pc-freak.net/blog/enable-rsyslog-and-syslog-cron-events-logging-in-varlogcron-log-on-debian-lenny/)
*  [用nohup命令让Linux下程序永远在后台执行](http://www.einit.com/user1/11/archives/2006/3603.html)
*  [解决文件名mp3标签和文本文件内容的乱码问题](http://wiki.ubuntu.org.cn/解决文件名mp3标签和文本文件内容的乱码问题)
*  [kubuntu 12.04 (KDE) ibus 图标及选词框不出现、firefox不支持的解决方法](http://forum.ubuntu.org.cn/viewtopic.php?f=80&t=373310)
*  [简单方法解决VLC中文字幕乱码](http://forum.ubuntu.org.cn/viewtopic.php?t=201887)
*  [Multiple public keys for one user](http://serverfault.com/questions/221760/multiple-public-keys-for-one-user)
*  [Enabling and disabling services during start up in GNU/Linux](http://www.aboutlinux.info/2006/04/enabling-and-disabling-services-during_01.html)
*  [触摸板](http://wiki.ubuntu.org.cn/%E8%A7%A6%E6%91%B8%E6%9D%BF) from ubuntu wiki cn
*  [Mounting Windows Partitions](https://help.ubuntu.com/community/MountingWindowsPartitions)
*  [How to set system wide umask?](http://stackoverflow.com/questions/10220531/how-to-set-system-wide-umask)
*  [What is Umask and How To Setup Default umask Under Linux?](http://www.cyberciti.biz/tips/understanding-linux-unix-umask-value-usage.html)
*  [Configure inherit group ownership on Linux folder](http://gsienkiewicz.wordpress.com/2013/04/05/configure-inherit-group-ownership-on-linux-folder/)

