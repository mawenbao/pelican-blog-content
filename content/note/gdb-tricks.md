Title: GDB技巧整理
Date: 2013-08-25 12:14
Update: 2014-05-26 13:17
Tags: gdb, trick, gnu

[1]: https://sourceware.org/gdb/onlinedocs/gdb/Source-Path.html "gdb Specifying Source Directories"
[2]: https://sourceware.org/gdb/onlinedocs/gdb/Symbols.html "gdb Examining the Symbol Table"

整理常用的gdb技巧。

## 和Symbol类型相关的命令
### ptype
ptype用于显示Symbol的类型，示例源码为:

    struct ABC {
        int val;
    }

    int main() {
        ABC abc;
        return 0;
    }

运行gdb：

    (gdb) b 7
    (gdb) r
    (gdb) ptype abc

    type = struct XXX {
        int val;
    }

ptype可以输出表达式的返回类型，具体介绍可参考[Examining the Symbol Table][2]。

### print {type} variable
print可以按照某种类型输出变量的值，示例源码如下:

    struct ABC {
        double val;
        int val2;
    }

    int main() {
        ABC abc;
        abc.val = 1.5;
        abc.val2 = 10;

        void *pAbc = &abc;

        return 0;
    }

运行gdb:

    (gdb) b 13
    (gdb) r

    (gdb) p pAbc
    $1 = (void *) 0x7fffffffe710

    (gdb) p {ABC} 0x7fffffffe710
    $2 = {val = 1.5, val2 = 10}

    (gdb) p {ABC} pAbc
    $3 = {val = 1.5, val2 = 10}

    (gdb) p * (ABC*) pAbc
    $4 = {val = 1.5, val2 = 10}

    (gdb) p {double} pAbc
    $5 = 1.5

    (gdb) p * (double*) pAbc
    $6 = 1.5

    (gdb) p {int} (pAbc + sizeof (double))
    $7 = 10

    (gdb) p * (int*) (pAbc + sizeof (double))
    $8 = 10

## 设置源码目录
参考[Specifying Source Directories][1]，使用`dir /path/to/your/sources`可在调试时添加一个源码目录。

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

    (gdb) source /path/to/breakpoints.txt

或gdb运行时导入

    gdb -x /path/to/breakpoints.txt prog

对于每次gdb运行都要调用的脚本，比如设置字符集等，可以放在~/.gdbinit初始文件里，这样每次gdb启动时都会自动调用。

## 自定义命令
参考[gdb/Define](https://sourceware.org/gdb/onlinedocs/gdb/Define.html)，可以在gdb中自定义命令，比如：

    (gdb) define hello
    (gdb) print "welcome"
    (gdb) print "hello $arg0"
    (gdb) end

然后如此调用

    (gdb) hello world

即可输出

    (gdb) $1 = "welcome"
    (gdb) $2 = "hello world"

## 阅读资料

1. [Copy between memory and a file](http://www.linuxtopia.org/online_books/redhat_linux_debugging_with_gdb/dump-restore-files.html)
2. [HowTo: Writing into process memory with GDB](https://isisblogs.poly.edu/2011/04/26/gdb-tricks/)
3. [Specifying Source Directories][1]
4. [Examining the Symbol Table][2]

