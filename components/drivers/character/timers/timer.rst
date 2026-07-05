定时器驱动程序
=============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

支持定时器驱动程序的文件可以在以下位置找到：

-  **接口定义**。NuttX 定时器驱动程序的头文件位于 ``include/nuttx/timers/timer.h``。此头文件包含定时器驱动程序的应用程序级别接口以及"上半部分"和"下半部分"驱动程序之间的接口。定时器驱动程序使用标准字符驱动程序框架。
-  **"上半部分"驱动程序**。通用的"上半部分"定时器驱动程序位于 ``drivers/timers/timer.c``。
-  **"下半部分"驱动程序**。平台特定的定时器驱动程序位于 ``arch/<architecture>/src/<hardware>`` 目录，针对特定处理器 ``<architecture>`` 和特定 ``<chip>`` 定时器外设设备。

有两种方式启用定时器支持和定时器示例。第一种更快更简单。只需运行以下命令即可使用包含定时器支持和示例的现成配置文件。您需要检查是否有适用于您特定芯片的定时器配置文件。您可以在特定板路径下检查：``/boards/<arch>/<chip>/<variant>/config``。

.. code-block:: console

   $ ./tools/configure.sh <variant>:timer

第二种方式是创建您自己的配置文件。为此，请按照以下说明操作。

在 ``menuconfig`` 中启用定时器支持和示例
----------------------------------------------------------

  1. 选择定时器实例

 要选择这些定时器，请使用以下路径在 ``menuconfig`` 中浏览：

  进入菜单 :menuselection:`System Type --> <Chip> Peripheral Selection` 并按 :kbd:`Enter`。

  然后根据可用性选择一个或多个定时器。

  2. 启用定时器支持

  进入菜单 :menuselection:`Device Drivers --> Timer Driver Support` 并按 :kbd:`Enter`。然后启用：

  - [x] Timer Support
  - [x] Timer Arch Implementation

  3. 包含定时器示例

  进入菜单 :menuselection:`Application Configuration --> Examples` 并按 :kbd:`Enter`。然后选择定时器示例。

  - [x] Timer example

  在该选项下方，可以手动配置一些参数，如标准定时器设备路径、超时时间、读取计数器的采样率、要执行的采样数以及其他参数。

定时器示例
-------------

之前选择的示例基本上会查询定时器状态，设置定时器报警间隔，设置定时器信号处理函数以在报警时通知（该函数仅递增一个变量），然后启动定时器。应用程序将通过 ``menuconfig`` 中预先配置的采样率定期查询定时器状态，以跟踪定时器到期前的剩余时间。读取完采样后，应用程序停止定时器。

可以查看 `示例代码 <https://github.com/apache/nuttx-apps/blob/master/examples/timer/timer_main.c>`_，其路径位于 apps 仓库中的 ``/examples/timer/timer_main.c``。

在 NuttX 中，定时器驱动程序是字符驱动程序，当芯片支持多个定时器时，每个定时器可通过 ``/dev`` 目录中的相应文件访问。每个定时器使用唯一的数字标识符注册（即 ``/dev/timer0``、``/dev/timer1``、...）。

使用以下命令运行示例：

.. code-block:: console

  `nsh> timer`

此命令将使用定时器 0。要使用其他定时器，请通过参数指定（其中 x 是定时器编号）：

.. code-block:: console

  `nsh> timer -d /dev/timerx`

应用程序级别接口
---------------------------

要在应用程序中使用定时器驱动程序，首先需要包含 NuttX 定时器驱动程序的头文件。它包含定时器驱动程序的应用程序级别接口。为此，包含：

.. code-block:: c

  #include <nuttx/timers/timer.h>

在应用程序级别，定时器功能可通过 ``ioctl`` 系统调用访问。可用的 ``ioctl`` 命令是：

 * :c:macro:`TCIOC_START`
 * :c:macro:`TCIOC_STOP`
 * :c:macro:`TCIOC_GETSTATUS`
 * :c:macro:`TCIOC_SETTIMEOUT`
 * :c:macro:`TCIOC_NOTIFICATION`
 * :c:macro:`TCIOC_MAXTIMEOUT`
 * :c:macro:`TCIOC_TICK_GETSTATUS`
 * :c:macro:`TCIOC_TICK_SETTIMEOUT`
 * :c:macro:`TCIOC_TICK_MAXTIMEOUT`

这些 ``ioctl`` 命令内部调用下半部分层操作，参数通过 ``ioctl`` 系统调用转发到这些操作。系统调用的返回值就是操作的返回值。
``struct timer_ops_s`` 保持指向每个操作实现的指针。以下是该结构体。

.. c:struct:: timer_ops_s
.. code-block:: c

   struct timer_ops_s
   {
      /* 必需方法 *******************************************************/

      /* 启动定时器，将时间重置为当前超时值 */

      CODE int (*start)(FAR struct timer_lowerhalf_s *lower);

      /* 停止定时器 */

      CODE int (*stop)(FAR struct timer_lowerhalf_s *lower);

      /* 获取当前定时器状态 */

      CODE int (*getstatus)(FAR struct timer_lowerhalf_s *lower,
                              FAR struct timer_status_s *status);

      /* 设置新的超时值（并重置定时器） */

      CODE int (*settimeout)(FAR struct timer_lowerhalf_s *lower,
                              uint32_t timeout);

      /* 超时时调用 NuttX 内部超时回调。
         * 注意：提供 callback==NULL 禁用。
         * 不要回调应用程序。
         */

      CODE void (*setcallback)(FAR struct timer_lowerhalf_s *lower,
                                 CODE tccb_t callback, FAR void *arg);

      /* 任何未被"上半部分"驱动程序识别的 ioctl 命令
         * 通过此方法转发给下半部分驱动程序。
         */

      CODE int (*ioctl)(FAR struct timer_lowerhalf_s *lower, int cmd,
                        unsigned long arg);

      /* 获取支持的最大超时值 */

      CODE int (*maxtimeout)(FAR struct timer_lowerhalf_s *lower,
                              FAR uint32_t *maxtimeout);
   };

由于 ``ioctl`` 系统调用需要文件描述符，在使用这些命令之前，需要打开定时器设备特殊文件以获取文件描述符。以下代码片段演示了如何做到这一点：

.. code-block:: c

  /* 打开定时器设备 */

  printf("Open %s\n", devname);

  fd = open(devname, O_RDONLY);
  if (fd < 0)
    {
      fprintf(stderr, "ERROR: Failed to open %s: %d\n",
              devname, errno);
      return EXIT_FAILURE;
    }

.. c:macro:: TCIOC_START

``TCIOC_START`` 命令调用 ``start`` 操作，描述如下。

.. c:function:: int start(void)

  start 操作配置定时器，如果已经调用了 ``TCIOC_NOTIFICATION`` 则启用中断，最后启动定时器。

  :return: 失败时返回 Linux 系统错误码，成功时返回 0。

此命令可以这样使用：

.. code-block:: c

  /* 启动定时器 */

  printf("Start the timer\n");

  ret = ioctl(fd, TCIOC_START, 0);
  if (ret < 0)
    {
      fprintf(stderr, "ERROR: Failed to start the timer: %d\n", errno);
      close(fd);
      return EXIT_FAILURE;
    }

.. c:macro:: TCIOC_STOP

``TCIOC_STOP`` 命令调用 ``stop`` 操作，描述如下。

.. c:function:: int stop(void)

  stop 操作停止定时器并禁用中断。

  :return: 失败时返回 Linux 系统错误码，成功时返回 0。

此命令可以这样使用：

.. code-block:: c

  /* 停止定时器 */

  printf("\nStop the timer\n");

  ret = ioctl(fd, TCIOC_STOP, 0);
  if (ret < 0)
    {
      fprintf(stderr, "ERROR: Failed to stop the timer: %d\n", errno);
      close(fd);
      return EXIT_FAILURE;
    }

.. c:macro:: TCIOC_GETSTATUS

``TCIOC_GETSTATUS`` 命令调用 ``getstatus`` 操作，描述如下。

.. c:function:: int getstatus(FAR struct timer_status_s *status)

  getstatus 操作收集定时器的当前信息。

  :param status: 指向结构体 ``timer_status_s`` 的可写指针。该结构体包含 3 个字段：``flags``（``uint32_t``）、``timeout``（``uint32_t``）和 ``timeleft``（``uint32_t``）。`flags` 的位 0 表示定时器状态，1 表示定时器正在运行，零表示已停止。`flags` 的位 1 表示是否已注册回调。`timeout` 表示配置触发报警的时间间隔，以微秒为单位。`timeleft` 间隔表示触发报警还剩多少微秒。以下代码片段演示了如何使用它以及如何访问这些字段。

  :return: 失败时返回 Linux 系统错误码，成功时返回 0。

此命令可以这样使用：

.. code-block:: c

  /* 获取定时器状态 */

  ret = ioctl(fd, TCIOC_GETSTATUS, (unsigned long)((uintptr_t)&status));
  if (ret < 0)
    {
      fprintf(stderr, "ERROR: Failed to get timer status: %d\n", errno);
      close(fd);
      exit(EXIT_FAILURE);
    }

  /* 打印定时器状态 */

  printf("  flags: %08lx timeout: %lu timeleft: %lu\n",
         (unsigned long)status.flags, (unsigned long)status.timeout,
         (unsigned long)status.timeleft);

.. c:macro:: TCIOC_SETTIMEOUT

``TCIOC_SETTIMEOUT`` 命令调用 ``settimeout`` 操作，描述如下。

.. c:function:: int settimeout(uint32_t timeout)

  settimeout 操作设置触发报警的超时间隔，然后触发中断。它定义了处理程序将被调用的定时器间隔。

  :param timeout: 类型为 ``uint32_t`` 的参数，超时值以微秒为单位。

  :return: 失败时返回 Linux 系统错误码，成功时返回 0。

此命令可以这样使用：

.. code-block:: c

  /* 设置定时器间隔 */

  printf("Set timer interval to %lu\n",
         (unsigned long)CONFIG_EXAMPLES_TIMER_INTERVAL);

  ret = ioctl(fd, TCIOC_SETTIMEOUT, CONFIG_EXAMPLES_TIMER_INTERVAL);
  if (ret < 0)
    {
      fprintf(stderr, "ERROR: Failed to set the timer interval: %d\n", errno);
      close(fd);
      return EXIT_FAILURE;
    }

.. c:macro:: TCIOC_NOTIFICATION

``TCIOC_NOTIFICATION`` 用于配置定时器回调，以便在定时器到期时通过信号通知应用程序。此命令调用 ``setcallback`` 操作。这里不描述它，因为应用程序不直接设置回调。相反，用户应配置信号处理程序来捕获通知，然后配置定时器通知器来通知和发信号给先前配置的信号处理程序。为了更好的性能，可以配置单独的 pthread 在 sigwaitinfo() 上等待定时器事件。

在任何情况下，此命令期望一个指向结构体 `timer_notify_s` 的只读指针。该结构体包含 2 个字段：``pid``（``pid_t``），表示接收信号的任务/线程的 ID，``event``（``struct sigevent``），描述任务将被通知的方式。

此命令可以这样使用：

.. code-block:: c

  printf("Configure the notification\n");

  notify.pid   = getpid();
  notify.event.sigev_notify = SIGEV_SIGNAL;
  notify.event.sigev_signo  = CONFIG_EXAMPLES_TIMER_SIGNO;
  notify.event.sigev_value.sival_ptr = NULL;

  ret = ioctl(fd, TCIOC_NOTIFICATION, (unsigned long)((uintptr_t)&notify));
  if (ret < 0)
    {
      fprintf(stderr, "ERROR: Failed to set the timer handler: %d\n", errno);
      close(fd);
      return EXIT_FAILURE;
    }

.. c:macro:: TCIOC_MAXTIMEOUT

``TCIOC_MAXTIMEOUT`` 命令调用 ``maxtimeout`` 操作，描述如下。

.. c:function:: int maxtimeout(uint32_t *status)

  maxtimeout 操作获取可配置的最大超时值。

  :param maxtimeout: 指向 ``uint32_t`` 类型变量的可写指针，将存储该值。
  :return: 失败时返回 Linux 系统错误码，成功时返回 0。

此命令可以这样使用：

.. code-block:: c

  /* 获取最大定时器超时 */

  printf("Get the maximum timer timeout\n");

  ret = ioctl(fd, TCIOC_MAXTIMEOUT, (uint32_t*)(&max_timeout));
  if (ret < 0)
    {
      fprintf(stderr, "ERROR: Failed to read the timer's maximum timeout: %d\n", errno);
      close(fd);
      return EXIT_FAILURE;
    }

  /* 打印支持的最大超时值 */

  printf("Maximum supported timeout: %" PRIu32 "\n", max_timeout);

``TCIOC_TICK_GETSTATUS`` 命令调用 ``getstatus`` 下半部分操作，并返回以定时器 tick 表示的当前定时器状态。从微秒到 tick 的转换由定时器上半部分驱动程序执行。

  ``getstatus`` 操作收集定时器的当前信息。当通过 ``TCIOC_TICK_GETSTATUS`` 调用时，``timeout`` 和 ``timeleft`` 字段在返回给调用者之前从微秒转换为定时器 tick。

  :param status: 指向结构体 timer_status_s 的可写指针。
                 该结构体包含与 `TCIOC_GETSTATUS` 使用的相同字段，但 timeout 和 timeleft 值以定时器 tick 而不是微秒表示。
  :return: 失败时返回 Linux 系统错误码，成功时返回 0。

此命令可以这样使用：

.. code-block:: c

  /* 以 tick 获取定时器状态 */

  ret = ioctl(fd, TCIOC_TICK_GETSTATUS, (unsigned long)((uintptr_t)&status));
  if (ret < 0)
    {
      fprintf(stderr, "ERROR: Failed to get timer tick status: %d\n", errno);
      close(fd);
      return EXIT_FAILURE;
    }

  printf("flags: %08lx timeout(ticks): %lu timeleft(ticks): %lu\n",
          (unsigned long)status.flags, (unsigned long)status.timeout,
          (unsigned long)status.timeleft);

``TCIOC_TICK_SETTIMEOUT`` 命令调用 ``settimeout`` 操作并设置以定时器 tick 表示的新超时值。

  settimeout 操作配置定时器在指定数量的定时器 tick 后到期并重置定时器。超时值由定时器上半部分驱动程序在调用下半部分 settimeout 操作之前从 tick 转换为微秒。

  :param timeout: 类型为 uint32_t 的参数，指定以定时器 tick 为单位的超时间隔。
  :return: 失败时返回 Linux 系统错误码，成功时返回 0。

此命令可以这样使用：

.. code-block:: c

  /* 以 tick 设置定时器超时 */

  printf("Set timer timeout to %lu ticks\n",
  (unsigned long)timeout_ticks);

  ret = ioctl(fd, TCIOC_TICK_SETTIMEOUT, timeout_ticks);
  if (ret < 0)
    {
      fprintf(stderr, "ERROR: Failed to set timer tick timeout: %d\n", errno);
      close(fd);
      return EXIT_FAILURE;
    }

``TCIOC_TICK_MAXTIMEOUT`` 命令调用 ``maxtimeout`` 操作并返回以定时器 tick 表示的最大支持超时值。

  maxtimeout 操作获取使用基于 tick 的时间单位时可配置的最大超时值。

  :param maxtimeout: 指向 uint32_t 类型变量的可写指针，将存储最大支持的超时值（以 tick 为单位）。
  :return: 失败时返回 Linux 系统错误码，成功时返回 0。

此命令可以这样使用：

.. code-block:: c

  /* 以 tick 获取最大定时器超时 */

  printf("Get the maximum timer timeout in ticks\n");

  ret = ioctl(fd, TCIOC_TICK_MAXTIMEOUT, (uint32_t *)(&max_timeout));
  if (ret < 0)
    {
      fprintf(stderr, "ERROR: Failed to read timer tick maximum timeout: %d\n", errno);
      close(fd);
      return EXIT_FAILURE;
    }

  /* 打印支持的最大超时值（tick） */

  printf("Maximum supported timeout (ticks): %" PRIu32 "\n", max_timeout);

这些代码片段取自示例，该示例提供了演示如何使用这些 ``ioctl`` 命令的优秀资源。

软件定时器实现 (timer_wdog)
------------------------------------------

``CONFIG_TIMER_WDOG`` 选项启用基于软件的定时器驱动程序接口实现。此实现不使用硬件定时器外设，而是利用 NuttX 内部看门狗（wdog）定时器子系统来提供定时器功能。

**概念**

wdog 子系统是内核级软件定时器机制，维护一个待处理超时队列。当启用 ``timer_wdog`` 时，它创建一个标准定时器设备（例如 ``/dev/timer0``），内部使用 ``wd_start()`` 和相关的 wdog API 来调度和管理超时。这允许没有专用硬件定时器的平台仍然为应用程序提供标准定时器驱动程序接口。

**启用 timer_wdog**

要启用此功能，请设置以下配置选项：

.. code-block:: none

   CONFIG_TIMER=y
   CONFIG_TIMER_WDOG=y

然后从板初始化代码调用 ``timer_wdog_initialize()``。

.. code-block:: c

   #include <nuttx/timers/timer_wdog.h>

   #ifdef CONFIG_TIMER_WDOG
     ret = timer_wdog_initialize(0);  /* 创建 /dev/timer0 */
     if (ret < 0)
       {
         syslog(LOG_ERR, "ERROR: timer_wdog_initialize failed: %d\n", ret);
       }
   #endif

**优点**

- **无硬件依赖**：适用于支持 NuttX wdog 子系统的任何平台，包括模拟器（sim）。
- **易于启用**：需要最少的板级代码；只需一个初始化调用。
- **标准接口**：应用程序使用与基于硬件的定时器相同的定时器 ioctl 命令，确保可移植性。
- **适用于测试**：非常适合在模拟器或缺少硬件定时器的平台上测试依赖定时器的应用程序代码。
- **多实例**：可以通过使用不同 ID 调用 ``timer_wdog_initialize()`` 来创建多个软件定时器。

**缺点**

- **分辨率受系统 tick 限制**：定时器分辨率受系统 tick 率（``CONFIG_USEC_PER_TICK``）约束。例如，10ms tick 时，最小超时粒度为 10ms。
- **不如硬件定时器精确**：软件定时器依赖于调度器，可能会出现抖动，特别是在系统负载较重时。
- **在中断上下文中运行**：超时回调在系统定时器中断的上下文中执行，这可能会为信号传递到应用程序引入延迟。
- **不适合高精度定时**：需要微秒级精度的应用程序应使用硬件定时器实现。

**使用场景**

- 基于模拟器的开发和测试
- 没有可用硬件定时器外设的平台
- 原型设计基于定时器的应用程序逻辑
- 教学目的和学习 NuttX 定时器接口
