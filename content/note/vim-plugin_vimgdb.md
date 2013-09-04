Title: vim gdb
Date: 2013-08-25 12:14
Tags: vim, plugin, gdb

# debian6上为Vim添加GDB调试功能

在debian6上为vim添加gdb调试功能。

## 准备工作

	
	apt-get install libncurses5-dev
	
	./configure --prefix=/usr/local --enable-cscope --enable-gdb --with-features=huge --enable-fontset 

## 问题

1. (未解决) 调试时在可视模式下，使用Ctrl-P添加监控变量时报错`Unable to create variable object`，只能直接使用gdb命令`createvar`。

## 参考资料

*  [vim+vimgdb完全编译安装手册](http://blog.sina.com.cn/s/blog_4c451e0e0100eofw.html)
*  [vi/vim使用进阶: 在VIM中使用GDB调试 – 使用vimgdb](http://easwy.com/blog/archives/advanced-vim-skills-vim-gdb-vimgdb/)
*  [How to connect vim with gdb — using clewn](http://chunhao.net/blog/how-to-connect-vim-with-gdb-using-clewn)

