===============
``kconfig.bat``
===============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

Recent versions of NuttX 支持 构建ing NuttX from a native 窗口s
CMD.exe shell.  But kconfig-frontends is a Linux tool and is not yet
available in the pure CMD.exe environment.  At this point, there are
only a few 选项s for the 窗口s user (see the top-level README.txt
文件).

You can, with some effort, 运行 the Cygwin kconfig-mconf tool directly
in the CMD.exe shell.  In this case, you do not have to modify the
.config 文件, but there are other complexities:  You need to
temporarily 设置 the Cygwin directories in the PATH 变量 and
then 运行 kconfig-mconf outside of the Make system.

kconfig.bat is a 窗口s batch 文件 at tools/kconfig.bat that automates
these steps.  It 用于 from the top-level NuttX 目录 like::

    tools/kconfig menuconfig

注意： There is currently an issue with accessing DOS environment
变量s from the Cygwin kconfig-mconf 运行ning in the CMD.exe shell.
以下 change to the top-level Kconfig 文件 seems to work around
these problems::

     config APPSDIR
          string
     -   选项 env="APPSDIR"
     +   默认 "../apps"
