======================
在 Renode 上运行 NuttX
======================

Renode (https://renode.io/) 是一个专用于复杂嵌入式系统的开源虚拟开发框架。

本页包含在 Renode 上运行某些 NuttX 板的说明。

stm32f4discovery
================

Renode 不支持 CCM 内存，因此我们必须使用 ``CONFIG_MM_REGIONS=1`` 来禁用它。

Renode 脚本::

  using sysbus
  $name?="STM32F4_Discovery"
  mach create $name
  machine LoadPlatformDescription @platforms/boards/stm32f4_discovery-kit.repl

  cpu PerformanceInMips 125

  $bin?=@nuttx

  showAnalyzer sysbus.usart2

  macro reset
  """
    sysbus LoadELF $bin
  """

  runMacro $reset


已使用 ``stm32f4discovery/nsh`` 测试。

nucleo-l073rz
=============

无法工作。NuttX 中没有针对 ``Cotex-M0`` 的 BASEPRI 实现。

nrf52840-dk
===========

默认情况下，Renode 使用启用了 EasyDMA 的 UART (UARTE)，NuttX 尚不支持。我们可以通过创建基于 Renode 默认实现的自定义机器描述来解决此问题::

  using "platforms/cpus/nrf52840.repl"

  uart0:
    easyDMA: false

Renode 脚本::

  using sysbus

  mach create
  machine LoadPlatformDescription @nrf52840_custom.repl

  $bin?=@nuttx

  showAnalyzer uart0

  macro reset
  """
    sysbus LoadELF $bin
  """

  runMacro $reset

已使用 ``nrf52840-dk/nsh`` 测试。

已知问题：

* ``QSPI`` 在 Renode 中未实现，

* ``PWM`` 无法工作，Renode 中缺少 ``NRF52_PWM_EVENTS_SEQSTARTED0_OFFSET`` 实现，

* ``ADC`` 无法工作，Renode 中缺少 ``NRF52_SAADC_EVENTS_CALDONE_OFFSET`` 实现，

* ``SoftDevice`` 无法工作，在 ``mpsl_init()`` 中崩溃

stm32f746g-disco
================

必须设置 ``CONFIG_ARMV7M_BASEPRI_WAR=y``。

Renode 脚本::

  using sysbus
  $name?="STM32F746"
  mach create $name
  machine LoadPlatformDescription @platforms/boards/stm32f7_discovery-bb.repl

  $bin ?= @nuttx

  showAnalyzer usart1
  showAnalyzer ltdc

  macro reset
  """
    sysbus LoadELF $bin
  """

  runMacro $reset

已使用 ``stm32f746g-disco/nsh`` 测试。

已知问题：

* ``stm32f746g-disco/lvgl`` - 由于不兼容的 I2C 触摸屏驱动导致崩溃

nucleo-h743zi
=============

Renode 不支持 ``PWR_CSR1_ACTVOSRDY`` 位，因此我们必须使用 ``CONFIG_STM32H7_PWR_IGNORE_ACTVOSRDY=y`` 来禁用它。

Renode 脚本::

  using sysbus
  mach create "nucleo_h743zi"
  include @platforms/boards/nucleo_h753zi.repl

  $bin=@nuttx

  showAnalyzer sysbus.usart3

  macro reset
  """
    sysbus LoadELF $bin
  """

  runMacro $reset

已使用 ``nucleo-h743zi/nsh`` 测试。
