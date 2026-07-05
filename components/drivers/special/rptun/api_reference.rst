=============
API 参考
=============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

本节描述可用于 RPTUN 操作的内核 API 和 NSH 命令。

内核 API
==========

rptun_initialize
----------------

.. c:function:: int rptun_initialize(FAR struct rptun_dev_s *dev)

   初始化并注册 RPTUN 设备。

   :param dev: 指向已配置 ops 的 RPTUN 设备结构的指针
   :return: 成功返回 OK；失败返回取反的 errno 值

   此函数创建 RPTUN 实例并将其注册到系统。如果设备配置为自动启动，它还将启动远程核。

rptun_boot
----------

.. c:function:: int rptun_boot(FAR const char *cpuname)

   启动远程 CPU。

   :param cpuname: 要启动的远程 CPU 名称
   :return: 成功返回 OK；失败返回取反的 errno 值

   示例：

   .. code-block:: c

      /* 启动名为 "M33" 的远程 CPU */
      ret = rptun_boot("M33");
      if (ret < 0)
        {
          syslog(LOG_ERR, "Failed to boot remote CPU: %d\n", ret);
        }

rptun_poweroff
--------------

.. c:function:: int rptun_poweroff(FAR const char *cpuname)

   停止远程 CPU。

   :param cpuname: 要停止的远程 CPU 名称
   :return: 成功返回 OK；失败返回取反的 errno 值

   示例：

   .. code-block:: c

      /* 停止名为 "M33" 的远程 CPU */
      ret = rptun_poweroff("M33");

rptun_reset
-----------

.. c:function:: int rptun_reset(FAR const char *cpuname, int value)

   复位远程 CPU。

   :param cpuname: 要复位的远程 CPU 名称
   :param value: 复位值（实现特定）
   :return: 成功返回 OK；失败返回取反的 errno 值

   示例：

   .. code-block:: c

      /* 复位名为 "M33" 的远程 CPU */
      ret = rptun_reset("M33", 0);

IOCTL 命令
==============

RPTUN 字符设备支持以下 ioctl 命令：

RPTUNIOC_START
--------------

启动与此 RPTUN 设备关联的远程 CPU。

.. code-block:: c

   int fd = open("/dev/rptun/remote", O_RDWR);
   ret = ioctl(fd, RPTUNIOC_START, 0);

RPTUNIOC_STOP
-------------

停止与此 RPTUN 设备关联的远程 CPU。

.. code-block:: c

   ret = ioctl(fd, RPTUNIOC_STOP, 0);

RPTUNIOC_RESET
--------------

复位与此 RPTUN 设备关联的远程 CPU。

.. code-block:: c

   int reset_value = 0;
   ret = ioctl(fd, RPTUNIOC_RESET, reset_value);

NSH 命令
============

``rptun`` NSH 命令提供用户空间对 RPTUN 设备的控制。

rptun start
-----------

启动远程核。

::

   nsh> rptun start /dev/rptun/<cpuname>

示例：

::

   nsh> rptun start /dev/rptun/M33

rptun stop
----------

停止远程核。

::

   nsh> rptun stop /dev/rptun/<cpuname>

示例：

::

   nsh> rptun stop /dev/rptun/M33

配置选项
=====================

以下 Kconfig 选项可用于 RPTUN：

CONFIG_RPTUN
------------

启用 RPTUN 驱动支持。

CONFIG_RPTUN_PRIORITY
---------------------

RPTUN 线程优先级。默认为 224。

CONFIG_RPTUN_STACKSIZE
----------------------

RPTUN 线程栈大小。默认为 4096。

头文件
============

- ``include/nuttx/rptun/rptun.h`` - 主 RPTUN 头文件，包含所有结构、宏和函数原型。

访问宏
=============

以下宏用于访问 RPTUN 操作：

.. code-block:: c

   /* 获取本地 CPU 名称 */
   RPTUN_GET_LOCAL_CPUNAME(dev)

   /* 获取远程 CPU 名称 */
   RPTUN_GET_CPUNAME(dev)

   /* 获取固件路径 */
   RPTUN_GET_FIRMWARE(dev)

   /* 获取地址环境 */
   RPTUN_GET_ADDRENV(dev)

   /* 获取资源表 */
   RPTUN_GET_RESOURCE(dev)

   /* 检查是否启用自动启动 */
   RPTUN_IS_AUTOSTART(dev)

   /* 检查是否为主核 */
   RPTUN_IS_MASTER(dev)

   /* 配置远程核 */
   RPTUN_CONFIG(dev, data)

   /* 启动远程核 */
   RPTUN_START(dev)

   /* 停止远程核 */
   RPTUN_STOP(dev)

   /* 向远程核发送通知 */
   RPTUN_NOTIFY(dev, vqid)

   /* 注册远程通知回调 */
   RPTUN_REGISTER_CALLBACK(dev, callback, arg)

   /* 注销回调 */
   RPTUN_UNREGISTER_CALLBACK(dev)

   /* 复位远程核 */
   RPTUN_RESET(dev, value)

   /* 触发远程核 panic */
   RPTUN_PANIC(dev)
