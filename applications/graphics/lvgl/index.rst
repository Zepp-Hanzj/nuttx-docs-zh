.. _lvgl:

=============
``lvgl`` LVGL
=============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

使用方法
-----

通过 ``#include <lvgl/lvgl.h>`` 或 ``#include <lvgl.h>`` 导入。

移植到 NuttX 的上游示例位于 ``examples/lvgldemo``。

LVGL 可以与帧缓冲设备配合使用。要查找已预配置此功能的示例板，请在 ``defconfig`` 文件中搜索 ``CONFIG_GRAPHICS_LVGL=y``。它们也都具有 ``CONFIG_VIDEO_FB=y``。

作为第二种选择，LVGL 可以与显示驱动程序通信并逐行显式绘制。对于这种情况，没有预配置的板。请参阅上游文档的 _Porting_ 部分获取更多提示。

资源
---------

- `API 文档及示例 <https://docs.lvgl.io/latest/en/html/index.html>`_
- `GitHub / LVGL / LVGL 库 <https://github.com/lvgl/lvgl>`_
- `GitHub / LVGL / 示例、教程、应用程序 <https://github.com/lvgl/lv_examples>`_
- `GitHub / LVGL / 桌面模拟器 <https://github.com/lvgl/lv_sim_eclipse_sdl>`_
- `GitHub / LVGL / Web 模拟器 <https://github.com/lvgl/lv_sim_emscripten>`_
