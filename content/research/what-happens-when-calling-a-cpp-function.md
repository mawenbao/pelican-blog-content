Title: C++函数调用过程解析
Date: 2014-05-01 14:48
Update: 2014-05-07 17:00
Tags: cpp, callstack, 函数调用

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
[17]: http://linux.die.net/man/5/elf
[18]: http://dbp-consulting.com/tutorials/debugging/linuxProgramStartup.html
[19]: http://www.ibm.com/developerworks/library/pa-dalign/
[20]: http://msdn.microsoft.com/en-us/library/windows/hardware/ff561499(v=vs.85).aspx
[21]: http://cocoafactory.com/blog/2012/11/23/x86-64-assembly-language-tutorial-part-1/
[22]: http://people.freebsd.org/~lstewart/references/amd64.pdf

用一个简单的例子解释C++函数调用的过程，备忘。

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

1. 栈(call stack, runtime stack或stack): 在Linux上我们编译程序后一般生成的可执行文件是ELF格式的，下图是一个简化版的ELF文件结构[^1]

        +----------------------+
        |       ... ...        |
        +----------------------+
        |        .text         | <- 程序的汇编代码
        +----------------------+
        |       ... ...        |
        +----------------------+
        |        .rodata       | <- 硬编码在源文件里的字符串
        +----------------------+
        |       ... ...        |
        +----------------------+
        |        .data         | <- 初始化的全局和静态变量
        +----------------------+
        |        .bss          | <- 未初始化的全局和静态变量
        +----------------------+
        |       ... ...        |
        +----------------------+
    
    可执行文件将会在运行时被载入内存中，下面是一个简化的进程虚拟地址空间图。

        +----------------------+ <- 高地址处
        |       ... ...        |
        +----------------------+ 
        |        stack         | <- 本文的主角，call stack，向低地址处生长
        +----------------------+ 
        |       ... ...        |
        +----------------------+ 
        |        heap          | <- 动态分配的内存，向高地址处生长
        +----------------------+
        |  uninitialized data  | <- 未初始化的全局变量和静态变量
        +----------------------+
        |   initialzed data    | <- 初始化的全局和静态变量，从ELF的.data区载入
        +----------------------+
        |        code          | <- 程序代码，从ELF的.text区载入
        +----------------------+
        |       ... ...        |
        +----------------------+ <- 低地址处

2. 寄存器:
    * %rax: 通常用于返回第一个整数。
    * %rbp: base pointer，指向当前frame的底部附近(caller的%rbp)。
    * %rsp: stack pointer，用于保存最新分配的frame的顶部，也就是stack顶部。
3. 调用者(caller)和被调用者(callee): 在函数foo的上下文中，调用者(caller)就是main函数，被调用者(callee)就是foo函数。
4. stack frame: stack是由一个个的stack frmae组成的，每次函数调用都会在栈上分配一个新的frame，该frame内保存了当前函数调用的上下文信息，包括请求参数(可能直接保存在寄存器中[^2])，返回地址和局部变量等内容。
5. 返回地址: callq指令会在调用函数的时候将下一条指令的地址push到stack上，当本次调用结束后，retq指令会跳转到被保存的返回地址处使程序继续执行。
6. stack上的数据是[字节对齐][19]的。
7. stack由高地址处向低地址处生长，在下图中`16(%rbp)`表示地址`16 + value of register[%rbp]`

        +----------------------+ <- 高地址处
        |       ... ...        |
        +----------------------+ 
        |      parameters      | <- 没有保存到寄存器里的callee的函数参数(如果有的话)
        +----------------------+ <- 16(%rbp) + n*8 n=0,1,2,3 ...
        |    return address    | <- callee的返回地址，callee的stack frame开始处
        +----------------------+ <- 8(%rbp)
        |     caller's %rbp    | <- 保存的是caller的%rbp
        +----------------------+ <- (%rbp) 
        |    saved registers   | <- 最开始是在函数调用中会被占用的寄存器(如果有的话)，调用结束后恢复
        +----------------------+
        | callee's locals etc. | <- 之后是函数内定义的局部变量和临时变量(保存函数参数寄存器等)
        +----------------------+
        |       ... ...        |
        +----------------------+
        |      parameters      | <- callee的callee的函数参数(如果有的话)
        +----------------------+ <- n*8(%rsp) n=0,1,2,3 ...
        |       ... ...        | <- 栈顶，calleee的stack frame结束处
        +----------------------+ <- (%rsp)
        |       ... ...        |
        +----------------------+ <- 低地址处

    当callee的函数参数太多(或存在不能存储到寄存器上的参数类型)时，多余的函数参数会按照从右向左的顺序依次入栈，占用caller的stack frame的空间。[^3]

8. 汇编指令:
    * leaveq: 相当于以下两条指令[^4]

            mov %rbp, %rsp // 将栈顶指针指向caller的frame指针
            pop %rbp       // 将caller的frame指针出栈并保存于%rbp中

    * callq: 将下一条指令的地址入栈，然后跳转到目标地址处执行[^5]。
    * retq: 将返回地址出栈并跳转到该地址处继续执行[^5]。

## 简单的例子
下面是一个非常简单的例子。

### cpp源代码
<script src="https://gist.github.com/mawenbao/96dbd44c385764ed90b0.js"></script>

使用如下命令编译`call_stack_example.cpp`

    g++ -g -O0 -fno-stack-protector call_stack_example.cpp -o a.out

为了让汇编代码更简单，我们在编译选项里使用`-fno-stack-protector`，这可以禁止gcc默认启用的Stack Protection[^6]，关于Stack Protection的详细信息可参考[Buffer overflow protection][13]和[StackGuard: Simple Stack Smash Protection for GCC][14]。

### 汇编代码和注释
然后使用`objdump`输出汇编代码

    objdump -dS a.out -j .text

下面是call_stack_example.cpp内三个函数的汇编代码和注释，gcc默认使用的是AT&T汇编语法。

<script src="https://gist.github.com/mawenbao/becea4b6acdc9d3dfb14.js"></script>

## 其他例子
### 函数参数传递
下面的例子取自[System V Application Binary Interface][5]的图3.5 Parameter Passing Example和图3.6 Register Allocation Example

假设有以下结构体和函数

    typedef struct {
        int a, b;
        double d;
    } structparm;

    extern void func(
        int e,
        int f,
        structparm s,
        int g,
        int h,
        long double ld,
        double m,
        __m256 y,
        double n,
        int i,
        int j,
        int k);

然后如下调用函数func:

    structparm s;
    int e, f, g, h, i, j, k;
    long double ld;
    double m, n;
    __m256 y;

    func (e, f, s, g, h, ld, m, y, n, i, j, k);

则函数参数的传递方式如下表

General Purpose Registers | Floating Point Registers | Stack Frame Offset
--------------------------|--------------------------|-------------------
%rdi: e         | %xmm0: s.d    | 0: ld 
%rsi: f         | %xmm1: m      | 16: j
%rdx: s.a, s.b  | %ymm2: y[^7]  | 24: k[^8]
%rcx: g         | %xmm3: n      |
%r8:  h         |               |
%r9:  i         |               |

## 额外阅读资料
1. [System V Application Binary Interface][5]
2. [Gentle Introduction to x86-64 Assembly][4]
3. [x86-64 Machine-Level Programming][6]
4. [Review of assembly language][7]
5. [Buffer Overflows and You][8]
6. [Protection against buffer overflows][11]
7. [Stack frame layout on x86-64][9]
8. [BUFFER OVERFLOW 6: The Function Stack][10]
9. [Linux x86 Program Start Up][18]
10. [x64 Architecture][20]
11. [X86_64 Assembly Language Tutorial: Part 1][21]
12. [Amd64 Overview][22]

[^1]: [man elf][17]，引用于2014-05-07。
[^2]: 关于参数是否通过寄存器传递的具体细则，请参考[System V Application Binary Interface][5]的`3.2.3 Parameter Passing`部分。
[^3]: 参考[System V Application Binary Interface][5]的3.2 Function Calling Sequence，引用于2014-05-07。
[^4]: [Wikipedia:function prologue][12], 引用于2014-05-04。 
[^5]: [Call vs Jmp: The Stack Connection][16]，引用于2014-05-05。
[^6]: 参考`man gcc`中关于`-fstack-protector`选项的说明。
[^7]: %ymm0-%ymm15是256位的浮点数寄存器，其低128位对应%xmm0-%xmm15
[^8]: 栈上的函数参数要按8字节对齐

