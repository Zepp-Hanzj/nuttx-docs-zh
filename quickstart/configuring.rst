.. include:: /substitutions.rst
.. _configuring:

===========
配置
===========

Apache NuttX 高度可配置：几乎所有功能都可以被配置加入或移出系统。
这使得可以为您的硬件和应用程序编译定制化的构建。

Apache NuttX 配置系统使用 Linux 的
`kconfig 系统 <https://www.kernel.org/doc/Documentation/kbuild/kconfig-language.txt>`_，
包括各种前端，允许您轻松修改配置。通常使用 ``menuconfig``
前端，这是一个基于控制台的菜单系统（更多信息请参见 `这里 <https://en.wikipedia.org/wiki/Menuconfig>`_）。

正如之前在 :doc:`compiling_make` 中所解释的，第一步是为您的开发板
加载一个预制的配置。然后，您可以根据需要修改此配置。在本示例中，
我们将展示如何修改 ``sim`` 构建的默认配置——这是一个在您自己计算机上
运行的 NuttX 构建。

#. 初始化开发板配置

    .. code-block:: console

       $ cd nuttx
       $ ./tools/configure.sh -l sim:nsh
         Copy files
         Select CONFIG_HOST_LINUX=y
         Refreshing...
         
#. 构建并运行

    .. code-block:: console

       $ make clean
       $ make -j
       $ ./nuttx
       User Logged-in!
       nsh>

   您可以通过输入 ``help`` 或 ``?`` 来探索 nsh。然后要退出，可以运行：

    .. code-block:: console

       nsh> quit

#. 修改配置

   在本例中，我们将移除登录功能（这样将直接启动到命令提示符）。为此，
   我们使用 ``menuconfig`` 前端。

    .. code-block:: console

       $ make menuconfig

   您将看到如下界面：

   .. image:: ../_static/images/menuconfig.png
       :width: 800px
       :align: center
       :alt: menuconfig 系统主界面截图

   |br|

   NSH 登录设置位于 :menuselection:`Application Configuration --> NSH Library` 下。
   您可以使用 :kbd:`🢁` 和 :kbd:`🢃` 键导航，使用 :kbd:`↵` 进入子菜单。
   要禁用相应设置，请转到 :menuselection:`Console Login` 并按 :kbd:`空格键`
   （使其显示为空格而不是星号）。

   现在您需要退出 ``menuconfig`` 并保存修改后的配置。使用 :kbd:`🡸` 和
   :kbd:`🡺` 方向键导航底部菜单。如果选择 :menuselection:`Exit`，
   系统将提示您保存配置。

#. 使用新配置构建

    .. code-block:: console

       $ make

#. 运行

    .. code-block:: console

       $ ./nuttx
       NuttShell (NSH) NuttX-12.10.0

   成功！

.. tip::
   如果您觉得每日消息（MOTD）很烦人并想关闭它，它在
   :menuselection:`Application Configuration --> NSH Library --> Message of the Day (MOTD)` 中配置。
   
快速配置更改
==========================

如果您确切知道要更改哪个配置符号，可以使用 ``kconfig-tweak`` 工具（随 ``kconfig-frontends`` 软件包提供）来快速更改设置，无需进入配置前端。这对于更改调试选项等设置非常有用：

.. code-block:: console

   $ kconfig-tweak --disable CONFIG_DEBUG_NET
   $ make olddefconfig  # 需要让 kconfig 系统检查配置
   $ kconfig-tweak --enable CONFIG_DEBUG_NET
   $ make olddefconfig

这对于脚本化您经常执行的配置更改也很有用：

.. code-block:: bash

   #!/bin/bash

   kconfig-tweak --disable CONFIG_DEBUG_ALERT
   kconfig-tweak --disable CONFIG_DEBUG_FEATURES
   kconfig-tweak --disable CONFIG_DEBUG_ERROR
   kconfig-tweak --disable CONFIG_DEBUG_WARN
   kconfig-tweak --disable CONFIG_DEBUG_INFO
   kconfig-tweak --disable CONFIG_DEBUG_ASSERTIONS
   kconfig-tweak --disable CONFIG_DEBUG_NET
   kconfig-tweak --disable CONFIG_DEBUG_NET_ERROR
   kconfig-tweak --disable CONFIG_DEBUG_NET_WARN
   kconfig-tweak --disable CONFIG_DEBUG_NET_INFO
   kconfig-tweak --disable CONFIG_DEBUG_SYMBOLS
   kconfig-tweak --disable CONFIG_DEBUG_NOOPT
   kconfig-tweak --disable CONFIG_SYSLOG_TIMESTAMP
   make oldconfig

引用配置
=======================

Defconfig 支持使用 ``#include`` 语句引用其他配置文件：

.. code-block::

   CONFIG_XXX1=y
   CONFIG_XXX2=y
   #include "configs/system.config"
   #include "configs/net.config"

默认的头文件搜索路径包括：

* 当前目录；
* ``${boards}/configs/common``；
* ``${boards}/common/configs``；

合并配置
===================

可以使用 tools/merge_config.py 脚本手动合并多个配置片段。

.. code-block:: console

   $ cd nuttx
   $ ./tools/merge_config.py -o defconfig .config1 .config2

许可证设置
=============

NuttX 包含具有各种开源许可证的组件。要使用这些组件，
您必须在 :menuselection:`License Setup` 菜单中显式启用
相应的许可证配置选项：

* ``CONFIG_ALLOW_BSD_COMPONENTS`` - BSD 许可证组件（NFS、SPIFFS、Bluetooth LE 等）
* ``CONFIG_ALLOW_GPL_COMPONENTS`` - GPL/LGPL 许可证组件
* ``CONFIG_ALLOW_MIT_COMPONENTS`` - MIT 许可证组件
* ``CONFIG_ALLOW_BSDNORDIC_COMPONENTS`` - 5-Clause Nordic 许可证组件（仅限 NRF 芯片）
* ``CONFIG_ALLOW_ECLIPSE_COMPONENTS`` - Eclipse Public License 组件
* ``CONFIG_ALLOW_ICS_COMPONENTS`` - ICS 许可证组件
* ``CONFIG_ALLOW_CUSTOM_PERMISSIVE_COMPONENTS`` - 自定义宽松许可证组件

.. warning::
   请仔细审查每个启用组件的许可条款，以确保
   符合您项目的许可要求。
