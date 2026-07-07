=====
睡眠
=====

NuttX 提供三种不同类型的睡眠接口。

通用睡眠接口
=======================

调度睡眠接口（基于 tick）
---------------------------------------

挂起调用线程指定的时间，直到时间到期或线程通过调度器操作被显式唤醒。

.. c:function:: void nxsched_abstick_sleep(clock_t ticks)

    挂起调用线程，直到指定的绝对时钟 tick 时间。

    :param ticks: 以时钟 tick 为单位的绝对时间。

.. c:function:: void nxsched_ticksleep(unsigned int ticks)

    挂起调用线程指定的系统 tick 数。

    :param ticks: 要睡眠的系统 tick 数。

.. c:function:: void nxsched_usleep(useconds_t usec)

    挂起调用线程指定的微秒数。

    :param usec: 要睡眠的微秒数。

.. c:function:: void nxsched_msleep(unsigned int msec)

    挂起调用线程指定的毫秒数。

    :param msec: 要睡眠的毫秒数。

.. c:function:: void nxsched_sleep(unsigned int sec)

    挂起调用线程指定的秒数。

    :param sec: 要睡眠的秒数。

.. c:function:: int nxsched_nanosleep(const struct timespec *rqtp, struct timespec *rmtp)

    挂起调用线程指定的 rqtp 参数时间。如果睡眠被信号中断，
    此函数将通过更新 rmtp 返回剩余时间。

    :param rqtp: 要挂起执行的时间量。
    :param rmtp: 如果 rmtp 参数非 NULL，它引用的 timespec 结构体将被更新为剩余时间。

    :return: 成功返回 0 (OK)，失败返回取负的 errno 值。

.. c:function:: void nxsched_wakeup(struct tcb_s *tcb)

    此函数用于在超时到期前唤醒当前处于睡眠状态的线程。

    :param tcb: 指向要唤醒的任务的 TCB 的指针。

基于信号的睡眠接口（基于 timespec）
----------------------------------------------

挂起调用线程指定的时间，直到时间到期或有信号传递给调用线程。

    .. note::
        实现依赖于信号框架，并基于标准 timespec 转换。

.. c:function:: void nxsig_usleep(useconds_t usec)

    挂起调用线程指定的微秒数。

    :param usec: 要睡眠的微秒数。

.. c:function:: void nxsig_sleep(unsigned int sec)

    挂起调用线程指定的秒数。

    :param sec: 要睡眠的秒数。

.. c:function:: int nxsig_nanosleep(const struct timespec *rqtp, struct timespec *rmtp)

    挂起调用线程指定的 rqtp 参数时间。如果睡眠被信号中断，
    此函数将通过更新 rmtp 返回剩余时间。

    :param rqtp: 要挂起执行的时间量。
    :param rmtp: 如果 rmtp 参数非 NULL，它引用的 timespec 结构体将被更新为剩余时间。

    :return: 成功返回 0 (OK)，失败返回取负的 errno 值。

忙等待睡眠接口
---------------------

在请求的持续时间内循环自旋，不放弃 CPU。延迟精度取决于 ``CONFIG_BOARD_LOOPSPERMSEC``。

.. c:function:: void up_mdelay(unsigned int milliseconds)

    内联延迟指定的毫秒数。

    :param milliseconds: 要延迟的毫秒数。

.. c:function:: void up_udelay(useconds_t microseconds)

    内联延迟指定的微秒数。

    :param microseconds: 要延迟的微秒数。

.. c:function:: void up_ndelay(unsigned long nanoseconds)

    内联延迟指定的纳秒数。

    :param nanoseconds: 要延迟的纳秒数。
