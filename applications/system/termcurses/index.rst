==============================================
``termcurses`` 终端 Curses 控制支持
==============================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 终端模拟库

Termcurses 库提供终端模拟支持，用于执行常见的屏幕操作，如光标移动、前景/背景
颜色控制和键盘转义序列映射。初始版本仅支持 ``vt100`` / ``ansi`` 终端类型，
但库架构具有可扩展的接口，允许在需要时支持其他模拟类型。

该库可以单独使用，也可以与 ``apps/graphics/pdcurses`` 库配合使用。pdcurses 库
已更新了 _termcurses_ 配置选项，可自动完全集成 termcurses 库。

用法
-----

要使用 termcurses 库，必须通过调用 ``termcurses_initterm()`` 函数来初始化例程。
此例程接受一个终端类型字符串，标识请求的终端模拟支持类型。如果传递 ``NULL`` 指针，
则例程将检查 ``TERM`` 环境变量并根据该字符串设置终端类型。如果仍然无法确定模拟类型，
例程将默认使用 ``vt100`` 模拟类型。

成功初始化后，``termcurses_initterm()`` 函数将分配一个新的终端上下文，
该上下文必须与所有后续的 termcurses 库函数一起传递。当不再需要此上下文时，
应调用 ``termcurses_deinitterm()`` 例程以进行正确的释放和终端清理。

与 ``telnetd`` 一起使用
--------------------------

将 termcurses 与 telnet 守护进程一起使用时，应启用 telnet 配置选项
``CONFIG_TELNET_SUPPORT_NAWS``。此选项向 telnet 库添加终端大小协商代码。
没有此选项，telnet 例程无法了解终端大小，因此 termcurses 例程必须默认使用
``80x24`` 屏幕模式。

与 ``pdcurses`` 一起使用
--------------------------

使用 pdcurses termcurses 支持时（即同时启用了 ``CONFIG_PDCURSES`` 和
``CONFIG_TERMCURSES`` 选项），pdcurses 输入设备应选择为 ``TERMINPUT``
（即设置 ``CONFIG_PDCURSES_TERMINPUT=y``）。这将使 pdcurses 键盘输入逻辑
使用 ``termcurses_getkeycode()`` 例程进行 curses 输入。


作者：Ken Pettit
日期：2018-2019
