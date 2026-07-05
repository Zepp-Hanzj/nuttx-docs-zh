==========================
RPTUN (Remoteproc 隧道)
==========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

RPTUN (Remoteproc 隧道) 是一个基于 OpenAMP 的高效核间通信框架。它主要解决非对称多处理 (AMP) 架构中运行 NuttX 的主核与远程核之间的生命周期管理和数据交换问题。

RPTUN 框架由两个核心组件组成：

- **RPTUN Remoteproc**：管理远程核的生命周期，包括启动、停止和复位操作。

- **VirtIO/Vhost RPTUN**：作为 VirtIO 的传输层，使标准 VirtIO/Vhost 设备能够跨物理核通信。

此外，RPTUN 向用户空间导出标准字符设备接口，允许开发人员通过命令行或应用程序进行调试和控制。

.. toctree::
   :maxdepth: 2

   architecture.rst
   resource_table.rst
   driver_porting.rst
   api_reference.rst

目标受众
===============

本文档面向需要在 NuttX 环境中开发和移植多核系统的嵌入式系统工程师，包括：

- 需要使用 RPTUN 进行核间通信的应用程序开发人员。
- 需要在新硬件平台 (BSP) 上适配 RPTUN 的驱动开发人员。

支持的 RPTUN 服务
========================

- RPMSG 文件系统
- RPMSG 域（远程）套接字
- RPMSG UART 驱动
- RPMSG 网络驱动
- RPMSG Usersock
- RPMSG 传感器驱动
- RPMSG RTC 驱动
- RPMSG MTD
- RPMSG 设备
- RPMSG 块驱动
- RPMSG IO 扩展器
- RPMSG uinput
- RPMSG CLK 驱动
- RPMSG Syslog
- RPMSG Regulator

源文件
============

- 框架实现：``nuttx/drivers/rptun/rptun.c``
- 公共头文件：``nuttx/include/nuttx/rptun/rptun.h``
