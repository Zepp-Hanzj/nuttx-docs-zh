=================================
``unity`` Unity testing framework
=================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

Unity 是由 ThrowTheSwitch.org 开发的 C 语言单元测试框架：

http://www.throwtheswitch.org/unity

.. note::

   GitHub 页面上有比网站上更详细的文档。可以在 `此 markdown 文档集合 <https://github.com/ThrowTheSwitch/Unity/tree/master/docs>`_ 中找到。

它非常简约，设计为也可以在嵌入式系统上运行。Unity 通过使用不同的宏进行高度可配置。这些在 `配置指南 <https://github.com/ThrowTheSwitch/Unity/blob/master/docs/UnityConfigurationGuide.md>`_ 中有描述。其中一些配置选项通过 Unity 测试框架的 Kconfig 选择菜单在 NuttX 中暴露，但并非所有选项都已实现。

.. note::

   如果您想在 Unity 中使用的某些配置选项在 NuttX 中缺失，请按照 :doc:`贡献指南 </contributing/index>` 提交 pull request。


Usage
=====

为了在 NuttX 中使用 Unity 框架测试您的应用程序，您可以创建一个测试应用程序。创建自定义 NuttX 应用程序的文档可以在 :doc:`这里 </guides/customapps>` 找到。

只需将您的应用程序标记为依赖于您使用的任何 Unity 选项：

.. code-block:: kconfig

   config MY_TESTS
       tristate "Test cases"
       depends on TESTING_UNITY
       depends on TESTING_UNITY_EXCLUDE_SETJMP
       depends on TESTING_UNITY_PRINT_FORMATTED
       depends on MY_APPLICATION_CODE

在应用程序的 main 函数中，您可以包含测试库并编写测试！

.. code-block:: c

   #include <testing/unity.h>

   void setUp(void) { /* Test setup code for Unity */ }
   void tearDown(void) { /* Test tear-down code for Unity */ }

   /* Short test case */
   
   static void test_mything__passes(void)
   {
     int mynum = 0;
     mynum++;
     TEST_ASSERT_EQUAL(1, mynum);
   }

   int main(void)
   {
      UNITY_BEGIN();
      RUN_TEST(test_mything__passes);
      return UNITY_END();
   }

现在当您构建代码时，您的测试应用程序将在 NSH 中可见并可运行。如果您运行它，您将看到测试报告！

.. code-block:: console

   nsh> mytests
   mytests_main.c:18:test_mything__passes:PASS

   -----------------------
   1 Tests 0 Failures 0 Ignored
