Title: Sphinx/Coreseek搭建全文搜索引擎二三事
Date: 2014-04-10 20:09
Update: 2014-04-18 16:01
Tags: 搜索引擎, 总结, 未完成

[1]: http://sphinxsearch.com/
[2]: http://www.coreseek.cn/
[3]: http://technology.chtsai.org/mmseg/
[4]: http://www.coreseek.cn/docs/coreseek_4.1-sphinx_2.0.1-beta.html#pysource
[5]: http://www.coreseek.cn/forum/4_11166_0.html
[6]: http://sphinxsearch.com/docs/archives/2.0.1/api-reference.html
[7]: http://www.coreseek.cn/products-install/install_on_bsd_linux/
[8]: https://www.gnu.org/software/libiconv/
[9]: http://forum.z27315.com/topic/15662-%E8%A7%A3%E5%86%B3%E7%BC%96%E8%AF%91libiconv%E6%97%B6%E7%9A%84gets-undeclared-here%E9%94%99%E8%AF%AF/
[10]: https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=667378
[11]: http://sphinxsearch.com/docs/archives/2.0.1/
[12]: http://sphinxsearch.com/docs/archives/2.0.1/confgroup-searchd.html
[13]: http://sphinxsearch.com/docs/archives/2.0.1/sphinxql-reference.html
[14]: http://sphinxsearch.com/docs/archives/2.0.1/confgroup-indexer.html
[15]: http://sphinxsearch.com/docs/archives/2.0.1/conf-mem-limit.html
[16]: http://en.wikipedia.org/wiki/Sphinx_(search_engine)#Performance_and_scalability
[17]: http://team.91town.com/2011/05/coreseek%E4%B8%8E%E7%AC%AC%E5%9B%9B%E5%9F%8E%E6%90%9C%E7%B4%A2/
[18]: http://www.coreseek.cn/docs/coreseek_4.1-sphinx_2.0.1-beta.html#pysource
[19]: http://www.coreseek.cn/docs/coreseek_4.1-sphinx_2.0.1-beta.html#coreseek-confgroup-pysource
[20]: http://www.coreseek.cn/products-install/python/
[21]: http://sphinxsearch.com/docs/archives/2.0.1/xmlpipe2.html
[22]: http://sphinxsearch.com/docs/archives/2.0.1/confgroup-source.html
[23]: http://sphinxsearch.com/docs/archives/2.0.1/confgroup-index.html
[24]: http://sphinxsearch.com/docs/archives/2.0.1/api-reference.html
[25]: http://sphinxsearch.com/docs/archives/2.0.1/sphinxql-reference.html
[26]: http://sphinxsearch.com/docs/archives/2.0.1/delta-updates.html
[27]: http://lxml.de/performance.html
[28]: http://lxml.de/performance.html#xpath
[29]: https://docs.python.org/2/library/stdtypes.html#object.__dict__
[30]: http://guppy-pe.sourceforge.net/#Heapy
[31]: https://docs.python.org/release/2.5.2/ref/slots.html
[32]: http://tech.oyster.com/save-ram-with-python-slots/
[33]: http://stackoverflow.com/questions/3522765/python-pickling-slots-error
[34]: http://stackoverflow.com/questions/472000/python-slots
[35]: https://docs.python.org/2.7/library/pickle.html#data-stream-format
[36]: http://stackoverflow.com/questions/563840/how-can-i-check-the-memory-usage-of-objects-in-ipython/565382#565382
[37]: https://wiki.python.org/moin/TimeComplexity

最近忙着做一个coreseek全文检索的项目，都没时间更新博客了。目前项目已接近尾声，这里总结下coreseek的安装，配置和项目的设计考量等，以备将来查询。

## 开发环境

* 操作系统: Ubuntu 12.04 x86-64
* Coreseek: 4.1测试版(Sphinx-2.0.1)
* Python: 2.7

## Sphinx/Coreseek简介
[Sphinx][1]是一个高性能的全文检索引擎，使用C++语言开发，采用GPL协议发布，可购买商业授权，目前的稳定版本是2.1.7。

[Coreseek][2]是基于Sphinx的中文全文检索引擎，使用[MMSEG算法][3]进行中文分词，并且提供[Python数据源][4]。Coreseek采用GPLv2协议发布，可购买商业授权，目前的稳定版本是3.2.14，基于Sphinx-0.9.9，测试版本是4.1，基于Sphinx-2.0.1。（另外，Coreseek官方论坛在2013年的年末称即将发布[5.0版本][5]，不过至今无详细消息）

## Sphinx/Coreseek安装
下载Coreseek-4.1的源代码

    wget http://www.coreseek.cn/uploads/csft/4.0/coreseek-4.1-beta.tar.gz
    tar xvf coreseek-4.1.beta.tar.gz
    cd coreseek-4.1-beta

解压后发现有三个目录，主要的目录结构如下

    coreseek-4.1-beta/
        csft-4.1/           coreseek修改sphinx-2.0.1后的代码
            api/            sphinx searchd[查询API][6]的实现
        mmseg-3.2.14/       libmmseg分词库
        testpack/           测试和配置示例
        README.txt          介绍和安装指南

按照官方的[安装指南][7]，依次安装mmseg和csft。如果在configure过程中提示缺少头文件，可通过apt-file查询需要安装的软件包。

### 安装mmseg-3.2.14
这里完全参考官方的安装指南即可

    cd mmseg-3.2.14
    ./bootstrap
    ./configure --prefix=/usr/local/mmseg3
    make && sudo make install

### 安装libiconv-1.14
先安装[libiconv][8]，用于字符集编码的转换。

    wget http://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.14.tar.gz
    tar xvf libiconv-1.14.tar.gz
    cd libiconv-1.14
    make && sudo make install

如果你的glibc版本在2.16以上，make时很有可能出现如下错误

    In file included from progname.c:26:0:
    ./stdio.h:1010:1: error: ‘gets’ undeclared here (not in a function)
    _GL_WARN_ON_USE (gets, "gets is a security hole - use fgets instead");
    ^

参考[这里][9]的方法，下载[patch文件](http://www.itkb.ro/userfiles/file/libiconv-glibc-2.16.patch.gz)，解压后打上patch即可。

在libiconv-1.14目录下执行

    wget -O - http://blog.atime.me/static/resource/libiconv-glibc-2.16.patch.gz | gzip -d - | patch -p0

或者考虑直接注释掉srclib/stdio.in.h文件的第698行（应该没问题），即

    //  _GL_WARN_ON_USE (gets, "gets is a security hole - use fgets instead");
 
### 安装csft-4.1
这里configure的参数和[安装指南][7]上稍有区别，一是添加`--with-python`选项来支持Python数据源，二是添加`LIBS=-liconv`来避免最后的链接错误。

    cd csft-4.1
    sh buildconf.sh
    ./configure --prefix=/usr/local/coreseek  --without-unixodbc --with-mmseg --with-mmseg-includes=/usr/local/mmseg3/include/mmseg/ --with-mmseg-libs=/usr/local/mmseg3/lib/ --with-mysql --with-python LIBS=-liconv
    make -j2 && sudo make install

如果`sh buildconf.sh`最后没有生成configure脚本，且提示`automake: warnings are treated as errors`，可以将configure.ac中的这行

    AM_INIT_AUTOMAKE([-Wall -Werror foreign])

改为
    
    AM_INIT_AUTOMAKE([-Wall foreign])

即删掉`-Werror`，然后重新运行`sh buildconf.sh`。

如果configure的时候提示没有安装MySQL的头文件，安装`libmysql++-dev`包即可。

如果你的gcc版本在4.7以上，编译的时候可能会因为sphinx的一个[bug][10]报错

    sphinxexpr.cpp:1746:43: error: ‘ExprEval’ was not declared in this scope, and no declarations were found by argument-dependent lookup at the point of instantiation [-fpermissive]

解决方法参考[bug报告][10]里的一个patch，在csft-4.1目录下执行

    wget -O - http://blog.atime.me/static/resource/sphinxexpr-gcc4.7.patch.gz | gzip -d - | patch -p0

或者你也可以直接修改src/sphixexpr.cpp文件的1746, 1777和1823行，将三行中的`ExprEval`改为`this->ExprEval`。

### 安装辅助工具
将`csft-4.1/contrib/scripts`目录下的searchd脚本拷贝到`/etc/init.d/`目录下，即可使用service命令启动和终止searchd服务。

安装好coreseek后，将`/usr/local/coreseek/share/man/`目录下的所有文件和目录都拷贝到`/usr/local/share/man/`目录里，即可使用man命令查看indexer和searchd的使用手册。

## Sphinx/Coreseek目录结构
按照上面的步骤正确安装Coreseek后，在`/usr/local/coreseek`可看到如下几个文件夹

    bin/            sphinx的程序目录
        searchd     搜索服务器程序
        indexer     索引建立工具
    etc/            配置文件目录
        csft.conf   默认配置文件
    share/
        man/        sphinx的man手册，建议拷贝到系统man目录，方便查询
    var/
        data/       默认的索引存放目录
        log/        默认的日志目录和pid文件目录

实际使用sphinx的流程大概如下:

1. 使用indexer建立或更新索引，如果searchd已经运行，则需要使用`--rotate`选项。
2. 运行searchd

例如：

    cd /usr/local/coreseek
    ./bin/indexer --all     # 第一次建立索引，使用默认配置文件/usr/local/coreseek/etc/csft.conf
    ./bin/searchd           # 使用默认配置文件/usr/local/coreseek/etc/csft.conf

## Sphinx/Coreseek配置
配置文件可参考Sphinx的[官方文档][11]和配置例子`/usr/local/coreseek/etc/sphinx.conf.dist`。

### searchd
配置示例

    searchd
    {
        listen          = 9312
        listen          = 9306:mysql41
        log             = /usr/local/coreseek/var/log/searchd.log
        query_log       = /usr/local/coreseek/var/log/query.log
        read_timeout    = 5
        max_children    = 30
        pid_file        = /usr/local/coreseek/var/log/searchd.pid
        max_matches     = 1000
        seamless_rotate = 1
        preopen_indexes = 1
        unlink_old      = 1
        workers         = threads # for RT to work
    }

这里面的诸多配置选项可参考[searchd program configuration options][12]。

其中，通过第二个listen配置`listen = 9306:mysql41`，你可以使用mysql的client来访问searchd的索引。

    mysql -h 127.0.0.1 -P 9306

然后使用[SphinxQL][13]查询语言即可搜索索引。

### indexer
配置示例

    indexer {
        mem_limit    = 1024M
        write_buffer = 16M
    }

索引工具indexer的配置相对少一些，参考[indexer program configuration options][14]。需要注意的是，mem_limit如果查过2048M会出问题[^1]。

### 数据源和索引配置
参考示例配置文件`/usr/local/coreseek/etc/sphinx.conf.dist`和官方文档[Data source configuration options][22]，[Index configuration options][23]即可。

## 数据源
### Python数据源
Coreseek开发了一个号称万能的Python数据源，使用起来比xmlpipe2要方便一些。其实就是用Python脚本来获取待索引数据，配置文档见[这里][18]，接口文档见[这里][19]，示例程序见[这里][20]。

### Xmlpipe2数据源
这是用Sphinx官方支持的一个"万能"数据源，其实就是将待索引数据按照xmlpipe2的[schema][21]写入标准输出中。

在数据源的配置项中需要设置type为xmlpipe2，另外还要设置一个xmlpipe_command选项，该选项的命令必须输出符合[xmlpipe2 schema][21]的xml文档到标准输出流(stdout)里，比如:

    source news_src
    {
        type = xmlpipe2
        xmlpipe_command = cat /tmp/xmlpipe2_out.xml
    }

## 建立索引
Sphinx使用indexer工具建立和更新索引，据称indexer的索引速度能达到10~15MB/秒[^2]。实际使用过程中，我尝试过分别用Python数据源和xmlpipe2数据源来建立索引，xmlpipe2稍微快一点点。使用Python数据源索引14G文本，大约50万个文件，最后生成2.3G索引，最快在2.8MB/秒左右，估计是慢在中文分词上。

### 自定义中文词库
## 查询
Sphinx支持使用SphinxAPI和SphinxQL查询数据。
### SphinxAPI
SphinxAPI用于和searchd通信，官方提供PHP, Python和Java的实现，API的文档见[此][24]。Coreseek携带的API和示例程序实现都放在`csft-4.1/api/`目录下。

### SphinxQL
SphinxQL是Sphinx提供的SQL方言，用于查询和管理索引，相比SphinxAPI，SphinxQL支持的操作更多，比如删除索引等，文档在[此][25]。

## 实际应用
### 项目简介
项目的部分需求：

1. 目前需要做全文检索的数据是html网页文件，总数在1000万左右，文件总大小大概是200GB，每天新增几千个文件左右。将来很可能需要检索pdf和mysql等不同的数据来源。
2. 提供RESTful风格的搜索接口，返回json格式的查询结果。因为搜索服务主要是内部使用，估计搜索请求的压力不大。

为缩短开发周期，整个项目采用Python实现，使用coreseek自带的Python数据源建立索引。

在开发过程中使用了如下的第三方Python packages:

* lxml-3.3.4: 解析html文件
* tornado-3.2: 异步http服务器，异步socket通信等

### 设计考量

#### 建立索引
上面有提到过，indexer是一个单线程的工具，建立中文索引的速度基本上很难超过3MB/秒，因此可以考虑将大的索引拆分成若干小索引，这些小索引可以同时建立，最后再合并成一个完整的索引。

因为待索引文档的基数很大，但每天更新的数量又比较小，所以建立索引的时候最好使用官方推荐的一种`Main + Delta`的方式，主(Main)索引只需要最开始建立一次，然后每天重建一次增量(Delta)索引并合并到主索引中，相关文档见[Delta index updates][26]。

#### Python相关
项目里需要使用Python查找和解析html文件。

文件查找没有使用Python标准库os的walk函数，当文件数量较多时，walk函数的效率会比较低。有兴趣的可以看下一个叫[betterwalk](https://github.com/benhoyt/betterwalk)的第三方库，据称比`os.walk`快不少。实际项目中，因为待索引文件的目录结构固定且很有规律，直接用`os.listdir`和`os.lstat`即可解决，`os.lstat`可以获取文件的最后修改日期，在建立增量索引的时候非常有用。

html文件的解析使用了口碑很给力的lxml库，用lxml解析html文件时通常有多种方法，使用之前最好仔细看一下lxml各个函数的[benchmark][27]，了解一下哪种方法更快一些，比如使用xpath查找html节点时，lxml的XPath类比xpath()函数要快好几倍[^3]。

另外，Python的多线程处理计算密集型(CPU Bound)任务是一个众所周知的大坑，比如多线程解析html文件。这时最好用多进程分别做解析任务，然后将解析好的文件收集起来。

前面说过indexer比较慢，一般建立索引的时候，速度瓶颈就在indexer上。因此解析好的文件通常要缓存起来，比如缓存在内存里。然而内存是紧俏资源，必须限量节约使用。

关于内存的限量使用，在实现时可以为缓存设定一个阀值，缓存满了就先暂停所有的文件扫描和解析进程，等缓存快没了的时候再继续，在Linux上使用SIGSTOP和SIGCONT信号可以很容易就实现这一功能。相比之下，如何准确的获取缓存对象所占用的内存大小倒是比较困难，折中的办法是统计整个进程的内存占用或是[间接的方法][36]，或者干脆通过限制缓存对象的数目来做限制（这个比较弱智的感觉）。

关于内存的节约使用，大家都知道一般的Python对象都会自动创建一个[\_\_dict\_\_][29]属性来存储其他的属性，然而不太广为人知的是，Python的内置类型dict是一个内存大户，当Python对象少的时候可能很难发现，如果在内存里存储十万或一百万个Python对象时，用Memory
Profiler（比如[Heapy][30]）做下profiling你会发现，光是`__dict__`本身（不包括存在`__dict__`里的数据）就能吃掉你巨量的内存。通过设置类属性[\_\_slots\_\_][31]可以禁止`__dict__`属性的自动创建，其中一个成功故事在[这里][32]，这个哥们通过`__slots__`节约了9G内存。需要说明的是，`__slots__`会带来一些[负面作用][34]，比较明显的一个是，使用version
0版本的pickle协议序列化定义了`__slots__`属性的对象会有报错，但使用更高级别的pickle协议则没问题[^4]（一般很少用到cPickle的[protocol version 0][35]，因为又慢又占空间)。

另外缓存所使用的数据结构也比较重要，直接用Python的内置类型list肯定不行，因为缓存应该是一个FIFO的队列，而`del(list[0])`操作是O(n)的时间复杂度[^5]，用collections.deque比较合适。

## 资源和参考资料
1. [Sphinx 2.0.1 Documentation][11]
2. [Coreseek与第四城搜索][17]，有很多性能相关的测试，很详尽。

[^1]: Sphinx indexer program configuration options, [mem_limit][15]，引用于2014-04-17。
[^2]: [Wikipedia:Sphinx][16]，引用于2014-04-17。
[^3]: lxml benchmarks and speed, [xpath][28]，引用于2014-04-18。
[^4]: [python pickling slots error][33]，引用于2014-04-18。
[^5]: [Python Time Complexity][37]，引用于2014-04-18。

