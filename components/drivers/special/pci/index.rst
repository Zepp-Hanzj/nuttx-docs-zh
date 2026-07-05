=================
PCI(e) 总线驱动
=================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

PCI(e) 总线驱动位于 ``drivers/pci`` 中。

支持的 PCI 设备
=====================

PCI QEMU 测试设备
--------------------

由 QEMU 提供的测试设备，通过 ``-device pci-testdev`` 启用。

PCI QEMU EDU 设备
-------------------

由 QEMU 提供的测试设备，通过 ``-device edu`` 启用。

虚拟机间共享内存设备 (ivshmem)
--------------------------------------

虚拟机间共享内存支持可在 ``drivers/pci/pci_ivshmem.c`` 中找到。

此实现适用于 ``ivshmem-v1``，与 QEMU 和 ACRN 虚拟机管理程序兼容，但不适用于使用 ``ivshmem-v2`` 的 Jailhouse 虚拟机管理程序。

16550 兼容串口卡
----------------------------

UART 16550 兼容 PCI 串口卡支持可在 ``drivers/serial/uart_pci_16550.c`` 中找到。

支持的设备：

- AX99100
- QEMU pci-serial 设备
- QEMU pci-serial-2x 设备
- QEMU pci-serial-4x 设备

Intel e1000
-----------

Intel e1000 兼容网卡支持可在 ``drivers/net/e1000.c`` 中找到。

支持的设备：

- Intel I219
- Intel 82540EM
- Intel 82574L

Intel igb
---------

Intel igb 兼容网卡支持可在 ``drivers/net/igb.c`` 中找到。

支持的设备：

- Intel 82576
- Intel I211

Intel igc
---------

Intel igc 兼容网卡支持可在 ``drivers/net/igc.c`` 中找到。

支持的设备：

- Intel I225LM
- Intel I226V

Kvaser PCI CAN 卡
-------------------

目前该卡仅在 QEMU 中可用。

驱动支持 SocketCAN 接口和字符驱动。

驱动需要在主机上运行 ``vcan``：

.. code:: shell

   sudo ip link add dev can0 type vcan
   sudo ip link set can0 up

在 ``x86_64`` 上运行驱动的示例命令：

.. code:: shell

   qemu-system-x86_64 -m 2G -cpu host -enable-kvm -kernel nuttx \
   -nographic -serial mon:stdio -object can-bus,id=canbus0 \
   -object can-host-socketcan,id=canhost0,if=can0,canbus=canbus0 \
   -device kvaser_pci,canbus=canbus0


CTUCANFD PCI CAN 卡
---------------------

目前该卡仅在 QEMU 中可用。

驱动支持 SocketCAN 接口和字符驱动。

驱动需要在主机上运行 ``vcan``：

.. code:: shell

   sudo ip link add dev can0 type vcan
   sudo ip link set can0 up

在 ``x86_64`` 上运行驱动的示例命令：

.. code:: shell

   qemu-system-x86_64 -m 2G -cpu host -enable-kvm -kernel nuttx \
   -nographic -serial mon:stdio -object can-bus,id=canbus0-bus \
   -object can-host-socketcan,if=can0,canbus=canbus0-bus,id=canbus0-socketcan \
   -device ctucan_pci,canbus0=canbus0-bus,canbus1=canbus0-bus

通过 PCI 的 xHCI
-------------

xHCI 支持已在 x86_64 目标上测试，包括 QEMU 和真实硬件。

此驱动的已知问题：

- 目前仅支持 USB2.0，NuttX 中尚无 USB3.0 支持。

- 尚不支持 USB HUB 设备

要在 QEMU 上启用 xHCI 支持，需要添加 ``-device qemu-xhci`` 参数。QEMU 中所有支持的 USB 设备可在 `QEMU 文档 <https://qemu-project.gitlab.io/qemu/system/devices/usb.html>`_ 中找到，但并非所有类都在 NuttX 中支持。
