.. include:: /substitutions.rst
.. _running:

=======
运行
=======

要在您的开发板上最终运行 NuttX，您首先需要将 NuttX 二进制文件烧录到板上。
作为一个简单的开始，建议您选择一个支持良好的开发板，该开发板还集成了
调试器/编程器，通过 USB 连接器暴露。

一个好的选择是 ST Microelectronics 的 Nucleo 或 Discovery 开发板，
因为 NuttX 中有大量支持 STM32 架构的开发板。此外，这些开发板通过
USB 连接暴露了一个 UART 端口，允许您通过交互式控制台与 NuttX 交互，
无需额外硬件。在本指南中，我们将使用 Nucleo F103RB 开发板。

烧录
========

有多种工具可以将 NuttX 二进制文件烧录到您的 Nucleo 开发板上。
一个常见的选择是使用 ``openocd``，它支持大量的编程器和目标微控制器。

您应该注意，``openocd`` 项目已经很久没有发布稳定版本了，
对较新硬件的支持可能只在最新的 Git 版本中可用，
因此实际上建议安装最新的开发版本。

.. tabs::

  .. code-tab:: console 安装稳定版本（Ubuntu）

     $ apt install openocd

  .. tab:: 从源代码安装最新版本

     .. code-block:: console

        $ git clone git://git.code.sf.net/p/openocd/code openocd
        $ cd openocd
        $ ./bootstrap
        $ ./configure --prefix=install/
        $ make install

     安装结果将在 ``openocd/install`` 下。您可以将
     ``openocd/install/bin`` 添加到您的 ``PATH`` 中。

现在，要将二进制文件烧录到您的开发板，连接 USB 数据线并执行：

.. code-block:: console

  $ cd nuttx/
  $ openocd -f interface/stlink-v2.cfg -f target/stm32f1x.cfg -c 'init' \
    -c 'program nuttx/nuttx.bin verify reset' -c 'shutdown'

访问 NuttShell
================

烧录完成后，开发板将复位并通过串行控制台提供命令提示符。
使用 Nucleo 开发板，您只需打开您选择的终端程序，
即可看到 ``nsh>`` 提示符（如果没有看到任何内容，请按 :kbd:`enter`）：

.. tabs::

  .. code-tab:: console picocom（命令行）

    $ picocom -b 115200 /dev/ttyUSB0

  .. code-tab:: console gtkterm（图形界面）

    $ gtkterm -s 115200 -p /dev/ttyUSB0

.. tip::

  在 Linux 上，您可能需要将自己添加到 ``dialout`` 组才能有权限访问串口：

  .. code-block:: console

    $ gpasswd -a <user> dialout

  其中 ``<user>`` 是您的用户名。您需要注销桌面会话才能使更改生效。
