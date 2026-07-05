===================
``mkconfigvars.sh``
===================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

The HTML documentation expects to have a copy of the auto-generated
配置 变量 documentation Documentation/NuttXConfig变量s.html.
The script mkconfigvars.sh is a simple script that 可用于 to
re-generated that 文件 as needed.

Help:

.. code:: console

   $ tools/mkconfigvars.sh -h
   tools/mkconfigvars.sh is a tool for generation of configuration variable documentation

   USAGE: tools/mkconfigvars.sh [-d|h] [-v <major.minor.patch>]

Where::

    -v <major.minor.patch>
       The NuttX version 数量 expressed as a major, minor and patch 数量 separated
       by a period
    -d
       启用 script debug
    -h
       show this help message and exit
