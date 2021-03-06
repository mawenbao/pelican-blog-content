Title: C++0x/C++11新特性总结
Date: 2014-06-04 12:50
Update: 2014-06-20 10:02
Tags: c++, c++11, 总结, 未完成

[1]: http://en.wikipedia.org/wiki/C++11
[2]: http://gcc.gnu.org/projects/cxx0x.html
[3]: http://clang.llvm.org/cxx_status.html#cxx11
[4]: http://msdn.microsoft.com/en-us/library/hh567368.aspx
[5]: http://harmful.cat-v.org/software/c++/
[6]: http://www.stroustrup.com/C++11FAQ.html
[7]: http://en.cppreference.com
[8]: http://www.cplusplus.com/reference/
[9]: https://github.com/mawenbao/cpp11-sample-code
[10]: http://www.cplusplus.com/reference/initializer_list/initializer_list/
[11]: http://akrzemi1.wordpress.com/2013/05/14/empty-list-initialization/
[12]: http://www.stroustrup.com/C++11FAQ.html#narrowing
[13]: http://en.wikipedia.org/wiki/Anonymous_function#C.2B.2B_.28since_C.2B.2B11.29

C++11(或C++0x)是目前的C++语言标准，新的标准将取代之前的C++03标准，并在其基础上扩展核心语言和标准库，本文总结C++0x/C++11的部分新特性，如有错漏之处欢迎反馈指正。

本文中出现的代码均在如下环境编译通过，其中多数取自网络并稍加修改，代码放在[这里][9]。

* OS: Ubuntu 14.04 x86-64
* 编译器: clang-3.5
* 标准库实现: libc++

**未完成，列提纲占坑先**

## 关于C++的吐槽
记得刚学编程的时候，老师介绍C++的第一句话就是C++是门很dirty的语言，当时还年少懵懂，不知所云，写C++久了之后才深有体会。以下是吐槽时间:

> [keeping somebody] from using C++ makes me feel like I saved a life.
> <footer class="text-right">aiju</footer> 

> All new features added to C++ are intended to fix previously new features added to C++.
> <footer class="text-right">David Jameson</footer> 

> Whenever I solve a difficult problem with C++, I feel like I’ve won a bar fight.
> <footer class="text-right">Michael Fogus</footer> 

但是，不可否认的是许多人正努力让C++变的更漂亮，C++11就是一个重大的改进。(更多吐槽请猛击[此处][5])

## 编译器支持
各家编译器对C++11语言特性的实现状况:

* GCC: [C++0x/C++11 Support in GCC][2]
* Clang: [C++11 implementation status][3]
* VC++: [C++11 features in Visual C++][4] 

除垃圾回收外，gcc4.8基本实现了C++11的所有语言特性，但是需要使用`-std=c++0x`或`-std=c++11` (>=gcc4.7[^1]) 选项来启用C++11支持。

在C++11标准库的支持方面，libc++(llvm)已全面支持C++11，libstdc++(gcc)要在gcc-4.9之后才支持C++11的regex。

## C++11核心语言扩展
### 统一初始化
**不推荐使用**

C++11引入了一种新的通用初始化方法`initializer list`，所有的变量都可以用一对大括号来进行初始化。

    :::cpp
    int myInt{};
    std::string myStr{"hello world"};
    std::vector<double> myVec{1.2, 2.3};
    
    class MyClass {
    public:
        MyClass(int a, std::string b): _a(a), _b(b) {}
    private:
        int _a;
        std::string _b;
    };

    MyClass myObj{250, "hello again"};

需要注意的是，初始化的值和变量的类型不一致时，会发生隐式类型转换，但不能发生narrowing conversion[^2]，比如:

    ::cpp
    double myDouble{250}; // ok
    int myInt{250.0};     // warning: narrowing conversion of ‘2.5e+2’
                          // from ‘double’ to ‘int’ inside { } [-Wnarrowing]

如果类有一个[initializer_list][10]构造函数，在用initializer list进行初始化时，会优先使用initializer_list构造函数。假设MyClass有如下两个构造函数:

    :::cpp
    MyClass(std::initializer_list<int>);
    MyClass(int);

我们这样初始化myObj:

    :::cpp
    MyClass myObj{250};

实际调用的是`MyClass(std::initializer_list<int>)`这个构造函数。因此，

    :::cpp
    std::vector<int> myVec{250, 10};

上面的代码调用`std::vector(std::initializer_list<int>)`这个构造函数，结果就是myVec包含两个元素，分别为250和10，而不是250个10(std::vector<int>(size_t, int))。

但是下面的代码调用了哪个构造函数:

    :::cpp
    std::vector<int> myVec{};

既符合vector的initializer_list构造函数，又符合vector的默认构造函数。使用`objdump -dSC`查看汇编代码，发现调用的是vector的默认构造函数，有种一坑未平一坑又起的感觉。。。
    
        vector<int> myVec{}; 
    400785:  48 8d 45 e0      lea    -0x20(%rbp),%rax
    400789:  48 89 c7         mov    %rax,%rdi
    40078c:  e8 65 00 00 00   callq  4007f6 <std::vector<int, std::allocator<int> >::vector()>
    400791:  48 8d 45 e0      lea    -0x20(%rbp),%rax
    400795:  48 89 c7         mov    %rax,%rdi
    400798:  e8 73 00 00 00   callq  400810 <std::vector<int, std::allocator<int> >::~vector()>

更多对空列表的探讨参见[Empty list initialization][11]，文中建议对所有提供了initializer_list构造函数的类也提供一个默认构造函数。

### 关键字auto和decltype
类似golang，C++11里使用auto定义的变量可以根据值自动推导变量类型。

    :::cpp
    auto myInt = 10;

decltype可以在编译时获取变量的类型。

    :::cpp
    int myInt = 10;
    decltype(myInt) myInt2 = 20;

需要注意的是，auto推导出的类型并不一定和decltype返回的一致。

    :::cpp
    const std::vector<int> v(10);
    auto myInt = v[0];          // myInt is int
    decltype(v[0]) myInt2 = 10; // myInt2 is const int& 

### 新的for循环写法
类似java的语法，搭配auto使用更方便。

    :::cpp
    int myIntArray[] {1, 2, 3, 4, 5};
    for (auto &i : myIntArray) {
        i *= 2;
    }

### 指针常量nullptr
C++11引入关键字nullptr来表示null指针常量，以取代之前的NULL宏。

    :::cpp
    int *pa = nullptr;          // pa is null
    bool pb = nullptr;          // pb is false
    long pc = (long) nullptr;   // pc is 0
    //long  pc = nullptr;       // error: cannot convert ‘std::nullptr_t’
                                // to ‘long’ in initialization

nullptr的类型是nullptr_t，可和其他类型的指针进行比较操作，可隐式转换为其他的指针类型或bool类型，不可隐式转换为int类型。

### 常量表达式constexpr
C++11引入关键字constexpr来允许用户定义编译期常数

    :::cpp
    constexpr int size = 100;

    constexpr int length() {
            return 150;
    }

    int myArr[length() + size];

### 强类型枚举
C++11里添加了一种新的枚举声明方式

    :::cpp
    enum class Animal {
        Cat,
        Dog,
        Duck,
        Donkey = 100
    };

和之前的enum不同的是，使用`enum class`声明的枚举值不能隐式的转换为int类型，作用域也缩窄为enum的名字`Animal`。

### 编译时断言
`static_assert`关键字可以在编译时测试断言

    :::cpp
    static_assert(const-expression, error-message);

### 匿名函数
C++11添加了新的语法来支持lambda匿名函数。[^3]

    [capture](parameters) -> return_type { function_body }

其中:

* `[capture]`用于捕获外部变量，以`[](int x, int y) -> int { return x + y; }`为例:
    * `[]`: no variables defined. Attempting to use any external variables in the lambda is an error.
    * `[x, &y]`: x is captured by value, y is captured by reference
    * `[&]`: any external variable is implicitly captured by reference if used
    * `[=]`: any external variable is implicitly captured by value if used
    * `[&, x]`: x is explicitly captured by value. Other variables will be captured by reference
    * `[=, &z]`: z is explicitly captured by reference. Other variables will be captured by value
* `(parameters)`用于定义lambda的参数列表
* `-> return_type`是返回类型，如果只有一个返回表达式，则可省略。
* `{function_body}`即函数体

一个简单的例子:

    :::cpp
    int a = 1;
    int b = 1;

    [=, &b] (int c) mutable {
        a = c;
        b = c;
    } (10);

    cout << a << endl;
    cout << b << endl;

结果只有b被修改，a不会发生改变。capture里的`=`捕获后默认是常量，因此无法赋值，加上`mutable`即可捕获为普通变量。

另外，对于`[capture]`为空的lambda函数，还可以配合auto来赋值给变量。

    :::cpp
    auto myMaxFunc = [](int a, int b) { return a > b ? a : b; };
    cout << myMaxFunc(2, 3) << endl;

## C++11标准库扩展
### 正则表达式std::regex
### 线程库std::thread
线程本地存储thread_local
### 原子操作std::atomic
### 工具库
#### std::tuple
#### std::integer_sequence
#### std::function和std::bind
#### std::chrono
### 容器
#### std::array
#### std::forward_list
#### std::unordered_map等
#### 老容器的新成员函数
* emplace, emplace_back和emplace_front: 比insert, push_back和push_front更高效
* cbegin, cend, crbegin和crend: 不管原容器对象是否为const，总是返回const_iterator

### 智能指针
### 伪随机数生成

## C++11的其他改进
### 右值引用

## 参考资料
1. [Wikipedia:C++11][1]
2. [C++11 FAQ][6]
3. [C++ reference][7]
4. [C++ library reference][8]

[^1]: [C++0x/C++11 Support in GCC][2]，引用于2014-06-04。
[^2]: [C++11 FAQ: Prevent Narrowing][12]，引用于2014-06-06。
[^3]: [Wikipedia: C++11 Anonymous function][13]，引用于2014-06-12。

