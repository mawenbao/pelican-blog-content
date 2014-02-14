Title: Chrome扩展编写总结
Date: 2014-02-14 14:59
Tags: Chrome, 扩展, plugin, 总结, 未完成

[1]: http://developer.chrome.com/extensions/devguide.html
[2]: http://developer.chrome.com/extensions/storage.html#sync-properties
[3]: http://developer.chrome.com/extensions/storage.html#local-properties
[4]: http://developer.chrome.com/extensions/storage.html
[5]: http://developer.chrome.com/extensions/getstarted.html
[6]: http://developer.chrome.com/extensions/overview.html
[7]: http://developer.chrome.com/extensions/i18n.html
[8]: https://developers.google.com/chrome/web-store/docs/i18n#localeTable

总结编写Chrome扩展时遇到的问题和相关注意事项，并收集与开发相关的资源，备忘。

## 入门教程
入门教程直接看官方的[Get Started][5]和[Overview][6]即可。

## Chrome接口
### 存储
存储接口的文档见[chrome.storage][4]。

Chrome的存储分同步存储区域(sync storage are)和本地存储区域(local storage are)。同步存储区域里的数据可以通过Chrome sync同步到网络账户中，而本地存储就存在用户的终端设备上。二者的接口完全一致，都是`chrome.storage.STORAGE_AREA.XXOO()`，使用时将STORAGE_AREA换为sync或local即可，具体的函数列表参考[接口文档][4]。

需要注意的是，Chrome存储有一定的配额。对同步存储区域而言，总存储量不能超过100K，单条存储不得超过4K，且最多存储512个条目(item)，详情见[sync-properties][2]。本地存储的配额相对大一些，总量不超过5M即可，单条存储没有限制，详情见[local-properties][3]。

### 国际化
接口文档见[chrome.i18n][7]。

相关的文件需要放在`_locales`文件夹里，并且在`manifest.json`里需要设置`default_locale`，Chrome支持的locale列表见[locale tables][8]。 

在css文件里可以通过`__MSG__MessageName__`来调用调用翻译，在js中可以通过`getMessage`函数来调用翻译。目前还不支持在html文件中调用翻译。

## 注意事项
1. 修改扩展的代码后，最好在`chrome://extensions/`里重新加载(Reload)一下。

## 阅读资料
1. [Chrome 开发指南][1]

