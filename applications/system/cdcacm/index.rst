======================================
``cdcacm`` CDC/ACM USB 串口设备
======================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``cdcacm`` 附加组件提供了一个 CDC/ACM（通信设备类/抽象控制模型）USB 串口设备驱动程序。
该驱动程序允许 NuttX 设备通过 USB 接口模拟串口通信。

配置选项
--------

- ``CONFIG_CDCACM`` – 启用 CDC/ACM USB 串口设备支持。
- ``CONFIG_CDCACM_COMPOSITE`` – 将 CDC/ACM 作为复合设备的一部分启用。
- ``CONFIG_CDCACM_CONSOLE`` – 启用 CDC/ACM 控制台。
- ``CONFIG_CDCACM_BULKIN_REQHEADERS`` – 设置批量输入请求头缓冲区数量。
- ``CONFIG_CDCACM_BULKOUT_REQHEADERS`` – 设置批量输出请求头缓冲区数量。
