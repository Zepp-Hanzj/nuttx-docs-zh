=========================================
``mbedtls`` Mbed TLS 加密库
=========================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 可以从 ``nuttx-apps``（位于 ``apps/crypto/mbedtls`` 下）构建 Mbed TLS 加密库。
在 ``menuconfig`` 中启用 ``CONFIG_CRYPTO_MBEDTLS`` 并根据需要选择应用程序选项。

Mbed TLS 通常用于 NuttX 上的 TLS 客户端和服务器。对于使用 MQTT-C 集成的
MQTT over TLS，请启用 ``CONFIG_CRYPTO_MBEDTLS`` 和
``CONFIG_NETUTILS_MQTTC_WITH_MBEDTLS``；参见 :doc:`../../netutils/mqttc/index`。
