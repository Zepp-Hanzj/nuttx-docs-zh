================================
``nxdiag`` NuttX 诊断工具
================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 诊断工具 (Nxdiag) 是一个命令行工具，可用于收集 NuttX 系统和主机系统的信息。
它还可以用于运行测试，以验证供应商的工具是否已正确安装和配置。

其主要目的是收集可用于调试问题的信息，并简化不熟悉用户的错误报告过程。

该工具使用 Python 脚本 (``nuttx/tools/host_info_dump.py``) 在构建期间收集主机系统信息，
并使用 C 程序收集 NuttX 系统信息并显示所有可用信息。有关 Python 脚本的更多信息，
请查看 ``host_info_dump.py`` 的命令行选项和代码注释。

或者，可以使用 ``host_info`` 目标而无需启用 nxdiag 应用程序和重新烧录即可获取系统信息。
该目标可在配置步骤之后工作，并打印有关 NuttX 和主机系统的信息。

.. note:: Nxdiag 需要 Python 3.6 或更高版本。在 Linux 发行版上，建议安装 ``distro`` Python 模块，
          因为它提供更准确的主机系统信息。

用法
-----

本页显示 ``nxdiag`` 选项。请注意，某些选项仅在启用相应的配置选项时才可用
（参见 :ref:`命令表 <nxdiagcmddependencies>`）。
要获取系统可用的 ``nxdiag`` 选项的完整列表，只需运行 ``nxdiag``::

    Usage: nxdiag [options]
    Options:
            -h                                 Show this message
            -n, --nuttx                        Output the NuttX operational system information.
            -f, --flags                        Output the NuttX compilation and linker flags used.
            -c, --config                       Output the NuttX configuration options used.
            -o, --host-os                      Output the host system operational system information.
            -p, --host-path                    Output the host PATH environment variable.
            -k, --host-packages                Output the host installed system packages.
            -m, --host-modules                 Output the host installed Python modules.
            -v, --vendor-specific              Output vendor specific information.
            --all                              Output all available information.

示例输出可以在 `这里 <https://pastebin.com/HSw1EvhR>`_ 查看。

.. toctree::
  :maxdepth: 2
  :caption: 目录

  config.rst
