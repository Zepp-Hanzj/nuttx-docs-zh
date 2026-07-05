=======================
``timer`` Timer example
=======================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

This is a simple test of the timer driver (see ``include/nuttx/timers/timer.h``).

Dependencies:

- ``CONFIG_TIMER`` – The timer driver must be selected

Example configuration:

- ``CONFIG_EXAMPLES_TIMER_DEVNAME`` – This is the name of the timer device that
  will be tested. Default: ``/dev/timer0``.
- ``CONFIG_EXAMPLES_TIMER_INTERVAL`` – This is the timer interval in microseconds.
  Default: ``1000000``.
- ``CONFIG_EXAMPLES_TIMER_DELAY`` – This is the delay between timer samples in
  microseconds. Default: ``10000``.
- ``CONFIG_EXAMPLES_TIMER_STACKSIZE`` – This is the stack size allocated when the
  timer task runs. Default: ``2048``.
- ``CONFIG_EXAMPLES_TIMER_PRIORITY`` – This is the priority of the timer task:
  Default: ``100``.
- ``CONFIG_EXAMPLES_TIMER_PROGNAME`` – This is the name of the program that will
  be used when the NSH ELF program is installed. Default: ``timer``.
