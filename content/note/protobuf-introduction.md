Title: Google Protocol Buffers介绍和总结
Date: 2013-10-24 16:13
Update: 2013-12-03 16:30
Tags: google, protobuf, library, tutorial

[1]: https://developers.google.com/protocol-buffers/docs/techniques#large-data "https://developers.google.com/protocol-buffers/docs/techniques#large-data"
[2]: https://developers.google.com/protocol-buffers/ "https://developers.google.com/protocol-buffers/"
[3]: http://www.ibm.com/developerworks/cn/linux/l-cn-gpb/ "http://www.ibm.com/developerworks/cn/linux/l-cn-gpb/"
[4]: https://github.com/mawenbao/protobuf-demo "https://github.com/mawenbao/protobuf-demo"

简要介绍和总结protobuf的一些关键点，从我之前做的ppt里摘录而成，希望能节省protobuf初学者的入门时间。[这是][4]一个简单的Demo。

## Protobuf 简介

Protobuf全称Google Protocol Buffers

*  [http://code.google.com/p/protobuf](http://code.google.com/p/protobuf)
*  结构化数据存储格式(xml, json)
*  用于通信协议、数据存储等
*  高效的序列化和反序列化
*  语言无关、平台无关、扩展性好
*  官方支持C++, Java, Python三种语言

## .proto文件

### 定义和使用
消息定义文件user_def.proto

    package user;
    message UserInfo { 
        required int64 id = 1;
        optional string name = 2;
        repeated bytes nick_name = 3;
    }

编译.proto，生成解析器代码

    protoc --cpp_out . user.proto  // user_def.pb.h user_def.pb.cc
    protoc --java_out . user.proto // user/UserInfo.java

### 字段ID

optional string name = `2`;

*  唯一性 
*  序列化后，1~15占一个字节，16~2047占两个字节

### 字段类型 

*  [https://developers.google.com/protocol-buffers/docs/proto#scalar](https://developers.google.com/protocol-buffers/docs/proto#scalar)
*  string vs. bytes

    .proto类型 | c++类型     | java类型   | 说明
    ---------- | ----------- | ---------- | ----------------------
    string     | std::string | String     | 必须是UTF-8或ASCII文本
    bytes      | std::string | ByteString | 任意的字节序列

### 编写建议

1. 常用消息字段(尤其是repeated字段)的ID尽量分配在1~15之间。
2. 尽可能多的（全部）使用optional字段。
3. 命名方式
    *  .proto文件名用underscore_speparated_names。
    *  消息名用CamelCaseNames。
    *  字段名用underscore_separated_names。

### 兼容性建议

1. 不能修改字段的ID。
2. 不能增删任何required字段。
3. [https://developers.google.com/protocol-buffers/docs/proto#updating](https://developers.google.com/protocol-buffers/docs/proto#updating)

## 序列化后的protobuf消息

*  一序列的键值对，键是消息字段的ID。
*  已知消息字段(.proto文件定义)按其ID顺序排列。
*  未知消息字段：
    *  c++和java: 排在已知字段之后且顺序不定。
    *  python: 不保留未知字段。
*  不包含未赋值的optional消息字段。
*  使用little-endian字节序存储。

## Protobuf优势

1. 扩展性好
    *  前后兼容
    *  引入(import)已定义的消息
    *  嵌套消息
2. 高效 [https://code.google.com/p/thrift-protobuf-compare/wiki/Benchmarking](https://code.google.com/p/thrift-protobuf-compare/wiki/Benchmarking)
    *  适合处理大量小数据(单个Message不超过1M)

## Protobuf劣势

1. 没有内置的Set, Map等容器类型。
2. 不适合处理单个Message超过1M的情景，详见[Large Data Sets][1]。

## 进一步阅读

*  .proto指南 [https://developers.google.com/protocol-buffers/docs/proto](https://developers.google.com/protocol-buffers/docs/proto)
*  .proto规范 [https://developers.google.com/protocol-buffers/docs/style](https://developers.google.com/protocol-buffers/docs/style)
*  序列化编码方式 [https://developers.google.com/protocol-buffers/docs/encoding](https://developers.google.com/protocol-buffers/docs/encoding)
*  教程 [https://developers.google.com/protocol-buffers/docs/tutorials](https://developers.google.com/protocol-buffers/docs/tutorials)
*  接口文档 [https://developers.google.com/protocol-buffers/docs/reference/overview](https://developers.google.com/protocol-buffers/docs/reference/overview)
*  Protobuf benchmarking [https://code.google.com/p/thrift-protobuf-compare/wiki/Benchmarking](https://code.google.com/p/thrift-protobuf-compare/wiki/Benchmarking)

## 阅读资料

*  [Protobuf documentation][2]
*  [Protobuf的使用和原理][3]

