================
Net Test Module
================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``apps/testing/nettest`` 目录用于构建与网络协议栈相关的测试用例。您可以在任何具有网络协议栈功能的设备上使用它。

Directory Structure
===================

::

    ├──tcp
    │  ├── test_tcp_connect_ipv4.c  # The testcase of TCP connect
    │  ├── ...
    │  ├── test_tcp_common.c        # TCP testcase common function
    │  ├── test_tcp.h               # TCP testcases declaration
    │  └── test_tcp.c               # TCP testcase execution entry
    ├──udp
    │  ├── ...
    │  ├── test_udp.h               # UDP testcases declaration
    │  └── test_udp.c               # UDP testcase execution entry
    ├── ...
    ├──utils                        # Utils for testcases
    │  ├── ...
    │  ├── nettest_netdump.c
    │  ├── nettest_tcpserver.c
    │  └── utils.h
    ├── CmakeLists.txt
    ├── Kconfig                     # Enable module testcases
    ├── Make.defs
    └── Makefile

How to Build
============

首先，此目录中的所有测试用例都依赖于 cmocka 框架，请确保启用以下 cmocka 配置：

- ``CONFIG_ALLOW_MIT_COMPONENTS=y``
- ``CONFIG_LIBC_REGEX=y``
- ``CONFIG_TESTING_CMOCKA=y``

然后，打开网络部分测试用例配置：

- ``CONFIG_TESTING_NET_TEST=y``

最后，您可以通过配置选择要启用的协议测试用例。一些协议配置依赖于其他网络配置；您可以在 ``Kconfig`` 文件中查看依赖关系。以 TCP 测试用例为例：

- ``CONFIG_NET_TCPBACKLOG=y``  – TCP 测试用例编译依赖
- ``CONFIG_NET_TCP=y``         – TCP 测试用例编译依赖
- ``CONFIG_TESTING_NET_TCP=y`` – TCP 测试用例配置项；对于其他协议，只需替换末尾的协议名称

How to Run
==========

测试用例构建完成后，您可以通过以下命令在命令行运行测试用例：

- ``cmocka --test test_tcp_connect_ipv4`` – 运行单个测试用例

- ``cmocka_net_tcp`` – 运行 TCP 测试用例（对于其他协议，只需替换末尾的协议名称）

此外，当您运行 ``cmocka`` 时，上述命令也将包含在内。

How to Add Testcases
====================

如果您想添加测试用例，请按照以下步骤操作：

1. 将测试用例源文件添加到相应的目录。请遵循以下源文件命名规则：

   ``test_<protocol>_<function description>_<additional description>.c``

   例如：``test_tcp_connect_ipv4.c``

   测试用例名称与源文件相同，例如 ``test_tcp_connect_ipv4()``。

2. 将测试用例源文件添加到 ``CMakeLists.txt`` 文件。

3. 将测试用例源文件添加到 ``Makefile`` 文件。

4. 将测试用例添加到相应的声明文件和执行入口文件。例如，``test_tcp_connect_ipv4()`` 需要添加到 ``test_tcp.h`` 和 ``test_tcp.c``。如果您有单独的 setup 函数，也需要将其添加到上述两个文件中。
