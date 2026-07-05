.. include:: /substitutions.rst
.. _citests:

======================================
本地运行 CI 运行时测试套件
======================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 在提交新的拉取请求时，会自动在
`模拟器 <https://nuttx.apache.org/docs/latest/guides/simulator.html>`__
和 QEMU 目标上运行持续集成（CI）测试。为避免测试失败，您也可以在提交新的拉取请求之前在本地计算机上运行它们。
本页面描述了执行此操作的逐步指南。

配置 NuttX
=================

NuttX 有一个模拟器目标，允许用户在计算机上将 NuttX 作为普通程序运行。具有 CI 测试功能的模拟器目标按以下方式配置和编译。

  .. code-block:: console

      $ cd nuttx
      $ ./tools/configure.sh sim:citest
      $ make

您应该看到带有内置测试应用程序的 NuttX shell。现在您可以退出模拟器。

  .. code-block:: console

      nsh> poweroff
      $
      $ # 我们回到了 Linux 提示符。


使用 ``tools/ci/testrun`` 运行 CI 测试
==========================================

本地运行 CI 测试需要系统上安装 Minicom 和 Python 3.6 或更新版本。其他依赖可以使用以下命令安装。

  .. code-block:: console

      $ cd tools/ci/testrun/env
      $ pip3 install -r requirements.txt
      $ cd ..
      $ cd script

现在您已准备好运行 CI 测试。测试本身通过以下命令运行。

  .. code-block:: console

      $ python3 -m pytest -m 'common or sim' ./ -B sim -P <nuttx-path> -L <log-path> -R sim -C --json=<log-path>/pytest.json

其中 nuttx-path 是 NuttX 根目录的绝对路径，log-path 是用户定义的用于保存测试日志的目录。
