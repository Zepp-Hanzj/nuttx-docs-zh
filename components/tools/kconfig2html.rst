==================
``kconfig2html.c``
==================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是 a C 文件 that 可用于 to 构建 a utility for converting the
NuttX 配置 in the Kconfig 文件s to an HTML document.  This
auto-generated documentation will, eventually, replace the manually
updated 配置 documentation that is falling woefully behind:

.. code:: console

   $ tools/kconfig2html.exe -h
   USAGE: tools/kconfig2html [-d] [-a <apps directory>] {-o <out file>] [<Kconfig root>]
          tools/kconfig2html [-h]

Where::

    -a : Select relative 路径 to the apps/ 目录. This 路径 is relative
         to the <Kconfig 目录>.  默认: ../apps
    -o : 发送 输出 to <out 文件>.  默认: 输出 goes to stdout
    -d : 启用 debug 输出
    -h : Prints this message and exits
    <Kconfig root> is the 目录 containing the root Kconfig 文件.
         默认 <Kconfig 目录>: .


.. note::

   In order to use this tool, some 配置 must be in-place with
   all necessary symbolic 链接s.  You can establish the configured symbolic
   链接s with::

       make con文本

   or more quickly with::

       make .dir链接s
