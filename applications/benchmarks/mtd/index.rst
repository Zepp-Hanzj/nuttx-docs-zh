============================================
``mtd`` MTD 测试和传输速率基准测试
============================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

此测试/基准测试应用程序执行擦除/写入操作以评估写入传输速率，
然后读回写入的内容以评估读取传输速率。
最后，它将读取的数据与之前写入的数据进行比较，以确保 MTD 设备按预期工作。

示例::

  nsh> mtd /dev/mtdblock0
  FLASH Test on device with:
    Sector size:        4096
    Sector count:        256
    Erase block:        4096
    Total size:      1048576

  Starting write operation...

  Write operation completed in 5.46 seconds
  Total bytes written: 1048576
  Transfer rate [write]: 187.55 KiB/s

  Starting read operation...

  Read operation completed in 0.11 seconds
  Total bytes read: 1048576
  Transfer rate [read]: 9309.09 KiB/s

  Data verification successful: read data matches written data
