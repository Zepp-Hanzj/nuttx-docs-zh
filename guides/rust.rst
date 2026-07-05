===============
NuttX 中的 Rust
===============

.. warning::
    本指南正在开发中。NuttX 中的 Rust 支持是实验性的。

简介
============
NuttX 正在探索 Rust 集成，以提供内存安全保证和现代语言特性，同时保持其小体积和实时能力。

本指南涵盖：

- 为 NuttX 开发设置 Rust 工具链
- 使用 NuttX 构建 Rust 组件
- Rust 和 C 之间的互操作性
- 测试 Rust 组件

前提条件
=============
- 已安装 Rust 工具链（推荐 rustup）
- 已配置 NuttX 构建环境
- 具备 Rust 和 NuttX 开发的基本知识

支持的平台
===================
- AArch64
- ARMv7-A
- ARMv6-M
- ARMv7-M
- ARMv8-M
- RISCV32
- RISCV64
- X86
- X86_64

入门指南
===============
1. 安装 Rust 工具链并切换到 nightly

更多详情请参阅 Rust 官方安装指南：https://www.rust-lang.org/tools/install

.. code-block:: bash

    rustup toolchain install nightly
    rustup default nightly

2. 准备 NuttX 构建环境

请确保你有一个可用的 NuttX 构建环境，并且已合并或 cherry-pick 以下 PR：

- https://github.com/apache/nuttx-apps/pull/2487
- https://github.com/apache/nuttx/pull/15469

3. 启用必要的内核配置

请在你的 NuttX 配置中启用以下配置：

- CONFIG_FS_LARGEFILE
- CONFIG_TLS_NELEM = 16
- CONFIG_DEV_URANDOM

推荐使用 ``rv-virt:nsh`` 板配合 make 构建系统来测试 Rust 应用程序，因为该配置已被验证可以工作。

对于 ``rv-virt:nsh`` 板，你应该禁用 ``CONFIG_ARCH_FPU`` 配置，因为尚不支持带 FPU 的 RISCV32。

4. 启用示例应用程序

请在你的 NuttX 配置中启用示例应用程序：
- CONFIG_EXAMPLES_HELLO_RUST_CARGO

5. 构建并运行示例应用程序

构建 NuttX 镜像并在你的目标平台上运行：

.. code-block:: bash

    qemu-system-riscv32 -semihosting -M virt,aclint=on -cpu rv32 -smp 8 -bios nuttx/nuttx -nographic

    NuttShell (NSH) NuttX-12.8.0
    nsh> hello_rust_cargo
    {"name":"John","age":30}
    {"name":"Jane","age":25}
    Deserialized: Alice is 28 years old
    Pretty JSON:
    {
    "name": "Alice",
    "age": 28
    }
    Hello world from tokio!

恭喜！你已成功在 NuttX 上构建并运行了 Rust 应用程序。

指定目标 CPU 以进行优化
======================================
为了针对特定 CPU 优化你的 Rust 应用程序，你可以使用 ``RUSTFLAGS`` 环境变量来指定目标 CPU。这可以通过启用特定于 CPU 的优化来显著提高性能。

``RUSTFLAGS`` 环境变量在处理共享相同指令集架构 (ISA) 但具有不同微架构的 CPU 时特别有用。例如，Cortex-M33 和 Cortex-M55 都共享 ``thumbv8m.main`` 目标名称，但它们具有不同的性能特性和功能。通过指定实际的 CPU 核心，你可以利用目标 CPU 的特定优化和功能，从而获得更好的性能和效率。

例如，如果你的目标是 Cortex-M33，你可以按如下方式设置 ``RUSTFLAGS`` 环境变量：

.. code-block:: bash

    export RUSTFLAGS="-C target-cpu=cortex-m33"

对于 Cortex-M55，你需要使用：

.. code-block:: bash

    export RUSTFLAGS="-C target-cpu=cortex-m55"

这确保 Rust 编译器生成针对特定 CPU 核心优化的代码，而不是通用的 ISA。

1. 设置 ``RUSTFLAGS`` 环境变量以包含 ``--target-cpu`` 标志：

.. code-block:: bash

    export RUSTFLAGS="-C target-cpu=your_cpu_model"

将 ``your_cpu_model`` 替换为你所针对的特定 CPU 型号。例如，对于 ARM Cortex-M4，你需要使用：

.. code-block:: bash

    export RUSTFLAGS="-C target-cpu=cortex-m4"

2. 使用指定的目标 CPU 构建你的 NuttX 镜像：

.. code-block:: bash

    make

这将确保 Rust 编译器为指定的 CPU 生成优化的代码。

编辑器集成
==================
为了在 NuttX 中为 Rust 开发启用正确的 IDE 支持，你需要配置编辑器以正确识别 Rust 项目结构。本节重点介绍 VS Code 配合 rust-analyzer，这是最流行的设置。

1. 在你的 NuttX 工作区中创建或更新 ``.vscode/settings.json``：

.. code-block:: json

    {
        "rust-analyzer.linkedProjects": [
            "nuttx-apps/examples/rust/slint/Cargo.toml"
        ]
    }

2. （可选）如果你使用自定义目标规范，可以设置 ``rust-analyzer.cargo.target``：

.. code-block:: json

    {
        "rust-analyzer.cargo.target": "thumbv8m.main-nuttx-eabihf"
    }

.. note::
    由于 NuttX 现在支持 Rust 标准库 (std)，通常不需要指定精确的目标三元组。对于大多数情况，默认的宿主目标应该可以正常工作。

    如果你正在使用一个紧密依赖 NuttX 目标的 crate，你可以如上所示指定目标三元组以获得更准确的代码分析。

此配置有助于 rust-analyzer 理解你的项目结构，并在 NuttX 中使用 Rust 代码时提供准确的代码分析、自动补全和其他 IDE 功能。
