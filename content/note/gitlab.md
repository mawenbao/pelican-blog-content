Title: gitlab
Date: 2013-08-25 12:14
Tags: gitlab, git

# Gitlab安装、配置及错误解决

使用Gitlab在VPS上搭建私人Git仓库。
## 安装

官方的[安装指南](https///github.com/gitlabhq/gitlabhq/blob/stable/doc/installation.md)非常详尽，参照着执行即可。注意安装数据库之前一定修改数据库配置文件`config/database.yml`里的用户名和密码，不要用root用户。使用如下命令查看gitlab安装状态

    cd ~gitlab/gitlab
    sudo -u gitlab -H bundle exec rake gitlab:check RAILS_ENV=production

## 配置

### 子域

在DNS管理界面为gitlab加一条A记录，指向服务器的IP即可。
## 迁移数据库到Mysql

1. 导出现有数据。

	bundle exec rake db:data:dump RAILS_ENV=production

2. 修改数据库配置文件config/database.yml。

	# backup old database settings first
	cp config/database.yml config/database.yml.old
	cp config/database.yml.mysql config/database.yml

修改database.yml中mysql数据库的用户名和密码。

3. 创建数据库。

	bundle exec rake db:setup RAILS_ENV=production

4. 导入数据。

	bundle exec rake db:data:load RAILS_ENV=production

## 问题

### 修改工程的默认域名
使用默认设置新建的工程，域名都是localhost，修改gitlab/config/gitlab.yml，如下所示，将host改为需要的域名。

	# Git Hosting configuration
	git_host:
	...
	    host: gitlab.atime.me
	...
	web:
	    host: gitlab.atime.me

### 迁移到Mysql时无法找到mysql2 adapter

使用命令`bundle exec rake db:data:load RAILS_ENV=production`初始化Mysql数据库时报以下错误:

	rake aborted!
	Please install the mysql2 adapter: `gem install activerecord-mysql2-adapter` (mysql2 is not part of the bundle. Add it to Gemfile.)

按照提示安装`activerecord-mysql2-adapter`后依然报同样的错误。修改gitlab的Gemfile($GitlabRoot/Gemfile)，找到如下一句:

	gem "mysql2", :group => :mysql

将其修改为
	
	gem "mysql2", :group => :production

若依然无效，添加如下一行即可。
	
	gem 'mysql2'

### sshd端口不是22

若sshd的端口不是22，则会遇到如下错误:

    ssh: connect to host localhost port 22: Connection refused

此时，在/home/gitlab/.ssh/config文件中加入如下内容即可。

    Host localhost
    Port 59581

### 查看文件源码时出现500错误

pygments需要python2.6或python2.7，如果安装了python2.6或python2.7后依然出现该错误，则可能是因为pygments无法找到python2，执行如下命令即可解决，参考[Error 500 while trying to see source file](https///github.com/gitlabhq/gitlabhq/issues/1774)。

    ln -s /usr/bin/python2.6 /usr/bin/python2

## 参考资料

*  [gitlab官方安装指南](https///github.com/gitlabhq/gitlabhq/blob/stable/doc/installation.md)
*  [Create subdomain and set it up](http://forum.linode.com/viewtopic.php?t=8004%3E) (for linode dns manager)
*  [Migrating to mysql](http://blog.gitlabhq.com/migrating-to-mysql/)  
*  [rake dbmigrate error](http://stackoverflow.com/questions/8408936/rake-dbmigrate-error)(on stackoverflow)
*  [Error 500 while trying to see source file](https///github.com/gitlabhq/gitlabhq/issues/1774)

