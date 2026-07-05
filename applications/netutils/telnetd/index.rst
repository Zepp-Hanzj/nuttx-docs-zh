================================
``telnetd`` Telnet 服务器守护进程
================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是从 uIP 改编的 Telnet 逻辑，已通用化以用作任何 shell 的前端。telnet 守护进程创建的会话被"包装"为字符设备，并映射到 ``stdin``、``stdout`` 和 ``stderr``。现在 telnet 会话可以被生成的任务继承。

Telnetd 使用提示
----------------------

Telnetd 被设置为 shell 的前端。NuttX 中 Telnetd 的主要用途是支持 NuttShell（NSH）Telnet 前端。有关如何将 Telnetd 集成到自定义应用程序中的信息，请参阅 ``apps/include/netutils/telnetd.h``。

要启用和链接 Telnetd 守护进程，您需要在 defconfig 文件中包含以下内容::

  CONFIG_NETUTILS_NETLIB=y
  CONFIG_NETUTILS_TELNETD=y

另外，如果启用了 Telnet 控制台，请确保在 NuttX 配置文件中设置以下内容，否则性能会非常差（因为每次 TCP 传输只有一个字符）：

- ``CONFIG_STDIO_BUFFER_SIZE`` – 某个 ``>= 64`` 的值。
- ``CONFIG_STDIO_LINEBUFFER=y`` – 由于 Telnetd 是面向行的，行缓冲是最佳选择。
