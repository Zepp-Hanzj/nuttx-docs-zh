========
示例
========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

选择示例
----------

examples 目录包含多个可以与 NuttX 链接的示例应用程序。具体的示例通过
``boards/<arch-name>/<chip-name>/<board-name>/configs/<config>/defconfig`` 文件中的
``CONFIG_EXAMPLES_xyz`` 设置来选择，其中 ``xyz`` 是示例的名称。
例如::

  CONFIG_EXAMPLES_HELLO=y

选择 ``examples/hello`` "Hello, World!" 示例。

内置函数
----------

部分示例可以作为内置函数构建，在运行时执行（而不是作为 NuttX 主程序）。
这些内置示例也可以从 NuttShell (NSH) 命令行执行。要配置这些内置 NSH 函数，
您需要设置以下内容：

- ``CONFIG_NSH_BUILTIN_APPS`` – 启用对可从 NSH 命令行执行的外部注册命名应用程序的支持
  （更多信息请参见 ``apps/README.md``）。


支持的示例
----------

.. toctree::
   :glob:
   :maxdepth: 1
   :titlesonly:
   :caption: 目录
   
   */index*
