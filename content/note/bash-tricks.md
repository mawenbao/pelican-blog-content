Title: Bash小技巧合集
Date: 2013-08-25 12:14
Update: 2014-06-26 09:55
Tags: bash, trick

收集一些bash下的技巧。

## 符号

bash里一些特殊的符号的作用。

### 两个连字符

'--': 仅有两个横杠(即连字符`-`)(two hyphens)，即后面没有任何长选项名的时候，表示重置命令的位置参数，'--'后的参数均从第一个参数开始算起。
## 变量

包括自定义变量和特殊变量。
###  自定义变量 

自定义变量赋值时，变量名和等号以及等号和值之间都不要有空白字符(空格、制表符等)，如:
    a=100
### 特殊变量

特殊变量是指bash保留的变量名。完整的特殊变量列表可参考[这里](http://tldp.org/LDP/abs/html/refcards.html)的table b-1。

*  $0 命令或脚本名
*  $1 第一个参数
*  ${10} 第十个参数
*  $# 参数个数
*  $? 上一个命令的返回值
*  $$ 脚本的pid
*  $_ 上一个命令的最后一个参数

## 内置命令

介绍bash的常用内置命令。
### set

设置bash选项和位置参数，常用的选项有:

    :::sh
	set -o         # 查看当前所有选项的状态
	set -o history # 开启bash历史记录
	set +o history # 关闭bash历史记录
    set -e         # 当脚本中有命令返回不为0时，立即退出脚本

### shopt

修改额外的bash选项，常用的选项有:

	shopt             # 查看所有选项的状态
	shopt -s extglob  # 启用扩展的glob匹配
	shopt -u extglob  # 禁用扩展的glob匹配
    shopt -s dotglob  # 使wildcard(*)匹配dot开头的文件(隐藏文件)

## 模式匹配

详细文档参考[pattern maching](http://www.gnu.org/software/bash/manual/bash.html#Pattern-Matching)。使用[shopt](#shopt)开启extglob后，除了`? * []`等常用的匹配符，bash还能支持以下模式，其中pattern-list是一个或多个用`|`符号分隔的模式。

	
	?(pattern-list)  Matches zero or one occurrence of the given patterns.
	*(pattern-list)  Matches zero or more occurrences of the given patterns.
	+(pattern-list)  Matches one or more occurrences of the given patterns.
	@(pattern-list)  Matches one of the given patterns.
	!(pattern-list)  Matches anything except one of the given patterns.

例如，目录test包含如下三个文件:
	
	test\
	    aaa.txt
	    aaa.log
	    bbb.txt

使用命令`ls !(a*).txt`将输出:
    bbb.txt

## IO重定向和复制文件描述符
Bash中可以通过`<`, `<<`, `>`和`>>`四个符号实现IO重定向，详情参考`man bash`的**REDIRECTION**部分。还可以通过`<&`和`>&`复制文件描述符，详情参考`man bash`的**Duplicating File Descriptors**部分。需要说明的是，当这两者混合使用的时候，必须注意先后顺序。援引`man bash`中的例子，

    ls >dirlist 2>&1

首先将ls的标准输出(1)重定向到dirlist文件，然后将ls的标准错误(2)设置为标准输出(已被重定向)的拷贝，所以ls的标准输出和标准错误都被重定向到了dirlist文件中。

    ls 2>&1 >dirlist

首先将ls的标准错误(2)设置为标准输出(1)的拷贝，然后将标准输出重定向到dirlist文件，所以ls的标准错误最终被写入标准输出中，而ls原本的标准输出被重定向到了dirlist文件中。

## 快捷键
bash的很多快捷键和emacs相似，可以多尝试一下。

    ctrl + a 行首
    ctrl + e 行尾
    ctrl + b 倒退一个字母
    ctrl + f 前进一个字母
    alt  + f 前进一个单词（可能被占用）
    alt  + b 倒退一个单词（可能被占用）

    ctrl + r 逆向搜索历史命令
    alt  + c 光标处字母大写或右边单词首字母大写
    alt  + u 光标至单词结尾转为大写
    alt  + l 光标单词结尾转为小写
    ctrl + t 交换左右字母
    alt  + t 交换左右单词
    ctrl + h 删除左边的字母
    ctrl + d 删除右边的字母

    # 剪切和粘贴的内容并不位于系统的剪贴板
    ctrl + y 粘贴
    ctrl + w 剪切左边的单词
    alt  + d 剪切光标至单词结尾的内容
    ctrl + k 剪切光标至行尾的内容
    ctrl + u 剪切光标至行首的内容

## 环境变量

### proxy环境变量
* `http_proxy`: http代理
* `socks_proxy`: socks代理

例如:

    http_proxy=localhost:12345

    socks_proxy=localhost:23456 wget http://url/of/the/file/to/download

## 阅读资料

*  [Reference Cards](http://tldp.org/LDP/abs/html/refcards.html) from ["advanced bash scripting guide"](http://tldp.org/LDP/abs/html/)
*  [The Set Builtin](http://www.gnu.org/software/bash/manual/bash.html#The-Set-Builtin) from gnu bash documentation
*  [The Shopt Builtin](http://www.gnu.org/software/bash/manual/bash.html#The-Shopt-Builtin) from gnu bash documentation
*  [Bourne Shell Variables](http://www.gnu.org/software/bash/manual/bash.html#Bourne-Shell-Variables) from gnu bash documentation
*  [Pattern Maching](http://www.gnu.org/software/bash/manual/bash.html#Pattern-Matching) from gnu bash documentation

