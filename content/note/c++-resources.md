Title: C/C++资源收集
Date: 2013-08-25 12:14
Update: 2014-04-24 15:21
Tags: c++, resource

收集有用的C/C++资源。

## C资源列表
### C类库
#### sglib
* 项目主页: [http://sglib.sourceforge.net/]()
* 说明: c的通用容器库。
* License: 保留Copyright，无其他要求[^1]。

#### libunwind
* 项目主页: [http://www.nongnu.org/libunwind/]()
* 说明: 可用于输出当前线程的堆栈信息等，详情见项目说明。
* License: 可用于商业用途，详情见源码附带的LICENSE文件。

#### libuv
* 项目主页: [https://github.com/joyent/libuv]()
* 说明: 异步I/O库，类似libevent和libev。相比libev，额外支持IOCP。
* License: [Node's license](https://github.com/joyent/libuv/blob/master/LICENSE)

## C++资源列表
### 文章
#### 语法相关

*  [如何正确使用C++多重继承](http://bigasp.com/archives/486) - C++多重继承 [存档](https://www.evernote.com/pub/wilbur_ma/share#b=f811aee8-c2e6-46e0-b058-bd9c0ff79489&st=p&n=017abb98-429f-4122-87e5-fff74bd18287)

#### 工具文档

*  [Doxygen注释](http://www.doxygen.nl/docblocks.html) - [总结](/note/c++-doxygen_summary.html)

#### 指针相关

*  [Smart Pointers - What, Why, Which?](http://ootips.org/yonat/4dev/smart-pointers.html)
*  [Why is it wrong to use std::auto_ptr<> with standard containers?](http://stackoverflow.com/questions/111478/why-is-it-wrong-to-use-stdauto-ptr-with-standard-containers)
*  [std::auto_ptr to std::unique_ptr](http://stackoverflow.com/questions/3451099/stdauto-ptr-to-stdunique-ptr)

#### 优化相关

*  [GCC编译优化指南](http://lamp.linux.gov.cn/Linux/optimize_guide.html)
*  [Software optimization resources](http://www.agner.org/optimize/)
*  [Wikibooks:Optimizing C++](http://en.wikibooks.org/wiki/Category:Optimizing_C%2B%2B)

### C++类库
#### gpertools
* 项目主页: [https://code.google.com/p/gperftools/]()
* 说明: 提供一个profiling工具pprof，和tcmalloc的实现。
* License: New BSD License

#### threading building blocks
* 项目主页: [https://www.threadingbuildingblocks.org/]()
* 说明: <q>Widely used C++ template library for task parallelism.</q>
* License: GPLv2 with a [runtime exception](http://gcc.gnu.org/onlinedocs/libstdc++/manual/bk01pt01ch01s02.html)

#### nedmalloc
* 项目主页: [http://www.nedprod.com/programs/portable/nedmalloc/]()
* 说明: 多线程memory allocator
* License: Boost Software License

#### zeromq
* 项目主页: [http://zeromq.org/]()
* 说明: 网络库(消息队列)
* License: GPLv3 with a static linking exception[^2]

[^1]: 见[http://sglib.sourceforge.net/#license]()。
[^2]: 见[http://zeromq.org/area:licensing]()。

