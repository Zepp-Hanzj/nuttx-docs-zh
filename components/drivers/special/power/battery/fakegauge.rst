==============
电池电量计
===============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 的电池电量计驱动，用于在生产环境中为充电器和 healthd 测量电池数据（电压、电流、容量、温度和充电状态）。

Fake Gauge
==========

NuttX 的模拟电池电量计驱动，用于测试和开发目的，模拟电池数据（电压、电流、容量、温度和充电状态）。它无需实际电池硬件即可提供模拟电池数据。它在预定义范围内生成随机值并定期更新，适用于：

  - 测试电池监控应用程序
  - 开发电源管理功能
  - 在没有实际硬件的情况下调试电池相关逻辑

特性
========

Fake Gauge 模拟关键电池参数。

  电压 (mV)：
  - 电压范围：4000mV 至 4200mV

  电流 (mA)：
  - 电流范围：-100mA 至 500mA
  - 电流分辨率：1mA

  容量 (%)：
  - 容量范围：0% 至 100%
  - 容量分辨率：1%

  温度 (0.1°C)：
  - 温度分辨率：0.1°C

  充电状态：
  - 充电中
  - 放电中
  - 未充电

  周期性数据更新（默认：5 秒）
  兼容 NuttX 电池电量计框架。


使用
=====

  文件信息
  - 路径：drivers/power/battery/battery_fakegauge.c
  - 许可证：Apache License 2.0

  依赖
  - NuttX 操作系统
  - NuttX 电池电量计框架 (nuttx/power/battery_gauge.h)
  - NuttX 工作队列用于周期性更新

  配置
  - 在 NuttX 配置文件中启用 fake gauge 驱动 (CONFIG_BATTERY_FAKEGAUGE=y)
  - 以秒为单位配置更新间隔 (CONFIG_BATTERY_FAKEGAUGE_UPDATE_INTERVAL)

此驱动仅用于开发和测试，不适用于实际电池的生产环境。
