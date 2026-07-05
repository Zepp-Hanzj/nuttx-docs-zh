=====================
单次定时器驱动程序
=====================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 定时子系统由四层组成：

  * 1 硬件定时器驱动程序：包含各种硬件定时器驱动程序的实现。
  * 2 定时器驱动程序抽象：如 Oneshot 和 Timer，提供单次/周期定时器硬件抽象。
  * 3 操作系统定时器接口：Arch_Timer(up_timer_*) 和 Arch_Alarm(up_alarm_*),
    提供相对定时器（在一定延迟后触发事件）和绝对定时器（在特定时间触发事件）接口。
  * 4 操作系统定时器抽象：wdog 定时器管理软件定时器，并为上层提供统一的定时器 API。

这里我们重点介绍单次定时器驱动程序抽象。

Oneshot 是提供以下功能的定时器驱动程序抽象：

  * 不同定时器硬件的统一 API。
  * 计数与自然时间之间功能正确且优化的时序转换。

背景
==========

计算机通常依赖硬件周期计数器来计算外部时钟信号的电平变化。这些信号由晶体振荡器产生。信号然后经过锁相环（PLL）进行倍频，并作为时钟信号输出到硬件周期计数器。

计数器向上或向下计数——每次电平变化时计数，实现基于硬件的定时。为了生成定时中断，定时器硬件包含一个比较器。当递减计数器达到零或周期计数器匹配预设值时，它触发 CPU 中断。

根据定时器的功能，我们可以抽象出定时器应提供的最小功能集：

  * 1. 读取当前周期计数
  * 2. 在绝对周期计数时触发事件
  * 3. 在相对周期计数后触发事件

从操作系统的角度来看，假设第一个可用，第二个和第三个在功能上是等效的。通过重新编程定时器，这些也可以模拟周期定时器。虽然这些方法在表达能力上相似，但使用相对延迟的定时器往往不如支持绝对定时的定时器精确和高效。这是因为读取当前时间会引入额外的 CPU 开销，影响时序精度和性能。

Oneshot 驱动程序 API
===================

OneShot 目前提供基于计数的新接口，同时为了兼容旧驱动程序也提供基于 timespec 的接口。我们强烈建议使用基于计数的接口，因为其性能更优越。此外，基于计数的 API 更容易实现，因为它们只需要专注于读写定时器相关的寄存器，而无需执行容易出错的时间转换。

在基于计数的接口设计中，oneshot 采用以下原则：

  * 极简设计：显著简化驱动程序的实现。
  * 基于计数的接口：使用计数周期作为读取时间和设置定时器的单位。
  * 支持绝对和相对定时器：兼容底层定时器硬件，无论它使用绝对还是相对定时。
  * 无状态返回：由于对定时器硬件的读/写操作不应失败，任何失败都应在驱动程序级别产生断言。
  * 无回调或参数：所有过期回调和参数管理都在上层处理，防止线程不安全的使用。

基于计数的接口如下：

  * ``clkcnt_t (*current)(FAR struct oneshot_lowerhalf_s *lower);``
  * ``void     (*start)(FAR struct oneshot_lowerhalf_s *lower, clkcnt_t delay);``
  * ``void     (*start_absolute)(FAR struct oneshot_lowerhalf_s *lower, clkcnt_t cnt);``
  * ``void     (*cancel)(FAR struct oneshot_lowerhalf_s *lower);``
  * ``clkcnt_t (*max_delay)(FAR struct oneshot_lowerhalf_s *lower);``

上述基于计数的接口提供以下功能：

  * 获取当前定时器计数，
  * 启动相对定时器，
  * 启动绝对定时器，
  * 取消定时器事件，
  * 获取最大定时器延迟。

请注意，如果驱动程序使用基于计数的 API，它应在初始化期间调用 ``oneshot_count_init`` 以告知上层定时器频率。

基于计数的接口通过 ``CONFIG_ONESHOT_COUNT`` 启用。

以下是已弃用的 timespec 接口：

  * ``int (*max_delay)(FAR struct oneshot_lowerhalf_s *lower, FAR struct timespec *ts);``
  * ``int (*start)(FAR struct oneshot_lowerhalf_s *lower, FAR const struct timespec *ts);``
  * ``int (*cancel)(FAR struct oneshot_lowerhalf_s *lower, FAR struct timespec *ts);``
  * ``int (*current)(FAR struct oneshot_lowerhalf_s *lower, FAR struct timespec *ts);``

它们提供以下功能：

  * 获取最大定时器延迟，
  * 启动相对定时器，
  * 取消定时器事件，
  * 获取当前定时器计数。

ClockCount
==========

推荐的 oneshot API 都是基于计数的。那么我们如何处理时间转换呢？我们提供了一个统一的 ClockCount(clockcount.h) 层，用于快速和安全的时间转换，包括：

  * 计数转 timespec
  * 计数转 tick
  * timespec 转计数
  * tick 转计数

我们注意到在时序转换中始终存在至少两次除法。因此 clockcount 实现了两种方法来加速时间转换：

  1. 不变除数除法优化：用于将计数转换为秒或 tick。可通过 ``CONFIG_ONESHOT_FAST_DIVISION`` 启用。
  此除法优化可以将除法转换为：

    * 一次无符号高位乘法（UMULH），
    * 一次减法，
    * 一次加法，和
    * 一次逻辑右移（LShR）。

  请注意，不变除数除法优化不一定提供性能优势。它与 UMULH 和 UDIV 指令在不同 CPU 平台上的开销有关。
  例如，在早期的 ARMv8A 平台（Cortex A-53）上，UMULH 需要 6 个周期，这意味着启用优化实际上比使用 UDIV 指令直接除法效率更低。

  2. 乘移近似除法：用于将增量计数转换为纳秒或 tick。

  请注意，默认情况下已启用。如果需要极其精确的时间转换，应禁用它。
  此方法以轻微的精度损失（几纳秒）换取更好的性能。但是，由于潜在的乘法溢出，它仅适用于相对时间转换。
  第一种方法是精确的，但需要大约 6-9 个 CPU 周期。近似方法只需要一次无符号乘法和一次 LShR，通常消耗约 4 个 CPU 周期，使其明显更快。

结合 1 和 2，我们可以实现快速且精确的时间转换。
