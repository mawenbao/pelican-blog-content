Title: Makefile
Date: 2013-08-25 12:14
Update: 2014-05-12 15:01
Tags: makefile, 总结

[1]: http://www.gnu.org/software/make/manual/html_node/Flavors.html
[2]: https://www.gnu.org/software/make/manual/html_node/Automatic-Variables.html
[3]: https://www.gnu.org/software/make/manual/html_node/Wildcard-Function.html#Wildcard-Function
[4]: https://www.gnu.org/software/make/manual/html_node/Text-Functions.html#index-subst-572
[5]: https://www.gnu.org/software/make/manual/html_node/Text-Functions.html#index-patsubst-573
[6]: https://www.gnu.org/software/make/manual/html_node/Text-Functions.html#index-filter-587
[7]: https://www.gnu.org/software/make/manual/html_node/Name-Index.html#Name-Index
[8]: http://stackoverflow.com/questions/2826029/passing-additional-variables-from-command-line-to-make
[9]: https://www.gnu.org/software/make/manual/html_node/Wildcard-Function.html#Wildcard-Function
[10]: https://www.gnu.org/software/make/manual/html_node/Substitution-Refs.html#Substitution-Refs
[11]: https://www.gnu.org/software/make/manual/html_node/Static-Usage.html#Static-Usage
[12]: http://www.gnu.org/software/make/manual/html_node/Functions.html#Functions
[13]: https://www.gnu.org/software/make/manual/html_node/Substitution-Refs.html

总结GNU Make的一些基础知识和技巧，以下内容均基于Ubuntu 14.04 x86_64平台的GNU Make 3.81。

## 变量
### 变量类型
make支持[两种风格的变量定义方式][1]:

1. 递归扩展变量(recursively expanded variables)
    * 使用`=`或define指令定义
    * `CFLAGS = $(CFLAGS) -O`会导致无限递归
    * 变量每次被展开的时候，所使用的函数都会重新被执行，会降低make的效率，更严重的是，wildcard等函数会返回预料之外的结果。
2. 简单扩展变量(simply expanded varialbes)
    * 使用`:=`或`::=`定义
    * 在变量定义的时候展开一次

### shell变量
shell变量应使用`@`转义，比如变量`${var}`要改为`$${var}`。

### 自动变量
下面是一些常用的[自动变量][2]

* `$<`: 第一个依赖
* `$@`: 目标
* `$?`: 修改时间在目标之后的依赖
* `$^`: 所有的依赖
* `$|`: 所有的order-only依赖

## 函数和指令
### wildcard
[wildcard函数][3]和直接使用通配符`*`的区别在于，wildcard函数可以在变量定义的时候立即展开（即搜索相应的匹配项），而`*`只有在规则中才会被展开。[^1]

### subst
[sust函数][4]用于替换字符串，格式是`$(subst from,to,text)`，其中from是要被替换的子串，to是要替换成的子串，text是需要被替换的字符串。注意from和to之间的逗号左右不要随意添加空格，否则也会被视为需要替换的内容。

### patsubst
[patsubst函数][5]可以匹配并保留第一个没被`\`转义的`%`字符，然后在替换成的字符串里使用，比如`$(patsubst %.css,%.min.css,hello.css)`替换的结果就是`hello.min.css`，同样的，逗号左右不要随意添加空白字符。类似的功能还可以用[Substitution References][13]实现，语法更简洁一些。

### filter
[filter函数][6]可以按一定的规则过滤目标，然后返回符合规则的数据。

## 规则
### order-only依赖

	a: b | c
	    command

上面的例子中，a是目标，b是常规依赖，c是order-only依赖。当a存在时，即便c的修改时间晚于a，该规则也不会更新a。

order-only依赖定义于规则的右侧，与常规依赖用`|`隔开。当目标存在时，不管其是否因order-only依赖而过期，均不更新目标。

### static pattern rules
当有大量类似的目标时，[static pattern rules][11]会很有用，格式如下

    targets ...: target-pattern: prereq-patterns ...
        recipe
        ...

用下面的一个简单例子说明

    a.o b.o c.o: %.o: %.c
        gcc -c -o $@ $<

这里targets是`a.o b.o c.o`，target pattern是`%.o`，prereq-patterns（只有一个）是`%.c`。target
pattern首先从targets里匹配出一个个的目标，然后按照类似于[patsubst](#8ada5b1bc79d74fd3e3f5ebef7534a3f)的方式替换prereq-patterns中的`%`字符，生成相应的依赖。在规则的命令中，可以像普通的规则一样使用`$<`（第一个依赖）和`$@`（目标）等[自动变量](#844084dafd840f9a7369142a70acf312)。

上面的规则可以拆成几条简单的规则:

    a.o:a.c
        gcc -c -o $@ $<

    b.o:b.c
        gcc -c -o $@ $<

    c.o:c.c
        gcc -c -o $@ $<

或者使用字符串替换，更方便一些

    source = ${wildcard *.c}
    objects = ${source:%.c=%.o}

    all: ${objects}

    ${objects}: %.o: %.c
        gcc -c -o $@ $<

## 其它
### 特殊的符号
* `@`: 用于规则中的命令之前，可以在make时只显示命令的输出而不显示命令的内容，比如

        all:
            @echo hello

    只输出hello，不会输出`echo hello`这条命令的内容。

### 传递变量
可以在命令行里设置Makefile的变量值，对如下的makefile

    TARGET=test
    create:
        mkdir -p ${TARGET}

可以通过如下的命令修改TARGET的值:

    make create TARGET=another
 
### .PHONY伪目标
尽可能使用`.PHONY`标示所有的伪目标，以避免潜在的问题。

常见的一例问题如下：

    :::makefile
    debug:
        mkdir -p debug
        cd debug && make -f ../Makefile

使用`make debug`命令时可能会提示`Nothing to be done for debug`，即debug目标已是最新。然而debug是伪目标，理论上每次执行都应该运行才对。问题出在debug目标的名称和本地的debug文件夹同名，使用`.PHONY`标识debug为伪目标即可解决此问题。

    :::makefile
    .PHONY: debug

### 不要滥用空白字符
1. `objects = a.o b.o # object files`，这里${objects}变量的值是`a.o b.o '（包含后面的一个空格）。
2. `str = ${subst abc, 123,abcde}`，这里${str}变量的值是` 123de'（包含开头的一个空格）。
3. `str = ${subst abc ,123,abcde}`，这里${str}变量的值还是`abcde`，因为要替换的子串`abc `（包含最后的空格）没有找到。

## 例子
假设有以下的场景，在`src`目录下有许多css文件，我们需要用yui-compressor将其压缩并输出到`output`目录，压缩后css的文件名不变，文件名后缀由`.css`改为`.min.css`，可以如下定义makefile

    :::makefile
    # 查找所有的css源文件
    CSS_SOURCE_FILES = ${wildcard src/*.css}
    # 构建目标名
    CSS_OUTPUT_FILES = ${subst src/,output/,${patsubst %.css,%.min.css,${CSS_SOURCE_FILES}}}

    all: ${CSS_OUTPUT_FILES}
    
    ${CSS_OUTPUT_FILES}: output/%.min.css: src/%.css
        @[ -d output ] || mkdir -p output
        yui-compressor -o $@ $<
    
    clean:
        rm -rf output

    .PHONY: all clean

## 阅读资料
* [GNU Make自动变量，函数和指令索引][7]
* [GNU Make函数说明和列表][12]
* [Passing additional variables from command line to make][8]

[^1]: [GNU Make Manual: The Function wildcard][9]，引用于2014-05-12。

