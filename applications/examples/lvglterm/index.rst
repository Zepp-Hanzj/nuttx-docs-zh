==============================================
``lvglterm`` NuttShell (NSH) 的 LVGL 终端
==============================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

一个 LVGL 应用程序，执行通过触摸屏键盘输入的 NuttShell (NSH) 命令
并显示 NSH 输出。前提配置设置：

- ``CONFIG_NSH_CONSOLE=y`` – 必须配置 NSH 使用控制台。
- ``CONFIG_LIBC_EXECFUNCS=y`` – 必须启用 posix_spawn()。
- ``CONFIG_PIPES=y`` – 必须启用管道。
- ``CONFIG_GRAPHICS_LVGL=y`` – 必须启用 LVGL 图形。
- ``CONFIG_LV_FONT_UNSCII_16=y`` – 必须启用 LVGL 字体 UNSCII 16。
