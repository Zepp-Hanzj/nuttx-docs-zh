.. warning::
  wolfSSL 使用 GPL 许可证

================================================
``wolfSSL`` wolfSSL SSL/TLS 加密库
================================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

安装
------------

从 nuttx-apps 安装
~~~~~~~~~~~~~~~~~~~~~~~~~~

跳转到第 6 步

从 wolfssl 安装
~~~~~~~~~~~~~~~~~~~~~~~

1) 创建工作目录（例如 ~/nuttxspace）::

    $ cd ~
    $ mkdir nuttxspace

2) 安装依赖::

    $ cd ~/nuttxspace
    $ sudo apt install -y bison flex gettext texinfo libncurses5-dev libncursesw5-dev gperf automake libtool pkg-config build-essential gperf genromfs libgmp-dev libmpc-dev libmpfr-dev libisl-dev binutils-dev libelf-dev libexpat-dev gcc-multilib g++-multilib picocom u-boot-tools util-linux
    $ sudo apt install -y kconfig-frontends
    $ sudo apt install -y gcc-arm-none-eabi binutils-arm-none-eabi

3) 将 nuttx 和 nuttx-apps 克隆到工作目录::

    $ git clone https://github.com/apache/nuttx.git nuttx
    $ git clone https://github.com/apache/nuttx-apps apps

4) 将此目录复制到工作目录的应用目录中::

    $ cp -R RTOS/nuttx/wolfssl ~/nuttxspace/apps/crypto/wolfssl

5) 设置 wolfSSL 以准备构建，``WOLFSSL_DIR`` 必须是原始 wolfssl 仓库的路径::

    $ cd ~/nuttxspace/apps/crypto/wolfssl
    $ WOLFSSL_DIR=<path-to-wolfssl-repo> ./setup-wolfssl.sh

6) 设置基线 NuttX 配置（板子 + NuttX Shell）::

     $ cd ~/nuttxspace/nuttx
     $ ./tools/configure.sh -l <board>:nsh

    如果您使用 wolfSSL 进行 TLS，且您的板子支持 ``netnsh`` 目标，则应使用该目标::

      $ ./tools/configure.sh -l <board>:netnsh

    示例：

    - NuttX 模拟器：``$ ./tools/configure.sh sim:nsh``
    - BL602 (RISC-V)：``$ ./tools/configure.sh -l bl602evb:nsh``
    - NUCLEO-L552ZE-Q (Cortex-M33)：``$ ./tools/configure.sh -l nucleo-l552ze:nsh``
    - NUCLEO-H753ZI：``$ ./tools/configure.sh -l nucleo-h743zi:nsh``
    - NUCLEO-F756ZG：``./tools/configure.sh -l nucleo-144:f746-nsh``

7) 启动自定义配置系统::

     $ make menuconfig

8) 配置 NuttX 以启用 wolfSSL 加密库测试应用程序：

    - 从主菜单选择：**Application Configuration > Cryptography Library Support**
    - 启用并选择 **wolfSSL SSL/TLS Cryptography Library**
    - 启用并选择 **wolfSSL applications**
    - 启用以下应用程序：

        - **wolfCrypt Benchmark application**
        - **wolfCrypt Test application**
        - **wolfSSL client and server example**

    - 从底部菜单选择 Save，保存到 ``.config`` 文件
    - 退出配置工具

    如果您使用 wolfSSL 进行 TLS，应使用 ``netnsh`` 目标，并应启用 NTP 或某种系统时间保持机制，以便 wolfSSL 拥有当前日期来检查证书。您还需要设置正确的网络配置，以便 NuttX 连接到互联网。

9) 构建 NuttX 和 wolfSSL::

     $ make

10) 烧录目标::

      ### 模拟器
      ./nuttx
      ### STM32 目标（地址可能不同）
      STM32_Programmer_CLI -c port=swd -d ./nuttx.bin 0x08000000

11) 使用串口监控工具连接到目标设备，Linux 上的设备通常是 ``/dev/ttyACM0``，但可能会有所不同::

      minicom -D /dev/ttyACM0

12) 在 NuttX Shell 中运行 wolfcrypt 基准测试和/或测试::

      nsh> wolfcrypt_test
      nsh> wolfcrypt_benchmark
      nsh> wolfssl_client_server

注意事项
-----

使用以下目标进行开发：

- STM NUCLEO-L552ZE-Q (Cortex-M33)
- STM NUCLEO-H753ZI
- STM NUCLEO-F756ZG
- DT-BL10 / BL602 (RISC-V)
- NuttX 模拟器
