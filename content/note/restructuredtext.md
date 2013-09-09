Title: restructuredText
Date: 2013-08-25 12:14
Tags: restructuredText, markup_language

restructuredText相关的东东.
## eclipse plugin

[resteditor](http://resteditor.sourceforge.net/), 该插件依赖[editor color theme](http://eclipsecolorthemes.org/)
插件, 可选择安装.
## 小技巧

### 中文语境里Markup两端空格
rst的许多Markup两端必须是空格, 比如链接、斜体等等. 然而对中文而言这么做很不美观, 折中的办法是使用反斜杠`\`转义的空格:

	
	\ `链接 `<link>`_\ 示例
	这里用\ *斜体*\ 显示

### 图片链接

`<wrap important center 100%>`
无效, 需要检查
`</wrap>`

以替换格式为例, 正确的使用方法是:

	
	|imageA|_
	.. |imageA| image:: http://url-of-the-image

## 参考资料

*  [Quick restructuredText](http://docutils.sourceforge.net/docs/user/rst/quickref.html)
*  [resteditor](http://resteditor.sourceforge.net/) eclipse plugin  
*  [editor color theme](http://eclipsecolorthemes.org/) eclipse plugin
*  [Image within link](https///github.com/jgm/pandoc/issues/678)

