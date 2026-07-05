Porting Layer
=============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

nimBLE 支持作为不同操作系统的一部分进行构建，不仅限于其 mynewt RTOS。
为 NuttX 编写了一个移植层，基本上是 Linux 移植层的副本。

修改移植层
---------------------------

NuttX 通过在移植层中添加一个条目来支持 nimBLE，该移植层用于支持不同的操作系统。
然而，nimBLE 通过从 YAML 配置文件生成配置头文件（``syscfg.h``）来支持每个操作系统。
如果您想修改移植层并更改其配置，您将需要重新生成此头文件。这个过程比较复杂，因为
nimBLE 使用自己的 ``newt`` 构建工具来执行此操作，并且还假设它将为其 mynewt 操作
系统构建，因此它实际上可能无法完全构建，但仍然会生成所需的文件。

首先，获取 newt 工具::

  $ cd apps/nimble
  $ git clone https://github.com/apache/mynewt-newt
  $ cd mynewt-newt

目前，您可能需要不稳定版本而非发布版本，因此选择一个已知可用的版本::

  $ git checkout c14c47bb683d
  $ ./build.sh

现在应该在 ``mynewt-newt/newt`` 下有一个 ``newt`` 二进制文件。扩展您的路径
使其可见::

  $ export PATH=mynewt-newt/newt:$PATH

现在，创建一个 ``newt`` 项目::

  $ newt new foo

我们想要 mynewt 操作系统和协议栈的最新主版本，因此编辑 ``foo/project.yml``
并将 ``vers`` 变量更改为 ``0.0.0``。然后执行::

  $ cd foo/
  $ newt upgrade

在 ``foo/repos`` 下将有 mynewt 和 nimble 仓库的克隆。由于此应用已经在
``foo`` 之外下载了 nimble 仓库，您可以删除 ``foo/repos/apache-mynewt-nimble``
并简单地创建一个指向 ``mynewt-nimble`` 目录的链接，这样您就可以直接在 nimBLE
代码上工作。

现在您可以对 ``yml`` 文件进行任何更改，例如
``porting/targets/nuttx/syscfg.yml``。最后，您可以使用以下命令构建::

  $ newt build @apache-mynewt-nimble/porting/targets/nuttx

这很可能无法完成，但生成的头文件应该在那里。所以现在将它们复制到 ``nuttx``
目标目录中的适当位置::

  $ cd foo/
  $ cp bin/@apache-mynewt-nimble/porting/targets/nuttx/generated/include/logcfg/logcfg.h \
	repos/apache-mynewt-nimble/porting/examples/nuttx/include/logcfg
  $ cp bin/@apache-mynewt-nimble/porting/targets/nuttx/generated/include/syscfg/syscfg.h \
	repos/apache-mynewt-nimble/porting/examples/nuttx/include/syscfg

如果这些更改是为了修复 nimBLE 中 NuttX 移植层的问题，您应该向 nimBLE 仓库提交
拉取请求以包含更新的头文件。建议先在 NuttX 邮件列表中提及该问题以确保更改是必要的。
