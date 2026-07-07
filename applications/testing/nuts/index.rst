================================
NuttX Unit Test Selection (NUTS)
================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NUTS 是一组单元测试套件，可以编译并在 NuttX 设备上运行，以验证操作系统 API 的正确运行。NUTS 依赖于 :doc:`cmocka </applications/testing/cmocka/index>` 测试框架来运行单元测试。

Building & Deploying
--------------------

为了在目标设备上构建和部署 NUTS，您需要启用 cmocka 库和 ``CONFIG_TESTING_NUTS``。启用 NUTS 后，您将在 Kconfig 中看到可用测试类别的列表。您可以启用要运行测试的类别。

启用测试类别后，您将能够访问该类别中每个测试组的开关。例如，如果您启用了 'devices' 类别，您将能够选择是否要包含 ``/dev/zero`` 或 ``/dev/null`` 等的测试。默认情况下，类别中的所有测试组都是启用的，必须通过禁用其开关来选择退出。

.. note::

   某些单独的测试可能有特定的依赖项需要先启用，因此不要假设 Kconfig 中可见的测试列表是完整的（除非您已在 Kconfig 中启用了显示隐藏选项）。例如，``/dev/urandom`` 依赖于 `CONFIG_DEV_URANDOM` 启用，并且在依赖项未被选择时不会在菜单中显示。

构建并部署到目标后，您可以使用以下命令查看测试结果（仅运行 ``/dev/zero`` 测试的示例）：

.. code:: console

   nsh> nuts
   [==========] /dev/zero: Running 8 test(s).
   [ RUN      ] open_rdonly
   [       OK ] open_rdonly
   [ RUN      ] open_rdwr
   [       OK ] open_rdwr
   [ RUN      ] open_wronly
   [       OK ] open_wronly
   [ RUN      ] readzero
   [       OK ] readzero
   [ RUN      ] readlarge
   [       OK ] readlarge
   [ RUN      ] writezero
   [       OK ] writezero
   [ RUN      ] writelarge
   [       OK ] writelarge
   [ RUN      ] wrrd
   [       OK ] wrrd
   [==========] /dev/zero: 8 test(s) run.
   [  PASSED  ] 8 test(s).

Included Tests
--------------

NUTS 测试按类别划分。每个类别中都有测试组/套件，其中包含与特定 API 相关的所有单独测试用例。

.. toctree::
   :caption: Test categories

   devices
   dstructs

Test Cases
----------

NUTS 的输出显示每个已包含在构建中的测试用例的通过/失败/跳过结果。虽然测试用例的名称旨在描述测试用例正在验证的内容，但有时需要更多信息。NUTS 中的每个测试用例都有相应的源代码注释/文档字符串，其中包含对测试验证内容的描述。您还可以通过查看测试中的断言语句来确定更多信息。

Adding New Tests
----------------

要添加新测试，首先请查看 :doc:`cmocka </applications/testing/cmocka/index>` API 文档。

然后，您应该在您希望扩展的类别下添加一个新的 ``.c`` 文件。所有测试用例都是静态函数，接受一个 ``void **state`` 以从 setup 函数传入上下文。每个测试用例函数应该有一个文档字符串注释，描述特定测试用例正在测试的内容（并且名称应尽可能具有描述性）。Setup 和 teardown 函数必须分别以 ``setup_`` 和 ``teardown_`` 开头，后缀是描述正在设置/拆除内容的名称。

从循环缓冲区测试套件中提取的测试用例示例：

.. code:: c

   static int setup_empty_cbuf(void **state)
   {
     *state = &g_cbuf;
     return circbuf_init(&g_cbuf, g_buf, sizeof(g_buf));
   }

   static int teardown_cbuf(void **state)
   {
     circbuf_uninit(*state);
     if (circbuf_is_init(*state)) return -1;
     return 0;
   }

   /****************************************************************************
    * Name: empty_postinit
    *
    * Description:
    *   Tests that a circular buffer is empty right after being initialized.
    ****************************************************************************/

   static void empty_postinit(void **state)
   {
     struct circbuf_s *cbuf = *state;

     assert_true(circbuf_is_empty(cbuf));
     assert_false(circbuf_is_full(cbuf));
     assert_uint_equal(0, circbuf_used(cbuf));
     assert_uint_equal(CBUF_SIZE, circbuf_space(cbuf));
   }

每个测试组必须实现一个公共函数来运行所有测试用例，遵循以下约定：

.. code:: c

   int nuts_category_group(void)
   {
     static const struct CMUnitTests tests[] =
     {
       cmocka_unit_test(this_is_test_one),
       cmocka_unit_test_setup_teardown(this_is_test_two, setup_func,
                                       teardown_func),
     };

     return cmocka_run_group_tests_name("group name", tests, NULL, NULL);
   }

其中 'category' 是测试类别的名称，'group' 是测试组的名称（即类别为 'devices'，组为 'devnull'）。

在该类别的 ``tests.h`` 头文件中，在公共函数原型下包含以下内容：

.. code:: c

   #ifdef CONFIG_TESTING_NUTS_CATEGORY_GROUP
   int nuts_category_group(void);
   #else
   #define nuts_category_group()
   #endif /* CONFIG_TESTING_NUTS_CATEGORY_GROUP */

其中 ``CONFIG_TESTING_NUTS_CATEGORY_GROUP`` 是切换测试组开/关的 Kconfig 选项。您需要将其添加到 NUTS Kconfig 文件中。

为了减少 ``Makefile``/``CMakeLists.txt`` 文件中的特殊开关数量，每个类别目录中的所有源文件都使用通配符包含。因此，为了避免编译未选择的测试组，每个测试组的 C 文件应该被以下保护包围：

.. code:: c

   #ifdef CONFIG_TESTING_NUTS_CATEGORY_GROUP

   /* ... your test cases and public test runner function ... */

   #endif /* CONFIG_TESTING_NUTS_CATEGORY_GROUP */
