=================
Thermal Framework
=================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

Thermal Framework 是内核中的一个子系统，为设备的热管理提供接口。它旨在监控各种组件的温度并调整其工作条件以防止过热。该框架负责控制冷却设备（如风扇和散热器）以将温度保持在安全范围内。它提供了一个统一的热管理接口，可供不同的热驱动使用。驱动可由硬件供应商实现以支持其特定的热管理需求。

简介
=====
1. 支持 Zone、Cooling Device 和 Governor
    - ``Zone``：负责监控指定区域的温度，通过温度传感器获取温度，传感器驱动通过回调函数返回温度。
    - ``Cooling Device``：冷却设备是一种可以使用 cpufreq、风扇等资源来降低温度的设备。预置了 cpufreq 冷却设备驱动以简化 CPU 调频温控。
    - ``Governor``：用于温控，可以使用预置的或自定义注册的，预置的 "step_wise" governor：
        - 当 "Zone" 的温度达到温度跳变点，且温度变化趋势上升或稳定（"step_wise" 每 20ms 获取一次对应 "Zone" 的值 [``CONFIG_THERMAL_DUMMY_POLLING_DELAY=200``，``CONFIG_USEC_PER_TICK=100``]，当前温度等于或大于上次获取的温度值），则提升 "Cooling Device" 的状态（通过 ``set_state`` 触发对应状态执行的冷却操作）。
        - 当 zone 的温度低于温度跳变点，且温度趋势稳定下降时，降低 "Cooling Device" 的状态。

#. 支持三种类型的温度跳变点：``THERMAL_NORMAL``、``THERMAL_HOT`` 和 ``THERMAL_CRITICAL``
    - ``NORMAL``：当设备温度达到此跳变点的温度时，需要启动控制。如果当前温度等于上次获取的温度，则保持温控级别（"cooling state"）。当大于时，"cooling state" 增加。
    - ``HOT``：当设备温度达到此跳变点时，需要更严格的温控（如资源限制）。如果当前温度等于或大于上次获取的温度，则温控级别增加。
    - ``CRITICAL``：关闭/重启设备。

#. 支持 ProcFS 节点，用于调试，可以获取 "Zone"、"Cooling Device"、"Trip" 和 "Governor" 之间的绑定信息、温度值和冷却状态；（例如，"Zone Device"（温度传感器）：``/proc/thermal/cpu_thermal``），写入 0 或 1 可关闭或开启 "Zone Device"；

设备驱动
=============
1. 冷却设备
    设备提供者应提供 ``struct thermal_cooling_device_ops_s`` 实例和私有数据（可选，例如 ``struct dummy_cooling_device_s``）。请参考 drivers/thermal/thermal_dummy.c::

      static const struct thermal_cooling_device_ops_s g_dummy_fan0_ops =
      {
        .set_state     = dummy_cdev_set_state,
        .get_state     = dummy_cdev_get_state,
        .get_max_state = dummy_cdev_get_max_state,
      };

      static struct dummy_cooling_device_s g_dummy_fan0_data =
      {
        .cur_state = 0,
        .max_state = 16,
      };

      int thermal_dummy_init(void)
      {
        FAR struct thermal_cooling_device_s *cdev;
        FAR struct thermal_zone_device_s *zdev;
        ...

        /* Cooling Device */
        cdev = thermal_cooling_device_register("fan0", &g_dummy_fan0_data,
                                               &g_dummy_fan0_ops);
        ...
      }

#. Zone 设备
    需要定义以下实例：
        - ``struct thermal_zone_device_ops_s``：获取温度，设置温度窗口（可选）
        - ``struct thermal_zone_params_s``：描述 zone、governor 和 cooling-maps
        - ``dummy_zone_device_s``（私有，可选）：用于温度和趋势

    例如，drivers/thermal/thermal_dummy.c::

      /* Zone Device */
      zdev = thermal_zone_device_register("cpu-thermal", &g_dummy_zone,
                                          &g_dummy_zone_ops, &g_dummy_params);

      static const struct thermal_zone_device_ops_s g_dummy_zone_ops =
      {
        .get_temp  = dummy_zdev_get_temp,
        .set_trips = dummy_zdev_set_trips,
      };

      static struct dummy_zone_device_s g_dummy_zone =
      {
        .temperature = 45,
        .raising = true,
      };

#. 测试/调试
    - 禁用 Zone Device：``echo 0 > /proc/thermal/cpu-thermal``
    - 获取绑定信息::

        nsh> cat /proc/thermal/cpu-thermal
        z:cpu-thermal t:77 t:1 h:16 l:0 c:fan0 s:7|7
        z:cpu-thermal t:77 t:1 h:3 l:3 c:cpufreq s:3|3
        z:cpu-thermal t:77 t:2 h:2 l:0 c:cpufreq s:3|2

板级定制
===================
Trip、Cooling Device、Governor 和 Zone 之间的绑定关系在 thermal_dummy.c 中展示。预期供应商适配器将在 ``CONFIG_ARCH_BOARD_CUSTOM_DIR`` 下提供与硬件相关的初始化以进行产品定制，如以下注释和结构所述：
::

  /* thermal-zones {
   *   "cpu-thermal" {
   *     polling-delay : CONFIG_THERMAL_DUMMY_POLLING_DELAY;
   *     passive-delay : CONFIG_THERMAL_DUMMY_PASSIVE_DELAY;
   *     governor      : "step_wise";
   *
   *     trips {
   *       "cpu_crit"   { 90, 10, THERMAL_CRITICAL };
   *       "cpu_alert1" { 70, 10, THERMAL_HOT };
   *       "cpu_alert0" { 60, 10, THERMAL_NORMAL };
   *     };
   *
   *     cooling-maps {
   *       "cpu_alert0" {
   *         { "cpu0", THERMAL_NO_LIMIT, 3 };
   *       };
   *       "cpu_alert1" {
   *         { "cpu0", THERMAL_NO_LIMIT, 3 };
   *         { "fan0", THERMAL_NO_LIMIT, THERMAL_NO_LIMIT };
   *       };
   *       "cpu_crit" {
   *         { NULL, THERMAL_NO_LIMIT, THERMAL_NO_LIMIT };
   *       };
   *     };
   *   };
   * };
   */

  static const struct thermal_zone_trip_s g_dummy_trips[] =
  {
    {.name = "cpu_crit",   .temp = 90, .hyst = 10, .type = THERMAL_CRITICAL},
    {.name = "cpu_alert1", .temp = 70, .hyst = 10, .type = THERMAL_NORMAL},
    {.name = "cpu_alert0", .temp = 60, .hyst = 10, .type = THERMAL_NORMAL},
  };

  static const struct thermal_zone_map_s g_dummy_maps[] =
  {
    {
      .trip_name = "cpu_alert1",
      .cdev_name = "cpufreq",
      .low    = 3,
      .high   = THERMAL_NO_LIMIT,
      .weight = 20
    },
    {
      .trip_name = "cpu_alert1",
      .cdev_name = "fan0",
      .low    = THERMAL_NO_LIMIT,
      .high   = THERMAL_NO_LIMIT,
      .weight = 20
    },
    {
      .trip_name = "cpu_alert0",
      .cdev_name = "cpufreq",
      .low    = THERMAL_NO_LIMIT,
      .high   = 2,
      .weight = 20
    },
  };

  static const struct thermal_zone_params_s g_dummy_params =
  {
    .gov_name = "step_wise",
    .polling_delay = CONFIG_THERMAL_DUMMY_POLLING_DELAY,
    .trips = g_dummy_trips,
    .num_trips = nitems(g_dummy_trips),
    .maps = g_dummy_maps,
    .num_maps = nitems(g_dummy_maps),
  };
