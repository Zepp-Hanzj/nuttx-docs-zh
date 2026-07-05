======
VirtIO
======

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

VirtIO（虚拟 I/O）是半虚拟化环境中虚拟设备的标准化接口。NuttX 基于 OpenAMP 实现了完整的 VirtIO 框架，支持各种 VirtIO 驱动，如 VirtIO-Net、VirtIO-Block、VirtIO-Serial 等。

框架支持不同的传输层实现，包括 VirtIO-MMIO、VirtIO-PCI 和 VirtIO-Remoteproc。

.. toctree::
   :maxdepth: 1
   :caption: 目录

   framework
