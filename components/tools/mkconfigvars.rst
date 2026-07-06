===================
``mkconfigvars.sh``
===================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

HTML 文档期望有一份自动生成的配置变量文档
Documentation/NuttXConfigVariables.html 的副本。
脚本 mkconfigvars.sh 是一个简单的脚本，可用于根据需要
重新生成该文件。

Help:

.. code:: console

   $ tools/mkconfigvars.sh -h
   tools/mkconfigvars.sh is a tool for generation of configuration variable documentation

   USAGE: tools/mkconfigvars.sh [-d|h] [-v <major.minor.patch>]

Where::

    -v <major.minor.patch>
       NuttX 版本号，表示为以句点分隔的主版本号、次版本号和补丁号
    -d
       启用脚本调试
    -h
       显示此帮助消息并退出
