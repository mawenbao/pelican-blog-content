Title: GDB技巧整理
Date: 2013-08-25 12:14
Update: 2014-07-01 17:44
Tags: gdb, trick, gnu

[1]: https://sourceware.org/gdb/onlinedocs/gdb/Source-Path.html "gdb Specifying Source Directories"
[2]: https://sourceware.org/gdb/onlinedocs/gdb/Symbols.html "gdb Examining the Symbol Table"
[3]: http://web.mit.edu/gnu/doc/html/gdb_10.html#SEC58
[4]: http://web.mit.edu/gnu/doc/html/gdb_10.html#SEC57
[5]: http://stackoverflow.com/questions/866721/how-to-generate-gcc-debug-symbol-outside-the-build-target
[6]: https://sourceware.org/gdb/onlinedocs/gdb/Separate-Debug-Files.html

整理常用的gdb技巧。

## 常用命令
常用的gdb命令...

### 启动gdb
1. 直接运行

        gdb --args prog arg1 arg2

2. 运行gdb后使用run命令

        gdb prog
        run arg1 arg2

3. attach到已运行的程序
    
        gdb --pid ${PID_OF_PROG}

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
print(p)可以按照某种类型输出变量的值，示例源码如下:

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

### examine
examine(x)可以按照一定的格式打印内存地址处的数据，详细文档可参考[这里][3]。

    (gdb) x/{COUNT}{FMT}{SIZE} {ADDRESS}

* `{COUNT}`: 打印的数目，默认为1。
* `{FMT}`:   打印的格式[^1]，默认为上次使用的{FMT}:
    * o(octal): 8进制整数
    * x(hex): 16进制整数
    * d(decimal): 10进制整数
    * u(unsigned decimal): 10进制非负整数
    * t(binary): 2进制整数
    * f(float): 浮点数
    * a(address): 输出相对于前面最近的符号的偏移
    * i(instruction): 输出地址处的汇编指令
    * c(char): 字符
    * s(string): c字符串(null-terminated string)
    * z(hex, zero padded on the left): 见说明
* `{SIZE}`: 打印的字节数目，默认为上次使用的{SIZE}:
    * b(byte): 1个字节
    * h(halfword): 2个字节
    * w(word): 4个字节
    * g(giant, 8 bytes): 8个字节
* {ADDRESS}: 目标地址

几个例子:

    (gdb) x/a 0x401419
    0x401419 <main()+113>:  0x55c3c900000000b8

    (gdb) x/i 0x40138d
    => 0x40138d <crash(int, double)+41>:    mov    -0x10(%rbp),%eax

    (gdb) x/1fg 140737488346064
    0x7fffffffdbd0: 10.125

### 设置源码目录
参考[Specifying Source Directories][1]，使用`dir /path/to/your/sources`可在调试时添加一个源码目录。

### 设置字符编码

gdb默认使用utf-8编码，可以使用如下命令修改编码。

    set charset GBK
    
也可直接在~/.gdbinit里设置。

## 高级技巧
一些不太广为人知的技巧...

### 加载独立的调试信息
gdb调试的时候可以从单独的符号文件中加载调试信息。

    (gdb) exec-file test
    (gdb) symbol-file test.debug

test是移除了调试信息的可执行文件, test.debug是被移除后单独存储的调试信息。参考[stackoverflow上的一个问题][5]，可以如下分离调试信息:

    # 编译程序，带调试信息(-g)
    gcc -g -o test main.c

    # 拷贝调试信息到test.debug
    objcopy --only-keep-debug test test.debug

    # 移除test中的调试信息
    objcopy --strip-debug test

    # 然后启动gdb
    gdb -s test.debug -e test

    # 或这样启动gdb
    gdb
    (gdb) exec-file test
    (gdb) symbol-file test.debug

分离出的调试信息test.debug还可以链接回可执行文件test中

    objcopy --add-gnu-debuglink test.debug test

然后就可以正常用addr2line等需要读取调试信息的程序了

    addr2line -e test 0x401c23

更多内容可阅读[GDB: Debugging Information in Separate Files][6]。

### 在内存和文件系统之间拷贝数据

1. 将内存数据拷贝到文件里

        dump binary value file_name variable_name
        dump binary memory file_name begin_addr end_addr 

2. 改变内存数据

    使用set命令

### 执行gdb脚本

常用的gdb操作，比如打断点等可以放在一个gdb脚本里，然后使用时导入即可。例如:

    b main.cpp:15
    b test.cpp:18

gdb运行时，使用source命令即可导入

    (gdb) source /path/to/breakpoints.txt

或gdb运行时导入

    gdb -x /path/to/breakpoints.txt prog

对于每次gdb运行都要调用的脚本，比如设置字符集等，可以放在~/.gdbinit初始文件里，这样每次gdb启动时都会自动调用。

### 自定义命令
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

[^1]: [GDB Output Formats][4], 引用于2014-07-01

