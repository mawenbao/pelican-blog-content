Title: c++ predefined macros
Date: 2013-08-25 12:14
Tags: c++, compiler, gcc, note

# 编译器内建宏

介绍msvc和gcc4的内建宏(predefined macros)。

## MSVC

详细的VS2012编译器内建宏可参考[该页面](http://msdn.microsoft.com/en-us/library/vstudio/b0084kay.aspx)。

编译器版本

	
	_MSC_VER         MSVC编译器版本
	_MSC_VER = 1600  MS VC++ 10.0  
	_MSC_VER = 1500  MS VC++ 9.0   
	_MSC_VER = 1400  MS VC++ 8.0   
	_MSC_VER = 1310  MS VC++ 7.1   
	_MSC_VER = 1300  MS VC++ 7.0   
	_MSC_VER = 1200  MS VC++ 6.0   
	_MSC_VER = 1100  MS VC++ 5.0   

系统架构

	
	_WIN32           32位编译器
	_WIN64           64位编译器

调试版本

	
	_DEBUG           Debug版本
	NDEBUG           Release版本

其他宏

	
	__cplusplus      C++编译

## GCC4

查看gcc4内建宏的方法，''gcc -dM -E - < /dev/null''，详细的宏介绍可参考[该页面](http://gcc.gnu.org/onlinedocs/cpp/Predefined-Macros.html)。

gcc版本

	
	__GNUC__         gcc主版本号
	__GNUC_MINOR__   gcc次版本号

系统架构

	
	_LP64(__LP64__)  LP64数据模型，用于64位系统
	

## 参考资料

*  [VS2012内建宏](http://msdn.microsoft.com/en-us/library/vstudio/b0084kay.aspx)
*  [GCC内建宏](http://gcc.gnu.org/onlinedocs/cpp/Predefined-Macros.html)

