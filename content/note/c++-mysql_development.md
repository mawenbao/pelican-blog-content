Title: 使用C++进行Mysql开发
Date: 2013-08-25 12:14
Tags: c++, mysql, dev, note

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
参考[#b67911656ef5d18c4ae36cb6741b7965](/note/gcc-quick_reference.html#b67911656ef5d18c4ae36cb6741b7965)，添加-L和-l两个选项即可。

	  g++ -L /usr/lib/mysql -l mysqlclient mysql-test.cpp
	
##  参考资料
	
	
