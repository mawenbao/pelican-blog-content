Title: ubuntu12.04 安装rtx
Date: 2013-08-25 12:14
Tags: wine, ubuntu, rtx

在ubuntu12.04上使用wine1.4安装rtx。

## 准备工作

    sudo apt-get install wine
    wget http://www.kegel.com/wine/winetricks 
    chmod +x winetrickh 
    winetricks msxml3 gdiplus riched20 riched30 ie6 vcrun6 vcrun2005sp1 
无法下载的包需要手动下载后放到~/.cache/winetricks/XXX/里，根据提示操作即可。

## 已解决问题

### rtx始终处于离线状态
个人设置 -> 回复设置 -> 自动转换状态 取消
### 中文字体乱码

在“Configure Wine”的“函数库”里添加“oleaut32"。

### 自己名字乱码

在“个人设置”里修改即可。

## 未解决问题

### 无法查看消息记录
错误提示如下。

	
	The native implementation of OLEAUT32.DLL cannot be used with Wine's RPCRT4.DLL. Remove OLEAUT32.DLL and try again.

## 参考资料

*  [关于用wine安装rtx的问题](http://www.oschina.net/question/193954_33387)
*  [Ubuntu 下 wine rtx 的安装（解决组织架构不显示问题）](http://www.oldfeel.cn/?p=840)
