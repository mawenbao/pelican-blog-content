Title: emacs golang environment
Date: 2013-08-25 12:14
Tags: emacs, config, golang

# Emacs Golang 配置(windows)

Windows系统下为Emacs配置golang开发环境。

## 工具

*  emacs 24.2
*  go 1.0.3 
*  auto-complete emacs自动补全库 http://cx4a.org/software/auto-complete/
*  gocode golang自动补全服务程序

## 配置过程

1. 安装emacs和go，假设emacs安装在%EMACS_HOME%目录，go安装在%GO_HOME%目录。
2. 为emacs和go配置好环境变量。
3. 安装gocode，运行之。

    gocode set propose-builtins true
    gocode set lib-path %GO_HOME%\pkg\windows_386
    gocode -s
最后将emacs/go-autocomplete.el拷贝到emacs的加载目录中。

4. 安装auto-complete，配置

	
	(when **auto-complete
	  (require 'auto-complete-config)
	  (add-to-list 'ac-dictionary-directories "~/.emacs.d/site-lisp/auto
	-complete/ac-dict")
	  (ac-config-default)
	  )

5. 为emacs配置go

	
	(when **go-lang
	  (require 'go-mode-load)
	  (require 'go-autocomplete)
	  (require 'auto-complete-config)
	  )


