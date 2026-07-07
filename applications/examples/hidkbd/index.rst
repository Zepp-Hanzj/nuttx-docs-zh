================================
\`\`hidkbd\`\` USB 主机 HID 键盘
================================

这是一个用于调试/验证 USB 主机 HID 键盘类驱动的简单测试。

- ``CONFIG_EXAMPLES_HIDKBD_DEFPRIO`` – 等待线程的优先级。默认值：``50``。
- ``CONFIG_EXAMPLES_HIDKBD_STACKSIZE`` – 等待线程的栈大小。默认值：``1024``。
- ``CONFIG_EXAMPLES_HIDKBD_DEVNAME`` – 要使用的键盘设备名称。默认值：``/dev/kbda``。
- ``CONFIG_EXAMPLES_HIDKBD_ENCODED`` – 解码用户缓冲区中的特殊按键事件。在这种情况下，示例代码将使用 ``include/nuttx/input/kbd_codec.h`` 中定义的接口来解码返回的键盘数据。这些特殊键包括上下方向键、Home 和 End 键等。如果未定义此项，将只向用户提供 7 位可打印和控制 ASCII 字符。需要 ``CONFIG_HIDKBD_ENCODED`` 和 ``CONFIG_LIBC_KBDCODEC``。
