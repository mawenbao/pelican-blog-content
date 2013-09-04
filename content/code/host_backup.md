Title: host backup script
Date: 2013-08-08 12:14
Tags: python, backup

# Host Backup 网站备份脚本

使用python脚本进行网站备份和恢复，可以通过配置文件自定义备份选项。仅支持linux系统和mysql数据库，在debian6上测试和使用。

*  当前版本: 0.0.3
*  最后更新: 2012.11.27
*  许可协议: [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html)
*  代码仓库: [Github](https///github.com/wilbur-ma/host-backup)
*  下载地址: [最新版本](https///github.com/wilbur-ma/host-backup/archive/master.zip)
## 介绍

### 更新历史

*  0.0.3    2012.11.27    增加dropbox支持(需要[dropbox sdk](https///www.dropbox.com/developers/reference/sdk))
*  0.0.2    2012.11.02    增加发送邮件功能
*  0.0.1    2012.10.26    第一个测试版本

### 依赖的软件

*  python2.6或python2.7
*  gnu tar - 文件打包
*  mysqldump, mysqlshow - 备份数据库和验证数据库密码
*  exim4, mutt - 通过邮件发送备份数据
*  [dropbox sdk](https///www.dropbox.com/developers/reference/sdk) (如果使用dropbox备份功能)
### 文件列表

*  [backup-config.ini](#backup-config.ini) 备份和恢复的配置文件
*  host-admin.py 用于备份和恢复
*  aes.py aes加密和解密，取自[slowaes工程](http://code.google.com/p/slowaes/)
### 注意事项

 1.  在debian上，备份/etc/mysql时必须同时备份mysql数据库中的mysql，否则恢复后会有`Stopping MySQL database server: mysqld failed`错误，解决方法可以参考[这里](tools/mysql/errors#stopping_mysql_database_servermysqld_failed错误)。
 2.  如果用exim4发送邮件时因为附件太大而发送失败，可以在/etc/exim4/update-exim4.conf.conf添加如下一行`MESSAGE_SIZE_LIMIT=1000m`，将1000m改为你需要的大小限制即可。
### 使用说明

 1.  安装依赖的软件。
 2.  为脚本添加执行权限`chmod +x host-admin.py`。
 3.  根据需要修改配置文件。
 4.  进行备份或恢复: 

    * `./host-admin.py -c daily-backup.ini -b` 使用daily-backup.ini中的配置进行备份，备份时会连同配置文件一起打包。
    * `./host-admin.py -c daily-backup.ini -f host-backup.tar -r`使用daily-backup.ini中的配置和host-backup.tar中的数据进行恢复。可以直接使用host-backup.tar中的配置文件daily-backup.ini。
## 配置文件说明

### backup-config.ini

 1.  第一次使用需要按提示设置mysql密码，加密后存于配置文件中。
 2.  如果想使用新的Mysql用户或密码，只需将DB.Mysql里的User和Passwor的值设为0。
 3.  FileList里的路径必须为绝对路径，多个路径必须使用分号`:`隔开。
 4.  OwnerList使用chown修改FileList中对应项的用户归属，其中项的名称必须和FileList中的名称一致。按照下面的配置文件恢复文件后，将FileList中Dokuwiki_Data项所包含的所有路径的归属用户和归属组改为www-data，即`chown www-data:www-data %path%`。
 5.  将Mail_List设为0可禁用邮件发送功能。多个邮件地址可用分号":"隔开。
 6.  Exclude_VCS使用gnu tar的`--exclude-vcs`选项实现。
 7.  Exclude_Pattern使用gnu tar的`--exclude`选项实现，多个pattern使用分号":"隔开，例如剔除后缀为tmp的文件，/var/blog/tmp目录，名为conf.d的目录和所有隐藏文件(文件夹)，可以使用如下pattern: `*.tmp:/var/blog/tmp:conf.d:\.*`，单个Pattern的详细说明请参考[GNU Tar文档](http://www.gnu.org/software/tar/manual/html_node/exclude.html)。

<code>

    [OwnerList]
    dokuwiki_data = www-data:www-data
    gitlab_config = gitlab:gitlab

    [FileList]
    vim_config = /root/.vimrc:/root/.vim_runtime
    system_config = /etc/nginx:/etc/apache2:/etc/phpmyadmin:/etc/mysql:/etc/exim4
    crontab = /root/crontab
    gitlab_config = /home/gitlab/gitlab/config/database.yml:/home/gitlab/gitlab/config/gitlab.yml
    backup_script = /etc/cron.daily/host-backup
    git_config = /root/.gitconfig:/root/.gitignore
    dokuwiki_data = /var/www/wiki/data/pages:/var/www/wiki/data/meta:/var/www/wiki/data/attic:/var/www/wiki/conf

    [General]
    exclude_vcs = 0			# 备份[FileList]中的文件时，是否排除版本控制系统的文件，参考man tar。
    date_format = %Y%m%d%H%M%S	# 备份文件名的日期格式，参考python的日期格式。
    exclude_pattern = 0
    remove_after_backup = 1		# 备份完毕后是否删除备份文件， 1为删除，0为不删除。
    remove_exist_first = 1		# 恢复备份文件时，如果目标文件存在则先删除之，1为删除，0为不删除。

    [Repo.Git]
    root_dir = 0 			# 不启用Git仓库备份功能

    [DB.Mysql]
    db_list = 0			# 使用半角冒号(:)分隔的mysql数据库列表
    user = 0			# Mysql用户名
    password = 0			# Mysql密码

    [Backup]
    with_dropbox = 0		# 设为1则启用dropbox备份，0为不启用。
    with_email = 1			# 设为1则启用email备份，0为不启用。

    [Email]
    mail_list = 0			# 使用半角冒号(:)分隔的邮件列表

    [Dropbox]
    access_token = 0		# 不要手动填写
    target_dir = /host-backup	# dropbox的备份文件夹，/为根目录
    app_secret = 0			# 你的APP_SECRET
    app_key = 0			# 你的APP_KEY
    user = 0			# Dropbox用户名
    password = 0			# Dropbox密码，不要手动填写
</code>
