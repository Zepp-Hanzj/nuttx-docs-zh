===========================
GNSS Lower Half uORB Driver
===========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

GNSS 下半部分驱动程序用于为 GNSS/GPS 设备创建 uORB 驱动程序。
上半部分驱动程序抽象了 NMEA 数据的解析和发布。此下半部分的实例化
方式类似于 :doc:`uORB 框架
</components/drivers/special/sensors/sensors_uorb>` 中的下半部分驱动程序。

有关如何使用此下半部分的示例，请参阅
`</components/drivers/special/sensors/l86xxx>`

应用编程接口
=================================

要在您的驱动程序中使用 GNSS 下半部分，只需包含以下头文件：

.. code-block:: c

      #include <nuttx/sensors/gnss.h>


GNSS 驱动程序的工作方式类似于 uORB 下半部分驱动程序，您必须为上半部分
实现多个操作。第一步是为您的 GNSS 设备定义自定义类型，其中必须包含对
下半部分结构体的引用。在本例中，设备基于 UART，因此包含多个成员以
方便其操作。

.. code-block:: c

   /* 自定义 GNSS 设备类型 */

   typedef struct
   {
     FAR struct file uart;          /* 获取数据的 UART 接口 */
     struct gnss_lowerhalf_s lower; /* GNSS 下半部分 */
     bool enabled;                  /* 启用状态 */
     char buffer[256];              /* UART 读取缓冲区 */
     mutex_t lock;                  /* 设备锁 */
     sem_t run;                     /* 启动/停止内核线程 */
   } my_gnss_dev_s;


然后，您可以创建操作表。

.. code-block:: c

   static const struct gnss_ops_s g_gnss_ops =
   {
     .control = my_gnss_control,
     .activate = my_gnss_activate,
     .set_interval = my_gnss_set_interval,
   }

这些函数与您用于实现 uORB 下半部分的函数非常相似。

* ``control`` 函数用于处理上半部分未实现的 ``IOCTL`` 命令

* ``activate`` 函数用于启用/禁用设备，以便在不使用时节省功耗

* ``set_interval`` 函数用于设置采样率

由您来实现这些函数，以满足上半部分驱动程序的要求。

对于此实现，由于我们从 UART 接口读取数据，我们将从 ``my_gnss_dev_s``
结构体的 ``uart`` 成员读取到读取缓冲区。这在内核线程中进行，该线程
轮询 UART 接口。读取数据后，我们只需将其发送到上半部分进行解析并
作为 uORB 数据发布。

我们提供给上半部分的数据不需要是以空字符结尾的字符串，甚至不需要是
完整的 NMEA 句子。上半部分会边解析边处理，并等到自己的缓冲区中有
完整句子后再进行解析。

以下是发布该数据的示例：

.. code-block:: c

   /* `dev` 是对我们 `my_gnss_dev_s` 结构体的引用 */

   err = nxmutex_lock(&dev->lock);
   if (err < 0)
     {
       snerr("Couldn't lock mutex\n");
       return err;
     }

   bw = file_read(&dev->uart, dev->buffer, sizeof(dev->buffer));

   if (bw <= 0)
     {
       snerr("No data on UART: %d\n", bw);
       nxmutex_unlock(&dev->lock);
       continue;
     }

   /* 将读取的数据发送到下半部分进行解析。不需要是完整的
    * NMEA 句子即可处理。
    */

   if (bw > 0)
     {
       dev->lower.push_data(dev->lower.priv, dev->buffer, bw, true);
     }

   nxmutex_unlock(&dev->lock);

实现以上所有内容后，在驱动程序的注册函数中，您需要在注册函数中
初始化 GNSS 设备的结构。

.. code-block:: c

   /* 此设备类型的注册函数 */

   int mygnss_register(FAR char const *uartpath, int devno)
   {
      FAR mygnss_dev_s *priv;
      int err;
      uint32_t nbuffers[SENSOR_GNSS_IDX_GNSS_MAX];

      /* 这是一个不考虑错误处理的简单示例 */

      priv = kmm_zalloc(sizeof(my_gnss_dev_s));

      /* 在此处初始化设备结构体的特定成员...
       */

      priv->lower.ops = &g_gnss_ops; /* 操作表 */
      priv->lower.priv = priv; /* 对下半部分的引用 */

      /* 这为处理这些事件集的每个缓冲区选择缓冲区大小。
       * 索引宏包含在 gnss 头文件中
       */

      nbuffers[SENSOR_GNSS_IDX_GNSS] = 1;
      nbuffers[SENSOR_GNSS_IDX_GNSS_SATELLITE] = 1;
      nbuffers[SENSOR_GNSS_IDX_GNSS_MEASUREMENT] = 1;
      nbuffers[SENSOR_GNSS_IDX_GNSS_CLOCK] = 1;
      nbuffers[SENSOR_GNSS_IDX_GNSS_GEOFENCE] = 1;

      /* 使用我们的信息注册下半部分驱动程序。
       * `SENSOR_GNSS_IDX_GNSS_MAX` 是我们 `nbuffers` 数组的长度。
       */

      err =
          gnss_register(&priv->lower, devno, nbuffers, SENSOR_GNSS_IDX_GNSS_MAX);
      if (err < 0)
        {
          snerr("Failed to register myGNSS driver: %d\n", err);
          /* 您应该通过清理资源来处理错误 */
        }

      /* 在此处处理启动内核线程和任何其他错误清理。 */

      return err;
   }

在设备代码中注册
===========================

要在设备代码中注册驱动程序，只需调用您编写的注册函数。您需要包含
您的头文件。

.. code-block:: c

   #if defined(CONFIG_SENSORS_MYGNSS) /* 更改为您的 GNSS 驱动程序 */
   #include <nuttx/sensors/mygnss.h>
   #endif

   /* 将此放在您的板卡实际启动函数中，其他驱动程序正在注册的位置。 */

   int my_board_bringup(void)
   {
     #if defined(CONFIG_SENSORS_MYGNSS)
       /* 在 USART0 上注册 myGNSS */

       ret = l86xxx_register("/dev/ttyS0", 0);
       if (ret < 0) {
         syslog(LOG_ERR, "Failed to register myGNSS driver: %d\n", ret);
       }
     #endif
   }

操作
=========

现在您应该看到几个不同的 uORB GNSS 主题在 ``/dev/uorb`` 下发布。
这些对应于您之前初始化的所有不同缓冲区类型，如地理围栏、时钟、
卫星等。普通的 ``sensor_gnss`` 设备将从 NMEA 句子中发布大量数据。

您可以使用 ``uorb_listener`` 应用程序
(:doc:`/applications/system/uorb/index`) 来查看数据是否正确发布。

.. code-block:: console

   nsh> uorb_listener sensor_gnss

   Monitor objects num:2
   object_name:sensor_gnss, object_instance:0
   sensor_gnss(now:237030000):timestamp:237030000,time_utc:1753502745,latitude:xxxxxxxx,longitude:xxxxxxxxxx,altitude:36.900002,altitude_ellipsoid:24.200001,0
