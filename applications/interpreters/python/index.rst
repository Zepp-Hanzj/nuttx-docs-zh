=============================
``Python`` Python 解释器
=============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

本指南介绍如何在 NuttX 上运行 Python。

*是的，您没听错*。**NuttX 上的 Python**。这是 `CPython <https://github.com/python/cpython>`_ 仓库到 NuttX 的移植。
`CPython` 仓库是 Python 编程语言的参考实现。
它使用 C 编写，是最广泛使用的 Python 解释器。

.. warning::
   Python for NuttX 仍处于实验阶段（因此需要启用 ``CONFIG_EXPERIMENTAL``）
   它并非在所有架构和配置上都完全可用。
   请查看 `nuttx-apps <https://github.com/apache/nuttx-apps/>`_ 仓库中的此
   `issue <https://github.com/apache/nuttx-apps/issues/2884>`_ 以了解当前状态。

工作原理
=================

1. Python for NuttX 在 RISC-V QEMU（模拟）和 Espressif 的 ESP32-S3 上运行。
2. Python 模块以 `pyc <https://docs.python.org/3/glossary.html#term-bytecode>`_（字节码格式）存储，并在启动时从 ROMFS 映像加载。
3. NuttX 上的 Python 包装应用程序自动挂载包含 Python 模块的 ROMFS 分区，并设置所需的环境变量（``PYTHONHOME`` 和 ``PYTHON_BASIC_REPL``）。

在 NuttX 上构建和运行 Python
====================================

``rv-virt`` (RISC-V QEMU)
----------------------------

使用 ``rv-virt:python`` 配置来构建 NuttX 的 Python。请注意，CMake 脚本不适用于此配置。目前请使用 makefile 构建：

.. code:: console

   $ cd nuttx
   $ make distclean
   $ ./tools/configure.sh rv-virt:python
   $ make -j$(nproc)
   $ ls -l nuttx

这将生成一个 ``nuttx`` 二进制文件。此文件可以使用 RISC-V QEMU 运行。

在运行 RISC-V QEMU 之前，使用以下命令创建原始磁盘映像：

.. code:: console

   $ dd if=/dev/zero of=./mydisk-1gb.img bs=1M count=1024

然后，使用以下命令运行 RISC-V QEMU：

.. code:: console

   $ qemu-system-riscv32 -semihosting -M virt,aclint=on -cpu rv32 -smp 8 \
      -global virtio-mmio.force-legacy=false \
      -device virtio-serial-device,bus=virtio-mmio-bus.0 \
      -chardev socket,telnet=on,host=127.0.0.1,port=3450,server=on,wait=off,id=foo \
      -device virtconsole,chardev=foo \
      -device virtio-rng-device,bus=virtio-mmio-bus.1 \
      -netdev user,id=u1,hostfwd=tcp:127.0.0.1:10023-10.0.2.15:23,hostfwd=tcp:127.0.0.1:15001-10.0.2.15:5001 \
      -device virtio-net-device,netdev=u1,bus=virtio-mmio-bus.2 \
      -drive file=./mydisk-1gb.img,if=none,format=raw,id=hd \
      -device virtio-blk-device,bus=virtio-mmio-bus.3,drive=hd \
      -bios none -kernel ./nuttx -nographic

   ABC[    0.062131] board_userled: LED 1 set to 0
   [    0.063269] board_userled: LED 2 set to 0
   [    0.063367] board_userled: LED 3 set to 0
   telnetd [4:100]

   NuttShell (NSH) NuttX-10.4.0
   nsh> python
   Python 3.13.0 (main, Dec  4 2024, 17:00:42) [GCC 13.2.0] on nuttx
   Type "help", "copyright", "credits" or "license" for more information.
   >>>

演示
^^^^

查看以下 `asciinema <https://asciinema.org/>`_ 演示以了解如何在 NuttX 上运行 Python。您可以从演示中复制和粘贴命令来亲自尝试。

.. image:: https://asciinema.org/a/bYYy1fyIOQ3hOY4lJ7L3WFcNb.svg
   :target: https://asciinema.org/a/bYYy1fyIOQ3hOY4lJ7L3WFcNb

ESP32-S3
--------

在此示例中，我们将使用 ESP32-S3 开发板。使用 ``esp32s3-devkit:python`` 配置来构建 NuttX 的 Python。
请注意，此 defconfig 使用带有 ESP32-S3-WROOM-2 模块的板子，具有 32MiB 闪存和 8MiB PSRAM。

使用以下命令构建并烧录 ESP32-S3 板：

.. code:: console

   $ cd nuttx
   $ make distclean
   $ ./tools/configure.sh esp32s3-devkit:python
   $ make flash ESPTOOL_BINDIR=./ ESPTOOL_PORT=/dev/ttyUSB0 -s -j$(nproc)

要在 ESP32-S3 上运行 Python，只需打开串口终端并连接到 ESP32-S3 板。
您将看到 NuttShell (NSH) 提示符。运行以下命令：

.. code:: console

   nsh> python
   Python 3.13.0 (main, Dec  4 2024, 17:00:42) [GCC 13.2.0] on nuttx
   Type "help", "copyright", "credits" or "license" for more information.
   >>>
