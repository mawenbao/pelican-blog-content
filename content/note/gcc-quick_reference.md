Title: GCC/G++快速使用指南
Date: 2013-08-25 12:14
Tags: gcc, tutorial, not-finished

使用一个例子介绍GCC/G++的编译选项。

## 准备工作

以debian6为例，安装必要的软件包。

    apt-get install build-essential

另外，在下面的例子中为了展示gcc的-L和-l选项，使用了mysql库，因此需要安装mysql-dev软件包

    apt-get install mysql-dev

## 例子

工程涉及4个文件，如下所示，源代码放在[这里](https///github.com/wilbur-ma/gcc-quick-start.git)。

	common.h  # 定义类型和宏等
	util.h    # include common.h
	util.cpp  # include util.h `<mysql/mysql.h>`
	main.cpp  # include common.h util.h

## Makefile

上面工程的Makefile定义如下。

	GCC = /usr/bin/g++
	GCC_FLAGS = -c -Wall
	LD_FLAGS = -L /usr/lib/mysql -l mysqlclient
	TARGET = gcc-quick-start
	OBJECTS = util.o main.o
	 
	all: $(TARGET)
	
	$(TARGET): $(OBJECTS)
		$(GCC) $(LD_FLAGS) -o $(TARGET) $(OBJECTS)
	
	%.o: %.c
		$(GCC) $(GCC_FLAGS) $<
	
	.PHONY: clean
	clean:
		rm -f $(OBJECTS) $(TARGET)

## 编译为动态/静态链接库

介绍将二进制文件打包为动态和静态链接库的方法。
### 动态链接库 shared library

   g++ -shared -o libctest.so -fPIC a.cpp b.cpp
 
### 静态链接库 static library

    g++ -c a.cpp b.cpp
    ar -rvs libtest.a a.o b.o 
    
## 注意事项

### 链接顺序
被依赖的库应当放在依赖它的库的后面，如A依赖于B，则B应置于A后。

    g++ ... A B

### 强制使用静态/动态库

使用-WL选项可以设置使用静态或动态库，可参考[这篇文章](http://stackoverflow.com/questions/3698321/g-linker-force-static-linking-if-static-library-exists)。

    g++ -Wl,-Bstatic -lz -lfoo -Wl,-Bdynamic -lbar -Wl,--as-needed

上面的命令将zlib和libfoo链接为静态库，将libbar链接为动态库。 -Wl选项将后面的用逗号隔开的参数列表传给链接器ld。

## 参考资料

*  [GCC Option Summary](http://gcc.gnu.org/onlinedocs/gcc-4.7.2/gcc/Option-Summary.html#Option-Summary) from gcc manual
*  [GCC 命令行详解](http://www.51testing.com/html/24/1817.html)
*  [GCC 中文手册](http://man.lupaworld.com/content/develop/GCC_zh.htm)
*  [Shared libraries with GCC on Linux](http://www.cprogramming.com/tutorial/shared-libraries-linux-gcc.html)
*  [Static, Shared Dynamic and Loadable Linux Libraries](http://www.yolinux.com/TUTORIALS/LibraryArchives-StaticAndDynamic.html)
*  [Shared Libraries](http://tldp.org/HOWTO/Program-Library-HOWTO/shared-libraries.html) from ["Program Library HOWTO"](http://tldp.org/HOWTO/Program-Library-HOWTO/)

