.. |br| raw:: html

   <br/>

======================
配置设置
======================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

上述命令的可用性取决于 NuttX 配置文件中可能启用或未启用的功能。
以下 :ref:`命令表 <nxdiagcmddependencies>` 指示了每个命令对 NuttX 配置设置的依赖关系。
通用配置设置在 NuttX 移植指南中讨论。
Nxdiag 特定的配置设置在本文档的 :ref:`底部 <nxdiagconfiguration>` 讨论。

请注意，``--vendor-specific`` 或 ``-v`` 选项将生成特定于供应商的信息和检查。
此选项的输出将取决于 NuttX 配置文件中选择的供应商。例如，如果启用了
``CONFIG_SYSTEM_NXDIAG_ESPRESSIF`` 配置设置，则此选项将提供 Espressif 设备的
自定义信息和检查。可以同时选择多个供应商。

.. _nxdiagcmddependencies:

选项对配置设置的依赖
=============================================

========================= ===========================================
选项                        依赖的配置
========================= ===========================================
``--help, -h``
``--nuttx, -n``
``--flags, -f``           ``CONFIG_SYSTEM_NXDIAG_COMP_FLAGS``
``--config, -c``          ``CONFIG_SYSTEM_NXDIAG_CONF``
``--host-os, -o``
``--host-path, -p``       ``CONFIG_SYSTEM_NXDIAG_HOST_PATH``
``--host-packages, -k``   ``CONFIG_SYSTEM_NXDIAG_HOST_PACKAGES``
``--host-modules, -m``    ``CONFIG_SYSTEM_NXDIAG_HOST_MODULES``
``--vendor-specific, -v``
``--all``

========================= ===========================================

.. _nxdiagconfiguration:

Nxdiag 特定配置设置
======================================

Nxdiag 的行为可以通过 ``boards/<arch>/<chip>/<board>/defconfig`` 文件中的以下设置进行修改：

========================================  ==================================
配置                                      描述
========================================  ==================================
 ``CONFIG_SYSTEM_NXDIAG_COMP_FLAGS``      启用 nxdiag 应用程序以列出 NuttX 编译
                                          标志。这对于调试主机和目标系统非常有用。
                                          启用 ``-f`` 和 ``--nuttx-flags`` 选项。

 ``CONFIG_SYSTEM_NXDIAG_CONF``            启用 nxdiag 应用程序以列出用于编译 NuttX
                                          的配置选项。这对于调试主机和目标系统非常有用。
                                          启用 ``-c`` 和 ``--nuttx-config`` 选项。

 ``CONFIG_SYSTEM_NXDIAG_HOST_PATH``       启用 nxdiag 应用程序以列出主机系统 PATH
                                          环境变量。这对于调试主机系统非常有用。
                                          启用 ``-p`` 和 ``--host-path`` 选项。

 ``CONFIG_SYSTEM_NXDIAG_HOST_PACKAGES``   启用 nxdiag 应用程序以列出主机系统上
                                          已安装的软件包。这对于调试主机系统非常有用。
                                          启用 ``-k`` 和 ``--host-packages`` 选项。

 ``CONFIG_SYSTEM_NXDIAG_HOST_MODULES``    启用 nxdiag 应用程序以列出主机系统上
                                          已安装的 Python 模块。这对于调试主机系统
                                          非常有用。启用 ``-m`` 和 ``--host-modules`` 选项。

 ``CONFIG_SYSTEM_NXDIAG_ESPRESSIF``       启用 Espressif 特定的信息和检查。

========================================  ==================================
