Title: c++宽字符处理
Date: 2009-08-14 17:21:21
Tags: c++, wchar

前一段时间写 GPA 计算器时需要处理宽字符串。初次接触宽字符遇到不少问题，最后通过查找资料都已解决，特记录于此以作备忘之用。

环境：Visual Studio 2005(ch), win32

## 与宽字符相关的输入输出

### 标准输入与输出
需包含 iostream 头文件，对于中文的输入输出建议包含 locale 头文件，并设置 locale 为“chs”。标准输入流为 wcin ，标准输出流为 wcout ，标准错误流为 wcerr 。

    :::cpp
    #include <iostream>
    #include <locale>
    // ...

    wcin.imbue(locale("chs"));
    wcout.imbue(locale("chs"));

    wcin >> // wstring
    wcout << // wstring

    // ...
    
### 文件输入与输出
相应的输入输出流换为 wifstream 和 wofstream 。

    :::cpp
    #include <fstream>
    #include <locale>
    #include <string>
    // ...

    void fun(string _flname) {
        wifstream wif(_flname.c_str());
        wif.imbue(locale("chs"));
        wstring wsline(L""); // L必需

        while (getline(wif, wsline)) // wif 与 wsline 的字符类型应相同，同为 char 或同为 wchar_t 。
        // ...

        wif.close();
    }
    // ...
    
### wstringstream 流
建议进行类型转换时，使用 wstringstream 流。

    :::cpp
    #include <stringstream>
    #include <locale>
    // ...

    wstringstream wssm;
    int ivar;
    double dvar;

    wssm.imbue(locale("chs"));

    wssm << L"123" << L" " << L"3.14159";
    wssm >> ivar >> dvar;

    // 由于 wssm 已到达末尾，如需继续转换，务必重置流状态为正常
    /* wssm.clear();
    * wssm << // ...
    * wssm >> // ...
    * // ...
    */

    // ...

## 其它
### wstring 类函数
使用 string 类的函数，注意字符类型为 wchar_t，相应的指针类型为 wchar_t* 。

