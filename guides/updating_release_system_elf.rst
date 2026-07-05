===========================================
使用 ELF 程序更新发布系统
===========================================

.. warning:: 
    迁移自： 
    https://cwiki.apache.org/confluence/display/NUTTX/Updating+a+Release+System+with+ELF+Programs

.. warning:: 
    迁移自： 
    https://cwiki.apache.org/confluence/display/NUTTX/Updating+a+Release+System+with+ELF+Programs

你可以通过添加 ELF 程序来增强已发布嵌入式系统的功能，这些程序可以从文件系统加载。这些程序可以存储在 SD 卡上或下载到板载 SPI FLASH 中，允许轻松更新或扩展系统的固件。

有两种方法可以实现这一点：

部分链接
================
这描述了构建部分链接的、可重定位的 ELF 程序，该程序依赖于 FLASH 中基础固件提供的符号表。

参考：
- 参见 :doc:`部分链接 ELF 程序 <partially_linked_elf>`

完全链接
============
这描述了构建完全链接的、可重定位的 ELF 程序，该程序不依赖于任何符号表信息。

参考：
- 参见 :doc:`完全链接 ELF 程序 <fully_linked_elf>`
