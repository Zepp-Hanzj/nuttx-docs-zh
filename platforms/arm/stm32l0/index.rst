==========
ST STM32L0
==========

.. note::
   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/


Supported MCUs
==============

STM32L071, STM32L072 and STM32L073

Peripheral Support
==================

The following list indicates peripherals supported in NuttX:

==========  =======  =====
Peripheral  Support  Notes
==========  =======  =====
FLASH       No
CRC         No
FIREWALL    No
PM          No
RCC         Yes      
CSR         No
GPIO        Yes
SYSCFG      Yes      
DMA         Yes
EXTI        Yes
ADC         Yes
DAC         No
COMP        No
LCD         No 
TSC         No
AES         Yes
RNG         Yes
TIM         Yes
LPTIM       No
IWDG        Yes
WWDG        Yes
RTC         No
I2C         Yes
USART       Yes
LPUSART     No
SPI         Yes
I2S         No
USB         Yes
==========  =======  =====

Supported Boards
================

.. toctree::
   :glob:
   :maxdepth: 1

   boards/*/*
