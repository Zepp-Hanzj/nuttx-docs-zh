==========================
``module`` 可加载模块
==========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

本示例构建了一个小型可加载模块测试用例。其中包括 ``examples/module/drivers`` 下的一个字符驱动。
该驱动使用可重定位的 ELF 格式构建，并安装在 ROMFS 文件系统中。
在运行时，加载并执行驱动模块。需要 ``CONFIG_MODULE``。其他配置选项：

- ``CONFIG_EXAMPLES_ELF_DEVMINOR`` – ROMFS 块驱动的次设备号。
  例如，``/dev/ramN`` 中的 ``N``。用于注册将保存包含待测试 ELF 可执行文件的
  ROMFS 文件系统的 RAM 块驱动。默认：``0``。

- ``CONFIG_EXAMPLES_ELF_DEVPATH`` – ROMFS 块驱动设备的路径。
  这必须与 ``EXAMPLES_ELF_DEVMINOR`` 匹配。用于注册将保存包含待测试 ELF
  可执行文件的 ROMFS 文件系统的 RAM 块驱动。默认：``/dev/ram0``。

**注意**：

1. ``CFLAGS`` 应在 ``CMODULEFLAGS`` 中提供。RAM 和 FLASH 内存区域可能需要长调用。
   对于 ARM，可能是::

     CMODULEFLAGS = $(CFLAGS) -mlong-calls

   同样，C++ 标志必须在 ``CXXMODULEFLAGS`` 中提供。

2. 您的顶层 ``nuttx/Make.defs`` 文件还必须包含适当的定义 LDMODULEFLAGS，
   以生成可重定位的 ELF 对象。使用 GNU LD 时，应包含 ``-r`` 和 ``-e <entry point>``。::

     LDMODULEFLAGS = -r -e module_initialize

   如果使用 GCC 进行链接，可能还需要包含 ``-nostdlib``。

3. 此示例还需要 ``genromfs``。``genromfs`` 可以作为 nuttx 工具链的一部分构建。
   也可以从 NuttX 工具仓库中找到的 ``genromfs`` 源码构建（``genromfs-0.5.2.tar.gz``）。
   无论如何，PATH 变量必须包含 ``genromfs`` 可执行文件的路径。

4. ELF 大小：此示例中的 ELF 文件默认情况下相当大，因为它们包含大量构建垃圾。
   您可以使用 ``objcopy --strip-unneeded`` 命令从 ELF 文件中删除不必要的信息，
   从而大大减小 ELF 二进制文件的大小。

5. 模拟器。您不能在 Cygwin 上的 NuttX 模拟器中使用此示例。
   这是因为 Cygwin GCC 不生成 ELF 文件，而是生成某种 Windows 原生二进制格式。

   如果您确实想这样做，可以创建一个 NuttX x86 ``buildroot`` 工具链，
   并使用它来构建 ROMFS 文件系统的 ELF 可执行文件。

6. 链接器脚本。您可能还想使用链接器脚本来更好地组合段。
   示例链接器脚本位于 ``nuttx/libc/elf/gnu-elf.ld``。
   该示例可能需要针对您的特定链接器输出进行调整，以正确定位额外的段。
   GNU LD ``LDMODULEFLAGS`` 可能如下::

     LDMODULEFLAGS = -r -e module_initialize -T$(TOPDIR)/libc/elf/gnu-elf.ld
