Title: 在Kubuntu 14.04上安装和配置Subversion 1.6
Date: 2014-04-23 12:52
Tags: ubuntu, 安装

[1]: http://olex.openlogic.com/packages/subversion

本来不想再写这种安装指南一类的文章，但是整个安装过程太虐，只好当作日志记录下来，以备日后查用。

公司的svn仓库是用subversion1.6创建的，一直没有升级。工作用的Kubuntu14.04仓库里的subversion是1.8.8的，两者完全不兼容，因此有了下文。

## 获取Subversion1.6源码

Subversion现在已经是Apache基金会下的软件了，但是官网的源码包里最低的版本是1.7的，貌似1.6版本的svn已经被彻底抛弃了的说。终于在[这里][1]找到了1.6的源码包，下载1.6.20的源码包。

## 安装依赖

Kubuntu上自带的gcc是4.8的，编译1.6.20的代码会有点问题，但是基本能绕过去。

下面是一些编译要用的工具，一般都应该装过了。

    sudo apt-get install autoconf automake libtool build-essential 

为了让svn支持http/https协议，需要安装neon

    sudo apt-get install libneon27 libneon27-dev

为了支持加密保存svn账户的密码，需要安装gnome-keyring。这里没有用Kubuntu自带的kwallet，因为1.6.20里自带的kwallet模块用gcc4.8编译会报错，有点麻烦的那种错。

    sudo apt-get install gnome-keyring libgnome-keyring-dev libkrb5-dev seahorse

seahorse是一个管理gnome-keyring的图形界面，装不装都可以。

最后是一些**可能**会依赖到的软件

    sudo apt-get install libaprutil1 libaprutil1-dev libdbus-1-dev libdbus-glib-1-dev

如果还缺少什么库，记得多用google和apt-file。

## 编译安装Subversion1.6

    ./configure --with-neon --with-ssl --with-gnome-keyring
    make -j4
    sudo make install

运行`svn --version`，查看svn版本和仓库获取模块，如果有

    * ra_neon : Module for accessing a repository via WebDAV protocol using Neon.
      - handles 'http' scheme
      - handles 'https' scheme

基本就算安装成功了

## 配置Subversion1.6
参考网上的一些经验，这里主要是让svn记得将密码保存在gnome-keyring里。

总共涉及到两个配置文件

1. `~/.subversion/config`

        [auth]
        password-stores = gnome-keyring

2. `~/.subversion/servers` (这个貌似可以直接用默认的配置)
    
        [global]
        store-passwords = yes
        store-plaintext-passwords = no

完了

