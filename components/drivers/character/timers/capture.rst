=======
捕获
=======

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

**捕获驱动程序**是一个字符设备驱动程序，允许在特定事件上捕获定时器值。这对于测量输入信号的频率、占空比或脉冲计数等任务非常有用。

本文档基于 STM32H7 定时器捕获驱动程序。

使用方法
=====

捕获驱动程序通过设备文件（例如 ``/dev/capture0``）访问。您可以使用标准文件操作以及 ``ioctl()`` 调用来检索捕获的值或配置驱动程序。

支持的 ``ioctl`` 命令
----------------------------

.. c:macro:: CAPIOC_DUTYCYCLE

   从捕获单元获取 PWM 占空比。

   **参数：** ``int8_t *``（指向占空比百分比的指针）。

.. c:macro:: CAPIOC_FREQUENCY

   从捕获单元获取脉冲频率。

   **参数：** ``int32_t *``（指向频率（Hz）的指针）。

.. c:macro:: CAPIOC_EDGES

   获取检测到的 PWM 边沿数量。

   **参数：** ``int32_t *``（指向边沿计数的指针）。

.. c:macro:: CAPIOC_ALL

   在单次调用中获取占空比、脉冲频率和边沿计数。

   **参数：** ``struct cap_all_s *``（包含所有值的结构体）。

.. c:macro:: CAPIOC_PULSES

   读取当前脉冲计数值。

   **参数：** ``int *``（指向脉冲计数的指针）。

.. c:macro:: CAPIOC_CLR_CNT

   清除脉冲计数值。

   **参数：** 无。

.. c:macro:: CAPIOC_FILTER

   配置毛刺过滤器。

   **参数：** ``uint32_t``（以纳秒为单位的过滤器值，``0`` 禁用）。

.. c:macro:: CAPIOC_HANDLER

   设置捕获事件的用户回调函数。

   **参数：** ``xcpt_t``（函数指针，``NULL`` 禁用）。

.. c:macro:: CAPIOC_ADD_WP

   向捕获单元添加监视点。

   **参数：** ``int``（要监视的值）。

.. c:macro:: CAPIOC_REGISTER

   注册捕获边沿事件通知。这允许应用程序在捕获边沿事件发生时接收异步信号通知，而不是轮询事件。

   **参数：** ``struct cap_notify_s *``（指向通知结构体的指针）。

   ``struct cap_notify_s`` 包含：

   * ``event`` - 信号事件配置（``struct sigevent``）
   * ``chan`` - 捕获通道号
   * ``type`` - 边沿类型（``CAP_TYPE_RISING``、``CAP_TYPE_FALLING`` 或 ``CAP_TYPE_BOTH``）
   * ``ptr`` - 用户数据指针

   **返回值：**

   * 成功时返回 ``OK``
   * 无效通道返回 ``-EINVAL``
   * 通道已被其他任务注册时返回 ``-EBUSY``

.. c:macro:: CAPIOC_UNREGISTER

   注销捕获边沿事件通知。

   **参数：** ``int``（通道号）。

   **返回值：** 成功时返回 ``OK``。

配置
-------------

要启用捕获驱动程序，请启用以下配置选项：

* ``CONFIG_CAPTURE`` - 启用捕获驱动程序框架
* ``CONFIG_CAPTURE_NOTIFY`` - 启用边沿事件的信号通知支持
* ``CONFIG_FAKE_CAPTURE`` - 启用用于测试的假捕获驱动程序（生成 10Hz 信号，50% 占空比）
* ``CONFIG_STM32H7_TIM4_CAP``（用于 STM32H7 定时器 4，平台特定）

``CONFIG_CAPTURE`` 选项启用下半部分驱动程序并注册 ``/dev/capture`` 设备。

``CONFIG_CAPTURE_NOTIFY`` 选项启用信号通知功能，允许应用程序在捕获边沿事件发生时接收异步通知。这需要硬件支持边沿中断，并依赖于 ``CONFIG_CAPTURE``。

``CONFIG_FAKE_CAPTURE`` 选项启用基于软件的假捕获驱动程序，模拟 10Hz 方波，50% 占空比。这对于在没有实际硬件的情况下进行开发和测试非常有用。它依赖于 ``CONFIG_CAPTURE`` 和 ``CONFIG_CAPTURE_NSIGNALS > 0``。

没有它时，仍然可以通过包含适当的头文件（例如 ``arch/arm/src/stm32h7/stm32_capture.h``）并执行手动初始化来进行捕获。

示例
-------

以下是使用捕获驱动程序读取信号频率的简单示例：

.. code-block:: c

    #include <stdio.h>
    #include <fcntl.h>
    #include <sys/ioctl.h>
    #include <nuttx/timers/capture.h>

    int main(int argc, char *argv[])
    {
      int fd;
      uint32_t frequency;

      fd = open("/dev/capture0", O_RDONLY);
      if (fd < 0)
        {
          perror("Failed to open capture device");
          return 1;
        }

      if (ioctl(fd, CAPIOC_FREQUENCY, (unsigned long)&frequency) < 0)
        {
          perror("Failed to get frequency");
          close(fd);
          return 1;
        }

      printf("Frequency: %u Hz\n", frequency);

      close(fd);
      return 0;
    }

信号通知示例
----------------------------

以下是使用信号通知进行事件驱动捕获的示例（需要 ``CONFIG_CAPTURE_NOTIFY``）：

.. code-block:: c

    #include <stdio.h>
    #include <signal.h>
    #include <fcntl.h>
    #include <sys/ioctl.h>
    #include <nuttx/timers/capture.h>

    static volatile int edge_count = 0;

    static void capture_handler(int signo, siginfo_t *info, void *context)
    {
      edge_count++;
    }

    int main(int argc, char *argv[])
    {
      int fd;
      struct cap_notify_s notify;
      struct sigaction sa;
      uint32_t frequency;
      uint8_t duty;

      /* 设置信号处理程序 */
      sa.sa_sigaction = capture_handler;
      sa.sa_flags = SA_SIGINFO;
      sigemptyset(&sa.sa_mask);
      sigaction(SIGUSR1, &sa, NULL);

      /* 打开捕获设备 */
      fd = open("/dev/capture0", O_RDONLY);
      if (fd < 0)
        {
          perror("Failed to open capture device");
          return 1;
        }

      /* 配置通道 0 双边沿通知 */
      notify.chan = 0;
      notify.type = CAP_TYPE_BOTH;
      notify.event.sigev_notify = SIGEV_SIGNAL;
      notify.event.sigev_signo = SIGUSR1;
      notify.event.sigev_value.sival_ptr = NULL;

      if (ioctl(fd, CAPIOC_REGISTER, (unsigned long)&notify) < 0)
        {
          perror("Failed to register notification");
          close(fd);
          return 1;
        }

      printf("Waiting for capture events...\n");

      /* 等待一些事件 */
      sleep(2);

      /* 获取频率和占空比 */
      ioctl(fd, CAPIOC_FREQUENCY, (unsigned long)&frequency);
      ioctl(fd, CAPIOC_DUTYCYCLE, (unsigned long)&duty);

      printf("Captured %d edges\n", edge_count);
      printf("Frequency: %u Hz, Duty: %u%%\n", frequency, duty);

      /* 注销通知 */
      ioctl(fd, CAPIOC_UNREGISTER, 0);

      close(fd);
      return 0;
    }

假捕获测试示例
-----------------------------

假捕获驱动程序可用于无硬件测试（需要 ``CONFIG_FAKE_CAPTURE``）：

.. code-block:: c

    #include <stdio.h>
    #include <fcntl.h>
    #include <sys/ioctl.h>
    #include <nuttx/timers/capture.h>

    int main(int argc, char *argv[])
    {
      int fd;
      uint32_t frequency;
      uint8_t duty;

      /* 打开假捕获设备 */
      fd = open("/dev/fake_capture0", O_RDONLY);
      if (fd < 0)
        {
          perror("Failed to open fake capture device");
          return 1;
        }

      /* 开始捕获 */
      ioctl(fd, CAPIOC_START, 0);

      /* 等待捕获稳定 */
      sleep(1);

      /* 读取值（应为 10Hz，50% 占空比） */
      ioctl(fd, CAPIOC_FREQUENCY, (unsigned long)&frequency);
      ioctl(fd, CAPIOC_DUTYCYCLE, (unsigned long)&duty);

      printf("Fake Capture - Frequency: %u Hz, Duty: %u%%\n",
             frequency, duty);

      /* 停止捕获 */
      ioctl(fd, CAPIOC_STOP, 0);

      close(fd);
      return 0;
    }

注意事项
-----

* 支持的实际 ``ioctl`` 命令集可能因硬件和驱动程序实现而异。
* ``CAPIOC_FREQUENCY`` 宏名称保留用于兼容性，即使 "frequency" 是正确的英文拼写。
* 始终检查 ``ioctl()`` 调用的返回值以进行错误处理。
* **重要：** 在 NuttX 的调试构建中，调用不支持的 ``ioctl`` 命令将在驱动程序中触发 ``DEBUGASSERT``，这将导致系统停止或崩溃。

信号通知功能
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

当启用 ``CONFIG_CAPTURE_NOTIFY`` 时：

* 应用程序可以注册异步边沿事件通知
* 支持具有独立配置的每通道注册
* 支持的边沿类型：上升沿（``CAP_TYPE_RISING``）、下降沿（``CAP_TYPE_FALLING``）或双边沿（``CAP_TYPE_BOTH``）
* 每个通道同时只能有一个任务注册
* 信号通知使用标准 POSIX ``sigevent`` 机制
* 下半部分驱动程序必须实现 ``bind()`` 和 ``unbind()`` 操作
* 适用于事件驱动的应用程序，如转速计、编码器和频率计数器

假捕获驱动程序
~~~~~~~~~~~~~~~~~~~

假捕获驱动程序（``CONFIG_FAKE_CAPTURE``）提供：

* 使用看门狗定时器的捕获事件软件模拟
* 固定 10Hz 频率，50% 占空比
* 每 50ms 边沿切换一次（上升沿和下降沿）
* 支持所有标准捕获操作，包括通知
* 可在 ``/dev/fake_capture0``、``/dev/fake_capture1`` 等访问
* 适用于无硬件的开发、测试和 CI/CD
* 平台无关的实现
* 启动时自动初始化（默认 2 个通道）

限制：

* 固定时序参数（运行时不可配置）
* 软件时序精度（非硬件精度）
* 适用于功能测试，不适用于时序精度验证
