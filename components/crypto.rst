====================
Crypto API Subsystem
====================

Overview
========

NuttX Crypto API 子系统为加密操作提供统一接口，支持各种加密、解密、哈希和认证算法。该子系统通过通用接口抽象了硬件和软件加密实现。

Supported Algorithms
====================

Symmetric Encryption Algorithms
--------------------------------

**AES (Advanced Encryption Standard)**

- AES-CBC 模式：
  - CRYPTO_AES_CBC（128 位密钥大小）
  - CRYPTO_AES_192_CBC（192 位密钥大小）
  - CRYPTO_AES_256_CBC（256 位密钥大小）

- AES-CTR 模式（计数器模式）：
  - CRYPTO_AES_CTR

- AES-XTS 模式（基于 XEX 的调整码本）：
  - CRYPTO_AES_XTS

- AES-GCM 模式（Galois/计数器模式）：
  - CRYPTO_AES_GCM_16

- AES-OFB 模式（输出反馈）：
  - CRYPTO_AES_OFB

- AES-CFB 模式（密码反馈）：
  - CRYPTO_AES_CFB_8（8 位）
  - CRYPTO_AES_CFB_128（128 位）

**其他分组密码模式**

- Blowfish (BLF)：
  - CRYPTO_BLF_CBC

- CAST (CAST-128)：
  - CRYPTO_CAST_CBC

- Rijndael（128 位）：
  - CRYPTO_RIJNDAEL128_CBC

- Null（无加密）：
  - CRYPTO_NULL

Authentication and Hashing Algorithms
--------------------------------------

**HMAC（基于哈希的消息认证码）**

- MD5-HMAC：
  - CRYPTO_MD5_HMAC

- SHA-1 HMAC：
  - CRYPTO_SHA1_HMAC

- SHA-2 HMAC：
  - CRYPTO_SHA2_256_HMAC（256 位）
  - CRYPTO_SHA2_384_HMAC（384 位）
  - CRYPTO_SHA2_512_HMAC（512 位）

**哈希函数**

- MD5：
  - CRYPTO_MD5

- SHA-1：
  - CRYPTO_SHA1

- SHA-2：
  - CRYPTO_SHA2_224（224 位）
  - CRYPTO_SHA2_256（256 位）
  - CRYPTO_SHA2_384（384 位）
  - CRYPTO_SHA2_512（512 位）

- RIPEMD-160：
  - CRYPTO_RIPEMD160（作为哈希函数）
  - CRYPTO_RIPEMD160_HMAC

**消息认证码**

- AES-GMAC（Galois 消息认证码）：
  - CRYPTO_AES_128_GMAC（128 位密钥）
  - CRYPTO_AES_192_GMAC（192 位密钥）
  - CRYPTO_AES_256_GMAC（256 位密钥）
  - CRYPTO_AES_GMAC（通用）

- AES-CMAC（基于密码的消息认证码）：
  - CRYPTO_AES_CMAC
  - CRYPTO_AES_128_CMAC（128 位）

- Poly1305：
  - CRYPTO_POLY1305
  - CRYPTO_CHACHA20_POLY1305
  - CRYPTO_CHACHA20_POLY1305_MAC

**流密码**

- ChaCha20：
  - CRYPTO_CHACHA20_POLY1305（带 Poly1305 MAC）

Integrity and Checksums
------------------------

- CRC-32：
  - CRYPTO_CRC32

- 扩展序列号 (ESN)：
  - CRYPTO_ESN

Compression
-----------

- Deflate 压缩：
  - CRYPTO_DEFLATE_COMP

Usage
=====

Crypto API 通过 cryptodev 接口访问，该接口提供用于初始化加密会话和执行操作的 ioctl 命令。

Basic Usage Pattern
-------------------

1. 打开 cryptodev 设备 (/dev/crypto)
2. 使用所需算法初始化加密会话
3. 提交加密操作（加密/解密/哈希）
4. 完成后关闭会话

有关更多详细信息，请参阅 cryptodev.h 头文件和特定驱动文档。

Asymmetric Cryptography
=======================

Public Key Algorithms
---------------------

**RSA (Rivest-Shamir-Adleman)**

- 支持可变密钥大小的 RSA 密钥对生成
- 使用多种填充方案的数字签名生成和验证：
  - PKCS#1 v1.5 填充 (CRK_RSA_PKCS15_SIGN, CRK_RSA_PKCS15_VERIFY)
  - PSS（概率签名方案）填充 (CRK_RSA_PSS_SIGN, CRK_RSA_PSS_VERIFY)
- 公钥加密和解密
- RSA 操作可通过 /dev/crypto cryptodev 接口访问

**ECDSA（椭圆曲线数字签名算法）**

- 支持不同曲线的 ECDSA 密钥对生成
- 数字签名生成和验证

ECC / ECDSA (Software)
----------------------

NuttX 还在 ``include/crypto/ecc.h`` 中提供了一个轻量级 ECC 实现和公共 API。它可用于 ECC 密钥生成、ECDH 共享密钥计算以及 ECDSA 签名/验证。公钥导出支持压缩形式（``ECC_BYTES + 1``）以及 X/Y 非压缩形式。

RSA Digital Signature Operations
--------------------------------

cryptodev 模块通过 cryptokey 接口支持 RSA 数字签名：

- **CRK_RSA_PKCS15_SIGN**：使用 PKCS#1 v1.5 填充生成 RSA 签名
  - 输入：消息哈希，私钥 ID
  - 输出：RSA 签名

- **CRK_RSA_PKCS15_VERIFY**：使用 PKCS#1 v1.5 填充验证 RSA 签名
  - 输入：消息哈希，签名，公钥 ID
  - 输出：验证结果

- **CRK_RSA_PSS_SIGN**：使用 PSS 填充生成 RSA 签名
  - 输入：消息哈希，私钥 ID
  - 输出：RSA 签名

- **CRK_RSA_PSS_VERIFY**：使用 PSS 填充验证 RSA 签名
  - 输入：消息哈希，签名，公钥 ID
  - 输出：验证结果

两种填充方案都通过 ``/dev/crypto`` 可访问的 cryptokey ioctl 接口支持。

Key Management Operations
--------------------------

cryptodev 模块提供全面的密钥管理接口：

**密钥派生**

- PBKDF2：
  - CRYPTO_PBKDF2_HMAC_SHA1
  - CRYPTO_PBKDF2_HMAC_SHA256

**密钥生成**

- CRK_GENERATE_AES_KEY：使用指定密钥 ID 生成 AES 密钥数据
  - 支持 128 位、192 位和 256 位密钥生成
  - 使用软件实现生成密码学安全的随机 AES 密钥
  - 生成的密钥可立即用于 AES 加密/解密操作

- CRK_GENERATE_RSA_KEY：使用指定密钥 ID 生成 RSA 密钥对（公钥和私钥）
- CRK_GENERATE_SECP256R1_KEY：使用指定密钥 ID 在 SECP256R1 曲线上生成 ECDSA 密钥对
  - 为 ECDSA 操作生成 P-256 椭圆曲线密钥对
  - 使用 NuttX 的轻量级 ECC 实现进行密钥生成
  - 生成的密钥可用于 ECDSA 数字签名操作

**密钥生命周期管理**

- CRK_DELETE_KEY：从驱动中删除指定密钥 ID 的密钥
- CRK_SAVE_KEY：将密钥数据持久化到 FLASH 存储中以实现非易失性存储
- CRK_LOAD_KEY：从 FLASH 加载先前保存的密钥数据到 RAM 中

**基于 MTD 的密钥存储**

NuttX 支持使用 MTD（内存技术设备）进行持久化密钥存储：

- 密钥可以保存到基于 MTD 的存储中以实现非易失性持久化
- 基于软件的密钥管理 (swkey) 提供透明的 MTD 集成
- 系统初始化时自动从 MTD 加载密钥
- 支持对称（AES）和非对称（RSA、ECC）密钥存储
- 实现跨重启的安全设备配置和凭据持久化

**使用密钥的加密操作**

一旦密钥被分配、生成或导入，它们可用于：

- 对称加密/解密操作 (AES)
- RSA 签名生成和验证
- ECDSA 数字签名操作
- 密钥交换协议
