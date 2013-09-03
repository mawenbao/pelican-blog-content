Title: windows tips
Date: 2013-08-08 12:14
Tags: windows, tip

# Tips on windows

收录一些windows下的技巧。

## DOS & Powershell

### 结束进程
    taskkill /f /pid 1234
    taskkill /f /im task_name.exe

### Cygwin git ca-bundle.cert错误

cygwin下用git向远程https仓库推送数据时遇到以下问题:

	
	error: error setting certificate verify locations:
	  CAfile: /usr/ssl/certs/ca-bundle.crt
	  CApath: none while accessing https://github.com/wilbur-ma/dokuwiki-tweak.git/info/refs
	fatal: HTTP request failed

参考[这里](http://tech.idv2.com/2012/09/14/cygwin-git-error/)，解决办法是在cygwin上安装ca-certificates。

## 参考资料

*  [cygwin下git出现ca-bundle.crt相关错误的解决办法](http://tech.idv2.com/2012/09/14/cygwin-git-error/)

{{tag>windows tip}}
