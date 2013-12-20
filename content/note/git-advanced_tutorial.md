Title: Git进阶教程
Date: 2013-08-25 12:14
Update: 2013-12-20 16:49
Tags: git, tutorial

Git的常用命令和场景可参考[Git快速使用指南](/note/git-quick_reference.html)，在这里介绍进一步的使用和部分生僻的命令。

## Git进阶使用场景

并不常见的使用场景。
### detached HEAD state

有时需要返回之前的提交状态，此时会处于“detached head“状态。

	mkdir git-test && cd $_ && git init  # 初始化一个新的git仓库
	touch a.txt && git add $_ && git commit -m "first commit"   # 添加文件a.txt并提交
	touch b.txt && git add $_ && git commit -m "second commit"  # 添加文件b.txt并提交
	git log --oneline  # 查看提交日志
	# 输出如下(##开头)
	## 8083b9e second commit
	## 15b7a79 first commit
	git branch         # 查看分支情况
	# 输出如下(##开头)
	## * master
	# 现在签出first commit
	git checkout 15b7a79
	# 输出如下(##开头)
	## Note: checking out '15b7a79'.
	## You are in 'detached HEAD' state.
	## ...

此时即处于detached head状态，当前的文件回到first commit后的样子。

	git branch
	# 输出如下所示(##开头)
	## * (no branch)
	## master

最后，可以用如下命令回到second commit状态。
    git checkout master

## Git生僻命令
### 检索日志和修改内容
检索提交消息

    git log --grep "hello world"

检索修改内容

    git log -S "hello world"

使用正则表达式检索修改内容

    git log -G "^hello world$"

## 参考资料

*  [Git Tip of the Week: Detached Heads](http://alblue.bandlem.com/2011/08/git-tip-of-week-detached-heads.html)

