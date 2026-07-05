==============
``refresh.sh``
==============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

.. note::

   This script with ``--silent`` is really obsolete. The silent 选项 really
   添加s 默认 值s. However, as of 217-07-09, defconfig 文件s are retained
   in a compressed format, i.e., with 默认 值s 移除d.  So the
   ``--silent`` option will accomplish nothing. Without ``--silent``, you will
   have the opportunity over override the 默认 值 from the command line
   and, in that case, the script may still have some minimal 值.

这是 a bash script that automates refreshing of board 默认 配置
(defconfig) 文件s. It does not do anything special that you cannot do manually,
but is useful for updating dozens of 配置 文件s. It is also used in the
NuttX CI process.

配置 文件s have to be updated because over time, the 配置
设置s change; new 配置s are 添加ed and new dependencies are 添加ed.
So an old 配置 文件 may not be usable anymore until it is refreshed.

Help is also available:

.. code:: console

   $ tools/refresh.sh --help
   tools/refresh.sh is a tool for refreshing board configurations

   USAGE: tools/refresh.sh [options] <board>:<config>+

   Where [options] include:
     --debug
        Enable script debug
     --silent
        Update board configuration without interaction.  Implies --defaults.
        Assumes no prompt for save.  Use --silent --prompt to prompt before saving.
     --prompt
        Prompt before updating and overwriting the defconfig file.  Default is to
        prompt unless --silent
     --defaults
        Do not prompt for new default selections; accept all recommended default values
     --nocopy
        Do not copy defconfig from nuttx/boards/<board>/configs to nuttx/.config
     --help
        Show this help message and exit
     <board>
        The board directory under nuttx/boards/arch/chip/
     <config>
        The board configuration directory under nuttx/boards/arch/chip/<board>/configs
     <archname>
        The architecture directory under nuttx/boards/
     <chipname>
        The chip family directory under nuttx/boards/<arch>/

     Note1: all configurations are refreshed if <board>:<config> is replaced with "all" keyword
     Note2: all configurations of arch XYZ are refreshed if "arch:<namearch>" is passed
     Note3: all configurations of chip XYZ are refreshed if "chip:<chipname>" is passed
     Note4: all configurations of board XYZ are refreshed if "board:<boardname>" is passed

The steps to refresh the 文件 taken by ``refresh.sh`` are:

1. Make ``tools/cmpconfig`` if it is not al读取y built.

2. Copy the defconfig 文件 to the top-level NuttX 目录 as ``.config``
   (being careful to save any previous ``.config`` 文件 that you might want to
   keep!).

3. Execute ``make` oldconfig` to update the configuration. ``make oldconfig``
   will prompt you for each change in the 配置 that requires that you
   make some decision. With the ``--silent`` option, the script will use ``make
   oldefconfig`` instead and you won't have to answer any questions; the refresh
   will simply accept the 默认 值 for any new 配置 设置s.

4. Then it 运行s ``tools/cmpconfig`` to show the real differences between the
   配置 文件s.  配置 文件s are complex and things can move
   around so a simple 'diff' between two 配置 文件s is often not
   useful.  But tools/cmpconfig will show only the meaningful differences
   between the two 配置 文件s.

5. It will edit the .config 文件 to comment out the 设置 of the
   ``CONFIG_APPS_DIR=`` 设置. This 设置 should not be in checked-in
   defconfig 文件s because the actually must be determined at the next time that
   the 配置 is installed.

6. Finally, the refreshed defconfig 文件 is copied back in place where it can be
   committed with the next 设置 of difference to the command line. If you select
   the ``--silent`` 选项, this 文件 copy will occur automatically. Otherwise,
   refresh.sh will prompt you first to avoid overwriting the defconfig 文件 with
   changes that you may not want.

Usage examples:

Update all boards without verbose 输出:

.. code:: console

   $ ./tools/refresh.sh --silent --defaults all

Update all boards and configs from `arm` architecture:

.. code:: console

   $ ./tools/refresh.sh --silent arch:arm

Update all boards from ``stm32f7`` chip family:

.. code:: console

   $ ./tools/refresh.sh --silent chip:stm32f7

Update all configs from ``stm32f103-minimum`` board:

.. code:: console

   $ ./tools/refresh.sh --silent board:stm32f103-minimum

Update only the `.nsh.` config from stm32f103-minimum board:

.. code:: console

   $ ./tools/refresh.sh --silent stm32f103-minimum:nsh
