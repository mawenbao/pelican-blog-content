Title: GnuPG快速使用指南
Date: 2013-08-25 12:14
Update: 2013-11-18 21:17
Tags: gnupg, tutorial

简单的GnuPG教程，重点介绍GnuPG的常用命令，更详细的使用说明请参考[GnuPG](http://www.gnupg.org/)的官方文档。

需要注意的是，以下内容均以GnuPG 1.4为基础进行说明。

## GnuPG常用命令

假设生成公钥/密钥时使用的UID为`wilbur ma`，并以此为例。 
### 生成新的钥匙

生成一对新的钥匙((钥匙指公钥和密钥)):

    gpg --gen-key

### 发送公钥

将UID为`wilbur ma`的公钥发送到GnuPG服务器，这样其他人可以直接使用[查找命令](#查找公钥)获取该公钥。

首先需要获取公钥的ID，使用如下命令查看:

    gpg --list-keys

输出如下:

    pub   2048R/A8FC260E 2012-12-12
    uid                  Wilbur Ma `<wilbur.ma@hotmail.com>`
    sub   2048R/F40188FA 2012-12-12  

则公钥的ID为`A8FC260E`，使用该ID发送公钥至'hkp://keys.gnupg.net'服务器:

    gpg --keyserver hkp://keys.gnupg.net --send-keys A8FC260E

### 查找公钥

在GnuPG服务器上使用名字或邮件地址查找公钥并导入钥匙环:

    gpg --keyserver hkp://keys.gnupg.net --search-keys wilbur.ma@hotmail.com

### 导出公钥

使用ASCII形式导出公钥。其中，`wilbur ma`为生成密钥时使用的名字:

    gpg -a -o "pubkey.txt" --export 'wilbur ma'   

### 导入公钥/密钥

导入上面导出的公钥:

    gpg --import pubkey.txt

导入公钥后需要首先对公钥进行签名，假设导入公钥的邮件地址为`wilbur.ma@hotmail.com`:

    gpg --edit-key wilbur.ma@hotmail.com
    trust

然后选择你的信任程度即可。

### 撤销钥匙

假设需要撤销ID为A8FC260E的公钥，首先生成撤销证书revoke.key:

    gpg -a -o revoke.key --gen-revoke A8FC260E

将revoke.key导入钥匙环中即可撤销本地的证书:

    gpg --import revoke.key

将被撤销的公钥的ID发送到钥匙服务器上即可撤销服务器上的公钥:

    gpg --keyserver hkp://keys.gnupg.net --send-keys A8FC260E

现在查看服务器上你的公钥，可以看到revoked字样。需要注意的是，撤销证书需要妥善保管，因为任何有权获取该证书的人均可撤销你的钥匙。

###  加密与解密 

使用UID为`wilbur ma`的公钥加密一段话，比如`hello world`:

    echo 'hello world' | gpg -a -r 'wilbur ma' -e > cipher.txt

生成类似如下形式的文件:

    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1.4.10 (GNU/Linux)

    hQEMA68owEX0AYj6AQf9Hi6HGLNIBTAGn/UqZMb98KCF4y+Nhph+Laua/eK7reE0
    3Pat6xMvkqAJUjpDSsHHHngTmG0/3MLA8XNj90AmVyii9MJXuh9bO1X1Sbi/SK5v
    jQfFgmmwz2WL6q61oOzRrE5xB0WGslOsIwk4SHBAqrjBPTfElmyzn3suh1smi4Hb
    jb8trfjqwTfioCzU0pk4a1yc3Bnhrbq4bpdnJ0NHI94JULOZAuSU3CajCJ17q973
    VXlq7o8GIqBb4Yr636Jzk0cIVmXUTYb1Zv4QiAmW6SypTE32qOW0iNDMRkNi1PYm
    AjdSNnB0zm59Qmw+EZtvXbTpk1k82Sajbx9ZlIvjc9JHAeQXQ0iEODueDFaKYjHX
    rNMCWyHjgYUn0YbF/6HH+30EffCjzFI3JHrJRf7Z/sxL43qhXpOH8DvsXn5hfWMo
    FwoxN5w7Ffk=
    ###### o6xx

    -----END PGP MESSAGE-----

使用UID为`wilbur ma`的公钥加密文件plain.txt，生成cipher.txt:

    gpg -r 'wilbur ma' -a -o cipher.txt -e plain.txt 

使用UID为`wilbur ma`的密钥解密上面生成的文件cipher.txt，需要输入该密钥的指纹(密码):
    
    gpg -r 'wilbur ma' -d cipher.txt

### 签名与验证

如果希望签名信息与文件内容同时存在于签名后的文件中，则可以执行如下命令。该命令使用UID为`wilbur ma`的密钥对文件plain.txt进行签名，输出为plain.sign.txt(包含原文件内容和签名信息):

    gpg -r 'wilbur ma' -o 'plain.sign.txt' --clearsign plain.txt

验证同时包含文件内容和签名信息的签名文件plain.sign.txt:

    gpg --verify plain.sign.txt

若输出`Good signature from...`之类的信息则表示验证成功，文件签名有效; 倘若输出`BAD signature from...`之类的信息，则说明文件验证失败，此时不应当信任被签名文件。

同时进行加密和签名操作:

    gpg -r 'wilbur ma' -a -o sign.txt -s -e plain.txt

解密并验证sign.txt:

    gpg -o new.txt -d sign.txt

如果希望签名信息存放于单独的文件中，则执行如下命令。该命令使用UID为`wilbur ma`的密钥对文件plain.txt进行签名，签名信息保存在plain.sig文件中，原文件不变:

    gpg -r 'wilbur ma' -a -o plain.sig -b plain.txt    

使用签名文件plain.sig验证被签名文件plain.txt:

    gpg --verify plain.sig plain.txt

### 管理钥匙

查看当前用户的所有公钥:

    gpg --list-keys

查看当前用户的所有密钥:

    gpg --list-secret-keys

编辑UID为`wilbur ma`的公钥，可以修改公钥的过期时间、指纹，以及对公钥进行签名(是否信任)，使用`help`查看所有可用操作。

    gpg --edit-key 'wilbur ma'

删除UID为`wilbur ma`的公钥:

    gpg --delete-key 'wilbur ma'

删除UID为`wilbur ma`的密钥:

    gpg --delete-secret-key 'wilbur ma'

## GnuPG钥匙安全

[Never ever encrypt and sign using the same key](http://serverfault.com/questions/397973/gpg-why-am-i-encrypting-with-subkey-instead-of-primary-key), because signing and decrypting are actually identical operations in the math of public-key encryption.

### 多对subkey

简单的解决办法是使用不同的subkey进行Encrypt和Sign操作，具体操作方法可参考Debian wiki上的[这篇文章](http://wiki.debian.org/subkeys)。为Encrypt和Sign分别创建单独的subkey后，使用`--edit-key`选项时，列出的钥匙应当类似于下面的样式:

    pub  2048R/950A754E  created: 2012-12-17  expires: never       usage: SC  
                       trust: ultimate      validity: ultimate
    sub  2048R/AA84BDB5  created: 2012-12-17  expires: never       usage: E   
    sub  2048R/680D52A1  created: 2012-12-17  expires: never       usage: S   
    [ultimate] (1). Tom (Tom Cat) `<tom@example.com>`

其中，usage后面的字符代表的意思分别为:

*  E = encrypt/decrypt (decrypt with your private key of a message you received)
*  S = sign (sign data. For example a file or to send signed e-mail)
*  C = certify (sign another key, establishing a trust-relation)
*  A = authentication (log in to SSH with a PGP key; this is relatively new usage)

#### 实际使用
为保证private master key的安全，将其放到离线的其他介质（比如U盘），并从钥匙环中删除。同时为方便日常使用，需要分别创建一个负责加密的subkey（默认已有）和一个负责签名的subkey。

首先创建密钥，注意替换`KEY_ID`为密钥的实际ID。

    :::bash
    # 创建新的钥匙对，默认会额外创建一个负责加密的subkey
    gpg --gen-key
    
    # 创建一个负责签名的subkey
    gpg --edit-key KEY_ID
    > addkey
    > select RSA (sign only)

    # 生成吊销证书（可选），!!生成的吊销证书必须妥善保管!!
    gpg -a -o KEY_ID.revoke.asc --gen-revoke

接下来，将`~/.gnupg`目录备份到U盘上

    :::bash
    cp -r ~/.gnupg /path/to/your/usb-drive/_gnupg

接下来，分别导出密钥（包含subkeys）和subkeys

    :::bash
    # 导出密钥（包含subkeys）
    gpg -a -o KEY_ID.sec.asc --export-secret-keys KEY_ID
    # 导出subkeys
    gpg -a -o KEY_ID.sub.asc --export-secret-subkeys KEY_ID

删除private master key之前，使用`gpg --list-secret-keys`可输出（举例）

    /home/wilbur/.gnupg/secring.gpg
    -------------------------------
    sec   4096R/A571E81D 2013-11-18 [有效至：2014-11-18]
    uid                  Ma Wenbao <mawenbao@hotmail.com>
    ssb   4096R/7F08122C 2013-11-18
    ssb   4096R/AC317C91 2013-11-18

通过如下两步间接删除private master key

    :::bash
    # 删除密钥
    gpg --delete-secret-keys
    # 导入subkeys
    gpg --import KEY_ID.sub.asc

    # 删除中间文件
    rm KEY_ID.sec.asc KEY_ID.sub.asc

此时，再执行`gpg --list-secret-keys`应当输出

    /home/wilbur/.gnupg/secring.gpg
    -------------------------------
    sec#  4096R/A571E81D 2013-11-18 [有效至：2014-11-18]
    uid                  Ma Wenbao <mawenbao@hotmail.com>
    ssb   4096R/7F08122C 2013-11-18
    ssb   4096R/AC317C91 2013-11-18

注意第三行的`sec`变成了`sec#`，表示private master key不存在。如此一来，master private key就被删掉了，日常加密和签名操作都通过subkeys进行，需要使用master private key时，挂载U盘然后执行如下操作就能看到master private key了。

    gpg --homedir /path/to/your/usb-drive/_gnupg --list-secret-keys

通常，如下三种情况需要使用到private master key

*  为他人的公钥签名
*  创建subkey
*  吊销subkey

为他人的公钥签名时，可先使用U盘上的gnupg配置文件签名，然后可导出签名后的公钥，最后再导入本地钥匙环中，操作如下

    :::bash
    # 下载某人的公钥
    gpg --homedir /path/to/your/usb-drive --keyserver hkp://keys.gnupg.net --recv-keys A571E81D
    # 为他人的公钥签名
    gpg --homedir /path/to/your/usb-drive --sign-key A571E81D
    # 导出签名后的公钥
    gpg --homedir /path/to/your/usb-drive -a -o A571E81D.pub.asc --export A571E81D
    # 导入本地钥匙环
    gpg --import A571E81D.pub.asc

### 多对key

相对更安全(更麻烦)的方法是创建两对钥匙，一对用于Sign操作，一对用于Encrypt操作。这样一来，其他用户需要同时拥有并签署你的两把钥匙。

## 参考资料

*  [Public-key cryptography](http://en.wikipedia.org/wiki/Public_key) from wikipedia
*  [Home page of GnuPG](http://www.gnupg.org/)
*  [GnuPG Mini Howto中文版](http://www.gnupg.org/howtos/zh/index.html)
*  [Gnu Privacy Guard Howto](https://help.ubuntu.com/community/GnuPrivacyGuardHowto) from Ubuntu wiki
*  [Creating a new GPG key](http://keyring.debian.org/creating-key.html) from Debian wiki
*  [Subkeys](http://wiki.debian.org/subkeys) from Debian wiki
*  [Multiple keys or multiple subkeys](http://www.macfreek.nl/memory/GPG_mail_signing#Multiple_Keys_or_Multiple_Subkeys)
*  [GPG quick start](http://www.madboa.com/geek/gpg-quickstart/)

