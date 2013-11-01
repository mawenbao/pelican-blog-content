Title: Makefile
Date: 2013-08-25 12:14
Update: 2013-11-01 10:55
Tags: makefile, tutorial

使用GNU Make 3.8的语法。

## 规则

### order-only依赖

	a: b | c
	    command

上面的例子中，a是目标，b是常规依赖，c是order-only依赖。当a存在时，即便c的修改时间晚于a，该规则也不会更新a。

order-only依赖定义域规则的右侧，与常规依赖用`|`隔开。当目标存在时，不管其是否因order-only依赖而过期，均不更新目标。

## 其它
### 传递变量
可以在命令行里设置Makefile的变量值，对如下的makefile

    TARGET=test
    create:
        make -p ${TARGET}

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

## 参考资料

*  [Passing additional variables from command line to make](http://stackoverflow.com/questions/2826029/passing-additional-variables-from-command-line-to-make)
