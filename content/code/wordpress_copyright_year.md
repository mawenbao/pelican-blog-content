Title: 为wordpress添加版权信息
Date: 2013-08-08 12:14
Tags: php, wordpress, copyright


许多wordpress主题不支持在页脚显示动态年限的版权信息，可以通过修改主题的footer.php来实现这一功能。
## 简单的动态年限代码

    $firstYear = 2012;
    $currentYear = date('Y');
    $copyInfo = "Copyright &copy ";
    if ($firstYear == $currentYear) {
        $copyInfo .= $firstYear;
    } else {
        $copyInfo .= ($firstYear . "-" . $currentYear);
    }
    $copyInfo .= (" `<a href='/blog'>`Wilbur's Home`</a>` - Some Rights Reserved " . "`<a rel='license' href='http://creativecommons.org/licenses/by-nc-nd/3.0/cn/'>``<img alt='知识共享许可协议' style='border-width:0' src='http://i.creativecommons.org/l/by-nc-nd/3.0/cn/80x15.png' />``</a>`");
    echo $copyInfo;

## 参考资料

*  php date http://php.net/manual/en/function.date.php
*  php 字符串操作 http://php.net/manual/en/language.operators.string.php
*  Idea http://wpfirstaid.com/2011/06/dynamic-copyright-revisited/

