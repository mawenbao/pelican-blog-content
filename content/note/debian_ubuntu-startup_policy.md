Title: Debian/Ubuntu自启动方法总结
Date: 2013-08-25 12:14
Update: 2013-12-05 14:50
Tags: debian, ubuntu, startup, note, 未完成

总结Debian/Ubuntu的启动方法.

## XDG AutoStart
将程序的快捷方式置于`/etc/xdg/autostart`即可随XDG自启动.下面是fcitx输入法的快捷方式.

    [Desktop Entry]
    Name=Fcitx
    Name[zh_CN]=Fcitx
    Name[zh_TW]=Fcitx
    Comment=Input Method
    Comment[zh_CN]=输入法
    Comment[zh_TW]=輸入法
    Exec=fcitx
    Icon=fcitx
    Terminal=false
    Type=Application
    Categories=System;Utility;
    StartupNotify=false
    X-GNOME-Autostart-Phase=Applications
    X-GNOME-AutoRestart=false
    X-GNOME-Autostart-Notify=false
    X-KDE-autostart-after=panel
    X-KDE-StartupNotify=false

## ~/.config/autostart
在以下环境里测试成功

* kde4

在`~/.config/autostart`文件夹下保存的desktop文件都会在用户登录后自动启动。也可直接在kde的启动配置里添加。

## /etc/rc.d

## rc.local

## /etc/X11/Xsession
`/etc/X11/Xsession.d`存放了很多图形界面的初始化脚本。

## Upstart
Ubuntu从6.10引入upstart，并在9.10将多数系统服务转换到upstart下，不过system v init system的服务依然被兼容。

## 阅读资料
1. [UbuntuBootupHowto](https://help.ubuntu.com/community/UbuntuBootupHowto)
2. [UpstartHowto](https://help.ubuntu.com/community/UpstartHowto)
3. [Upstart Intro, Cookbook and Best Practises](http://upstart.ubuntu.com/cookbook/)
