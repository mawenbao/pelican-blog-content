Title: Git配置文件介绍和举例
Date: 2013-08-25 12:14
Update: 2014-05-17 13:27
Tags: git, config

收集常用的Git配置。

## 配置文件介绍

Git的配置文件分为系统级别(system)、用户级别(global)和仓库级别三个，详细内容可参考man git-config。
### /etc/gitconfig
系统级别的git配置文件，对系统上的所有用户和所有代码仓库都有效，可被用户级别(~/.gitconfig)和仓库级别(.git/config)的配置文件覆盖。

使用`git config --system ...` 命令可以修改该配置。

### ~/.gitconfig

用户级别的git配置文件，对该用户的所有代码仓库都有效，可被仓库级别的配置文件(.git/config)覆盖。

使用`git config --global ...` 命令可以直接修改该配置。

### $repo/.git/config

仓库级别的git配置文件，仅对当前代码仓库($repo)有效，但是可覆盖定义在/etc/gitconfig和~/.gitconfig里的配置。

`git config ...` 命令默认修改此配置文件，如果想使用另外的路径存储配置文件可以为git confi命令使用'-f/--file'选项。

### .gitmodules

配置git仓库的子模块。可参考[这里](https://www.kernel.org/pub/software/scm/git/docs/gitmodules.html).

## 常用配置项
### http代理
    git config http.proxy 'http://localhost:8087'
    git config http.proxy 'socks5://localhost:8088'

### alias
git config中的alias可以像bash的内置命令alias一样为常用的很长的命令分配一个别名，比如

    git config alias.lsm "ls-files -m"

然后使用`git lsm`即相当于`git ls-files -m`的效果。

另外如果alias的命令开头带叹号`!`，则表示后面的命令将被视为shell命令[^1]，例如

    git config alias.lsm '!git ls-files -m'

效果和之前一样，需要注意的是为防止shell解释叹号，命令左右要用单引号。

## 配置文件举例

以我的用户级git配置文件和全局ignore文件为例。
### 我的~/.gitconfig

	# user info
	git config --global user.name = me
	git config --global user.email = me@my.com
	# core settings
	git config --global diff.tool vimdiff
	git config --global core.editor = vim
	git cofnig --global core.excludesfile ~/.gitignore
	# alias
	git config --global alias.br branch
	git config --global alias.co checkout
	git config --global alias.df difftool
	git config --global alias mg merge
	git config --global alias.st status
	git config --global alias.last "log --pretty=oneline -1 HEAD"
	git config --global alias.glog "log --graph --date=short --pretty=tformat:'%ad %h %s'"
	git config --global alias.unstage "reset HEAD"
	

### 我的~/.gitgnore

用于忽略部分文件，用户级别的ignore文件位于~/.gitignore，仓库级别的ignore文件位于$repo/.gitignore。详情请参考`man 5 gitignore`。

	
	# Backup files
	*~
	 
	# Version control
	.svn*
	
	# Compiled source
	*.com
	*.class
	*.dll
	*.exe
	*.o
	*.so
	*.py[co]
	*.egg-info
	nbproject/
	
	# Archives
	*.7z
	*.dmg
	*.gz
	*.iso
	*.jar
	*.rar
	*.tar
	*.zip
	
	# OS generated files
	.DS_Store
	.DS_Store?

## 其他相关的设置
### 使用ssh传输协议

    git clone ssh://name@host/absolute/path/to/repo
    git clone name@host:/path/to/repo

如果ssh的端口不是默认的22或者需要定义单独的密钥位置，则需要修改ssh的配置文件`~/.ssh/config`，详情可参考[ssh配置](/note/debian_ubuntu-tricks.html#81b946c715e023cc04458d7aeae15546)。

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

## 阅读资料

*  [Ignoring files from github](https://help.github.com/articles/ignoring-files)
*  [yyfrankyy's git config](http://f2e.us/wiki/git-config.html#!/)

[^1]: 参考`man git config`的Variables部分`alias.*`的说明，引用于2014-05-13。

