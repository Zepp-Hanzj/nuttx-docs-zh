======
search
======

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

哈希表函数
====================

``search`` 子目录包含 POSIX ``search.h`` 头文件中定义的哈希表函数的实现。
这些函数提供了创建、搜索和管理哈希表的标准接口。

概述
--------

哈希表是一种提供高效键值存储和检索的数据结构。NuttX 中的实现遵循
SysV/XPG4 规范，提供可重入（``_r`` 后缀）和不可重入两种版本的哈希表 API。

哈希表使用链地址法进行冲突解决，其中哈希表中的每个桶包含一个单链表，
存储哈希到相同值的条目。

函数
---------

可重入函数
^^^^^^^^^^^^^^^^^^^

这些函数是线程安全的，操作用户提供的哈希表结构：

``hcreate_r()``
  创建一个新的哈希表。

  **原型：**

  .. code-block:: c

     int hcreate_r(size_t nel, FAR struct hsearch_data *htab);

  **参数：**

  - ``nel``：哈希表中的元素数量。实际表大小将向上舍入到最近的 2 的幂，
    最小为 16，最大为 ``2^(sizeof(size_t)*8-6)``。
  - ``htab``：指向哈希表数据结构的指针。

  **返回值：**

  - 成功返回 ``1``
  - 失败返回 ``0``，并设置 ``errno``：

    - ``EINVAL``：如果 ``htab`` 中已存在表
    - ``ENOMEM``：如果内存分配失败

  **说明：**

  创建一个至少包含 ``nel`` 个桶的哈希表。表大小会自动调整为 2 的幂，
  以便高效地进行哈希值取模运算。

``hdestroy_r()``
  销毁哈希表并释放所有相关内存。

  **原型：**

  .. code-block:: c

     void hdestroy_r(FAR struct hsearch_data *htab);

  **参数：**

  - ``htab``：指向要销毁的哈希表的指针。

  **说明：**

  释放哈希表中的所有条目以及表结构本身。调用此函数后，哈希表指针
  将被设置为 NULL。如果设置了 ``htab->free_entry``，则会对每个条目
  调用它以释放键和数据。

``hsearch_r()``
  在哈希表中搜索条目。

  **原型：**

  .. code-block:: c

     int hsearch_r(ENTRY item, ACTION action, FAR ENTRY **retval,
                   FAR struct hsearch_data *htab);

  **参数：**

  - ``item``：包含搜索键的条目（INSERT 时同时包含数据）。
  - ``action``：要执行的操作：

    - ``FIND``：搜索现有条目
    - ``ENTER``：如果未找到则插入条目
    - ``DELETE``：如果找到则删除条目

  - ``retval``：存储找到/创建的条目指针的位置。
  - ``htab``：指向哈希表的指针。

  **返回值：**

  - 成功返回 ``1``（条目已找到、已插入或已删除）
  - 失败返回 ``0``（条目未找到或分配失败）

  **说明：**

  此函数搜索具有匹配键的条目。行为取决于 action 参数：

  - ``FIND``：如果找到则返回条目，未找到则将 ``*retval`` 设为 NULL。
  - ``ENTER``：如果找到则返回条目，未找到则创建新条目。
  - ``DELETE``：如果找到则移除并释放条目。

  键的比较使用 ``strcmp()`` 完成。

``hforeach_r()``
  遍历哈希表中的所有条目。

  **注意：** 这是一个非 POSIX 扩展函数。

  **原型：**

  .. code-block:: c

     void hforeach_r(hforeach_t handle, FAR void *data,
                     FAR struct hsearch_data *htab);

  **参数：**

  - ``handle``：对每个条目调用的回调函数。
  - ``data``：传递给回调函数的用户数据。
  - ``htab``：指向哈希表的指针。

  **说明：**

  对哈希表中的每个有效条目调用提供的回调函数。回调函数接收
  条目的指针和用户数据。

不可重入函数
^^^^^^^^^^^^^^^^^^^^^^^

这些函数操作全局哈希表，不是线程安全的：

- ``hcreate()``
- ``hdestroy()``
- ``hsearch()``

它们在 ``hcreate.c`` 中作为可重入版本的包装器实现，使用全局
``hsearch_data`` 结构。

数据结构
---------------

``ENTRY``
  表示单个哈希表条目。

  .. code-block:: c

     typedef struct entry
     {
       FAR char *key;
       FAR void *data;
     } ENTRY;

``struct hsearch_data``
  哈希表控制结构。

  .. code-block:: c

     struct hsearch_data
     {
       FAR struct internal_head *htable;
       size_t htablesize;
       CODE void (*free_entry)(FAR ENTRY *entry);
     };

``ACTION``
  ``hsearch_r()`` 可能操作的枚举。

  .. code-block:: c

     typedef enum
     {
       FIND,
       ENTER,
       DELETE
     } ACTION;

哈希函数
-------------

实现使用由全局变量 ``g_default_hash`` 指向的可自定义哈希函数。
默认实现在 ``hash_func.c`` 中提供。

实现细节
----------------------

**桶大小：**

- 最小：16 个桶（``MIN_BUCKETS``）
- 最大：``2^(sizeof(size_t)*8-6)`` 个桶（``MAX_BUCKETS``）
- 表大小始终为 2 的幂

**冲突解决：**

实现使用单链表（``SLIST``）的链地址法处理哈希冲突。

**内存管理：**

- 键和数据以指针形式存储在 ``ENTRY`` 结构中
- 调用者负责管理键和数据的生命周期
- 删除条目时，如果设置了 ``free_entry`` 回调则会调用它
- 默认的 ``free_entry`` 函数（``hfree_r``）同时释放键和数据

**哈希计算：**

.. code-block:: c

   hashval = (*g_default_hash)(item.key, strlen(item.key));
   bucket_index = hashval & (htablesize - 1);

使用按位与运算而非取模运算是可行的，因为表大小始终为 2 的幂。

使用示例
-------------

.. code-block:: c

   #include <search.h>
   #include <stdio.h>
   #include <string.h>

   int main(void)
   {
     struct hsearch_data htab = {0};
     ENTRY item;
     ENTRY *found;

     /* 创建包含 100 个元素的哈希表 */
     if (!hcreate_r(100, &htab))
       {
         fprintf(stderr, "Failed to create hash table\n");
         return 1;
       }

     /* 插入条目 */
     item.key = strdup("key1");
     item.data = strdup("value1");
     hsearch_r(item, ENTER, &found, &htab);

     item.key = strdup("key2");
     item.data = strdup("value2");
     hsearch_r(item, ENTER, &found, &htab);

     /* 搜索条目 */
     item.key = "key1";
     if (hsearch_r(item, FIND, &found, &htab))
       {
         printf("Found: %s = %s\n", found->key, (char *)found->data);
       }

     /* 删除条目 */
     item.key = "key1";
     hsearch_r(item, DELETE, &found, &htab);

     /* 销毁哈希表 */
     hdestroy_r(&htab);

     return 0;
   }

标准符合性
--------------------

**POSIX 标准函数：**

- ``hcreate_r()``
- ``hdestroy_r()``
- ``hsearch_r()``

**非 POSIX 扩展：**

- ``hforeach_r()`` - NuttX 特有的扩展，用于遍历哈希表条目
