使用 VPNKit 的网络支持
===============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

可以配置模拟使用 VPNKit 来提供网络支持。
虽然这是为 macOS 开发的，但它也应该能在其他平台上工作。

配置
--

.. code-block:: bash

    CONFIG_SIM_NETDEV=y
    CONFIG_SIM_NETDEV_TAP is not set
    CONFIG_SIM_NETDEV_VPNKIT=y
    CONFIG_SIM_NETDEV_VPNKIT_PATH="/tmp/vpnkit-nuttx"

你可以使用 ``sim:vpnkit`` 配置，其中包含上述设置。

.. code-block:: bash

    ./tools/configure.sh sim:vpnkit

VPNKit 设置
---------

请参阅 `https://github.com/moby/vpnkit` 获取构建说明。

如果你的机器上安装了 Docker Desktop for Mac，
你可以在以下位置找到 vpnkit 二进制文件：

.. code-block:: bash

    /Applications/Docker.app/Contents/Resources/bin/com.docker.vpnkit

也提供包含静态 Linux 二进制文件的 Docker 镜像：

`https://hub.docker.com/r/djs55/vpnkit`

如何运行
----

你可以按如下方式使用：

.. code-block:: bash

    % vpnkit --ethernet /tmp/vpnkit-nuttx &
    % ./nuttx

NuttX 的 ``CONFIG_SIM_NETDEV_VPNKIT_PATH`` 应与 vpnkit 的
``--ethernet`` 选项匹配。
