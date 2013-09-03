Title: c++ mysql development
Date: 2013-08-25 12:14
Tags: c++, mysql, dev, note

# 使用C++进行Mysql开发

介绍用C++语言进行Mysql开发的东东。

## 准备工作
开始编码之前，需要准备的事项。

### 依赖的软件
需要安装mysql-dev库。

	# debian系发行版
	apt-get install libmysqlclient-dev
	# rpm系linux发行版
	yum install mysql-devel

###  编译参数
参考[:tools:gcc:gcc-quick-ref#makefile|这里的Makefile]]，添加-L和-l两个选项即可。

	  g++ -L /usr/lib/mysql -l mysqlclient mysql-test.cpp
	
##  参考资料
	
	
