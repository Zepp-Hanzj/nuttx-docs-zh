=========================
特定于架构的代码
================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 配置包括：

* 处理器架构特定文件。  这些是包含的文件
  在此文件中讨论的“arch/<arch-name>/”目录中。

* 芯片/SoC 特定文件。  每个处理器架构都嵌入
  芯片或片上系统 (SoC) 架构。  全芯片
  架构包括处理器架构加上芯片特定的架构
  中断逻辑、通用 I/O (GPIO) 逻辑以及专用、
  内部外设（如 UART、USB 等）。

  这些特定于芯片的文件包含在特定于芯片的文件中
  ``arch/<arch-name>/`` 目录中的子目录并被选择
  通过 CONFIG_ARCH_name 选择

* 主板特定文件。  为了可用，芯片必须是
  包含在董事会环境中。  板配置定义
  板的附加属性，包括外围设备等
  LED、外围设备（如网络、USB 等）。

  这些特定于板的配置文件可以在
  ``boards/<arch>/<chip>/<board>`` sub-directories.

该文件将解决处理器架构特定的文件
包含在``arch/<arch-name>/`` 目录中。  该文件
include/nuttx/arch.h 标识了必须提供的所有 API
这个架构特定的逻辑。  （其中还包括
``arch/<arch-name>/arch.h`` 如下所述）。

``arch/`` 中的目录结构
================

“arch/” 目录包含特定于体系结构的逻辑。  完整的
板端口由架构特定的代码定义
目录以及“boards/”中特定于板的配置
目录。  每个架构必须提供一个子目录 <arch-name>
在“arch/”下，具有以下特征::

        <架构名称>/
        |-- 包括/
        |   |--<芯片名称>/
        |   |  `--（芯片特定的头文件）
        |   |--<其他芯片>/
        |   |-- arch.h
        |   |-- irq.h
        |   |-- 系统调用.h
        |   `-- 类型.h
        `--src/
            |--<芯片名称>/
            |  `--（芯片特定源文件）
            |--<其他芯片>/
            |-- 生成文件
            `--（特定于体系结构的源文件）

文件摘要
====

``include/<chip-name>/``

  该子目录包含芯片特定的头文件。

``include/arch.h``

  这是任何架构特定定义的挂钩，可能是
  系统需要的。  它包含在“include/nuttx/arch.h”中

``include/types.h``

  这为标准提供了特定于架构/工具链的定义
  类型。  该文件应键入：``_int8_t``，``_uint8_t``，``_int16_t``，
  ``_uint16_t``, ``_int32_t``, ``_uint32_t``

  如果架构支持 64 位整数：``_int24_t``、``_uint24_t``、
  ``_int64_t``, ``_uint64_t``

  请注意，这些类型名称有一个前导下划线字符。  这
  文件将被“include/stdint.h”和 typedef 包含（间接）
  到不带下划线字符的最终名称。  这个环岛
  这样做的方式允许将 stdint.h 从
  如果用户更喜欢使用“include/”目录
  由其工具链头文件提供的定义。

``irqstate_t``

  必须定义为保持中断所需的大小
  启用/禁用状态。

  该文件将被包含在“include/sys/types.h”中并被制作
  可用于所有文件。

``include/irq.h``

  该文件需要定义一些特定于架构的函数
  （如果编译器支持内联，通常是内联）和结构。
  这些包括：

``struct xcptcontext``

  该结构代表保存的线程上下文。

``irqstate_t up_irq_save(void)``

  用于禁用所有中断。

``void up_irq_restore(irqstate_t flags)``

  用于将中断使能恢复到与之前“up_irq_save”相同的状态
  被称为。

  注意：这些接口不可用于应用程序代码，但可以
  只能在操作系统代码中使用。  而且，一般来说，这些
  函数**永远**不应该直接调用，除非你知道
  你所做的绝对好。  相反，你通常应该使用
  包装函数``enter_ritic_section()`` 和
  ``leave_critical_section()`` as prototyped in ``include/nuttx/irq.h``.

  该文件还必须定义 NR_IRQS，即支持的 IRQ 总数
  由董事会。

-``include/syscall.h``：这个文件需要定义一些
   架构特定的函数（通常是内联的，如果编译器
   支持内联）以支持软件中断或
   *系统调用*\ 可以在用户模式应用程序中使用
   进入内核模式 NuttX 函数。该文件必须始终是
   提供以防止编译错误。然而，它只需要
   如果架构包含有效的函数声明
   supports the ``CONFIG_BUILD_PROTECTED`` or
   ``CONFIG_BUILD_KERNEL``\ 配置。

   有关详细信息，请参阅:doc:`/components/syscall`。

``src/<chip-name>/``

  该子目录包含芯片特定的源文件。

``src/Makefile``

  该 makefile 将被执行来构建目标 src/libup.a 和
  src/up_head.o。  up_head.o 文件保存了入口点
  系统（例如，上电复位入口点）。  它将用于
  最终链接libup.a和其他系统档案来生成
  最终可执行文件。

支持的架构
=====

支持的架构列表可以在：ref:`支持的平台 <platforms>` 中找到。
