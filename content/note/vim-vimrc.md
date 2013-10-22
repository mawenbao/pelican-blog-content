Title: VIMRC收集
Date: 2013-08-25 12:14
Tags: vim, config
Update: 2013-10-22 16:08

[1]: http://yyq123.blogspot.com/2009/10/vim-statusline.html "http://yyq123.blogspot.com/2009/10/vim-statusline.html"
[2]: http://superuser.com/questions/322865/how-to-make-vim-always-show-the-encoding-of-current-opened-file
[3]: https://github.com/amix/vimrc "https://github.com/amix/vimrc"
[4]: http://vim.wikia.com/wiki/Highlight_unwanted_spaces "http://vim.wikia.com/wiki/Highlight_unwanted_spaces"
[5]: http://vim.wikia.com/wiki/Remove_unwanted_spaces "http://vim.wikia.com/wiki/Remove_unwanted_spaces"

记录vim的配置方法，收集好的vim配置文件。

## vim配置文件。
在linux系统上，vim的配置文件入口是`~/.vimrc`，下面是一些优秀的vim配置文件。

*  [The Ultimate vimrc][3]

## vim配置

### 设置状态行status line
总是开启状态行

    set laststatus=2

关闭状态行

    :set laststatus=0

具体的配置可参考[VIM学习笔记 状态行(statusline)][1]这篇文章，我的配置是:

    set laststatus=2 "总是开启状态行
    set statusline=\ %F%m%r%h\ %w\ \ \ \ %{&ff}:%{&fenc!=''?&fenc:&enc}\ \ \ \ %l,%c:%p%%

状态行依次显示 文件路径[是否只读][是否修改过] 文件格式(unix或dos):文件编码 行号,列号:当前阅读百分比

### tab和space等空白字符设置

设置tab

    set tabstop=4 "tab宽度设为4个空格
    set shiftwidth=4 "自动缩进为4个空格
    set expandtab  "使用space代替tab 

高亮多余的空白字符，参考[Highlight unwanted spaces][4]。

    highlight ExtraWhitespace ctermbg=red guibg=red
    match ExtraWhitespace /\s\+$/
    autocmd BufWinEnter * match ExtraWhitespace /\s\+$/
    autocmd InsertEnter * match ExtraWhitespace /\s\+\%#\@<!$/
    autocmd InsertLeave * match ExtraWhitespace /\s\+$/
    autocmd BufWinLeave * call clearmatches()

保存文档时删除行尾多余的空白字符(trailing whitespaces)，参考[Remove unwanted spaces][5]。

    autocmd BufWritePre * :%s/\s\+$//e

## 参考资料

*  [VIM学习笔记 状态行(statusline)][1]
*  [How to make vim always show the encoding of current opened file?][2]
*  [Highlight unwanted spaces][4]
*  [Remove unwanted spaces][5]

