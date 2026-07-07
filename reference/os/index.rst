=================
Architecture APIs
=================

文件 ``include/nuttx/arch.h`` 通过函数原型列出了所有必须由架构特定逻辑提供的 API。
架构特定逻辑必须与之交互的内部 OS API 同样在 ``include/nuttx/arch.h`` 或其他头文件中定义。

.. toctree::
  addrenv.rst
  app_vs_os.rst
  arch.rst
  board.rst
  conventions.rst
  iob.rst
  led.rst
  mutex.rst
  newreno.rst
  notifier.rst
  nuttx.rst
  paging.rst
  shm.rst
  smp.rst
  sleep.rst
  time_clock.rst
  wqueue.rst
  events.rst
