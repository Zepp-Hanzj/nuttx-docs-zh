==================================================
``i8sak`` or ``i8`` IEEE 802.15.4 Swiss Army Knife
==================================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

描述
===========

i8sak 应用是一个有用的 CLI，用于测试各种 IEEE 802.15.4 功能。它也可作为学习
如何与 NuttX IEEE 802.15.4 MAC 层交互的起点。

i8sak CLI 可用于同时操作多个 MAC 层网络。支持 MAC 字符驱动接口和使用套接字的
网络接口。MAC 字符驱动用于未启用网络且您希望应用程序直接使用 IEEE 802.15.4 的
情况。但在大多数情况下，您可能会使用 6LoWPAN 网络支持，因此可以直接从套接字接口
控制 MAC，而无需使用 MAC 字符驱动。IEEE 802.15.4 MAC 字符驱动在 NuttX 中默认
显示为 ``/dev/ieeeN``。

当您首次使用指定接口名称调用 i8sak 时，它会创建一个 i8sak 实例并启动一个守护进程
来处理处理工作。该实例被认为是"粘性的"，因此可以在会话开始时运行 ``i8 /dev/ieee0``
或 ``i8 wpan0``，然后在后续所有调用中省略接口名称。支持的 i8sak 实例数量可通过
menuconfig 控制。

``i8sak`` 应用有许多可配置的设置。大多数选项是_粘性的_，意味着如果您设置了端点
短地址一次，任何使用端点短地址的未来操作都可以默认使用之前使用的地址。这对于
缩短命令长度特别有用。

使用方法
==========

i8sak 应用有一系列可调用的 CLI 函数。默认的 i8sak 命令是 ``i8``，以便快速
方便地输入。

一个测试设置包含 2 个来自 MikroElektronika 的 Clicker2-STM32 板，配备
BEE-click（MRF24J40）无线电。选择一个设备作为 PAN 协调器。此设备称为设备 A。

在该设备上运行::

  i8 /dev/ieee0 startpan cd:ab

这将告诉 MAC 层，它现在应使用 PAN ID CD:AB 作为 PAN 协调器。目前，此功能假设
我们运行的是非信标启用的 PAN，因为截至目前，信标启用网络尚未完成。

配置 PAN 协调器短地址和 EP 短地址::

  i8 set saddr 0A:00
  i8 set ep_saddr 0B:00

接下来，在同一设备上运行::

  i8 acceptassoc

注意在第二个命令中，我们没有使用设备名称，因为它是_粘性的_，所以除非我们在
字符驱动之间来回切换，否则只需使用一次。

acceptassoc 命令（不带任何参数）告知 ``i8sak`` 实例接受所有关联请求。
acceptassoc 命令还允许您通过 ``-e`` 选项指定扩展地址来仅接受来自单个设备的请求。

例如::

  i8 acceptassoc -e DEADBEEF00FADE0B

但在此示例中，让我们只使用不带参数的命令。

现在，第二个设备将作为端点设备。i8sak 实例默认处于端点模式。让我们将第二个设备
称为设备 ``B``。

在设备 B 上运行::

  i8 /dev/ieee0 assoc

此命令尝试与配置的端点地址处的节点关联。如果一切设置正确，设备 A 应该有日志信息
表明有设备尝试关联且已接受关联。在设备 ``B`` 上，控制台应显示关联请求成功。
使用所有默认设置，设备 B 应该已被分配短地址 ``0x000B``。

如果您使用数据包嗅探器跟踪，应该看到类似以下内容::

  1) 关联请求
      Frame Type      - CMD
      Sequence Number - 0
      Dest. PAN ID    - 0xFADE
      Dest. Address   - 0x000A
      Src.  PAN ID    - 0xFFFE
      Src.  Address   - 0xDEADBEEF00FADE0C
      Command Type    - Association Request

      1a) ACK
          Frame Type      - ACK
          Sequence Number - 0

  2) 数据请求
      Frame Type      - CMD
      Sequence Number - 1
      Dest. PAN ID    - 0xFADE
      Dest. Address   - 0x000A
      Src.  PAN ID    - 0xFFFE
      Src.  Address   - 0xDEADBEEF00FADE0C
      Command Type    - Data Request

      2a) ACK
          Frame Type      - ACK
          Sequence Number - 1

  3) 关联响应
      Frame Type      - CMD
      Sequence Number - 0
      Dest. PAN ID    - 0xFADE
      Dest. Address   - 0xDEADBEEF00FADE0C
      Src.  Address   - 0xDEADBEEF00FADE0A
      Command Type    - Association Response
      Assigned SADDR  - 0x000B
      Assoc Status    - Successful

      3a) ACK
          Frame Type      - ACK
          Sequence Number - 0

默认端点地址可通过 Kconfig 配置或使用 ``set`` 命令动态设置。

以下是设置端点短地址的方法::

  i8 set ep_saddr 0a:00

设置地址时，重要的是确保端点寻址模式按您需要的方式配置：使用 ``s`` 表示短寻址，
使用 ``e`` 表示扩展寻址::

  i8 set ep_addrmode s

设备 B 现在已成功与设备 A 关联。如果您想从设备 B 向设备 A 发送数据，请在设备 B
上运行以下命令::

  i8 tx ABCDEF

这将立即（实际上不是立即，事务使用 CSMA 发送）向设备 A 发送帧，帧载荷为
``0xABCDEF``

从设备 A 向设备 B 发送数据有所不同。在 IEEE 802.15.4 中，必须从协调器提取帧。
要准备帧，请在设备 A 上运行以下命令::

  i8 tx AB

因为设备模式是 PAN 协调器，``i8sak`` 应用知道将数据作为间接事务发送。如果您在
协调器（但不是 PAN 协调器）设备上运行 ``i8sak`` 应用，可以使用 ``-d`` 选项强制
``i8sak`` 应用直接发送事务，而不是发送给父协调器。

**注意**：目前，间接事务超时已禁用。这意味着必须提取帧，否则空间可能耗尽。这仅
用于测试阶段，因为没有超时更容易调试。重新启用超时可能会影响 ``i8sak`` 应用中间接
事务功能的行为。

要提取数据，请在设备 ``B`` 上运行以下命令::

  i8 poll

此命令轮询端点（在本例中是我们的设备 A PAN 协调器）以查看是否有任何数据。在设备 B
的控制台中，您应该看到轮询请求状态输出。
