==================
``gcov`` gcov 工具
==================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

gcov 是一个用于测试代码覆盖率的工具。程序运行后，可以查看每个文件的行覆盖率、
函数覆盖率和分支覆盖率。

支持
-------

当前系统支持四种代码覆盖率检测实现：

1. GCC 原生实现
2. CLANG 原生实现
3. GCC 覆盖率 nuttx 精简版
4. CLANG 覆盖率 nuttx 精简版

下表显示了四种实现之间的具体差异（截至 24.11.26）：

支持              GCC原生    CLANG原生     GCC-nuttx精简版    CLANG-nuttx精简版
编译器版本:        ALL          ALL        GCC 13.2 及以下    CLANG 17.0 及以下

程序覆盖率统计支持：

主程序              √            √                 √                     √
中断程序            ×            √                 √                     √

架构支持：

    arm                √            √                 √                     √
    arm64              √            √                 √
    riscv              √            √
    X86_X64            √            √
    xtensa             √            √
    sim                √            √

用法
=====

应用用法
---------
用法::

    gcov [-d path] [-t strip] [-r] [-h]

其中：

  -d 转储覆盖率，path 是覆盖率文件的路径，默认输出到标准输出
  -t 去除路径前缀的层数
  -r 重置覆盖率
  -h 显示此帮助文本并退出

适用平台示例
--------------------------------

1. SIM 平台用法

  1. 请启用以下配置

    # 支持对 sim 中所有代码的插桩
    1. CONFIG_COVERAGE_TOOLCHAIN=y

    # 启用插桩
    2. CONFIG_COVERAGE_ALL=y

    # 启用 gcov 应用
    3. CONFIG_SYSTEM_GCOV=y

  2. 编译并运行
     ```
     $ 代码编译后，会在 *.o 文件旁边生成同名的 *.gcno 文件。
     $ 编译完成后，运行待测试的代码，执行完成后退出 sim
     ```

  3. 运行 gcov 应用
     ```
     $ gcov -d path_to_gcno_file
     ```

  4. 检查是否生成成功
     ```
     在项目根目录执行以下命令检查是否有 gcda 文件生成（代码覆盖率数据）
     find ./ -name "*.gcno"
     find ./ -name "*.gcda"
     ```

  5. 示例：
     ```
     $ ./tools/configure.sh sim:nsh
     nsh: poweroff
     $ ./nuttx/tools/gcov.py -t gcov
     然后用浏览器打开 ./gcov/result/index.html
     ```

2. 适用于设备

  由于实现方式的差异，设备端分为 GCC 和 CLANG

  1. GCC

    1. 请启用以下配置

      # 推荐使用 nuttx 精简版
      CONFIG_COVERAGE_MINI=y

      # 启用 gcov 应用
      CONFIG_SYSTEM_GCOV=y

      # 请根据编译器在 makefile 中添加不同的编译选项
      CFLAGS += -fprofile-arcs -ftest-coverage -fno-inline

    2. 运行 gcov 应用
       ```
       $ gcov -d path_to_gcno_file
       ```

    3. 导出数据

      在设备上运行代码后，在 nuttx 命令行中执行 gcov -d /tmp/gcov 命令
      将生成的数据保存到文件系统。您需要使用您的方法将文件导出到主机。

    4. 生成报告

      1. 安装工具

        sudo apt install lcov

      2. 生成报告

        运行以下命令生成覆盖率报告

        # 默认在 vela 项目根目录生成，添加参数指定报告生成位置
        # -t 参数指定 gcov 版本，需要与 gcc 版本匹配

        # sim
        ./tools/gcov.py -t gcov

        # arm 平台
        ./tools/gcov.py -t arm-none-eabi-gcov

    5. 影响和注意事项
       ```
       1. 使用 .tools/gcov.sh 工具前，需要确保 *.gcno 和 *.gcda 文件存在
       2. 如果 *.gcno 不存在，请在 distclean 后重新编译代码
       3. 如果 *.gcda 不存在，请检查并使用 poweroff 正常退出 Vela
       ```

  2. CLANG

    # NXboards/arm/mps/mps3-an547/configs/gcov 中有现成的 defconfig 可供参考

    1. 请启用以下配置

      # 推荐使用 nuttx 精简版
      CONFIG_COVERAGE_MINI=y

      # 启用 gcov 应用
      CONFIG_SYSTEM_GCOV=y

      # 请根据编译器在 makefile 中添加不同的编译选项
      CFLAGS += -fprofile-instr-generate -fcoverage-mapping

    2. 修改链接脚本

      请在链接脚本中为以下数据找到相应的存储位置：

      详细示例请参考 boards/arm/mps/mps3-an547/scripts/flash.ld

      .. code-block:: none
          __llvm_prf_names : {
              __start__llvm_prf_names = .;
              KEEP (*(__llvm_prf_names))
              __end__llvm_prf_names = .;
          }

          __llvm_prf_data : {
              __start__llvm_prf_data = .;
              KEEP (*(__llvm_prf_data))
              __end__llvm_prf_data = .;
          }

          __llvm_prf_vnds : {
              __start__llvm_prf_vnds = .;
              KEEP (*(__llvm_prf_vnds))
              __end__llvm_prf_vnds = .;
          }

          __llvm_prf_cnts : {
              __start__llvm_prf_cnts = .;
              KEEP (*(__llvm_prf_cnts))
              __end__llvm_prf_cnts = .;
          }


    3. 运行 gcov 应用

      ```
      $ gcov -d path_to_gcno_file
      ```

    4. 导出数据

    5. 生成报告

      请执行以下命令，其中

      1. xxxfile：设备上导出的数据文件
      2. xxxelf：设备对应的 ELF 文件

      # 转换导出的覆盖率数据文件
      llvm-profdata merge -sparse xxxfile -o result.profdata

      # 生成可视化 html 文件
      llvm-cov show -format=html xxxelf -instr-profile=result.profdata -output-dir=./coverage/html
