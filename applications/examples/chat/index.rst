====================
``chat`` AT over TTY
====================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

演示通过 TTY 设备的 AT 聊天功能。这对于 AT 调制解调器很有用，例如建立 ``pppd`` 连接（参见相关的 ``pppd`` 示例）。此外，一些 AT 调制解调器（例如 u-blox 制造的）具有内部 TCP/IP 协议栈，通常带有 TLS/SSL 实现。在这种情况下，聊天工具可用于配置内部 TCP/IP 协议栈、建立套接字连接、设置安全性（例如，将 base64 编码的证书下载到调制解调器），并通过 TTY 设备上的套接字执行数据交换。

有用的配置参数：

- ``CONFIG_EXAMPLES_CHAT_PRESET[0..3]`` – 预设聊天脚本。
- ``CONFIG_EXAMPLES_CHAT_TTY_DEVNODE`` – TTY 设备节点名称。
- ``CONFIG_EXAMPLES_CHAT_TIMEOUT_SECONDS`` – 默认接收超时。
