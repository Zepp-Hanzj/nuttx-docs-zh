======================================
Nix Flake 可复现开发环境
======================================

本指南说明如何使用 Nix flake 为 NuttX 设置可复现的开发环境。
Nix flake 确保所有必需的构建工具和依赖项始终可用，
简化了新手入门并减少了"在我的机器上可以运行"的问题。

前提条件
-------------

* 在你的系统上安装了 `Nix <https://nixos.org/download/>`_。
* 启用了 Nix flakes（在你的 ``nix.conf`` 中添加 ``experimental-features = nix-command flakes``）。

设置开发环境
--------------------------------------

要进入 **NuttX 构建** 开发 shell，导航到 NuttX 目录的根目录并运行：

.. code-block:: bash

    nix develop ./tools/nix

此命令将：

* 下载并设置所有必要的构建工具和依赖项，包括：

  * CMake、Ninja、GNU Make
  * Clang 工具
  * ARM 工具链（gcc-arm-embedded）
  * Automake、Bison、Flex、Genromfs、Gettext、Gperf
  * Kconfig-frontends、libelf、expat、gmp、isl、libmpc、mpfr、ncurses、zlib
  * 带有 kconfiglib 的 Python

* 将 ``CMAKE_EXPORT_COMPILE_COMMANDS`` 环境变量设置为 ``ON``。
* 显示欢迎消息。

进入开发 shell 后，你可以像往常一样继续构建 NuttX。

设置文档环境
-----------------------------------------

该 flake 还提供了 **文档** 开发 shell，包含 Sphinx 以及
构建 NuttX 文档所需的所有扩展。

要进入文档 shell，运行：

.. code-block:: bash

    nix develop ./tools/nix#docs

此命令将：

* 提供带有 Sphinx 和扩展的 Python 3.13，包括：

  * sphinx-rtd-theme
  * myst-parser
  * sphinx-tabs
  * sphinx-autobuild
  * sphinx-copybutton
  * sphinx-togglebutton
  * sphinx-design
  * sphinx-tags
  * sphinx-collapse
  * pytz、importlib-metadata

* 允许你在不全局安装任何内容的情况下构建和预览文档。

用法示例：

.. code-block:: bash

    # 构建 HTML 文档（必须在 Documentation/ 目录下运行）
    make html

更多详情请参阅 :doc:`/contributing/documentation` 指南。

优势
--------

* **可复现性：** 确保所有开发者和机器之间具有一致的构建环境。
* **简化入门：** 新贡献者只需一条命令即可快速设置开发环境。
* **依赖管理：** 所有依赖项由 Nix 管理，避免与系统范围的软件包发生冲突。
* **独立环境：** 保持固件构建工具和文档工具隔离，或根据需要组合它们。

Nix Flake 的内容
-------------------------

`flake.nix` 文件定义了两个 `devShells`：

* ``devShells.default`` - NuttX 构建环境：

.. code-block:: nix

    buildInputs = [
      # Build tools
      pkgs.cmake
      pkgs.ninja
      pkgs.gnumake
      pkgs.clang-tools

      # ARM toolchain
      pkgs.gcc-arm-embedded

      # NuttX dependencies
      pkgs.automake
      pkgs.bison
      pkgs.flex
      pkgs.genromfs
      pkgs.gettext
      pkgs.gperf
      pkgs.kconfig-frontends
      pkgs.libelf
      pkgs.expat.dev
      pkgs.gmp.dev
      pkgs.isl
      pkgs.libmpc
      pkgs.mpfr.dev
      pkgs.ncurses.dev
      pkgs.zlib
      pkgs.python313Packages.kconfiglib
    ];

    shellHook = ''
      export CMAKE_EXPORT_COMPILE_COMMANDS=ON
      echo "Welcome to NuttX devShell"
    '';

* ``devShells.docs`` - 文档环境（来自 `Documentation/flake.nix`）：

.. code-block:: nix

    python.withPackages (ps: with ps; [
      sphinx
      sphinx_rtd_theme
      myst-parser
      sphinx-tabs
      sphinx-autobuild
      sphinx-copybutton
      sphinx-togglebutton
      sphinx-design
      sphinx-tags
      sphinx-collapse
      pytz
      importlib-metadata
    ]);

此设置确保固件开发和文档构建都是完全可复现和隔离的。
