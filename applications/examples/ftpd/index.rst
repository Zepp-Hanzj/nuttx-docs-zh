===================
``ftpd`` FTP 守护进程
===================

本示例测试 ``apps/netutils/ftpd`` 中的 FTPD 守护进程。以下是 FTPD 示例特定的配置（FTPD 守护进程本身可能还需要其他配置选项）。

- ``CONFIG_EXAMPLES_FTPD`` – 启用 FTPD 示例。
- ``CONFIG_EXAMPLES_FTPD_PRIO`` – FTP 守护进程的优先级。默认值：``SCHED_PRIORITY_DEFAULT``。
- ``CONFIG_EXAMPLES_FTPD_STACKSIZE`` – 为 FTP 守护进程分配的栈大小。默认值：``2048``。
- ``CONFIG_EXAMPLES_FTPD_NONETINIT`` – 定义此选项以禁止 ``apps/examples/ftpd`` 配置网络。如果在运行示例之前已配置网络，则需要禁止网络配置。

NSH 总是初始化网络，因此如果定义了 ``CONFIG_NSH_NETINIT``，则 ``CONFIG_EXAMPLES_FTPD_NONETINIT`` 也会被定义（在这种情况下不需要显式定义）：

- ``CONFIG_NSH_BUILTIN_APPS`` – 将 FTPD 守护进程示例测试构建为 NSH 内置函数。默认情况下，FTPD 守护进程将作为独立应用程序构建。

如果未定义 ``CONFIG_EXAMPLES_FTPD_NONETINIT``，则可以指定以下选项来自定义网络配置：

- ``CONFIG_EXAMPLES_FTPD_NOMAC`` – 如果硬件没有自己的 MAC 地址，定义此选项为 ``=y`` 以提供一个用于测试的临时地址。
- ``CONFIG_EXAMPLES_FTPD_IPADDR`` – 目标 IP 地址。默认值：``10.0.0.2``。
- ``CONFIG_EXAMPLES_FTPD_DRIPADDR`` – 默认路由器地址。默认值：``10.0.0.1``。
- ``CONFIG_EXAMPLES_FTPD_NETMASK`` – 子网掩码。默认值：``255.255.255.0``。

需要 TCP 网络支持。同时需要 pthreads，因此必须将此项设置为 'n'：

- ``CONFIG_DISABLE_PTHREAD`` – 需要 ``pthread`` 支持。

其他可能感兴趣的 FTPD 配置选项：

- ``CONFIG_FTPD_VENDORID`` – FTP 通信中使用的供应商名称。默认值：``NuttX``。
- ``CONFIG_FTPD_SERVERID`` – FTP 通信中使用的服务器名称。默认值：``NuttX FTP Server``。
- ``CONFIG_FTPD_CMDBUFFERSIZE`` – 单条命令的最大大小。默认值：``512`` 字节。
- ``CONFIG_FTPD_DATABUFFERSIZE`` – 数据传输的 I/O 缓冲区大小。默认值：``2048`` 字节。
- ``CONFIG_FTPD_WORKERSTACKSIZE`` – 为每个 FTP 守护进程工作线程分配的栈大小。默认值：``2048`` 字节。

以下 netutils 库应在您的 ``defconfig`` 文件中启用：

  CONFIG_NETUTILS_NETLIB=y
  CONFIG_NETUTILS_FTPD=y
