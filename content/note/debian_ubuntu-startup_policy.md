Title: debian ubuntu startup policy
Date: 2013-08-25 12:14
Tags: debian, ubuntu, startup, note

# Debian/Ubuntu自启动方法总结
总结Debian/Ubuntu的启动方法.

## XDG AutoStart
将程序的快捷方式置于''/etc/xdg/autostart''即可随XDG自启动.下面是fcitx输入法的快捷方式.

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

## /etc/rc.d

### rc.local

## 参考资料

