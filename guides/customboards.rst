====================
自定义开发板操作指南
====================

如 :doc:`../quickstart/configuring` 中所述，受支持的开发板（也称为"树内"开发板）使用标准语法进行配置：

    .. code-block:: console

      $ cd nuttx
      $ ./tools/configure.sh -l board-name:config-name
        Copy files
        Select CONFIG_HOST_LINUX=y
        Refreshing...

有时将新的或自定义的开发板添加到 NuttX 板树本身并不合适或不希望这样做。如果是这样，可以在自定义目录中树外定义开发板，并且仍然可以轻松构建。

添加自定义开发板
==================

需要与树内开发板提供的相同文件集（即 configs、Kconfig、scripts 等），但这些文件可以放在您选择的目录中。

在此示例中，文件假定存在于：
 ``../nuttx/CustomBoards/MyCustomBoardName``

    .. code-block:: console

      $pwd
      /home/nuttx/nuttx
      $ ls -1 ../CustomBoards/MyCustomBoardName
      configs
      helpers
      include
      Kconfig
      scripts
      $ ls ../CustomBoards/MyCustomBoardName/configs
      nsh
      MyCustomConfig
      $

在此阶段，文件的内容并不重要。值得注意的例外是名为 ``defconfig`` 的文件，它存储在 ``MyCustomConfig`` 目录中（参见上面的列表）。

此文件是自动生成的，不应手动编辑。但是，也不应盲目地从现有板复制，因为其中的值对于自定义板是不正确的。这会导致问题，因为下面调用的 configure 脚本应该在 NuttX 源码树中创建一些符号链接，并且它使用 ``defconfig`` 文件的内容来实现这一点。由于文件不存在，configure 脚本将失败，这会阻止用户自动创建 ``defconfig`` 文件。

作为变通方法，需要提供一个最小的 ``defconfig`` 文件。参见 AVR 架构的示例：

    .. code-block:: kconfig

      CONFIG_ARCH="avr"
      CONFIG_ARCH_AVR=y
      CONFIG_ARCH_BOARD_CUSTOM=y
      CONFIG_ARCH_BOARD_CUSTOM_DIR_RELPATH=y
      CONFIG_ARCH_BOARD_CUSTOM_DIR="../CustomBoards/MyCustomBoardName/"
      CONFIG_ARCH_BOARD_CUSTOM_NAME="MyCustomBoardName"
      CONFIG_ARCH_CHIP="avrdx"

此最小文件应足以使 configure 脚本成功。可以使用 ``make menuconfig`` 进行额外更改，然后可以使用 ``make savedefconfig`` 生成正确的 ``defconfig`` 文件。

要构建自定义板，请更改上面示例的内容以适应您的架构和芯片，然后使用此语法，与树内板和配置略有不同：

    .. code-block:: console

      $ ./tools/configure.sh -l ../CustomBoards/MyCustomBoardName/configs/MyCustomConfig
      Copy files
      Select CONFIG_HOST_LINUX=y
      Refreshing...

Kconfig 设置
================

配置板后，为确保后续构建正确运行，需要设置两个 Kconfig 设置。这些是：

:menuselection:`Board Selection --> Custom Board Configuration --> Custom Board Name`

:menuselection:`Board Selection --> Custom Board Configuration --> Relative custom board directory`

它们应设置为适合您的板名和目录位置。

.. Note::
   如果您随后运行 ``make distclean`` 操作，则这些设置将丢失。应在构建之前和/或运行 ``make menuconfig`` 之前将其添加回来。
