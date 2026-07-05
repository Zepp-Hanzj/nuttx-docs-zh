====================
帧缓冲驱动
====================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

帧缓冲区是一个内存映射的缓冲区，用于表示驱动视频显示所需的所有像素。

帧缓冲驱动适用于以下场景：

#. 需要保存驱动视频显示所需的所有像素时。包括：

   #. 直接访问底层帧缓冲区的图形库；
   #. 需要回读图像数据的高级 UI（例如 alpha 混合）；

#. 期望帧缓冲区存在的应用程序；

绑定
========

LCD 和帧缓冲驱动通常不由用户代码直接访问，而是绑定到另一个更高级别的设备驱动。通常的绑定顺序是：

#. 从硬件特定的帧缓冲设备驱动获取 ``struct fb_vtable_s`` 实例，然后
#. 将该实例提供给更高级别设备驱动的初始化方法。

.. _genericlcdfb:

通用 LCD 帧缓冲
------------------------

本示例将介绍从用户空间到硬件特定细节的路径，说明 LCD 屏幕如何绑定到帧缓冲区。

#. ``include/nuttx/video/fb.h`` 提供了使用帧缓冲驱动所需的所有结构和 API：

   #. ``drivers/video/fb.c`` 是更高级别的设备驱动。``struct fb_vtable_s`` 的实例将被提供给它；
   #. ``fb_register`` 在 ``/dev/fbN`` 注册帧缓冲字符设备，其中 N 是显示编号；
   #. 它还提供了 ``up_fbinitialize`` 的原型，可以由以下方式定义：

      #. ``arch/<arch>/src/<chip>`` 目录中的特定设备；
      #. 或者由 ``drivers/lcd/lcd_framebuffer.c`` 中的 LCD 帧缓冲适配器定义，该适配器在帧缓冲驱动和 LCD 屏幕驱动之间提供中间接口；

#. 假设我们使用 LCD 帧缓冲（``CONFIG_LCD_FRAMEBUFFER = y``）：

   #. 此接口实现了 ``up_fbinitialize``，它：

      #. 提供 ``struct fb_vtable_s`` 的实例（``struct lcdfb_dev_s`` 的成员）；
      #. 调用 ``board_lcd_initialize`` 和 ``board_lcd_getdev`` LCD 特定函数。这些函数定义在 ``boards/<arch>/<chip>/<board>/src`` 中，原型在 ``include/nuttx/board.h`` 中；

#. 最后，LCD 屏幕驱动通常位于 ``drivers/lcd/`` 中，实现了 ``include/nuttx/lcd/lcd.h`` 中定义的回调：

    #. ``include/nuttx/lcd/lcd.h`` 提供了使用 LCD 屏幕所需的结构和 API，无论使用帧缓冲适配器还是 :doc:`lcd`；

VSYNC
======

垂直同步 (VSync) 将应用程序图形的帧率与显示器的刷新率同步，有助于建立稳定性。如果不同步，可能会导致画面撕裂，即图像出现水平锯齿边缘或在整个屏幕上出现重影的现象。

VSYNC 偏移
------------

在 VSYNC 事件期间，屏幕开始显示第 N 帧，而渲染器开始为第 N+1 帧合成窗口。应用程序处理等待的输入并生成第 N+2 帧。当渲染器渲染时间较短时，从渲染结束到屏幕显示完成可能延迟近两帧。为解决此问题，可以使用 ``FBIOSET_VSYNCOFFSET`` 设置 VSYNC 偏移时间（以微秒为单位），利用 VSYNC 偏移减少从输入设备到屏幕的延迟。


示例
========

示例适用于 :ref:`genericlcdfb` 的特定情况：

.. _ttgotdisplayesp32_fb:

TTGO T-Display ESP32 开发板
---------------------------

此开发板包含一个 ST7789 TFT 显示屏 (135x240)。通过选择 ``ttgo_t_display_esp32:lvgl_fb`` 配置，``lvgldemo`` 示例将使用帧缓冲接口构建。

* ``boards/xtensa/esp32/ttgo_t_display_esp32/src/esp32_bringup.c`` 注册帧缓冲驱动：

.. code-block:: c

   #ifdef CONFIG_VIDEO_FB
     ret = fb_register(0, 0);
     if (ret < 0)
       {
         syslog(LOG_ERR, "ERROR: Failed to initialize Frame Buffer Driver.\n");
       }
   #endif

* 当 ``CONFIG_LCD_FRAMEBUFFER = y`` 时，帧缓冲适配器中的 ``up_fbinitialize`` 将被调用：

   * ``board_lcd_initialize`` 和 ``board_lcd_getdev`` 定义在 ``boards/xtensa/esp32/common/src/esp32_st7789.c`` 中：

       * ``board_lcd_initialize`` 通过定义连接到显示控制器的 SPI 接口来初始化开发板上的 LCD 硬件；
       * ``board_lcd_getdev`` 调用 ``st7789_lcdinitialize`` 并返回指定 LCD 的 LCD 对象引用；
       * ``st7789_lcdinitialize`` 是 LCD 屏幕驱动的一部分，位于 ``drivers/lcd/st7789.c``；

* LVGL 演示应用程序 (``lvgldemo``) 使用 ``ioctl`` 系统调用触发 ``FBIO_UPDATE`` 请求到更高级别的设备驱动，以使用帧缓冲数据刷新 LCD 屏幕：

.. code-block:: c

   ioctl(state.fd, FBIO_UPDATE, (unsigned long)((uintptr_t)&fb_area));

NuttX 模拟器
----------------

:doc:`NuttX 模拟器 </platforms/sim/sim/index>` 提供了一个基于 X11 的帧缓冲驱动，用于在兼容 X11 的主机上模拟帧缓冲使用。

通过选择 ``sim:lvgl_fb`` 配置，``lvgldemo`` 示例将使用帧缓冲驱动构建。

* ``boards/sim/sim/sim/src/sim_bringup.c`` 以与 :ref:`ttgotdisplayesp32_fb` 相同的方式注册帧缓冲驱动；
* 当分别设置 ``CONFIG_SIM_FRAMEBUFFER = y`` 和 ``CONFIG_SIM_X11FB = y`` 时，将构建 ``arch/sim/src/sim/up_framebuffer.c`` 和 ``arch/sim/src/sim/up_x11framebuffer.c``；

   * ``up_framebuffer.c`` 提供 ``up_fbinitialize``，并
   * 调用 ``up_x11framebuffer.c`` 中的 ``up_x11initialize``，该函数将基于 X11 的窗口初始化为帧缓冲区。这是底层"驱动"。

* LVGL 演示应用程序 (``lvgldemo``) 使用 ``ioctl`` 系统调用触发 ``FBIO_UPDATE`` 请求到更高级别的设备驱动，以通常方式使用帧缓冲数据刷新 LCD 屏幕；

.. warning::

   必须考虑帧缓冲区需要表示整个显示器的像素。以 320x480 @RGB565 LCD 屏幕为例，这将是 300KiB，对于内存受限的设备来说可能太大。

   然而，当内存不受限制时，帧缓冲区可以为应用程序提供更快的显示内容更新方式，因为写入 RAM 映射缓冲区比进行多次 SPI 传输更快。

   对于内存受限的设备，请考虑使用 :doc:`lcd`。
