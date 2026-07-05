=========================================
``nxwm`` NuttX 小型窗口管理器 (NxWM)
=========================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

本目录为配备触摸屏的小型嵌入式设备提供了一个小型桌面——NxWM。NxWM 是一个真正的多窗口管理器，但一次只显示一个窗口。这种简化有助于基于 LCD 的产品的性能（与平铺窗口管理器的方式相同），并能充分利用小显示屏。从人机工程学角度来看，在小显示屏上管理多个窗口是很困难的。

窗口管理器由任务栏组成，任务栏上有代表运行中任务的图标。如果您触摸任务的图标，它就会显示在最前面。每个窗口都有一个工具栏，包含 (1) 标题、(2) 最小化按钮和 (3) 停止应用程序按钮，使用这些功能的标准图标。

任务栏中始终有一个可用的启动窗口。当您触摸启动窗口图标时，它会弹出启动窗口，其中包含代表所有可用应用程序的图标。如果您触摸启动窗口中的某个图标，它将被启动并添加到任务栏中。

有一个定义附加应用程序的基类和一个支持集成新应用程序的接口。唯一提供的应用程序是 NxTerm。这是一个在窗口中运行的 NSH 会话。您应该能够选择启动菜单中的 NX 图标，并创建任意数量的 NSH 会话窗口。（键盘输入仍然通过串口进行。）

注意 1：NxWM 需要 ``NuttX-7.19`` 或更高版本才能与当前的 ``NxWidgets-1.18`` 版本配合工作。

.. toctree::
   :maxdepth: 1
   :titlesonly:
   :caption: 目录

   cnxconsole.rst

Doxygen
-------

在 Ubuntu 中安装必要的软件包
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. 安装以下软件包::

   $ sudo aptitude install doxygen doxygen-doc doxygen-gui dot2tex graphviz

2. （可选）从最新源代码安装 Doxygen。

   Ubuntu 软件包已过时。Doxygen 版本越新，文档外观越好。

   进入临时文件夹下载源代码，然后运行 [1]::

     $ svn co https://doxygen.svn.sourceforge.net/svnroot/doxygen/trunk doxygen-svn
     $ cd doxygen-svn
     $ ./configure
     $ make
     $ make install

生成文档
~~~~~~~~~~~~~~~~~~~~~~~~

此处描述两种方法：

1. 使用提供的 ``gendoc.sh`` 脚本::

     trunk/NXWidgets/Doxygen/gendoc.sh

   该脚本只需要一个参数，即生成文档的绝对路径。即::

     $ cd /path/to/nuttx/trunk/NXWidgets/Doxygen/
     $ mkdir doc
     $ ./gendoc.sh $PWD/doc

2. 直接使用 ``Doxyfile``：

   ``Doxyfile`` 文件包含 Doxygen 设置的运行配置，仅在必要时编辑。

   要生成文档，请输入::

     $ cd /path/to/nuttx/trunk/NXWidgets/Doxygen/
     $ doxygen Doxyfile

参考文献
~~~~~~~~~~

[1] http://www.stack.nl/~dimitri/doxygen/download.html
