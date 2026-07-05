=========
SocketCAN
=========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

SocketCAN 设备驱动
========================

- ``include/nuttx/net/netdev.h``。所有与驱动相关的
  结构体和 API 都在此头文件中提供。
  结构体 struct net_driver_s 定义了该接口，并通过
  ``netdev_register()`` 注册到网络。

- ``include/nuttx/can.h``。CAN 和 CAN FD 帧数据结构
  以及 dlc 到 len 大小的转换

  .. code-block:: c

     uint8_t can_bytes2dlc(uint8_t nbytes);
     uint8_t can_dlc2bytes(uint8_t dlc);

- ``int netdev_register(FAR struct net_driver_s *dev, enum net_lltype_e lltype)'``。
  每个驱动通过调用 ``netdev_register()`` 注册自身。

- ``Include/nuttx/net/can.h``。包含 CAN dlc 到 CAN FD len 大小的
  查找表

- **初始化顺序如下**。

  #. NuttX 启动时调用 ``xxx_netinitialize(void)``，
     在此函数中调用您自己的初始化函数来初始化您的 CAN 驱动
  #. 在您自己的初始化函数中创建 net_driver_s 结构，
     设置所需的初始值，并为 SocketCAN 注册所需的回调
  #. 然后确保 CAN 接口处于关闭模式（通常通过调用 d_ifdown 函数完成）
  #. 使用 netdev_register 注册 net_driver_s

- **接收顺序如下**。

  #. 设备产生中断
  #. 在您的中断处理程序中处理此中断
  #. 当接收到新的 CAN 帧时处理此帧
  #. 当 CAN 帧是普通 CAN 帧时分配 can_frame 结构，
     当它是 CAN FD 帧时分配 canfd_frame 结构
     （注意您当然可以预分配并只使用指针）。
  #. 将帧从驱动复制到您在上一步中分配的结构中。
  #. 将 net_driver_s d_buf 指针指向分配的 can_frame
  #. 调用 ``can_input(FAR struct net_driver_s *dev)``
     函数 ``include/nuttx/net/can.h``

- **发送顺序如下**。

  #. 套接字层执行 d_txavail 回调
  #. txavail 函数的示例可以在
     ``arch/arm/src/s32k1xx/s32k1xx_flexcan.c`` 中找到
  #. txpoll 函数的示例可以在
     ``arch/arm/src/s32k1xx/s32k1xx_flexcan.c`` 中找到
  #. 在您的 ``transmit(struct driver_s *priv)`` 函数中，
     检查 ``net_driver_s.d_len`` 的长度是否与
     ``struct can_frame`` 或 ``struct canfd_frame`` 的大小匹配，
     然后将 ``net_driver_s.d_buf`` 指针的内容转换为正确的 CAN 帧结构

SocketCAN 协议栈
========================

SocketCAN 是基于 BSD 套接字 API 的 CAN 协议栈实现，
提供更标准化和灵活的 CAN 通信接口。
SocketCAN 使用网络协议栈框架，允许应用程序
使用标准套接字系统调用（如 ``socket()``、``bind()``、
``send()``、``recv()`` 等）进行 CAN 通信。

架构
------------

SocketCAN 实现遵循标准网络层层次结构：

#. **应用层接口**：使用标准套接字 API（AF_CAN 地址族）
#. **协议层**：CAN 协议处理（位于 ``net/can/``）
#. **设备层**：CAN 网络设备驱动

文件位置
--------------

支持 SocketCAN 的文件可在以下位置找到：

-  **协议实现**：SocketCAN 协议栈位于 ``net/can/`` 目录
-  **头文件**：``include/nuttx/net/can.h``
-  **主要模块**：

   - ``can_conn.c`` - 连接管理
   - ``can_sockif.c`` - 套接字接口实现
   - ``can_sendmsg.c`` - 消息发送
   - ``can_sendmsg_buffered.c`` - 带缓冲的消息发送
   - ``can_recvmsg.c`` - 消息接收
   - ``can_poll.c`` - 轮询支持
   - ``can_callback.c`` - 回调处理

配置选项
---------------------

要启用 SocketCAN，配置以下选项：

-  ``CONFIG_NET_CAN`` - 启用 SocketCAN 支持
-  ``CONFIG_NET_CAN_NOTIFIER`` - 启用 CAN 通知器（可选）
-  ``CONFIG_NET_CAN_NBUFFERS`` - CAN 缓冲区数量
-  ``CONFIG_NET_RECV_BUFSIZE`` - 接收缓冲区大小

使用说明
-----------

SocketCAN 使用标准套接字编程模型：

.. code-block:: c

   /* 创建 CAN 套接字 */
   int sock = socket(AF_CAN, SOCK_RAW, CAN_RAW);

   /* 绑定到 CAN 接口 */
   struct sockaddr_can addr;
   addr.can_family = AF_CAN;
   addr.can_ifindex = if_nametoindex("can0");
   bind(sock, (struct sockaddr *)&addr, sizeof(addr));

   /* 发送 CAN 帧 */
   struct can_frame frame;
   frame.can_id = 0x123;
   frame.can_dlc = 8;
   /* 填充数据 */
   send(sock, &frame, sizeof(frame), 0);

   /* 接收 CAN 帧 */
   recv(sock, &frame, sizeof(frame), 0);

功能特性
--------

-  **标准套接字 API**：使用熟悉的套接字编程接口
-  **过滤支持**：通过套接字选项设置 CAN ID 过滤器
-  **非阻塞 I/O**：支持非阻塞模式和轮询
-  **多连接**：支持多个套接字同时访问同一 CAN 总线
-  **读缓冲**：支持数据读缓冲以防止数据丢失
-  **CAN FD 支持**：如果配置中启用了 CAN FD，则支持 CAN FD 帧
-  **可扩展**：易于扩展以支持其他 CAN 协议
