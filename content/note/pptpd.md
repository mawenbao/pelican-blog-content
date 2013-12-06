Title: 使用pptpd搭建VPN
Date: 2013-08-25 12:14
Update: 2013-12-06 13:08
Tags: pptpd, vpn

pptpd存在安全隐患，详情可参考[这里](http://pptpclient.sourceforge.net/protocol-security.phtml)。

介绍在debian squeeze上使用pptpd搭建vpn的方法。
## 安装并配置pptpd

安装pptpd

    apt-get install pptpd

修改pptpd的配置文件`/etc/pptpd.conf`，将以下两行的注释符`#`去掉:

    localip 192.168.0.1
    remoteip 192.168.0.234-238,192.168.0.245

## 修改PPPD DNS配置

在`/etc/ppp/options`添加Google的Public DNS:

    ms-dns 8.8.8.8
    ms-dns 8.8.4.4

可以使用`man pppd`查看pppd及其配置文件的用户手册。

## 修改日志输出位置
pptpd默认将日志写入`/var/log/syslog`系统日志，在`/etc/ppp/options`里加入如下一行启用单独的日志。

    logfile /var/log/pptpd.log

## 修改连接数
pptpd的默认配置只有6个IP可供分配，pptpd启动时日志里经常见到如下的警告信息。

    Maximum of 100 connections reduced to 6, not enough IP addresses given

如果想要增加更多的连接，可修改`/etc/pptpd.conf`的`remoteip`选项。

    remoteip 192.168.0.234-248,192.168.0.245

上面的配置将连接数增加到16个，需要注意的是，连接数同时受`remoteip`和`connections`两个配置项控制，详情可参考`man pptpd.conf`。

## 设置VPN用户名和密码

假设用户名为`xiaoming`，密码为`123`(不要设置过于简单的密码)，则在`/etc/ppp/chap-secrets`添加如下一行:

    xiaoming pptpd 123 *

上面的`*`表示任何ip均可访问你的vpn，也可以改为自己的一些ip，ip之间用逗号或空格隔开。

## 设置iptables规则

首先配置nat表的翻译规则, 将目标IP为192.168.0.0/24的包转向eth0接口. 在[iptables配置文件](/tips/server_security#iptables)的nat表中添加如下规则:
	
	-A POSTROUTING -s 192.168.0.0/24 -o eth0 -j MASQUERADE

若配置文件中还没有nat表的配置, 添加如下规则:

	*nat
	-A POSTROUTING -s 192.168.0.0/24 -o eth0 -j MASQUERADE
	COMMIT

然后配置filter表的规则, 在合适的位置((比如在`-A INPUT -j DROP`这种规则的前面))添加如下内容:

	
	-A FORWARD -s 192.168.0.0/24 -j ACCEPT
	-A FORWARD -d 192.168.0.0/24 -j ACCEPT

最后运行iptables-restore命令导入以上配置文件即可. 如果使用以上规则后无法连接成功，则在合适的位置添加如下规则:

	
	-A INPUT -p tcp --dport 1723 -m state --state NEW -j ACCEPT

上面的规则允许使用tcp协议建立到1723端口的连接。pptpd默认监听1723端口，可以使用如下命令查看:

    sudo netstat -nap | grep pptpd

## 修改sysctl.conf

修改`/etc/sysctl.conf`，去掉下面一句前面的注释符`#`:

    net.ipv4.ip_forward=1

重新加载sysctl.conf:

    sysctl -p

## 重启pptpd服务

    service pptpd restart
    service pppd-dns restart

## 遇到问题?

### 无法连接或连接后无法解析DNS
经过以上设置后，如果依然无法成功连接到VPN服务器，或者连接成后却无法正常访问网络。出现类似`DNS 查找失败`的错误，首先检查你的iptables规则，如果没有问题可以先停掉pptpd服务:

    service stop pptpd

修改pptpd的配置文件`/etc/ppp/options`，开启debug输出。然后运行`pptpd -f`，这时候再从客户端连接，根据`pptpd -f`的输出信息解决问题。

也可查看pppd的日志，默认情况下，pptpd将日志记录于系统日志`/var/log/syslog.*`。

### ppp0: compressor dropped pkt

貌似不能算错，在日志里看到很多这样的信息。Google一番后发现[这里](http://comments.gmane.org/gmane.linux.ppp/1594)的解答比较靠谱，但是要修改pppd的源码并重新编译，所以没有实际测试。问题出在:
> PPPD reduces the MTU of the interface, because MPPE encryption needs
> additional 4 bytes. Windows clients do not see if that way, however.
> This leads to problems, because the Windows client sends a TCP MSS
> of 4 bytes too large for PPPD.
> What you can do is change the PPPD, so that it does not reduce the MTU anymore.
> See the patch below.
> 
> Alternatively, set the MTU of the PPP interface in the ip-up script.

解决方法是给pppd源码打patch:

    :::diff
	--- sources/p/pppd/pppd/ccp.c	2004/01/16 09:47:28	1.1.1.1
	+++ sources/p/pppd/pppd/ccp.c	2004/10/15 15:08:50	1.1.1.1.4.1
	@@ -1191,7 +1191,12 @@

	  		     */
	  		    mtu = netif_get_mtu(f->unit);
	  		    if (mtu)
	-			netif_set_mtu(f->unit, mtu - MPPE_PAD);
	+		    {
	+			// Removed the lowering of the MTU, because it causes
	+			// problems with routing (TCP/MSS: Windows clients
	+			// do not care about this reduced packet size)
	+			//netif_set_mtu(f->unit, mtu - MPPE_PAD);
	+		    }
	  		    else
	  			newret = CONFREJ;
	  		}

### Virtualbox上的系统无法使用pptp vpn

Virtualbox的NAT实现不支持GRE协议，解决方案可参考[PPTP VPN connections from VirtualBox guests](http://angryfifer.blogspot.com/2012/03/pptp-vpn-connections-from-virtualbox.html)

## 参考资料

*  [Debian、Ubuntu下pptpd的架设方法](http://popu.org/post_5.html)
*  [debian下设置pptpd](http://liuzuhuijunlian.blog.163.com/blog/static/72489767201111233410835/)
*  [PPTP Server Configuration](http://www.dd-wrt.com/wiki/index.php/PPTP_Server_Configuration)
*  [PPTP and iptables problem](http://blog.gmane.org/gmane.network.poptop/page=15)
*  [ppp_mppe osize issue](http://comments.gmane.org/gmane.linux.ppp/1594) for error "compressor dropped pkt"
*  [pptp client diagnosis howto](http://pptpclient.sourceforge.net/howto-diagnosis.phtml)

