=================
``ymodem`` YMODEM
=================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是 `ymodem 协议 <http://pauillac.inria.fr/~doligez/zmodem/ymodem.txt>`_。
根据该协议实现了 sb rb 应用程序，分别用于发送文件和接收文件。

用法
-----

常见用法
~~~~~~~~~~~~

在 Ubuntu 系统中，需要安装 lszrz，可以使用 ``sudo apt install lszrz``。
使用 minicom 与开发板通信。

高级用法
~~~~~~~~~~~~~~

为了实现更快的传输速度，在 YMODEM 协议中添加了特定的 HEADER ``STC``
来表示自定义长度。在开发板上使用 ``sb`` 和 ``rb`` 命令时，可以使用 ``-k``
选项设置自定义数据包的长度，单位为 KB。因此，需要使用 ``sbrb.py`` 进行文件传输，
并且需要 ``sbrb.py`` -k 设置与开发板相同的长度。根据测试，使用 -k 32 时，
可以达到波特率的 93%，并且完全兼容原始 ymodem 协议。

首先，需要为 sbrb.py 添加软链接，例如
``sudo ln -s /home/<name>/.../<nuttxwork>/apps/system/ymodem/sbrb.py /usr/bin``
然后可以将 sbrb.py 配置到 minicom 中。``<Ctrl + a> z o`` 然后选择
``File transfer protocols`` 并创建两个选项，命令为 'sbrb.py -k 32'。如下所示

=========== ============= ==== === ======= ======= =====
名称        程序          名称 U/D 全屏    IO重定向 多文件
=========== ============= ==== === ======= ======= =====
ymodem-k    sbrb.py -k 32 Y    U   N       Y       Y 
ymodem-k    sbrb.py -k 32 N    D   N       Y       Y 
=========== ============= ==== === ======= ======= =====

在开发板上使用 ``sb -k 32`` 或 ``rb -k 32`` 进行文件传输。

发送文件到 PC
--------------

使用 sb 命令，如 ``nsh> sb /tmp/test.c ...``，此命令支持同时发送多个文件。
然后使用 ``<Ctrl + a> , r`` 选择 ``ymodem`` 接收开发板文件。

发送文件到开发板
-----------------

使用 rb 命令，如 ``nsh> rb``，此命令支持同时接收多个文件。
然后使用 ``<Ctrl + a> , s`` 选择 ``ymodem``，然后选择要发送的文件。

帮助
~~~~

可以使用 ``sb -h`` 或 ``rb -h`` 获取帮助。

调试
-----

由于使用串口进行通信，日志会打印到调试文件。
可以使用 ``CONFIG_SYSTEM_YMODEM_DEBUGFILE_PATH`` 设置调试文件路径。
