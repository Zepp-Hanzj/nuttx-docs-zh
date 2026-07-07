===============================
``flash_test`` SMART Flash 测试
===============================

作者：Ken Pettit，日期：2013 年 4 月 24 日

本示例执行 SMART Flash 块设备测试。测试对 SMART MTD 块设备进行扇区分配、读取、写入、释放和垃圾回收测试。

- ``CONFIG_EXAMPLES_FLASH_TEST=y`` – 启用 Flash 测试。

依赖项：

- ``CONFIG_MTD_SMART=y`` – SMART 块驱动支持。
- ``CONFIG_BUILD_PROTECTED=n`` 和 ``CONFIG_BUILD_KERNEL=n`` – 该测试使用内部 OS 接口，因此在 NUTTX 内核构建中不可用。

该应用程序执行 SMART Flash 块设备测试。测试对 SMART MTD 块设备进行扇区分配、读取、写入、释放和垃圾回收测试。该测试只能作为 NSH 命令构建。

**注意**：该测试使用内部 OS 接口，因此在 NUTTX 内核构建中不可用：

  Usage:
    flash_test mtdblock_device

  Additional options:
    --force                     to replace existing installation
