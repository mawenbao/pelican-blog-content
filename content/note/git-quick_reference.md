Title: Git快速使用指南
Date: 2013-08-25 12:14
Update: 2014-01-21 16:46
Tags: git, 教程

阅读“[Pro Git](http://git-scm.com/book)“后写的笔记，当做速查手册(quick git reference)来用，以供日常查阅。常见的git错误和解决方案可参考[git问题整理](/tools/git/errors)。

使用git的时候，不管出现什么问题，只要修改被commit了，你所要做的就是:

<img alt="Keep calm and use git reflog" width="200px" src="/static/images/note/keep-calm-and-use-git-reflog.png">

(图片取自[
KEEP CALM AND USE GIT REFLOG](http://www.keepcalm-o-matic.co.uk/p/keep-calm-and-use-git-reflog/))

## 特殊符号

详细内容可参考gitglossary的man页。

    man 7 gitglossary

或直接查看[这里](http://linux.die.net/man/7/gitglossary)。

    HEAD      # the commit at the tip of a branch
    HEAD^     # first parent of HEAD
    HEAD~2    # second parent of HEAD
    HEAD^^    # first parent of HEAD^ 
    HEAD~3    # first parent of HEAD^^(HEAD~2)
    HEAD~3^2  # second parent of HEAD^^
    
    ORIG_HEAD # previous state of HEAD, equivalent to HEAD@{1}
    
    origin    # default upstream repository
    master    # default development branch

## 常见的使用场景

介绍git的常用场景。
###  克隆远程仓库 

    git clone https://github.com/git/git.git
    git log --stat

### 创建新的仓库

    git init
    git add .
    git status
    git commit -m "first commit"
    git remote add origin https://github.com/your/git/repo.git
    git push -u origin master

### 查看改动内容

 | A | git commit | B | git add | C | 
 | - | ---------- | - | ------- | - | 

以上面的图为例进行说明，A表示最后一次提交的版本，B表示最后一次追踪或暂存(stage，使用git add命令)后的版本，C表示尚未加入追踪的版本。

比较尚未追踪的文件改动和已追踪的版本，即比较C和B。

    git diff

比较尚未提交但已追踪的文件改动和已提交的版本，即比较B和A。

    git diff --cached

或

    git diff --staged

### 取消文件跟踪或修改

如果想停止追踪已提交的文件，可以使用如下命令。下面的命令仅将文件从暂存里移除，不会删除文件。

    git rm --cached file1 file2 ...

对于尚未提交的文件，也可以用git reset将文件恢复到某次提交时的状态。下面的命令仅将文件的修改从暂存里移除，不会影响到实际的文件内容。

    git reset HEAD file1 file2 ...

也可使用如下命令取消文件修改，不过提交之后的所有修改内容(包括暂存的修改内容)都会丢失且**不可恢复**。

    git checkout HEAD -- file1 file2 ...

若想丢弃(不可恢复)提交后暂存的修改，可用如下命令。尚未用git add加入暂存的修改不会受影响。

    git reset HEAD --hard

### 提交更改

    git add .
    git status
    git commit -am "commit message"
    git pull
    git push origin master

### 修改最后一次提交

仅修改**本地**的提交。

    git commit --amend

### 查看上一次提交的文件path/to/file

    git show HEAD^:path/to/file

## 命令详解

### git-tag

查看man页获取详细信息。

    man git-tag

查看所有标签。

    git tag

使用模式匹配查找标签。

    git tag -l 'v1.*'

创建annotated标签。

    git tag -a v1.0 -m "version 1.0"

查看刚刚添加的标签。

    git show v1.0

创建使用gpg签署的标签。

    git tag -s v1.5 -m "version 1.5, signed tag"

验证被签署的标签，需要有签署者的公钥。

    git tag -v v1.5 

为之前的某次提交创建标签，假设该次提交的校验和是9fceb02d0ae598e95dc970b74767f19372d61af8。

    git tag -a v2.0 -m "version 2.0, previous commit" 9fceb02d0ae598e95dc970b74767f19372d61af8

把某个标签推送到远程服务器上。

    git push origin v2.0

把所有标签都推送到远程服务器上。

    git push origin --tags

### git-branch

查看man页获取详细信息。

    man git-branch

查看所有分支，以星号(*)开头的分支为当前分支。

    git branch -v

新建并切换到某一分支。

    git branch issue20
    git checkout issue20

或

    git branch -b issue20

分支合并，将issue20分支并入master分支。

    git checkout master
    git merge issue20

删除无用的分支。

    git branch -d issue20

强制删除未合并的分支。

    git branch -D issue21

分支合并时遇到冲突，可参考[这里](http://git-scm.com/book/zh/Git-%E5%88%86%E6%94%AF-%E5%88%86%E6%94%AF%E7%9A%84%E6%96%B0%E5%BB%BA%E4%B8%8E%E5%90%88%E5%B9%B6#遇到冲突时的分支合并)的方法解决冲突后再合并。

查看已合并到当前分支的分支，通常而言，未用星号(*)标识的分支均可被删除。。

    git branch --merged

查看尚未合并的分支。

    git branch --no-merged 

删除远程分支

    git push origin :branch-name

### git-bundle

查看man页获取以详细信息。

    man git-bundle

bundle命令可以对git仓库进行打包，如下所示。

    cd hello-world.git
    git bundle create hello-world.bundle --all

验证打包文件

    git bundle verify hello-world.bundle

打包文件解包

    git clone hello-world.bundle

### git-log

控制git-log输出格式的选项:

	选项             说明
	-p               按补丁格式显示每个更新之间的差异。
	--stat           显示每次更新的文件修改统计信息。
	--shortstat      只显示 --stat 中最后的行数修改添加移除统计。
	--name-only      仅在提交信息后显示已修改的文件清单。
	--name-status    显示新增、修改、删除的文件清单。
	--abbrev-commit  仅显示 SHA-1 的前几个字符，而非所有的 40 个字符。
	--relative-date  使用较短的相对时间显示（比如，“2 weeks ago”）。
	--graph          显示 ASCII 图形表示的分支合并历史。
	--pretty         使用其他格式显示历史提交信息。可用的选项包括 oneline，short，full，fuller 和 format（后跟指定格式）。

控制git-log输出范围的选项，可与以上选项同时使用:

	选项               说明
	-(n)               仅显示最近的 n 条提交
	--since, --after   仅显示指定时间之后的提交。
	--until, --before  仅显示指定时间之前的提交。
	--author           仅显示指定作者相关的提交。
	--committer        仅显示指定提交者相关的提交。

输出日志仅限于影响到某些文件的提交，下面的命令仅输出修改LICENSE或README的提交的日志。

    git log -- LICENSE README

### git-reflog
记录了HEAD指针的完整改动历史，通常用于于查找“丢失”的commit和跨分支查看提交历史。当因为某些操作导致某些commit“丢失”时，可以使用`git reflog`配合`git reset --hard`来恢复到之前的提交状态。

### git-remote

使用man查看详细内容。

    man git-retmote

查看所有的远程仓库。

    git remote -v

查看某个远程仓库(short-name为其别名)的详细内容。

    git remote show [short-name]

修改远程仓库的别名(short-name)。

    git remote rename [short-name] [short-name]

删除远程仓库(short-name为其别名)。

    git remote rm [short-name]
    
### git-stash

使用man查看详细内容。

    man git-stash

### git-rebase

修改commit历史

### git-cherry-pick
通常用于将其他分支的提交rebase到当前分支上。

### git-bitsect

二分查找commit历史

### git-blame

查看每一行的具体修改时间和修改人员。

### git-update-index

更新git索引

### git-ls-files

列出文件
	
	-c, --cached
	Show cached files in the output (default)
	
	-d, --deleted
	Show deleted files in the output
	
	-m, --modified
	Show modified files in the output
	
	-o, --others
	Show other (i.e. untracked) files in the output

使用ls-files和update-index来更新git索引

    git ls-files -d -m -o -z | xargs -0 git update-index --add --remove

## Git技巧

一些git的小技巧。

### 自动补全

git的代码仓库里有针对shell和bash等unix shell的命令行补全脚本，使用后会提高不少工作效率，可以从[这里](https://github.com/git/git/tree/master/contrib/completion)下载。

以bash为例，依次执行以下命令即可。

    wget -O ~/.git-completion.bash https://raw.github.com/git/git/master/contrib/completion/git-completion.bash
    echo "source ~/.git-completion.bash" >> ~/.bashrc
    source ~/.bashrc

### 命令别名

对于使用频率较高的git命令，可以为其创建短小的别名。可以参考[这里](http://git-scm.com/book/zh/Git-%E5%9F%BA%E7%A1%80-%E6%8A%80%E5%B7%A7%E5%92%8C%E7%AA%8D%E9%97%A8#Git-命令别名)和[我的git配置](/tools/git/config#我的gitconfig)里的alias部分。

### 使用ssh协议访问远程仓库

使用ssh协议访问远程仓库时，如果仓库所在服务器的sshd端口号不是默认的22的话，git将无法访问。解决方法是，在~/.ssh/config里修改服务器的port。

    Host ip_or_host_name_of_target_server
    Port sshd_port_number
    
比如，

    Host github.com
    Port 22
    Host *
    Port 1234

### 忽略某些文件

可参考[我的Ignore](/tools/git/config#我的gitgnore)文件。
### 提交范围

可参考[Commit Ranges](http://git-scm.com/book/ch6-1.html#Commit-Ranges)。

通常用于git log和git diff，主要有两种格式:

*  double dot ..
*  triple dot ...

## Git进阶教程

更多内容可参考[这里](/note/git-advanced_tutorial.html)。

## 阅读资料

*  [The Pro Git Book](http://git-scm.com/book/zh/)
*  [Git user manual](http://www.kernel.org/pub/software/scm/git/docs/user-manual.html)
*  [gitglossary(7)](http://linux.die.net/man/7/gitglossary)
*  [git-tag(1)](http://linux.die.net/man/1/git-tag)
*  [git-branch(1)](http://linux.die.net/man/1/git-branch)
*  [git-bundle(1)](http://linux.die.net/man/1/git-bundle)
*  [git-remote(1)](http://linux.die.net/man/1/git-remote)
*  [Specify ssh port for git](http://serverfault.com/questions/218256/specify-ssh-port-for-git)
    
