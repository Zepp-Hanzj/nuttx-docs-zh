=========
makerlisp
=========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

This port use the MakerLisp machine based on an eZ80F091 ez80Acclaim!
Microcontroller, and the Zilog ZDS-II Windows command line tools.  The
development environment is Cygwin under Windows. A Windows native
development environment is available but has not been verified.

配置
==

nsh_flash
---------

``nsh.zdsproj``
    是一个简单的 ZDS-II 项目，允许你使用 ZDS-II 调试器。

``nsh.zfpproj``
    是一个简单的项目，允许你使用智能闪存编程。
    注意：截至编写时此项目可能无法正常工作，
    可能是由于项目中的 RAM 配置。请改用 ZDS-II，
    如上层 README.txt 文件中所述

``nsh_flash.ztgt``
    是伴随项目文件的目标文件。
  This one is identical to ``boards/scripts/makerlisp_ram.ztgt``.

``nsh_ram.ztgt``
    是伴随项目文件的目标文件。
  This one is identical to ``boards/scripts/makerlisp_flash.ztgt``.

nsh_ram
-------

``nsh.zdsproj``
    是一个简单的 ZDS-II 项目，允许你使用 ZDS-II 调试器。

``nsh.zfpproj``
    是一个简单的项目，允许你使用智能闪存编程。
    注意：截至编写时此项目可能无法正常工作，
    可能是由于项目中的 RAM 配置。请改用 ZDS-II，
    如上层 README.txt 文件中所述

``nsh_flash.ztgt`` is the target file that accompanies the project files.  This
  one is identical to boards/scripts/makerlisp_ram.ztgt.

``nsh_ram.ztgt``
  is the target file that accompanies the project files.  This
  one is identical to boards/scripts/makerlisp_flash.ztgt.

sdboot
------

``sdboot.zdsproj`` is a simple ZDS-II project that will allow you
  to use the ZDS-II debugger.

``sdboot.zfpproj`` is a simple project that will allow you to use the Smart Flash
    注意：截至编写时此项目可能无法正常工作，
    可能是由于项目中的 RAM 配置。请改用 ZDS-II，
    如上层 README.txt 文件中所述

``sdboot_flash.ztgt`` is the target file that accompanies the project files.
  This one is identical to ``boards/scripts/makerlisp_ram.ztgt``.

``sdboot_ram.ztgt``
    是伴随项目文件的目标文件。
  This one is identical to ``boards/scripts/makerlisp_flash.ztgt``.
