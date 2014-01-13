Title: Ubuntu下使用rtxSync监听rtx
Date: 2013-10-17 11:12:00
Tags: rtx, rtxSync, ubuntu

[1]: http://blog.csdn.net/xcwenn/article/details/8840646 "rtxSync"
[2]: http://code.google.com/p/san2/downloads/detail?name=rtxSync.1.0.1.tar.gz&can=2&q= "download rtxSync 1.0.1"
[3]: http://joncraton.org/media/files/nc111nt.zip "download netcat for windows"
[4]: http://joncraton.org/blog/46/netcat-for-windows

介绍在ubuntu系统上使用rtxSync监听虚拟机内安装的rtx消息的方法。平时基本上在Ubuntu系统下工作，但是公司内部通讯用的是腾讯通rtx。尝试过用wine跑rtx，虽然可行但是效果不好，没办法只好在虚拟机里装rtx，为了及时查看新消息，需要rtxSync的帮助。

## rtxSync
[rtxSync][1]主要包含一个rtx的插件`rtxsync.rpi`和ubuntu任务栏通知程序`xptray`，当有新的rtx消息时，xptray会闪烁。最新的rtxSync可在[这里][2]下载。

## 安装依赖的软件包
首先为rtxSync的任务栏通知程序`xptray.py`安装依赖的软件包：

    sudo apt-get install python-appindicator python-gtk2

另外，`xptray.py`的代码里有引入`pynotify`库，不过在代码(1.0.1版本)里并没有实际使用。所以如果运行xptray提示找不到`pynotify`模块的话，可以注释掉`xptray.py`开头的这一行：

    #import pynotify

接下来按照作者的[教程][1]安装即可。

## 常见问题

### 有新消息时xptray不闪烁
按如下步骤排查错误所在：

1. 在虚拟机上ping ubuntu系统，如果ping不通，则是虚拟机网络设置的问题。
2. 如果网络正常，在[这里][3]下载[netcat for windows][4]，解压后将nc.exe放在`C:\Windows`文件夹下，假设xptray的监听地址为
`10.1.5.85:3000`，则在虚拟机的cmd上执行命令

        echo 1 | nc -u -w 1 10.1.5.85 3000
    如果xptray不闪烁，很有可能是监听地址配置错误，或rtx上的rtxsync配置有误。重新配置后，重启rtx和xptray再查看。

## 阅读资料

*  [rtx消息 虚拟机xp 通知到 主机ubuntu][1]

