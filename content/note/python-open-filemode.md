Title: python open() filemode
Date: 2013-08-29 15:12:00
Tags: python, note

# Python内置函数open()打开模式总结
总结python2.7中open函数的打开模式。

## open()
参考python2.7的网上文档:

    open(name[, mode[, buffering]])

    Open a file, returning an object of the file type described in section File Objects. If the file cannot be opened, IOError is raised. When opening a file, it’s preferable to use open() instead of invoking the file constructor directly.

    The first two arguments are the same as for stdio‘s fopen(): name is the file name to be opened, and mode is a string indicating how the file is to be opened.

## 各模式总结
依据python2.7的文档可知，open的mode参数和fopen的mode参数作用一致。下面是简单的总结：

*  r: 只能读，文件必须已存在
*  w: 只能写，文件不存在则创建之
*  r+: 可读写，文件必须存在，open后不会清空（truncate）文件的内容
*  w+: 可写读，文件不存在则创建之，已存在则在open后立刻清空（truncate）文件的内容

## 参考资料
*  [python2.7 documentation for open()](http://docs.python.org/2/library/functions.html#open)
*  [cplusplus fopen()](http://www.cplusplus.com/reference/cstdio/fopen/)
*  [Confused by python file mode “w+”](http://stackoverflow.com/questions/16208206/confused-by-python-file-mode-w) 
