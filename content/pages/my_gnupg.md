Title: 我的公钥
Date: 2012-12-14 20:36:23
Update: 2013-11-18 11:15
Comment: off

## 何时使用公钥
如果需要给我发送一些私密信息或者验证我签署的文件，你可能会用到我的公钥。

## 获取我的公钥
基于安全考虑，推荐直接从gpg服务器获取并导入我的公钥。关于gpg的使用，可以参考我整理的[GnuPG快速使用手册](/note/gnupg.html "GnuPG快速使用指南")。

我的公钥可直接从gpg服务器上获得，运行以下命令即可。

    gpg --keyserver hkp://keys.gnupg.net --recv-keys A571E81D

导入成功之后，首先用你的密钥对我的公钥进行签名，执行如下命令即可。

    gpg --sign-key A571E81D

## 更新我的公钥
如果你以前用过我的公钥，用之前只需更新即可。

    gpg --keyserver hkp://keys.gnupg.net --refresh-keys A571E81D

## 使用我的公钥进行加密或验证
执行如下命令把plain.txt加密为cipher-message.txt，然后把cipher-message.txt发送给我即可。

    gpg -r mawenbao@hotmail.com -a -o cipher-message.txt -e plain.txt

验证文件是否来自我本人。收到我签名的文件reply.txt后，执行以下命令。

    gpg --verify reply.txt

如果输出Good signature from…之类的信息则表示验证成功，说明reply.txt的确来自我本人。

通常情况下，我会发送加密过的签名文件，此时运行如下命令解密并验证文件。其中reply-cipher.txt为加密并签名过的文件，reply-plain.txt为解密后的文件。

    gpg -o reply-plain.txt -d reply-cipher.txt

如果运行命令后输出Good signature from…之类的信息则表示验证成功。倘若输出Bad signature from…之类的信息则表示验证失败，说明reply-plain.txt里的内容很有可能不是来自我本人。
