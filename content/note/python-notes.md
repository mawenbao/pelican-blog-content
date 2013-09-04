Title: notes
Date: 2013-08-25 12:14
Tags: python, note

# Python Notes

记录一些零散的Python笔记。

## Paramiko

paramiko的ssh.exec_command()命令会开启一个单独的session，而且在exec_command中设定的环境变量不会传递给后续的脚本。解决方法是使用bash执行命令:

    ssh.exec_command("bash -l -c 'some commands and some scripts...'")
    
