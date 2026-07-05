==========================
``camera`` 相机快照
==========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

此示例在 NuttX Shell 中实现为 ``camera`` 命令。命令的概要如下。::

  nsh> camera ([-jpg]) ([capture num])

  -jpg        : this option is set for storing JPEG file into a storage.
              : If this option isn't set capturing raw RGB565 data in a file.
              : raw RGB565 is default.

  capture num : this option instructs number of taking pictures.
              : 10 is default.

存储将根据可用的存储选项自动选择。

执行示例::

  nsh> camera
  nximage_listener: Connected
  nximage_initialize: Screen resolution (320,240)
  Take 10 pictures as RGB file in /mnt/sd0 after 5 seconds.
  After finishing taking pictures, this app will be finished after 10 seconds.
  Expier time is pasted.
  Start capturing...
  FILENAME:/mnt/sd0/VIDEO001.RGB
  FILENAME:/mnt/sd0/VIDEO002.RGB
  FILENAME:/mnt/sd0/VIDEO003.RGB
  FILENAME:/mnt/sd0/VIDEO004.RGB
  FILENAME:/mnt/sd0/VIDEO005.RGB
  FILENAME:/mnt/sd0/VIDEO006.RGB
  FILENAME:/mnt/sd0/VIDEO007.RGB
  FILENAME:/mnt/sd0/VIDEO008.RGB
  FILENAME:/mnt/sd0/VIDEO009.RGB
  FILENAME:/mnt/sd0/VIDEO010.RGB
  Finished capturing...
  Expier time is pasted.
  nximage_listener: Lost server connection: 117
