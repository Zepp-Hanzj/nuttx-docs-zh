========================
``mqttc`` MQTT-C 示例
========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是一个使用 MQTT-C 的简单 MQTT 发布者示例。

默认情况下，它发布到 "test" 主题并退出。默认行为（包括主机、端口、主题、消息和循环计数）
可以通过不同的参数进行更改。

纯 TCP（无 Mbed TLS）
=======================

测试方法：
在主机上启动 MQTT 代理并订阅 "test" 主题。这里使用 mosquitto::

  mosquitto&
  mosquitto_sub -t test

确保 mosquitto 未配置为仅本地模式。

从 nsh：

启动内置应用程序 ``mqttc_pub`` 并指定主机::

  mqttc_pub -h HOST

目标将发布消息 "test"。

使用 Mbed TLS 的 TLS
=================

要使用 TLS，请在 ``menuconfig`` 中启用 Mbed TLS 和支持 Mbed TLS 的 MQTT-C
（参见 :doc:`../../netutils/mqttc/index`）。同一个 ``mqttc_pub`` 二进制文件支持 TLS 构建；
默认端口变为 **8883**。您可以传递 ``-c`` 并指定 PEM 格式的代理 CA 证书路径。

有关完整的配置符号、CLI 选项和单独的 ``mqttc_mbedtls_pub`` 示例，
请参见 :doc:`../../netutils/mqttc/index`。
