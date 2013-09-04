Title: bash tricks
Date: 2013-08-25 12:14
Tags: bash, trick

# Bash小技巧合集

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


### shopt

修改额外的bash选项，常用的选项有:

	shopt             # 查看所有选项的状态
	shopt -s extglob  # 启用扩展的glob匹配
	shopt -u extglob  # 禁用扩展的glob匹配


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


## 参考资料

*  [Reference Cards](http://tldp.org/LDP/abs/html/refcards.html) from ["advanced bash scripting guide"](http://tldp.org/LDP/abs/html/)
*  [The Set Builtin](http://www.gnu.org/software/bash/manual/bash.html#The-Set-Builtin) from gnu bash documentation
*  [The Shopt Builtin](http://www.gnu.org/software/bash/manual/bash.html#The-Shopt-Builtin) from gnu bash documentation
*  [Bourne Shell Variables](http://www.gnu.org/software/bash/manual/bash.html#Bourne-Shell-Variables) from gnu bash documentation
*  [Pattern Maching](http://www.gnu.org/software/bash/manual/bash.html#Pattern-Matching) from gnu bash documentation

