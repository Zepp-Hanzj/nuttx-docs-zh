======================================
USB 视频类 (UVC) Gadget 驱动
======================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

概述
========

UVC gadget 驱动 (``drivers/usbdev/uvc.c``) 实现了 USB 视频类 1.1 设备，使 NuttX 在主机端显示为 USB 摄像头。驱动暴露一个字符设备 (``/dev/uvc0``)，应用程序向其写入视频帧。它内部处理所有 UVC 类特定的控制请求（PROBE / COMMIT），并使用批量传输进行视频数据传输。

驱动支持两种模式：

- **独立模式** – UVC 功能是总线上唯一的 USB 类。
- **复合模式** – UVC 功能与其他 USB 类驱动（如 CDC/ACM）通过 NuttX 复合设备框架组合。

特性
========

- UVC 1.1 兼容（未压缩 YUY2 格式）
- 视频数据的批量传输模式
- 与主机的自动 PROBE / COMMIT 协商
- ``poll()`` 支持 – 应用程序可以等待主机开始流式传输（``POLLOUT``）并检测断开连接（``POLLHUP``）
- 运行时视频参数 – 分辨率和帧率在初始化时传递，因此 USB 描述符始终匹配实际传感器
- ``boardctl()`` 集成，便于应用程序级启动

配置
=============

驱动通过以下 Kconfig 选项启用：

.. code-block:: kconfig

   CONFIG_USBUVC=y                  # 启用 UVC gadget 支持
   CONFIG_USBUVC_COMPOSITE=n        # 设为 y 以使用复合设备模式
   CONFIG_USBUVC_EPBULKIN=1         # 批量 IN 端点编号（独立模式）
   CONFIG_USBUVC_EP0MAXPACKET=64    # EP0 最大包大小（独立模式）
   CONFIG_USBUVC_EPBULKIN_FSSIZE=64 # 批量 IN 全速最大包大小
   CONFIG_USBUVC_NWRREQS=4          # 预分配写请求数量
   CONFIG_USBUVC_NPOLLWAITERS=2     # poll 等待者数量

头文件
============

- ``include/nuttx/usb/uvc.h`` – 公共 API、UVC 描述符常量和数据结构。

数据结构
===============

``struct uvc_params_s``
-----------------------

传递给初始化函数，以便 USB 描述符反映实际传感器能力::

  struct uvc_params_s
  {
    uint16_t width;    /* 帧宽度（像素） */
    uint16_t height;   /* 帧高度（像素） */
    uint8_t  fps;      /* 每秒帧数 */
  };

公共接口
=================

独立模式
---------------

``usbdev_uvc_initialize()``
  初始化 UVC gadget 并注册 ``/dev/uvc0``。*params* 可以为 ``NULL`` 以使用默认值（320 × 240 @ 5 fps）。返回用于后续 ``usbdev_uvc_uninitialize()`` 的句柄。

``usbdev_uvc_uninitialize()``
  拆除 UVC gadget 并注销字符设备。

复合模式
--------------

``usbdev_uvc_classobject()``
  创建用于复合设备内部的 UVC 类驱动实例。

``usbdev_uvc_classuninitialize()``
  销毁由 ``usbdev_uvc_classobject()`` 创建的类驱动实例。

``usbdev_uvc_get_composite_devdesc()``
  为复合框架填充 ``composite_devdesc_s``。

boardctl 集成
--------------------

应用程序可以通过 ``boardctl()`` 管理 UVC gadget::

  struct boardioc_usbdev_ctrl_s ctrl;
  struct uvc_params_s params = { .width = 320, .height = 240, .fps = 15 };
  FAR void *handle = (FAR void *)&params;

  ctrl.usbdev   = BOARDIOC_USBDEV_UVC;
  ctrl.action   = BOARDIOC_USBDEV_CONNECT;
  ctrl.instance = 0;
  ctrl.config   = 0;
  ctrl.handle   = &handle;

  boardctl(BOARDIOC_USBDEV_CONTROL, (uintptr_t)&ctrl);

  /* ... 使用 /dev/uvc0 ... */

  ctrl.action = BOARDIOC_USBDEV_DISCONNECT;
  boardctl(BOARDIOC_USBDEV_CONTROL, (uintptr_t)&ctrl);

设备操作
================

1. 应用程序打开 ``/dev/uvc0`` 进行写入。
2. 使用 ``poll()`` 配合 ``POLLOUT`` 等待 USB 主机开始流式传输（即主机发送 VS_COMMIT_CONTROL SET_CUR 请求）。
3. 通过 ``write()`` 写入完整的视频帧。驱动自动在前面添加 2 字节的 UVC 载荷头（带有 FID / EOF 位）。
4. 当主机停止流式传输时，``write()`` 返回 ``-EAGAIN``。应用程序可以再次 ``poll()`` 等待主机重新启动。
5. 当主机显式停止流式传输时报告 ``POLLHUP``。
