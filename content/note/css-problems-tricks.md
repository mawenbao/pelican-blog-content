Title: CSS技巧和问题整理
Date: 2014-01-02 17:33
Tags: css, problem, trick

[1]: http://www.w3.org/TR/CSS2/tables.html#height-layout
[2]: http://stackoverflow.com/questions/1993277/css-table-layout-why-does-table-row-not-accept-a-margin "Position: fixed changes width of element when using percentages"
[3]: http://www.sitepoint.com/forums/showthread.php?752068-How-to-add-padding-amp-margin-to-LI-elements-with-display-table-row "How to add padding & margin to LI elements with display:table-row?"
[4]: http://stackoverflow.com/questions/1993277/css-table-layout-why-does-table-row-not-accept-a-margin "CSS table layout - why does table-row not accept a margin?"

整理日常使用CSS时遇到的问题和技巧。

## CSS技巧
### word-wprap研究。
word-wrap: break-word;
word-break

## CSS问题
### #1
使用百分数定义width的div，其position变为static之后，宽度发生突变。具体问题见[这里][2]。

解决方法在position变为static之后添加：

    width: inherit;


### #2
具有`display: table-row`的元素无法设置margin。具体问题见[这里][4]。

问题的原因在[http://www.w3.org/TR/CSS2/tables.html#height-layout][1]有介绍，简单的说（引用stackoverflow上的回答），就是：

> When you use display:table-row, the height of the DIV is solely determined by the height of the table-cell elements in it. Thus, margin, padding, and height on those elements have no effect.

解决办法是为table-cell设置height，参考了某个论坛上的一个[帖子][3]。

## 参考资料
1. [css2: tables][1]
2. [Position: fixed changes width of element when using percentages][2]
3. [How to add padding & margin to LI elements with display:table-row?][3]
4. [CSS table layout - why does table-row not accept a margin?][4]

