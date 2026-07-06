==============
``refresh.sh``
==============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

.. note::

   使用 ``--silent`` 的此脚本实际上已经过时。silent 选项实际上只是添加默认值。
   然而，自 217-07-09 以来，defconfig 文件以压缩格式保留，即默认值已被移除。
   因此 ``--silent`` 选项不会产生任何效果。不使用 ``--silent`` 时，你将有机会
   从命令行覆盖默认值，在这种情况下，该脚本可能仍有一些最低限度的作用。

这是一个用于自动刷新开发板默认配置 (defconfig) 文件的 bash 脚本。
它不会执行任何你无法手动完成的特殊操作，但对于更新数十个配置文件非常有用。
它也用于 NuttX 的 CI 流程中。

配置文件需要定期更新，因为随着时间的推移，配置设置会发生变化；
新的配置选项被添加，新的依赖关系被引入。因此，旧的配置文件可能不再可用，
直到被刷新。

也可以获取帮助：

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

``refresh.sh`` 刷新文件的步骤如下：

1. 如果 ``tools/cmpconfig`` 尚未构建，则先构建它。

2. 将 defconfig 文件复制到 NuttX 顶层目录并重命名为 ``.config``
   （请注意保存你可能想要保留的任何先前的 ``.config`` 文件！）。

3. 执行 ``make oldconfig`` 以更新配置。``make oldconfig`` 将针对每一项需要
   你做出决策的配置变更进行提示。使用 ``--silent`` 选项时，脚本将改为使用
   ``make oldefconfig``，你无需回答任何问题；刷新过程将直接接受所有新配置
   设置的默认值。

4. 然后运行 ``tools/cmpconfig`` 来显示配置文件之间的实际差异。
   配置文件很复杂，内容可能会发生位置变化，因此两个配置文件之间的简单
   'diff' 通常没有太大用处。而 tools/cmpconfig 将仅显示两个配置文件之间
   有意义的差异。

5. 它将编辑 .config 文件以注释掉 ``CONFIG_APPS_DIR=`` 的设置。
   此设置不应出现在已提交的 defconfig 文件中，因为它实际上必须在
   下次安装配置时确定。

6. 最后，刷新后的 defconfig 文件被复制回原位，以便下次提交时将差异
   保存到命令行。如果你选择了 ``--silent`` 选项，此文件复制将自动进行。
   否则，refresh.sh 将先提示你确认，以避免用你可能不想要的更改
   覆盖 defconfig 文件。

使用示例：

更新所有开发板（不显示详细输出）：

.. code:: console

   $ ./tools/refresh.sh --silent --defaults all

更新 ``arm`` 架构的所有开发板和配置：

.. code:: console

   $ ./tools/refresh.sh --silent arch:arm

更新 ``stm32f7`` 芯片系列的所有开发板：

.. code:: console

   $ ./tools/refresh.sh --silent chip:stm32f7

更新 ``stm32f103-minimum`` 开发板的所有配置：

.. code:: console

   $ ./tools/refresh.sh --silent board:stm32f103-minimum

仅更新 stm32f103-minimum 开发板的 `.nsh.` 配置：

.. code:: console

   $ ./tools/refresh.sh --silent stm32f103-minimum:nsh
