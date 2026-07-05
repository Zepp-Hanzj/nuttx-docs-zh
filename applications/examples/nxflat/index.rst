========================
``nxflat`` NXFLAT 二进制
========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

本示例构建了一个小型 NXFLAT 测试用例。其中包括 ``examples/nxflat`` tests 下的多个测试程序。
这些测试使用 NXFLAT 格式构建，并安装在 ROMFS 文件系统中。
在运行时，ROMFS 文件系统中的每个程序都会被执行。需要 ``CONFIG_NXFLAT``。
