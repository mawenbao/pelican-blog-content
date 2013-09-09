Title: Python PIL 例子
Date: 2013-08-08 12:14
Tags: python, PIL


PIL(Python Imaging Library)是Python的标准图像库，下面是一个生成文本图像的简单例子。
## 开发环境

Require:

*  Python 2.6 or Python 2.7
*  arrial.ttf 字体文件
## 代码

### lan.txt
定义生成图片时的文本，每行生成一张图片。

	bash
	c
	cpp
	csharp
	css
	diff
	erlang
	html
	ini
	java
	javascript
	jquery
	lisp
	lua
	make
	perl
	php
	powershell
	python
	ruby
	scheme
	sql
	tcl
	text
	vb
	vim
	xml
	vim
	conf

### genPics.py

生成图像的主程序文件，读取lan.txt并将每行的数据使用arrial.ttf字体生成一张png图片。

    :::python
	#!/usr/bin/env python
	 
	import Image, ImageFont, ImageDraw
	import os
	
	picDir = "16pics"
	if not os.path.exists(picDir):
	    os.makedirs(picDir)
	
	# read language names
	lanNames = []
	with open("lan.txt", "r") as f:
	    lanNames = f.readlines()
	
	# width and height of each picture
	width, height = 80, 30
	# font settings
	fontPath = "arial.ttf"
	fontSize = 14
	font = ImageFont.truetype(fontPath, fontSize) 
	
	for n in lanNames:
	    n = n.strip()
	    img = Image.new("RGB", (width, height), "white")
	    draw = ImageDraw.Draw(img)
	    fontWidth, fontHeight = font.getsize(n)
	    draw.text(((width-fontWidth)/3, (height-fontHeight)/4), n, font=font, fill="black")
	    imageLoc = "%s/syntax_%s.png" % (picDir, n)
	    img.save(imageLoc, "png")
	    print("Generate %s" % imageLoc)

## 参考资料

*  [PIL Tutorial](http://effbot.org/imagingbook/)
*  [PIL文档](http://www.pythonware.com/library/pil/handbook/index.htm)

