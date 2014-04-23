Title: Debian/Ubuntu 常用软件
Date: 2013-08-25 12:14
Update: 2014-04-23 11:14
Tags: debian, ubuntu, package, resource

介绍常用Debian/Ubuntu平台上的软件和部分软件的使用方法。可在[Linux Packages Search](http://pkgs.org/)查找需要的软件包。

## 软件列表

下面是常用的debian软件列表，直接运行`apt-get install %package-name%`即可安装。

系统管理

*  apropos 查找说明手册
*  apt-file 可用于查找文件所属的软件包
*  batch & atq 设置和管理一次计划任务
*  chkconfig 管理系统服务
*  exim4 邮件服务器
*  fallocate 创建指定大小的空文件
*  htop 比top更直观的进程监控/系统信息软件
*  locate 配合updatedb进行文件索引和搜索
*  mutt 收发邮件
*  p7zip 7zip的linux版本
*  shred 涂改和彻底删除文件，使其无法被恢复
*  tcpdump packet analyzer
*  translate-toolkit
*  unzip 解压zip压缩格式的文件
*  watch 每隔一段时间执行某个程序，然后全屏输出执行结果
*  zgrep 类似于grep，但支持在压缩文件中查找 
*  zip 压缩为zip格式 

应用

*  httrack 制作镜像网站
*  xsel 剪贴板工具

开发相关

*  build-essential
*  python2.6 python2.6-dev
*  python-setuptools
*  python-pip
*  php5-fpm
*  phpmyadmin
*  mysql-server-5.1
*  ruby1.9.1
*  addr2line 可以将objdump中的函数地址翻译为文件名和行数

网络

*  jnettop 监控最占用网络流量的连接

## 软件快速使用指南

介绍部分生僻软件或工具的快速使用指南。

### strace
常用于调试程序，可以输出程序的系统调用。

    -f      同时输出fork出的子进程的系统调用
    -p PID  输出进程号为PID的进程的系统调用

### shred
rm只是删除了文件系统中相关的项，并没有彻底抹掉磁盘上文件的内容。shred可以将文件进行一定次数的涂改并删除(-n)。

    shred -i 100 password.txt # 涂改100次，默认3次
    shred -u -i 100 password.txt # 涂改100次然后删除

### rtcwake
将操作系统休眠一段时间后再醒来。

    rtcwake -m mem -s 10

上面的命令表示，休眠10秒后再醒来。

### screen

### diff

生成patch文件。

    diff -ru file_a.old file_a.new > file_a.patch

比较目录

    diff -rq dir_a dir_b
### dos2unix unix2dos unix2mac

如名称所示，用于windows，unix和mac os换行符的转换。
### file

查看文件类型

    file /bin/ls

### find

查找命令，使用-name选项时，应注意引用(单引号或双引号均可)查找字符串，否则查找内容可能不全?

    find . -name "*.html"

### ldd

查看程序依赖的共享库，通常用于检查`error while loading shared libraries`之类的错误。

    ldd -v /bin/ls

### lsb_release

查看linux发行版的信息:

    lsb_release -a

也可使用

    cat /etc/issue

或

    uname -a

### objdump

display information from object files，常用于查看目标文件的架构。

    objdump -f /usr/lib64/libacl.so

输出:

	/usr/lib64/libacl.so:     file format elf64-x86-64
	architecture: i386:x86-64, flags 0x00000150:
	HAS_SYMS, DYNAMIC, D_PAGED
	start address 0x0000003141a01900

### pkill

踢掉登录的用户。

    last | head

输出如下:

	wilbur   pts/1        116.236.230.250  Fri Jan  4 14:11   still logged in   
	wilbur   ppp0         222.66.81.66     Fri Jan  4 09:26 - 09:29  (00:03)    
	wilbur   pts/0        222.66.81.66     Fri Jan  4 09:20   still logged in

运行以下命令即可踢掉终端为pts/0的用户。

    pkill -kill -t pts/0

### strings

查看文件里的可读字符，通常配合grep查看二进制文件里的某些可读信息。

    strings /bin/ls | grep -i usage

### su

参考[这里的回复](http://www.computing.net/answers/solaris/get-the-home-directory-after-su/5035.html)

>su `<user id>` doesn't change the user environment - including environmental variables. To change the environment, you must execute su - `<user id>`. According to the su MAN page:
>If the first argument to su is a dash (-), the environment will be changed to what would be expected if the user >actually logged in as the specified user.

### uname

查看系统信息

    uname -a

### type

bash的内置命令，可通过`man builtins`查看使用说明，通常用`type -a <command>`查找当前环境下的可执行文件的所有位置。

## 阅读资料

*  [Get The Home Directory After Su](http://www.computing.net/answers/solaris/get-the-home-directory-after-su/5035.html)

