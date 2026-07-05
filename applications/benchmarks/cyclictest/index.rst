================================
``Cyclictest`` 基准测试工具
================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

Cyclictest 是一个简单的程序，用于衡量实时操作系统的实时性能。
最初，此程序来自 Linux ``rt-tests``。
然而，NuttX 拥有自己的 cyclictest 工具，它深受原始程序的启发，
但不使用某些高级功能，同时添加了与 NuttX 相关的功能。

新的 cyclictest 的创建源于这样一个事实：截至 2025 年 2 月，
POSIX 时间函数（如 ``clock_gettime`` 和 ``clock_nanosleep``）
依赖于系统滴答（如果系统未编译为 Tickless 模式），
这使得小延迟几乎不可能实现。但是，如果我们使用硬件设备定时器，
可以通过一些 ``ioctl`` 调用实现小的周期性延迟。

需要重新审视文档，以了解当 NuttX 编译为 tickless 模式时 cyclictest 的表现。

在 NuttX 中替代 ``clock_gettime`` 和 ``clock_nanosleep``
------------------------------------------------------------------

配置这样的设备定时器很简单：首先，使用 ``TCIOC_SETTIMEOUT`` ``ioctl`` 调用设置定时器的超时时间。
然后执行 ``TCIOC_NOTIFICATION`` ``ioctl`` 调用。
之后，可以使用 ``poll`` 函数轮询定时器，当定时器超时时返回。

线程延迟唤醒可以通过在 ``poll`` 函数返回后调用 ``TCIOC_GETSTATUS`` ``ioctl`` 调用来测量。
该 ``ioctl`` 调用填充 ``timer_status_s`` 结构体，其中包含两个重要字段：``uint32_t timeleft`` 和 ``uint32_t timeout``。
线程的延迟可以计算为 ``timeout - timeleft``。

程序使用方法
---------------------

尽管存在一些差异，NuttX 移植版本尽可能忠实于原始程序，保持最重要的命令行参数相同。
用户可以选择两种"等待方法"之一：

- ``clock_nanosleep``（``W_NANOSLEEP``），
- 轮询设备（``W_DEVTIMER``）。

用户还可以选择两种"测量方法"之一：

- ``clock_gettime``（``M_GETTIME``），
- 使用设备定时器（``M_TIMER_API``）。

可以组合使用等待和测量方法。截至 2025 年 2 月，
使用 ``W_DEVTIMER`` 和 ``M_TIMER_API`` 产生最佳结果。
但是，它需要由您的 BSP 注册一个定时器设备（例如 ``/dev/timer1``）。
还请注意，当使用 ``W_DEVTIMER`` 时，只有一个线程可以轮询定时器。

可以提供以下命令行参数：

- ``-c --clock [CLOCK]``：0 选择 ``CLOCK_REALTIME``，1 选择 ``CLOCK_MONOTONIC``（默认）
- ``-d --distance [US]``：线程间隔的距离。默认为 500 us。
- ``-D --duration [TIME]``：设置测试持续时间（秒）。默认为 0（无限制）。
- ``-e --help``：显示帮助并退出。
- ``-h --histogram [US]``：将直方图数据输出到标准输出。US 是要打印的最大值。
- ``-H --histofall``：与 ``-h`` 相同，不同之处在于在右侧显示一个额外的直方图列，包含所有线程直方图的汇总数据。如果 cyclictest 只运行一个线程，则 ``-H`` 选项等同于 ``-h``。
- ``-i --interval [US]``：线程间隔。默认为 1000 us。
- ``-l --loops [N]``：测量循环次数。默认为 0（无限制）。
- ``-m --measurement [METHODS]``：设置时间测量方法。0 选择 ``clock_gettime``，1 使用 NuttX 定时器 API。请注意，如果选择 1，需要在 ``-T`` 中指定定时器设备（例如 ``/dev/timer0``）。
- ``-n --nanosleep [METHOD]``：设置等待方法：0 选择 ``clock_nanosleep``，1 等待定时器设备上的 POLLIN 标志。默认为 0。选择 1 仅适用于一个线程，因此 ``-t`` 值设置为 1。如果选择 METHOD 1，需要在 ``-T`` 中指定定时器设备（例如 ``/dev/timer0``）。
- ``-q --quiet``：仅在退出时打印摘要。
- ``-p --prio``：设置第一个线程的优先级。
- ``-t --threads [N]``：要创建的测试线程数。默认为 1。
- ``-T --timer-device [DEV]``：测量定时器设备。当 ``-m=1`` 或 ``-n=1`` 时必须指定。
- ``-y --policy [NAME]``：设置调度策略，其中 NAME 为 fifo、rr、batch、idle、normal、other。

示例用法
-------------
``cyclictest -p 150 -T /dev/timer1 -m 1 -n 1 -h 20 -D 100 -i 50``

由于使用了 ``W_DEVTIMER``，只有一个线程每 50 us 运行一次。
测量方法是设备定时器本身，在 ``-T`` 中指定。
测试运行 100 秒。优先级提升到 150，因此测量不受其他任务或通信的影响。

命令输出（在 Microchip ATSAMV71Q21B @ 300 MHz 上测试）：

.. code-block:: text

  # Histogram
  000000 000000
  000001 000000
  000002 000000
  000003 000000
  000004 000000
  000005 000000
  000006 000000
  000007 000000
  000008 000000
  000009 000000
  000010 603045
  000011 1395782
  000012 000804
  000013 000153
  000014 000034
  000015 000083
  000016 000030
  000017 000000
  000018 000000
  000019 000000
  # Total: 001999931
  # Min Latencies: 00010
  # Avg Latencies: 00010
  # Max Latencies: 00016
  # Histogram Overflows: 00000
