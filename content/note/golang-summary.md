Title: Golang学习杂记
Date: 2013-12-25 18:01
Update: 2014-02-20 14:23
Tags: golang, 总结

[1]: https://code.google.com/p/go-wiki/wiki/SliceTricks "golang slice tricks"
[2]: http://golang.org/doc/faq#pass_by_value
[3]: http://golang.org/ref/spec#Program_execution
[4]: http://golang.org/doc/faq
[5]: http://golang.org/ref/spec
[6]: http://golang.org/doc/effective_go.html
[7]: http://play.golang.org/
[8]: http://www.scvalex.net/posts/29/ "Escape Analysis in Go"
[9]: http://bbs.mygolang.com/thread-406-1-1.html "你真的懂defer了吗"
[10]: http://blog.golang.org/gobs-of-data
[11]: http://golang.org/pkg/encoding/gob/
[12]: http://golang.org/pkg/container/list/#pkg-overview
[13]: http://golang.org/pkg/time/#LoadLocation
[14]: http://golang.org/pkg/time/#Time.In
[15]: http://en.wikipedia.org/wiki/List_of_tz_database_time_zones
[16]: http://golang.org/cmd/6g/
[17]: http://golang.org/cmd/8g/
[18]: http://golang.org/doc/install/gccgo
[19]: http://blog.golang.org/profiling-go-programs
[20]: http://golang.org/ref/spec#RangeClause
[21]: http://golang.org/doc/go1#deleted
[22]: http://golang.org/cmd/cgo/

记录Golang的一些关键语法和易错易混淆的知识点。以下内容均基于Linux x86-64平台下的Go1.2，其中可能有错漏之处，欢迎反馈。

## 开发环境和工具
升级Go之前，必须先移除旧的版本。

### 环境变量
Go开发涉及的环境变量有两个:

*  `GOROOT`: go的安装目录，类似于Java的`JAVA_HOME`变量。
*  `GOPATH`: go的工作目录，所有通过`go get`下载的第三方库都会位于该目录下。

然后设置`PATH`变量:

    export PATH=$PATH:$GOROOT/bin:$GOPATH/bin

### 编译器版本
golang的编译器有如下几个版本：

*  [6g][16]: x86-64架构(64位操作系统)上使用的编译器
*  [8g][17]: x86架构(32位操作系统)上使用的编译器
*  [gccgo][18]: GCC的前端，有些时候用gccgo编译出的可执行程序比6g和8g编译出的要快几倍。

### 辅助工具
*  `go tool pprof`: profiling工具，参考文章[Profiling Go Programs][19]。
*  `gofmt`: 格式化go源码。

        find . -name "*.go" | xargs gofmt -w

## 语法总结
### 0值
Zero value

*  boolean: `false`
*  integer: `0`
*  float: `0.0`
*  string: `""`
*  pointer, function, interface, slice, channel, map: `nil`

### 值传递
**Everything** in Go is passed by value[^1]。

### 引用类型
pointer, slice, channel和map均可看作引用类型，发生值拷贝时，被拷贝的仅仅是指向实际数据的指针[^1]。

### range表达式
range表达式仅在循环开始前执行一次[^2]，每次循环的迭代都会对左边的迭代变量赋一次值[^2]，因此在循环中对迭代变量的修改不会影响到其他的迭代。

    a := []int{ 1, 2, 3 }
    for i, v := range a {
        println(i)
        i -= 1
    }

输出`1 2 3`(省略了换行符)。

### 数组和slice
#### 数组类型
1. 数组的长度也是其类型的一部分，`[3]int`和`[4]int`类型不同。
2. 和slice不同，发生值拷贝时，数组的所有数据都会被拷贝。

#### slice和数组的定义

    sl := []int{1, 2, 3}
    ar := [3]int{1, 2, 3}

上面的代码中，sl是长度和容量均为3的slice，ar是长度为3的数组。

#### slice和append
使用append时，如果slice对应的array的长度不够，go会创建一个新的array以容纳新添加的数据，所有旧的array数据都会被拷贝到新的array里。需要频繁使用append时，需要考虑到其效率问题。

对于数据量已知且每次append一条数据的情况，推荐如下使用方式。

    // 初始化一个长度为10的数组
    sourceArray := [5]int{ 1, 2, 3, 4, 5}
    // 初始化一个长度和容量均为10的slice
    targetSlice := make([]int, len(sourceArray))
    // 使用range遍历数组，注意不使用第二个返回值以避免额外的拷贝开销
    for i := range sourceArray {
        // 依次在目标slice的i位置插入数组的对应元素
        targetSlice = append(targetSlice[:i], sourceArray[i])
    }

#### slice和数组访问越界
以下是常见的使用场景和常见的错误：

    ar := [3]int{1, 2, 3} // len(ar) == 3
    sa := ar[:]           // len(sa) == 3
    sb := ar[:2]          // len(sb) == 2

    ar[3:] // []
    sa[3:] // []
    sb[2:] // panic

    ar[4:] // compiler error
    sa[4:] // panic 访问越界
    sb[3:] // panic 访问越界

超过slice长度的元素，即使slice指向的数组里存在该元素，使用slice访问依然会越界。

    ar[3]  // == 3
    sb[3]  // panic error

### string类型
string使用UTF-8编码。

### map
    value, found := MapABC[key]
    
上面的代码中，value依然是map中key对应的值的拷贝。如果不使用第二个参数found，如下

    value := MapABC[key]

则当key不存在时，value被初始化为对应的0值。

### 初始化
常见的初始化方法。

1. new初始化变量为0值，返回指针。
2. 构造函数，使用`&`可返回指针，成员的默认值为0值。
3. make仅用于初始化slice, map和channel三种类型，返回实际变量。
4. 源文件中的init函数，所有的init函数按引用顺序在程序运行后依次执行，参考[这里][3]。

### 赋值操作符
使用`:=`需要注意的地方。

1. 左边的成员至少要有一个是未声明的变量。
2. 已声明的变量，在同一作用域内，变量值被改写。
3. 如果已声明的变量作用域在外层，则定义一个新的同名变量，会屏蔽外层的变量。

### iota
每个const关键字都会将iota的值重置为0，每个const表达式让iota增加1。

    const m = iota // m = 0
    const n = iota // n = 0

    const (
        a = iota   // a = 0
        b = iota   // b = 1
        c          // c = 2
    )

    const (
        d = 1 << iota // iota重置为0，d = 1
        e             // e = 1 << 1 = 2
        f             // f = 1 << 2 = 4
    )

在同一个const表达式中多次使用iota，其值不变。

    const (
        a, b = iota, 1 << iota // a = 0, b = 1
        c, d                   // c = 1, d = 2
        e, f                   // e = 2, f = 4
    )

### 函数参数和命名的返回变量
*  函数参数和命名的返回变量的作用域就是函数体。
*  命名的返回变量默认值为0值，一个单独的`return`会返回命名的返回值的当前值。

### 函数
函数可以作为值附给变量，代码见[这里](http://play.golang.org/p/DABfLTIDIm)。

    package main

    func test(a int) int {
        return a
    }

    func main() {
        var fun func(int)int = test
        println(fun(100))
    }
    
### vector容器
Go1删除了vector容器[^3]，所有的vector操作均可通过slice配合一定的技巧实现，具体请参考[Slice技巧][1]。

### 返回临时变量的指针
在Golang里，返回临时变量的指针是完全合法的，比如下面的函数。

    func test() *int {
        a := 5
        return &a
    }

原因在于，对于使用`&`符号取址的变量，go编译器将其分配到heap上。进一步阅读可参考[faq: stack or heap](http://golang.org/doc/faq#stack_or_heap)和[Escape Analysis in Go][8]。

## 标准库
### sql
Open()返回的`type DB`是一个数据库的句柄，而不是一个数据库连接，另外Open函数也不一定立即建立和数据库的连接（见Open函数的说明）。

`type DB`维护着一个数据库连接池，在多个goroutine之间并发使用是安全的。由于连接池的存在，每次执行Query()和Exec()等函数的并不一定是同一个数据库连接，因此如果有需要，可以使用Begin()函数创建一个数据库事务，在Begin()和Commit()/Rollback()之间的数据库操作将被保证在同一个数据库连接上执行。

基于以上的事实，每次数据库请求都调用Open()和Close()是不明智甚至是不正确的。

### gob
gob.Encode(a interface{})，如果a保存的是指针类型，实际编码的是a所指向的数据。

引用一，[http://blog.golang.org/gobs-of-data][10]

> This flexibility also applies to pointers. Before transmission, all pointers are flattened. Values of type int8, *int8, **int8,****int8, etc. are all transmitted as an integer value, which may then be stored in int of any size, or *int, or ******int, etc. 

引用二，[http://golang.org/pkg/encoding/gob/][11]

> Pointers are not transmitted, but the things they point to are transmitted; that is, the values are flattened. Recursive types work fine, but recursive values (data with cycles) are problematic. **This may change**.

### time
涉及到时区的常用函数：

*  LoadLocation: 根据时区的名称获取对应的Location，时区名称可参考[List of tz database time zones][15]，文档见[此][13]。
*  In(Location): 将time转换为Location所在的时区，返回转换后的time，文档见[此][14]。

### list
golang的list实现了一个双向链表[^4]，不适合随机存取(按索引取值)，不是goroutine安全的。相比slice，list适合用在需要频繁在首尾插入元素或删除某个元素的情况。

## 疑难问题
### 在循环中删除slice的元素
<span class="text-danger">
不要这么做，考虑用[list](#10ae9fc7d453b0dd525d0edf2ede7961)替换slice。
</span>

    a := []int { 1, 2, 4, 5 }
    println(len(a)) // 4
    println(a[4:])  // []
    println(a[5:])  // panic

以上是一些关于slice的基础知识，下面举个循环中删除slice元素的例子。假设我们有如下一个需求：

> 给定一个slice []int{1, 2, 4, 5}，我们希望通过一个for循环删除其中的偶数元素，期望的输出是1, 5。

以下的代码会直接panic，原因是在第4次迭代的时候，发生了slice访问越界(此时slice长度为3, i为3)，完整代码见[这里](http://play.golang.org/p/85hbFJgWGz)。

    a := []int{1, 2, 4, 5}
    for i, _ := range a {
        if a[i]%2 == 0 {
            // delete a[i]
            a = append(a[:i], a[i+1:]...)
        }
    }
    fmt.Println(a)

以下的代码不会panic，但结果不是我们期望的。完整代码见[这里](http://play.golang.org/p/o8-OrdSVfH):

    s := []int{1, 2, 4, 5}
    for i := 0; i < len(s); i++ {
        if s[i]%2 == 0 {
            // delete s[i]
            s = append(s[:i], s[i+1:]...)
        }
    }
    fmt.Println(s)

输出`[1 4 5]`。

原因在于删除第二个元素`2`之后，目标slice变为了`[]int{1, 4, 5}`，而此时i为1，下一次迭代i自增后直接略过了`4`。解决方案是在删除过后，将i减1。如下，完整代码见[这里](http://play.golang.org/p/3sxuJfcCVa):

    s := []int{1, 2, 4, 5}
    for i := 0; i < len(s); i++ {
        if s[i]%2 == 0 {
            // delete s[i]
            s = append(s[:i], s[i+1:]...)
            i -= 1
        }
    }
    fmt.Println(s) 

### defer
以下参考了文章[《你真的懂defer了吗》][9]中的代码。

例子1，见[这里](http://play.golang.org/p/wY8p-jY0ex)，输出1。

    package main

    func fun() (m int) {
        defer func() {
            m++
        }()
        return 0
    }

    func main() {
        println(fun())
    }

defer在return之前执行，但return并非原子操作。具体的说return分两步，首先为返回变量赋值`m = 0`，然后空返回`return`。 而实际上defer在这两步之间被执行，即先给返回变量赋值，然后执行defer语句，最后一个空的return语句，因此上面的函数可改写为：

    func fun() (m int) {
        m = 0 // 返回变量赋值
        m++ // defer
        return
    }

另外一个例子，见[这里](http://play.golang.org/p/8mBfLOYMPk)，输出5。

    package main

    func fun() (r int) {
        t := 5
        defer func() {
            t = t + 5
        }()
        return t
    }

    func main() {
        println(fun())
    }

上面的fun函数可改写为：

    func fun() (r int) {
        t := 5
        r = t
        t = t + 5
        return
    }

### 无法获取map元素的地址
代码见[这里](http://play.golang.org/p/J4eOCvSKn-)

    package main

    type A struct {
        Value int
    }
    func (a A) getVal() int {
        return a.Value
    }
    func (a *A) getVal2() int {
        return a.Value
    }

    func main() {
        a := map[int]A{ 1: A{10} }
                
        //println(&a[1])          // wrong, cannot take the address of a[1]

        println(a[1].Value)       // ok
        //a[1].Value = 20         // wrong, cannot assign to a[1].Value
                                    
        println(a[1].getVal())    // ok
        //println(a[1].getVal2()) // wrong, cannot call pointer method on a[1]; cannot take the address of a[1]
    }

分别取消注释的代码并运行可看到相应的编译错误，总之就是map的index操作获得的变量无法取其指针。

另一段代码，见[这里](http://play.golang.org/p/QAShQtVyO1)

    package main

    type A struct {
        Value int
    }

    func main() {
        a := map[int]A{ 1: A{10} }
        b := map[int]int{ 1: 10 }
                    
        //a[1].Value += 10 // error, cannot assign to a[1].Value
        b[1] += 10
                                
        println(a[1].Value)
        println(b[1])
    }

取消注释的行并运行可看到注释后的编译错误，原因我暂时也不清楚。

解决的方法主要有两个，在map的值使用指针类型(*A)，代码见[这里](http://play.golang.org/p/omlBnBZYfT)。

    package main

    type A struct {
        Value int
    }

    func main() {
        a := map[int]*A{ 1: &A{10} }
                
        a[1].Value += 10
                        
        println(a[1].Value)
    }

或者使用一个临时变量，代码见[这里](http://play.golang.org/p/-gBUhLGIXN)。

    package main

    type A struct {
        Value int
    }

    func main() {
        a := map[int]A{ 1: A{10} }
                
        tmp := a[1]
        tmp.Value += 10
        a[1] = tmp
        
        println(a[1].Value)
    }

关于此问题的讨论链接:

*  [golang-nutes>Address of map entries](https://groups.google.com/forum/#!topic/golang-nuts/V_5kwzwKJAY)
*  [golang-nuts>Why can't I assign to struct in map?](https://groups.google.com/forum/?fromgroups=#!topic/golang-nuts/4_pabWnsMp0)
*  [go issue: spec: cannot assign to a field of a map element directly: m["foo"].f = x](https://code.google.com/p/go/issues/detail?id=3117)

### for循环变量重复使用问题

示例代码如下，见[这里](http://play.golang.org/p/F-Y1Jgt9t8)，输出`3 3 3`。

    package main

    import "time"

    func main() {
        for _, a := range []int{1, 2, 3} {
            go func() {
                println(a)
            }()
        }
        time.Sleep(2)   
    }

原因是Golang的for循环会在各个迭代中重复使用循环变量，通常不会有问题，但是结合goroutine使用会有错，详细内容可参考[Effective Go#Channels](http://golang.org/doc/effective_go.html#channels)中的相关解释。

要想输出`1 2 3`而不是`3 3 3`，解决方法是在每次迭代中使用循环变量的拷贝值。

    for _, a := range []int{1, 2, 3} {
        go func(val int) {
            println(val)
        }(a)
    }

或者

    for _, a := range []int{1, 2, 3} {
        a := a
        go func() {
            println(a)
        }()
    }
    
## 书籍推荐
### Go学习笔记 By雨痕
这其实是人家的学习笔记，内容详细且全面，非常适合通读。

## 其他资源
*  [Go Playground][7] 方便共享golang的代码，向别人请教问题时尤其有用。

## 其他问题
### 动态链接
众所周知，除了用[cgo][22]链接的c动态库之外，golang库都是被静态链接到可执行文件的。对于没有动态链接这个特性，官方貌似一直没有给出具体解释，目前看来估计以后也不会实现。

## 阅读资料
1. [Effective Go][6]
2. [The Go Programming Language Specification][5]
3. [Golang Frequently Asked Questions (FAQ)][4]
4. [Escape Analysis in Go][8]
5. [你真的懂defer了吗][9]
6. [Gobs of data][10]
7. [Profiling Go Programs][19]

[^1]: Golang Frequently Asked Questions (FAQ), [When are function parameters passed by value][2], 引用于2014.01.17.
[^2]: The Go Programming Language Specification, [range clause][20], version of Nov 13, 2013.
[^3]: Go 1 Release Notes, [deleted packages][21].
[^4]: Golang Package Documentation, [list package overview][12].

