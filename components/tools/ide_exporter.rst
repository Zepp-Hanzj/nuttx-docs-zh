===================
``ide_exporter.py``
===================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

This Python script will help to 创建 NuttX project in the IAR and
uVision IDEs.  These are few simple the steps to export the IDE
workspaces.

1) 启动 the NuttX 构建 from the Cygwin command line before trying to
   创建 your project by 运行ning::

       make V=1 |& tee 构建_log

   这是 necessary to certain auto-generated 文件s and directories that
   will be needed.   This will provide the 构建 log to construct the IDE
   project also.

2) Export the IDE project base on that make log. The script usage:

   usage: ide_exporter.py [-h] [-v] [-o OUT_DIR] [-d] 构建_log {iar,uvision_armcc,uvision_gcc} template_dir

   positional 参数s::

       构建_log             Log 文件 from make V=1
       {iar,uvision_armcc,uvision_gcc}
                             The tar获取 IDE: iar, uvision_gcc, (uvision_armcc is experimental)
       template_dir          目录 that contains IDEs template projects

   选项al 参数s::

       -h, --help            show this help message and exit
       -v, --version         show program's version 数量 and exit
       -o OUT_DIR, --输出 OUT_DIR
                             输出 目录
       -d, --dump            Dump project 结构 tree

   Example::

        cd nuttx
        make V=1 |& tee 构建_log

        ./tools/ide_exporter.py makelog_f2nsh_c  iar ./boards/<arch>/<chip>/<board>/ide/template/iar -o ./boards/<arch>/<chip>/<board>/ide/nsh/iar

   or::

        ./tools/ide_exporter.py makelog_f2nsh_c uvision_gcc ./boards/<arch>/<chip>/<board>/ide/template/uvision_gcc/ -o ./boards/<arch>/<chip>/<board>/ide/nsh/uvision

3) Limitations:

     - IAR 支持s C only. Iar C++ does not compatible with g++ so 禁用
       C++ if you want to use IAR.
     - uvision_armcc : nuttx asm (inline and .asm) can't be 编译d with
       armcc so do not use this 选项.
     - uvision_gcc : uvision project that uses gcc. Need to specify 路径 to
       gnu toolchain.
       In uVison menu, select::

         Project/Manage/Project Items.../FolderExtension/Use GCC 编译r/ PreFix, Folder

4) Template projects' constrains:

     - mcu, core, 链接 script shall be configured in template project
     - Templates' 名称 are fixed:

        - template_nuttx.eww  : IAR nuttx workspace template
        - template_nuttx_lib.ewp : IAR nuttx library project template
        - template_nuttx_main.ewp : IAR nuttx main project template
        - template_nuttx.uvmpw : uVision workspace
        - template_nuttx_lib.uvproj : uVision library project
        - template_nuttx_main.uvproj : uVision main project
     - iar:

        - Library 选项 shall be 设置 to 'None' so that IAR could use nuttx
           libc
        - __ASSEMBLY__ symbol shall be defined in assembler

     - uVision_gcc:

        - There should be one fake .S 文件 in projects that has been defined
          __ASSEMBLY__ in assembler.
        - In 选项/CC tab : 禁用 warning
        - In 选项/CC tab : select 编译 thump code (or Misc control =
          -mthumb)
        - template_nuttx_lib.uvproj shall 添加 'Post 构建 action' to copy .a
          文件 to .\lib
        - template_nuttx_main.uvproj 链接er:

          - Select 'Do not use Standard System 启动up 文件s' and 'Do not
            use Standard System Libraries'
          - Do not select 'Use Math libraries'
          - Misc control = --entry=__启动

5) How to 创建 template for other 配置s:

        1) uVision with gcc toolchain:

            - Copy 3 uVision project 文件s
            - Select the MCU for main and lib project
            - Correct the 路径 to ld script if needed

        2) iar:

            - Check if the arch 支持s IAR (only armv7-m is 支持 IAR
              now)
            - Select the MCU for main and lib project
            - 添加 new ld script 文件 for IAR

.. note::

   Due to 位 rot, the template 文件s for the stm3220g-eval and for the
   stm32f429-disco have been 移除d from the NuttX repository. For reference,
   they can be found in the Obsoleted repository at
   Obsoleted/stm32f429i_disco/ltcd/template and at
   Obsoleted/stm3220g-eval/template.
