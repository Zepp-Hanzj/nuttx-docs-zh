==================
``elf`` ELF 加载器
==================

本示例构建了一个小型 ELF 加载器测试用例。它包含 ``examples/elf`` 测试下的多个测试程序。这些测试使用可重定位的 ELF 格式构建，并安装到可配置的文件系统中。运行时，文件系统会被挂载，然后逐一执行每个程序。需要 ``CONFIG_ELF``。
支持两种不同类型的文件系统：内部文件系统（包含在 NuttX 二进制文件中）和外部文件系统（不包含在二进制文件中）。外部文件系统需要手动上传。对于内部文件系统，示例支持 ``romfs`` 和 ``cromfs`` 文件系统。对于外部文件系统，可以使用任何已提供的文件系统（``vfat`` 等），同时也支持 ``romfs`` 文件系统，其镜像（``romfs.img``）会自动生成。

配置选项：

- ``CONFIG_EXAMPLES_ELF_DEVMINOR`` – ROMFS 块驱动的次设备号。例如 ``/dev/ramN`` 中的 ``N``。用于注册将承载包含待测试 ELF 可执行文件的 ROMFS 文件系统的 RAM 块驱动。默认值：``0``。

- ``CONFIG_EXAMPLES_ELF_DEVPATH`` – ROMFS 块驱动设备的路径。必须与 ``EXAMPLES_ELF_DEVMINOR`` 匹配。用于注册将承载包含待测试 ELF 可执行文件的 ROMFS 文件系统的 RAM 块驱动。默认值：``/dev/ram0``。

**注意事项**：

1. ``CFLAGS`` 应在 ``CELFFLAGS`` 中提供。RAM 和 FLASH 内存区域可能需要长调用。对于 ARM，可能需要：

     CELFFLAGS = $(CFLAGS) -mlong-calls

   类似地，C++ 标志必须在 ``CXXELFFLAGS`` 中提供。

2. 顶层 ``nuttx/Make.defs`` 文件还必须包含适当的定义 ``LDELFFLAGS``，以生成可重定位的 ELF 对象。使用 GNU LD 时，应包含 ``-r`` 和 ``-e main``（某些平台上为 ``_main``）：

     LDELFFLAGS = -r -e main

   如果使用 GCC 进行链接，可能还需要包含 ``-nostdlib``。

3. ELF 文件大小：本示例中的 ELF 文件默认情况下非常大，因为包含了大量构建冗余信息。可以使用 ``objcopy --strip-unneeded`` 命令从 ELF 文件中移除不必要的信息，从而大幅减小 ELF 二进制文件的大小。

4. 模拟器。无法在 Cygwin 上的 NuttX 模拟器中使用本示例。这是因为 Cygwin GCC 不会生成 ELF 文件，而是生成某种 Windows 原生二进制格式。

   如果确实需要这样做，可以创建 NuttX x86 构建工具链，并使用它来为 ROMFS 文件系统构建 ELF 可执行文件。

5. 链接器脚本。您可能还需要使用链接器脚本来更好地合并段。示例链接器脚本位于 ``nuttx/binfmt/elf/gnu-elf.ld``。该示例可能需要根据您的特定链接器输出进行调整，以正确定位附加段。GNU LD 的 ``LDELFFLAGS`` 可能为：

     LDELFFLAGS = -r -e main -T$(TOPDIR)/binfmt/elf/gnu-elf.ld

6. 为外部文件系统生成 ``romfs.img`` 时，需要使用 ``openocd`` 或您首选的编程器将镜像（``romfs.img``）手动复制到配置的 ``CONFIG_EXAMPLES_ELF_DEVPATH`` 起始位置。
