===========
CAN 驱动
===========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 支持字符设备 CAN 作为非常底层的 CAN 驱动程序，以及 SocketCAN 作为更高级别（开销更大）的选项。
此驱动程序仅支持数据交换，不包含任何高级 CAN 协议。NuttX CAN 驱动程序分为两部分：

#. "上半部分"，通用驱动程序，为应用程序级代码提供通用 CAN 接口，以及
#. "下半部分"，特定于平台的驱动程序，实现底层定时器控制以实现 CAN 功能。

支持 CAN 的文件可以在以下位置找到：

-  **接口定义**。NuttX CAN 驱动程序的头文件位于 ``include/nuttx/can/can.h``。此头文件包括 CAN 驱动程序的应用程序级接口以及"上半部分"和"下半部分"驱动程序之间的接口。CAN 模块使用标准字符驱动程序框架。
-  **"上半部分"驱动程序**。通用"上半部分"CAN 驱动程序位于 ``drivers/can.c``。
-  **"下半部分"驱动程序**。特定于平台的 CAN 驱动程序位于 ``arch/<architecture>/src/<hardware>`` 目录，针对特定处理器 ``<architecture>`` 和特定 ``<chip>`` CAN 外设设备。

``struct timeval ch_ts``：存储在 ``can_hdr_s`` 结构中的此成员变量取决于 ``CONFIG_CAN_TIMESTAMP``，用于存储 CAN 消息的时间戳。

上半部分驱动程序支持以下 ``ioctl`` 命令：

- **CANIOC_RTR**：将给定消息（作为 ``ioctl`` 参数传递）作为远程请求发送。成功返回时，传递的消息结构将用接收到的消息内容更新；即消息 ID 和标准/扩展 ID 指示位保持不变，但 DLC 和数据位将用接收到的消息内容更新。如果在指定超时后未收到响应，ioctl 将返回。
- **CANIOC_GET_BITTIMING**：返回当前位定时设置。
- **CANIOC_SET_BITTIMING**：设置新的位定时值。
- **CANIOC_ADD_STDFILTER**：为标准 11 位地址添加地址过滤器。
- **CANIOC_ADD_EXTFILTER**：为扩展 29 位地址添加地址过滤器。
- **CANIOC_DEL_STDFILTER**：移除标准 11 位地址的地址过滤器。
- **CANIOC_DEL_EXTFILTER**：移除标准 29 位地址的地址过滤器。
- **CANIOC_GET_CONNMODES**：获取当前总线连接模式。
- **CANIOC_SET_CONNMODES**：设置新的总线连接模式值。
- **CANIOC_BUSOFF_RECOVERY**：启动 BUS-OFF 恢复序列。
- **CANIOC_SET_NART**：启用/禁用 NART（无自动重试）。
- **CANIOC_SET_ABOM**：启用/禁用 ABOM（自动总线关闭管理）。
- **CANIOC_IFLUSH**：刷新已接收但未读取的数据。
- **CANIOC_OFLUSH**：刷新已写入但未发送的数据。
- **CANIOC_IOFLUSH**：刷新已接收但未读取的数据和已写入但未发送的数据。
- **CANIOC_SET_STATE**：设置特定的 CAN 控制器状态。
- **CANIOC_GET_STATE**：获取特定的 CAN 控制器状态。
- **CANIOC_SET_TRANSVSTATE**：设置特定的 CAN 收发器状态。
- **CANIOC_GET_TRANSVSTATE**：获取特定的 CAN 收发器状态。
- **CANIOC_SET_MSGALIGN**：设置消息对齐方式。读取和写入的消息可以配置为按给定字节的倍数对齐。默认值为 1。对齐影响读取和写入操作。值 0 有特殊含义，写入行为与值 1 相同，但读取将始终只提供单个消息。
- **CANIOC_GET_MSGALIGN**：获取消息对齐方式。解释参见 CANIOC_SET_MSGALIGN。

上半部分驱动程序支持**严格的 TX 优先级排序**：

-  当 CAN 控制器硬件支持从硬件发送缓冲区取消正在进行的传输时，可以使用以下传输取消机制来避免当所有硬件发送缓冲区都满时的优先级反转。

-  **行为**：当硬件发送缓冲区已满且软件 tx_pending 列表中有排队的帧时，驱动程序将软件 tx_pending 列表中的最高优先级帧与当前驻留在硬件中的最高优先级帧进行比较。如果挂起的最高优先级帧的优先级高于硬件驻留的最高优先级帧，驱动程序将：

   - 取消当前在硬件发送缓冲区中的最低优先级帧的传输（控制器必须支持取消）。
   - 将已取消的帧重新插入软件 tx_pending 列表中的适当位置。
   - 用从软件 tx_pending 列表中取出的较高优先级帧填充空出的硬件发送缓冲区。

   此机制有助于在所有硬件发送缓冲区都满时防止优先级反转，确保最高优先级的帧始终首先传输。

-  **注意**：此上下文中的"硬件发送缓冲区"指的是各个硬件发送消息缓冲区，而不是硬件 FIFO。

-  **要求**：
   - CAN 控制器必须支持取消正在进行的缓冲传输。

   - 驱动程序实现（上半部分/下半部分）必须与取消操作配合，并正确管理 tx_pending 和 tx_sending 列表。

   - 该功能应通过配置选项（``CONFIG_CAN_STRICT_TX_PRIORITY``）启用。

**使用说明**：上半部分驱动程序的默认行为是在 ``read`` 时返回多个消息。参见 `此主题指南 </guides/reading_can_msgs.html>`_。

**示例**：``drivers/can/mcp2515.c``。
