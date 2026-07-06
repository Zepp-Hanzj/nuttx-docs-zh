===================
``ide_exporter.py``
===================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

此 Python 脚本可帮助在 IAR 和 uVision IDE 中创建 NuttX 项目。
以下是导出 IDE 工作区的简单步骤。

1) 在尝试创建项目之前，先从 Cygwin 命令行启动 NuttX 构建::

       make V=1 |& tee build_log

   这对于某些自动生成的文件和目录是必要的。
   这也会提供构建日志以构建 IDE 项目。

2) 基于该 make 日志导出 IDE 项目。脚本用法：

   usage: ide_exporter.py [-h] [-v] [-o OUT_DIR] [-d] build_log {iar,uvision_armcc,uvision_gcc} template_dir

   positional arguments::

       build_log             来自 make V=1 的日志文件
       {iar,uvision_armcc,uvision_gcc}
                             目标 IDE：iar、uvision_gcc（uvision_armcc 为实验性）
       template_dir          包含 IDE 模板项目的目录

   optional arguments::

       -h, --help            显示此帮助消息并退出
       -v, --version         显示程序版本号并退出
       -o OUT_DIR, --output OUT_DIR
                             输出目录
       -d, --dump            转储项目结构树

   Example::

        cd nuttx
        make V=1 |& tee build_log

        ./tools/ide_exporter.py makelog_f2nsh_c  iar ./boards/<arch>/<chip>/<board>/ide/template/iar -o ./boards/<arch>/<chip>/<board>/ide/nsh/iar

   or::

        ./tools/ide_exporter.py makelog_f2nsh_c uvision_gcc ./boards/<arch>/<chip>/<board>/ide/template/uvision_gcc/ -o ./boards/<arch>/<chip>/<board>/ide/nsh/uvision

3) Limitations:

     - IAR 仅支持 C。Iar C++ 与 g++ 不兼容，因此如果要使用 IAR 请禁用 C++。
     - uvision_armcc：NuttX 汇编（inline 和 .asm）无法用 armcc 编译，
       因此不要使用此选项。
     - uvision_gcc：使用 gcc 的 uVision 项目。需要指定 GNU 工具链路径。
       在 uVision 菜单中选择::

         Project/Manage/Project Items.../FolderExtension/Use GCC compiler/ PreFix, Folder

4) Template projects' constrains:

     - MCU、核心、链接脚本应在模板项目中配置
     - 模板名称是固定的：

        - template_nuttx.eww  : IAR NuttX 工作区模板
        - template_nuttx_lib.ewp : IAR NuttX 库项目模板
        - template_nuttx_main.ewp : IAR NuttX 主项目模板
        - template_nuttx.uvmpw : uVision 工作区
        - template_nuttx_lib.uvproj : uVision 库项目
        - template_nuttx_main.uvproj : uVision 主项目
     - iar:

        - 库选项应设置为 'None'，以便 IAR 可以使用 NuttX 的 libc
        - __ASSEMBLY__ 符号应在汇编器中定义

     - uVision_gcc:

        - 项目中应有一个假的 .S 文件，其中已在汇编器中定义了 __ASSEMBLY__。
        - 在 Option/CC 标签页：禁用警告
        - 在 Option/CC 标签页：选择 Compile thumb 代码（或 Misc control = -mthumb）
        - template_nuttx_lib.uvproj 应添加 'Post build action' 以将 .a 文件复制到 .\\lib
        - template_nuttx_main.uvproj Linker:

          - 选择 'Do not use Standard System Startup Files' 和 'Do not
            use Standard System Libraries'
          - 不要选择 'Use Math libraries'
          - Misc control = --entry=__start

5) 如何为其他配置创建模板：

        1) 使用 gcc 工具链的 uVision：

            - 复制 3 个 uVision 项目文件
            - 为主项目和库项目选择 MCU
            - 如需要，更正到 ld 脚本的路径

        2) iar:

            - 检查架构是否支持 IAR（目前仅 armv7-m 支持 IAR）
            - 为主项目和库项目选择 MCU
            - 为 IAR 添加新的 ld 脚本文件

.. note::

   由于年久失修，stm3220g-eval 和 stm32f429-disco 的模板文件
   已从 NuttX 仓库中移除。作为参考，可以在 Obsoleted 仓库中找到它们：
   Obsoleted/stm32f429i_disco/ltcd/template 和
   Obsoleted/stm3220g-eval/template。
