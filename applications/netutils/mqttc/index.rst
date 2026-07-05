========================
``mqttc`` MQTT-C 库
========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

概述
========

`MQTT-C <https://github.com/LiamBindle/MQTT-C>`_ 客户端库通过 ``nuttx-apps``（``apps/netutils/mqttc``）集成到 NuttX 中。它提供了一个具有小型平台抽象层的 MQTT v3.1.1 客户端。

您可以通过纯 TCP 使用 MQTT-C，或者在启用 TLS 的情况下使用 Mbed TLS。TLS 路径为包含库的代码和 ``examples/mqttc`` 发布者应用程序定义了 ``MQTT_USE_MBEDTLS``。

先决条件
=============

- NuttX 代码树和匹配的 ``nuttx-apps`` 检出版本（请参阅每个仓库中的顶层 ``README``）。
- 工作网络栈和到 MQTT 代理的路由（以太网、Wi-Fi 或其他），除非您仅在主机上运行回环测试。
- 对于带证书验证的 TLS，请确保设备在连接前具有有效的时钟（RTC 或 NTP）；否则 ``notBefore`` / ``notAfter`` 的验证可能会失败。

配置
=============

从 ``menuconfig`` 启用 MQTT-C 包和可选组件：

**库和 TLS**

- ``CONFIG_NETUTILS_MQTTC``：构建 MQTT-C 静态库。
- ``CONFIG_CRYPTO_MBEDTLS``：构建 Mbed TLS（TLS 集成所需）。
- ``CONFIG_NETUTILS_MQTTC_WITH_MBEDTLS``：使用 ``MQTT_USE_MBEDTLS`` 编译 MQTT-C 和依赖的应用程序。此选项依赖于 ``CRYPTO_MBEDTLS`` 并选择 ``DEV_URANDOM`` 作为熵源。
- ``CONFIG_NETUTILS_MQTTC_VERSION``：上游 MQTT-C 版本字符串（默认为 ``1.1.5``）。

**示例：``mqttc_pub``（``apps/examples/mqttc``）**

- ``CONFIG_EXAMPLES_MQTTC``：构建 NSH 发布者示例。程序名称为 ``CONFIG_EXAMPLES_MQTTC_PROGNAME``（默认为 ``mqttc_pub``）。需要 ``NETUTILS_MQTTC``。
- ``CONFIG_EXAMPLES_MQTTC_ALLOW_UNVERIFIED_TLS``：如果 TLS 验证失败，仍然继续。适用于使用自签名代理的开发；不要在生产环境中依赖此选项。

**捆绑的上游示例（``apps/netutils/mqttc``）**

- ``CONFIG_NETUTILS_MQTTC_EXAMPLE``：从 MQTT-C 代码树构建额外的示例程序。启用 Mbed TLS 时生成 ``mqttc_mbedtls_pub``；否则生成 ``mqttc_posix_pub`` 和 ``mqttc_posix_sub``。
- ``CONFIG_NETUTILS_MQTTC_TEST``：基于 CMocka 的测试。当 ``CONFIG_NETUTILS_MQTTC_WITH_MBEDTLS`` 启用时，此选项不可用。

启用 TLS 的 ``mqttc_pub`` 的最小 ``kconfig`` 片段如下：

.. code-block:: kconfig

   CONFIG_CRYPTO_MBEDTLS=y
   CONFIG_NETUTILS_MQTTC=y
   CONFIG_NETUTILS_MQTTC_WITH_MBEDTLS=y
   CONFIG_EXAMPLES_MQTTC=y

使用 Mbed TLS 的 ``mqttc_pub``
=================================

当设置了 ``CONFIG_NETUTILS_MQTTC_WITH_MBEDTLS`` 时，``mqttc_pub`` 使用 Mbed TLS 进行代理连接。默认代理端口为 **8883**（TLS）。典型参数：

.. code-block:: text

   mqttc_pub -h BROKER [-p PORT] [-c CAFILE] [-t TOPIC] [-m MESSAGE] [-n COUNT] [-q QOS]

- ``-h``：代理主机名或地址（非默认使用时必需）。
- ``-p``：端口（TLS 模式下默认为 ``8883``）。
- ``-c``：包含代理 CA 证书（或证书链）的 PEM 文件路径。如果省略，示例使用嵌入式测试 CA（PolarSSL/Mbed TLS 测试材料），仅适用于匹配的测试服务器——不适用于任意的生产代理。
- ``-t``、``-m``、``-n``、``-q``：主题、负载、发布重复次数和服务质量。

示例（NSH，网络启动后）：

.. code-block:: text

   nsh> mqttc_pub -h mqtt.example.com -p 8883 -c /etc/ssl/certs/broker-ca.pem

如果验证失败且您必须在启动期间使用自签名代理，请启用 ``CONFIG_EXAMPLES_MQTTC_ALLOW_UNVERIFIED_TLS`` 或修复设备上的 CA/时间。

使用 ``mqttc_mbedtls_pub``
===========================

当设置了 ``CONFIG_NETUTILS_MQTTC_EXAMPLE`` 和 ``CONFIG_NETUTILS_MQTTC_WITH_MBEDTLS`` 时，``mqttc_mbedtls_pub`` 程序从上游 ``examples/mbedtls_publisher.c`` 构建。它接受位置参数：

.. code-block:: text

   mqttc_mbedtls_pub CAFILE [ADDRESS [PORT [TOPIC]]]

默认值与上游示例类似（例如，如果未覆盖，使用公共测试代理和端口 ``8883``）。使用与您的代理匹配的 CA 文件。

构建系统（Make 和 CMake）
==============================

基于 Make 和基于 CMake 的 NuttX 构建都支持这些选项。对于 CMake，请确保 Mbed TLS 和 MQTT-C 目标解析包含路径和依赖关系；最近的 ``nuttx-apps`` 更改在两个 TLS 选项都启用时将 ``mqttc`` 连接到 ``mbedtls``。

另请参阅
========

- :doc:`../../examples/mqttc/index` — ``mqttc_pub`` 的快速测试步骤。
- :doc:`../../crypto/mbedtls/index` — Mbed TLS 包概述。
- :doc:`../paho_mqtt/index` — Eclipse Paho MQTT C 客户端（替代方案）。
