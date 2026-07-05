======================================
``nand`` - NAND Flash Device Simulator
======================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

为了在模拟器中测试与 NAND Flash 设备配合工作的文件系统，此模块提供了一个虚拟的 NAND Flash 设备及其驱动程序，以允许手动（或脚本化）测试，并提供了一个选项来记录底层执行的各种操作以及设备状态，包括设备中每个页面的读取、写入和擦除计数。

Structure of NAND Flash
=======================

大多数 NAND Flash 共享一个通用接口，由 `Open NAND Flash Interface (ONFI) <https://www.onfi.org/>`_ 指定。

在此上下文中需要的重要部分是，NAND Flash 被划分为多个块。每个块又被划分为多个页面。

这里是特别之处。如果您想擦除一个页面，您需要擦除它所属的*整个*块，即块是 NAND Flash 中最小的可擦除单元。然而，页面是可以写入数据或从中读取数据的最小单元。

为什么需要擦除操作？编程/擦除 (P/E) 周期规定，在写入数据之前需要先擦除页面（以及其所在的块）（先擦后写）。

每个页面有一个数据区域和一个备用区域。根据数据区域的大小，备用区域可能有不同的结构（方案）。所有必需的方案都在 ``/drivers/mtd/mtd_nandscheme.c`` 中定义（在 ``g_nand_sparescheme*`` 结构体中）。

由于 NAND Flash 的特性，在测试时，制造商可能认为某个块未通过某些测试，并通过在其中每个页面的备用区域（取决于数据区域的大小，因此也取决于备用区域的方案）的特定位置写入特定值，将其标记为**坏块**。

.. NOTE::
    * 虽然某些标记为坏块的块*可能仍然可以工作*，但不建议在其中存储任何数据。

    * 备用数据是记录一个块是否为坏块的**唯一**记录。请不要擦除它。

    * 某些块在持续使用后可能会变坏，需要由文件系统或驱动程序将其标记为坏块。

目前，此模拟器仅支持 512 B 大小的页面，这意味着它将遵循 ``g_nand_sparescheme512`` 方案作为其备用区域，因此坏块标记位于索引 ``5`` 处。

如果一个块*不是*坏块，它在坏块标记位置包含一个值 ``0xff``。任何其他值表示它是一个坏块。

RAM to Device (Lower Half)
==========================

由于这是一种模拟，使用运行模拟器的主机的 RAM 来创建设备。虽然操作速度远不及原始设备（RAM 的工作速度比实际设备快得多），但功能方面已尽可能保持一致。

首先，``/include/nuttx/mtd/nand.h`` 有一个结构 ``struct nand_dev_s``，定义了一个原始 NAND MTD 设备（最底层）。其字段 ``nand_dev_s->raw`` 的类型为 ``struct nand_raw_s *``（定义在 ``include/nuttx/mtd/nand_raw.h`` 中），这将保存原始设备的方法。主要有 3 个方法需要关注：

* eraseblock
* rawread
* rawwrite

遵循 NAND Flash 的功能，这三个方法在 ``/drivers/mtd/nand_ram.c`` 中以 ``nand_ram_*`` 实现，将 RAM 模拟为虚拟 NAND Flash。

虽然在实际设备中，备用区域跟随数据区域（在大多数方案中），但因为这是虚拟的，我们可以将两者分别放在两个单独的数组中，即 ``nand_ram_flash_data`` 和 ``nand_ram_flash_spare``，分别用于数据和备用。每个数组的元素数量与设备中的页面数量相同。

由于备用区域有一些可用的备用字节，一些空间被用作计数器，用于记录每个页面的读取/写入/擦除次数，从而为测试者提供虚拟设备磨损的清晰图像。

.. NOTE::
    ECC 扩展尚未实现，因此备用区域中的 ECC 位尚未被使用或正确初始化。

方法 ``nand_ram_initialize()`` 接受一个预分配的原始设备空间（类型为 ``struct nand_raw_s``，定义在 ``include/nuttx/mtd/nand_raw.h`` 中），并将这 3 个自定义方法以及设备信息（如页面大小、块大小等）附加到其中。这些构成了驱动程序的下半部分。

Upper Half
==========

方法 ``nand_ram_initialize()`` 还初始化了一个 ``struct mtd_dev_s *``（定义在 ``include/nuttx/mtd/mtd.h`` 中），并将其返回。此结构包含对我们自定义下半部分的引用（在 ``mtd_dev_s->raw`` 中），以及包含方法 ``nand_*`` 的上半部分（定义在 ``drivers/mtd/mtd_nand.c`` 中）。

Wrapper Over Upper Half
=======================

从 ``nand_ram_initialize()`` 接收的上半部分及其附加的下半部分包含以下 5 个上半部分方法：

* erase
* bread
* bwrite
* ioctl
* isbad
* markbad

每个驱动程序的上半部分需要在 NuttX 中注册后才能出现在设备列表中（在 ``/dev`` 中）。我们将注册一个包装器来替代先前获取的上半部分，以改进日志记录。包装器方法定义为 ``drivers/mtd/mtd_nandwrapper.c`` 中的 ``nand_wrapper_*``。

这里有一个复杂之处。实际上半部分是一个 MTD 设备，但更具体地说，它是一个 NAND MTD 设备，由 ``struct nand_dev_s`` 表示。由于其定义方式，``struct mtd_dev_s`` 构成了 ``struct nand_dev_s`` 的开头，因此它们可以相互进行类型转换（前提是所需的内存可访问）。我们的包装器是对 MTD 设备的包装，因此它本身也是一个 MTD 设备。MTD 设备方法接受一个 ``struct mtd_dev_s *dev`` 来描述设备本身（这是使用 ``register_mtddriver`` 注册的实际设备），其中包括其方法。我们的包装器方法也接收这样一个设备，其中包含包装器设备及其包装函数。但这样就无法访问实际的上半部分方法本身。因此，``dev`` 不是 ``struct nand_dev_s`` 类型，而是 ``struct nand_wrapper_dev_s`` 类型，它是 ``struct nand_dev_s`` 的超集，而 ``struct nand_dev_s`` 本身又是 ``struct mtd_dev_s`` 的超集。与前一种情况类似，``struct mtd_dev_s`` 构成了 ``struct nand_wrapper_dev_s`` 的开头，因此类型可以互换。

``drivers/mtd/mtd_nandwrapper.c`` 中的方法 ``nand_wrapper_*`` 在记录日志后将参数传递给实际的上半部分对应方法。*但传递给实际上半部分的设备仍然是包装器，而不是实际上半部分，因为上半部分方法可能在内部调用其他方法，我们也可能需要记录这些调用。*

Registering Device & Background Task
====================================

然后使用 ``register_mtddriver`` 注册此包装器，整个过程作为后台任务启动，以便在 ``nand`` 命令返回到 shell 后设备可以继续运行。

``nand`` 命令使用 ``task_create()`` 启动一个专用的 NuttX 任务，等待设备注册完成，然后将控制权返回给 shell。这使模拟器在后台保持活动状态，而不依赖于 ``fork()``，因为 ``fork()`` 的执行模型不适合模拟器使用的扁平构建中的这种长时间运行的初始化。

Known Issues
============

* ECC 尚未实现。
* MLC NAND Flash 尚未实现。
* 由于设备名称固定，不能有多个此虚拟设备的实例。
