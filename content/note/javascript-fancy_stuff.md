Title: Javascript Fancy Stuff
Date: 2013-08-25 12:14
Tags: javascript, note

收集一些华丽的Javascript工具或代码。

## 侧边栏自动滚动

参考[stackoverflow](http://stackoverflow.com/questions/9350461/how-to-add-css-style-if-user-scroll-page-over-112px/9350600#9350600)上的问题和[这个jquery插件](https://github.com/cheald/floatingFixed/blob/master/jquery.floatingFixed.js).

html代码如下:

	`<div id="p-toc">`
	目录
	...
	`</div>`

css代码如下:

	/* scrool sidebar toc */
	#p-toc {
	    overflow-y: auto;
	    height: 90%;
	}
	.sidebar-absolute {
	    width: 160px;
	    position: absolute;
	}
	.sidebar-fixed {
	    top: 0px;
	    width: 160px;
	    position: fixed;
	}

js代码如下:

	(function(){
	    var oDiv=document.getElementById("p-toc");
	    var H=0,iE6;
	    var Y=oDiv;
	    while(Y){H+=Y.offsetTop;Y=Y.offsetParent};
	    iE6=window.ActiveXObject&&!window.XMLHttpRequest;
	    if(!iE6){
	        window.onscroll=function() {
		    var s=document.body.scrollTop||document.documentElement.scrollTop;
		    if (s>H) {
		        oDiv.className="portal sidebar-fixed";
		        if (iE6) {
			    oDiv.style.top=(s-H)+"px";
			}
		    } else {
		        oDiv.className="portal sidebar-absolute";
		    }
		};
	    }
	})();

## 阅读资料

