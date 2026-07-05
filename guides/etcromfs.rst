=========================
etc romfs
=========================
ROMFS 映像是 ``/etc`` 目录的内容，包括启动脚本，包含 NuttX 支持的任何命令，以及其他所需的自定义内容。

配置
=============

.. code-block:: console

  CONFIG_NSH_ROMFS          /* 在 "/etc" 挂载 ROMFS 文件系统，并在 "/etc/init.d.rc.sysinit" 提供系统初始化脚本，
                               在 "etc/init.d/rcS" 提供启动脚本。 */
  CONFIG_ETC_ROMFSMOUNTPT   /* ROMFS 卷的默认挂载点是 "/etc"，但可以通过此设置更改。
                               这必须是以 '/' 开头并用引号括起来的绝对路径。 */
  CONFIG_ETC_ROMFSDEVNO     /* 这是 ROMFS 块设备的次设备号。默认值为 '0'，
                               对应 "/dev/ram0"。 */
  CONFIG_ETC_ROMFSSECTSIZE  /* 这是 ROMFS 卷使用的扇区大小。由于默认卷非常小，
                               默认值为 64，但如果 ROMFS 卷变大，应增加此值。
                               选择的任何值必须是 2 的幂。 */

此功能还依赖于：

.. code-block:: console

  CONFIG_DISABLE_MOUNTPOINT  /* 如果禁用挂载点支持，则无法挂载任何文件系统。 */
  CONFIG_FS_ROMFS            /* 此选项启用 ROMFS 文件系统支持。 */

启动脚本
================

**启动脚本**。启动脚本包含 NuttX 支持的任何命令（即您在输入 'nsh> help' 时看到的命令）。提供的实现旨在为启动文件的使用提供极大的灵活性。本段将讨论所有配置选项设置为默认值时的常规行为。

在此默认情况下，启用 ``CONFIG_ETC_ROMFS`` 将使 NuttX 在启动时表现如下：

  -  NuttX 将创建一个只读 RAM 磁盘（ROM 磁盘），其中包含一个小型 ROMFS 文件系统，内容如下::

      `--init.d/
          `-- rcS
          `-- rc.sysinit

     其中 ``rcS`` 是启动脚本。
     其中 ``rc.sysinit`` 是系统初始化脚本。

  -  然后 NuttX 将在 ``/etc`` 挂载 ROMFS 文件系统，结果为::

      |--dev/
      |   `-- ram0
      `--etc/
          `--init.d/
              `-- rcS
              `-- rc.sysinit

  -  默认情况下，``rc.sysinit`` 脚本的内容优先使用 TMPFS 作为 ``/tmp``，在未启用 TMPFS 时回退到 FAT RAMDISK::

      # Mount /tmp on TMPFS
      mount -t tmpfs /tmp

      # Otherwise create a RAMDISK and mount it at /tmp
      mkrd -m 1 -s 512 1024
      mkfatfs /dev/ram1
      mount -t vfat /dev/ram1 /tmp

  -  NSH 将在系统初始化时（在第一个 NSH 提示符之前）执行 ``/etc/init.d/rc.sysinit`` 中的脚本。执行脚本后，根文件系统将如下所示::

      |--dev/
      |   |-- ram0
      |   `-- ram1
      |--etc/
      |   `--init.d/
      |       `-- rcS
      |       `-- rc.sysinit
      `--tmp/

**示例配置**。以下是一些在 NuttX 配置文件中包含 ``CONFIG_ETC_ROMFS=y`` 的配置。它们可能提供有用的示例：

  -  ``boards/arm/stm32/hymini-stm32v/nsh2``
  -  ``boards/arm/dm320/ntosd-dm320/nsh``
  -  ``boards/sim/sim/sim/nsh``
  -  ``boards/sim/sim/sim/nsh2``
  -  ``boards/sim/sim/sim/nx``
  -  ``boards/sim/sim/sim/nx11``
  -  ``boards/sim/sim/sim/touchscreen``

在大多数情况下，配置设置了 *默认* 的 ``/etc/init.d/rc.sysinit`` 和 ``/etc/init.d/rcS`` 脚本。默认脚本在这里：``apps/nshlib/rc.sysinit.template`` 和 ``apps/nshlib/rcS.template``。（rc.sysinit.template 中的有趣值如 ``XXXMKRDMINORXXX`` 在构建时通过 ``sed`` 替换）。此默认配置在启用时将 ``/tmp`` 挂载为 TMPFS，否则创建 RAMDISK 并在 ``/tmp`` 挂载 FAT，如上所述。

自定义启动脚本
============================

要修改启动行为，需要研究三件事：

  #. **配置选项。** 与 `配置` 一起讨论的附加 ``CONFIG_ETC_ROMFS`` 配置选项

  #. ``tools/mkromfsimg.sh`` **脚本**。脚本 ``tools/mkromfsimg.sh`` 创建 ``etc_romfs.c``。它不会自动执行。如果您想更改与创建和挂载 ``/tmp`` 目录相关的配置设置，则需要使用 ``tools/mkromfsimg.sh`` 脚本重新生成此头文件。

     此脚本的行为取决于几件事：

     #. 已安装配置的配置设置。

     #. ``genromfs`` 工具（可从 `http://romfs.sourceforge.net <http://romfs.sourceforge.net/>`__ 获取）或包含在 NuttX buildroot 工具链中。NuttX 工具仓库中也有快照 `此处 <https://bitbucket.org/nuttx/tools/src/master/genromfs-0.5.2.tar.gz>`__。

     #. 用于生成 C 头文件的 ``xxd`` 工具（xxd 是完整 Linux 或 Cygwin 安装的正常部分，通常是 ``vi`` 包的一部分）。

     #. 文件 ``include/arch/board/rc.sysinit.template`` 和文件 ``include/arch/board/rcs.template``

  #. ``rc.sysinit.template``。文件 ``apps/nshlib/rc.sysinit.template`` 包含 ``rc.sysinit`` 文件的一般形式；配置值被插入此模板文件以生成最终的 ``rc.sysinit`` 文件。

     ``rcS.template``。文件 ``apps/nshlib/rcS.template`` 包含 ``rcS`` 文件的一般形式；配置值被插入此模板文件以生成最终的 ``rcS`` 文件。

     要生成自定义的 ``rc.sysinit`` 和 ``rcS`` 文件，需要将 ``rc.sysinit.template`` 和 ``rcS.template`` 的副本放在 ``tools/`` 中，并根据所需的启动行为进行更改。运行 ``tools/mkromfsimg.h`` 创建 ``etc_romfs.c``，需要将其复制到 ``arch/board/src`` 并在 Makefile 中编译。

所有启动行为都包含在 ``rc.sysinit.template`` 和 ``rcS.template`` 中。``mkromfsimg.sh`` 脚本的作用是 (1) 将特定配置设置应用于 ``rc.sysinit.template`` 以创建最终的 ``rc.sysinit``，以及 ``rcS.template`` 以创建最终的 ``rcS``，(2) 生成包含 ROMFS 文件系统映像的源文件 ``etc_romfs.c``。为此，``mkromfsimg.sh`` 使用两个必须安装在系统中的工具：

  #. 用于生成 ROMFS 文件系统映像的 ``genromfs`` 工具。

  #. 用于创建 C 头文件的 ``xxd`` 工具。

自定义 ROMFS 映像
=======================

ROMFS 映像可以从相应的 ``board/arch/board/board/src/etc`` 目录中的内容生成，并通过 Makefile 添加。

**示例配置**。以下是一些在 NuttX 配置文件中包含 ``CONFIG_ETC_ROMFS=y`` 的配置。它们可能提供有用的示例：

  -  ``boards/risc-v/bl808/ox64/src/etc``
  -  ``boards/risc-v/qemu-rv/rv-virt/src/etc``
  -  ``boards/risc-v/esp32c3/esp32c3-devkit/src/etc``
  -  ``boards/risc-v/k230/canmv230/src/etc``
  -  ``boards/risc-v/jh7110/star64/src/etc``
  -  ``boards/arm64/rk3399/nanopi_m4/src/etc``
  -  ``boards/sim/sim/sim/src/etc``
