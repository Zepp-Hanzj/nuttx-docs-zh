=========================================
调试时禁用栈转储
=========================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

.. warning:: 
    迁移自： 
    https://cwiki.apache.org/confluence/display/NUTTX/Disabling+the+Stack+Dump+During+Debugging

栈转储例程会在调试期间使 GDB 的输出变得混乱。要禁用它，请在板级配置的 defconfig 文件中设置此配置选项：

.. code-block:: c

    CONFIG_ARCH_STACKDUMP=n