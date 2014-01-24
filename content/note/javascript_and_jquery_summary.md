Title: Javascript和jQuery使用总结
Date: 2013-12-30 15:16
Update: 2014-01-24 11:03
Tags: javascript, jquery, 总结, 未完成

[1]: http://api.jquery.com/category/selectors/
[2]: http://learn.jquery.com/performance/
[3]: http://gregfranko.com/blog/jquery-best-practices/ "jquery best practices"
[4]: http://spoiledmilk.com/blog/html5-changing-the-browser-url-without-refreshing-page/
[5]: http://www.w3.org/TR/2011/WD-html5-author-20110705/history.html#dom-history-pushstate
[6]: https://developer.mozilla.org/en-US/docs/Web/API/Element.getBoundingClientRect
[7]: http://www.jacklmoore.com/notes/mouse-position/

总结近期学到的javascript和jquery知识点，备忘。

## Javascript
### 全局变量
在全局作用域里定义的变量是全局变量，在局部作用域里不用var定义的变量是全局变量，window对象的属性是全局变量[^1]; 在局部作用域里使用var定义的变量是局部变量。

### 修改地址栏的url且不刷新页面
参考[这篇文章][4]，修改url的同时将其加入浏览器的历史里，代码如下。

    window.history.pushState('anything', 'history title', 'url');

pushState函数的具体说明见[这里][5]。

### 获取DOM元素的坐标
`getBoundingClientRect`函数可获取html元素在浏览器可视区域内的坐标和长宽，函数文档见[这里][6]。

### ASCII string and integer
使用`charCodeAt()`和`String.fromCharCode()`可在两者之间进行转换。

    "a".charCodeAt(0);
    // 97

    String.fromCharCode(97 + 1);
    // "b"

## jQuery
### selectors
所有的selectors见[jQuery Selectors][1]，常用的有

*  ID selector: #id, $('#elemId') 根据html元素的id属性获取一个对应的jQuery对象.
*  Class selector: .class, $('.elemClass') 根据html的class属性获取一个jQuery对象列表.
*  CSS selectors: $('#divId ul li') 根据css的selector获取一个jQuery对象列表.
*  Header selector: :header, $(':header') 获取所有的html headers: h1 ~ h6. 

### animate函数
未完成

### 坐标和元素大小
坐标计算。

*  $('#elemId').scrollTop(): 获取已滚过的垂直距离。
*  $('#elemId').scrollLeft(): 获取已滚过的水平距离。
*  $('#elemId').offset(): 获取相对于document的坐标，不同于getBoundingClientRect。
*  $('#elemId').position(): 获取相对于父节点的坐标。

元素大小计算。

*  $('#elemId').height(): 获取高度。
*  $('#elemId').width(): 获取宽度。
*  $(window).height(): 获取浏览器可视区域的高度。
*  $(window).width(): 获取浏览器可视区域的宽度。

鼠标坐标[^2]

*  clientX, clientY: 鼠标在浏览器的viewport内的相对坐标。
*  screenX, screenY: 鼠标在用户屏幕内的相对坐标。
*  pageX, pageY: 鼠标相对于html document的坐标。

### 滚动条的滚动长度计算
滚动条内的元素的实际长度，等于该元素的实际显示长度和滚动条的滚动长度之和。

以整个html页面的垂直滚动条为例，滚动条的滚动长度（将滚动条拖至最低端的时候，$(window).scrollTop()的值），使用`$(document).height() - $(window).height()`计算即可，其中$(document).height()是页面的实际高度，而$(window).height()是页面的实际显示高度。

另外，使用jQuery的animate函数滚动某个带滚动条的元素时，注意animate每次都是从滚动条的最顶端开始滚动，因此如果要每次滚动一点点（比如20px），则需要加上滚动条已滚过的距离，如下。

    var target = $('#some-element');
    target.animate(
        { scrollTop: target.scrollTop() + 20 },
        400
    );

## Performance tips
jQuery性能优化相关的文章可参考[Performance][2]，[jQuery best practices][3]，以下是部分总结。

1. 缓存jQuery selector获取的jQuery对象。

        var myElem = $('#elemId');

        for(var i = 0; i < 100; i++) {
            myElem.attr(...);
        }

2. 需要改变20个以上元素的css样式时，不要用`.css`函数。

        // Fine for up to 20 elements, slow after that:
        $("a.swedberg").css("color", "#0769ad");
         
        // Much faster:
        $("<style type=\"text/css\">a.swedberg { color: #0769ad }</style>").appendTo("head");

3. 遍历数组时，不要每次都调用它的`length`属性。

        var myLength = myArray.length;

        for(var i = 0; i < myLength; i++) {
            // do stuff
        }

4. 添加多个html元素时，尽量一次添加多个，而不是每次添加一个。

        var myHtml = "";
         
        $.each(myArray, function(i, item) {
            myHtml += "<li>" + item + "</li>";
        });

        $("#ballers").html(myHtml);

5. 从DOM里分离html元素。DOM操作很慢且耗费资源，频繁的对DOM中的html元素进行修改会降低效率。

        var $table = $("#myTable");
        var $parent = $table.parent();

        $table.detach();

        // ... add lots and lots of rows to table
        for(var i = 0; i < 1000; i++) {
            $table.append("<tr><td>hello world</td></tr>");
        }

        $parent.append($table);

## 阅读资料
1. [jQuery selectors][1]
2. [HTML5: Changing the browser-URL without refreshing page][4]
3. [pushState函数][5]
4. [getBoundingRect函数][6]
5. [jQuery best practices][3]
6. [jQuery performance tips][2]

[^1]: 多数浏览器里，全局变量都是window对象的属性。
[^2]: 详细介绍参考[Cross-browser mouse positioning][7]。

