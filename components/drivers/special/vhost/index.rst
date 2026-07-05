=====
Vhost
=====

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

Vhost 是 NuttX 中 VirtIO 的后端实现。在标准 Linux 内核中，Vhost 是一种通过卸载 VirtIO 设备数据平面处理来提高虚拟机 I/O 性能的技术，NuttX 将此概念扩展到跨核通信场景。

在 NuttX 中，Vhost 被定义为完整的 VirtIO 后端实现。它通过 Vhost-Rptun/PCI <-> VirtIO-Rptun/PCI 与 VirtIO 前端配合工作，实现跨核通信。本质上，NuttX 中的 Vhost 是 VirtIO Device 的完整实现，类似于 QEMU 中的 VirtIO Device 实现。

比较
==========

下表比较了 NuttX Vhost、Linux Vhost 和 QEMU VirtIO Device：

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - 维度
     - NuttX Vhost
     - Linux Vhost
     - QEMU VirtIO Device
   * - 使用场景
     - 跨核通信
     - 虚拟化性能
     - 虚拟化
   * - 传输支持
     - Rptun 和 PCI
     - MMIO 和 PCI
     - MMIO 和 PCI
   * - 数据平面
     - 包含
     - 包含
     - 包含
   * - 控制平面
     - 包含
     - 不包含（由虚拟机管理程序）
     - 包含

Vhost 和 VirtIO 是互补的概念，代表"后端"和"前端"的关系。在跨核通信场景中，一方充当"前端"（VirtIO Driver），另一方充当"后端"（Vhost Driver，即 VirtIO Device 实现）。

.. toctree::
   :maxdepth: 1
   :caption: 目录

   framework
