=========================================
NTFC（NuttX 社区测试框架）
=========================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NTFC 支持通过 :doc:`模拟器
</platforms/sim/sim/index>`、QEMU 和串口连接的真实硬件进行 NuttX 自动化测试。该框架能够自动检测 NuttX 镜像中的可用应用程序，并使用基于 pytest 的测试用例执行适用的测试。

框架和官方测试用例可在以下地址获取：

- https://github.com/apache/nuttx-ntfc
- https://github.com/apache/nuttx-ntfc-testing

详细文档可在框架仓库中找到。

CI 迁移到 NTFC 的工作正在进行中。当前使用 NTFC 的配置包括：

- :doc:`risc-v/qemu-rv </platforms/risc-v/qemu-rv/index>`：``rv-virt/citest64``
- :doc:`risc-v/qemu-rv </platforms/risc-v/qemu-rv/index>`：``rv-virt/citest``
- :doc:`sim/sim </platforms/sim/sim/index>`：``sim/citest``
- :doc:`arm/imx6 </platforms/arm/imx6/index>`：``sabre-6quad/citest``
- :doc:`arm64/qemu </platforms/arm64/qemu/boards/qemu-armv8a/index>`：``qemu-armv8a/citest``
- :doc:`arm64/qemu </platforms/arm64/qemu/boards/qemu-armv8a/index>`：``qemu-armv8a/citest_smp``

NTFC 将测试日志导出为 CI 构件。这允许从 CI 直接下载所有启用了 ``citest`` 配置的目标的测试日志（包括
:doc:`ostest </applications/testing/ostest/index>` 输出）。
