==========================
专用设备驱动
==========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

所有可供应用程序逻辑访问的设备驱动分为以下两类：(1) 字符设备驱动，可通过标准驱动操作（``open()``、``close()``、``read()``、``write()`` 等）进行访问；(2) 块设备驱动，只能作为挂载文件系统的一部分或前文所述的其他特殊用例进行访问。

除此之外，还有一些专用"驱动"只能在操作系统内部逻辑中使用，应用程序逻辑无法访问。这些专用驱动将在以下章节中讨论。

.. note::
  虽然特殊驱动是 *内部的*，但在某些情况下，也有位于这些特殊驱动之上的字符/块设备驱动，从而将其暴露给应用程序。

.. toctree::
  :caption: 支持的驱动

  audio.rst
  clk.rst
  devicetree.rst
  devmem.rst
  dma.rst
  framebuffer.rst
  i2c.rst
  i3c.rst
  ioexpander.rst
  lcd.rst
  mtd/index.rst
  regmap.rst
  reset.rst
  rpmsg/index.rst
  rptun/index.rst
  rwbuffer.rst
  sensors.rst
  segger.rst
  spi.rst
  syslog.rst
  sdio.rst
  usbdev.rst
  uvc.rst
  usbhost.rst
  usbmisc.rst
  usbmonitor.rst
  usrsock.rst
  video.rst
  pipes.rst
  pinctrl.rst
  ptp.rst
  mmcsd.rst
  net/index.rst
  pci/index.rst
  power/index.rst
  vhost/index.rst
  virtio/index.rst
  wireless.rst
