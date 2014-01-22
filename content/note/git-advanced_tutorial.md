Title: Git进阶教程
Date: 2013-08-25 12:14
Update: 2014-01-21 16:34
Tags: git, 教程

Git的常用命令和场景可参考[Git快速使用指南](/note/git-quick_reference.html)，在这里介绍进一步的使用和部分生僻的命令。

## Git概念和技巧
### Git使用ssh协议

    git clone ssh://name@host/absolute/path/to/repo
    git clone name@host:/path/to/repo

### Index vs. Working tree
使用git reset命令的时候不容易搞懂Index和Working tree这两个概念，下面简要总结一下。

![git index & working tree](/static/images/note/git-index-working-tree.png)

(图片取自stackoverflow上的一个[回答](http://stackoverflow.com/questions/3689838/difference-between-head-working-tree-index-in-git)，来源未知)

#### Git index
有时候也被称作Staging area和Cache，git add等命令会将文件改动暂存在index中(.git/index)，运行git status后，列在Changes to be committed后面的改动都位于index上。

Git index中的改动可以用git commit提交到本地仓库中。

#### Git working tree
也被称作Working directory，git add之前的文件改动都是在working tree中进行的，运行git status后，列在Changes not staged for commit和Untracked files后面的改动都位于working tree上。

## Git进阶使用场景

并不常见的使用场景。
### git reset
#### git reset --soft
既没修改index也没修改working tree，只是将当前HEAD指针放到ORIG_HEAD里，然后将HEAD指向目标Commit(默认为HEAD)。

如果要撤销`git reset --soft`，只需要使用`git reflog`找到最近的一次提交，然后对其再做一次reset即可，比如`git reset --soft HEAD@{0}`。

#### git reset --mixed
重置index，不修改working tree。通常用于将git add的改动移出index，不会修改文件内容。

#### git reset --hard
重置index和working tree，完全恢复到目标comit(默认是HEAD)的状态。所有未commit或stash的改动都会**丢失**，使用此命令需多加小心。

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
### git rev-list
按时间逆序列出提交对象，常用于查找涉及到某些文件的提交的hash。例如，查找所有关系到文件readme的提交：

    git rev-list HEAD -- readme

更多功能参考`man git-rev-list`。

### git add
git add默认情况下只更新新添加文件和修改过的文件的索引，对于不是用git rm删除的文件，会被忽略掉。可以使用`git add --all`选项来更新所有改动的索引。

> 'git add --ignore-removal <pathspec>', which is the current default, ignores paths you removed from your working tree.

> 'git add --all <pathspec>' will let you also record the removals.

### 检索日志和修改内容
检索提交消息

    git log --grep "hello world"

检索修改内容

    git log -S "hello world"

使用正则表达式检索修改内容

    git log -G "^hello world$"

## 阅读资料

*  [Git Tip of the Week: Detached Heads](http://alblue.bandlem.com/2011/08/git-tip-of-week-detached-heads.html)

