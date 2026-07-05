========================================
从中断处理程序发出事件信号
========================================

.. warning:: 迁移自 
    https://cwiki.apache.org/confluence/display/NUTTX/Signaling+Events+from+Interrupt+Handlers

从中断唤醒多个线程的最佳方式？
=================================================

    我想创建一个字符设备驱动，将相同的数据传递给所有正在读取它的任务。数据是排队的还是只获取最新样本并不太重要。问题只是如何唤醒等待的线程。

在最基本的层面上，线程可以等待信号量、信号或消息队列（非空或非满）。然后在这些之上有更高级的包装器，如互斥锁、信号量、poll 等等待。但在底层，这些是三种基本的等待机制。任何一种都可以用来实现你想要的功能。

在 NuttX 中，在每个 IPC 的信号发送方面投入了额外的设计工作，使其可以方便地被中断处理程序使用。这种行为是 NuttX 独有的；POSIX 没有关于中断处理程序的任何规定。因此，我们将主要讨论不可移植的 OS 接口。

    到目前为止我考虑了以下选项：

你基本上已经遍历了等待机制的列表：

消息队列
==============

  1) 在设备打开时打开一个消息队列（每个任务一个新队列）并将它们保存在列表中。在 ISR 中向这些队列的非阻塞端点发送消息。在设备 ``read()`` 中从阻塞端点读取。我需要为消息队列生成名称，因为似乎没有匿名消息队列？

当你开始一个项目时，决定一个共同的 IPC 机制作为设计基础是一个好主意。POSIX 消息队列是一个很好的选择：为每个线程分配一个消息队列，每个线程的 ``main()`` 简单地等待消息队列。这是一个很好的架构，经常被使用。

但是，我可能会避免创建大量消息队列只是为了支持中断级信号。有其他不使用那么多内存的方式来实现。所以，如果你有消息队列，就使用它们。如果没有，保持简单。

在这种情况下，你的等待任务将在调用 ``mq_receive()`` 时阻塞，直到收到消息。然后它将唤醒并可以处理消息。在中断处理程序中，当感兴趣的事件发生时，它将调用 ``mq_send()``，这将唤醒等待的任务。

在这种情况下使用消息队列的优点是：1）你可以在消息中传递相当多的数据，2）它在基于消息的应用程序架构中集成得很好。缺点是，从中断处理程序发送的消息数量有限制，因此可能会出现数据溢出条件，即可能接收到的中断事件比可用消息能报告的多。

此限制是由于不能从中断处理程序动态分配内存。相反，中断处理程序仅限于使用预分配的消息。预分配消息的数量由 ``CONFIG_PREALLOC_MQ_MSGS`` + 8 给出。``CONFIG_PREALLOC_MQ_MSGS`` 可以由正常任务逻辑或中断级逻辑使用。额外的八个是中断处理逻辑的紧急池（该值目前不可配置）。

如果任务逻辑用完了所有 ``CONFIG_PREALLOC_MQ_MSGS`` 消息，它将回退到动态分配消息，这会带来一定的性能和确定性行为成本。

如果中断级用完了所有 ``CONFIG_PREALLOC_MQ_MSGS`` 消息，它将回退使用 8 个预分配消息的紧急池。如果这些也用尽，则消息将不会发送，中断实际上丢失。

信号量
==========

  2) 为每个设备打开分配一个信号量并保存在列表中。当共享缓冲区中有新数据可用时发送信号量。在 ``sched_lock()`` 内读取数据。

如果你没有使用消息队列的架构，并且所有这些线程只等待中断事件而不等待其他东西，那么信号量信号也可以很好地工作。在这种情况下，你基本上是将信号量用作条件变量，所以你必须小心。

注意：你不需要多个信号量。你可以用一个信号量做到这一点。如果信号量用于此目的，则将其初始化为零：

.. code-block:: c

    sem_init(&sem, 0, 0);
    sem_setprotocol(&sem, SEM_PRIO_NONE);

``sem_setprotocol()`` 是一个非标准的 NuttX 函数，应在 ``sem_init()`` 之后立即调用。此函数调用的效果是禁用该特定信号量的优先级继承。因此，用于信号发送的信号量上不应有优先级继承操作。有关更多信息，请参阅 :doc:`/guides/signaling_sem_priority_inheritance`。

由于信号量初始化为零，每次线程加入等待线程组时，计数会递减。因此，像这样的简单循环可以唤醒所有等待的线程：

.. code-block:: c

    int svalue;
    int ret;
    
    for (; ; )
    {
        ret = sem_getvalue(&sem, &svalue);
        if (svalue < 0)
        {
            sem_post(&sem);
        }
        else
        {
            break;
        }
    }

注意：``sem_getvalue()`` 的这种使用是不可移植的。在许多环境中，如果有等待者在信号量上，``sem_getvalue()`` 不会返回负值。

上面的代码片段本质上就是 NuttX ``pthread_cond_broadcast()`` 所做的（参见 `nuttx/sched/pthread_condbroadcast.c <https://github.com/apache/nuttx/blob/master/sched/pthread/pthread_condbroadcast.c>`_）。在 NuttX 中，条件变量实际上只是信号量的包装器，赋予了它们一些新属性。你甚至可以从中断处理程序调用 ``pthread_cond_broadcast()``：有关用法信息，请参阅 http://pubs.opengroup.org/onlinepubs/009695399/functions/pthread_cond_signal.html。

上述两种机制都不是这些接口的可移植用法。但是，没有可移植的接口可以直接与中断处理程序通信。

如果你想向单个等待线程发信号，有更简单的方法。在等待任务中：

.. code-block:: c

    semt_t g_mysemaphore;
    volatile bool g_waiting;
    ...
    
    sem_init(&g_mysemaphore);
    sem_setprotocol(&g_mysemaphore, SEM_PRIO_NONE);
    ...
    
    flags = enter_critical_section();
    g_waiting = true;
    while (g_waiting)
    {
        ret = sem_wait(&g_mysemaphore);
        ... handler errors ...
    }
    
    leave_critical_section(flags);

在上面的代码片段中，禁用中断是为了设置和测试 ``g_waiting``。当任务等待中断事件时，中断当然会自动且原子地重新启用。

然后在中断处理程序中

.. code-block:: c 

    extern semt_t g_mysemaphore;
    extern volatile bool g_waiting;
    ...
    
    if (g_waiting)
    {
        g_waiting = false;
        sem_post(&g_mysemaphore);
    }

也可以使用整数类型计数器代替 bool 类型来支持多次等待。在这种情况下，这等同于上面使用 ``sem_getvalue()`` 的情况，但不依赖于 ``sem_getvalue()`` 的不可移植属性。

注意：当信号量用于信号发送和优先级继承时，两者之间可能存在不当的交互。在这种情况下，你应该使用 ``sem_setprotocol(SEM_PRIO_NONE)`` 禁用信号发送信号量上的优先级继承。有关更多信息，请参阅 :doc:`/guides/signaling_sem_priority_inheritance`。

信号
=======

  3) 在调用 ``read()`` 时将线程 id 存储在列表中。使用 ``sigqueue()`` 唤醒线程。在 ``sched_lock()`` 内从共享缓冲区读取数据。

信号也可以很好地工作。信号有一个副作用，有时很有帮助，有时很麻烦：它们会导致几乎所有类型的等待（``read()``、``sem_wait()`` 等）唤醒并返回 ``errno=EINTR`` 的错误。

这有时很有帮助，因为你可以唤醒 ``recv()`` 或 ``read()`` 等，检测产生信号的事件，并做一些处理。这有时很麻烦，因为你必须记住处理 ``EINTR`` 返回值，即使你不关心它。

POSIX 信号定义包含一些支持，可以使这对你来说更容易。这些支持目前在 NuttX 中未实现。例如，``kill()`` 接口（http://pubs.opengroup.org/onlinepubs/009695399/functions/kill.html）支持此行为：

"如果 pid 为 0，sig 将发送给所有进程组 ID 等于发送者进程组 ID 的进程（不包括一组未指定的系统进程），并且该进程有权限发送信号。"

"如果 pid 为 -1，sig 将发送给该进程有权限发送该信号的所有进程（不包括一组未指定的系统进程）。"

"如果 pid 为负数但不是 -1，sig 将发送给所有进程组 ID 等于 pid 绝对值的进程（不包括一组未指定的系统进程），并且该进程有权限发送信号。"

NuttX 目前不支持进程组。但这可能是一个好的 RTOS 扩展。如果你和其他人认为这很有用，我可能可以在一天左右添加这样一个功能的基础。

``poll()``
==========

  是否有更好的我还没有发现的方法？

你显然没有提到的是 ``poll()``。参见 http://pubs.opengroup.org/onlinepubs/009695399/functions/poll.html。由于你正在编写设备驱动，支持驱动中的 ``poll()`` 方法似乎是自然的解决方案。参见 ``drivers/`` 目录中的许多示例，``drivers/pipes/pipe_common.c`` 是一个。每个线程可以简单地在 ``poll()`` 上等待；当事件发生时，驱动可以唤醒一组等待者。在底层，这只是一组 ``sem_post``。但它也是一个非常标准的机制。

在你的情况下，``poll()`` 的语义可能需要稍微调整。由于它们都专注于数据 I/O 事件，你可能需要调整某些事件标志的含义。

``poll()`` 在这种情况下的另一个创造性用法：

  那将是很棒的事情！PX4 项目以某种方式实现了这个（用 C++），所以如果许可证允许，也许可以很快移植到 NuttX？
  
  https://pixhawk.ethz.ch/px4/dev/shared_object_communication

我对这个了解不多，但如果它符合你的需求，可能值得一看。
