==================
``kconfig2html.c``
==================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是一个 C 文件，可用于构建将 NuttX Kconfig 文件中的配置
转换为 HTML 文档的实用工具。此自动生成的文档最终将取代
严重滞后的手动更新配置文档：

.. code:: console

   $ tools/kconfig2html.exe -h
   USAGE: tools/kconfig2html [-d] [-a <apps directory>] {-o <out file>] [<Kconfig root>]
          tools/kconfig2html [-h]

Where::

    -a : 选择 apps/ 目录的相对路径。此路径相对于
         <Kconfig 目录>。默认: ../apps
    -o : 将输出发送到 <out file>。默认: 输出到 stdout
    -d : 启用调试输出
    -h : 打印此消息并退出
    <Kconfig root> 是包含根 Kconfig 文件的目录。
         默认 <Kconfig 目录>: .


.. note::

   要使用此工具，必须就地配置好所有必要的符号链接。
   你可以通过以下命令建立已配置的符号链接::

       make context

   或更快地::

       make .dirlinks
