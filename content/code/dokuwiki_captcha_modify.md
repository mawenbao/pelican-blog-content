Title: 修改dokuwiki的captcha插件
Date: 2013-08-08 12:14
Tags: php, dokuwiki, captcha

修改dokuwiki的captcha插件，为登录表单也添加验证码(captcha)支持，可以在配置页面开启或关闭登录表单的验证码框。

## 代码

修改后的代码在[这里](https///github.com/wilbur-ma/dokuwiki-tweak/tree/master/plugin-captcha)，2010-06-07发布的captcha插件的patch在[这里](https///raw.github.com/wilbur-ma/dokuwiki-tweak/master/patch/captcha-plugin.patch)下载。在插件文件夹使用如下命令即可:
    patch -p2 < captcha-plugin.patch
## 遇到的问题

###  global $ID"" =====
原因未知，尚待解决

在`AUTH_LOGIN_CHECK`的handler里使用`global $ID`后，`$ID`实际为空字符串，原因暂且未知，改用`getID()`函数后即可解决这一问题。
## 参考资料

*  [Dokuwiki Event System](doku>devel/events)
*  [DokuWiki Event Handlers](doku>devel/event_handlers)
*  [Dokuwiki Event Reference List](doku>devel/events_list)
*  [Dokuwiki Core Overview](doku>devel/overview)
*  [Dokuwiki Environment](doku>devel/environment)
*  [Action Modes aka. do Modes](doku>devel/action_modes)
*  [Dokuwiki CAPTCHA plugin](doku>plugin/captcha)

