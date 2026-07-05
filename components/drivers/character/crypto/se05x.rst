============
SE05X 驱动
============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

此驱动程序通过使用 `NXP plug and trust nano <https://github.com/NXPPlugNTrust/nano-package>`_ 实现对 NXP SE05X 安全元件的访问。

.. note::
   目前此驱动程序仅在 SE050 上进行了测试。

API
===

驱动程序支持读取/写入 SE05X 的密钥库以及额外功能，如 Diffie-Hellman 密钥派生和使用密钥库中的密钥签署 CSR 及验证证书。
有关可用的 API 函数，请参考 ``drivers/crypto/pnt/pnt_se05x_api.h``；有关 ioctl 命令，请参考 ``include/nuttx/crypto/se05x.h``。

以下工具使用了 SE05X 驱动程序（可作为参考项目）：

- ``controlse`` 应用程序可用于从 NSH 控制 SE05X。

- ``setest`` 应用程序从 NSH 测试所有 SE05X ioctl 功能。

数据手册可在 `NXP 网站 <https://www.nxp.com/products/security-and-authentication/authentication/edgelock-se050-plug-trust-secure-element-family-enhanced-iot-security-with-high-flexibility:SE050>`_ 上获取。

配置
=============

- ``DEV_SE05X`` 启用对 NXP SE050 或 SE051 提供的 /dev/se05x 安全元件的支持

  - 通道通信接口

    - ``DEV_SE05X_SCP03`` SCP03 安全通道（未实现）

      - ``DEV_SE05X_SCP03_KEY_FILE`` 指定包含 SCP03 通道认证所需密钥的文件。
        位置可以相对于 NuttX 根文件夹。文件应包含 SCP03_ENC_KEY、SCP03_MAC_KEY 和 SCP03_DEK_KEY 的字节数组初始化定义。

    - ``DEV_SE05X_PLAIN`` 明文通信

  - ``SE05X_LOG_LEVEL`` SE05x 日志分为以下级别：ERROR、WARNING、INFO、DEBUG。
