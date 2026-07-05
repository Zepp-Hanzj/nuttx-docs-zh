============================
STM32 空指针检测
============================

空指针问题
========================

软件 bug 的一个常见原因是空指针。如果指针未初始化且未检查，它们可能是 NULL。使用 NULL 指针几乎总是会导致不好的事情发生。通常，NULL 指针访问会导致错误异常和/或诊断崩溃。但在地址 0x0000:0000 处有有效地址解码的 MCU 上，使用 NULL 指针可能根本不会导致崩溃，而是可能导致奇怪的行为，有时可能难以调试。

Cortex-M 内存
===============

Cortex-M 系列（Cortex-M0、M3 和 M4）就是这样的 MCU。它们的中断向量位于地址零处。因此，NULL 指针访问不一定会导致崩溃。相反，NULL 指针将访问向量表附近的内存，谁知道接下来会发生什么？

STM32 内存别名
=====================

STMicro STM32 系列 Cortex-M3/4 MCU 的做法略有不同。FLASH 的物理地址为 0x0800:0000；STM32 向量表物理上位于 0x0800:0000 而不是 0x0000:0000。如果 STM32 硬件配置为从 FLASH 启动，STM32 将重新映射 FLASH 内存，使其在地址 0x0000:0000 处别名。这样，STM32 可以从 FLASH 或外部内存或它能够映射的任何其他内存区域启动。

在 NuttX 链接器脚本中，应用程序被链接为从物理 FLASH 区域地址 0x0800:0000 执行。所有有效的 FLASH 内存访问将访问 0x0800:0000 FLASH 地址范围内的内存。但非法的 NULL 指针访问将访问从 0x0000:0000 开始的 FLASH 别名副本。所以我们仍然有这个问题。

Cortex-M 内存保护单元
===================================

内存保护单元 (MPU) 是 Cortex-M 实现的可选组件。最流行的 Cortex-M3/4 MCU 大多支持 MPU。MPU 可用于保护内存区域，以便如果有任何对某些内存区域的未授权访问尝试，将发生内存保护违规异常，系统将检测到非法访问。

有关 Cortex-M3/4 系列和 Cortex-M3/4 MPU 的更多信息，请参阅 ARM 网站。例如参见 `2.2. Memory Protection Unit (MPU) <http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.dai0179b/CHDFDFIG.html>`_。

使用 MPU 检测空指针使用
==========================================

因此，对于 STM32，我们可以做的一件事是编程 MPU 以禁止软件访问从地址 0x0000:0000 开始的内存区域。Petteri Aimonen 在 NuttX 论坛上发布了一个代码片段，展示了如何做到这一点。以下是 Petteri 的帖子：

.. code-block:: C

   /* Catch any null pointer dereferences */

   int region = 0;

   putreg32(region, MPU_RNR);
   putreg32(0, MPU_RBAR);
   putreg32(MPU_RASR_ENABLE | MPU_RASR_SIZE_LOG2(20) | (0xFF << MPU_RASR_SRD_SHIFT) | MPU_RASR_AP_NONO, MPU_RASR);
   mpu_control(true, false, true);
