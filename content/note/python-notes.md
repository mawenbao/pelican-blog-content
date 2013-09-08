Title: notes
Date: 2013-08-25 12:14
Tags: python, note

# Python笔记

记录一些零散的Python笔记。

## Paramiko

paramiko的ssh.exec_command()命令会开启一个单独的session，而且在exec_command中设定的环境变量不会传递给后续的脚本。解决方法是使用bash执行命令:

    ssh.exec_command("bash -l -c 'some commands and some scripts...'")
    
## Python2.x设置默认编码为UTF-8
Python2的默认编码是ascii，可以采用如下方法设置为UTF-8。

在`/usr/lib/python2.7/sitecustomize.py`(sitecustomize.py的路径可能因python版本和安装位置而异)加入如下的代码：

    :::python
    import sys 
    sys.setdefaultencoding("UTF-8")

## 参考资料

*  [修改python的默认编码](http://stackoverflow.com/questions/2276200/changing-default-encoding-of-python)

