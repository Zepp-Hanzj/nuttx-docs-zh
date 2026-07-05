==========================================
``paho_mqtt`` Eclipse Paho MQTT C 库
==========================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``paho_mqtt`` 包将 Eclipse Paho MQTT C 库集成到 NuttX 中。该库提供 MQTT 客户端功能，支持 MQTT 协议版本 3.1、3.1.1 和 5.0。该包包括用于程序化访问的库和用于发布和订阅 MQTT 主题的命令行工具。

概述
========

Eclipse Paho MQTT C 库是 MQTT 协议的客户端实现。它提供同步和异步 API，用于连接到 MQTT 代理、发布消息和订阅主题。

此 NuttX 集成包括：

- **MQTT 5.0 客户端库**（``LIB_MQTT5``）：通过 C API 调用提供 MQTT 客户端功能的库。

- **命令行工具**（``UTILS_MQTT5``）：
  - ``mqtt_pub``：用于向 MQTT 主题发布消息的工具
  - ``mqtt_sub``：用于订阅 MQTT 主题和接收消息的工具

如果尚未存在，库将在构建过程中自动从 Eclipse Paho GitHub 仓库下载。

配置
=============

库配置
---------------------

启用 MQTT 5.0 库：

.. code-block:: kconfig

   CONFIG_LIB_MQTT5=y

工具配置
---------------------

启用 MQTT 命令行工具：

.. code-block:: kconfig

   CONFIG_UTILS_MQTT5=y
   CONFIG_UTILS_MQTT5_PRIORITY=100
   CONFIG_UTILS_MQTT5_STACKSIZE=16384

配置选项
---------------------

- ``CONFIG_LIB_MQTT5``：启用 MQTT 5.0 客户端库
- ``CONFIG_UTILS_MQTT5``：启用 MQTT 命令行工具（需要 ``CONFIG_LIB_MQTT5``）
- ``CONFIG_UTILS_MQTT5_PRIORITY``：MQTT 工具的任务优先级（默认：100）
- ``CONFIG_UTILS_MQTT5_STACKSIZE``：MQTT 工具的堆栈大小（默认：16384）

用法
=====

mqtt_pub - 发布消息
----------------------------

``mqtt_pub`` 工具向 MQTT 主题发布消息。

mqtt_pub 语法
~~~~~~~~~~~~~~~

.. code-block:: bash

   mqtt_pub [topicname] [options]

mqtt_pub 选项
~~~~~~~~~~~~~~~~

连接选项：
  - ``-h, --host <host>``：MQTT 代理主机名（默认：localhost）
  - ``-p, --port <port>``：网络端口（默认：1883）
  - ``-c, --connection <url>``：连接字符串（覆盖 host/port）
  - ``-i, --clientid <id>``：客户端 ID（默认：paho-c-pub）
  - ``-u, --username <user>``：认证用户名
  - ``-P, --password <pass>``：认证密码
  - ``-k, --keepalive <seconds>``：保活超时（默认：10）

消息选项：
  - ``-t, --topic <topic>``：要发布到的 MQTT 主题
  - ``-m, --message <message>``：要发送的消息负载
  - ``-f, --filename <file>``：从文件读取消息
  - ``-q, --qos <0|1|2>``：服务质量级别（默认：0）
  - ``-r, --retained``：设置保留消息标志
  - ``-n, --null-message``：发送零长度消息

MQTT 版本：
  - ``-V, --MQTTversion <31|311|5>``：MQTT 协议版本（默认：311）

mqtt_pub 示例
~~~~~~~~~~~~~~~~~

发布简单消息：

.. code-block:: bash

   mqtt_pub -h 192.168.1.100 -t "test/topic" -m "Hello MQTT"

使用 QoS 1 和保留标志发布：

.. code-block:: bash

   mqtt_pub -h 192.168.1.100 -t "test/topic" -m "Retained message" -q 1 -r

从文件发布：

.. code-block:: bash

   mqtt_pub -h 192.168.1.100 -t "test/topic" -f message.txt

mqtt_sub - 订阅主题
-------------------------------

``mqtt_sub`` 工具订阅 MQTT 主题并接收消息。

mqtt_sub 语法
~~~~~~~~~~~~~~~

.. code-block:: bash

   mqtt_sub [topicname] [options]

mqtt_sub 选项
~~~~~~~~~~~~~~~~

连接选项：
  - ``-h, --host <host>``：MQTT 代理主机名（默认：localhost）
  - ``-p, --port <port>``：网络端口（默认：1883）
  - ``-c, --connection <url>``：连接字符串（覆盖 host/port）
  - ``-i, --clientid <id>``：客户端 ID（默认：paho-c-sub）
  - ``-u, --username <user>``：认证用户名
  - ``-P, --password <pass>``：认证密码
  - ``-k, --keepalive <seconds>``：保活超时（默认：10）

订阅选项：
  - ``-t, --topic <topic>``：要订阅的 MQTT 主题（支持通配符）
  - ``-q, --qos <0|1|2>``：服务质量级别（默认：0）
  - ``-R, --no-retained``：不打印保留消息
  - ``--no-delimiter``：不在消息之间使用分隔符
  - ``--delimiter <string>``：自定义分隔符（默认：\\n）

MQTT 版本：
  - ``-V, --MQTTversion <31|311|5>``：MQTT 协议版本（默认：311）

主题通配符
~~~~~~~~~~~~~~~

- ``+``：单级通配符（匹配一个主题级别）
  - 示例：``sensor/+/temperature`` 匹配 ``sensor/room1/temperature``
- ``#``：多级通配符（匹配多个级别，必须在末尾）
  - 示例：``sensor/#`` 匹配 ``sensor/`` 下的所有主题

mqtt_sub 示例
~~~~~~~~~~~~~~~~~

订阅主题：

.. code-block:: bash

   mqtt_sub -h 192.168.1.100 -t "test/topic"

使用通配符订阅：

.. code-block:: bash

   mqtt_sub -h 192.168.1.100 -t "sensor/#"

使用 QoS 1 订阅：

.. code-block:: bash

   mqtt_sub -h 192.168.1.100 -t "test/topic" -q 1

库 API
===========

MQTT 5.0 库提供同步和异步 API。主要头文件为：

- ``MQTTAsync.h``：异步 MQTT 客户端 API
- ``MQTTClient.h``：同步 MQTT 客户端 API

有关详细的 API 文档，请参阅 Eclipse Paho MQTT C 库文档：https://www.eclipse.org/paho/clients/c/。
