.. todo:: revise and update links

========================
开发环境
========================

Linux + GNU ``make`` + GCC/binutils for Linux
=============================================

这是 NuttX 最自然的开发环境。可以使用任何版本的 GCC/binutils 工具链。有一个高度修改的 `buildroot <http://buildroot.uclibc.org/>`__ 可从 `NuttX Bitbucket.org <https://bitbucket.org/nuttx/buildroot/downloads/>`__ 页面下载。此下载可用于在 Linux 或 Cygwin 下构建 NuttX 兼容的 ELF 工具链。该工具链将支持 ARM、m68k、m68hc11、m68hc12 和 SuperH 移植。buildroot GIT 可在 NuttX `buildroot GIT <https://bitbucket.org/nuttx/buildroot>`__ 访问。

Linux + GNU ``make`` + SDCC for Linux
=====================================

使用 `SDCC <http://sdcc.sourceforge.net/>`__ 编译器的 Linux 环境也非常可用。SDCC 编译器支持 8051/2、z80、hc08 和其他微控制器。基于 SDCC 的逻辑测试较少，如果你使用 NuttX 中未经充分测试的 SDCC 部分，可能会遇到一些编译问题。

Windows with Cygwin + GNU ``make`` + GCC/binutils (custom built under Cygwin)
=============================================================================

这个组合也很好用。它的效果与原生 Linux 环境一样好，只是编译和构建时间稍长。上面提到的自定义 NuttX `buildroot <https://bitbucket.org/nuttx/buildroot/downloads/>`__ 也可以在 Cygwin 环境中构建。

Windows with Cygwin + GNU ``make`` + SDCC (custom built under Cygwin)
=====================================================================

此组合未被报告曾经测试过，但可能也能正常工作。

Windows with Cygwin + GNU ``make`` + Windows Native Toolchain
=============================================================

这是一个更困难的环境。在这种情况下，Windows 原生工具链不知道 Cygwin *沙箱*，而是在原生 Windows 环境中操作。主要困难是：

-  **路径**。原生工具链的完整路径必须遵循 Windows 标准。例如，路径 ``/home/my\ name/nuttx/include`` 可能需要转换为类似 ``'C:\cygwin\home\my name\nuttx\include'`` 才能被工具链使用。
-  **符号链接** NuttX 依赖符号链接将平台特定目录安装到构建系统中。在 Linux 上，使用真正的符号链接。在 Cygwin 上，使用模拟的符号链接。不幸的是，对于在 Cygwin *沙箱* 外操作的原生 Windows 应用程序，这些符号链接无法使用。
-  **依赖关系** NuttX 使用 GCC 编译器的 ``-M`` 选项生成 make 依赖关系。这些依赖关系保存在系统中名为 ``Make.deps`` 的文件中。对于 GCC 以外的编译器，不支持以这种方式生成依赖关系。

**支持的 Windows 原生工具链**。目前，使用以下 Windows 原生工具链：

#. 为 Windows 构建的 GCC（如 CodeSourcery、Atollic、devkitARM 等），
#. 为 Windows 构建的 SDCC，
#. 用于 Z16F、z8Encore 和 eZ80Acclaim 器件的 ZiLOG XDS-II 工具链。

Windows Native (``CMD.exe``) + GNUWin32 (including GNU ``make``) + MinGW Host GCC compiler + Windows Native Toolchain
=====================================================================================================================

已添加构建支持，以支持在 Windows 控制台而非类 POSIX 环境中进行原生构建。

此构建：

#. 使用所有 Windows 风格路径
#. 主要使用来自 cmd.exe 的 Windows 批处理命令，以及
#. GNUWin32 的一些扩展

此功能首次出现在 NuttX-6.24 中，仍应被视为进行中的工作，因为：（1）尚未在所有目标和工具上验证，（2）仍缺少一些成熟环境的便利功能。如果在 NuttX 配置文件中定义了 ``CONFIG_WINDOWS_NATIVE=y``，则会启动 Windows 原生构建逻辑：

目前，此构建环境还需要：

**Windows 控制台**。构建必须在 Windows 控制台窗口中执行。可以使用 Windows 自带的标准 ``CMD.exe`` 终端。ConEmu 终端可能更可取。可以从以下地址下载：http://code.google.com/p/conemu-maximus5/

**GNUWin32**。构建仍然依赖一些类 Unix 命令。GNUWin32 工具可能在这里有用。可以从 http://gnuwin32.sourceforge.net/ 下载。详见顶层 ``nuttx/README.txt`` 文件中的一些下载、构建和安装说明。

**MinGW-GCC**。MinGW-GCC 用于编译构建所需的 ``nuttx/tools`` 目录中的 C 工具。MinGW-GCC 可以从 http://www.mingw.org/ 下载。如果你使用 GNUWin32，建议不要安装可选的 MSYS 组件，因为可能会有冲突。

Wine + GNU ``make`` + Windows Native Toolchain
==============================================

以下由一位 ez80 用户报告，使用 ZiLOG ZDS-II Windows 原生工具链：

   "我在 wine（UNIX 的 Windows 模拟器）上安装了 ZDS-II 5.1.1（基于 ez80 的板的 IDE），令我惊讶的是，不需要太多更改就可以使 NuttX 的 GIT 快照可构建……我尝试了 nsh 配置，构建过程成功完成。需要说明的一点是：NuttX 的 ez80 makefile 引用了 ``cygpath`` 工具。Wine 提供了类似的 ``winepath``，它兼容且提供兼容的语法。要使用它，``winepath``（它本身是一个 shell 脚本）必须作为 ``cygpath`` 复制到 ``$PATH`` 中的某个位置，并按照以下补丁进行编辑：

   "更好的解决方案是将 ``Makefiles`` 中的所有 ``cygpath`` 引用替换为 ``$(CONVPATH)``（或在 shell 脚本中使用 ``${CONVPATH}``），并根据当前使用的环境将 ``CONVPATH`` 设置为 ``cygpath`` 或 ``winepath``。

其他环境
==================

**环境依赖**。NuttX 的主要环境依赖是（1）GNU make，（2）bash 脚本，以及（3）Linux 实用程序（如 cat、sed 等）。如果你有支持 GNU make 或与 GNU make 兼容的 make 工具的其他平台，那么 NuttX 很可能也能在该环境中工作（需要一些移植工作）。如果不支持 GNU make，则需要对 Make 系统进行一些重大修改。

**MSYS**。MSYS 未经过专门测试，但一些用户将其视为上述任何 Cygwin 环境中 Cygwin 的替代方案。这并不奇怪，因为 MSYS 基于较旧版本的 Cygwin（cygwin-1.3）。然而，MSYS 已被修改为在 Windows 环境中比 Cygwin 具有更好的互操作性，这对某些用户可能有价值。

但是，MSYS 不能与原生 Windows NuttX 构建一起使用，因为它会调用 MSYS bash shell 而不是 ``CMD.exe`` shell。在原生 Windows 构建环境中使用 GNUWin32。
