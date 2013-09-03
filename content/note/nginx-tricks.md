Title: nginx tricks
Date: 2013-08-25 12:14
Tags: nginx, trick

# Nginx小技巧

收集使用nginx过程中发现的小技巧。

## 配置技巧

这里记录一些nginx配置方面的技巧。
### 访问txt文件时提示下载

txt文件的MIME类型为text/plain，使用浏览器访问时默认行为是直接在浏览器中显示。如果需要将默认行为改为直接下载，可以在nginx配置文件中添加如下规则即可。
    location ~* \.(txt) {
      add_header Content-Disposition "attachment";
    }
对于某些特殊的文件，如果在访问时需要直接在浏览器上显示文件内容，则可使用如下规则，以gpg的asc加密文件为例。
    location ~* \.(asc) {
      default_type text/plain;
      add_header Content-Disposition "inline";
    }
## 参考资料

*  [How can I make sure that Nginx serves plaintext files as a download, instead of inline?](http://serverfault.com/questions/364370/how-can-i-make-sure-that-nginx-serves-plaintext-files-as-a-download-instead-of)

