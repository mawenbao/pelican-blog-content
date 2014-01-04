Title: GCC相关的环境变量
Date: 2013-08-25 12:14
Update: 2014-01-03 09:36
Tags: gcc, config

介绍GCC在编译阶段和程序运行阶段用到的环境变量。

## GCC编译时用到的环境变量

GCC编译时用到的变量。
### C_INCLUDE_PATH

GCC编译时查找头文件的目录列表。比如:

	echo $C_INCLUDE_PATH
	# outputs
	## /usr/include:/usr/local/include

### CPLUS_INCLUDE_PATH

### LIBRARY_PATH
gcc和g++在编译的链接(link)阶段查找库文件的目录列表，比如:

	echo $LIBRARY_PATH
	# outputs
	## /usr/lib:/usr/lib64:/usr/local/lib:/usr/local/lib64

## 程序运行时用到的环境变量

程序运行阶段用到的变量。
#### LD_LIBRARY_PATH

程序运行时查找动态链接库(.so文件)的目录列表。比如:

	echo $LD_LIBRARY_PATH
	# outputs
	## /usr/lib:/usr/lib64:/usr/local/lib:/usr/local/lib64

#### Debian动态链接库搜索路径

Debian系统上，如果修改LD_LIBRARY_PATH没有用，可修改/etc/ld.so.conf或/etc/ld.so.conf.d/*.conf，将库目录作为一行加入以上的conf文件中，然后运行ldconfig命令即可。

    vi /etc/ld.so.conf.d/my.conf
    ldconfig

或者自定义一个库目录的配置文件(例如my.conf)，然后用ldconfig -f /path/to/my.conf加载该配置文件。

    vi ~/project/test/ld_lib.conf
    ldconfig -f ~/project/test/ld_lib.conf

ld_lib.conf的例子。

    /usr/local/lib
    /path/to/your/shared/lib/directory

### ld.so查找库文件的顺序

ld.so用于查找并加载动态链接库文件(*.so)，详情可参考[man ld.so](http://linux.die.net/man/8/ld.so)。
>ld.so  loads the shared libraries needed by a program, prepares the program to run, and then runs it.  Unless explicitly specified via the -static option to ld dur?
>ing compilation, all Linux programs are incomplete and require further linking at run time.
>
>      The necessary shared libraries needed by the program are searched for in the following order
>
>      o      Using the environment variable LD_LIBRARY_PATH (LD_AOUT_LIBRARY_PATH for a.out programs).  Except if the executable is a setuid/setgid binary, in which  case it is ignored.
>
>      o      From the cache file /etc/ld.so.cache which contains a compiled list of candidate libraries previously found in the augmented library path.
>
>      o      In the default path /lib, and then /usr/lib.

## 参考资料

*  [Environment variables](http://www.network-theory.co.uk/docs/gccintro/gccintro_23.html) from ["An Introduction to GCC"](http://www.network-theory.co.uk/gcc/intro/)
*  [LIBRARY_PATH和LD_LIBRARY_PATH环境变量的区别](http://www.cnblogs.com/panfeng412/archive/2011/10/20/library_path-and-ld_library_path.html)
*  [Linux: Set OR Change The Library Path](http://www.cyberciti.biz/faq/linux-setting-changing-library-path/)
*  [ld.so(8)](http://linux.die.net/man/8/ld.so)

