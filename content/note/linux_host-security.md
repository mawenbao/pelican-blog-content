Title: Linux服务器安全策略
Date: 2013-08-08 12:14
Update: 2013-10-30 14:17
Tags: linux_server, security

记录网站安全策略, 主要参考[Linode的文档](http://library.linode.com/securing-your-server)写成。
## 添加sudo用户

安装sudo

	apt-get install sudo

创建新用户并将其加入sudo组
	
	adduser your_user_name
	usermod -a -G sudo your_user_name

然后注销当前登录并使用新的用户名登录.

## ssh配置

### 生成Key
生成ssh公钥和密钥, 默认位于~/.ssh/
	
	ssh-keygen -C your_comment

`~/.ssh/authorized_keys`用于保存已验证的公钥, 因此必须确认~/.ssh文件夹和~/.ssh/authorized_keys文件不能被其他用户访问.

	chown -R your_user_name:your_user_name ~/.ssh
	chmod 700 ~/.ssh
	chmod 600 ~/.ssh/authorized_keys

将你的公钥添加到服务器的`~/.ssh/authorized_keys`中, 这样不用密码即可登录.

### 修改默认监听端口

假设新端口为7788，首先使用netstat命令查看该端口是否已被占用:

    sudo netstat -nap | grep 7788

若7788还未被使用，则修改`/etc/ssh/sshd_config`，将 `Port 22`改为`Port 7788` 重启ssh服务即可:

    sudo service ssh restart

最后记得为新的端口添加iptables规则，参考[#iptables](#iptables)，在`/etc/iptables.firewall.rules`中将 `-A INPUT -p tcp -m state --state NEW --dport 22 -j ACCEPT` 改为 `-A INPUT -p tcp -m state --state NEW --dport 59581 -j ACCEPT`
然后使用`iptables-restore < /etc/iptables.firewall.rules`导入新的规则。这样即可禁用22端口，并开启59581端口。

### 禁止使用密码登录，禁止root用户登录

修改`/etc/ssh/sshd_config`文件, 修改或添加如下几行:
	
	PasswordAuthentication no
	PermitRootLogin no

保存后重启ssh服务
	
	sudo service ssh restart 

## 日志监控

### denyhosts
denyhosts通过分析`/var/log/auth.log`来将某些非正常的ip添加到`/etc/hosts.deny`中，可通过如下命令安装。
	
	sudo apt-get install denyhosts

配置文件位于`/etc/denyhosts.conf`

### logwatch

logwatch分析系统日志, 并提取重要的信息发到你的邮箱里, 通过如下命令安装:

    sudo apt-get install logwatch 

拷贝配置文件

    sudo cp /usr/share/logwatch/default.conf/logwatch.conf /etc/logwatch/logwatch.conf

修改`/etc/logwatch/logwatch.conf`:

    Output = mail                # 发送邮件 
    Format = html                # 生成html格式的报告
    MailTo = your_email_address  # 定义你的邮箱地址

运行`logwatch`命令, 稍等片刻后检查是否收到logwatch的邮件. 如果一切正常则可以把logwatch添加到cron计划任务中让其自动运行. (debian6上logwatch默认自动加入cron任务, 检查`/etc/cron.daily/00logwatch`), 如果无法收到邮件, 请检查服务器的邮件发送配置, 可参考[这里](./build_linux_host#邮件设置)的相关配置.

## 防火墙

### 用Tcp Wrappers控制服务访问
使用logwatch后，经常发现某些ip会暴力猜解ssh密码，对某些烦人的IP，可以使用Tcp Wrappers限制其对某些服务的访问。

`/etc/hosts.allow`和`/etc/hosts.deny`两个文件用于控制远端对某些服务的访问，但必须注意的是，通常只有两类服务可以被`/etc/hosts.allow`和`/etc/hosts.deny`限制:

 1.  由tcpwrapper服务(tcpd)启动的服务，需要安装xinetd软件，并在`/etc/xinetd.conf`和`/etc/xinetd.d/*`进行相应的设置。
 2.  编译时即添加了libwrapper库支持的服务，使用`apt-cache rdepends libwrap0`查看所有内置支持librwapper的软件。

这里仅介绍第二类情况的配置方法，多数系统服务默认使用此种方法使用Tcp Wrappers。如果想查看某个服务是否内置支持libwrapper，则可以使用如下方法。以sshd为例，使用如下命令查看某个服务是否使用tcpwrappers库:
	
	ldd /usr/sbin/sshd | grep libwrap

如果输出结果包含`libwrap.so`或`libwrap.so.0`，则表示ssh使用了tcpwrappers库。

对于以上两种服务，我们可以用`/etc/hosts.deny`限制远程访问。`/etc/hosts.allow`和`/etc/hosts.deny`的语法，可以使用`man 5 hosts_access`和`man 5 hosts_options`查看，下面做简要介绍:
	
	<daemon list>:<client list>[:<option>:<option>:...]

其中

    ? daemon list 
    :逗号或空格(tab)分隔的服务列表，或ALL通配符。
    ? client list 
    :逗号或空格(tab)分隔的host或ip列表。
    ? option 
    : 其他选项。

所以，如果要禁止ip为x.x.x.x的用户访问所有服务，可以在`/etc/hosts.deny`里添加如下一行:
	
	ALL: x.x.x.x

需要注意的是，`/etc/hosts.allow`比`/etc/hosts.deny`拥有更高的优先级，即当两个文件里定义了同样的规则时，以`/etc/hosts.allow`为准。
### iptables

学习iptables配置的最好方法是阅读[iptables的文档](http://www.netfilter.org/documentation/).
#### 安装iptables-persistent软件包

安装iptables-persistent后, 将iptables配置文件放在`/etc/iptables/rules`即可实现开机自动导入iptables规则. 修改该配置文件后执行`service iptables-persistent start`即可使用iptables-restore重新加载`/etc/iptables/rules`.
#### 我的iptables配置文件

注意, 使用时需要将下面三行中的$PORT变量改为你的实际端口号:

	-A INPUT -p tcp --dport $YOUR_HTTP_PORT -j ACCEPT
	-A INPUT -p tcp --dport $YOUR_HTTPS_PORT -j ACCEPT
	-A INPUT -p tcp -m state --state NEW --dport $YOUR_SSHD_PORT -j ACCEPT

然后将下面一行中的$YOUR_IP改为你的IP地址:
	
	-A INPUT -s $YOUR_IP -j ACCEPT 

下面是我的`/etc/iptables/rules`:

    # filter表规则
    
    *filter
    #  Allow all loopback (lo0) traffic and drop all traffic to 127/8 that doesn't use lo0
    -A INPUT -i lo -j ACCEPT
    -A INPUT -d 127.0.0.0/8 -j REJECT

    #  Accept all established inbound connections
    -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

    #  Allow all outbound traffic - you can modify this to only allow certain traffic
    -A OUTPUT -j ACCEPT

    #  Allow HTTP and HTTPS connections from anywhere (the normal ports for websites and SSL).
    -A INPUT -p tcp --dport $YOUR_HTTP_PORT -j ACCEPT
    -A INPUT -p tcp --dport $YOUR_HTTPS_PORT -j ACCEPT

    #  Allow SSH connections
    #  The -dport number should be the same port number you set in sshd_config
    -A INPUT -p tcp -m state --state NEW --dport $YOUR_SSHD_PORT -j ACCEPT

    #  Allow ping
    -A INPUT -p icmp -j ACCEPT

    #  Log iptables denied calls
    -A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables denied: " --log-level 7

    # Allow to create new pptp connections
    -A INPUT -p tcp --dport 1723 -m state --state NEW -j ACCEPT

    # Enable forward for pptpd
    -A FORWARD -s 192.168.0.0/24 -j ACCEPT
    -A FORWARD -d 192.168.0.0/24 -j ACCEPT 

    # Allow input for my ips
    -A INPUT -s $YOUR_IP -j ACCEPT 

    #  Drop all other inbound - default deny unless explicitly allowed policy
    -A INPUT -j DROP
    -A FORWARD -j DROP 
    COMMIT

    # nat表规则

    *nat 
    # for pptpd

    -A POSTROUTING -s 192.168.0.0/24 -o eth0 -j MASQUERADE 
    COMMIT

#### unable to initialize table filter
安装`xtables-addons-common`即可。

## 阅读资料

*  [Securing your server](http://library.linode.com/securing-your-server) from linode documentation
*  [Control Network Traffic with iptables](http://library.linode.com/security/firewalls/iptables) from linode documentation  
*  [Securing debian howto](http://www.debian.org/doc/manuals/securing-debian-howto/ch4.en.html)
*  [Network Security with tcpwrappers (hosts.allow and hosts.deny)](http://ubuntu-tutorials.com/2007/09/02/network-security-with-tcpwrappers-hostsallow-and-hostsdeny/)
*  [Quick HOWTO : Ch14 : Linux Firewalls Using iptables](http://www.linuxhomenetworking.com/wiki/index.php/Quick_HOWTO_:_Ch14_:_Linux_Firewalls_Using_iptables)
*  [Debian iptables wiki](http://wiki.debian.org/iptables)
*  [Iptables docuemntation](http://www.netfilter.org/documentation/)

