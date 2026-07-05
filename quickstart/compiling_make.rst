.. include:: /substitutions.rst
.. _compiling:

===================
使用 Make 编译
===================

现在我们已经安装了 Apache NuttX 的前置依赖并下载了源代码，
可以开始将源代码编译为可在嵌入式板上运行的可执行二进制文件了。

初始化配置
========================

第一步是为给定的开发板初始化 NuttX 配置，基于
一个预先存在的配置。要列出所有支持的配置，可以执行：

    .. code-block:: console

       $ cd nuttx
       $ ./tools/configure.sh -L | less

输出格式为 ``<board name>:<board configuration>``。您会发现
通常所有开发板都支持 ``nsh`` 配置，这是一个很好的起点，
因为它可以启动进入交互式命令行
:doc:`/applications/nsh/index`。

要选择一个配置，将 ``<board name>:<board configuration>`` 选项
传递给 ``configure.sh`` 并指定您的主机平台，例如：

    .. code-block:: console

       $ cd nuttx
       $ ./tools/configure.sh -l stm32f4discovery:nsh

``-l`` 表示我们在 Linux 上（也支持 macOS 和 Windows 构建）。
使用 ``-h`` 参数查看所有可用选项。

然后您可以使用基于菜单的配置系统自定义此配置：

.. code-block:: console

   $ cd nuttx
   $ make menuconfig

修改配置在 :doc:`configuring` 中介绍。

构建 NuttX
===========

现在我们可以构建 NuttX。为此，您只需运行：

  .. code-block:: console

     $ cd nuttx
     $ make

构建完成后将在 ``nuttx`` 目录中生成二进制输出文件。
通常包括 ``nuttx`` ELF 文件（适合使用 ``gdb`` 调试）和
``nuttx.bin`` 文件（可烧录到开发板上）。

要清理构建，可以执行：

  .. code-block:: console

     $ make clean

.. tip::

  要提高构建速度（或任何其他目标如 ``clean``），您可以
  向 ``make`` 传递 ``-jN`` 标志，其中 ``N`` 是要启动的
  并行任务数（通常是您机器上的处理器数量）。
