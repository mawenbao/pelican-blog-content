Title: SMTP协议相关知识总结
Date: 2013-12-18 10:58
Tags: 总结, email, smtp

[1]: http://tools.ietf.org/html/rfc5321 "RFC5321"
[2]: http://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol
[3]: http://the-welters.com/professional/smtp.html "SMTP Commands"
[4]: http://en.wikipedia.org/wiki/MIME
[5]: http://en.wikipedia.org/wiki/Extended_SMTP

SMTP(Simple Mail Transfer Protocol), 是邮件的传输协议，用于从邮件客户端向邮件服务器发送电子邮件，协议的具体定义可参考[rfc5321][1]。Linux上常用的邮件服务器有postfix和exim4等，默认端口是25。

## SMTP命令
### 常用命令
常用的主要有5个，按实际使用顺序，分别为HELO, MAIL, RCPT, DATA和QUIT。

    HELO relay.example.org
    MAIL FROM:<bob@example.org>
    RCPT TO:<alice@example.com>
    RCPT TO:<theboss@example.com>
    DATA
    mail header

    mail body
    QUIT

HELO向邮件服务器初始化一次会话，MAIL设置发信人地址，RCP设置收信人地址，可以有多个，DATA表示之后为邮件内容（包括邮件头和邮件正文），最后QUIT结束该会话。

详细的命令介绍可参考[SMTP Commands][3]。

### HELO vs EHLO
HELO和EHLO命令都可用于向邮件服务器初始化一个会话，不同的是EHLO对HELO进行了扩展以支持[Extended SMTP][2]。

## 易混淆点
### 行分隔符
邮件头每一行末尾使用CRLF(`\r\n`)结束，邮件头和邮件正文使用一个空行分割。例如

    From: mawenbao@hotmail.com\r\nTo: hello@world.com\r\nSubject: Hello world\r\n\r\nThis is the email body.

### Base64编码正文
如果用Base64对邮件正文进行编码，邮件头中应设置

    Content-Transfer-Encoding: base64

## 其他相关知识
### MIME
MIME(Multipurpose Internet Mail Extensions)对电子邮件格式进行扩展，以支持非ASCII字符集，非文本文件附件和multipart的邮件正文等。详细信息可参考[wikipedia:MIME][4]。

常用MIME头有MIME-Version, Content-Type和Content-Transfer-Encoding，MIME-Version标识MIME版本，Content-Type说明邮件正文的编码和格式。比如

    From: mawenbao@hotmail.com
    To: hello@world.com
    Subject: hello world
    MIME-Version: 1.0
    Content-Type: text/html; charset="UTF-8"

    <html><head></head><body><h1>Hello world</h1>

为方便阅读，在上面的例子中，所有的\r\n换行符均使用回车替换。

## 阅读资料
1. [RFC5321][1]
2. [wikipedia:Simple Mail Transfer Protocol][2]
3. [wikipedia:Extended SMTP][5]
4. [wikipedia:MIME][4]
5. [SMTP Commands][3]

