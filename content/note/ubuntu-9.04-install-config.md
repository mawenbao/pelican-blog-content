Title: Ubuntu 9.04硬盘安装和基本配置
Date: 2009-09-06 10:42:14
Tags: ubuntu, install, config

Ubuntu 9.04的硬盘安装和基本配置。

## 硬盘安装

### vmlinuz initrd.gz 获得
将安装盘debian-XX.iso 与 vmlinuz, initrd.gz 置于同一驱动器根目录下

    http://http.us.debian.org/debian/dists/lenny/main/installer-i386/current/images/hd-media/
    ftp://ftp.sjtu.edu.cn/debian/dists/lenny/main/installer-i386/current/images/hd-media/

### grub4dos 命令
在grub4dos命令行界面执行如下命令。如不成功，应检查vmlinuz和initrd.gz文件与安装盘debian-XX.iso是否对应。如还不成功，可在kernel命令最后添加generic-ide命令。

    > find debian-XX.iso
    (hd0,4) // e.g.
    > root (hd0,4)
    > kernel /vmlinuz
    > initrd /initrd.gz
    > boot

## 基本配置

### 网络设置
ADSL设置

    root-terminal> fdisk -l
    partition table
    ...
    root-terminal> mkdir /media/diskX
    root-terminal> mount /dev/sdaX /media/diskX
    root-terminal> mount -o loop /media/diskX/debian-XX.iso /media/cdrom
    root-terminal> apt-get install pppoeconf
    ...
    
### 软件源设置
`/etc/apt/sources.list`：

    deb ftp://ftp.sjtu.edu.cn/debian lenny main contrib non-free
    deb-src ftp://ftp.sjtu.edu.cn/debian lenny main contrib non-free

### 字体

    apt-get install ttf-bitstream-vera msttcorefonts
 
### scim输入法

    apt-get install scim scim-pinyin
 
## 常用软件

### Emacs 23编译和安装
从源码编译安装emacs23：

    git clone git://git.savannah.gnu.org/emacs.git

    sudo apt-get build-dep emacs21
    build-essential
    xserver-xorg
    xorg-dev
    libncurses5
    libncurses5-dev
    libgtk2.0-dev

    ./configure --with-x --with-x-toolkit=gtk
    make bootstrap
    sudo make install 

配合emcas用的工具：

    cscope
    global
    dictd
    dict-gcide
    dict-wn

    Character Encoding
    gnu recode
    convmv

    dialog --- Display dialog boxes from shell scripts

### 其他常用软件

    perl 
    perl-doc 
    JavaScript::Packer

    drupal
    lighttpd
    postgresql-8.4
    php5-cli  php5-cgi  php5-pgsql  php5-gd

    CHM 
    CHM Viewer
    chm2pdf
    
 
