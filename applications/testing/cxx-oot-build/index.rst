========================================
``cxx-oot-build`` Out-of-Tree Build Test
========================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``cxx-oot-build`` 测试自动化了使用 NuttX 导出 tarball 构建 **Out-of-Tree (OOT)** NuttX 项目的过程。其主要目的是验证 NuttX 可以在主源代码树之外构建，并防止 C++ 项目构建过程中的回归问题。

**重要提示：** 此测试使用了一个专门的 defconfig，该配置**不能**用于运行实际应用程序。它纯粹用于 CI/构建验证。功能性 OOT 项目应按照 :ref:`cpp_cmake` 中的说明进行配置。

测试脚本位于：

- ``tools/ci/cibuild-oot.sh``

### Out-of-Tree App Content

此 OOT 测试的源内容位于：

- ``apps/testing/cxx-oot-build``

其结构为构建 C++ NuttX 应用程序提供了基本骨架：

.. code-block:: text

    testing/cxx-oot-build
    ├── CMakeLists.txt
    ├── include
    │   └── HelloWorld.hpp
    └── src
        ├── HelloWorld.cpp
        └── main.cpp

这个最小结构包括：

- `CMakeLists.txt` - OOT C++ 项目的构建指令  
- `include/HelloWorld.hpp` - 示例头文件  
- `src/HelloWorld.cpp` - 示例类实现  
- `src/main.cpp` - 测试应用程序的入口点  

### How to Run the Test

从 NuttX CI 工具目录执行测试脚本：

    cd ${NUTTX_PATH}/tools/ci
    ./cibuild-oot.sh

该脚本执行以下步骤：

1. 为 ``cxx-oot-build`` 板级配置 NuttX
2. 构建 NuttX 的导出 tarball
3. 通过解压 tarball 准备 Out-of-Tree 项目
4. 使用 CMake 构建 OOT 项目
5. 验证输出二进制文件 ``oot`` 和 ``oot.bin`` 是否存在

### Expected Output

成功时，您应该看到：

    ✅ SUCCESS: OOT build completed. Output:
    -rwxrwxr-x 1 <user> <group> 94K <date> /path/to/oot
    -rwxrwxr-x 1 <user> <group> 46K <date> /path/to/oot.bin

如果任何步骤失败，脚本将立即退出并显示错误消息。

### Notes

- 此测试不需要额外的配置选项。``cxx-oot-build`` defconfig 已预先配置为可以正确构建，但**不适合运行应用程序**。
- 对于功能性 OOT 构建，请按照 :doc:`这里 </guides/cpp_cmake>` 记录的流程操作。
