===============================
``ficl`` Ficl Forth 解释器
===============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

Ficl 是一种编程语言解释器，设计为嵌入其他系统中作为命令、宏和开发原型语言。

这是 Ficl（"Forth 启发的命令语言"）的 DIY 移植。请参阅
http://ficl.sourceforge.net/。它是一个 "" 移植，因为 Ficl 源代码不在该目录中，
只有一个环境和说明，可以让您在 NuttX 下构建 Ficl。其余的由您自己完成。

构建说明
------------------

免责声明：此安装步骤仅在使用 Ficl 4.1.0 时进行过验证。
对于新版本，您可能需要对此说明或此目录中的文件进行一些调整。
请将此信息视为 _建议_ - 不一定经过验证的说明。

1. ``cd`` 到 ``interpreters/ficl``

2. 下载 Ficl：http://sourceforge.net/projects/ficl/files/

3. 解压 Ficl 压缩文件。

   例如，``unzip ficl-4.1.0.zip`` 将在 ``interpreters/ficl/ficl-4.1.0`` 留下文件。

4. 使用 ``configure.sh`` 脚本配置在 ``interpreters/ficl`` 目录中构建 Ficl。

   例如，``./configure.sh ficl-4.1.0`` 将在 ficl 构建目录中留下 Makefile 片段 ``Make.srcs``。

5. 创建您的 NuttX 配置。使用 ``make menuconfig``，您应该选择::

     CONFIG_INTERPRETERS_FICL=y

6. 配置并构建 NuttX。成功完成后，Ficl 对象将在 ``apps/libapps.a`` 中可用，
   NuttX 二进制文件将链接该文件。当然，除非您编写了使用它的应用程序代码，
   否则 Ficl 将不起作用！
