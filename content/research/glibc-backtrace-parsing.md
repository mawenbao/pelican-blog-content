Title: 输出并解析C++的调用堆栈
Date: 2014-04-25 15:04
Update: 2014-04-25 17:04
Tags: gcc, sigsegv, call stack, debug, linux

[1]: http://man7.org/linux/man-pages/man5/elf.5.html

本文简要介绍在Linux上输出和解析C++的call stack的方法。

开发环境:

    * 编译器: gcc 4.8.2
    * 操作系统: Ubuntu 14.04 x86_64

## 输出调用堆栈
glibc中提供了`backtrace()`和`backtrace_symbols()`两个函数来输出和解析程序的call stack，详情见`man backtrace`。

下面的代码修改自backtrace手册里的例子，当程序收到SIGSEGV信号（内存访问越界）时，输出程序的调用堆栈，以方便定位崩溃点。

<script src="https://gist.github.com/mawenbao/11278165.js"></script>

这段代码在第29行必然会引发内存访问越界。

使用如下的命令编译代码，这是release版本

    g++ -rdynamic -o test.r test_backtrace.cpp

为了解析文件的行号等信息，我们还需要一个debug版本

    g++ -rdynamic -g -o test.d test_backtrace.cpp

上面的编译命令中，加入`-rdynamic`可以将所有非static全局变量和非static函数的符号输出到符号表中。如果你不想在release版本中使用`-rdynamic`选项，编译debug版本的时候也不能用，否则符号表会不一致，从而影响后面的解析过程。

## 解析bactrace输出
运行上面的程序，输出如下

    ./test.r(_Z18print_stack_framesi+0x25) [0x400a02]
    /lib/x86_64-linux-gnu/libc.so.6(+0x36ff0) [0x7f7ddcfb6ff0]
    ./test.r(_Z7myfunc2i+0xe) [0x400ab4]
    ./test.r(_Z6myfuncv+0x19) [0x400ad1]
    ./test.r(main+0x23) [0x400af6]
    /lib/x86_64-linux-gnu/libc.so.6(__libc_start_main+0xf5) [0x7f7ddcfa1ec5]
    ./test.r() [0x400919]

每一行的中括号里的十六进制数是返回地址，小括号里加号之前的内容是mangle后的函数名称，加号之后的十六进制数是返回地址相对函数地址的偏移量。

以第一行为例，首先解析函数名，mangle后的函数名称是`_Z18print_stack_framesi`，使用`c++filt`命令可以将其demangle

    c++filt _Z18print_stack_framesi

输出`print_stack_frames(int)`。

然后使用addr2line获取返回地址所在的行号

    addr2line -e test.d 0x400a02

输出`/home/wilbur/test_backtrace.cpp:13`

需要注意的是，addr2line必须读取额外的调试信息来解析返回地址所在的行号，这也是我们之前编译debug版本的`test.d`的原因。

## python解析脚本
下面是一个专门解析backtrace输出的python脚本。

<script src="https://gist.github.com/mawenbao/11282888.js"></script>

输入如下命令

    ./test.r | python backtrace_parser.py ./test.d

输出如下

    [./test.r]  /home/wilbur/test_backtrace.cpp:13  print_stack_frames(int)
    [./test.r]  /home/wilbur/test_backtrace.cpp:29  myfunc2(int)
    [./test.r]  /home/wilbur/test_backtrace.cpp:35  myfunc()

## backtrace和core dump
Linux的core dump机制可以让你的程序在崩溃的时候在磁盘上保留一份gdb可调试的内存镜像。相比core dump，backtrace虽然只能提供函数的名称和行号等信息，但是胜在简便灵活。另外在生产环境中，许多时候可能不方便使用gcc的`-g`选项编译程序，因此就算有core dump也很难用gdb进行调试。

## 扩展阅读

1. [man 5 elf][1]

