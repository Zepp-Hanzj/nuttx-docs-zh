====
SLIP
====

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

SLIP 配置
==================

#. 使用配置中启用 SLIP 来配置和构建 NuttX。将其加载到 FLASH 并启动设备。

#. 使用串行电缆连接到 Linux 机器。本讨论假设两端的串行设备都是
   ``/dev/ttyS0``。

#. 在目标端重置并在 Linux 端附加 SLIP：

   .. code-block:: bash

      $ modprobe slip
      $ slattach -L -p slip -s 57600 /dev/ttyS0 &

   这应该创建一个名为 sl0 或 sl1 等的接口。添加 -d 以获取调试输出。
   这将显示接口名称。

   注意：包含 -L 选项是为了抑制硬件流控制的使用。
   仅当您在目标上不支持硬件流控制时才需要这样做。

   注意：Linux slip 模块将其 MTU 大小硬编码为 296。因此您最好也将
   ``CONFIG_NET_ETH_MTU`` 设置为 296。

#. 将线路交给 SLIP 驱动后，您必须配置网络接口。同样，使用标准的
   ifconfig 和 route 命令。假设我们已从您的目标（地址为 10.0.0.2）
   连接到地址为 192.168.0.101 的主机 PC。在 Linux PC 上，
   您需要以 root 身份执行以下操作（假设 SLIP 附加到设备 sl0）：

   .. code-block:: bash

      $ ifconfig sl0 10.0.0.1 pointopoint 10.0.0.2 up
      $ route add 10.0.0.2 dev sl0

#. 用于监控/调试流量：

   .. code-block:: bash

      $ tcpdump -n -nn -i sl0 -x -X -s 1500

   注意：如果硬件握手不可用，您可以尝试 slattach 选项 -L，
   该选项应启用"3 线操作"。
