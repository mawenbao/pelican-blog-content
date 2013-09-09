Title: Linux服务器常见错误
Date: 2013-08-08 12:14
Tags: linux_server, problem


记录Linux服务器上常见的错误和解决方案，安装和配置参考[这里](/tips/build_linux_host)。
## 系统管理相关

### grep: line too long
使用grep的时候遇到下面的错误:

    grep: line too long

参考[stackoverflow](http://stackoverflow.com/questions/3657236/grep-line-too-long-error-message)上的方法解决，即使用find命令查找出的文件作为grep的输入，比如查找`/etc`下

    find /etc -type f -print0 | xargs -r0 grep -E '<([0-9]{1,3}\.){3}[0-9]{1,3}\>'

如果以上方法无效，给grep添加`-I`选项(忽略二进制文件)后再尝试一下。
### exim4 25端口被占用

在exim4的错误日志/var/log/exim4/paniclog中发现如下信息:
	
	socket bind() to port 25 for address 127.0.0.1 failed
	...

表示25端口已被占用，先使用`service exim4 stop`停止exim4服务，再使用`nmap 127.0.0.1`查看端口占用情况，输出如下所示:

	Starting Nmap 5.00 ( http://nmap.org ) at 2012-11-28 09:32 CST
	Interesting ports on localhost (127.0.0.1):
	Not shown: 992 closed ports
	PORT     STATE SERVICE
	22/tcp   open  ssh
	25/tcp   open  smtp
	80/tcp   open  http
	111/tcp  open  rpcbind
	443/tcp  open  https
	587/tcp  open  submission
	3306/tcp open  mysql
	9000/tcp open  cslistener
	
	Nmap done: 1 IP address (1 host up) scanned in 0.23 seconds

发现25端口被smtp服务占用，估计是之前的sendmail卸载出了问题。使用`netstat -apn | grep 25`命令查看占用25端口的进程情况，
输出如下所示:
	
	tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN      29229/sendmail: MTA
	tcp        0     52 173.230.150.224:22      116.236.230.250:3505    ESTABLISHED 19238/0         
	tcp        0      0 173.230.150.224:22      116.236.230.250:15840   ESTABLISHED 15727/sshd: bgfw [p
	unix  11     [ ]         DGRAM                    2543     1747/rsyslogd       /dev/log
	unix  2      [ ]         DGRAM                    111257   29229/sendmail: MTA 
	unix  3      [ ]         STREAM     CONNECTED     170425   19564/nginx.conf    

确认是pid为29229的sendmail占用了25端口，使用`kill 29229`结束sendmail进程。使用`dpkg -l | grep sendmail`查看sendmail的安装情况，输出如下:
	
	rc  sendmail-base          8.14.3-9.4            powerful, efficient, and scalable Mail Transport Agent
	rc  sendmail-bin           8.14.3-9.4            powerful, efficient, and scalable Mail Transport Agent
	rc  sendmail-cf            8.14.3-9.4            powerful, efficient, and scalable Mail

表示sendmail*已被删除，但是仍保留配置文件。如果想删除sendmail的配置文件，使用`apt-get purge sendmail*`即可。最后使用`service exim4 start`启动exim4服务。

## nginx相关

这里收集与nginx相关的错误和解决方案。

### 访问软链接文件提示403 Forbidden

访问使用ln -s命令建立的软链接文件提示403 Forbidden错误，而链接原文件的权限为644，貌似没有问题。我的服务器用户为www-data，软链接文件为link-file，使用`sudo -u www-data vi link-file`后，无法读取该文件，vim提示Permission Denied错误。

Google一番后，在[这里](http://unix.stackexchange.com/questions/20993/symbolic-link-not-allowed-or-link-target-not-accessible-apache-on-centos-6)找到了答案，原来www-data用户无法访问链接文件的某些父目录，修改其权限(为www-data用户添加执行权限)后再访问该链接文件，错误消失。

### 访问php页面提示An Error Occurred

采用了[这里](/tips/build_linux_host#安装和配置nginx)的安装和配置方法，访问php页面的时候出现下述错误:
	
	An error occurred.
	
	Sorry, the page you are looking for is currently unavailable.
	Please try again later.
	
	If you are the system administrator of this resource then you should check the error log for details.
	
	Faithfully yours, nginx.

最常见的原因是php-fastcgi或php5-fpm服务没有正常运行，使用`service php-fastcgi start`启动php-fastcgi或`service php5-fpm restart`启动php5-fpm后恢复正常。

## php相关

### php5-fpm和eaccelerator冲突
为了优化php，我在服务器上安装了php5-apc和eaccelerator，并使用php5-fpm管理fastcgi进程，我的wordpress博客使用w3 total cache进行缓存管理和优化，而w3 total cache使用php5-apc缓存php中间代码。问题发生在某次修改w3 total cache的配置时，博客突然就无法访问了，然而访问同一服务器下的dokuwiki时却十分正常。查看了相关的日志后发现如下信息。

php5-fpm日志中连续报child exited on signal 11'这样的错, 如下所示:
	
	[07-Dec-2012 08:54:02] NOTICE: [pool www] child 15696 started
	[07-Dec-2012 08:54:02] WARNING: [pool www] child 15688 exited on signal 11 (SIGSEGV) after 3.914094 seconds 

从而导致nginx报错'recv() failed (104: Connection reset by peer)', 如下:
	
	2012/12/06 19:08:26 [error] 7944#0: *160 recv() failed (104: Connection reset by peer) while reading response    header from upstream, client: 116.232.98.129, server: blog.atime.me, request: "GET /about/ HTTP/1.1", upstream:  "fastcgi://127.0.0.1:9000", host: "blog.atime.me", referrer: "http://blog.atime.me/archives/"

暂时没找到问题原因。解决方案分两种:

 1.  将php5-fpm换回spwan-fcgi。
 2.  将php5-fpm的php配置中所有关于eaccelerator的内容删掉后再重启服务。

### php5-fpm启动时报错segment fault: pthread.so ...

重启服务器后，php5-fpm报错segment fault，并启动失败。原因是apc.ini配置文件有错，apc.ini中定义的php-apc文件夹不存在导致。

    apc.mmap_file_mask=/tmp/php-apc/apc.XXXXXX

创建/tmp/php-apc文件夹后，php5-fpm启动正常。

### Class 'PMA_Message' not found

使用nginx配合php5-fpm解析php文件，某次登录phpmyadmin的时候，输入密码正确但无法进入，始终停留在登录页面。查看nginx日志发现如下错误信息:
	
	PHP message: PHP Notice:  Undefined property: PMA_Error...
	PHP message: PHP Fatal error:  Class 'PMA_Message' not found in...

经查后发现是php session目录不存在(或权限不对)所致，重新创建php session目录并为www-data用户分配权限后问题解决。

## 参考资料

*  [socket bind() to port 25 for address 146.232.128.43 failed](http://www.exim.org/lurker/message/20030730.105421.ee14dd63.en.html) from exim4 mail list
*  [grep line too long error message](http://stackoverflow.com/questions/3657236/grep-line-too-long-error-message) from StackOverflow
*  [Symbolic link not allowed or link target not accessible](http://unix.stackexchange.com/questions/20993/symbolic-link-not-allowed-or-link-target-not-accessible-apache-on-centos-6) from StackExchange

