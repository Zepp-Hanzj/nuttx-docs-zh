=======================
``can`` CAN 设备测试
=======================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

如果 CAN 设备配置为环回模式，则此示例可用于测试 CAN 设备的环回功能。它只是发送一系列 CAN 消息，并验证这些消息是否与发送时完全一致返回。

此测试依赖于以下特定的 CAN/NSH 配置设置（您特定的 CAN 设置可能需要额外的配置）。

- ``CONFIG_CAN`` – 启用 CAN 支持。
- ``CONFIG_CAN_LOOPBACK`` – CAN 驱动程序可能支持也可能不支持用于测试的环回模式。STM32 CAN 驱动程序支持环回模式。
- ``CONFIG_NSH_BUILTIN_APPS`` – 将 CAN 测试构建为 NSH 内置函数。默认：构建为独立程序。

此示例的特定配置选项包括：

- ``CONFIG_EXAMPLES_CAN_DEVPATH`` – CAN 设备的路径。默认：``/dev/can0``。
- ``CONFIG_EXAMPLES_CAN_NMSGS`` – 采集此数量的 CAN 消息后程序终止。默认：无限期发送和接收消息。

默认行为假设为环回模式。消息被发送，然后读取并验证。对于其他类型的测试（仅发送或接收但不验证 CAN 消息），可以更改此行为。

- ``CONFIG_EXAMPLES_CAN_READONLY`` – 仅接收消息。
- ``CONFIG_EXAMPLES_CAN_WRITEONLY`` – 仅发送消息。
