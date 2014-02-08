Title: Vim Macro
Date: 2013-08-25 12:14
Update: 2014-02-08 16:28
Tags: vim, 教程

介绍Vim宏的用法
## 初步使用

 1.  普通模式下按`q`键开始录制，输入小写字母作为宏的名称。
 2.  按`q`结束录制。
 3.  使用`@`和宏的名称进行回放，若需多次回放只需在`@`前加上回放次数。

## 高级技巧
### 自增和自减
vim的`ctrl-a`和`ctrl-x`快捷键分别能够将当前数字加一和减一，录制宏的时候合理使用这两个快捷键可以完成许多特殊的工作。

假设当前有如下文本（光标位于t字母上）：

    1. test

在vim中依次执行如下命令（井号`#`之后为注释内容），注意大小写：

    qa          # 开始录制宏，命名为a
    Y           # 复制当前行
    p           # 将复制的一行粘贴到下一行
    2 ctrl-a    # 先按2，然后按ctrl-a，表示将当前数字增加2
    q           # 停止录制
    3@a         # 连续执行三次命名为a的宏

最后文本变为：

    1. test
    3. test
    5. test
    7. test
    9. test

## 阅读资料

1. [Vi and Vim Macro Tutorial: How To Record and Play](http://www.thegeekstuff.com/2009/01/vi-and-vim-macro-tutorial-how-to-record-and-play/)
2. [Increasing or decreasing numbers](http://vim.wikia.com/wiki/Increasing_or_decreasing_numbers)

