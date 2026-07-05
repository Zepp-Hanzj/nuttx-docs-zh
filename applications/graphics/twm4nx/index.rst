===================================
``twm4nx`` 标签窗口管理器 (TWM)
===================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

Twm4Nx 是将 twm（标签窗口管理器，也称 Tom's 窗口管理器）版本 ``1.0.10`` 移植到 NuttX NX 窗口服务器的产物。不，"移植"这个词并不准确。它是从内到外对 TWM 进行的重新设计，以适配 NuttX NX 服务器。Twm4Nx 这个名称反映了这一渊源。但 Twm4Nx 更像是对 TWM 的致敬，而非简单的移植。

原始的 TWM 基于 X11，提供了丰富的功能。TWM 提供了标题栏、异形窗口、多种形式的图标管理、用户自定义宏函数、点击输入和指针驱动的键盘焦点、图形上下文以及用户指定的按键和指针按钮绑定等功能。

另一方面，Twm4Nx 基于 NuttX NX 服务器，该服务器仅提供相对最基本的支撑。额外的绘图支持来自 NuttX NxWidgets 库（这也促成了向 C++ 的转变）。

Twm4Nx 进行了大幅精简，面向资源极为有限的小型嵌入式系统。例如，不假设文件系统的可用性；不使用 ``.twmrc`` 文件。不使用位图（字体除外）。

TWM 的许可证可能与 NuttX 使用的 BSD 许可证兼容。原始 TWM 许可证要求在每个文件中保留版权声明以及原始许可证的完整副本，您可以在本目录的 ``COPYING`` 文件中找到该许可证。

状态
------

进展
~~~~~~~~

- ``2019-04-28`` 此次移植非常艰难。由于依赖 X11 功能（或仅仅因为不清楚如何使用），大量 TWM 逻辑被移除。替代逻辑仅基本到位，但仍需完成更多工作才能拥有完整的系统（因此标记为 ``EXPERIMENTAL``）。需要完成的工作包括：

  1. 右键点击应弹出窗口列表（类似图标管理器？）
  2. 为实现类似 TWM 的行为，窗口框架和工具栏应在窗口获得焦点时高亮显示。
  3. 在工具栏上右键点击应弹出窗口特定菜单。

- ``2019-05-02`` 取得了一些测试进展。系统启动并连接初始化了 VNC 窗口。但由于某种原因，VNC 客户端断开了连接。服务器不再连接，因此 Twm4Nx 阻塞并最终挂起。

- ``2019-05-08`` 放弃 VNC 接口后，使用直接硬件帧缓冲效果好多了。背景正确显示，图标管理器正确出现在右上角。图标管理器窗口可以最小化或恢复。图标管理器窗口可以通过工具栏标题栏拖拽并在窗口上移动（在用于测试的特定硬件上移动不太流畅）。

- ``2019-05-10`` 在背景上左键点击可弹出主菜单。目前只有两个选项：_Desktop_ 将最小化所有窗口，"Twm4Nx Icon Manager" 将恢复并/或将图标管理器窗口提升到层级顶部。后一个选项仅在桌面非常拥挤时才有意义。

- ``2019-05-13`` 添加了 NxTerm 应用程序。如果通过 ``CONFIG_TWM4XN_NXTERM`` 启用，主菜单中将出现 _NuttShell_ 条目。点击后将在 Twm4Nx 窗口中启动一个 NSH 会话。

- ``2019-05-14`` 现在可以在桌面上移动图标了。包含避免与其他图标和背景图像碰撞的逻辑。后者是一个问题。背景图像部件需要移除；它可能会遮挡桌面图标。我们需要直接在背景上绘制图像，不使用部件。

- ``2019-05-15`` 调整大小功能现在在 Twm4Nx 中似乎正常工作了。

- ``2019-05-20`` 校准屏幕现已就位。

- ``2019-05-21`` 添加了 ``CONTEMPORARY`` 主题。仍有一些小问题。

- ``2019-06-01`` 一个复古的模拟段式 LCD 时钟现已就位。

使用指南
------

图标管理器
~~~~~~~~~~~~

- 启动时，仅显示图标管理器窗口。图标管理器是 TWM 中更常见桌面图标的替代方案。目前 Twm4Nx 同时支持桌面图标和图标管理器。

  每当从主菜单启动新应用程序时，其名称会显示在图标管理器中。选择名称将恢复该窗口，或将其提升到显示顶部。

主菜单
~~~~~~~~~

- 在背景上任何空白位置（中心图像或其他图标除外）触摸/点击将弹出主菜单。选项：

  - Desktop。最小化所有窗口并显示桌面。
  - Twm4Nx Icon Manager。恢复并/或将图标管理器提升到显示顶部。
  - Calibration。执行触摸屏重新校准。
  - Clock。在窗口中启动时钟实例。使用 ``apps/graphics/slcd`` 中的复古 LCD 模拟。
  - NuttShell。启动在 NxTerm 中运行的 NSH 实例。

- 选择终端菜单选项后，所有窗口将关闭。

窗口工具栏
~~~~~~~~~~~~~~~

- 大多数窗口顶部都有工具栏。它是可选的，但在大多数窗口中使用。
- 工具栏包含窗口标题和零到 4 个按钮：

  - 右侧：可能显示菜单按钮。在当前实现中，菜单按钮未被使用，始终被隐藏。
  - 左侧：最左侧是 (1) 终止按钮（如果存在）。如果存在，点击时将关闭窗口。并非所有窗口都可以关闭。例如，您无法关闭图标管理器或菜单窗口。然后是 (2) 调整大小按钮。如果存在且被选中，则开始下面描述的调整大小流程。在此之前可能有一个最小化按钮，用于将窗口最小化为图标。

移动窗口
~~~~~~~~~~~~~~~

- 拖拽工具栏中的标题，将窗口移动到所需位置。

调整窗口大小
~~~~~~~~~~~~~~~~~

- 窗口必须具有带方块的绿色调整大小按钮，否则无法调整大小。
- 按下调整大小按钮。左上角应弹出一个小窗口，显示当前窗口大小。
- 在窗口中任意位置（非工具栏）触摸并滑动手指。调整大小窗口将显示新大小，但显示不会进行其他更新。认为持续的大小更新会使低端 MCU 不堪重负。支持的操作包括：

  - 向右移动增加窗口宽度
  - 向左移动减少窗口宽度
  - 向下移动增加窗口高度
  - 向上移动减少窗口高度
  - 其他方向的移动将同时影响窗口的高度和宽度。

- **注意**：调整大小期间，来自所有其他窗口的非关键事件将被忽略。

主题
~~~~~~

- 配置系统支持两种主题：

  - ``CONFIG_TWM4NX_CLASSIC`` -- 带有深色主色调的强边框窗口。令人联想起 Windows 98。
  - ``CONFIG_TWM4NX_CONTEMPORARY`` -- 采用柔和色调的无边框窗口，呈现更现代的外观。

问题
~~~~~~

``2019-05-16`` Twm4Nx 处于非常完整的状态，但成熟度大约仅为 _alpha_。您应该预期会遇到一些未记录的问题。请报告您遇到的任何问题。

以下是所有已知问题和缺失的功能：

TWM 兼容性问题：

1. 在 Twm4Nx 中，调整大小的工作方式略有不同。
2. 右键点击应弹出窗口列表。
3. 为实现类似 TWM 的行为，窗口框架和工具栏应在窗口获得焦点时高亮显示。
4. 在工具栏上右键点击应弹出窗口特定的菜单。

目前没有解决这些兼容性问题的近期计划。

其他问题/错误。Twm4Nx 正在逐步成熟并趋于稳定。尽管如此，仍有一些问题和未测试的功能需要解决：

1. 图标拖拽移动包含避免与其他图标和背景图像碰撞的逻辑。后者是一个问题。我们需要直接在背景上绘制图像，不使用部件。
2. ``CONTEMPORARY`` 主题的工具栏中存在一些颜色瑕疵。看起来像是在工具栏部件周围绘制了边框（尽管配置为无边框）。
3. 大多数 Twm4Nx 配置设置硬编码在 ``*_config.hxx`` 头文件中。这些都需要提取出来并通过 Kconfig 文件使其可访问。
4. 当打开大量 NxTerm 窗口（约 15 个）时，会出现一些奇怪的行为。具体来说，无法在窗口中启动 NSH，导致窗口显示为空白。所有其他行为似乎正常。最可能的原因是某些 NxTerm 资源分配静默失败，导致处于不可用状态。用于测试的板子有 128MB SDRAM，因此内存可能不是限制因素。然而，这些是 RAM 支持的窗口，将使用大量内存。主要问题在于，可能应以某种方式管理窗口数量，以确保最终用户在资源使用率高时不会遇到异常行为。
5. 带子菜单的菜单尚未验证。当前代码库中没有使用子菜单，因此当选择子菜单项时可能会出现问题：该菜单及其所有上级菜单都应关闭。
6. 工具栏最左侧可能有一个可选的 MENU 按钮。在当前代码库中，没有任何窗口使用它，因此未经验证。在生成和路由 MENU 按钮事件到应用程序时可能会出现问题。可能还有其他未经验证的功能。
7. X/Y 输入可通过触摸屏或鼠标。仅触摸屏输入已验证。不过，两者差异很小。主要问题在于光标支持：鼠标需要光标。光标图像也会根据状态（如抓取和拖动或调整大小）而变化。还有可能使用鼠标的自动提升功能。所有这些逻辑都已到位，但均未经过验证。
8. NxTerm 窗口确实需要可滚动。在小显示屏上仅有几行很难使用。一个相关的可用性问题是字体高度：字体报告的最大字体高度导致显示上行距较大，从而在小窗口中可见的行数更少。后一个问题源于字体而非 Twm4Nx。
9. 在 ``SLcd::CSLcd::getWidth()`` 中计算 LCD 宽度时存在一个微小的舍入误差。目前是向下截断，需要向上取整。这有时会在时钟显示上留下一小条一像素宽的细缝。该显示总是能恢复，这只是外观问题。

添加 Twm4Nx 应用程序
--------------------------

应用程序工厂和主菜单
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

原始 TWM 支持 .twmrc 文件，您可以在其中描述桌面上支持的应用程序程序。目前 Twm4Nx 没有这样的启动文件。相反，所有应用程序必须通过运行时接口添加。本段提供了这些接口的概述。

目前，仅为 Twm4Nx 开发了两个应用程序：(1) 托管 NSH 的 NxTerm，类似于 Unix 环境中托管 Bash shell 的 XTerm，以及 (2) 触摸屏校准应用程序。让我们以 NxTerm 应用程序为例，因为触摸屏校准是一个相当特殊的部分。

这些示例应用程序可以在以下位置找到：``apps/graphics/twm4nx/apps`` 和 ``apps/include/graphics/twm4nx/apps``

简而言之，添加应用程序涉及一个挂接到主菜单的"工厂对象"。工厂对象是用于创建其他对象实例的对象。工厂对象的表示方式完全由应用程序开发者决定。一种选择是使用纯虚基类 ``IApplicationFactory``，定义在 ``apps/include/graphics/twm4nx/iapplication.hxx`` 中。该基类仅提供一个方法::

  bool initialize(FAR CTwm4Nx *twm4nx);

其中 CTwm4Nx 是 Twm4NX 会话实例，允许类实现与会话特定资源交互。例如，如果平台支持多个显示，则需要多个会话。

实际上，应用程序工厂实现类继承自以下基类：

1. ``IApplicationFactory``。提供通用的 ``initialize()`` 方法。
2. ``IApplication``。提供应用程序在主菜单中条目的信息。
3. ``CTwm4NxEvent``。将应用程序工厂挂接到 Twm4Nx 事件通知系统。

初始化包括实例化应用程序工厂实例并调用其 ``IApplicationFactory::initialize()`` 方法。应用程序工厂实例是单例，必须在会话的整个生命周期内持续存在。对于 NxTerm 应用程序工厂，这在 ``apps/graphics/twm4nx/src/twm4nx_main.c`` 中完成::

  CNxTermFactory nxtermFactory;
  success = nxtermFactory.initialize(twm4nx);

除了通用初始化外，``IApplicationFactory::initialize()`` 方法还必须向主菜单注册一个新条目。您可以在 ``apps/graphics/twm4nx/apps/cnxterm.c`` 中看到示例::

  FAR CMainMenu *cmain = twm4nx->getMainMenu();
  return cmain->addApplication(this);

``CMainMenu::addApplication()`` 方法的参数类型为 ``IApplication *``。但请记住，我们的应用程序实现 ``class`` 继承自 ``IApplication``。

IApplication 纯虚基类也定义在 ``apps/include/graphics/twm4nx/iapplication.hxx`` 中。它本质上描述了当菜单项被选中时主菜单逻辑应执行的操作。它包括以下方法：

1. ``getName()``。提供将在主菜单中为此选项显示的名称字符串。
2. ``getSubMenu()``。一种可能是，选择主菜单项可能会弹出另一个子菜单选项。
3. ``getEventHandler()``。返回用于路由菜单选择事件的 ``CTwm4NxEvent`` 实例。请记住，我们的应用程序工厂继承自 ``CTwm4NxEvent``，因此此函数只需返回 'this' 指针。
4. ``getEvent()``。提供在事件通知中使用的事件 ID。返回值必须符合 ``apps/include/graphics/twm4nx/twm4nx_events.hxx`` 中的描述。具体来说，事件的接收者必须是 ``EVENT_RECIPIENT_APP``。

然后，当使用指定事件调用应用程序工厂的 ``CTwm4NxEvent::event()`` 方法时，Twm4Nx 应用程序即被启动。

应用程序窗口
~~~~~~~~~~~~~~~~~~~

应用程序工厂如何启动应用程序实例完全取决于应用程序设计者。通常这包括启动新的应用程序任务。应用程序的一般特性包括：

1. 它可能应继承自 ``CTwm4NxEvent``，以便能够接收来自系统的事件。
2. 要创建窗口，它必须实例化并初始化一个 ``CWindow`` 实例。
3. 它必须配置应用程序事件以接收来自 Twm4Nx 的通知。

要创建应用程序窗口，应用程序必须调用 ``CWindowFactory::createWindow()`` 方法。对于 NxTerm 示例，如下所示::

  NXWidgets::CNxString name("NuttShell");

  uint8_t wflags = (WFLAGS_NO_MENU_BUTTON | WFLAGS_HIDDEN);

  FAR CWindowFactory *factory = m_twm4nx->getWindowFactory();
  m_nxtermWindow = factory->createWindow(name, &CONFIG_TWM4NX_NXTERM_ICON,
                                          (FAR CIconMgr *)0, wflags);

窗口工厂是另一个创建和管理窗口实例的工厂。``createWindow()`` 方法需要四个参数：

1. 窗口的名称。这是在窗口工具栏中显示的名称，可以与主菜单条目中使用的名称相同。
2. 与窗口关联的图标图像的引用。这是窗口最小化为图标时在桌面上显示的图像。类型为 ``NXWidgets::SRlePaletteBitmap``。
3. 此窗口所属的图标管理器实例的指针。可以为 NULL 以使用默认的 Twm4Nx 图标管理器。
4. 描述窗口属性的一组标志。

  标志值由 ``apps/include/graphics/twm4nx/cwindow.hxx`` 中提供的 ``WFLAGS_*`` 定义：

  - ``WFLAGS_NO_MENU_BUTTON`` -- 从工具栏中省略菜单按钮。
  - ``WFLAGS_NO_DELETE_BUTTON`` -- 从工具栏中省略删除按钮。
  - ``WFLAGS_NO_RESIZE_BUTTON`` -- 从工具栏中省略调整大小按钮。
  - ``WFLAGS_NO_MINIMIZE_BUTTON`` -- 从工具栏中省略最小化按钮。
  - ``WFLAGS_NO_TOOLBAR`` -- 完全省略工具栏。
  - ``WFLAGS_ICONMGR`` -- 此窗口是图标管理器。
  - ``WFLAGS_MENU`` -- 此窗口是菜单窗口。
  - ``WFLAGS_HIDDEN`` -- 启动时隐藏窗口。

实例化 ``CWindow`` 后，可以配置应用程序所需的事件，如 NxTerm 应用程序中所示::

  struct SAppEvents events;
  events.eventObj    = (FAR void *)this;
  events.redrawEvent = EVENT_NXTERM_REDRAW;
  events.resizeEvent = EVENT_NXTERM_RESIZE;
  events.mouseEvent  = EVENT_NXTERM_XYINPUT;
  events.kbdEvent    = EVENT_NXTERM_KBDINPUT;
  events.closeEvent  = EVENT_NXTERM_CLOSE;
  events.deleteEvent = EVENT_NXTERM_DELETE;

  bool success = m_nxtermWindow->configureEvents(events);

再次提醒，应用程序继承自 ``CTwm4NxEvent``。因此，将 ``this`` 作为上面的事件对象传递，确保特定事件被路由到应用程序实例。

在应用程序窗口中的绘图可以使用 NXWidgets 的设施，通过与窗口关联的 ``NXWidgets::CGraphicsPort`` 来执行。不过，NxTerm 应用程序不执行任何绘图；该绘图由 NxTerm 驱动程序执行。

``NXWidgets::CGraphicsPort`` 可以从 ``CWindow`` 实例（例如 ``m_window``）获取::

  FAR NXWidgets::CWidgetControl *control = m_window->getWidgetControl();
  NXWidgets::CGraphicsPort *port = control->getGraphicsPort();

然后，该 ``CGraphicsPort`` 被传递给部件构造函数，将部件绑定到该窗口，并强制所有部件绘图在窗口内进行。

显然，关于绘图还有很多可以描述的，远超本 README 文件所能涵盖的范围。
