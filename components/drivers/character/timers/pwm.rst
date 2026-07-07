============
PWM 驱动程序
============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

就本驱动程序而言，PWM 设备是任何生成受控频率和脉冲宽度的周期性输出脉冲的设备。此类设备可用于执行脉冲宽度调制输出或频率/脉冲计数调制输出（例如控制步进电机）。

NuttX PWM 驱动程序分为两部分：

#. "上半部分"，通用驱动程序，为应用程序代码提供通用 PWM 接口，
#. "下半部分"，平台特定的驱动程序，实现底层定时器控制以实现 PWM 功能。

支持 PWM 的文件可以在以下位置找到：

-  **接口定义**。NuttX PWM 驱动程序的头文件位于 ``include/nuttx/timers/pwm.h``。此头文件包含 PWM 驱动程序的应用程序级别接口以及"上半部分"和"下半部分"驱动程序之间的接口。PWM 模块使用标准字符驱动程序框架。但是，由于 PWM 驱动程序是设备控制接口而不是数据传输接口，应用程序可用的大部分功能通过驱动程序 ioctl 调用实现。
-  **"上半部分"驱动程序**。通用的"上半部分" PWM 驱动程序位于 ``drivers/timers/pwm.c``。
-  **"下半部分"驱动程序**。平台特定的 PWM 驱动程序位于 ``arch/<architecture>/src/<hardware>`` 目录，针对特定处理器 ``<architecture>`` 和特定 ``<chip>`` PWM 外设设备。

应用程序级别接口
===========================

要在应用程序中使用 PWM 驱动程序，首先需要包含 NuttX 定时器驱动程序的头文件。它包含 PWM 驱动程序的应用程序级别接口。为此，包含：

.. code-block:: c

  #include <nuttx/timers/pwm.h>

PWM 驱动程序注册为 ``/dev`` 命名空间中的 POSIX 字符设备文件。需要打开设备以获取文件描述符以进行后续操作。

PWM 仅通过 ``ioctl`` 接口访问，``read`` 和 ``write`` 函数没有任何效果。以下 ``ioctl`` 命令可用：

 * :c:macro:`PWMIOC_SETCHARACTERISTICS`
 * :c:macro:`PWMIOC_GETCHARACTERISTICS`
 * :c:macro:`PWMIOC_START`
 * :c:macro:`PWMIOC_STOP`

.. c:macro:: PWMIOC_SETCHARACTERISTICS

``PWMIOC_SETCHARACTERISTICS`` 命令设置 PWM 特性，如频率、占空比、死区时间等。这些特性通过 ``pwm_info_s`` 结构体设置。

.. c:struct:: pwm_info_s
.. code-block:: c

   struct pwm_info_s
   {
      /* 脉冲序列的频率 */
      uint32_t           frequency;
   #ifdef CONFIG_PWM_MULTICHAN
      /* 每通道输出状态 */
      struct pwm_chan_s  channels[CONFIG_PWM_NCHANNELS];
   #else
      /* 脉冲序列的占空比，"1"到"0"持续时间。
       * 最大值：65535/65536 (0x0000ffff)
       * 最小值：    1/65536 (0x00000001)
       */
      ub16_t             duty;
   #ifdef CONFIG_PWM_DEADTIME
      /* 主输出的死区时间值 */
      ub16_t             dead_time_a;
      /* 互补输出的死区时间值 */
      ub16_t             dead_time_b;
   #endif
   #ifdef CONFIG_PWM_PULSECOUNT
      /* 要生成的脉冲数量。0 表示生成无限数量的脉冲 */
      uint32_t           count;
   #endif
      /* 通道极性 */
      uint8_t            cpol;
      /* 禁用通道极性 */
      uint8_t            dcpol;
   #endif /* CONFIG_PWM_MULTICHAN */
      /* 用户提供的参数，用于下半部分 */
      FAR void           *arg;
   };

如果使用多通道（设置了 ``CONFIG_PWM_MULTICHAN``），结构体 ``pwm_chan_s`` 保存一个 PWM 通道的表示。

.. c:struct:: pwm_chan_s
.. code-block:: c

   struct pwm_chan_s
   {
      /* 脉冲序列的占空比，"1"到"0"持续时间。
       * 最大值：65535/65536 (0x0000ffff)
       * 最小值：    1/65536 (0x00000001)
       */
      ub16_t duty;
   #ifdef CONFIG_PWM_OVERWRITE
      /* 通道覆写 */
      bool ch_outp_ovrwr;
      /* 通道覆写值 */
      bool ch_outp_ovrwr_val;
   #endif
   #ifdef CONFIG_PWM_DEADTIME
      /* 主输出的死区时间值 */
      ub16_t dead_time_a;
      /* 互补输出的死区时间值 */
      ub16_t dead_time_b;
   #endif
      /* 通道极性 */
      uint8_t cpol;
      /* 禁用通道极性 */
      uint8_t dcpol;
      /* 通道号 */
      int8_t channel;
   };

除了占空比和频率之外，``ioctl`` 命令还允许设置许多其他 PWM 特性。这些功能可能并非所有 PWM 控制器都支持，用户在这种情况下应始终参考目标文档。

如果设置了 ``CONFIG_PWM_OVERWRITE`` 且 ``ch_outp_ovrwr`` 为 true，则可以使用 ``ch_outp_ovrwr_val`` 中设置的值覆写通道输出。配置选项 ``CONFIG_PWM_DEADTIME`` 和字段 ``dead_time_a`` 和 ``dead_time_b`` 提供了在互补输出之间设置死区时间的选项。这指示驱动程序自动为互补 PWM 输出插入输出激活延迟，例如用于 H 桥电机控制。

用户还可以设置默认通道极性 ``cpol`` 和禁用通道极性 ``dcpol``。如果设置为零，则使用默认控制器值（或配置中确定的值）。以下定义可用于设置极性：

.. code-block:: c

   /* 未定义，默认输出状态取决于架构 */
   #define PWM_CPOL_NDEF             0
   /* 逻辑零 */
   #define PWM_CPOL_LOW              1
   /* 逻辑一 */
   #define PWM_CPOL_HIGH             2

   /* 未定义，默认输出状态取决于架构 */
   #define PWM_DCPOL_NDEF            0
    /* 逻辑零 */
   #define PWM_DCPOL_LOW             1
    /* 逻辑一 */
   #define PWM_DCPOL_HIGH            2

.. c:macro:: PWMIOC_GETCHARACTERISTICS

命令 ``PWMIOC_GETCHARACTERISTICS`` 的工作方式与 ``PWMIOC_SETCHARACTERISTICS`` 相同，但它获取当前设置的值而不是设置它们。

.. c:macro:: PWMIOC_START

``PWMIOC_START`` 命令启动脉冲输出。在此操作之前应设置 PWM 通道的特性。

.. c:macro:: PWMIOC_STOPS

``PWMIOC_STOPS`` 命令停止脉冲输出。

.. c:macro:: PWMIOC_FAULTS_FETCH_AND_CLEAR

``PWMIOC_FAULTS_FETCH_AND_CLEAR`` 命令清除故障输入。某些故障可以被锁存（即使源不再活动仍保持活动状态），必须从软件中清除。这提供了从应用程序清除故障并重新启用 PWM 输出的选项。它也可用于获取当前故障。

该调用接受指向 ``unsigned long`` 变量的指针作为参数，一个位掩码定义要清除哪些故障。驱动程序清除这些故障并用清除前的活动故障填充参数。参数变量等于零将不会清除任何故障，但用户将获得当前活动的故障。如果传递 NULL 作为参数，则清除所有当前设置的故障且不执行获取。

这可能并非所有驱动程序都支持。

应用示例
~~~~~~~~~~~~~~~~~~~

示例应用程序可以在 ``nuttx-apps`` 仓库的 ``examples/pwm`` 路径下找到。

.. code-block :: bash

   nsh> pwm

配置
=============

本节描述 ``Kconfig`` 中的常见 PWM 配置。读者应参考目标文档以获取目标特定配置。

PWM 由 ``CONFIG_PWM`` 配置选项启用。选项 ``CONFIG_PWM_MULTICHAN`` 选择对一个 PWM 实例的多通道支持。如果使用多通道，配置选项 ``CONFIG_PWM_NCHANNELS`` 定义每个实例的最大通道数。每个定时器/控制器可能支持比此值更少的输出通道。

引脚覆写生成由 ``CONFIG_PWM_OVERWRITE`` 选项启用。这支持在不需要等待周期结束的情况下生成 0 或 1 的引脚覆写。

``CONFIG_PWM_DEADTIME`` 选项提供了在互补 PWM 输出之间引入死区时间值的可能性。
