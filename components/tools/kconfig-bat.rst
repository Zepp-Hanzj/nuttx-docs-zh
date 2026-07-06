===============
``kconfig.bat``
===============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

最新版本的 NuttX 支持从原生 Windows CMD.exe shell 构建 NuttX。
但 kconfig-frontends 是一个 Linux 工具，在纯 CMD.exe 环境中尚不可用。
目前，Windows 用户只有少数几个选项（参见顶层 README.txt 文件）。

你可以通过一些努力，直接在 CMD.exe shell 中运行 Cygwin kconfig-mconf 工具。
在这种情况下，你不必修改 .config 文件，但还有其他复杂性：
你需要临时在 PATH 变量中设置 Cygwin 目录，
然后在 Make 系统之外运行 kconfig-mconf。

kconfig.bat 是位于 tools/kconfig.bat 的 Windows 批处理文件，
用于自动执行这些步骤。它从顶层 NuttX 目录使用，如下::

    tools/kconfig menuconfig

注意：目前存在从 CMD.exe shell 中运行的 Cygwin kconfig-mconf 访问
DOS 环境变量的问题。对顶层 Kconfig 文件的以下更改似乎可以解决这些问题::

     config APPSDIR
          string
     -   option env="APPSDIR"
     +   default "../apps"
