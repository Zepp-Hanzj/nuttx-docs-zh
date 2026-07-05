============================
``vconfig`` VLAN 配置工具
============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

vconfig 是一个用于管理 NuttX 中 VLAN（虚拟局域网）接口的工具。它允许用户在网络上添加、删除和显示 VLAN。

用法
-----

使用方法很简单::

    nsh> help ; vconfig
    Usage: vconfig add <interface> <vlan_id> [priority]
           vconfig rem|del <vlan-interface>

示例
~~~~~~~~

添加 VLAN 接口::

    nsh> vconfig add eth0 10

删除 VLAN 接口::

    nsh> vconfig rem|del eth0.10

资源
~~~~~~~~~

* https://en.wikipedia.org/wiki/Virtual_LAN
* https://www.nuttx.org/


