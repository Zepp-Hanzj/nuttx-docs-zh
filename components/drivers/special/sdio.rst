===================
SDIO 设备驱动
===================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

-  ``include/nuttx/sdio.h``。使用 SDIO 驱动所需的
   所有结构和 API 都在此头文件中提供。

-  ``struct sdio_dev_s``。每个 SDIO 设备驱动必须实现
   ``struct sdio_dev_s`` 的一个实例。该结构定义了包含以下方法的调用表：

   互斥：

   初始化/设置：

   命令/状态/数据传输：

   事件/回调支持：

   DMA 支持：

-  **绑定 SDIO 驱动**。SDIO 驱动通常不由用户代码直接
   访问，而是绑定到另一个更高级别的设备驱动。通常的绑定顺序是：

   #. 从硬件特定的 SDIO 设备驱动获取 ``struct sdio_dev_s`` 的
      实例，然后
   #. 将该实例提供给更高级别设备驱动的初始化方法。

-  **示例**：``arch/arm/src/stm32/stm32_sdio.c`` 和
   ``drivers/mmcsd/mmcsd_sdio.c``

实现 SDIO 下半部分
===============================

在实现新的 SDMMC 控制器驱动（SDIO 下半部分）时，它必须提供 ``struct sdio_dev_s`` 中定义的接口。

调用流程（简化示例）
------------------------------

SDIO/MMCSD 的完整卡识别和初始化调用流程更为复杂，包括额外的命令（例如 CMD0、CMD8、ACMD41 / CMD1、CMD2、CMD3、错误处理、重试等）。为了记录下半部分对 R2/CID/CSD 处理的要求，CMD9 附近的简化交互如下：

1. ``SDIO_SENDCMD``：发送产生 R2 响应的命令（例如，CMD2 用于 CID，CMD9 用于 CSD）。
2. ``SDIO_WAITRESPONSE``：轮询硬件完成命令。
3. ``SDIO_RECVR2``：检索 136 位响应，并将解码后的 128 位 CID/CSD 载荷提供给 MMCSD 上半部分。

有关完整的卡初始化和命令序列，请参阅 MMC/SD 物理层规范中的卡初始化流程图。

R2（136 位）响应和 CSD/CID
---------------------------------

标准 R2 响应格式包括 7 位 CRC，许多硬件控制器会自动验证和剥离。MMCSD 上半部分期望提供的 128 位缓冲区包含标准布局（位 127-0）的 CID 或 CSD 载荷。

如果控制器剥离了 CRC 字节，硬件寄存器中的剩余位通常是错位的（移位的）。如果寄存器中不包含 CRC，下半部分必须将四个 32 位字左移一个字节（8 位），然后通过 ``recv_r2`` 返回。

参见 ``arch/arm64/src/bcm2711/bcm2711_sdio.c`` 或 ``arch/arm64/src/imx9/imx9_usdhc.c`` 了解此移位逻辑的参考实现。
