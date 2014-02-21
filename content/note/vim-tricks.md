Title: Vim技巧总结
Date: 2014-02-20 17:26
Tags: vim, trick, 总结, 未完成

总结在使用vim过程中学到的技巧。

## 删除但不拷贝
vim的<kbd>d</kbd>快捷键在删除文本的时候同时会将被删除的内容拷贝到默认寄存器(register `"`)，如果只想删除一行而不拷贝到默认寄存器，可以键入<kbd>"_dd</kbd>，意思就是删除当前行并将被删除的内容存入`_`寄存器，而`_`寄存器是一个类似`/dev/null`的黑洞，存入其中的内容也都瞬间蒸发了。

更多关于vim寄存器的教程可参考`:help registers`和文章[Vim 101: Registers](http://usevim.com/2012/04/13/registers/)。

