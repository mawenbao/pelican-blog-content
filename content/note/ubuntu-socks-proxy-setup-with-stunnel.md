Title: 使用dante-server和stunnel搭建socks代理服务器
Date: 2013-12-04 13:30
Tags: note, proxy, socks5, ubuntu

[1]: https://wido.me/sunteya/setup-a-socks-proxy-server-pass-by-secure-firewall/ "https://wido.me/sunteya/setup-a-socks-proxy-server-pass-by-secure-firewall/"
[2]: https://www.digitalocean.com/community/articles/how-to-set-up-an-ssl-tunnel-using-stunnel-on-ubuntu "https://www.digitalocean.com/community/articles/how-to-set-up-an-ssl-tunnel-using-stunnel-on-ubuntu"
[3]: http://www.inet.no/dante/doc/faq.html "http://www.inet.no/dante/doc/faq.html"
[4]: http://www.stunnel.org/faq.html "http://www.stunnel.org/faq.html"

总结在Ubuntu上使用Dante和Stunnel搭建socks代理服务器的过程，以供日后查询。

dante-server是一个免费的socks代理服务器，stunnel可以对tcp连接进行ssl加密，相关程序的版本为

*  Ubuntu: 12.04 x86_64
*  dante-server: v1.1.19
*  stunnel: 4.42

## 安装和配置dante-server

### 安装dante-server
    apt-get install dante-server

### 配置dante-server
dante-server的默认配置文件为`/etc/danted.conf`，配置说明

1. 仅在本地(localhost)监听1999端口，端口可任意选（注意使用netstat -nap | grep 1999查看端口是否被占用)。
2. 不写日志文件(dante-server会写超多日志）。
3. method设置为none表示没有登录验证。

完整的配置文件如下

    #logoutput: /var/log/danted.log
    logoutput: stderr
    # listen locally
    internal: 127.0.0.1 port = 1999
    #internal: eth0 port = 1999
    external: eth0

    method: none

    user.privileged: proxy
    user.notprivileged: nobody
    user.libwrap: nobody

    connecttimeout: 30
    iotimeout: 86400

    client pass {
        from: 192.168.0.0/0 port 1-65535 to: 0.0.0.0/0
    }

    client pass {
        from: 127.0.0.0/8 port 1-65535 to: 0.0.0.0/0
    }

    client block {
        from: 0.0.0.0/0 to: 0.0.0.0/0
        log: connect error
    }

    block {
        from: 0.0.0.0/0 to: 127.0.0.0/8
        log: connect error
    }

    pass {
        from: 192.168.0.0/0 to: 0.0.0.0/0
        protocol: tcp udp
    }

    pass {
        from: 127.0.0.0/8 to: 0.0.0.0/0
        protocol: tcp udp
    }

    block {
        from: 0.0.0.0/0 to: 0.0.0.0/0
        log: connect error
    }

配置完毕后重启dante-server

    service danted restart

### 使用freeradius进行登录验证
未完成

### dante-server查错
关闭dante-server服务

    service danted stop

非daemon模式运行，并打开debug输出

    danted -d -f /etc/danted.conf

## 安装和配置stunnel

### 安装stunnel

    apt-get install stunnel

### 配置stunnel服务器
stunnel4的配置文件默认位于`/etc/stunnel`目录内，配置文件的例子在`/usr/share/doc/stunnel4/examples`目录。

首先，将`/etc/default/stunnel4`的ENABLED改为1，以启用stunnel服务。

然后创建stunnel的服务器证书

    cd /etc/stunnel
    mkdir certs && cd certs
    openssl req -new -x509 -days 3650 -nodes -config /usr/share/doc/stunnel4/examples/stunnel.cnf -out stunnel.pem -keyout stunnel.pem

接下来创建stunnel配置文件`/etc/stunnel/stunnel.conf`，配置说明

1. 日志位于/var/lig/stunnel4/stunnel4.log，默认日志级别为debug(7)，下面的配置里修改为warning(4)。
2. 证书和key都为上面创建的stunnel.pem。
3. 最后的danted服务配置，stunnel将在1998端口监听dante-server的连接请求，并转发到dante-server的监听端口1999。

完整的配置文件如下

    :::ini
    chroot = /var/lib/stunnel4/
    ; Chroot jail can be escaped if setuid option is not used
    setuid = stunnel4
    setgid = stunnel4

    ; PID is created inside the chroot jail
    pid = /stunnel4.pid

    ; Debugging stuff (may useful for troubleshooting)
    ; log level is waring(4), debug log level is 7
    debug = 4 
    output = /stunnel.log

    CAfile = /etc/stunnel/certs/stunnel.pem
    cert = /etc/stunnel/certs/stunnel.pem
    verify = 2 

    ; Disable support for insecure SSLv2 protocol
    options = NO_SSLv2

    ; The following options provide additional security at some performance penalty
    ; Default ECDH/DH parameters are strong/conservative, so it is quite safe to
    ; comment out these lines in order to get a performance boost
    options = SINGLE_ECDH_USE
    options = SINGLE_DH_USE

    client = no

    [danted]
    accept = 1998
    connect = 127.0.0.1:1999

最后，重启stunnel服务
    
    service stunnel restart

### 配置stunnel客户端
在你的客户端机器上安装stunnel，并将`/etc/default/stunnel4`的ENABLED改为1。

然后将服务器端生成的stunnel.pem拷贝到客户端系统，假设放在`/etc/stunnel/stunnel.pem`。

接下来创建配置文件`/etc/stunnel/stunnel.conf`，配置说明

1. 客户端配置文件与服务端基本类似(日志配置等)，注意将client设置为yes。
2. 最后的danted服务配置，stunnel将在本地的1997端口监听dante-server的socks连接请求，并发送到服务端stunnel监听的1998端口（见服务端配置）。注意将配置中的YOUR_SERVER改为你的服务器域名或IP。

完整的配置文件如下

    :::ini
    chroot = /var/lib/stunnel4/
    setuid = stunnel4
    setgid = stunnel4

    ; actually /var/lib/stunnel4/stunnel4.pid
    pid = /stunnel4.pid

    verify = 2 

    ; Debugging stuff (may useful for troubleshooting)
    ; warning level 4, debug is level 7
    debug = 4 
    output = /stunnel.log

    ; Disable support for insecure SSLv2 protocol
    options = NO_SSLv2

    ; The following options provide additional security at some performance penalty
    ; Default ECDH/DH parameters are strong/conservative, so it is quite safe to
    ; comment out these lines in order to get a performance boost
    options = SINGLE_ECDH_USE
    options = SINGLE_DH_USE

    cert = /etc/stunnel/stunnel.pem
    CAfile = /etc/stunnel/stunnel.pem
    client = yes 

    [danted]
    accept = 127.0.0.1:1997
    connect = YOUR_SERVER:1998

最后重启客户端stunnel服务

    service stunnel restart

## 使用socks5代理
按照上文的相关配置，将浏览器的socks5代理项设置为localhost:1997即可使用。

## 查错
遇到问题先检查程序日志，如有需要可修改配置文件的日志输出级别。 根据日志的相关错误输出，先在程序官网的faq页面检索。

*  [dante-server faq][3]
*  [stunnel faq][4]

如果不能找到解决方案，再查看相关文档和google即可。

## 参考资料

1. [通过 stunnel 搭建安全高性能的 sockts 代理服务器][1]
2. [How To Set Up an SSL Tunnel Using Stunnel on Ubuntu][2]

