Title: Debian/Ubuntu常见问题及解决方法整理
Date: 2013-08-25 12:14
Update: 2013-11-30 12:04
Tags: debian, ubuntu, problem

记录使用Debian/Ubuntu时遇到的问题及其解决方法。

## 网络问题

### ping: connect: network is unreachable
使用`service networking restart`后无法联网，运行`ifconfig`后发现没有eth0，这时需要手动配置eth0接口，注意将$IP_ADDRESS, $MASK和$GATE_WAY改为你的IP地址、子网掩码和网关地址:
    
    ifconfig eth0 $IP_ADDRESS netmask $MASK
    route add default gw $GATE_WAY

## Kubuntu常见问题合集
### fcitx无法在konsole和kate中使用
安装qt4-qtconfig，并在qtconfig的`界面`选项卡中选择`fcitx`为默认输入法，保存后退出。然后重启konsole或kate即可。

### ssh连接慢
编辑`/etc/ssh/ssh_config`文件，注释掉如下的两行配置：

    #GSSAPIAuthentication yes
    #GSSAPIDelegateCredentials no

关于GSSAPI Authentication，可参考[Using GSSAPI authentication at SLAC](http://www.slac.stanford.edu/comp/unix/sshGSSAPI.html)。

## 系统管理
### fcitx无法使用
在Chrome和Firefox中，fcitx无法使用。运行`fctix-diagnose`根据提示在`~/.xprofile`里设置如下变量。

    export QT_IM_MODULE=fcitx
    export GTK_IM_MODULE=fcitx
    export XMODIFIERS=@im=fcitx

如果使用kdm，还需要创建文件`/etc/X11/Xsession.d/93fcitx`:

    !#/bin/bash

    export QT_IM_MODULE=fcitx
    export GTK_IM_MODULE=fcitx
    export XMODIFIERS=@im=fcitx

最后重启系统即可。

## 阅读资料

*  [connect: network is unreachable的解决](http://blog.csdn.net/xuyaqun/article/details/6283829)
*  [fcitx在konsole和kate等程序中无法使用的解决办法](http://magic282.me/2012/09/fix-the-problem-that-fcitx-cannot-input-the-qt-programs-such-as-konsole-and-kate/)


