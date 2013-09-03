Title: makefile
Date: 2013-08-25 12:14
Tags: makefile, tutorial

# Makefile

使用GNU Make 3.8的语法。

## 规则

### order-only依赖

	
	a: b | c
	    command

上面的例子中，a是目标，b是常规依赖，c是order-only依赖。当a存在时，即便c的修改时间晚于a，该规则也不会更新a。

order-only依赖定义域规则的右侧，与常规依赖用''|''隔开。当目标存在时，不管其是否因order-only依赖而过期，均不更新目标。
## 参考资料

