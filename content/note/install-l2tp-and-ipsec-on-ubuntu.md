Title: 在Ubuntu12.04上安装l2tp/ipsec VPN服务器
Date: 2013-11-06 13:46
Tags: vpn, l2tp, ipsec, ubuntu

[1]: http://wangyan.org/blog/debian-l2tp-ipsec-vpn.html "http://wangyan.org/blog/debian-l2tp-ipsec-vpn.html"

记录我在Ubuntu服务器上安装l2tp/ipsec VPN的过程，以供日后查询。ipsec用于验证和加密数据包，由openswan提供；l2tp即第二层隧道协议，由xl2tpd提供。

## 安装相关软件

默认配置即可，后面另有详细介绍。

    sudo apt-get install openswan xl2tpd ppp

## 配置ipsec
注意三件事

1. 将`YOUR_SERVER_IP_ADDRESS`改为你的服务器的ip地址。
2. 将`YOUR_IPSEC_SHARED_KEY`改为你的ipsec共享密钥。
3. 注意配置文件的缩进。

### /etc/ipsec.conf

    sudo cat >/etc/ipsec.conf<<EOF
    version 2.0
     
    config setup
        nat_traversal=yes
        virtual_private=%v4:10.0.0.0/8,%v4:192.168.0.0/16,%v4:172.16.0.0/12
        oe=off
        protostack=netkey

    conn L2TP-PSK-NAT
        rightsubnet=vhost:%priv
        also=L2TP-PSK-noNAT

    conn L2TP-PSK-noNAT
        authby=secret
        pfs=no
        auto=add
        keyingtries=3
        rekey=no
        ikelifetime=8h
        keylife=1h
        type=transport
        left=YOUR_SERVER_IP_ADDRESS
        leftprotoport=17/1701
        right=%any
        rightprotoport=17/%any
    EOF

### /etc/ipsec.secrets

    sudo cat >/etc/ipsec.secrets<<EOF
    YOUR_SERVER_IP_ADDRESS %any: PSK "YOUR_IPSEC_SHARED_KEY"
    EOF

### 重启并检查ipsec配置

    sudo service ipsec restart
    sudo ipsec verify

输出没有FAILED项即可，WARNING可以不管。

## 配置xl2tpd
### /etc/xl2tpd/xl2tpd.conf

    sudo cat >/etc/xl2tpd/xl2tpd.conf<<EOF
    [global]
    ipsec saref = yes
 
    [lns default]
    local ip = 10.10.11.1
    ip range = 10.10.11.2-10.10.11.245
    refuse chap = yes
    refuse pap = yes
    require authentication = yes
    pppoptfile = /etc/ppp/xl2tpd-options
    length bit = yes
    EOF

### /etc/ppp/xl2tpd-options

    sudo cat >/etc/ppp/xl2tpd-options<<EOF
    require-mschap-v2
    ms-dns 8.8.8.8
    ms-dns 8.8.4.4
    asyncmap 0
    auth
    crtscts
    lock
    hide-password
    modem
    name l2tpd
    proxyarp
    lcp-echo-interval 30
    lcp-echo-failure 4
    EOF

## 添加ppp用户和密码
将USER和PASSWORD改为你的用户名和密码即可。

    sudo cat >>/etc/ppp/chap-secrets<<EOF
    USER * PASSWORD *
    EOF

## 配置数据包转发
### 调整系统配置

    for each in /proc/sys/net/ipv4/conf/*
    do
        echo 0 > $each/accept_redirects
        echo 0 > $each/send_redirects
    done

    sed -i 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/g' /etc/sysctl.conf
    sysctl -p

### 配置iptables规则
尚未验证

    iptables -t nat -A POSTROUTING -j MASQUERADE
    iptables -I FORWARD -p tcp --syn -i ppp+ -j TCPMSS --set-mss 1356

## 重启xl2tpd服务器

    service xl2tpd restart

## 错误检查

### 查看日志

*  ipsec的认证日志默认输出到`/var/log/auth.log`，如果建立vpn连接后看到`IPsec SA established transport mode`即表示认证成功。
*  xl2tpd的日志默认输出到`/var/log/syslog`，可以在`/etc/ppp/xl2tpd-options`配置里添加`debug`（重启xl2tpd)来查看更详细的日志。

### xl2tpd非daemon模式运行

    xl2tpd -D

## 参考资料

*  [Debian/Ubuntu L2TP/IPSec VPN 安装笔记][1]
