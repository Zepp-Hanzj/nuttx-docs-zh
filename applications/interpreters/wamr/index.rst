==================================
``wamr`` WebAssembly 微运行时
==================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

本指南介绍如何在 NuttX 上试用 WAMR。

安装 WASI SDK
================

我们需要能够构建 WASM 程序。可以通过安装 ``wasi-sdk`` 来实现，如
`WAMR 指南 <https://wamr.gitbook.io/document/basics/getting-started/host_prerequsites>`_ 中所示。

确保安装可通过 ``/opt/wasi-sdk`` 在您的主机上访问，因为下面的 WASM hello world 示例的构建脚本需要这样。

构建 NuttX
==============

我们使用 `sim/wamr` 配置来构建带有 WAMR 的 NuttX。请注意，在撰写本文时，CMake 脚本不适用于此配置。目前请使用 makefile 构建：

.. code:: console

   $ cd nuttx
   $ tools/configure.sh sim/wamr
   $ make -j4
   $ ls -l nuttx
   -rwxrwxr-x 1 yf yf 4176376 Jun 10 08:11 nuttx

这将生成一个 ``nuttx`` 二进制文件。此外，WASM 示例可在
``apps/interpreters/wamr/wamr/product-mini/app-samples/hello-world`` 文件夹中找到。
我们按如下方式构建示例：

.. code:: console

   $ cd apps/interpreters/wamr/wamr/product-mini/app-samples/hello-world
   $ ./build.sh
   $ ls -l test.wasm
   -rwxrwxr-x 1 yf yf  413 Jun 10 08:18 test.wasm

稍后可以从 NuttX 访问 ``test.wasm`` 程序。

在 NSH 中试用 WAMR
===============

将 ``test.wasm`` 复制到 ``nuttx`` 程序所在的文件夹，然后运行 ``./nuttx`` 启动 NuttX，并从 NSH 运行 ``iwasm /data/test.wasm``：

.. code:: console

   $ ./nuttx

   NuttShell (NSH) NuttX-12.4.0
   nsh> iwasm /data/test.wasm
   Hello world!
   buf ptr: 0x1460
   buf: 1234
   nsh>
