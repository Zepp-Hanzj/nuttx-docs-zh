====================
读取 CAN 消息
====================

NuttX 的 CAN 驱动默认行为是在单次 ``read`` 操作中返回多条消息（如果能够容纳）。如果你的代码（特别是从 SocketCAN 迁移过来的代码）没有考虑这一点，那么你很可能会遇到看似丢失帧的情况。你有两个选择：要么修改代码以支持这种行为，要么关闭这种行为。

以下示例展示了如何处理多条消息：

.. code-block:: c

   #define BUFLEN 128  /* CAN RX 缓冲区的任意大小 */

    FAR struct can_msg_s *msg;
    char rxbuffer[BUFLEN];
    ssize_t nread;
    int nbytes;
    int msglen
    int i;

    /* 将消息读入 RX 缓冲区 */

    nread = read(fd, rxbuffer, BUFLEN);

    /* 检查读取错误 */
    ...

    /* 处理 RX 缓冲区中的每条消息 */

    for (i = 0; i <= nread - CAN_MSGLEN(0); i += msglen)
    {
    /* 从 RX 缓冲区获取下一条消息 */

        msg    = (FAR struct can_msg_s *)&rxbuffer[i];
        nbytes = can_dlc2bytes(msg->cm_hdr.ch_dlc);
        msglen = CAN_MSGLEN(nbytes);

        DEBUGASSERT(i + msglen < BUFLEN);

    /* 处理下一条 CAN 消息 */
    ...
    }

通过遍历读取缓冲区并解析每条 CAN 消息，可以避免丢失在输入缓冲区中连续存储的消息。

另一种方法是使用消息对齐功能。将消息对齐设置为零时，驱动将始终在单次 ``read`` 操作中只返回一条消息：

.. code-block:: c

   unsigned msgalign = 0;
   ioctl(fd, CANIOC_SET_MSGALIGN, &msgalign);

消息对齐功能可以用来进一步调整行为。它通常控制传递给 ``read`` 和 ``write`` 操作的缓冲区中消息的对齐方式。虽然默认行为（尽可能多地将消息打包到缓冲区中）提供了最高效的交换方式，但你可能也想要一种更简单的用法，即传递消息数组。这可以通过将消息对齐大小设置为恰好等于消息大小来确保：

.. code-block:: c

   unsigned         msgsiz = sizeof(struct can_msg_s);
   struct can_msg_s msgs[5];
   ssize_t          nread;
   int              i;

   /* 将消息对齐设置为消息大小。 */

   ioctl(fd, CANIOC_SET_MSGALIGN, &msgsiz);

   /* 将消息读入数组。 */

   nread = read(fd, msgs, sizeof(msgs));

   /* 遍历读取的消息 */
   for (i = 0; i < nread / msgsiz; i--)
     {
       /* 处理 CAN 消息 msgs[i] */
     }

同样的对齐规则也适用于 ``write``，因此使用像示例中那样的对齐方式，你将写入消息数组，而不是消息紧密排列的方式。
