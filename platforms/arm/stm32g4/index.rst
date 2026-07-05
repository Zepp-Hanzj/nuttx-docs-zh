==========
ST STM32G4
==========

.. note::
   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/


Supported MCUs
==============

TODO

Peripheral Support
==================

The following list indicates peripherals supported in NuttX:

==========  =======  =====
Peripheral  Support  Notes
==========  =======  =====
FLASH       Yes
PM          ?
RCC         Yes
CRS         No
GPIO        Yes
SYSCFG      Yes      
DMA         Yes
DMAMUX      Yes
EXTI        Yes
CRC         ?
CORDIC      Yes
FMAC        No
FSMC        ?
QUADSPI     ?
ADC         Yes
DAC         Yes
VREFBUS     ?
COMP        ?
OPAMP       Yes
RNG         ?
HRTIM       Yes
TIM         Yes
LPTIM       No
IRTIM       No
AES         ?
RTC         Yes
TAMP        No
USART       Yes
LPUART      No
SPI         Yes
I2S         ?
SAI         No
I2C         Yes
IWDG        ?
WWDG        ?
FDCAN       Yes
USB         Yes
UCPD        No
==========  =======  =====

Supported Boards
================

.. toctree::
   :glob:
   :maxdepth: 1

   boards/*/*
