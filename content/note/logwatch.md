Title: Logwatch简单配置教程
Date: 2013-08-25 12:14
Tags: logwatch, security, debian, tutorial

简要介绍Debian/Ubuntu和CentOS上logwatch的配置方法和常见错误，详细的配置教程见[参考资料](#参考资料)。
## 配置文件说明

Debian/Ubuntu上logwatch配置目录的结构如下:
	
	/etc/logwatch/
	    conf/             # 配置目录
	        logfiles/         # logwatch日志文件组(*.conf)
	        services/         # logwatch日志服务(*.conf)
	    scripts/          # 可执行脚本
	        logfiles/         # 可包含多个logwatch日志文件组的子目录，对应的logwatch日志服务运行时，子目录下的脚本会自动被调用
	        services/         # logwatch日志服务的脚本
	        shared/           # 可被多个logwatch日志服务引用的脚本
	    logwatch.conf     # 主配置文件

CentOS的logwatch.conf位于/etc/logwatch/conf目录下。
## 例解logwatch配置步骤

用一个简单的例子说明添加logwatch监控的步骤，详细的配置教程见[参考资料](#35808e79fa5f367a06c83a78b857519c)。
### 创建logwatch日志文件组

用一个简单的例子介绍logwatch的配置方法。首先创建logwatch日志文件组配置文件`/etc/logwatch/conf/logfiles/test.conf`:

    LogFile = /path/to/your/logfile
    LogFile = /path/to/your/second/logfile

### 创建logwatch服务过滤器

然后，创建logwatch服务配置文件`/etc/logwatch/conf/services/test.conf`:

    Title = IMCS     # 日志文件里的标题
    LogFile = test   # logwatch日志文件组的名字，通常是对应的配置文件的文件名部分

### 创建logwatch服务过滤器脚本

创建logwatch服务的过滤器脚本`/etc/logwatch/scripts/services/test`:

    #!/bin/bash

    grep -i ERROR

上面的脚本会从日志文件里过滤出包含`ERROR`的行。最后，为新建的脚本添加执行权限:

    chmod +x /etc/logwatch/scripts/services/test

## 主配置文件logwatch.conf

在logwatch.conf里添加或修改如下选项可以将监控报告以html的格式发送到你的邮箱里。

    Output = html                # 生成html格式的报告
    MailTo = your_email_address  # 定义你的邮箱地址
## 常见错误解决

记录logwatch常见错误的解决方法。
### 无法发送邮件

CentOS5.4上使用sendmail发送邮件。正常运行一段时间后，突然不再发送邮件。检查后发现，配置一切正常，可以手动发邮件，使用logwatch的`--print`选项输出正常。

最后在`logwatch --print`的输出里发现如下信息:
	
	Large Mailbox threshold: 40MB (41943040 bytes)
	  Warning: Large mailbox: root (257959878)

解决办法是清空旧的mailbox(/var/spool/mail/root)或将mailbox上限调大。参考[这里](http://haprakjingga.wordpress.com/2008/07/11/setting-sendmail-largeboxes-in-logwatch-report/)的方法，将`/usr/share/logwatch/default.conf/services/sendmail-largeboxes.conf`的`sendmail_largeboxes_size`变量设置的大一些即可。
## 参考资料

*  [HOWTO Customize LogWatch](http://web.archive.org/web/20080822051428/http://www.logwatch.org/tabs/docs/HOWTO-Customize-LogWatch.html)
*  [Managing your log files](http://tuxradar.com/content/managing-your-log-files)
*  [Logwatch with metalog](http://en.gentoo-wiki.com/wiki/Logwatch_with_Metalog)
*  [Setting sendmail-largeboxes in logwatch report](http://haprakjingga.wordpress.com/2008/07/11/setting-sendmail-largeboxes-in-logwatch-report/)

