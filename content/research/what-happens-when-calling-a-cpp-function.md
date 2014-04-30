Title: C++函数调用过程总结
Date: 2014-04-30 14:48
Tags: cpp, 未完成

[1]: http://www.ualberta.ca/CNS/RESEARCH/LinuxClusters/mem.html
[2]: http://en.wikipedia.org/wiki/Call_stack
[3]: http://cseweb.ucsd.edu/classes/sp10/cse141/pdf/02/S01_x86_64.key.pdf
[4]: http://www.x86-64.org/documentation/assembly.html
[5]: http://www.x86-64.org/documentation/abi-0.99.pdf
[6]: http://www.classes.cs.uchicago.edu/archive/2009/spring/22620-1/docs/handout-03.pdf
[7]: http://stackoverflow.com/questions/1395591/what-is-exactly-the-base-pointer-and-stack-pointer-to-what-do-they-point
[8]: http://turkeyland.net/projects/overflow/crash.php
[9]: http://eli.thegreenplace.net/2011/09/06/stack-frame-layout-on-x86-64/
[10]: http://www.tenouk.com/Bufferoverflowc/Bufferoverflow2a.html
[11]: http://www.win.tue.nl/~aeb/linux/hh/protection.html

用一个简单的例子解释C++函数调用的过程，备忘。

**未完成**

## 实验环境
以下是本次实验的环境配置

    * 操作系统: Ubuntu 14.04 x86_64
    * 编译器: gcc-4.8.2

## 开始之前
开始之前，建议先阅读如下几篇文章，对call stack和asm多少有点了解，下文会涉及到很多这方面的东西。

* [Understanding Memory][1]
* [Wikipedia:call stack][2]
* [A Readers Guide to x86 Assembly][3]

## 调用堆栈简介

## 简单的例子
下面是一个非常简单的例子。

<script src="https://gist.github.com/mawenbao/96dbd44c385764ed90b0.js"></script>

使用如下命令编译`call_stack_example.cpp`

    g++ -g -O0 call_stack_example.cpp -o a.out

然后使用`objdump`输出汇编代码

    objdump -dS a.out -j .text

下面是call_stack_example.cpp内两个函数的汇编代码。

<script src="https://gist.github.com/mawenbao/becea4b6acdc9d3dfb14.js"></script>

## 阅读资料
1. [x86-64 abi][5]
2. [Gentle Introduction to x86-64 Assembly][4]
3. [x86-64 Machine-Level Programming][6]
4. [What is exactly the base pointer and stack pointer? To what do they point?][7]
5. [Buffer Overflows and You][8]
6. [Buffer overflow Protection][11]
7. [Stack frame layout on x86-64][9]
8. [BUFFER OVERFLOW 6: The Function Stack][10]

