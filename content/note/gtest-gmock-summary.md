Title: googletest和googlemock使用总结
Date: 2014-02-26 11:08
Tags: google, c++, 总结, 单元测试, 未完成

googletest和googlemock使用总结，尚待补充。

googletest和googlemock是c++里很好用的单元测试框架。另外，若无特别说明，以下内容均基于googletest 1.7和googlemock 1.7。

## googletest
### 简单的例子
<script src="https://gist.github.com/mawenbao/9223908.js"></script>

### 注意事项
#### 比较字符串
比较C String用`ASSERT_STREQ`或`EXPECT_STREQ`，比较std::string用`ASSERT_EQ`和`EXPECT_EQ`，见[详细说明](https://code.google.com/p/googletest/wiki/V1_7_Primer#String_Comparison)。

## googlemock

## 阅读资料
1. [googletest 1.7 documentation](https://code.google.com/p/googletest/wiki/V1_7_Documentation)
2. [googlemock 1.7 documentation](https://code.google.com/p/googlemock/wiki/V1_7_Documentation)

