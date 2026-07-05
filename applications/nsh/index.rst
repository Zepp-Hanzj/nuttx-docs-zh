===============
NuttShell (NSH)
===============

NuttShell 是一个功能非常完善的 shell 系统，用于 NuttX，类似于
bash 及其他类似选项。它支持丰富的内置命令、脚本编写功能，以及
将您自己的应用程序作为"内置"应用（与 NuttX 二进制文件集成在一起）
运行的能力。NSH 作为应用程序实现，其大部分功能来自名为 ``nshlib`` 的库。

因此，NSH 是完全可选的，可以禁用它，让 NuttX 直接启动指定的任务
而不是主 ``nsh`` 应用程序。

.. toctree::
  :maxdepth: 2
  :caption: 目录

  nsh.rst
  commands.rst
  config.rst
  customizing.rst
  builtin.rst
  installation.rst
  login.rst
  running_apps.rst
