====================
FOC 驱动程序接口
====================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

磁场定向控制（FOC）是控制同步或异步交流电机的常用技术。FOC 的主要目标是控制供电设备中的直轴电流（Id）和交轴电流（Iq）。

内核端设备负责以下工作：

#. 更新 PWM 占空比
#. 返回 ADC 电流采样
#. 将用户空间与 PWM 事件同步

NuttX FOC 驱动程序分为两部分：

#. "上半部分"，通用驱动程序，为应用程序代码提供通用 FOC 接口，
#. "下半部分"，平台特定的驱动程序，实现 FOC 功能的底层逻辑。

支持 FOC 的文件可以在以下位置找到：

-  ``include/nuttx/motor/foc/foc.h``。
   用户空间可用的"上半部分" FOC 接口。
-  ``include/nuttx/motor/foc/foc_lower.h``。
   "下半部分" FOC 接口。
-  ``drivers/motor/foc/foc_dev.c``。
   通用的"上半部分" FOC 驱动程序。
-  ``drivers/motor/foc/foc_pwr.c``。
   FOC 的通用功率级。

应用程序可用的大部分功能通过驱动程序的 ioctl 调用实现。支持的 ioctl 命令：

- ``MTRIOC_START`` - 启动 FOC 设备，参数：无。
- ``MTRIOC_STOP`` - 停止 FOC 设备，参数：无。
- ``MTRIOC_GET_STATE`` - 获取 FOC 设备状态，
  参数：``struct foc_state_s`` 指针。
  这是一个阻塞操作，用于将用户空间应用程序与 ADC 采样同步。
- ``MTRIOC_CLEAR_FAULT`` - 清除 FOC 设备故障状态，
  参数：无。
- ``MTRIOC_SET_PARAMS`` - 设置 FOC 设备操作参数，
  参数：``struct foc_params_s`` 指针。
- ``MTRIOC_SET_CONFIG`` - 设置 FOC 设备配置，
  参数：``struct foc_cfg_s`` 指针。
- ``MTRIOC_GET_INFO`` - 获取 FOC 设备信息，
  参数：``struct foc_info_s`` 指针。

此外，板级逻辑可以实现：

- ``MTRIOC_SET_BOARDCFG`` - 返回板级特定的 FOC 配置
- ``MTRIOC_GET_BOARDCFG`` - 设置板级特定的 FOC 配置
