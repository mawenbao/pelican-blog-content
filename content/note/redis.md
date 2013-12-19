Title: Redis相关
Date: 2013-12-19 13:36
Tags: redis, memory cache

Redis是一个键值对存储系统，相比memcached，redis支持多种数据结构（如list, sorted set等）和数据持久化。

## 安装
在[这里](http://redis.io/download)下载最新稳定版redis，下面以2.8.3版本为例。

    wget http://download.redis.io/releases/redis-2.8.3.tar.gz

解压并编译安装

    tar -xvf redis-2.8.3.tar.gz
    cd redis-2.8.3
    make
    sudo make install
    cd utils
    sudo ./install_server.sh

默认情况下，redis服务器使用6379端口，配置文件位于`/etc/redis/6379.conf`，日志位于`/var/log/redis_6379.log`，init脚本位于`/etc/init.d/redis_6379`，数据目录在`/var/lib/redis/6379/`。以上参数均可在运行install_server.sh脚本的时候设置。

