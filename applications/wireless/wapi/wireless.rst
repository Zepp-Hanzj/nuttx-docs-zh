==============================
Configuring a Wireless Network
==============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``wapi`` 通过设置接入点的参数来连接到接入点。

.. note:: 通常，单个无线接口对应一种操作模式：站点模式（STA）或 SoftAP。
   例如，``wlan0`` 可能对应 STA 模式，``wlan1`` 对应 SoftAP。为启用 STA 的
   接口设置密码和 ESSID 将使其连接到无线网络，而为启用 SoftAP 的接口设置相同
   参数将提供具有这些连接参数的无线网络。请查看
   :ref:`ESP32 Wi-Fi Station Mode (wlan0) <esp32_wi-fi_sta>` 和
   :ref:`ESP32 Wi-Fi SoftAP Mode (wlan1) <esp32_wi-fi_softap>` 部分。

设置密码
======================

``wapi psk`` 命令用于设置 AP 认证安全。其参数为::

   wapi psk <ifname> <passphrase> <index/flag> [wpa]

-  ``<ifname>`` 是设置为站点模式（STA）的接口名称；
-  ``<passphrase>`` 是密码。其长度取决于认证算法。请注意，``wapi psk`` 命令
   也用于设置开放认证，但此参数在后面，因此可能需要设置一个"虚拟"密码才能将认证
   设置为无；
-  ``<index/flag>`` 可以数字或文本方式设置，如下所示：

 -  [0] WPA_ALG_NONE - 连接到开放 AP；
 -  [1] WPA_ALG_WEP - 连接到 WEP 加密的 AP（不推荐）；
 -  [2] WPA_ALG_TKIP - 使用 TKIP 算法（不推荐）；
 -  [3] WPA_ALG_CCMP - 使用 CCMP 算法（推荐）；

-  ``[wpa]`` 设置 WPA 版本（如适用）：

 -  [0] WPA_VER_NONE；
 -  [1] WPA_VER_1；
 -  [2] WPA_VER_2（默认，如未另行选择）；
 -  [3] WPA_VER_3；

设置网络名称（ESSID）
================================

可以使用 ``wapi essid`` 命令设置无线网络的名称::

   wapi essid <ifname> <essid> <index/flag>

-  ``<ifname>`` 是设置为站点模式（STA）的接口名称；
-  ``<essid>`` 是无线网络的名称；
-  ``<index/flag>`` 选择是否连接到 AP：

 -  [0] WAPI_ESSID_OFF - 不连接到 AP；
 -  [1] WAPI_ESSID_ON - 连接到由提供的 ESSID 指示的 AP；
 -  [2] WAPI_ESSID_DELAY_ON - 延迟 AP 连接；

示例
========

连接到开放网络
-------------

::

   wapi psk wlan0 mypasswd WPA_ALG_NONE
   wapi essid wlan0 myssid WAPI_ESSID_ON

或等效地

::

   wapi psk wlan0 mypasswd 0
   wapi essid wlan0 myssid 1

连接到 WPA2-PSK 网络
--------------------------------

::

   wapi psk wlan0 mypasswd WPA_ALG_CCMP
   wapi essid wlan0 myssid WAPI_ESSID_ON

或等效地：

 ::

   wapi psk wlan0 mypasswd 3
   wapi essid wlan0 myssid 1

连接到 WPA3-SAE 网络
--------------------------------

::

   wapi psk wlan0 mypasswd WPA_ALG_CCMP WPA_VER_3
   wapi essid wlan0 myssid WAPI_ESSID_ON

或等效地：

 ::

   wapi psk wlan0 mypasswd 3 3
   wapi essid wlan0 myssid 1

连接到隐藏的（WPA2-PSK）网络
-----------------------------------------

::

   wapi psk wlan0 mypasswd WPA_ALG_CCMP
   wapi essid wlan0 myssid WAPI_ESSID_DELAY_ON
   wapi ap wlan0 aa:bb:cc:dd:dd:ff

或等效地：

 ::

   wapi psk wlan0 mypasswd 3
   wapi essid wlan0 myssid 2
   wapi ap wlan0 aa:bb:cc:dd:dd:ff
