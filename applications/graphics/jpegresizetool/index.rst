================
JPEG 调整大小工具
================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

一个使用 ``libjpeg`` 库参数调整 JPEG 图像大小的轻量级实用程序。该工具既可作为如何使用 ``libjpeg`` 的简单示例，也可作为实用的可脚本化的图像调整器。

使用方法
=====

.. code-block:: bash

   jpegresize <input.jpg> <output.jpg> <scale> <quality>

参数
---------

- **input.jpg** -- 输入 JPEG 图像的路径。
- **output.jpg** -- 调整大小后的输出图像路径。
- **scale** -- 缩小分母。目前，``libjpeg`` 支持 ``1``、``2``、``4`` 或 ``8`` 的值。例如，值 ``8`` 将图像尺寸缩小 8 倍。
- **quality** -- JPEG 质量因子，范围为 ``0`` 到 ``100``。
  - **80% 以上**：压缩几乎不可察觉。
  - **20% 左右**：出现强烈的压缩伪影。

示例
=======

将图像缩小 8 倍，质量为 20%：

.. code-block:: bash

   jpegresize /sd/IMAGES/000000a1.jpg /sd/TEMP/THUMBS/000000a1.jpg 8 20

注意事项
=====

- 此示例假设 ``libjpeg`` 在您的构建环境中可用。
- 该工具专为嵌入式系统或自动化脚本中的简单性和小占用空间图像处理而设计。
