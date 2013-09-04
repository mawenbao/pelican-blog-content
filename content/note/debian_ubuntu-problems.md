Title: debian ubuntu problems
Date: 2013-08-25 12:14
Tags: debian, ubuntu, problem

# Debian/Ubuntu常见问题及解决方法整理

记录使用Debian/Ubuntu时遇到的问题及其解决方法。

## 网络问题

### ping: connect: network is unreachable
使用`service networking restart`后无法联网，运行`ifconfig`后发现没有eth0，这时需要手动配置eth0接口，注意将$IP_ADDRESS, $MASK和$GATE_WAY改为你的IP地址、子网掩码和网关地址:
    
    ifconfig eth0 $IP_ADDRESS netmask $MASK
    route add default gw $GATE_WAY

## 参考资料

*  [connect: network is unreachable的解决](http://blog.csdn.net/xuyaqun/article/details/6283829)

