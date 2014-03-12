Title: awstats+nginx配置笔记
Date: 2013-11-04 16:33
Update: 2014-03-12 22:34
Tags: awstats, perl, nginx, ubuntu, note, 教程

[1]: http://hi.baidu.com/icokeeer/item/2588471c9403c9e05f53b1e2 "http://hi.baidu.com/icokeeer/item/2588471c9403c9e05f53b1e2"
[2]: http://wangyan.org/blog/howto-setup-geoip-for-awstats.html "http://wangyan.org/blog/howto-setup-geoip-for-awstats.html"
[3]: http://awstats.atime.me/cgi-bin/awstats.pl?config=blog.atime.me
[4]: http://awstats.sourceforge.net/docs/awstats_faq.html#MULTILOG "FAQ-COM360 : HOW CAN I PROCESS SEVERAL LOG FILES IN ONE RUN?"

awstats可以分析服务器日志，并提供图形化的分析结果，demo可参考本博客的[awstats页面][3]。以下是一篇简单的awstats教程，记录我在ubuntu系统上安装和配置awstats7.2 + nginx的过程。

## awstats7.2下载和配置
下载awstats

    :::bash
    cd /tmp
    wget http://prdownloads.sourceforge.net/awstats/awstats-7.2.zip
    cd /usr/local 
    sudo unzip /tmp/awstats-7.2.zip
    sudo mv awstats-7.2 awstats

以`blog.atime.me`为例，创建新的配置文件`/etc/awstats/awstats.blog.atime.me.conf`

    :::bash
    cd /usr/local/awstats
    perl tools/awstats_configure.pl
    # 根据提示依次输入
    # web server config file path: none
    # build a new AWStats config/profile: y
    # awstats config file name: blog.atime.me(改成自己的网站名即可)
    # awstats config file path: (不填，使用默认值/etc/awstats)

    # 编辑配置文件
    sudo vi /etc/awstats/awstats.blog.atime.me.conf
    # 将LogFile改为nginx的access日志的位置
    # LogFile="/var/log/nginx/access.log"

    sudo chown -R www-data:www-data /usr/local/awstats/wwwroot

    # 修改awstats的输出目录为/usr/local/awstats/wwwroot/output
    # DirData="/usr/local/awstats/wwwroot/output"
    sudo -u www-data mkdir /usr/local/awstats/wwwroot/output
    
    # 测试新生成的配置文件是否有效
    sudo ./wwwroot/cgi-bin/awstats.pl -config=blog.atime.me

以上的过程如果顺利完成，则表示awstats已配置成功。

## nginx配置
准备工作

    # 安装spawn-fcgi
    sudo apt-get install spawn-fcgi libfcgi0ldbl fcgiwrap

配置nginx，添加一个新的子域`awstats.atime.me`，先在dns服务商那里添加相应的A记录。

    cd /etc/nginx/sites-available
    sudo vi awstats.conf

写入如下内容

    :::nginx
    server {
        listen 80;
        root /usr/local/awstats/wwwroot;
        server_name awstats.atime.me;

        location ~ \.pl$ {
            gzip off;
            include /etc/nginx/fastcgi_params;
            fastcgi_pass unix:/var/run/fcgiwrap.socket;
            fastcgi_index index.pl;
        }
    }

然后

    cd ../sites-enabled
    sudo ln -s ../sites-available/awstats.conf .

修改nginx的access日志的输出格式

    sudo vi /etc/nginx/nginx.conf

找到`Logging Settings`部分，将access_log改为

    log_format main '$remote_addr - $remote_user [$time_local] "$request" ' '$status $body_bytes_sent "$http_referer" ' '"$http_user_agent"   "$http_x_forwarded_for"';
    access_log /var/log/nginx/access.log main;

最后，重新载入nginx配置文件

    sudo service nginx reload

载入配置无误，则可以通过如下网址访问awstats的分析结果

[http://awstats.atime.me/cgi-bin/awstats.pl?config=blog.atime.me][3]

## 其他功能
### 使用GeoIP插件分析访问者IP所在国家
详情可参考[AWStats 国家地区扩展 GeoIP 安装配置][2]。

    :::bash
    # 下载IP数据
    cd /usr/local/awstats/wwwroot
    sudo wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
    sudo gzip -d GeoIP.dat.gz

    # 安装GeoIP C API
    cd /tmp
    wget http://geolite.maxmind.com/download/geoip/api/c/GeoIP-1.4.8.tar.gz
    tar -zxf GeoIP-1.4.8.tar.gz
    cd GeoIP-1.4.8/
    ./configure
    make && make install

    # 安装GeoIP插件
    cd /tmp
    wget http://geolite.maxmind.com/download/geoip/api/perl/Geo-IP-1.39.tar.gz
    tar -zxf Geo-IP-1.39.tar.gz
    cd Geo-IP-1.39
    perl Makefile.PL LIBS='-L/usr/local/lib'
    make && make install

最后，修改awstats的配置文件，将如下一行取消注释并修改为

    LoadPlugin="geoip GEOIP_STANDARD /usr/local/awstats/wwwroot/GeoIP.dat"

### 通过网页界面更新awstats
确保www-data用户对awstats的输出目录拥有写权限，然后在awstats的配置文件里做如下修改

    AllowToUpdateStatsFromBrowser=1

### 读取多个日志文件
按照官方的[建议][4]，可以使用awstats自带的一个脚本`logresolvemerge.pl`来解析多个日志文件。

`logresolvemerge.pl`脚本还支持直接读取gz和bz2等压缩文件，默认位于awstats安装目录的tools文件夹里。使用该脚本的话需要将配置文件里的`LogFile`改为类似下面的样子（注意修改logresolvemerge.pl的位置）：

    LogFile="/usr/local/awstats/tools/logresolvemerge.pl /var/log/nginx/access.log* |" 

需要注意的是，为使`logresolvemerge.pl`脚本能访问相应的日志文件，需要为分配合理的权限。

## 问题
### 关键词乱码
修改配置文件，取消`LoadPlugin="decodeutfkeys"`一行的注释即可，然后重新生成报告。

## 阅读资料
    
*  [Ubuntu Nginx Awstats Fastcgi][1]
*  [AWStats 国家地区扩展 GeoIP 安装配置][2]

