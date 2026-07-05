=============================================
``calib_udelay`` udelay 校准工具
=============================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

此工具用于校准配置选项 ``CONFIG_BOARD_LOOPSPERMSEC``。NuttX 使用此选项在板级逻辑中需要非常基本的忙等待休眠时执行忙等待（即在循环中旋转）。当基于定时器的休眠函数对较短的计时没有足够低的分辨率时（即系统每 1ms 一次 tick 但您希望休眠 100us），有时也会使用此选项。

在将 NuttX 移植到新板时，此示例程序对于获取 ``CONFIG_BOARD_LOOPSPERMSEC`` 的校准值非常有用。

.. note::

   如果您在测试驱动程序时遇到意外问题，请确保此配置选项已校准。如果未校准，可能会导致驱动程序中的时序错误/不正确。

以下是运行应用程序的示例输出：

.. code-block:: console

   nsh> calib_udelay

   Calibrating timer for main calibration...
   Performing main calibration for udelay.This will take approx. 17.280 seconds.
   Calibration slope for udelay:
     Y = m*X + b, where
       X is loop iterations,
       Y is time in nanoseconds,
       b is base overhead,
       m is nanoseconds per loop iteration.

     m = 5.33333333 nsec/iter
     b = -199999.99999995 nsec

     Correlation coefficient, R² = 1.0000

   Without overhead, 0.18750000 iterations per nanosecond and 187500.00 iterations per millis.

   Recommended setting for CONFIG_BOARD_LOOPSPERMSEC:
      CONFIG_BOARD_LOOPSPERMSEC=187500

您可以简单地从控制台输出中复制粘贴该值，并在 Kconfig 菜单中设置它作为您板子的值。

程序在不带任何参数的情况下运行。程序运行方式的配置选项（进行更多测量等）可以在其 Kconfig 菜单中查看。将光标高亮显示在配置选项上按 ``h`` 可以阅读每个选项作用的帮助文本。
