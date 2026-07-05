=================
RPMSG 文件系统
=================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

一旦 RPMsg 链路可用，我们可以使用 rpmsg 文件系统借助 RPMsg 文件系统驱动程序来挂载远程目录。

这里我们展示一个从远程端挂载和使用主文件系统路径的示例，它就像使用本地文件系统一样简单。

构建
========

在文件系统服务器端（主节点），我们需要启用 ``CONFIG_FS_RPMSGFS_SERVER`` 配置。

在文件系统客户端（远程端），我们需要启用 ``CONFIG_FS_RPMSGFS`` 配置。

然后我们相应地构建两端。

运行
=======

使用以下命令从远程节点的 ``nsh`` 会话中将主节点的 ``/proc`` 文件系统挂载到 ``/proc.master``。

.. code:: console

  remote> mount -t rpmsgfs -o cpu=master,fs=/proc /proc.master
  remote> cat /proc/uptime /proc.master/uptime 
        39.06                                                                      
        39.06                                                                      
  remote>

注意 ``-o cpu=master,fs=/proc`` 指定 ``master`` 节点的 ``/proc`` 路径作为源，``/proc.master`` 是远程端的挂载点。该挂载点下的所有文件实际上都托管在主节点端。``-t rpmsgfs`` 选择 RPMsg 文件系统驱动程序来处理操作。
