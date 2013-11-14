Title: GDB技巧整理
Date: 2013-08-25 12:14
Tags: gdb, trick, gnu

整理常用的gdb技巧。

## 设置字符编码

gdb默认使用utf-8编码，可以使用如下命令修改编码。

    set charset GBK
    
也可直接在~/.gdbinit里设置。

## 常用调试命令

## 命令行参数

1. 直接运行

    gdb --args prog arg1 arg2

2. 运行gdb后使用run命令

    gdb prog
    run arg1 arg2

## 在内存和文件系统之间拷贝数据

1. 将内存数据拷贝到文件里

    dump binary value file_name variable_name
    dump binary memory file_name begin_addr end_addr 

2. 改变内存数据

使用set命令

## 执行gdb脚本

常用的gdb操作，比如打断点等可以放在一个gdb脚本里，然后使用时导入即可。例如:

    b main.cpp:15
    b test.cpp:18

gdb运行时，使用source命令即可导入
    (gdb)source /path/to/breakpoints.txt
或gdb运行时导入
    $gdb -x /path/to/breakpoints.txt prog

对于每次gdb运行都要调用的脚本，比如设置字符集等，可以放在~/.gdbinit初始文件里，这样每次gdb启动时都会自动调用。

## 参考资料

*  [Copy between memory and a file](http://www.linuxtopia.org/online_books/redhat_linux_debugging_with_gdb/dump-restore-files.html)
*  [HowTo: Writing into process memory with GDB](https://isisblogs.poly.edu/2011/04/26/gdb-tricks/)
