======================
``fastboot`` fastbootd
======================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

准备工作
==========================

- 检查 fastboot 工具（主机端）：:code:`fastboot --version`
- 下载并安装 fastboot 工具（主机端）：`platform-tools <https://developer.android.com/tools/releases/platform-tools>`__
- 启用 fastbootd 应用程序（设备端）：:code:`CONFIG_USBFASTBOOT=y` 和 :code:`CONFIG_SYSTEM_FASTBOOTD=y`
- 启动 fastbootd（设备端）：:code:`fastbootd &`

命令
==========================

- :code:`fastboot reboot [FLAG]`: 重启设备，:code:`[FLAG]` 的更多详情：`g_resetflag <https://github.com/apache/nuttx-apps/blob/master/nshlib/nsh_syscmds.c#L114>`__ 和 `boardioc_softreset_subreason_e <https://github.com/apache/nuttx/blob/master/include/sys/boardctl.h#L458>`__
- :code:`fastboot flash <PARTITION> <FILENAME>`: 使用给定的 :code:`<FILENAME>` 刷写分区 :code:`<PARTITION>`
- :code:`fastboot erase <PARTITION>`: 擦除给定分区
- 获取变量
   - :code:`fastboot getvar product`: 获取产品名称
   - :code:`fastboot getvar kernel`: 获取内核名称
   - :code:`fastboot getvar version`: 获取操作系统版本字符串
   - :code:`fastboot getvar slot-count`: 获取槽位数量
   - :code:`fastboot getvar max-download-size`: 获取最大下载大小
- OEM
   - :code:`fastboot oem filedump <PARTITION> [OFFSET] [LENGTH]`: 从 :code:`<OFFSET>`（默认为零）获取 :code:`<PARTITION>` 的 :code:`<LENGTH>`（默认为全部）字节数据
   - :code:`fastboot oem memdump <ADDRESS> <LENGTH>`: 从地址 :code:`<ADDRESS>` 转储 :code:`<LENGTH>` 字节内存
   - :code:`fastboot oem shell <COMMAND>`: 执行自定义命令，例如 "oem shell ps"、"oem shell ls /dev/"
- :code:`fastboot get_staged <OUT_FILE>`: 将上一个命令暂存的数据写入文件 :code:`<OUT_FILE>`，例如 "oem filedump" 和 "oem memdump"

示例
==========================

- 退出 fastboot 模式：:code:`fastboot reboot`
- 将 app.bin 刷写到 /dev/app 分区：:code:`fastboot flash app ./app.bin`
- 擦除 /dev/userdata 分区：:code:`fastboot erase userdata`
- 转储 /dev/app 分区：:code:`fastboot filedump /dev/app` 然后 :code:`fastboot get_staged ./dump_app.bin`
- 转储从 0x44000000 到 0x440b6c00 的内存：:code:`fastboot oem memdump 0x44000000 0xb6c00` 然后 :code:`fastboot get_staged ./mem_44000000_440b6c00.bin`
- 创建大小为 320KB 的 RAM 磁盘 "/dev/ram10"：:code:`fastboot oem shell "mkrd -m 10 -s 512 640"`
