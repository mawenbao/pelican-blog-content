Title: Debian软件管理常用命令
Date: 2013-08-25 12:14
Tags: debian, ubuntu, apt, dpkg

参考了[这篇文章](http://www.thegeekstuff.com/2009/10/debian-ubuntu-install-upgrade-remove-packages-using-apt-get-apt-cache-apt-file-dpkg/)，在这里记录debian系统上管理软件经常用到的命令，以方便以后查询。
## apt

### apt-get

*  `apt-get install` 安装软件
*  `apt-get -f install` 修复依赖关系
*  `apt-get -u install` 升级软件  
*  `apt-get remove %pkg%` 删除软件
*  `apt-get purge %pkg%` 删除软件及其配置文件
*  `apt-get -u upgrade` 升级所有已安装的软件
*  `apt-get dist-upgrade` 升级操作系统到下一个版本
*  `apt-get build-dep %pkg%` 安装依赖的软件
### apt-cache

*  `apt-cache search` 根据软件名或软件介绍查找软件
*  `apt-cache show` 显示软件的基本信息
*  `apt-cache showpkg` 显示软件的详细信息，包括详细的依赖信息等
*  `apt-cache depends` 显示软件的依赖信息
### apt-file

*  `apt-file list` 列出软件包含的所有文件
*  `apt-file show` 同`apt-file list`
*  `apt-file find` 根据软件包含的文件的名称来搜索软件，使用`-x`或--regexp选项可支持perl正则表达式查询。
*  `apt-file search` 同`apt-file search` 

## dpkg

### dpkg

*  `dpkg -l` 列出所有已安装的软件
*  `dpkg -i `<.deb>` 安装本地deb软件包
*  `dpkg -L` 列出已安装的软件所包含的文件
*  `dpkg -r` 删除软件包
*  dpkg --force-all -r 强制删除软件包
*  dpkg --force-all -P 强制删除软件包及其配置文件（若删除失败可先尝试强制安装该软件包）
### dpkg-reconfigure

重新配置软件
### dpkg-deb 暂无

### dpkg-source 暂无
### dpkg-query 暂无

### dpkg list status

使用dpkg -l(--list)命令时，在软件包的前面会有两个字符(如ii)显示安装状态，如下所示:

	
	...
	ii  php5-memcached                         5.3.19-1~dotdeb.0                      memcached module for php5
	ii  php5-mysql                             5.3.19-1~dotdeb.0                      MySQL module for php5
	rc  php5-suhosin                           5.3.19-1~dotdeb.0                      suhosin module for php5
	...

以下是状态的说明。
#### 第一个字符

第一个字符表示被标记的安装状态:

1.  u: Unknown (an unknown state)
2.  i: Install (marked for installation)
3.  r: Remove (marked for removal)
4.  p: Purge (marked for purging)
5.  h: Hold
#### 第二个字符

第二个字符表示当前状态:

1.  n: Not - The package is not installed
2.  i: Inst – The package is successfully installed
3.  c: Cfg-files – Configuration files are present
4.  u: Unpacked - The package is stilled unpacked
5.  f: Failed-cfg - Failed to remove configuration files
6.  h: Half-inst - The package is only partially installed
7.  w: Trig - Wait
8.  t: Trig - Pend
## 参考资料

*  [apt-get, apt-file, apt-cache和dpkg的例子](http://www.thegeekstuff.com/2009/10/debian-ubuntu-install-upgrade-remove-packages-using-apt-get-apt-cache-apt-file-dpkg/)
*  [How to interpret the status of dpkg (–list)?](http://linuxprograms.wordpress.com/2010/05/11/status-dpkg-list/)

