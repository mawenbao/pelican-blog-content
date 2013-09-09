Title: Debian6上安装haskell pandoc
Date: 2013-08-25 12:14
Tags: debian, install, haskell, pandoc


debian6 squeeze上在安装haskell和pandoc
## 安装haskell platform和cabal

首先安装依赖的软件包

	apt-get install libgmp3-dev freeglut3 freeglut3-dev

然后下载ghc 7.4.2, 在[这里](http://www.haskell.org/ghc/download_ghc_7_4_2)选择合适的版本。解压后执行:

	cd ghc-7.4.2
	./configure
	make install

在[这里](http://www.haskell.org/platform/linux.html)下载haskell，然后编译安装。

	./configure
	make 
	make install

最后，更新cabal软件列表和cabal-install。

	cabal update
	cabal install cabal-install

## Cabal常用命令

*  `cabal list`
*  `cabal install`
## 安装pandoc

	cabal install pandoc
	ln -s ~/.cabal/bin/pandoc /usr/bin/pandoc

## 参考资料

*  [Haskell Platform for Ubuntu 11.10](https///gist.github.com/1524859)
*  [“cannot determine current directory” while building haskell](http://askubuntu.com/questions/95081/cannot-determine-current-directory-while-building-haskell)

