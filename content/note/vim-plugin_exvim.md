Title: ExVim
Date: 2013-08-25 12:14
Tags: vim, plugin, shortcut


一直懒于折腾vim，平常也就用它的快捷键。前几天在豆瓣的Vim小组上看到[ExVim](http://www.ex-dev.com/exvim/)的广告，在windows上安装后用了下发现挺顺手，这里简要介绍下。

## 小技巧

*  `<leader>`键默认为`\`
## 错误及解决办法

使用exvim过程中遇到的错误。
### :e test.vimentry报错

按照ExVim维基上的教程创建工程(test)时，访问工程的vimentry文件提示如下错误:

	
	Error: ./.vimfiles.test not found!
	Error detected while processing function g:exES_SetEnviroment..exUtility#CreateQuickGenProject:
	Line 87:
	E482: Can't create file .vimfiles.test/quick_gen_project_pre_custom.bat
	Line 90:
	E482: Can't create file .vimfiles.test/quick_gen_project_post_custom.bat

应该是.vimfiles.test文件夹不存在的缘故，手动创建该文件夹再访问vimentry文件即正常。


