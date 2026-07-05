=========================
线程本地存储
=========================

线程本地存储 (TLS) 是一种允许每个线程拥有自己变量副本的机制。这对于在线程中被多个函数使用但不应与其他线程共享的变量很有用。

在 NuttX 中使用 TLS 有几种方法：

1. 使用 POSIX 标准中的 ``pthread_key_create()`` 和 ``pthread_setspecific()``。这是最可移植的方法，但需要平台支持 pthreads。
2. 使用 C 标准中的 ``thread_local`` 或 ``__thread`` 关键字：https://gcc.gnu.org/onlinedocs/gcc/extensions-to-the-c-language-family/thread-local-storage.html

配置
=============

.. code-block:: console

    CONFIG_SCHED_THREAD_LOCAL  /* 启用原生线程本地存储支持 */


启用它以支持原生线程本地存储，这要求编译器配置了 ``--enable-tls`` 选项，如果编译器支持，这种方法更高效。

如果你的编译器支持它，你仍然需要进一步配置才能使用它：

1. 在 menuconfig 中启用 ``CONFIG_SCHED_THREAD_LOCAL``
2. 在链接器脚本中处理 ``tbss`` 和 ``tdata`` 段，你可以参考 rv-virt 中的示例

要确认你的编译器是否支持 TLS，你可以尝试以下命令：

.. code-block:: console

    arm-none-eabi-gcc --verbose
    COLLECT_GCC=arm-none-eabi-gcc
    COLLECT_LTO_WRAPPER=/home/huang/.local/pkg/arm/bin/../libexec/gcc/arm-none-eabi/13.3.1/lto-wrapper
    Target: arm-none-eabi
    Configured with: /data/jenkins/workspace/GNU-toolchain/arm-13/src/gcc/configure --target=arm-none-eabi --prefix=/data/jenkins/workspace/GNU-toolchain/arm-13/build-arm-none-eabi/install --with-gmp=/data/jenkins/workspace/GNU-toolchain/arm-13/build-arm-none-eabi/host-tools --with-mpfr=/data/jenkins/workspace/GNU-toolchain/arm-13/build-arm-none-eabi/host-tools --with-mpc=/data/jenkins/workspace/GNU-toolchain/arm-13/build-arm-none-eabi/host-tools --with-isl=/data/jenkins/workspace/GNU-toolchain/arm-13/build-arm-none-eabi/host-tools --disable-shared --disable-nls --disable-threads --disable-tls --enable-checking=release --enable-languages=c,c++,fortran --with-newlib --with-gnu-as --with-headers=yes --with-gnu-ld --with-native-system-header-dir=/include --with-sysroot=/data/jenkins/workspace/GNU-toolchain/arm-13/build-arm-none-eabi/install/arm-none-eabi --with-multilib-list=aprofile,rmprofile --with-pkgversion='Arm GNU Toolchain 13.3.Rel1 (Build arm-13.24)' --with-bugurl=https://bugs.linaro.org/
    Thread model: single
    Supported LTO compression algorithms: zlib
    gcc version 13.3.1 20240614 (Arm GNU Toolchain 13.3.Rel1 (Build arm-13.24))

然后你可以在输出中看到 ``--disable-tls``，这意味着你的编译器不支持 TLS。

在这种情况下，你仍然可以使用线程本地相关关键字，但它将由 libgcc 的 emutls 实现。
