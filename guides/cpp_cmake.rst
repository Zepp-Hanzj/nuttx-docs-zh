.. include:: /substitutions.rst
.. _cpp_cmake:

=======================
使用 CMake 的 C++ 示例
=======================

在某些情况下，开发者打算在已设置的硬件和配置上使用 NuttX 平台实现软件，且不允许进行更改。在这种情况下，与操作源码树的接触越少越好，仅将其用于应用程序。

目前可以采用以下几种方法：

* https://cwiki.apache.org/confluence/display/NUTTX/Building+NuttX+with+Applications+Outside+of+the+Source+Tree
* https://www.programmersought.com/article/61604062421/

我们看到 C++ 语言在嵌入式系统应用程序中的使用日益增多。CMake (https://www.cmake.org) 是用于构建 C++ 项目的首选构建系统。NuttX 支持基于 C++ 的项目。

使用 NuttX 的"构建为库"流程，可以使用 C++ 语言和 cmake 构建工具来构建 NuttX 应用程序。

本文档将展示如何使用此 cmake 重新实现 hellocpp 项目。

准备工作
===========

#. NuttX 基础编译更改

    对于此示例，加载配置 'stm32f4discovery:nsh' 进行构建（Linux 主机）

    .. code-block:: console

       $ cd nuttx
       $ ./tools/configure.sh -l stm32f4discovery:nsh

    有关 configure.sh 工具的更多信息，请参见 :ref:`quickstart/compiling_make:Initialize Configuration`。

    在 menuconfig 中，典型 NuttX 配置需要更改的主要要点如下：

    * RTOS 功能 -> 任务和调度 -> 应用程序入口点设为 'main'
    * 库例程 -> 拥有 C++ 编译器
    * 库例程 -> 拥有 C++ 初始化 -> C++ 库 -> 工具链 C++ 支持（您也可以选择基本版本或 LLVM 版本）
    * 库例程 -> 拥有 C++ 初始化 -> C++ 库 -> C++ 低级库选择 -> GNU 低级 libsupc++
    * 库例程 -> 语言标准 -> 选择您想要的版本 - 对于此示例我们将使用 "c++17"
    * 库例程 -> 启用异常支持 -> 启用 C++ 异常支持 - 对于此示例我们将选择它
    * 库例程 -> 启用 RTTI 支持 -> 启用 C++ RTTI 功能（如 dynamic_cast()/typeid()） - 对于此示例我们不启用它


    构建 NuttX 并生成导出

    .. code-block:: console

       $ make export

创建项目
====================

#. 创建项目文件结构

    项目结构组织如下：

    .. code-block:: console

       hellocpp/
       hellocpp/CMakeLists.txt
       hellocpp/nuttx-export-12.10.0/
       hellocpp/main.cpp
       hellocpp/HelloWorld.h
       hellocpp/HelloWorld.cpp

    目录 'nuttx-export-12.10.0' 是之前执行 make export 流程时创建的文件的解压内容。

#. 文件内容

* hellocpp/CMakeLists.txt

.. code-block:: cmake

    cmake_minimum_required(VERSION 3.12...3.31)

    project(HelloCpp
            VERSION 1.0
            DESCRIPTION "Hello world C++ NuttX"
    )

    set(CMAKE_CXX_STANDARD 17)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)

    set(SOURCE_FILES
            ${CMAKE_CURRENT_SOURCE_DIR}/HelloWorld.cpp
            ${CMAKE_CURRENT_SOURCE_DIR}/main.cpp
    )

    set(EXE_NAME "hello")
    add_executable(${EXE_NAME} ${SOURCE_FILES})

    add_custom_command(
            TARGET ${EXE_NAME}
            POST_BUILD
            COMMAND ${CMAKE_OBJCOPY} ARGS -S -O binary ${CMAKE_BINARY_DIR}/${EXE_NAME} ${CMAKE_BINARY_DIR}/${EXE_NAME}.bin


* hellocpp/main.cpp

.. code-block:: c++

    #include <memory>

    #include "HelloWorld.h"

    extern "C" int main(int, char*[])
    {
        auto pHelloWorld = std::make_shared<CHelloWorld>();
        pHelloWorld->HelloWorld();

        CHelloWorld helloWorld;
        helloWorld.HelloWorld();

        return 0;
    }


* hellocpp/HelloWorld.h

.. code-block:: c++

    #ifndef HELLOWORLD_H
    #define HELLOWORLD_H

    class CHelloWorld
    {
    public:
        CHelloWorld();
        ~CHelloWorld() = default;

        bool HelloWorld();

    private:
        int mSecret;
    };

    #endif

* hellocpp/HelloWorld.cpp

.. code-block:: c++

    #include <cstdio>
    #include <string>

    #include "HelloWorld.h"

    CHelloWorld::CHelloWorld()
    {
        mSecret = 42;
        std::printf("Constructor: mSecret=%d\n",mSecret);
    }


    bool CHelloWorld::HelloWorld()
    {
        std::printf("HelloWorld: mSecret=%d\n",mSecret);

        std::string sentence = "Hello";
        std::printf("TEST=%s\n",sentence.c_str());

        if (mSecret == 42)
        {
            std::printf("CHelloWorld: HelloWorld: Hello, world!\n");
            return true;
        }
        else
        {
            std::printf("CHelloWorld: HelloWorld: CONSTRUCTION FAILED!\n");
            return false;
        }
    }


构建
========

要启动构建，请使用 cmake 流程：

.. code-block:: console

    $ mkdir build
    $ cd build
    $ cmake .. -DCMAKE_TOOLCHAIN_FILE=../nuttx-export-12.10.0/scripts/toolchain.cmake
    $ make

生成两个二进制文件：一个 elf 文件（用于调试目的）和一个二进制文件（用于刷写到开发板）
