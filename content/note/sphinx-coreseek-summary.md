Title: Sphinx/Coreseek搭建全文搜索引擎二三事
Date: 2014-04-10 20:09
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

最近忙着做一个coreseek全文检索的项目，都没时间更新博客了。目前项目已接近尾声，这里总结下coreseek的安装，配置和项目的设计考量等，以备将来查询。

未完成

## 项目简介
项目的部分需求：

1. 目前需要做全文检索的数据是html网页文件，总数在1000万左右，文件总大小大概是200GB，每天新增1000个文件左右。将来很可能需要检索pdf和mysql等不同的数据来源。
2. 提供RESTful风格的搜索接口，返回json格式的查询结果。因为搜索服务主要是内部使用，估计搜索请求的压力不大。

为缩短开发周期，整个项目使用python实现。

## 开发环境

* 操作系统: Ubuntu 12.04 x86-64
* Coreseek: 4.1测试版
* Python: 2.7

另外在开发过程中使用了如下的第三方Python packages:

* lxml-3.3.4: 解析html文件
* tornado-3.2: 异步http服务器，异步socket通信等

## Sphinx/Coreseek简介
[Sphinx][1]是一个高性能的全文检索引擎，使用C++语言开发，采用GPL协议发布，可购买商业授权，目前的稳定版本是2.1.7。

[Coreseek][2]是基于Sphinx的中文全文检索引擎，使用[MMSEG算法][3]进行中文分词，并且提供[Python数据源][4]。Coreseek采用GPLv2协议发布，可购买商业授权，目前的稳定版本是3.2.14，基于Sphinx-0.9.9，测试版本是4.1，基于Sphinx-2.0.1。（另外，Coreseek官方论坛在2013年的年末称即将发布[5.0版本][5]，不过至今无详细消息）

## Coreseek安装
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

## Coreseek目录结构
## Sphinx配置
### searchd
### indexer
## 数据源
### Python数据源
### Xmlpipe2数据源
## 其他
### 自定义中文词库
### lxml & tornado etc
## 设计考量
### indexer速度慢?
### 分布式searchd
## 资源和参考资料

