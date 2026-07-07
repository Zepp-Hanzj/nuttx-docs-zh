=============
Shared Memory
=============

共享内存接口仅在 NuttX 内核构建（``CONFIG_BUILD_KERNEL=y``）中可用。
这些接口支持可在多个用户进程之间共享的用户内存区域。
用户接口在标准头文件 ``include/sys/shm.h`` 中提供。
除两个用于配置平台特定 MMU 资源的底层函数外，
所有支持共享内存的逻辑都在 NuttX 内核中实现。
这些接口描述如下：

.. c:function:: int up_shmat(FAR uintptr_t *pages, unsigned int npages, uintptr_t vaddr)

  将共享内存区域映射（附加）到用户虚拟地址。

  :param pages: 指向物理地址数组第一个元素的指针，每个元素对应一页内存。
  :param npages: 要映射的物理页列表中的页数。
  :param vaddr: 对应于（连续）虚拟地址区域起始位置的虚拟地址。

  :return: 成功返回零（OK）；失败返回负的 errno 值。

.. c:function:: int up_shmdt(uintptr_t vaddr, unsigned int npages)

  从用户虚拟地址取消映射（分离）共享内存区域。

  :param vaddr: 对应于（连续）虚拟地址区域起始位置的虚拟地址。
  :param npages: 要取消映射的页数。

  :return: 成功返回零（OK）；失败返回负的 errno 值。
