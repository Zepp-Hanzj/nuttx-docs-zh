======================
看门狗定时器驱动程序
======================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 支持一个低级的两部分看门狗定时器驱动程序。

#. "上半部分"，通用驱动程序，为应用程序代码提供通用的看门狗定时器接口，
#. "下半部分"，平台特定的驱动程序，实现底层定时器控制以实现看门狗定时器功能。

支持看门狗定时器驱动程序的文件可以在以下位置找到：

-  **接口定义**。NuttX 看门狗定时器驱动程序的头文件位于 ``include/nuttx/timers/watchdog.h``。此头文件包含看门狗定时器驱动程序的应用程序级别接口以及"上半部分"和"下半部分"驱动程序之间的接口。看门狗定时器驱动程序使用标准字符驱动程序框架。
-  **"上半部分"驱动程序**。通用的"上半部分"看门狗定时器驱动程序位于 ``drivers/timers/watchdog.c``。
-  **"下半部分"驱动程序**。平台特定的看门狗定时器驱动程序位于 ``arch/<architecture>/src/<hardware>`` 目录，针对特定处理器 ``<architecture>`` 和特定 ``<chip>`` 看门狗定时器外设设备。

有两种方式启用看门狗定时器支持和看门狗示例。第一种更快更简单。只需运行以下命令即可使用包含看门狗定时器支持和示例的现成配置文件。您需要检查是否有适用于您特定芯片的看门狗配置文件。您可以在特定板路径下检查：``/boards/<arch>/<chip>/<board>/config``。

.. code-block:: console

   $ ./tools/configure.sh <board>:watchdog

第二种方式是创建您自己的配置文件。为此，请按照以下说明操作。

在 ``menuconfig`` 中启用看门狗支持和示例
------------------------------------------------------------

1. 选择看门狗定时器实例

   要选择这些 wdt，请使用以下路径在 ``menuconfig`` 中浏览：

   进入菜单 :menuselection:`System Type --> <Chip> Peripheral Selection` 并按 :kbd:`Enter`。然后根据您芯片的可用性选择一个或多个看门狗定时器。

2. 启用看门狗定时器支持

   进入菜单 :menuselection:`Device Drivers --> Timer Driver Support` 并按 :kbd:`Enter`。然后启用：

   - [x] Watchdog Timer Support

3. 包含看门狗定时器示例

   进入菜单 :menuselection:`Application Configuration --> Examples` 并按 :kbd:`Enter`。然后选择看门狗定时器示例。

 - [x] Watchdog Timer example

在该选项下方，可以手动配置一些示例将使用的标准参数，但它们也可以稍后作为命令行参数传递。参数如下：标准定时器设备路径（定义 WDT 实例）、超时期限（看门狗到期的期限）、ping 延迟（喂狗之间的间隔时间）和 ping 时间（示例将喂狗的总间隔，超过此间隔后，狗将饥饿，芯片将触发中断或复位。

4. 包含调试看门狗功能

   为了获取看门狗定时器状态，您需要启用它。对于生产代码和您的应用程序，您可以禁用它。

   进入菜单 :menuselection:`Build Setup --> Debug Options` 并按 :kbd:`Enter`。然后启用：

   - [x] Enable Debug Features
   - [x] Watchdog Timer Debug Features

看门狗定时器示例
----------------------

之前选择的示例基本上会执行以下操作：

* 打开看门狗设备
* 设置看门狗超时
* 启动看门狗定时器
* 在 ``pingtime`` 期间以 ``pingdelay`` 的延迟 ping（喂狗），如果启用了调试则打印 wdt 状态。
* 进入无 ping 的无限循环。这将导致看门狗定时器在超时后复位芯片，即定时器到期后。

可以查看 `示例代码 <https://github.com/apache/nuttx-apps/blob/master/examples/watchdog/watchdog_main.c>`_，其路径位于 apps 仓库中的 ``/examples/watchdog/watchdog_main.c``。

在 NuttX 中，看门狗定时器驱动程序是字符驱动程序，当芯片支持多个看门狗定时器时，每个定时器可通过 ``/dev`` 目录中的相应特殊文件访问。每个看门狗定时器使用唯一的数字标识符注册（即 ``/dev/watchdog0``、``/dev/watchdog1``、...）。

使用以下命令运行示例：

.. code-block:: console

  nsh> wdog

此命令将使用看门狗定时器 0。要使用其他定时器，请通过参数指定（其中 x 是定时器编号）：

.. code-block:: console

  nsh> wdog -i /dev/watchdogx

应用程序级别接口
----------------------------

要在应用程序中使用看门狗定时器驱动程序，首先需要包含 NuttX 看门狗定时器驱动程序的头文件。它包含定时器驱动程序的应用程序级别接口。为此，包含：

.. code-block:: c

  #include <nuttx/timers/watchdog.h>

在应用程序级别，看门狗定时器功能可通过 ``ioctl`` 系统调用访问。这些 ``ioctl`` 命令内部调用下半部分层操作，参数通过 ``ioctl`` 系统调用转发到这些操作。该示例提供了演示如何使用这些 ``ioctl`` 命令的优秀资源。可用的 ``ioctl`` 命令是：

.. c:macro:: WDIOC_START

此命令启动看门狗定时器。

.. c:macro:: WDIOC_STOP

此命令停止看门狗定时器。

.. c:macro:: WDIOC_GETSTATUS

此命令获取看门狗定时器的状态。它接收指向结构体 ``watchdog_status_s`` 的可写指针作为参数。下半部分驱动程序将当前状态写入此结构体。

.. c:struct:: watchdog_status_s
.. code-block:: c

	struct watchdog_status_s
	{
	  uint32_t  flags;          /* 参见上面的 WDFLAGS_* 定义 */
	  uint32_t  timeout;        /* 当前超时设置（毫秒） */
	  uint32_t  timeleft;       /* 看门狗到期前的剩余时间（毫秒） */
	};

.. c:macro:: WDIOC_SETTIMEOUT

此命令设置超时值，即触发复位或中断的值。参数是以毫秒为单位的 ``uint32_t`` 值。

.. c:macro:: WDIOC_CAPTURE

此命令注册一个在超时时触发的用户回调。它接收指向结构体 ``watchdog_capture_s`` 的指针作为参数。如果用户回调为 NULL，则仅配置复位。并非所有芯片都支持超时时中断。此命令是可选的，即如果不使用，标准行为是在超时时复位。

.. c:struct:: watchdog_capture_s
.. code-block:: c

	struct watchdog_capture_s
	{
	  CODE xcpt_t newhandler;   /* 新的看门狗捕获处理程序 */
	  CODE xcpt_t oldhandler;   /* 之前的看门狗捕获处理程序（如果有） */
	};

.. c:macro:: WDIOC_KEEPALIVE

 此命令重置看门狗定时器，又称为 "**ping**"、"**kick**"、"**pet**"、"**feed**" the dog"。

启用内置系统监控以重置看门狗
-------------------------------------------------------

自动监控提供了一个操作系统内部机制来自动启动并重复重置看门狗。

要启用它，请按照以下说明操作：

1. 选择一个看门狗定时器实例

 要选择 wdt，请使用以下路径在 ``menuconfig`` 中浏览：

 进入菜单 :menuselection:`System Type --> <Chip> Peripheral Selection` 并按 :kbd:`Enter`。然后选择一个看门狗定时器。

2. 启用自动监控选项

   进入菜单 :menuselection:`Device Drivers --> Timer Driver Support` 并按 :kbd:`Enter`。然后启用：

   - [x] Watchdog Timer Support

   然后再次按 :kbd:`Enter` 进入看门狗定时器支持菜单。最后启用自动监控选项：

   - [x] Auto-monitor

   选择该选项后，您可能需要配置一些参数：

   * **超时**：这是看门狗定时器到期时间，以秒为单位。
   * **保持活动间隔**：这是喂狗的间隔。以秒为单位。它不能大于超时。如果此间隔等于超时间隔，则此间隔将自动更改为超时的一半。
   * **保持活动方式**：这是确定谁来喂狗的选择。有 4 种可能的选择，描述如下。

     ``Capture callback``：此选择注册看门狗定时器回调，每次到期时（即超时时）重置看门狗。

     ``Timer callback``：此选择也使用定时器回调来重置看门狗，但它将在每个"保持活动间隔"重置看门狗。

     ``Worker callback``：此选择使用工作队列在每个"保持活动间隔"重置看门狗。此选择依赖于启用低优先级或高优先级工作队列。
     如果只启用了高优先级工作队列，则使用此队列，否则使用低优先级工作队列。

     因此，在启用之前，进入菜单 :menuselection:`RTOS Features --> Work queue support` 并按 :kbd:`Enter`。

     - [x] Low priority (kernel) worker thread

     ``Idle callback``：此选择设置空闲回调来喂狗。它依赖于 PM 模块，因为此回调由 PM 状态更改触发。
     要启用它，请执行以下操作：

     进入菜单 :menuselection:`Device Drivers` 并启用：

     - [x] Power Management Support

     选择其中一个选项后，芯片将通过这些选项之一保持活动。
