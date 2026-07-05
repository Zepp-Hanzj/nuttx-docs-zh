# NuttX 中文文档

Apache NuttX RTOS 官方文档的中文翻译版本。

## 构建

```bash
# 安装依赖
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 构建 HTML
make html

# 实时预览
make autobuild
```

构建产物在 `_build/html/`。

## 目录结构

```
├── introduction/     # 简介
├── quickstart/       # 快速入门
├── guides/           # 开发指南
├── contributing/     # 贡献指南
├── faq/              # 常见问题
├── components/       # 内核组件（P1）
├── reference/        # API 参考（P1）
├── debugging/        # 调试指南（P1）
├── implementation/   # 实现细节（P1）
├── standards/        # 标准合规（P1）
├── platforms/        # 平台文档（P2）
├── applications/     # 应用文档（P2）
├── sync.py           # 增量同步工具
└── _upstream/        # 上游快照
```

## 增量同步

当 NuttX 上游文档更新时，使用 `sync.py` 检测变更：

```bash
# 1. 快照上游文档
python3 sync.py snapshot --upstream ../nuttx/Documentation

# 2. 对比变更
python3 sync.py diff --upstream ../nuttx/Documentation

# 3. 查看翻译进度
python3 sync.py status
```

## 翻译规范

- RST 结构（标题、指令、引用、代码块）保持不变
- 技术术语保留英文：NuttX, RTOS, POSIX, CMake, GPIO, UART 等
- 代码示例、URL、文件路径不翻译
- 指令内容（note、warning 等文本）翻译为中文

## 许可

Apache License 2.0
