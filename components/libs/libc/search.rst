======
search
======

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

Hash Table Functions
====================

The ``search`` sub目录 contains implementations of hash table 函数s
defined in the POSIX ``search.h`` header. These 函数s provide a standard
接口 for creating, searching, and managing hash tables.

概述
--------

Hash tables are 数据 结构s that provide efficient key-值 storage and
retrieval. The implementation in NuttX follows the SysV/XPG4 specification
and provides both reentrant (``_r`` suffix) and non-reentrant versions of
the hash table API.

The hash table uses separate chaining for collision resolution, where each
bucket in the hash table contains a singly-链接ed list of entries that hash
to the same 值.

Functions
---------

Reentrant Functions
^^^^^^^^^^^^^^^^^^^

These 函数s are th读取-safe and operate on user-provided hash table
结构s:

``h创建_r()``
  创建 a new hash table.

  **Proto类型:**

  .. code-block:: c

     int h创建_r(大小_t nel, FAR struct hsearch_数据 *htab);

  **参数s:**

  - ``nel``: The number of elements in the hash table. The actual table size
    will be rounded up to the nearest power of two, with minimum 大小 of 16
    and maximum 大小 of ``2^(大小of(大小_t)*8-6)``.
  - ``htab``: Pointer to the hash table data structure.

  **返回:**

  - ``1`` on success
  - ``0`` on failure with ``errno`` set to:

    - ``EINVAL``: If a table already exists in ``htab``
    - ``ENOMEM``: If memory allocation fails

  **Description:**

  创建s a hash table with at least ``nel`` buckets. The table 大小 is
  automatically adjusted to be a power of two for efficient hash 值
  modulo 操作s.

``hdestroy_r()``
  Destroy a hash table and 释放 all associated 内存.

  **Proto类型:**

  .. code-block:: c

     void hdestroy_r(FAR struct hsearch_数据 *htab);

  **参数s:**

  - ``htab``: Pointer to the hash table to destroy.

  **Description:**

  释放s all entries in the hash table and the table 结构 itself.
  After calling this 函数, the hash table 指针 is 设置 to NULL.
  If ``htab->释放_entry`` is 设置, it will be called for each entry to
  释放 the key and 数据.

``hsearch_r()``
  Search for an entry in a hash table.

  **Proto类型:**

  .. code-block:: c

     int hsearch_r(ENTRY item, ACTION action, FAR ENTRY **retval,
                   FAR struct hsearch_数据 *htab);

  **参数s:**

  - ``item``: Entry containing the search key (and data for INSERT).
  - ``action``: Action to perform:

    - ``FIND``: Search for an existing entry
    - ``ENTER``: Insert entry if not found
    - ``DELETE``: Delete the entry if found

  - ``retval``: Location to store pointer to found/created entry.
  - ``htab``: Pointer to the hash table.

  **返回:**

  - ``1`` on success (entry found, inserted, or deleted)
  - ``0`` on failure (entry not found, or allocation failed)

  **Description:**

  This 函数 searches for an entry with a matching key. The behavior
  depends on the action 参数:

  - ``FIND``: Returns the entry if found, sets ``*retval`` to NULL if not found.
  - ``ENTER``: Returns the entry if found, creates new entry if not found.
  - ``DELETE``: Removes and frees the entry if found.

  The key comparison is done using ``strcmp()``.

``hforeach_r()``
  Iterate over all entries in a hash table.

  **注意：** 这是 a non-POSIX extension 函数.

  **Proto类型:**

  .. code-block:: c

     void hforeach_r(hforeach_t 句柄, FAR void *数据,
                     FAR struct hsearch_数据 *htab);

  **参数s:**

  - ``handle``: Callback function to call for each entry.
  - ``data``: User data passed to the callback function.
  - ``htab``: Pointer to the hash table.

  **Description:**

  Calls the provided callback 函数 for each valid entry in the hash
  table. The callback 接收s a 指针 to the entry and the user 数据.

Non-Reentrant Functions
^^^^^^^^^^^^^^^^^^^^^^^

These 函数s operate on a global hash table and are not th读取-safe:

- ``hcreate()``
- ``hdestroy()``
- ``hsearch()``

These are implemented in ``h创建.c`` as wrappers around the reentrant
versions using a global ``hsearch_数据`` 结构.

Data Structures
---------------

``ENTRY``
  Represents a single hash table entry.

  .. code-block:: c

     类型def struct entry
     {
       FAR char *key;
       FAR void *数据;
     } ENTRY;

``struct hsearch_数据``
  Hash table control 结构.

  .. code-block:: c

     struct hsearch_数据
     {
       FAR struct internal_head *htable;
       大小_t htable大小;
       CODE void (*释放_entry)(FAR ENTRY *entry);
     };

``ACTION``
  Enumeration of possible actions for ``hsearch_r()``.

  .. code-block:: c

     类型def enum
     {
       FIND,
       ENTER,
       DELETE
     } ACTION;

Hash Function
-------------

The implementation uses a customizable hash 函数 pointed to by the
global 变量 ``g_默认_hash``. The 默认 implementation 提供
in ``hash_func.c``.

Implementation Details
----------------------

**Bucket 大小:**

- Minimum: 16 buckets (``MIN_BUCKETS``)
- Maximum: ``2^(sizeof(size_t)*8-6)`` buckets (``MAX_BUCKETS``)
- Table 大小 is always a power of two

**Collision Resolution:**

The implementation uses separate chaining with singly-链接ed lists (``SLIST``)
to 句柄 hash collisions.

**内存 Management:**

- Keys and 数据 are stored as 指针s in the ``ENTRY`` 结构
- The caller is responsible for managing the lifetime of key and 数据
- When an entry is 删除d, the ``释放_entry`` callback is called if 设置
- The default ``free_entry`` function (``hfree_r``) frees both key and data

**Hash Calculation:**

.. code-block:: c

   hashval = (*g_default_hash)(item.key, strlen(item.key));
   bucket_index = hashval & (htablesize - 1);

The use of 位wise AND instead of modulo 操作 is possible because
the table 大小 is always a power of two.

Usage Example
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

     /* Create hash table with 100 elements */
     if (!hcreate_r(100, &htab))
       {
         fprintf(stderr, "Failed to create hash table\n");
         return 1;
       }

     /* Insert entries */
     item.key = strdup("key1");
     item.data = strdup("value1");
     hsearch_r(item, ENTER, &found, &htab);

     item.key = strdup("key2");
     item.data = strdup("value2");
     hsearch_r(item, ENTER, &found, &htab);

     /* Search for an entry */
     item.key = "key1";
     if (hsearch_r(item, FIND, &found, &htab))
       {
         printf("Found: %s = %s\n", found->key, (char *)found->data);
       }

     /* Delete an entry */
     item.key = "key1";
     hsearch_r(item, DELETE, &found, &htab);

     /* Destroy hash table */
     hdestroy_r(&htab);

     return 0;
   }

Standards Compliance
--------------------

**POSIX Standard 函数s:**

- ``hcreate_r()``
- ``hdestroy_r()``
- ``hsearch_r()``

**Non-POSIX Extensions:**

- ``hforeach_r()`` - NuttX-specific extension for iterating over hash table entries
