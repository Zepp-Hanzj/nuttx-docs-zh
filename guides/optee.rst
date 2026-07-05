=======================
与 OP-TEE 的接口
=======================

概述
========

NuttX 支持通过三种不同的传输方式与 OP-TEE OS 进行基本接口交互：
本地网络、RPMsg 和原生安全监控调用（SMC，在 ARM 上）。
任务可以通过 TEE（``/dev/tee#``）字符设备上的 IOCTL 与 OP-TEE 驱动
（进而与 OP-TEE OS）进行接口交互。此接口应允许使用/集成 libteec，
尽管 NuttX 官方不支持此功能，且不在本指南范围内。

驱动支持打开和关闭会话、分配和注册共享内存，
以及调用 OP-TEE 可信应用程序（TA）上的函数。
驱动还支持称为 RPC 的反向命令（TA -> 普通世界）。
一些 RPC 完全由内核驱动处理，而其他 RPC 则需要
TEE supplicant 用户空间进程正在运行（已打开 ``/dev/teepriv#``）。
与 libteec 类似，supplicant 不是官方支持的。

.. note::
   ``/dev/teepriv#`` 仅供 supplicant 使用，不应被任何其他 NuttX 应用程序使用。


启用 OP-TEE 驱动
==========================

驱动使用以下之一启用：

- ``CONFIG_DEV_OPTEE_LOCAL``
- ``CONFIG_DEV_OPTEE_RPMSG``
- ``CONFIG_DEV_OPTEE_SMC``

以上所有选项还需要 ``CONFIG_ALLOW_BSD_COMPONENTS`` 和 ``CONFIG_FS_ANONMAP``。
因此，要启用驱动，至少需要类似以下内容：

.. code-block::

  CONFIG_ALLOW_BSD_COMPONENTS=y
  CONFIG_DEV_OPTEE_SMC=y
  CONFIG_FS_ANONMAP=y

每种实现（本地、RPMsg 或 SMC）可能有进一步的依赖
（例如 RPMsg 需要 ``CONFIG_NET_RPMSG`` 等），
并可能有进一步的参数需要配置（例如通过 ``CONFIG_OPTEE_REMOTE_CPU_NAME``
配置 RPMsg 远程 CPU 名称）。

.. warning::
  ``CONFIG_DEV_OPTEE_SMC`` 仅在 arm64 上测试过。另外请注意，
  在配置了 ``CONFIG_ARM*_DCACHE_DISABLE=y`` 的情况下，
  你可能会遇到共享内存问题，具体取决于安全世界中数据缓存的状态。

如果启用了 ``CONFIG_DEV_OPTEE_SMC``，我们还可以使用
``CONFIG_DEV_OPTEE_SUPPLICANT`` 为 TEE supplicant 启用内核驱动。

可以通过查看 ``/dev/tee0`` 和 ``/dev/teepriv0``（用于 supplicant）
来验证驱动是否成功注册。例如，与系统中运行的 TEE OS 不兼容
将阻止 ``/dev/tee0`` 字符设备的注册。

支持的 IOCTL
================

所有 IOCTL 在失败时返回负错误码。除非另有说明（参见 ``TEE_IOC_SHM_ALLOC``），
否则所有 IOCTL 在成功时返回 0。

- ``TEE_IOC_VERSION``：查询 TEE 驱动的版本和功能。

  - 使用 ``struct tee_ioctl_version_data`` 获取版本和功能。
    此驱动支持 OP-TEE，因此你应该期望在 ``.impl_id`` 中仅收到
    ``TEE_IMPL_ID_OPTEE``，在 ``.impl_caps`` 中仅收到 ``TEE_OPTEE_CAP_TZ``。
    该驱动符合 GlobalPlatform 规范，你应该始终期望在 ``.gen_caps`` 中
    收到 ``TEE_GEN_CAP_GP | TEE_GEN_CAP_MEMREF_NULL``。
    如果使用 SMC 实现，驱动还支持共享内存注册，
    因此你还可以期望在 ``.gen_caps`` 中收到 ``TEE_GEN_CAP_REG_MEM``。

- ``TEE_IOC_OPEN_SESSION``：与可信应用程序打开会话。

  - 期望一个 ``struct tee_ioctl_buf_data`` 指针，指向一个
    ``struct tee_ioctl_open_session_arg`` 实例，至少设置 ``.uuid``。
    你通常可以使用 ``uuid_enc_be()`` 将 ``uuid_t`` 结构编码为
    ``.uuid`` 字段中期望的原始字节缓冲区。
    成功调用后，你可以在 ``.session`` 字段中获得会话标识符。

- ``TEE_IOC_CLOSE_SESSION``：关闭与可信应用程序的会话。

  - 期望一个 ``struct tee_ioctl_close_session_arg`` 指针，
    ``.session`` 字段设置为要关闭的会话标识符。

- ``TEE_IOC_INVOKE``：调用先前打开的可信应用程序会话上的函数。

  - 期望一个 ``struct tee_ioctl_buf_data`` 指针，指向一个
    ``struct tee_ioctl_invoke_arg`` 实例。你可以使用
    ``TEE_IOCTL_PARAM_SIZE()`` 宏来计算调用参数结构中
    ``struct tee_ioctl_param`` 参数的可变长度数组的大小。
    至少，接口期望设置 ``.func``、``.session``、``.num_params``
    和 ``.params`` 字段。可以选择设置 ``.cancel_id`` 以在需要时
    稍后取消此命令。
    你可能注意到 ``struct tee_ioctl_param`` 的字段名相当晦涩
    （``.a``、``.b``、``.c``）。这可以通过将来使用 union 来改进，
    但在那之前，请参阅 ``include/nuttx/tee.h`` 了解详情。
    简而言之，对于共享内存引用，``.a`` 是共享内存缓冲区中的偏移量，
    ``.b`` 是缓冲区大小，``.c`` 是共享内存标识符
    （由 ``TEE_IOC_SHM_ALLOC`` 或 ``TEE_IOC_SHM_REGISTER`` 返回的 ``.id`` 字段）。

- ``TEE_IOC_CANCEL``：取消当前调用的命令。

  - 期望一个 ``struct tee_ioctl_cancel_arg`` 指针，
    ``.session`` 和 ``.cancel_id`` 字段已设置。

- ``TEE_IOC_SHM_ALLOC``：在用户空间和安全 OS 之间分配共享内存。

  - 期望一个 ``struct tee_ioctl_shm_alloc_data`` 指针，
    ``.size`` 字段已设置，忽略 ``.flags`` 字段。成功返回时，
    返回内存文件描述符，可以对其使用 ``mmap()``（带 ``MAP_SHARED``）。
    它还在 ``.id`` 中返回用于内存引用的标识符。

- ``TEE_IOC_SHM_REGISTER``：向安全 OS 注册共享内存引用。

  - 期望一个 ``struct tee_ioctl_shm_register_data`` 实例的指针，
    除 ``.id`` 外所有字段已设置。``.flags`` 可以是 ``TEE_SHM_REGISTER``
    和 ``TEE_SHM_SEC_REGISTER`` 的任意组合，但不能是 ``TEE_SHM_ALLOC``。
    ``TEE_SHM_REGISTER`` 向驱动注册内存以在 ``/dev/tee#`` 字符设备关闭时
    自动清理（不是释放！）。
    ``TEE_SHM_SEC_REGISTER`` 向安全 OS 注册内存以供后续在 memref 中使用，
    如果同时指定了 ``TEE_SHM_REGISTER``，则在驱动关闭时自动注销。
    ``.addr`` 应指向要注册的（用户）内存，``.size`` 应指示其大小。
    在指定共享内存引用时可以使用返回的 ``.id`` 字段
    （``tee_ioctl_param.c`` 字段）。

- ``TEE_IOC_SUPPL_RECV``：从 OP-TEE 接收需要 supplicant 用户空间交互的 RPC 请求。

  - 期望一个 ``struct tee_ioctl_buf_data`` 实例的指针，
    ``.buf_ptr`` 字段指向用户分配的缓冲区，该缓冲区必须包含
    ``struct tee_iocl_supp_send/recv_arg``，后跟若干
    ``struct tee_ioctl_param`` 参数。``.buf_len`` 字段向内核传达
    该缓冲区的长度。如果用户传递的参数数量大于 ``OPTEE_MAX_PARAM_NUM``
    或小于 OP-TEE 发送的参数数量，ioctl 将失败。
    TEE supplicant 默认使用 5 个 ``struct tee_ioctl_param`` 参数。

- ``TEE_IOC_SUPPL_SEND``：响应从 OP-TEE 接收的需要 supplicant 用户空间交互的 RPC 请求。

  - 期望一个 ``struct tee_ioctl_buf_data`` 实例的指针，
    ``.buf_ptr`` 字段指向用户分配的缓冲区，该缓冲区必须包含
    ``struct tee_iocl_supp_send/recv_arg``，后跟若干
    ``struct tee_ioctl_param`` 参数。``.buf_len`` 字段向内核传达
    该缓冲区的长度。参数数量取决于 OP-TEE 期望的 RPC 响应大小。

典型用法
=============

#. 包含必要的头文件：

   .. code-block:: c

     #include <stdio.h>
     #include <stdlib.h>
     #include <fcntl.h>
     #include <unistd.h>
     #include <errno.h>
     #include <sys/ioctl.h>
     #include <nuttx/tee.h>
     #include <uuid.h>

#. 打开 TEE 字符设备

   .. code-block:: c

     int fd = open("/dev/tee0", O_RDONLY | O_NONBLOCK);

#. 检查版本和功能

   .. code-block:: c

     struct tee_ioctl_version_data ioc_ver;

     int ret = ioctl(fd, TEE_IOC_VERSION, (unsigned long)&ioc_ver);
     if (ret < 0)
       {
         printf("Failed to query TEE driver version and caps: %d, %s\n",
               ret, strerror(errno));
         return ret;
       }

     /* check ioc_ver accordingly */

#. 与可信应用程序打开会话

   .. code-block:: c

     const uuid_t *uuid = [...];
     struct tee_ioctl_open_session_arg ioc_opn = { 0 };
     struct tee_ioctl_buf_data ioc_buf;

     uuid_enc_be(&ioc_opn.uuid, uuid);

     ioc_buf.buf_ptr = (uintptr_t)&ioc_opn;
     ioc_buf.buf_len = sizeof(struct tee_ioctl_open_session_arg);

     ret = ioctl(fd, TEE_IOC_OPEN_SESSION, (unsigned long)&ioc_buf);
     if (ret < 0)
       {
         return ret;
       }

     /* use ioc_opn.session returned */

#. 调用可信应用程序的函数

   .. code-block:: c

     const size_t num_params = 1;
     struct tee_ioctl_invoke_arg *ioc_args;
     struct tee_ioctl_buf_data ioc_buf;
     size_t ioc_args_len;

     ioc_args_len = sizeof(struct tee_ioctl_invoke_arg) +
                    TEE_IOCTL_PARAM_SIZE(num_params);

     ioc_args = (struct tee_ioctl_invoke_arg *)calloc(1, ioc_args_len);
     if (!ioc_args)
       {
         return -ENOMEM;
       }

     ioc_args->func = <SOME_FUNCTION_ID>;
     ioc_args->session = ioc_opn.session;
     ioc_args->num_params = num_params;
     ioc_args->params[0].attr = TEE_IOCTL_PARAM_ATTR_TYPE_MEMREF_OUTPUT;

     ioc_buf.buf_ptr = (uintptr_t)ioc_args;
     ioc_buf.buf_len = ioc_args_len;

     ret = ioctl(fd, TEE_IOC_INVOKE, (unsigned long)&ioc_buf);
     if (ret < 0)
       {
         goto err_with_args;
       }

     /* use result (if any) in ioc_args->params */

#. 通过驱动分配共享内存

   .. code-block:: c

     struct tee_ioctl_shm_alloc_data ioc_alloc = { 0 };
     int memfd;
     void *shm;

     ioc_alloc.size = 1024;

     memfd = ioctl(fd, TEE_IOC_SHM_ALLOC, (unsigned long)&ioc_alloc);
     if (memfd < 0)
       {
         return memfd;
       }

     shm = mmap(NULL, ioc_alloc.size, PROT_READ | PROT_WRITE, MAP_SHARED,
                memfd, 0);
     if (shm == MAP_FAILED)
       {
         close(memfd);
         return -ENOMEM;
       }

#. 向驱动和安全 OS 注册共享内存

   .. code-block:: c

     /* The following will fail if TEE_GEN_CAP_REG_MEM is not reported in
      * the returned `ioc_ver.gen_caps` in step 1 above
      * Note: user memory used does not have to be allocated through IOCTL
      */

     struct tee_ioctl_shm_register_data ioc_reg = { 0 };

     ioc_reg.addr = (uintptr_t)<some user memory ptr>;
     ioc_reg.length = <user memory size>;

     memfd = ioctl(fd, TEE_IOC_SHM_REGISTER, (unsigned long)&ioc_reg);
     if (memfd < 0)
       {
         return ret;
       }

     /* use ioc_reg.id returned in OP-TEE parameters (e.g. open, invoke) */

     close(memfd);

#. 在调用中使用注册的共享内存

   .. code-block:: c

     const size_t num_params = 1;
     struct tee_ioctl_invoke_arg *ioc_args;
     struct tee_ioctl_buf_data ioc_buf;
     size_t ioc_args_len;

     ioc_args_len = sizeof(struct tee_ioctl_invoke_arg) +
                    TEE_IOCTL_PARAM_SIZE(num_params);

     ioc_args = (struct tee_ioctl_invoke_arg *)calloc(1, ioc_args_len);
     if (!ioc_args)
       {
         return -ENOMEM;
       }

     ioc_args->func = <SOME_FUNCTION_ID>;
     ioc_args->session = ioc_opn.session;
     ioc_args->num_params = num_params;
     ioc_args->params[0].attr = TEE_IOCTL_PARAM_ATTR_TYPE_MEMREF_OUTPUT;
     ioc_args->params[0].a = 0;
     ioc_args->params[0].b = ioc_reg.length;
     ioc_args->params[0].c = ioc_reg.id;

     ioc_buf.buf_ptr = (uintptr_t)ioc_args;
     ioc_buf.buf_len = ioc_args_len;

     ret = ioctl(fd, TEE_IOC_INVOKE, (unsigned long)&ioc_buf);
     if (ret < 0)
       {
         goto err_with_args;
       }

     /* use result (if any) in ioc_args->params */

#. 通过 TEE supplicant 的 OP-TEE 安全存储支持

   .. code-block:: shell

     optee_supplicant -f /data/tee > /dev/null &

这将在后台运行 OP-TEE supplicant，使用 ``/data/tee`` 作为 TEE 文件系统的目录。
输出重定向到 ``/dev/null`` 以抑制标准输出。确保 supplicant 的用户空间支持
已启用，且 ``/data`` 以读写方式挂载。

supplicant 运行后，安全存储对象可以由可信应用程序（TA）创建、检索和管理。
在典型的工作流中，在 NuttX 上运行的客户端应用程序（CA）调用 TA 中的命令，
该命令可能需要读取或创建持久对象。在这种情况下，OP-TEE 生成的某些 RPC
会从 CA 路由到 TEE supplicant 进行处理（前提是 supplicant 在后台运行）。
supplicant 处理完请求后，使用 ``TEE_IOC_SUPPL_SEND`` 进行响应，
内核驱动在 CA 的上下文中将此响应传回给 CA。

#. OP-TEE REE 时间请求

在此场景中，不需要用户空间 supplicant，因为响应可以直接由内核驱动处理。

OP-TEE 应用程序可以使用以下方式从 NuttX 时钟请求当前时间：

   .. code-block:: c

     TEE_GetREETime(&t);

NuttX 内核驱动将以 ``CLOCK_REALTIME`` 响应 TA，
它代表机器对当前墙钟时间的最佳猜测。
