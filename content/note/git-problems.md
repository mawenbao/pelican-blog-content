Title: Git问题整理
Date: 2013-08-25 12:14
Tags: git, problem
Update: 2013-10-18 10:40

[1]: https://www.kernel.org/pub/software/scm/git/docs/git-config.html "git config(1) manual page"


整理git使用过程中遇见的错误及其解决方案。

## 中文文件或目录名被转码

git默认会对路径里超过0x80的字节进行转码，设置`core.quotepath`为`fasle`可以禁止自动转码，详情见[git-config(1)][1]的`core.quotepath`部分。

    git config --global core.quotepath false
    
## fatal: cannot exec .. Permission denied

使用git alias命令`git st`(参考[这里的配置](./config#全局配置))时提示如下错误:
	
    fatal: cannot exec git st: Permission denied

参考[stackoverflow](http://stackoverflow.com/questions/7997700/git-aliases-causing-permission-denied-error)上的解答, 使用如下方法解决. 

1. 安装strace
	
    apt-get install strace

2. 使用strace执行`git st`
	
    strace -f -e execve git st

3. 根据输出结果进行修正, 我的错误在于$PATH变量设置有误.

## Cygwin git ca-bundle.cert错误

cygwin下用git向远程https仓库推送数据时遇到以下问题:

    error: error setting certificate verify locations:
    CAfile: /usr/ssl/certs/ca-bundle.crt
    CApath: none while accessing https://github.com/wilbur-ma/dokuwiki-tweak.git/info/refs
    fatal: HTTP request failed

参考[这里](http://tech.idv2.com/2012/09/14/cygwin-git-error/)，解决办法是在cygwin上安装ca-certificates。

## recursion detected in die handler 
使用`git push`的时候遇到如下问题:

    fatal: recursion detected in die handler

参考[这里](http://stackoverflow.com/questions/12651749/git-push-fails-rpc-failed-result-22-http-code-411)的问题，问题原因是http.postBuffer默认上限为1M所致。在git的配置里将http.postBuffer变量改大一些即可，比如将上限设为5M：

    git config http.postBuffer 5242880

问题的原解决答案为：
> If you attempt to push a large set of changes to a Git repository with HTTP or HTTPS, you may get an error message such as error: RPC failed; result=22, HTTP code = 411. This is caused by a Git configuration default which limits certain HTTP operations to 1 megabyte.
>
> To change this limit run within your local repository
>
> git config http.postBuffer *bytes*
> where bytes is the maximum number of bytes permitted.

## 参考资料

*  [git aliases causing permission denied error](http://stackoverflow.com/questions/7997700/git-aliases-causing-permission-denied-error)
*  [git push fails: RPC failed; result=22, HTTP code = 411](http://stackoverflow.com/questions/12651749/git-push-fails-rpc-failed-result-22-http-code-411)
*  [git-config(1) Manual Page][1]

