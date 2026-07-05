====
z20x
====

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

微控制器。此目录包含将 NuttX 移植到 z80x 开发板的内容，
该开发板基于 ez80Acclaim! eZ80F091 微控制器。

配置
==


hello
-----

``hello.zdsproj``
    是一个简单的 ZDS-II 项目，允许你使用 ZDS-II 调试器。

``hello.zfpproj``
    是一个简单的项目，允许你使用智能闪存编程。
    注意：截至编写时此项目可能无法正常工作，
    可能是由于项目中的 RAM 配置。请改用 ZDS-II，
    如上层 README.txt 文件中所述

``hello_ram.ztgt`` is the target file that accompanies the project files.
    此文件与 ``boards/scripts/z20x_ram.ztgt`` 相同。

``hello_flash.ztgt``
    是伴随项目文件的目标文件。
    此文件与 ``boards/scripts/z20x_flash.ztgt`` 相同。

nsh
---

``nsh.zdsproj``
    是一个简单的 ZDS-II 项目，允许你使用 ZDS-II 调试器。

``nsh.zfpproj``
    是一个简单的项目，允许你使用智能闪存编程。
    注意：截至编写时此项目可能无法正常工作，
    可能是由于项目中的 RAM 配置。请改用 ZDS-II，
    如上层 README.txt 文件中所述

``nsh_ram.ztgt``
    是伴随项目文件的目标文件。
    此文件与 ``boards/scripts/z20x_ram.ztgt`` 相同。

``nsh_flash.ztgt``
    是伴随项目文件的目标文件。
    此文件与 ``boards/scripts/z20x_flash.ztgt`` 相同。

sdboot
------

``sdboot.zdsproj``
    是一个简单的 ZDS-II 项目，允许你使用 ZDS-II 调试器。

``sdboot.zfpproj``
    是一个简单的项目，允许你使用智能闪存编程。
    注意：截至编写时此项目可能无法正常工作，
    可能是由于项目中的 RAM 配置。请改用 ZDS-II，
    如上层 README.txt 文件中所述

``sdboot_flash.ztgt``
    是伴随项目文件的目标文件。
    此文件与 ``boards/scripts/z20x_ram.ztgt`` 相同。

``sdboot_ram.ztgt``
    是伴随项目文件的目标文件。
    此文件与 ``boards/scripts/z20x_flash.ztgt`` 相同。

w25boot
-------

``w25boot.zdsproj``
    是一个简单的 ZDS-II 项目，允许你使用 ZDS-II 调试器。

``w25boot.zfpproj``
    是一个简单的项目，允许你使用智能闪存编程。
    注意：截至编写时此项目可能无法正常工作，
    可能是由于项目中的 RAM 配置。请改用 ZDS-II，
    如上层 README.txt 文件中所述

``w25boot_flash.ztgt``
    是伴随项目文件的目标文件。
    此文件与 boards/scripts/z20x_ram.ztgt 相同。

``w25boot_ram.ztgt``
    是伴随项目文件的目标文件。
    此文件与 boards/scripts/z20x_flash.ztgt 相同。
