================
NuttX CI 流程
================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 是一个复杂系统，拥有大量编译时可配置的开关和值。更重要的是，NuttX 支持数百个不同的硬件目标，涵盖多种不同的架构。这种复杂性使得为传入的补丁建立 CI 测试流程至关重要。

.. note::

   NuttX 的 CI 资源有限，并非内核中的所有内容都能在 CI 中进行合理测试（例如，目前尚不支持通过 CI 直接在硬件目标上进行测试，但正在努力实现中）。

   因此，NuttX 仍然要求补丁作者进行自己的本地测试（特别是在适用的硬件上），并在提交补丁时附上测试结果，以便审查者对更改不会引入明显的回归问题有一定信心。

.. tip::

   NuttX 始终感谢对流程的改进！如果您有改进 CI 基础设施的建议，请告知社区。我们的 CI 团队目前承担着很高的工作量。

本文档的重点是在 `nuttx <https://github.com/apache/nuttx>`_（和 `nuttx-apps
<https://github.com/apache/nuttx-apps>`_）GitHub 仓库上打开 PR 时进行的 CI 测试。

CI 阶段
=========

当打开 PR 时，会执行以下 CI 操作：

* PR 标签器为 PR 分配标签
* 使用主机工具 :doc:`checkpatch.sh
  </components/tools/checkpatch>` 检查 PR
* 使用 `Super-Linter
  <https://github.com/super-linter/super-linter/pkgs/container/super-linter>`_ 执行代码检查
* 根据修改的文件执行构建测试
* 通过 :doc:`/testing/ntfc` 在模拟器/仿真器上执行一些 CI 运行时测试

PR 标签
======================

此操作负责：

* 为 PR 添加与更改文件对应的标签（例如，``arch/arm/**`` 下更改的文件标记为 ``Arch: arm``）
* 为 PR 添加大小标签（例如 ``Size: XS``、``Size: M`` 等）

此操作的工作流文件位于
``.github/workflows/labeler.yml``。该文件包含以注释形式的文档。为了计算 PR 标签，它：

* 从 GitHub 获取有关更改的信息（即更改的文件和行数）
* 汇总总更改行数并根据此数字分配 PR 大小标签
* 使用 `.github/labeler.yml` 中的通配符路径到标签的映射来为 PR 分配正确的更改标签

标签类型包括：

* 架构标签（即 ``Arch: arm``、``Arch: risc-v`` 等），与 ``arch/`` 中的更改相关
* 板级标签（即 ``Board: arm``、``Board: sim`` 等），与 ``boards/`` 中的更改相关
* 领域标签（即 ``Area: Bluetooth``、``Area: Crypto``、``Area: Drivers``），
  与多个不同的内核"领域"相关

此工作流运行完成后，PR 的标签将根据计算结果进行更新，pull-requests 选项卡中的 PR 可以根据这些标签进行排序。

.. tip::

   您可以按 ``Size: XS``、``Size: S`` 过滤 PR，以便在工作间隙快速审查小型 PR :)

Checkpatch
==========

有关 ``checkpatch.sh`` 工具本身的更多信息，请参阅
:doc:`/components/tools/checkpatch`。

此操作的目的是验证 PR 是否符合 :doc:`C 编码标准
</contributing/coding_style>`、不包含拼写错误，并符合
:doc:`提交信息格式 </contributing/making-changes>`。此外，还添加了对 CMake 文件的格式检查。

此操作的工作流文件非常短，位于
``.github/workflows/check.yml``。

构建
=====

这是 CI 流程中最复杂的步骤，也是持续时间最长的。它选择与更改文件关联的 NuttX 配置类别（``defconfig`` 文件），并并行构建所有配置。它还使用
``tools/refresh.sh`` 工具检查是否有配置需要规范化（有关更多信息，请参阅 :doc:`/components/tools/refresh`）。

此检查的工作流文件位于 ``.github/workflows/build.yml``。
此工作流的名称具有误导性，因为它不仅构建配置，还会规范化配置并在支持的架构上运行 :doc:`NTFC </testing/ntfc>` 测试。

构建工作流中执行的步骤包括：

1. 获取源代码：检出 ``nuttx`` 和 ``nuttx-apps`` 仓库。源文件作为构件添加到 GitHub Action 中，以便后续步骤可以下载。

2. 并行为 NuttX 支持的每个主机操作系统/环境选择要执行的构建。这些包括 Linux、MacOS、MSVC 和 MYSYS2。

   .. note::

      通常仅在 Linux 环境中执行。在所有主机选项上执行构建会消耗太多资源。

      MacOS 构建当前始终被跳过，但有时会为 MSVC 和 MYSYS2 执行测试。这些构建是 Linux 上执行的总构建的一小部分，但被选中以覆盖一定范围的架构。一些选定的构建包括 ``raspberrypi-pico:nsh``、
      ``rv-virt:nsh``、``sim:windows`` 等。

3. 为主机配置（即 Linux）选择构建后，将并行执行构建。例如，如果在步骤 2 中选定的 Linux
   构建为 ``arm-01``、``arm-02`` 和 ``arm-03``，此步骤将并行为每个类别执行构建测试。

   这涉及编译每个类别中包含的所有 ``defconfig`` 配置，并在它们上运行 ``tools/refresh.sh``。一些类别（如 ``sim-01``）还会执行 NTFC 测试。在这种情况下，NTFC 运行时测试将使用该架构指定的 ``citest/defconfig`` 配置运行。

4. 每个类别的构建完成后，将在每个类别的运行器中运行 ``make host_info`` 作为健全性检查。

5. 所有选定的 Linux 构建完成后，将执行树外（OOT）构建测试。这是使用 ``tools/ci/cibuild-oot.sh`` 完成的。

每个构建类别（``arm-01`` 等）都会生成一个构建构件，其中包含该类别所有生成的构建输出。这包括生成的 ``nuttx.bin``、``nuttx.elf``、``nuttx.hex`` 等二进制文件。您可以下载构件，将 NuttX 镜像刷写到目标设备并进行测试，以避免自己构建所有镜像！
