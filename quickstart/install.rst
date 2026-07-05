.. include:: /substitutions.rst
.. _install:

==========
安装
==========

开始使用 NuttX 的第一步是安装一系列必需的工具、用于目标架构的工具链，
以及最终下载 NuttX 源代码本身。

前置条件
=============

首先，根据您的操作系统安装以下系统依赖：

.. tabs::

  .. tab:: Linux（基于 Debian）

    运行以下命令安装软件包：

    .. code-block:: console

      $ sudo apt install \
      $ bison flex gettext texinfo libncurses5-dev libncursesw5-dev xxd \
      $ git gperf automake libtool pkg-config build-essential gperf genromfs \
      $ libgmp-dev libmpc-dev libmpfr-dev libisl-dev binutils-dev libelf-dev \
      $ libexpat1-dev gcc-multilib g++-multilib picocom u-boot-tools util-linux

  .. tab:: Linux（Fedora / 基于 RPM）

    运行以下命令安装软件包：

    .. code-block:: console

      $ sudo dnf install \
      $ bison flex gettext texinfo ncurses-devel ncurses ncurses-compat-libs \
      $ git gperf automake libtool pkgconfig @development-tools gperf genromfs \
      $ gmp-devel mpfr-devel libmpc-devel isl-devel binutils-devel elfutils-libelf-devel \
      $ expat-devel gcc-c++ g++ picocom uboot-tools util-linux

  .. tab:: macOS
  
    运行以下命令安装软件包：

    .. code-block:: console

      $ brew tap discoteq/discoteq
      $ brew install flock
      $ brew install x86_64-elf-gcc  # 用于模拟器
      $ brew install u-boot-tools  # 某些平台集成 u-boot

  .. tab:: Windows / WSL

    如果您在 Windows 上构建 Apache NuttX 并使用 WSL，请按照
    Linux 的安装指南进行操作。该方案已在 Ubuntu 18.04 版本上验证通过。

    通过 USB 与编程工具交互可能会遇到一些问题。最近 WSL 2 已添加
    USBIP 支持，已有人将其与 STM32 平台配合使用，但配置并不简单：
    https://learn.microsoft.com/en-us/windows/wsl/connect-usb

  .. tab:: Windows/Cygwin

    下载并安装 `Cygwin <https://www.cygwin.com/>`_，使用最小化安装，
    并额外安装以下软件包::

        make              bison             libmpc-devel
        gcc-core          byacc             automake-1.15
        gcc-g++           gperf             libncurses-devel
        flex              gdb               libmpfr-devel
        git               unzip             zlib-devel

KConfig 前端
----------------

NuttX 配置系统使用 `KConfig <https://www.kernel.org/doc/Documentation/kbuild/kconfig-language.txt>`_，
它通过一系列交互式菜单式 *前端* 来操作，属于
``kconfig-frontends`` 软件包的一部分。根据您的操作系统，您可以使用预编译的
软件包，也可以从源代码构建，源代码位于
`NuttX tools 仓库 <https://bitbucket.org/nuttx/tools/src/master/kconfig-frontends/>`_：

.. tabs::

  .. code-tab:: console Ubuntu 20.04 LTS 及更新版本

    $ sudo apt install kconfig-frontends

  .. code-tab:: console Ubuntu 18.04 LTS 及更早版本

    $ git clone https://bitbucket.org/nuttx/tools.git
    $ cd tools/kconfig-frontends
    $ ./configure --enable-mconf --disable-nconf --disable-gconf --disable-qconf
    $ make
    $ make install

  .. code-tab:: console Fedora

    $ git clone https://bitbucket.org/nuttx/tools.git
    $ cd tools/kconfig-frontends
    $ ./configure --enable-mconf --disable-nconf --disable-gconf --disable-qconf
    $ aclocal
    $ automake
    $ make
    $ sudo make install

  .. code-tab:: console macOS

    $ git clone https://bitbucket.org/nuttx/tools.git
    $ cd tools/kconfig-frontends
    $ patch < ../kconfig-macos.diff -p 1
    $ ./configure --enable-mconf --disable-shared --enable-static --disable-gconf --disable-qconf --disable-nconf
    $ make
    $ sudo make install

NuttX 也默认支持 `kconfiglib <https://github.com/ulfalizer/Kconfiglib>`_，
这是一个用 Python 2/3 实现的 Kconfig 工具。与 ``kconfig-frontends`` 相比，
kconfiglib 为 NuttX 提供了多平台支持的可能性（在 Windows 原生/Visual Studio 中配置 NuttX），
并且 ``kconfiglib`` 具有更强的 Kconfig 语法检查功能，有助于开发者避免
一些 Kconfig 语法错误。通过以下命令安装 kconfiglib：

.. code-block:: shell

  sudo apt install python3-kconfiglib

如果您在 Windows 上使用，还需要安装 windows-curses 支持：

.. code-block:: shell

  pip install windows-curses


工具链
=========

要构建 Apache NuttX，您需要根据目标平台安装相应的工具链。
某些操作系统（如 Linux）会提供各种架构的工具链。
这通常是一个简便的选择，但您应该注意，在某些情况下
操作系统提供的版本可能存在问题，使用其他来源的
广泛使用的构建版本可能更好。

以下示例展示了如何安装 ARM 架构的工具链：

.. tabs::

  .. code-tab:: console Ubuntu (deb)

    $ sudo apt install gcc-arm-none-eabi binutils-arm-none-eabi

  .. tab:: macOS

    对于 32 位 ARM 目标，如 STM32：

    .. code-block:: console
      
      $ brew install --cask gcc-arm-embedded

    对于 64 位 ARM 目标，如 Allwinner A64：

    .. code-block:: console
      
      $ brew install --cask gcc-aarch64-embedded

  .. tab:: 从 arm.com 安装

    首先，创建一个目录来存放工具链：

    .. code-block:: console

      $ usermod -a -G users $USER
      $ # 获取一个知道我们在该组中的登录 shell：
      $ su - $USER
      $ sudo mkdir /opt/gcc
      $ sudo chgrp -R users /opt/gcc
      $ sudo chmod -R u+rw /opt/gcc
      $ cd /opt/gcc

    下载并解压工具链：

    .. code-block:: console

      $ HOST_PLATFORM=x86_64-linux   # 使用 'aarch64-linux' 用于 ARM64 Linux，或 'mac' 用于 Intel macOS
      $ # Windows 有一个 zip 文件（gcc-arm-none-eabi-10.3-2021.10-win32.zip）
      $ curl -L -O https://armkeil.blob.core.windows.net/developer/Files/downloads/gnu-rm/10.3-2021.10/gcc-arm-none-eabi-10.3-2021.10-${HOST_PLATFORM}.tar.bz2
      $ tar xf gcc-arm-none-eabi-10.3-2021.10-${HOST_PLATFORM}.tar.bz2

    将工具链添加到您的 `PATH`：

    .. code-block:: console

      $ echo "export PATH=/opt/gcc/gcc-arm-none-eabi-10.3-2021.10/bin:$PATH" >> ~/.bashrc

    如果您不使用 bash，可以编辑您 shell 的 rc 文件。

.. tip::
  在 Apache NuttX CI 辅助脚本
  `script <https://github.com/apache/nuttx/tree/master/tools/ci/cibuild.sh>`_
  和 Docker `container <https://github.com/apache/nuttx/tree/master/tools/ci/docker/linux/Dockerfile>`_
  中有关于如何获取大多数支持架构的最新工具链的提示。
  
.. todo::
  所需工具链应作为每个架构文档的一部分（参见 `相关 issue <https://github.com/apache/nuttx/issues/2409>`_）。

下载 NuttX
==============

Apache NuttX 在 GitHub 上积极开发。有两个主要仓库，
`nuttx <https://github.com/apache/nuttx>`_ 和 `apps <https://github.com/apache/nuttx-apps>`_，
其中后者在技术上是可选的（但推荐使用以获得完整功能）。如果您打算贡献更改、
需要绝对最新的版本，或者您只是更喜欢使用 git 工作，您应该克隆这些
仓库（推荐）。否则，您可以选择下载任何
`稳定版本 <https://nuttx.apache.org/download/>`_ 的归档包。

.. tabs::

  .. tab:: 克隆 git 仓库
  
    .. code-block:: console

       $ mkdir nuttxspace
       $ cd nuttxspace
       $ git clone https://github.com/apache/nuttx.git nuttx
       $ git clone https://github.com/apache/nuttx-apps apps

    开发源代码也可以作为压缩归档获取：

    .. code-block:: console

       $ mkdir nuttxspace
       $ cd nuttxspace
       $ curl -L https://github.com/apache/nuttx/tarball/master -o nuttx.tar.gz 
       $ curl -L https://github.com/apache/nuttx-apps/tarball/master -o apps.tar.gz
       $ tar zxf nuttx.tar.gz --one-top-level=nuttx --strip-components 1
       $ tar zxf apps.tar.gz --one-top-level=apps --strip-components 1
       
    也提供 ``.zip`` 归档（适用于 Windows 用户）：只需将 ``tarball`` 替换为
    ``zipball``。

  .. tab:: 下载稳定版本
  
    前往 `releases <https://nuttx.apache.org/download/>`_ 并选择要下载的版本。以下
    示例使用 12.2.1 版本：

    .. code-block:: console
    
       $ mkdir nuttxspace
       $ cd nuttxspace
       $ curl -L https://www.apache.org/dyn/closer.lua/nuttx/12.2.1/apache-nuttx-12.2.1.tar.gz?action=download -o nuttx.tar.gz
       $ curl -L https://www.apache.org/dyn/closer.lua/nuttx/12.2.1/apache-nuttx-apps-12.2.1.tar.gz?action=download -o apps.tar.gz
       $ tar zxf nuttx.tar.gz
       $ tar zxf apps.tar.gz
