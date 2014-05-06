Title: C++函数调用过程总结
Date: 2014-04-30 14:48
Update: 2014-05-06 08:51
Tags: cpp, 未完成

[1]: http://www.ualberta.ca/CNS/RESEARCH/LinuxClusters/mem.html
[2]: http://en.wikipedia.org/wiki/Call_stack
[3]: http://cseweb.ucsd.edu/classes/sp10/cse141/pdf/02/S01_x86_64.key.pdf
[4]: http://www.x86-64.org/documentation/assembly.html
[5]: http://www.x86-64.org/documentation/abi-0.99.pdf
[6]: http://www.classes.cs.uchicago.edu/archive/2009/spring/22620-1/docs/handout-03.pdf
[7]: http://www.scs.stanford.edu/nyu/04fa/notes/l2.pdf
[8]: http://turkeyland.net/projects/overflow/crash.php
[9]: http://eli.thegreenplace.net/2011/09/06/stack-frame-layout-on-x86-64/
[10]: http://www.tenouk.com/Bufferoverflowc/Bufferoverflow2a.html
[11]: http://www.win.tue.nl/~aeb/linux/hh/protection.html
[12]: http://en.wikipedia.org/wiki/Function_prologue
[13]: http://en.wikipedia.org/wiki/Buffer_overflow_protection
[14]: ftp://gcc.gnu.org/pub/gcc/summit/2003/Stackguard.pdf
[15]: http://en.wikipedia.org/wiki/Instruction_pointer
[16]: https://www.cs.uaf.edu/2012/fall/cs301/lecture/09_24_call_and_ret.html

用一个简单的例子解释C++函数调用的过程，备忘。

**未完成**

## 实验环境
以下是本次实验的环境配置

    * 操作系统: Ubuntu 14.04 x86_64
    * 编译器: gcc-4.8.2

## 开始之前
### 阅读资料
开始之前，建议先阅读如下几篇文章，对call stack和asm多少有点了解，下文会涉及到很多这方面的东西。

* [Understanding Memory][1]
* [Wikipedia:call stack][2]
* [A Readers Guide to x86 Assembly][3]
* [Wikipedia:function prologue][12]

### 预备知识
下面是一些在后面的解释中会用到的知识，以下说明均基于x86-64平台。

1. 栈(call stack或stack): 下图是一个简化版的进程虚拟地址空间图。

        +----------------------+
        |       ... ...        | <- 高地址处
        +----------------------+ 
        |    stack segment     |
        +----------------------+
        |       ... ...        |
        +----------------------+
        |     data segment     |
        +----------------------+
        |       ... ...        | <- 低地址处
        +----------------------+

1. 调用者(caller)和被调用者(callee): 在函数foo的上下文中，调用者(caller)就是main函数，被调用者(callee)就是foo函数。
2. stack frame: stack是由一个个的stack frmae组成的，每次函数调用都会在栈上分配一个新的frame，该frame内保存了当前函数调用的上下文信息，包括请求参数(可能直接保存在寄存器中[^2])，返回地址和局部变量等内容。
3. 返回地址: callq指令会在调用函数的时候将下一条指令的地址push到stack上，当本次调用结束后，retq指令会跳转到被保存的返回地址处使程序继续执行。
4. 寄存器%rbp和%rsp: %rbp(stack base pointer)指向当前frame的顶部附近(caller的%rbp)，而%rsp(stack pointer)用于保存最新分配的frame的底部，也就是stack顶部。

        +------------------+
        |     ... ...      | <- 高地址处
        +------------------+ 
        |   parameters     | <- 函数参数(如果有的话)，callee的stack frame开始处
        +------------------+
        |  return address  | <- callee的返回地址
        +------------------+
        |  caller's %rbp   | <- callee的%rbp
        +------------------+
        |  callee's locals | <- 最开始是函数内定义的局部变量
        +------------------+
        | saved registers  | <- 最后是寄存器(函数参数)的拷贝， callee的%rsp，栈顶，calleee的stack frame结束处
        +------------------+
        |     ... ...      | <- 低地址处
        +------------------+

1. 在x86-64架构的操作系统上，栈是从高地址向低地址生长的，因此`sub $0x18,%rsp`命令将栈扩容0x18个字节。
3. leaveq: 相当于以下两条指令[^3]

        mov %rbp, %rsp // 将栈顶指针指向caller的frame指针
        pop %rbp       // 将caller的frame指针出栈并保存于%rbp中

4. callq: 将下一条指令的地址入栈，然后跳转到目标地址处执行[^4]。
5. retq: 将返回地址出栈并跳转到该地址处继续执行[^4]。
## 简单的例子
下面是一个非常简单的例子。

### cpp源代码
<script src="https://gist.github.com/mawenbao/96dbd44c385764ed90b0.js"></script>

使用如下命令编译`call_stack_example.cpp`

    g++ -g -O0 -fno-stack-protector call_stack_example.cpp -o a.out

为了让汇编代码更简单，我们在编译选项里使用`-fno-stack-protector`，这可以禁止gcc默认启用的Stack Protection[^1]，关于Stack Protection的详细信息可参考[Buffer overflow protection][13]和[StackGuard: Simple Stack Smash Protection for GCC][14]。

### 汇编代码
然后使用`objdump`输出汇编代码

    objdump -dS a.out -j .text

下面是call_stack_example.cpp内三个函数的汇编代码，gcc默认使用的是AT&T汇编语法。

<script src="https://gist.github.com/mawenbao/becea4b6acdc9d3dfb14.js"></script>

### foo函数调用过程解析

## 额外阅读资料
1. [System V Application Binary Interface][5]
2. [Gentle Introduction to x86-64 Assembly][4]
3. [x86-64 Machine-Level Programming][6]
4. [Review of assembly language][7]
5. [Buffer Overflows and You][8]
6. [Protection against buffer overflows][11]
7. [Stack frame layout on x86-64][9]
8. [BUFFER OVERFLOW 6: The Function Stack][10]

[^1]: 参考`man gcc`中关于`-fstack-protector`选项的说明。
[^2]: 关于参数是否通过寄存器传递的具体细则，请参考[System V Application Binary Interface][5]的`3.2.3 Parameter Passing`部分。
[^3]: [Wikipedia:function prologue][12], 引用于2014-05-04。 
[^4]: [Call vs Jmp: The Stack Connection][16]，引用于2014-05-05。

