Title: git problems
Date: 2013-08-25 12:14
Tags: git, problem

# Git问题整理

整理git使用过程中遇见的错误及其解决方案。

## Git错误

收集整理常见的git错误。
### fatal: cannot exec .. Permission denied

使用git alias命令`git st`(参考[这里的配置](./config#全局配置))时提示如下错误:

	
	fatal: cannot exec git st: Permission denied

参考[stackoverflow](http://stackoverflow.com/questions/7997700/git-aliases-causing-permission-denied-error)上的解答, 使用如下方法解决. 

1. 安装strace

	
	apt-get install strace

2. 使用strace执行`git st`

	
	strace -f -e execve git st

3. 根据输出结果进行修正, 我的错误在于$PATH变量设置有误.

### Cygwin git ca-bundle.cert错误

cygwin下用git向远程https仓库推送数据时遇到以下问题:

	
	error: error setting certificate verify locations:
	  CAfile: /usr/ssl/certs/ca-bundle.crt
	  CApath: none while accessing https://github.com/wilbur-ma/dokuwiki-tweak.git/info/refs
	fatal: HTTP request failed

参考[这里](http://tech.idv2.com/2012/09/14/cygwin-git-error/)，解决办法是在cygwin上安装ca-certificates。

## 参考资料

*  [git aliases causing permission denied error](http://stackoverflow.com/questions/7997700/git-aliases-causing-permission-denied-error)

