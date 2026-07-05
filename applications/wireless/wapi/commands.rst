========
Commands
========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

此页面显示 ``wapi`` 命令、其参数和输出。要获取系统中可用的完整 ``wapi``
命令列表，只需运行 ``wapi``::

    nsh> wapi
    Usage:
            wapi show         <ifname>
            wapi scan         <ifname>
            wapi scan_results <ifname>
            wapi ip           <ifname> <IP address>
            wapi mask         <ifname> <mask>
            wapi freq         <ifname> <frequency>  <index/flag>
            wapi essid        <ifname> <essid>      <index/flag>
            wapi psk          <ifname> <passphrase> <index/flag> <wpa>
            wapi disconnect   <ifname>
            wapi mode         <ifname>              <index/mode>
            wapi ap           <ifname>              <MAC address>
            wapi bitrate      <ifname> <bitrate>    <index/flag>
            wapi txpower      <ifname> <txpower>    <index/flag>
            wapi country      <ifname> <country code>
            wapi sense        <ifname>
            wapi pta_prio     <ifname>  <index/flag>
            wapi help

    Frequency Flags:
            [0] WAPI_FREQ_AUTO
            [1] WAPI_FREQ_FIXED

    ESSID Flags:
            [0] WAPI_ESSID_OFF
            [1] WAPI_ESSID_ON

    Passphrase algorithm Flags:
            [0] WPA_ALG_NONE
            [1] WPA_ALG_WEP
            [2] WPA_ALG_TKIP
            [3] WPA_ALG_CCMP

    Passphrase WPA version:
            [0] WPA_VER_NONE
            [1] WPA_VER_1
            [2] WPA_VER_2
            [3] WPA_VER_3

    Operating Modes:
            [0] WAPI_MODE_AUTO
            [1] WAPI_MODE_ADHOC
            [2] WAPI_MODE_MANAGED
            [3] WAPI_MODE_MASTER
            [4] WAPI_MODE_REPEAT
            [5] WAPI_MODE_SECOND
            [6] WAPI_MODE_MONITOR
            [7] WAPI_MODE_MESH

    Bitrate Flags:
            [0] WAPI_BITRATE_AUTO
            [1] WAPI_BITRATE_FIXED

    TX power Flags:
            [0] WAPI_TXPOWER_DBM
            [1] WAPI_TXPOWER_MWATT
            [2] WAPI_TXPOWER_RELATIVE

    pta prio Flags:
            [0] WAPI_PTA_PRIORITY_COEX_MAXIMIZED
            [1] WAPI_PTA_PRIORITY_COEX_HIGH
            [2] WAPI_PTA_PRIORITY_BALANCED
            [3] WAPI_PTA_PRIORITY_WLAN_HIGHD
            [4] WAPI_PTA_PRIORITY_WLAN_MAXIMIZED

参数
=========

命令的参数可在 ``wapi`` 的使用帮助中查看。

.. note:: ``<>`` 表示必需参数，``[]`` 表示可选参数。

以下是简要说明：

``<ifname>``
------------

接口名称取决于架构，通常为特定操作模式设置。例如，``wlan0`` 是用于 STA 模式的
接口，``wlan1`` 用于 SoftAP。

请参阅 :doc:`Supported Platforms </platforms/index>` 了解平台特定的定义。
例如，请查看 :ref:`ESP32 Wi-Fi Station Mode <esp32_wi-fi_sta>` 和
:ref:`ESP32 Wi-Fi SoftAP Mode <esp32_wi-fi_softap>` Wi-Fi 部分。

``<index/flag>``
----------------

``<index/flag>`` 可以使用数字或文本值。例如，对于 ``wapi psk`` 命令，可以
不加区分地使用::

    nsh> wapi psk wlan0 mypasswd 3
    nsh> wapi psk wlan0 mypasswd WPA_ALG_CCMP
