=====================
System Time and Clock
=====================

基本系统定时器
==================

**系统定时器** 在大多数实现中，系统时间由定时器中断提供。
该定时器中断的运行频率由 ``CONFIG_USEC_PER_TICK`` 决定（默认为 10000 微秒，即 100Hz。
如果选择了 ``CONFIG_SCHED_TICKLESS``，则默认为 100 微秒）。
定时器每 ``CONFIG_USEC_PER_TICK`` 微秒产生一次中断，并递增名为 ``g_system_ticks`` 的计数器。
``g_system_ticks`` 为计算 *运行时间（up-time）* 和以 ``CONFIG_USEC_PER_TICK`` 为单位的
已用时间间隔提供时间基准。``g_system_ticks`` 的范围默认为 32 位。
但如果 MCU 支持 ``long long`` 类型且选择了 ``CONFIG_SYSTEM_TIME16``，
则将改为支持 64 位系统定时器。

**系统定时器精度** 在许多系统上，由于频率或分频器的限制，
无法实现 ``CONFIG_USEC_PER_TICK`` 所指定的精确时间间隔。
因此，``CONFIG_USEC_PER_TICK`` 指定的时间间隔可能只是近似值，
实际 *运行时间* 可能存在小误差。然而，这些小误差会随时间累积，
经过较长时间后，MCU 实际 *运行时间* 的误差可能会大到不可接受的程度。

如果硬件产生的定时器滴答周期不是精确的 ``CONFIG_USEC_PER_TICK``，
*并且* 你要求 MCU 的运行时间精确，那么你可以采取以下措施：

-  也许你可以将 ``CONFIG_USEC_PER_TICK`` 调整到不同的值，
   以便能精确实现该值。
-  或者你可以使用一种称为 *Delta-Sigma 调制* 的技术。
   （由 Uros Platise 建议）。参见以下示例。

**Delta-Sigma 调制示例**。考虑以下场景：系统定时器是一个以 32.768KHz 驱动的
向上计数定时器。可以使用分频器，但分频因子为一时精度最高。
该计数器向上计数，直到计数值等于匹配值，然后产生定时器中断。
目标频率为 100Hz（``CONFIG_USEC_PER_TICK`` 为 10000）。

在这种情况下无法获得精确的 100Hz 频率。为了获得该精确频率，
需要提供 327.68 的匹配值。最接近的整数值是 328，但理想匹配值介于 327 和 328 之间。
最接近的值 328 将产生 99.9Hz 的实际定时器频率！这在某些用法中可能导致显著的定时误差。

使用 Delta-Sigma 调制可以从长期上消除这种误差。考虑以下示例实现：

  #. 初始时累加器为零，匹配值设置为 328：

     .. code-block:: c

      accumulator = 0;
      match = 328;

  #. 每次定时器中断时，累加器根据当前间隔的误差更新，在本例中为误差的 100 倍。
     因此在第一次定时器中断时，累加器更新如下：

     .. code-block:: c

        if (match == 328)
          {
            accumulator += 32; // 100*(328 - 327.68)
          }
        else
          {
            accumulator -= 68; // (100*(327 - 327.68)
          }

  #. 在同一次定时器中断中，设置新的匹配值：

     .. code-block:: c

      if (accumulator < 0)
        {
          match = 328;
        }
      else
        {
          match = 327;
        }

通过这种方式，定时器间隔从一次中断到下一次中断进行控制，
从而产生精确的 100Hz 平均频率。

硬件
========

要启用硬件模块，请使用以下配置选项：

``CONFIG_RTC``
   启用对硬件 RTC 的通用支持。特定架构可能需要其他特定设置。
``CONFIG_RTC_EXTERNAL``
   大多数 MCU 在芯片内部集成了 RTC 硬件。其他 RTC，
   即 *外部* RTC，可能作为独立芯片提供，通常通过 SPI 或 I2C
   等串行接口与 MCU 连接。这些外部 RTC 与内置 RTC 的区别在于，
   它们要等到操作系统完全启动并能支持所需串行通信后才能初始化。
   ``CONFIG_RTC_EXTERNAL`` 将配置操作系统，使其延迟时间设施的初始化。
``CONFIG_RTC_DATETIME``
   RTC 有两种常见类型：(1) 简单的电池供电计数器，在断电时保持时间；
   (2) 完整的日期/时间 RTC，提供日期和时间信息（通常为 BCD 格式）。
   如果选择了 ``CONFIG_RTC_DATETIME``，则表示使用第二种 RTC。
   在这种情况下，RTC 用于"初始化"普通的 NuttX 定时器，
   而 NuttX 系统定时器提供更高分辨率的时间。
``CONFIG_RTC_HIRES``
   如果未选择 ``CONFIG_RTC_DATETIME``，则使用简单的电池供电计数器。
   这种简单计数器有两种不同的实现，基于计数器的时间分辨率：
   典型 RTC 的时间分辨率为 1 秒，通常支持 32 位 ``time_t`` 值。
   在这种情况下，RTC 用于"初始化"普通的 NuttX 定时器，
   而 NuttX 定时器提供更高分辨率的时间。
   如果在 NuttX 配置中启用了 ``CONFIG_RTC_HIRES``，
   则 RTC 提供更高分辨率的时间，并完全替代系统定时器用于日期和时间。
``CONFIG_RTC_FREQUENCY``
   如果定义了 ``CONFIG_RTC_HIRES``，则必须提供高分辨率 RTC 的频率。
   如果未定义 ``CONFIG_RTC_HIRES``，则 ``CONFIG_RTC_FREQUENCY`` 默认为一。
``CONFIG_RTC_ALARM``
   如果 RTC 硬件支持闹钟设置，则启用此选项。当闹钟触发时将执行回调函数。

这需要以下基本函数来读取和设置时间：

-  ``up_rtc_initialize()``。根据所选配置初始化内置的 MCU 硬件 RTC。
   此函数在 OS 初始化序列的早期调用一次。注意，依赖于 OS 资源（如 SPI 或 I2C）
   可用性的外部 RTC 硬件初始化必须延迟到系统完全启动后。在这种情况下，
   使用其他 RTC 特定的初始化函数。
-  ``up_rtc_time()``。以秒为单位获取当前时间。这类似于标准的 ``time()`` 函数。
   此接口仅在选择低分辨率 RTC/计数器硬件实现时需要。仅在设置了 ``CONFIG_RTC``
   但未设置 ``CONFIG_RTC_HIRES`` 和 ``CONFIG_RTC_DATETIME`` 时，
   RTOS 在初始化期间使用它来设置系统时间。
-  ``up_rtc_gettime()``。从高分辨率 RTC 时钟/计数器获取当前时间。
   此接口仅由高分辨率 RTC/计数器硬件实现支持。
   它用于替代系统定时器（``g_system_ticks``）。
-  ``up_rtc_settime()``。将 RTC 设置为提供的时间。所有 RTC 实现都必须能够
   根据标准 timespec 设置时间。

系统滴答与时间
====================

系统滴答由 ``g_system_ticks`` 表示。

以系统基本定时器的速率运行，用于时间片调度等。

如果存在硬件 RTC（``CONFIG_RTC``）且启用了高分辨率定时（``CONFIG_RTC_HIRES``），
则初始化成功后，变量会被对 ``up_rtc_gettime()`` 的调用覆盖，
即使在断电模式下也会持续运行。

在设置了 ``CONFIG_RTC_HIRES`` 的情况下，``g_system_ticks`` 以系统定时器的速率
持续计数，但该定时器在断电模式下会被禁用。通过比较此时间和 RTC（实际时间），
可以确定实际的系统活跃时间。要获取该变量请使用：

无滴答操作系统
===========

**默认系统定时器**。默认情况下，NuttX 配置使用周期性定时器中断来驱动所有系统定时。
定时器由架构特定代码提供，该代码以 ``CONFIG_USEC_PER_TICK`` 控制的速率调用 NuttX。
``CONFIG_USEC_PER_TICK`` 的默认值为 10000 微秒，对应于 100 Hz 的定时器中断频率。

每次定时器中断时，NuttX 执行以下操作：

-  递增计数器。该计数器即系统时间，分辨率为 ``CONFIG_USEC_PER_TICK`` 微秒。
-  检查是否到了对选择轮询调度的任务执行时间片操作的时间。
-  检查定时事件是否过期。

这种默认系统定时器有什么问题？其实没有。它可靠且仅占用很小一部分 CPU 带宽。
但我们可以做得更好。默认系统定时器的一些局限性，按重要性递增排列如下：

-  **开销**：虽然 100Hz 系统定时器中断的 CPU 使用率确实很低，但大部分仍是
   浪费的处理时间。在大多数定时器中断中，除了递增计数器外没有其他需要做的事情。
-  **分辨率**：所有系统定时的分辨率也由 ``CONFIG_USEC_PER_TICK`` 决定。
   因此默认情况下无法以优于 10 毫秒的分辨率计时。要提高此分辨率，
   可以减小 ``CONFIG_USEC_PER_TICK``。但这样系统定时器中断将占用更多
   CPU 带宽来处理无用中断。
-  **功耗**：但最大的问题是功耗。当系统空闲时，它进入轻量低功耗模式
   （对于 ARM，通过 ``wfi`` 或 ``wfe`` 指令进入此模式）。
   但每次中断都会将系统从低功耗模式唤醒。因此，更高的中断频率会导致更大的功耗。

**无滴答操作系统**。所谓的 *无滴答操作系统* 为这个问题提供了一种解决方案。
其基本概念是消除周期性定时器中断，代之以单次触发的区间定时器。
它变为事件驱动而非轮询：默认系统定时器是轮询设计。每次中断时，
NuttX 逻辑检查是否需要做任何事情，如果有则执行。

使用区间定时器，可以预知下一个有意义的 OS 事件何时发生，
设置区间定时器并等待其触发。当区间定时器触发时，执行预定的活动。

无滴答平台支持
-------------------------

要使用无滴答操作系统，必须从平台特定代码中提供特殊支持。
与默认系统定时器一样，平台特定代码必须提供定时器资源以支持 OS 行为。
目前这些定时器资源仅在少数平台上提供。仿真的示例实现位于
``nuttx/arch/sim/src/up_tickless.c``。Atmel SAMA5 的另一个示例位于
``nuttx/arch/arm/src/sama5/sam_tickless.c``。以下段落将说明如何为任何平台提供无滴答 OS 支持。

无滴答配置选项
------------------------------

-  ``CONFIG_ARCH_HAVE_TICKLESS``：如果平台提供 *无滴答 OS* 支持，
   则应在架构的 ``Kconfig`` 文件中选择此设置。以下是仿真平台中
   ``arch/Kconfig`` 文件中的选择方式：

   .. code-block:: console

     config ARCH_SIM
        bool "Simulation"
        select ARCH_HAVE_TICKLESS
        ---help---
                Linux/Cygwin user-mode simulation.

   当选择仿真平台时，``ARCH_HAVE_TICKLESS`` 会自动选择，
   通知配置系统可以选择 *无滴答 OS* 选项。

-  ``CONFIG_SCHED_TICKLESS``：如果选择了 ``CONFIG_ARCH_HAVE_TICKLESS``，
   则可以使用此选项在 NuttX 中启用 *无滴答 OS* 功能。

-  ``CONFIG_SCHED_TICKLESS_ALARM``：无滴答选项可以通过简单的区间定时器
   （加上已用时间）或闹钟来支持。区间定时器允许在一段时间后触发事件。
   通过闹钟，可以设置未来的时间点，当闹钟触发时获得事件。
   此选项选择使用闹钟。

   闹钟的优点是避免了一些小的定时误差；区间定时器的优点是硬件要求可能更简单。

-  ``CONFIG_USEC_PER_TICK``：此选项并非 *无滴答 OS* 独有，
   但在选择 *无滴答 OS* 时其含义发生变化。在默认配置中，
   系统时间由周期性定时器中断提供，默认系统定时器配置为 100Hz，
   即 ``CONFIG_USEC_PER_TICK=10000``。如果选择了 ``CONFIG_SCHED_TICKLESS``，
   则没有系统定时器中断。在这种情况下，``CONFIG_USEC_PER_TICK`` 不控制任何定时器速率。
   它仅决定 ``clock_systime_ticks()`` 报告的时间分辨率，
   以及可为某些延迟（包括看门狗定时器和延迟工作）设置的时间分辨率。

   在这种情况下仍然存在权衡：``CONFIG_USEC_PER_TICK`` 越低越好，
   以获得更高的定时分辨率。但是，时间当前以 ``unsigned int`` 存储。
   在某些系统上可能是 16 位宽，但在大多数当代系统上是 32 位。
   无论哪种情况，较小的 ``CONFIG_USEC_PER_TICK`` 值都会减少
   可表示延迟的范围。因此权衡在于范围和分辨率之间
   （如果你确实需要两者，也可以修改代码使用 64 位值）。

   默认的 100 微秒可提供最长 120 小时的延迟范围。

   此值不应小于底层定时器的分辨率，否则可能产生错误。

无滴答导入接口
----------------------------

平台特定代码必须提供的接口在 ``include/nuttx/arch.h`` 中定义，
以下列出并在后续段落中概述：

  - ``<arch>_timer_initialize()`` 初始化定时器设施。在初始化序列早期
    由 ``up_initialize()`` 调用。
  - ``up_timer_gettime()``：从平台特定时间源返回当前时间。

无滴答选项可以通过简单的区间定时器（加上已用时间）或闹钟来支持。
区间定时器允许在一段时间后触发事件。通过闹钟，可以设置未来的时间点，
当闹钟触发时获得事件。

如果定义了 ``CONFIG_SCHED_TICKLESS_ALARM``，则平台代码必须提供以下内容：

-  ``up_alarm_cancel()``：取消闹钟。
-  ``up_alarm_start()``：启用（或重新启用）闹钟。

如果 *未* 定义 ``CONFIG_SCHED_TICKLESS_ALARM``，则平台代码必须提供以下类似函数：

-  ``up_timer_cancel()``：取消区间定时器。
-  ``up_timer_start()``：启动（或重新启动）区间定时器。

注意，平台特定实现可能需要两个硬件定时器：(1) 满足 ``up_timer_start()``
和 ``up_timer_cancel()`` 要求的区间定时器，以及 (2) 处理 ``up_timer_gettime()``
要求的计数器。理想情况下，两个定时器都以 ``CONFIG_USEC_PER_TICK``
决定的速率运行（且绝对不能慢于该速率）。

由于定时器是有限的资源，在某些系统上使用两个定时器可能存在问题。
如果单个定时器始终保持自由运行模式，则可以用单个定时器完成工作。
一些定时器/计数器具有在定时器匹配比较值时产生比较中断的能力，
同时继续计数而不停止。如果你的硬件支持这样的计数器，
可以使用 ``CONFIG_SCHED_TICKLESS_ALARM`` 选项，只需将比较计数设置为
自由运行定时器的值 *加上* 所需延迟。这样你就可以用一个定时器实现两者：
闹钟和自由运行计数器！

除了这些导入接口外，RTOS 还将导出以下接口供平台特定区间定时器实现使用：

- ``nxsched_process_timer()``：在区间定时器到期时由平台特定逻辑调用。

.. c:function:: void archname_timer_initialize(void)

  初始化所有平台特定定时器设施。此函数在初始化序列早期由 up_initialize() 调用。
  返回时，当前运行时间应可从 up_timer_gettime() 获取，区间定时器已准备好使用
  （但未在积极计时）。命名取决于架构，例如对于 STM32，``archname`` 将是 ``stm32``。

  :return: 成功返回零（OK）；失败返回负的 errno 值。

  **假设**：在初始化序列早期调用，此时不需要特殊的并发保护。

.. c:function:: int up_timer_gettime(FAR struct timespec *ts)

  返回自上电以来（更准确地说，自 ``<arch>`` ``_timer_initialize()``
  被调用以来）的已用时间。此函数在功能上等同于时钟 ID 为 ``CLOCK_MONOTONIC``
  的 ``clock_gettime()``。此函数为报告当前时间提供基础，
  也用于消除区间时间计算中微小误差的累积。

  :param ts: 提供返回运行时间的位置。

  :return: 成功返回零（OK）；失败返回负的 errno 值。

  **假设**：从正常任务上下文调用。实现必须提供正确操作所需的互斥机制，
  这可以包括禁用中断以确保原子寄存器操作。

.. c:function:: int up_alarm_cancel(FAR struct timespec *ts)

  取消闹钟并返回取消闹钟的时间。这两个步骤需要尽可能原子地完成。
  除非通过 ``up_alarm_start()`` 重新启动闹钟，否则不会调用
  ``nxsched_process_timer()``。如果作为竞争条件，调用此函数时闹钟已过期，
  则返回的是当前时间。

  :param ts: 返回过期时间的位置。如果定时器未激活，应返回当前时间。
    ``ts`` 可以为 ``NULL``，此时不返回时间。

  :return: 成功返回零（OK）；失败返回负的 errno 值。

  **假设**：可从中断级处理或正常任务级调用。内部可能需要禁用中断以确保不可重入性。

.. c:function:: int up_alarm_start(FAR const struct timespec *ts)

  启动闹钟。当闹钟触发时（除非调用 ``up_alarm_cancel`` 停止它），
  将调用 ``nxsched_process_timer()``。

  :param ts: 闹钟预期触发的未来时间。当闹钟触发时，定时器逻辑将调用
    ``nxsched_process_timer()``。

  :return: 成功返回零（OK）；失败返回负的 errno 值。

  **假设**：可从中断级处理或正常任务级调用。内部可能需要禁用中断以确保不可重入性。

.. c:function:: int up_timer_cancel(FAR struct timespec *ts)

  取消区间定时器并返回定时器上的剩余时间。这两个步骤需要尽可能原子地完成。
  除非通过 ``up_timer_start()`` 重新启动定时器，否则不会调用
  ``nxsched_process_timer()``。如果作为竞争条件，调用此函数时定时器已过期，
  则必须清除待处理的中断，以避免虚假调用 ``nxsched_process_timer()``，
  并返回零剩余时间。

  :param ts: 返回剩余时间的位置。如果定时器未激活，应返回零。

  :return: 成功返回零（OK）；失败返回负的 errno 值。

  **假设**：可从中断级处理或正常任务级调用。内部可能需要禁用中断以确保不可重入性。

.. c:function:: int up_timer_start(FAR const struct timespec *ts)

  启动区间定时器。在超时完成时（除非调用 ``up_timer_cancel()``
  停止计时）将调用 ``nxsched_process_timer()``。

  :param ts: 提供直到 ``nxsched_process_timer()`` 被调用的时间间隔。

  :return: 成功返回零（OK）；失败返回负的 errno 值。

  **假设**：可从中断级处理或正常任务级调用。内部可能需要禁用中断以确保不可重入性。

看门狗定时器接口
=========================

NuttX 提供通用的看门狗定时器设施。此设施允许 NuttX 用户指定一个看门狗定时器函数，
该函数将在指定的延迟后以滴答级分辨率运行。看门狗定时器函数将在定时器中断处理程序的
上下文中运行。因此，看门狗定时器函数只能使用有限的 NuttX 接口。
但看门狗定时器函数可以使用 ``mq_send()``、``sigqueue()`` 或 ``kill()``
与 NuttX 任务通信。

- :c:func:`wd_start`
- :c:func:`wd_start_next`
- :c:func:`wd_restart`
- :c:func:`wd_restart_next`
- :c:func:`wd_cancel`
- :c:func:`wd_gettime`
- 看门狗定时器回调

.. c:function:: int wd_start(FAR struct wdog_s *wdog, clock_t delay, \
                 wdentry_t wdentry, wdparm_t arg)

  此函数将看门狗添加到定时器队列中。指定的看门狗函数将在指定的滴答数过后
  从中断级调用。看门狗定时器可以从中断级启动。

  看门狗在定时器中断处理程序的上下文中执行。

  看门狗定时器仅执行一次。

  要替换超时延迟或要执行的函数，请使用相同的 wdog 再次调用 wd_start；
  对给定看门狗 ID，只有最近的 wd_start() 才有效。

  :param wdog: 看门狗 ID
  :param delay: 以时钟滴答为单位的延迟计数
  :param wdentry: 超时时调用的函数
  :param arg: 传递给 wdentry 的参数。

  **注意**：参数必须为 ``wdparm_t`` 类型。

  :return: 成功返回零（``OK``）；失败返回负的 ``errno`` 值以指示错误性质。

  **假设/限制：** 看门狗例程在定时器中断处理程序的上下文中运行，
  并受所有 ISR 限制。

  **POSIX 兼容性：** 这是一个非 POSIX 接口。VxWorks 提供以下可比较的接口：

  .. code-block:: c

    STATUS wdStart (WDOG_ID wdog, int delay, FUNCPTR wdentry, int parameter);

  与 VxWorks 接口的区别包括：

  -  当前实现支持传递给 wdentry 的多个参数；VxWorks 仅支持单个参数。最大参数数量由以下决定

.. c:function:: int wd_start_next(FAR struct wdog_s *wdog, clock_t delay, \
                 wdentry_t wdentry, wdparm_t arg)

   此函数基于上次到期时间重新启动看门狗定时器。它可用于实现周期性看门狗定时器。
   例如，在看门狗回调中调用此函数（而非 wd_start）以重新启动下一个定时器，
   从而获得更好的定时精度。
   注意，在看门狗回调之外调用此函数需要设置 wdog->expired。

  :param wdog: 看门狗 ID
  :param delay: 以时钟滴答为单位的延迟计数
  :param wdentry: 超时时调用的函数
  :param arg: 传递给 wdentry 的参数。

  **注意**：参数必须为 ``wdparm_t`` 类型。

  :return: 成功返回零（``OK``）；失败返回负的 ``errno`` 值以指示错误性质。

  **假设/限制：** 看门狗例程在定时器中断处理程序的上下文中运行，并受所有 ISR 限制。

.. c:function:: int wd_cancel(FAR struct wdog_s *wdog)

  此函数取消当前正在运行的看门狗定时器。看门狗定时器可以从中断级取消。

  :param wdog: 要取消的看门狗 ID。

  :return: ``OK`` 或 ``ERROR``

  **POSIX 兼容性：** 这是一个非 POSIX 接口。VxWorks 提供以下可比较的接口：

  .. code-block:: c

    STATUS wdCancel (WDOG_ID wdog);

.. c:function:: int wd_gettime(FAR struct wdog_s *wdog)

  返回指定看门狗到期前的剩余时间。

  :param wdog: 标识请求所针对的看门狗。

  :return: 看门狗定时器到期前的剩余时间（以系统滴答为单位）。
    零表示 wdog 无效或 wdog 已过期。

.. c:type:: void (*wdentry_t)(wdparm_t arg)

  **看门狗定时器回调**：当看门狗到期时，将调用此类型的回调函数。

  参数以标量 ``wdparm_t`` 值传递。对于 ``sizeof(pointer) < sizeof(uint32_t)`` 的系统，
  以下联合体定义了指针在 ``uint32_t`` 中的对齐方式。例如，SDCC MCS51 通用指针为 24 位，
  但 ``uint32_t`` 为 32 位。

  根据定义，我们始终有 ``sizeof(pointer) <= sizeof(uintptr_t)``。

  .. code-block:: c

    union wdparm_u
    {
      FAR void     *pvarg; /* 通用指针的大小 */
      uint32_t      dwarg; /* 足够容纳 32 位值 */
      uintptr_t     uiarg; /* sizeof(uintptr_t) >= sizeof(pointer) */
    };

    #if UINTPTR_MAX >= UINT32_MAX
    typedef uintptr_t wdparm_t;
    #else
    typedef uint32_t  wdparm_t;
    #endif

高分辨率定时器接口
================================

硬实时应用（如电机控制）通常需要纳秒级的任务定时，而基于滴答的定时器（如 wdog）
无法提供。将滴答间隔减小到微秒或纳秒级是不切实际的，因为这会使 CPU 被中断淹没。

高分辨率定时器（HRTimer）是一种能够实现纳秒级定时分辨率的定时器抽象，
主要用于需要高分辨率时钟事件的场景。随着集成电路技术的进步，
现代高分辨率定时器硬件（如典型的 x86 HPET）已能满足亚纳秒级定时要求，
并提供飞秒级的抖动控制。

尽管 NuttX 内核中当前的硬件定时器抽象（`up_alarm/up_timer`）已支持纳秒级定时，
但其软件定时器抽象 wdog 及定时器超时中断处理流程仍停留在微秒级（滴答）分辨率，
无法满足高分辨率定时需求。

为此，NuttX 提供了高分辨率定时器（hrtimer），实现真正的纳秒级精度。
HRTimer 主要提供以下功能接口：

**以纳秒设置定时器**：配置软件定时器在指定的纳秒时间触发。

**取消定时器**：取消软件定时器。

**处理定时器超时**：在定时器事件触发后执行超时处理。

用户可以注册 hrtimer 回调，在指定延迟后执行。回调在定时器中断上下文中运行，
因此只能使用有限的 NuttX 接口（如 ``mq_send()``、``sigqueue()``、``nxevent_post()``
或 ``kill()``）与任务通信。

hrtimer 实现主要包括以下接口：

**hrtimer_start(timer, func, arg, delay)**：异步启动已完成或已被异步取消的
  定时器（其回调函数可能仍在执行）。

**hrtimer_cancel(timer)**：异步取消定时器。注意，此接口的语义与 Linux 的
  `try_to_cancel` 完全不同。它确保定时器一定能被成功取消，
  但可能需要等待其回调函数执行完毕。

**hrtimer_cancel_sync(timer)**：同步取消定时器。如果定时器的回调函数仍在执行，
  此函数将自旋等待直到回调完成。它确保用户始终可以获得定时器的所有权。

HRTimer 的状态机图如下：

.. code-block:: text

  +------------------------------------------------------+
  |                 HRTIMER 状态图                        |
  +------------------------------------------------------+
  |                                                      |
  |     +----------------------+                         |
  |     | HRTIMER_COMPLETED    |                         |
  |     |      (private)       |                         |
  |     +----------------------+                         |
  |                |                                     |
  |                | hrtimer_start                       |
  |                |                                     |
  |                |                                     |
  |                v                                     |
  |     +----------------------+                         |
  |     | HRTIMER_PENDING      |---------------------+   |
  | +-->|      (shared)        |<---+                |   |
  | |   +----------------------+    |                |   |
  | |            |                  |timer callback  |   |
  | |            |hrtimer_expiry    |return non-zero |   |
  | |            |                  |                |   |
  | |            v                  |                |   |
  | |   +----------------------+    |                |   |
  | |   | HRTIMER_RUNNING      |----+                |   |
  | |   |      (shared)        |                     |   |
  | |   +----------------------+                     |   |
  | |                    |                           |   |
  | |                    |                           |   |
  | |                    |timer return zero          |   |
  | |                    |or                         |   |
  | |                    |hrtimer_cancel             |   |
  | |                    |                           |   |
  | |                    v                           |   |
  | |               +----------------------+         |   |
  | |               | HRTIMER_CANCELED     |<--------+   |
  | +---------------|    (half_shared)     |             |
  | hrtimer_start   +----------------------+             |
  |                        |                             |
  |     hrtimer_cancel_sync|                             |
  |         wait all cores |                             |
  |                        v                             |
  |     +----------------------+                         |
  |     | HRTIMER_COMPLETED    |                         |
  |     |      (private)       |                         |
  |     +----------------------+                         |
  |             ^  |                                     |
  |             |  |                                     |
  |             +--+                                     |
  |            hrtimer_cancel                            |
  +------------------------------------------------------+

各状态的具体定义如下：

**HRTIMER_PENDING|shared**：`hrtimer->func != NULL`。即 hrtimer 已被插入 hrtimer 队列，
正在等待执行。

**HRTIMER_COMPLETED|private**：`hrtimer->func == NULL` ∧
`∀c ∈ [0, CONFIG_SMP_NCPUS), (g_hrtimer_running[c] & ~(1u)) != hrtimer`
即 hrtimer 不处于待处理状态，且没有核心正在执行 hrtimer 的回调函数。

**HRTIMER_RUNNING|shared**：`hrtimer->func == NULL` ∧
`∃c ∈ [0, CONFIG_SMP_NCPUS), g_hrtimer_running[c] == hrtimer`。
即 hrtimer 不处于待处理状态，且至少有一个核心正在执行 hrtimer 的回调函数。

**HRTIMER_CANCELED|half_shared**：`hrtimer->func == NULL` ∧
`∀c ∈ [0, CONFIG_SMP_NCPUS), g_hrtimer_running[c] != hrtimer`。
即 hrtimer 不处于待处理状态，所有核心都已失去对 hrtimer 的所有权——
意味着它们不能再读取或写入 hrtimer——但其回调函数可能仍在执行过程中。

- :c:func:`hrtimer_init`
- :c:func:`hrtimer_cancel`
- :c:func:`hrtimer_cancel_sync`
- :c:func:`hrtimer_start`
- :c:func:`hrtimer_gettime`
- 高分辨率定时器回调

.. c:function:: void hrtimer_init(FAR hrtimer_t *hrtimer, hrtentry_t func)

  此函数初始化高分辨率定时器实例。设置到期回调及其参数。此函数不会启动定时器。

  :param hrtimer: 指向 hrtimer 实例的指针
  :param func: 到期回调函数

  :return: 无。

  **POSIX 兼容性：** 这是一个非 POSIX 接口。

.. c:function:: int hrtimer_cancel(FAR hrtimer_t *hrtimer)

  异步取消高分辨率定时器。

  如果定时器已启动但尚未到期，它将从定时器队列中移除，回调不会被调用。

  如果定时器回调当前正在执行，此函数将标记定时器为已取消并立即返回。
  正在运行的回调允许完成，但不会再次被调用。

  函数完成后，调用者获得有限的所有权，允许重新启动定时器但不能释放。
  回调可能仍在另一个 CPU 上执行。请谨慎使用以避免并发问题。

  :param hrtimer: 要取消的定时器实例

  :return: 成功返回 ``OK``；失败返回负的 errno 值。

  **POSIX 兼容性：** 这是一个非 POSIX 接口。

.. c:function:: int hrtimer_cancel_sync(FAR hrtimer_t *hrtimer)

  同步取消高分辨率定时器并等待定时器变为非活动状态。

  此函数首先调用 hrtimer_cancel() 请求取消定时器。它将定时器设置为已取消状态，
  并等待所有引用被释放。调用者获得完整所有权，此函数返回后可以安全地释放定时器。

  此函数可能休眠，不能在中断上下文中调用。

  :param hrtimer: 要取消的定时器实例

  :return: 成功返回 ``OK``；失败返回负的 errno 值。

  **POSIX 兼容性：** 这是一个非 POSIX 接口。

.. c:function:: int hrtimer_start(FAR hrtimer_t *hrtimer, \
                                  hrtimer_entry_t func, \
                                  uint64_t expired, \
                                  enum hrtimer_mode_e mode)

  此函数以绝对或相对模式启动高分辨率定时器。

  :param hrtimer: 要取消的定时器实例
  :param func: 到期回调函数
  :param ns: 以纳秒为单位的定时器到期时间（绝对或相对）
  :param mode: HRTIMER_MODE_ABS 或 HRTIMER_MODE_REL

  :return: 成功返回 ``OK``；失败返回负的 errno 值。

  **POSIX 兼容性：** 这是一个非 POSIX 接口。

.. c:function:: uint64_t hrtimer_gettime(FAR hrtimer_t *timer)

  获取定时器到期前的剩余时间。

  :param timer: 要查询的定时器实例

  :return: 下次到期前的剩余时间（以纳秒为单位）。

  **假设：**
    - timer 不为 NULL。

  **POSIX 兼容性：** 这是一个非 POSIX 接口。

.. c:type:: uint64_t (*hrtimer_entry_t)(FAR hrtimer_t *hrtimer, \
                                        uint64_t expired)

  **高分辨率定时器回调**：当 hrtimer 到期时，将调用此类型的回调函数。

  :param timer: 传递给回调函数的 hrtimer 指针，执行回调函数时不要修改 hrtimer。
  :param expired: 定时器到期的时间（以纳秒为单位）

  :return: 下次到期前的延迟（以纳秒为单位）。
