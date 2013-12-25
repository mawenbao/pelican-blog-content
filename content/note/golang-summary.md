Title: Golang学习杂记
Date: 2013-12-25 18:01
Tags: golang, 总结, 未完成

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

记录Golang的一些关键语法和易错易混淆的知识点。目前边学边记，没什么条理，等内容充实后需要整理一下。

以下内容均基于Go1.2，其中可能有错漏之处，欢迎反馈。

## 语法总结
### 0值
*  boolean: `false`
*  integer: `0`
*  float: `0.0`
*  string: `""`
*  pointer, function, interface, slice, channel, map: `nil`

### 值传递
**Everything** in Go is passed by value，参考[这里][2]。

### 引用类型
pointer, slice, channel和map均可看作引用类型，发生值拷贝时，被拷贝的仅仅是指向实际数据的指针，参考[这里][2]。

### slice和append
使用append时，如果slice对应的array的长度不够，go会会创建一个新的array以容纳新添加的数据，所有旧的array数据都会被拷贝到新的array里。需要频繁使用append时，需要考虑到其效率问题。

对于数据量已知且每次append一条数据的情况，推荐如下使用方式。

    sourceArray := [5]int{ 1, 2, 3, 4, 5}  // 初始化一个长度为10的数组
    targetSlice := make([]int, len(sourceArray)) // 初始化一个长度和容量均为10的slice
    for i := range sourceArray { // 使用range遍历数组，注意不使用第二个返回值以避免额外的拷贝开销
        targetSlice = append(targetSlice[:i], sourceArray[i]) // 依次在目标slice的i位置插入数组的对应元素
    }

### slice和数组

    sl := []int{1, 2, 3}
    ar := [3]int{1, 2, 3}

上面的代码中，sl是长度和容量均为3的slice，ar是长度为3的数组。

### string类型
string使用UTF-8编码。

### 数组类型
1. 数组的长度也是其类型的一部分，[3]int和[4]int类型不同。
2. 和slice不同，发生值拷贝时，数组的所有数据都会被拷贝。

### map
    value, found := MapABC[key]
上面的代码中，value依然是map中key对应的值的拷贝。如果不使用第二个参数found，如下

    value := MapABC[key]

则当key不存在时，value被初始化为对应的0值。

### 初始化
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
**未完成**

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
Go1删除了vector容器，所有的vector操作均可通过slice配合一定的技巧实现，具体请参考[Slice技巧][1]。

### 返回临时变量的指针
在Golang里，返回临时变量的指针是完全合法的，比如下面的函数。

    func test() *int {
        a := 5
        return &a
    }

原因在于，对于使用`&`符号取址的变量，go编译器将其分配到heap上。进一步阅读可参考[faq: stack or heap](http://golang.org/doc/faq#stack_or_heap)和[Escape Analysis in Go][8]。

## Golang标准库
### gob
gob.Encode(a interface{})，如果a保存的是指针类型，实际保存的是a所指向的数据。

引用一，[http://blog.golang.org/gobs-of-data][10]

> This flexibility also applies to pointers. Before transmission, all pointers are flattened. Values of type int8, *int8, **int8,****int8, etc. are all transmitted as an integer value, which may then be stored in int of any size, or *int, or ******int, etc. 

引用二，[http://golang.org/pkg/encoding/gob/][11]

> Pointers are not transmitted, but the things they point to are transmitted; that is, the values are flattened. Recursive types work fine, but recursive values (data with cycles) are problematic. **This may change**.

## 疑难问题
### defer
以下的代码参考了文章[你真的懂defer了吗][9]中的代码。

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
    
## Golang书籍推荐
### Go学习笔记 By雨痕
这其实是人家的学习笔记，内容详细且全面，非常适合通读。

## 其他资源
*  [Go Playground][7] 方便共享golang的代码，向别人请教问题时尤其有用。

## 参考资料
1. [Effective Go][6]
2. [The Go Programming Language Specification][5]
3. [Golang Frequently Asked Questions (FAQ)][4]
4. [Escape Analysis in Go][8]
5. [你真的懂defer了吗][9]
6. [Gobs of data][10]

