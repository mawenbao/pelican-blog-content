Title: C++问题总结
Date: 2014-01-07 09:24
Update: 2014-01-11 21:25
Tags: c++, 总结, 未完成

[1]: http://en.wikipedia.org/wiki/Plain_Old_Data_Structures
[2]: http://stackoverflow.com/questions/4178175/what-are-aggregates-and-pods-and-how-why-are-they-special
[3]: http://stackoverflow.com/questions/620137/do-the-parentheses-after-the-type-name-make-a-difference-with-new
[4]: http://gcc.gnu.org/onlinedocs/gcc/Variable-Length.html

总结日常编程中遇到的C++疑难问题，备忘。以下总结多基于C++03标准。

## VLA
c99标准支持VLA(variable length arrays)，而在c11标准里VLA是一个可选的特性，具体实现需看编译器。简单的VLA例子如下：

    int arrlen() { return 10; }
    char arr[arrlen()];

在上面的例子里，arr就是一个VLA。

gcc从c90标准开始便提供VLA扩展，且将VLA数组被分配到栈上[^1]。这样潜在的问题是，当目标数组过大时可能导致栈溢出(stack overflow)。因此建议是，除非必要且明确知道数组不会太大，不要使用VLA。

## POD
POD(plain old data)或PODS(plain old data structure)是指不包含构造函数(constructor)，析构函数(deconstructor)和虚函数(virtual function)等面向对象特性的数据类型。引用wikipedia上[Plain_Old_Data_Structures][1]的话：

> A PODS class has no user-defined copy assignment operator, no user-defined destructor, and no non-static data members that are not themselves PODS. Moreover, a PODS class must be an aggregate, meaning it has no user-declared constructors, no private nor protected non-static data, no base classes and no virtual functions.

更详细的介绍可参考一篇stackoverflow上的问答[What are Aggregates and PODs and how/why are they special?][2]

## 变量隐式初始化
不要依赖这些特性，应当在任何时候对任何类型的变量都主动初始化。

当变量仅被声明而未做初始化时：

*  在静态存储区中，POD类型都会被隐式的初始化为0。
*  在栈上，变量（局部变量）的初始值通常是不确定的。
*  class的默认构造函数总是会被调用，未在构造函数初始化列表里的POD成员变量初始值通常是不确定的(non-POD类型会调用其默认构造函数)。

## new A和new A()

> Sometimes the memory returned by the new operator will be initialized, and sometimes it won't depending on whether the type you're newing up is a POD (plain old data), or if it's a class that contains POD members and is using a compiler-generated default constructor.

上面这段话引用自stackoverflow上问题[Do the parentheses after the type name make a difference with new?][3]的一个回答，另外作者还仔细的对new A和new A()进行了总结。

懒得去纠结这种问题，总之记得一件事情，不管是什么类型都用`new A()`来初始化，另外：

1. non-POD类型必须提供无参构造函数，且其初始化列表必须包含该类的所有成员变量。
2. POD类型在new之后应当用memset等方式重新赋值。

## 调用函数的时候发生了什么

## 阅读资料
1. [wikipedia:Plain_Old_Data_Structures][1]
2. [What are Aggregates and PODs and how/why are they special?][2]
3. [Do the parentheses after the type name make a difference with new?][3]

[^1]: GNU gcc documentation [Arrays of Variable Length][4]

