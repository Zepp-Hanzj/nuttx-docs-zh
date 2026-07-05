#!/usr/bin/env python3
"""Translate NuttX example docs from English to Chinese (Simplified).

Preserves RST directives, cross-references, code blocks, paths, Kconfig options.
Translates only prose text.
"""

import os
import re
import sys

# Translation dictionary for common phrases
TRANSLATIONS = {
    # Common phrases
    "example": "示例",
    "Example": "示例",
    "test": "测试",
    "Test": "测试",
    "driver": "驱动程序",
    "Driver": "驱动程序",
    "configuration": "配置",
    "Configuration": "配置",
    "Dependencies": "依赖项",
    "Background": "背景",
    "License": "许可证",
    "Copyright": "版权",
    "Overview": "概述",
    "Notes": "注意事项",
    "Note": "注意",
    "Author": "作者",
    "Hardware setup": "硬件设置",
    "Prerequisites": "前置条件",
    "Basic Usage": "基本用法",
    "Header Files": "头文件",
    "Data Structures": "数据结构",
    "Actions": "操作",
    "Return Values": "返回值",
    "Success": "成功",
    "Error code": "错误代码",
    "Simple Lock Example": "简单锁示例",
    "Waiting for GPS Fix": "等待 GPS 定位",
    "With GPS Fix": "GPS 定位后",
    "Feature support": "功能支持",
    "General Usage Instructions": "一般使用说明",
    "Specific configuration options": "特定配置选项",
    "Execution example": "执行示例",
    "Sample parameters": "示例参数",
    "What is": "什么是",
    "run without any command line arguments": "不带任何命令行参数运行",
}


def translate_file(src_path, dst_path):
    """Translate a single RST file from English to Chinese."""
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Get the relative path for display
    rel = os.path.relpath(src_path, os.path.expanduser(
        '~/workspace/nuttx-docs-zh/_upstream/applications/examples'))

    # Parse out directory name for context
    parts = rel.split('/')
    example_name = parts[0] if parts else ''

    translated = translate_rst(content, example_name)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)

    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(translated)


def translate_rst(content, example_name):
    """Translate RST content preserving structure."""
    lines = content.split('\n')
    result = []
    in_code_block = False
    in_table = False
    table_separator_count = 0
    in_directive = False
    in_literal_block = False
    title_added_note = False

    i = 0
    while i < len(lines):
        line = lines[i]

        # Detect code blocks (.. code-block:: or :: or literal blocks)
        if re.match(r'\.\.\s+code-block::', line):
            in_code_block = True
            result.append(line)
            i += 1
            continue

        if in_code_block:
            # Code block ends when we hit a non-empty, non-indented line
            # or a blank line followed by a non-indented line
            if line.strip() == '':
                result.append(line)
                i += 1
                # Peek ahead
                if i < len(lines) and lines[i].strip() != '' and not lines[i].startswith('   '):
                    in_code_block = False
                elif i < len(lines) and lines[i].strip() == '':
                    # Double blank line ends code block
                    in_code_block = False
                continue
            elif not line.startswith('   ') and line.strip() != '':
                in_code_block = False
            else:
                result.append(line)
                i += 1
                continue

        # Detect tables (lines of ===)
        if re.match(r'^=+\s', line) or re.match(r'^=+$', line):
            in_table = True
            table_separator_count += 1
            result.append(line)
            i += 1
            continue

        if in_table:
            if table_separator_count >= 2 and line.strip() == '':
                in_table = False
                table_separator_count = 0
            result.append(line)
            i += 1
            continue

        # Detect literal block after :: directive
        if in_literal_block:
            if line.startswith('   ') or line.strip() == '':
                result.append(line)
                i += 1
                continue
            else:
                in_literal_block = False

        # Check for :: at end of line (literal block indicator)
        if line.rstrip().endswith('::') and not line.startswith('..'):
            in_literal_block = True

        # Detect RST directives (.. directive::)
        if re.match(r'^\.\.\s+\w', line):
            # Don't translate directives
            result.append(line)
            i += 1
            continue

        # Detect title underline (=== --- ~~~ ^^^ ***)
        if re.match(r'^[=\-~\^\*]{3,}\s*$', line):
            result.append(line)
            i += 1
            continue

        # Detect title line (line before underline)
        # Check if next line is a title underline
        if i + 1 < len(lines) and re.match(r'^[=\-~\^\*]{3,}\s*$', lines[i + 1]):
            # This is a title line - translate it
            translated_title = translate_line(line)
            result.append(translated_title)

            # Add note after first title (the main document title)
            if not title_added_note and re.match(r'^[=]{3,}\s*$', lines[i + 1]):
                result.append(lines[i + 1])  # underline
                i += 2
                title_added_note = True
                result.append('')
                result.append('.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/')
                result.append('')
                continue
            else:
                result.append(lines[i + 1])
                i += 2
                continue

        # Detect bullet points
        if re.match(r'^\s*[-*•]\s+', line):
            indent = len(line) - len(line.lstrip())
            bullet_char = line.strip()[0]
            rest = line.strip()[2:]  # Remove "- " or "* "
            translated_rest = translate_list_item(rest)
            result.append(' ' * indent + bullet_char + ' ' + translated_rest)
            i += 1
            continue

        # Detect numbered list items
        if re.match(r'^\s*\d+\.\s+', line):
            match = re.match(r'^(\s*\d+\.\s+)(.*)', line)
            if match:
                prefix = match.group(1)
                rest = match.group(2)
                translated_rest = translate_line(rest)
                result.append(prefix + translated_rest)
                i += 1
                continue

        # Detect cross-references and roles (don't translate)
        if ':doc:`' in line or ':ref:`' in line or ':c:func:`' in line or ':c:macro:`' in line:
            # Translate the prose part, keep the roles
            result.append(translate_line_with_roles(line))
            i += 1
            continue

        # Regular line - translate if it's prose
        if line.strip() == '' or line.strip().startswith('..') or line.startswith('   :'):
            result.append(line)
        else:
            result.append(translate_line(line))

        i += 1

    return '\n'.join(result)


def translate_line(line):
    """Translate a single line of prose text."""
    if not line.strip():
        return line

    # Don't translate lines that are mostly code/paths/config
    if is_code_line(line):
        return line

    return do_translate(line)


def translate_line_with_roles(line):
    """Translate a line that contains RST roles."""
    # This is complex - for now, do a simple translation
    return do_translate(line)


def translate_list_item(text):
    """Translate a list item, preserving Kconfig options and code."""
    return do_translate(text)


def is_code_line(line):
    """Check if a line is primarily code/configuration."""
    stripped = line.strip()

    # Lines starting with CONFIG_
    if stripped.startswith('CONFIG_') or stripped.startswith('``CONFIG_'):
        return True

    # Lines that are pure code
    if stripped.startswith('#include') or stripped.startswith('#define'):
        return True

    # Command lines
    if stripped.startswith('$ ') or stripped.startswith('nsh>'):
        return True

    # File paths
    if stripped.startswith('/') and ' ' not in stripped:
        return True

    return False


def do_translate(text):
    """Main translation function for English to Chinese."""
    if not text.strip():
        return text

    # Preserve leading/trailing whitespace
    leading = ''
    trailing = ''
    stripped = text.strip()

    if not stripped:
        return text

    leading_ws = text[:len(text) - len(text.lstrip())]
    trailing_ws = text[len(text.rstrip()):]

    # Translation map - comprehensive English to Chinese
    t = stripped

    # Short simple descriptions (one-liners)
    simple_translations = {
        "ABNT CODI example": "ABNT CODI 示例",
        "ADXL372 test program": "ADXL372 测试程序",
        "Audio tone generator example (RTTL player).": "音频音调生成器示例（RTTL 播放器）。",
        "Battery monitor example.": "电池监控示例。",
        "BME680 sensor example.": "BME680 传感器示例。",
        "BMI160 sensor example.": "BMI160 传感器示例。",
        "BMP180 Barometer sensor example.": "BMP180 气压传感器示例。",
        "Buttons driver example.": "按键驱动程序示例。",
        "PWM Capture example.": "PWM 捕获示例。",
        "TinyCBOR Test Example": "TinyCBOR 测试示例",
        "DroneCAN example.": "DroneCAN 示例。",
        "embedlog example.": "embedlog 示例。",
        "ESP32 HIMEM Example.": "ESP32 HIMEM 示例。",
        "Embedded Template Library (ETL) C++ example": "嵌入式模板库（ETL）C++ 示例",
        "Framebuffer overlay test tool.": "帧缓冲区叠加层测试工具。",
        "FM Synthesizer examples.": "FM 合成器示例。",
        "Hall effect sensor example.": "霍尔效应传感器示例。",
        "HDC1008 driver example.": "HDC1008 驱动程序示例。",
        "Hello World in Nim.": "Nim 语言的 Hello World 示例。",
        "Hello World in WASM.": "WASM 的 Hello World 示例。",
        "Hello World in Zig.": "Zig 语言的 Hello World 示例。",
        "I2S loopback test.": "I2S 环回测试。",
        "Rainbow example for ``APA102`` LED Strip.": "``APA102`` LED 灯带彩虹示例。",
        "APDS-9960 Test Application.": "APDS-9960 测试应用程序。",
        "Analog Joystick": "模拟摇杆",
        "Discrete Joystick": "离散摇杆",
        "Network Bridge": "网络桥接",
        "Read GPIO Buttons": "读取 GPIO 按键",
        "Camera Snapshot": "相机快照",
        "CAN Device Test": "CAN 设备测试",
        "ELF loader": "ELF 加载器",
        "FTP Client": "FTP 客户端",
        "FTP daemon": "FTP 守护进程",
        "Framebuffer": "帧缓冲区",
        "SMART Flash test": "SMART Flash 测试",
        "Serial Hardware Flow Control": "串口硬件流控",
        "FOC motor controller example": "FOC 电机控制器示例",
        "FT80x GUI Chip": "FT80x GUI 芯片",
        "GPIO Read and Write": "GPIO 读写",
        "GPS example": "GPS 示例",
        "USB Host HID keyboard": "USB 主机 HID 键盘",
        "Transfer Through I2C": "通过 I2C 传输",
        "Trivial IGMP": "简单 IGMP 测试",
        "Hello World": "Hello World",
        "Hello World in C++": "C++ 的 Hello World",
        "Current/Power Monitor INA219": "电流/功率监测器 INA219",
        "Current/Power Monitor INA226": "电流/功率监测器 INA226",
        "Humidity Sensor": "湿度传感器",
        "Calibration tool for udelay": "udelay 校准工具",
        "Ajdtime function example": "adjtime 函数示例",
        "Barometer sensor example": "气压传感器示例",
        "sensor example": "传感器示例",
    }

    # Try exact match first
    if t in simple_translations:
        return leading_ws + simple_translations[t] + trailing_ws

    # Longer translations for full paragraphs
    full_translations = {
        "A mindlessly simple test of an ADC devices. It simply reads from the ADC device\nand dumps the data to the console forever.": "一个非常简单的 ADC 设备测试。它只是从 ADC 设备读取数据，并将数据不断输出到控制台。",
        "This test depends on these specific ADC/NSH configurations settings (your\nspecific ADC settings might require additional settings).": "此测试依赖于以下特定的 ADC/NSH 配置设置（您特定的 ADC 设置可能需要额外的配置）。",
        "Specific configuration options for this example include:": "此示例的特定配置选项包括：",
        "A simple example that tests the alarm IOCTLs of the RTC driver.": "一个测试 RTC 驱动程序闹钟 IOCTL 的简单示例。",
        "Dependencies:": "依赖项：",
        "Configuration Pre-requisites:": "配置前置条件：",
        "Example Configuration:": "示例配置：",
        "NuttX configuration prerequisites:": "NuttX 配置前置条件：",
        "Optional NuttX configuration settings:": "可选的 NuttX 配置设置：",
        "NuttX configuration settings specific to this example:": "此示例特定的 NuttX 配置设置：",
        "Configuration options:": "配置选项：",
        "NuttX configuration settings:": "NuttX 配置设置：",
        "Also needed:": "还需要：",
        "Background\n----------": "背景\n------",
        "License\n-------": "许可证\n------",
    }

    if t in full_translations:
        return leading_ws + full_translations[t] + trailing_ws

    # For longer paragraphs, translate word by word / phrase by phrase
    result = translate_paragraph(t)
    return leading_ws + result + trailing_ws


def translate_paragraph(text):
    """Translate a paragraph of English text to Chinese."""
    # This is the core translation logic
    # We'll do pattern-based translation

    # Check if line contains backticks (inline code) - be careful
    # First, extract inline code segments
    segments = []
    remaining = text
    while '``' in remaining:
        idx = remaining.index('``')
        if idx > 0:
            segments.append(('text', remaining[:idx]))
        end_idx = remaining.index('``', idx + 2)
        segments.append(('code', remaining[idx:end_idx + 2]))
        remaining = remaining[end_idx + 2:]
    if remaining:
        segments.append(('text', remaining))

    # Translate only 'text' segments
    translated_parts = []
    for kind, part in segments:
        if kind == 'code':
            translated_parts.append(part)
        else:
            translated_parts.append(translate_prose(part))

    return ''.join(translated_parts)


def translate_prose(text):
    """Translate English prose to Chinese."""
    if not text.strip():
        return text

    # Comprehensive sentence-level translations
    replacements = [
        # Sentences about the application
        (r'This application demonstrates the usage of adjtime\(\) interface used to\nsynchronize system clock time if its value varies from real time \(usually get by\nexternal RTC\)\.',
         '此应用程序演示了 adjtime() 接口的用法，用于在系统时钟时间与实际时间不一致时（通常由外部 RTC 提供）进行同步。'),

        (r'This is a simple test of the analog joystick driver\. See details about this\ndriver in ``nuttx/include/nuttx/input/ajoystick\.h``\.',
         '这是模拟摇杆驱动程序的简单测试。有关此驱动程序的详细信息，请参阅 ``nuttx/include/nuttx/input/ajoystick.h``。'),

        (r'This is a simple test of the discrete joystick driver\. See details about this\ndriver in ``nuttx/include/nuttx/input/djoystick\.h``\.',
         '这是离散摇杆驱动程序的简单测试。有关此驱动程序的详细信息，请参阅 ``nuttx/include/nuttx/input/djoystick.h``。'),

        (r"A simple test of a system with multiple networks\. It simply echoes all UDP\npackets received on network ``1`` and network ``2`` to network ``2`` and network ``1``,\nrespectively\. Interface ``1`` and interface may or may not lie on the same\nnetwork\.",
         "多网络系统的简单测试。它将在网络 ``1`` 和网络 ``2`` 上接收到的所有 UDP 数据包分别回传到网络 ``2`` 和网络 ``1``。接口 ``1`` 和接口可能在同一网络上，也可能不在。"),

        (r'This directory contains a small program that will mount a ROMFS file system\ncontaining the BASIC test files extracted from the Bas ``2\.4`` release\.',
         '此目录包含一个小程序，它将挂载一个 ROMFS 文件系统，其中包含从 Bas ``2.4`` 版本中提取的 BASIC 测试文件。'),

        (r"This example builds a small ELF loader test case\. This includes several test\nprograms under ``examples/elf`` tests\. These tests are built using the relocatable\nELF format and installed in a configurable file system\. At run time, the file system\nis mounted and each program is executed\. Requires ``CONFIG_ELF``\.",
         "此示例构建了一个小型 ELF 加载器测试用例。这包括 ``examples/elf`` 测试下的多个测试程序。这些测试使用可重定位的 ELF 格式构建，并安装在可配置的文件系统中。在运行时，文件系统被挂载并执行每个程序。需要 ``CONFIG_ELF``。"),

        (r'Two distinct types of file systems are supported: internal \(included in the NuttX binary\)\nand external \(not included in the binary\)\. The external file systems need to be uploaded\nmanually\. For the internal file systems the sample supports the ``romfs`` and ``cromfs``\nfilesystems\. For the external file systems any of the provided file systems can be used\n\(``vfat``, \.\.\.\), but also the ``romfs`` filesystem for which the image \(``romfs\.img``\) is\nautomatically generated\.',
         '支持两种不同类型的文件系统：内部文件系统（包含在 NuttX 二进制文件中）和外部文件系统（不包含在二进制文件中）。外部文件系统需要手动上传。对于内部文件系统，示例支持 ``romfs`` 和 ``cromfs`` 文件系统。对于外部文件系统，可以使用任何提供的文件系统（``vfat`` 等），也可以使用 ``romfs`` 文件系统，其映像（``romfs.img``）会自动生成。'),

        (r'This is the mandatory, \"Hello, World\" example\. It is little more than\n``examples/null`` with a single ``printf`` statement\. Really useful only for\nbringing up new NuttX architectures\.',
         '这是必备的 "Hello, World" 示例。它只不过是 ``examples/null`` 加上一个 ``printf`` 语句。仅在开发新的 NuttX 架构时才真正有用。'),

        (r'This is C\+\+ version of the \"Hello, World\" example\. It is intended only to\nverify that the C\+\+ compiler is functional, that basic C\+\+ library support is\navailable, and that class are instantiated correctly\.',
         '这是 "Hello, World" 示例的 C++ 版本。它仅用于验证 C++ 编译器是否正常工作、基本的 C++ 库支持是否可用，以及类是否能正确实例化。'),

        (r'This is a simple FTP client shell used to exercise the capabilities of the FTPC\nlibrary \(``apps/netutils/ftpc``\)\.',
         '这是一个简单的 FTP 客户端 Shell，用于测试 FTPC 库（``apps/netutils/ftpc``）的功能。'),

        (r'This example exercises the FTPD daemon at ``apps/netutils/ftpd``\. Below are\nconfigurations specific to the FTPD example \(the FTPD daemon itself may require\nother configuration options as well\)\.',
         '此示例测试位于 ``apps/netutils/ftpd`` 的 FTPD 守护进程。以下是 FTPD 示例的特定配置（FTPD 守护进程本身可能还需要其他配置选项）。'),

        (r'This sample is implemented as ``camera`` command on NuttX Shell\. The synopsis of\nthe command is as below\.': '此示例在 NuttX Shell 中实现为 ``camera`` 命令。命令的概要如下。'),

        (r'If the CAN device is configured in loopback mode, then this example can be used\nto test the CAN device in loop back mode\. It simply sends a sequence of CAN\nmessages and verifies that those messages are returned exactly as sent\.',
         '如果 CAN 设备配置为环回模式，则此示例可用于测试 CAN 设备的环回功能。它只是发送一系列 CAN 消息，并验证这些消息是否与发送时完全一致返回。'),

        (r'This tool is used for calibrating the configuration option\n``CONFIG_BOARD_LOOPSPERMSEC``\. This option is used by NuttX to perform\nbusy-waiting \(i\.e\., spinning in a loop\) when a very basic busy-wait sleep is\nneeded in board logic\. This is also sometimes used when the timer-based sleep\nfunctions do not have a low enough resolution for shorter timings \(i\.e\. system\ntick every 1ms but you want to sleep for 100us\)\.',
         '此工具用于校准配置选项 ``CONFIG_BOARD_LOOPSPERMSEC``。NuttX 使用此选项在板级逻辑中需要非常基本的忙等待休眠时执行忙等待（即在循环中旋转）。当基于定时器的休眠函数对较短的计时没有足够低的分辨率时（即系统每 1ms 一次 tick 但您希望休眠 100us），有时也会使用此选项。'),

        (r"When porting NuttX a new board, this example program is very useful to get a\ncalibrated value for ``CONFIG_BOARD_LOOPSPERMSEC``\.",
         "在将 NuttX 移植到新板时，此示例程序对于获取 ``CONFIG_BOARD_LOOPSPERMSEC`` 的校准值非常有用。"),

        (r'This application is a simple demonstration which serves to test the\n:doc:`framebuffer character driver': '此应用程序是一个简单的演示，用于测试 :doc:`framebuffer character driver'),

        (r'This example can be used to interact with GPS devices in NuttX\. It uses the\n`MINMEA': '此示例可用于与 NuttX 中的 GPS 设备进行交互。它使用 `MINMEA'),

        (r'library to parse standard NMEA\nmessages and print out GPS data to the console\.\n\nTo use the program, provide the character device path for the GPS serial\nconnection as the only argument\. If no path is provided, the program will\ndefault to ``/dev/ttyS1``\.\n\nIf you want to be able to see the floating point output of this program, make\nsure you remember to enable ``CONFIG_LIBC_FLOATINGPOINT``\.\n\nThe program loops forever parsing NMEA values from the serial device\.',
         '库来解析标准 NMEA 消息，并将 GPS 数据打印到控制台。\n\n要使用此程序，请将 GPS 串行连接的字符设备路径作为唯一参数提供。如果未提供路径，程序将默认使用 ``/dev/ttyS1``。\n\n如果您想看到此程序的浮点输出，请确保启用 ``CONFIG_LIBC_FLOATINGPOINT``。\n\n程序将持续循环解析来自串行设备的 NMEA 值。'),

        (r'This example performs a SMART flash block device test\. This test performs a\nsector allocate, read, write, free and garbage collection test on a SMART MTD\nblock device\.',
         '此示例执行 SMART Flash 块设备测试。此测试在 SMART MTD 块设备上执行扇区分配、读取、写入、释放和垃圾回收测试。'),

        (r'This application performs a SMART flash block device test\. This test performs a\nsector allocate, read, write, free and garbage collection test on a SMART MTD\nblock device\. This test can be built only as an NSH command',
         '此应用程序执行 SMART Flash 块设备测试。此测试在 SMART MTD 块设备上执行扇区分配、读取、写入、释放和垃圾回收测试。此测试只能构建为 NSH 命令'),

        (r'This test uses internal OS interfaces and so is not available in the\nNUTTX kernel build': '此测试使用内部 OS 接口，因此在 NUTTX 内核构建中不可用'),

        (r'A simple test of serial hardware flow control\.': '串口硬件流控的简单测试。'),

        (r'The main purpose of this example is to provide a universal template to\nimplement the motor controller based on the kernel-side FOC device and\nthe application-side FOC library\.',
         '此示例的主要目的是提供一个通用模板，用于基于内核端 FOC 设备和应用程序端 FOC 库实现电机控制器。'),

        (r'At the moment, this example implements a simple open-loop velocity controller\.',
         '目前，此示例实现了一个简单的开环速度控制器。'),

        (r'This example has not yet implemented any mechanism to protect the\npowered device\. This means that there is no overtemeprature\nprotection, no overcurrent protection and no overvoltage protection\.',
         '此示例尚未实现任何保护供电设备的机制。这意味着没有过温保护、没有过流保护，也没有过压保护。'),

        (r'Make sure that you power the device properly and provide current\nlimits on your own so as not to break your hardware\.',
         '请确保正确供电并自行提供电流限制，以免损坏硬件。'),

        (r'The FOC PI current controller parameters can be obtained from the given\nequations:': 'FOC PI 电流控制器参数可从以下公式获得：'),

        (r'Sample parameters for some commercially available motors': '一些商用电机的示例参数'),

        (r'This examples has ports of several FTDI demos for the FTDI/BridgeTek FT80x GUI\nchip\. As an example configuration, see\n``nuttx/boards/arm/stm32/viewtool-stm32f107/configs/ft80x/defconfig``\.',
         '此示例移植了多个 FTDI 演示程序，用于 FTDI/BridgeTek FT80x GUI 芯片。示例配置请参阅 ``nuttx/boards/arm/stm32/viewtool-stm32f107/configs/ft80x/defconfig``。'),

        (r'This example exercises ``netutils/discover`` utility\. This example initializes and\nstarts the UDP discover daemon\. This daemon is useful for discovering devices in\nlocal networks, especially with DHCP configured devices\. It listens for UDP\nbroadcasts which also can include a device class so that groups of devices can\nbe discovered\. It is also possible to address all classes with a kind of\nbroadcast discover\.',
         '此示例测试 ``netutils/discover`` 工具。此示例初始化并启动 UDP 发现守护进程。此守护进程用于发现本地网络中的设备，特别是使用 DHCP 配置的设备。它监听 UDP 广播，广播可以包含设备类别，以便发现设备组。也可以通过一种广播发现来寻址所有类别。'),

        (r'This example will automatically be built as an NSH built-in if\n``CONFIG_NSH_BUILTIN_APPS`` is selected\. Otherwise, it will be a standalone\nprogram with entry point ``discover_main``\.',
         '如果选择了 ``CONFIG_NSH_BUILTIN_APPS``，此示例将自动构建为 NSH 内置应用。否则，它将作为独立程序运行，入口点为 ``discover_main``。'),

        (r'This is a simple test of the NuttX GPIO driver\.': 'NuttX GPIO 驱动程序的简单测试。'),

        (r'This is a simple infinite loop that polls the ``INA219`` sensor and displays the\nmeasurements\.': '这是一个简单的无限循环，轮询 ``INA219`` 传感器并显示测量结果。'),

        (r'This is a simple infinite loop that polls the ``INA226`` sensor and displays the\nmeasurements\.': '这是一个简单的无限循环，轮询 ``INA226`` 传感器并显示测量结果。'),

        (r'This is a trivial test of the NuttX IGMP capability\. It present it does not do\nmuch of value – Much more is needed in order to verify the IGMP features\!',
         '这是 NuttX IGMP 功能的简单测试。目前它没有做太多有价值的工作——要验证 IGMP 功能还需要更多测试！'),

        (r'A mindlessly simple test of an I2C driver\. It reads an write garbage data to the\nI2C transmitter and/or received as fast possible\.',
         '一个非常简单的 I2C 驱动程序测试。它尽可能快地读取和写入垃圾数据到 I2C 发送器和/或接收器。'),

        (r'This test depends on these specific I2S/AUDIO/NSH configurations settings \(your\nspecific I2S settings might require additional settings\)\.',
         '此测试依赖于以下特定的 I2S/AUDIO/NSH 配置设置（您特定的 I2S 设置可能需要额外的配置）。'),

        (r'A simple reader example for the ``HTS221`` humidity sensor\.',
         '``HTS221`` 湿度传感器的简单读取示例。'),

        (r"This is a simple test to ``debug/verify`` the USB host HID keyboard class driver\.",
         "这是 USB 主机 HID 键盘类驱动程序的简单``调试/验证``测试。"),

        (r'Bas is an interpreter for the classic dialect of the programming language BASIC\.\nIt is pretty compatible to typical BASIC interpreters of the 1980s, unlike some\nother UNIX BASIC interpreters, that implement a different syntax, breaking\ncompatibility to existing programs\. Bas offers many ANSI BASIC statements for\nstructured programming, such as procedures, local variables and various loop\ntypes\. Further there are matrix operations, automatic LIST indentation and many\nstatements and functions found in specific classic dialects\. Line numbers are\nnot required\.',
         'Bas 是编程语言 BASIC 经典方言的解释器。它与 1980 年代典型的 BASIC 解释器非常兼容，不像其他一些 UNIX BASIC 解释器实现了不同的语法，破坏了与现有程序的兼容性。Bas 提供了许多用于结构化编程的 ANSI BASIC 语句，如过程、局部变量和各种循环类型。此外还有矩阵操作、自动 LIST 缩进以及特定经典方言中的许多语句和函数。不需要行号。'),

        (r'The interpreter tokenises the source and resolves references to variables and\njump targets before running the program\. This compilation pass increases\nefficiency and catches syntax errors, type errors and references to variables\nthat are never initialised\. Bas is written in ANSI C for UNIX systems\.',
         '解释器在运行程序之前对源代码进行分词并解析变量和跳转目标的引用。此编译过程提高了效率并捕获语法错误、类型错误以及从未初始化的变量引用。Bas 使用 ANSI C 为 UNIX 系统编写。'),

        (r'From NSH, the startup command sequence is as follows\. This is only an example,\nyour configuration could have different mass storage devices, mount paths, and\nFTP directories:': '从 NSH 启动的命令序列如下。这只是一个示例，您的配置可能有不同的存储设备、挂载路径和 FTP 目录：'),

        (r'The output will show ``nan`` and ``0`` for values while waiting to obtain a fix,\nat which point real values will begin to appear\.',
         '在等待定位期间，输出将显示 ``nan`` 和 ``0``，定位后将开始显示实际值。'),

        (r'You can now see the information is filled in with the data from the GPS\.',
         '您现在可以看到信息已填入来自 GPS 的数据。'),

        (r'Fixed-point readings may have a different scale than the floating-point\nreadings\. For instance, the altitude above is fixed-point, but is actually\n73\.172 meters in floating point\.',
         '定点读数可能与浮点读数具有不同的比例。例如，上面的高度是定点的，但实际上是浮点的 73.172 米。'),

        (r'Storage will be selected automatically based on the available storage option\.',
         '存储将根据可用的存储选项自动选择。'),

        (r'where you need to replace ``/dev/ttyACM0`` with your selected serial device\.',
         '您需要将 ``/dev/ttyACM0`` 替换为您选择的串行设备。'),
    ]

    for eng, chn in replacements:
        text = text.replace(eng, chn)

    # More targeted replacements
    additional = [
        ('The default behavior assumes loopback mode. Messages are sent, then read and\nverified. The behavior can be altered for other kinds of testing where the test\nonly sends or received (but does not verify) can messages.',
         '默认行为假设为环回模式。消息被发送，然后读取并验证。对于其他类型的测试（仅发送或接收但不验证 CAN 消息），可以更改此行为。'),
        ('Only receive messages.', '仅接收消息。'),
        ('Only send messages.', '仅发送消息。'),
        ('Enables CAN support.', '启用 CAN 支持。'),
        ('Enables the simple UDP bridge test.', '启用简单的 UDP 桥接测试。'),
        ('Enables the FLASH Test.', '启用 FLASH 测试。'),
        ('Enable the FTPD example.', '启用 FTPD 示例。'),
        ('Enable the RTC driver alarm test.', '启用 RTC 驱动程序闹钟测试。'),
        ('Enable the analog joystick example.', '启用模拟摇杆示例。'),
        ('Enable the discrete joystick example.', '启用离散摇杆示例。'),
        ('Enable the I2C test.', '启用 I2C 测试。'),
        ('Enables the I2C test.', '启用 I2C 测试。'),
        ('The analog joystick driver.', '模拟摇杆驱动程序。'),
        ('The discrete joystick driver.', '离散摇杆驱动程序。'),
        ('RTS device must be initialized to allow user space\n  access to the RTC.',
         'RTC 驱动程序必须初始化以允许用户空间访问 RTC。'),
        ('Support for RTC alarms must be enabled.', '必须启用 RTC 闹钟支持。'),
        ('RTC device path', 'RTC 设备路径'),
        ('Alarm signal.', '闹钟信号。'),
        ('Alarm daemon priority.', '闹钟守护进程优先级。'),
        ('Alarm daemon stack size.', '闹钟守护进程栈大小。'),
        ('Joystick device name.', '摇杆设备名称。'),
        ('Signal used to signal the test\n  application.', '用于通知测试应用程序的信号。'),
        ('Signal used to signal the test\napplication.', '用于通知测试应用程序的信号。'),
        ('A CAN driver may or may not support a loopback mode\n  for testing. The STM32 CAN driver does support loopback mode.',
         'CAN 驱动程序可能支持也可能不支持用于测试的环回模式。STM32 CAN 驱动程序支持环回模式。'),
        ('Build the CAN test as an NSH built-in function.\n  Default: Built as a standalone program.',
         '将 CAN 测试构建为 NSH 内置函数。默认：构建为独立程序。'),
        ('Build the ADC test as an NSH built-in function.\n  Default: Built as a standalone program.',
         '将 ADC 测试构建为 NSH 内置函数。默认：构建为独立程序。'),
        ('Build the I2S test as an NSH built-in function.\n  Default: Built as a standalone program.',
         '将 I2S 测试构建为 NSH 内置函数。默认：构建为独立程序。'),
        ('Enabled ADC support.', '启用 ADC 支持。'),
        ('Enabled I2S support.', '启用 I2S 支持。'),
        ('Enabled audio support.', '启用音频支持。'),
        ('Enable audio device support.', '启用音频设备支持。'),
        ('Enabled support for the I2S character device.', '启用 I2S 字符设备支持。'),
        ('The path to the CAN device.', 'CAN 设备的路径。'),
        ('The default path to the ADC device.', 'ADC 设备的默认路径。'),
        ('The minor device number of the ROMFS block\n  driver. For example, the ``N`` in ``/dev/ramN``. Used for registering the\n  RAM block driver that will hold the ROMFS file system containing the BASIC\n  files to be tested. Default:',
         'ROMFS 块驱动程序的次设备号。例如，``/dev/ramN`` 中的 ``N``。用于注册将保存包含 BASIC 测试文件的 ROMFS 文件系统的 RAM 块驱动程序。默认值：'),
        ('The minor device number of the ROMFS block\n  driver. For example, the ``N`` in ``/dev/ramN``. Used for registering the\n  RAM block driver that will hold the ROMFS file system containing the ELF\n  executables to be tested. Default:',
         'ROMFS 块驱动程序的次设备号。例如，``/dev/ramN`` 中的 ``N``。用于注册将保存包含 ELF 可执行测试文件的 ROMFS 文件系统的 RAM 块驱动程序。默认值：'),
        ('The path to the ROMFS block driver device.\n  This must match ``EXAMPLES_BASTEST_DEVMINOR``. Used for registering the RAM\n  block driver that will hold the ROMFS file system containing the BASIC files\n  to be tested. Default:',
         'ROMFS 块驱动程序设备的路径。必须与 ``EXAMPLES_BASTEST_DEVMINOR`` 匹配。用于注册将保存包含 BASIC 测试文件的 ROMFS 文件系统的 RAM 块驱动程序。默认值：'),
        ('The path to the ROMFS block driver device.\n  This must match ``EXAMPLES_ELF_DEVMINOR``. Used for registering the RAM block\n  driver that will hold the ROMFS file system containing the ELF executables to\n  be tested. Default:',
         'ROMFS 块驱动程序设备的路径。必须与 ``EXAMPLES_ELF_DEVMINOR`` 匹配。用于注册将保存包含 ELF 可执行测试文件的 ROMFS 文件系统的 RAM 块驱动程序。默认值：'),
        ('network device name', '网络设备名称'),
        ('The register name of the network ``n``\n  device. Must match the previously registered driver name and must not be the\n  same as other',
         '网络 ``n`` 设备的注册名称。必须与先前注册的驱动程序名称匹配，且不能与其他'),
        ('listen port number.', '监听端口号。'),
        ('send port number.', '发送端口号。'),
        ('send/receive I/O buffer.', '发送/接收 I/O 缓冲区。'),
        ('daemon stacksize.', '守护进程栈大小。'),
        ('daemon task priority.', '守护进程任务优先级。'),
        ('If used as a NSH add-on, then it is assumed that initialization of both networks\nwas performed externally prior to the time that this test was started.\nOtherwise, the following options are available:',
         '如果用作 NSH 附加组件，则假定在测试开始之前，两个网络的初始化已在外部完成。否则，以下选项可用：'),
        ('Select of the network ``n`` hardware does\n  not have a built-in MAC address. If selected, the MAC address. provided by\n  ``CONFIG_EXAMPLES_BRIDGE_NETn_MACADDR`` will be used to assign the MAC address\n  to the network n device.',
         '选择网络 ``n`` 硬件是否没有内置 MAC 地址。如果选择，将使用 ``CONFIG_EXAMPLES_BRIDGE_NETn_MACADDR`` 提供的 MAC 地址分配给网络 n 设备。'),
        ('Use DHCP Client to get the network n IP\n  address.', '使用 DHCP 客户端获取网络 n 的 IP 地址。'),
        ('is not selected, then this is the fixed IP address for network ``n``.',
         '未选择，则这是网络 ``n`` 的固定 IP 地址。'),
        ('default router IP address\n  (Gateway).', '默认路由器 IP 地址（网关）。'),
        ('mask.', '掩码。'),
        ('If you are testing any drivers and have unexpected issues with them, make\nsure that this configuration option has been calibrated. It can cause\nbad/incorrect timings in drivers if not calibrated.',
         '如果您在测试驱动程序时遇到意外问题，请确保此配置选项已校准。如果未校准，可能会导致驱动程序中的时序错误/不正确。'),
        ('You can simply copy paste the value from the console output and use it as the\nvalue for your board by setting it in the Kconfig menu.',
         '您可以简单地从控制台输出中复制粘贴该值，并在 Kconfig 菜单中设置它作为您板子的值。'),
        ('The program is run without any arguments. Configuration options for how the\nprogram runs (taking more measurements, etc.) can be seen in its Kconfig menu.\nPress ``h`` with the configuration option highlighted under your cursor to read\nthe help text about what each option does.',
         '程序在不带任何参数的情况下运行。程序运行方式的配置选项（进行更多测量等）可以在其 Kconfig 菜单中查看。将光标高亮显示在配置选项上按 ``h`` 可以阅读每个选项作用的帮助文本。'),
        ('Here is the example output from running the application:',
         '以下是运行应用程序的示例输出：'),
        ('Here is an example of the console output:',
         '以下是控制台输出的示例：'),
        ("A simple reader example for the", "一个简单的读取示例，用于"),
        ('where:\n  - Kp  - PI proportional coefficient', '其中：\n  - Kp  - PI 比例系数'),
        ('- Ki  - PI integral coefficient', '- Ki  - PI 积分系数'),
        ('- Rs  - average phase serial resistance', '- Rs  - 平均相串联电阻'),
        ('- Ls  - average phase serial inductance', '- Ls  - 平均相串联电感'),
        ('- pp  - pole plant', '- pp  - 极点'),
        ('- ccb - current control bandwidth', '- ccb - 电流控制带宽'),
        ('- T   - sampling period', '- T   - 采样周期'),
        ('The following configuration options must be enabled:', '以下配置选项必须启用：'),
        ('Enable board spinlock support', '启用板级自旋锁支持'),
        ('Header Files\n------------\n\nInclude the following headers in your application:',
         '头文件\n------\n\n在您的应用程序中包含以下头文件：'),
        ('Data Structures\n---------------\n\nThe BOARDIOC_SPINLOCK interface uses the following structure:',
         '数据结构\n--------\n\nBOARDIOC_SPINLOCK 接口使用以下结构：'),
        ('Actions\n-------\n\nThe following action values are supported:',
         '操作\n------\n\n支持以下操作值：'),
        ('Return Values\n^^^^^^^^^^^^^\n\n* **0** - Success\n* **Negative value** - Error code (converted to errno)',
         '返回值\n^^^^^^\n\n* **0** - 成功\n* **负值** - 错误代码（转换为 errno）'),
        ('Simple Lock Example\n-------------------\n\nHere\'s a basic example of acquiring and releasing a spinlock:',
         '简单锁示例\n----------\n\n以下是获取和释放自旋锁的基本示例：'),
        ('The program supports different features depending on the characteristics of the\nframebuffer driver. If the framebuffer requires ``FB_UPDATE``, this example\nbehaves accordingly.',
         '程序根据帧缓冲区驱动程序的特性支持不同的功能。如果帧缓冲区需要 ``FB_UPDATE``，此示例将相应地执行。'),
        ('If the framebuffer supports ``FB_OVERLAY``, then the application also supports\ngetting and displaying the overlay information.',
         '如果帧缓冲区支持 ``FB_OVERLAY``，则应用程序还支持获取和显示叠加层信息。'),
        ('If the virtual y resolution is double that of the y resolution when the\nframebuffer is initially queried, the application will attempt to use\ndouble-buffer rendering by fetching a second framebuffer corresponding to the\n``display + 1``, where ``display`` is the display number that was associated\nwith the first framebuffer.',
         '如果虚拟 y 分辨率是初始查询帧缓冲区时 y 分辨率的两倍，应用程序将尝试使用双缓冲渲染，通过获取对应于 ``display + 1`` 的第二个帧缓冲区，其中 ``display`` 是与第一个帧缓冲区关联的显示编号。'),
        ('The application ignores the pixel format provided by the framebuffer character\ndriver, and only inspects the \'bits per pixel\' (depth) field. Currently, only\nthe following bits per pixel are supported (with the corresponding formats\nassumed):',
         '应用程序忽略帧缓冲区字符驱动程序提供的像素格式，仅检查"每像素位数"（深度）字段。目前仅支持以下每像素位数（假定对应格式）：'),
        ('Skipping issues like this one can generally be avoided by rendering to a\nseparate buffer first, and then copying that buffer to the framebuffer in one\noperation.',
         '此类跳过问题通常可以通过先渲染到单独的缓冲区，然后将该缓冲区一次性复制到帧缓冲区来避免。'),
        ('The program interacts with the framebuffer through the interfaces described in\nthe linked page in order to render a very simple image consisting of 6\nconcentric, colourful rectangles. Note that between each rectangle, the program\nsleeps for 500 milliseconds. Rectangle are drawn from outermost to innermost, in\ndescending size.',
         '程序通过链接页面中描述的接口与帧缓冲区交互，以渲染由 6 个同心彩色矩形组成的非常简单的图像。注意在每个矩形之间，程序休眠 500 毫秒。矩形从最外层到最内层按递减大小绘制。'),
        ('The image displayed by the ``fb`` example, shown on the Pinephone. Credit to\nLup Yuen Lee.',
         '``fb`` 示例显示的图像，在 Pinephone 上展示。由 Lup Yuen Lee 提供。'),
        ('The application renders directly to the framebuffer provided by the character\ndriver. On some devices, the entire rendering operation may not be complete\nin time for the video synchronization, causing screen tearing or skips. This\nis the case for the',
         '应用程序直接渲染到字符驱动程序提供的帧缓冲区。在某些设备上，整个渲染操作可能无法及时完成视频同步，导致画面撕裂或跳过。这就是'),
        ('and the results can\nbe seen below.', '的情况，结果如下所示。'),
        ('The framebuffer example output, but with skipped pixels.', '帧缓冲区示例输出，但有像素跳过。'),
        ('BoardIOC_SPINLOCK Spinlock Example', 'BOARDIOC_SPINLOCK 自旋锁示例'),
        ('This example demonstrates the usage of the BOARDIOC_SPINLOCK board control\ninterface for managing hardware spinlock operations in NuttX. The BOARDIOC_SPINLOCK\ninterface provides a low-level mechanism to synchronize access to shared resources\nacross multiple threads or CPUs using spinlock primitives.',
         '此示例演示了 BOARDIOC_SPINLOCK 板控制接口在 NuttX 中管理硬件自旋锁操作的用法。BOARDIOC_SPINLOCK 接口提供了一种底层机制，用于使用自旋锁原语同步多线程或 CPU 之间对共享资源的访问。'),
        ('BOARDIOC_SPINLOCK is a board control request that allows applications to perform\natomic spinlock operations through the boardctl() interface.',
         'BOARDIOC_SPINLOCK 是一个板控制请求，允许应用程序通过 boardctl() 接口执行原子自旋锁操作。'),
        ('The BOARDIOC_SPINLOCK interface supports three primary operations:',
         'BOARDIOC_SPINLOCK 接口支持三种主要操作：'),
        ('Acquire a spinlock (blocks until available)', '获取自旋锁（阻塞直到可用）'),
        ('Try to acquire a spinlock (non-blocking)', '尝试获取自旋锁（非阻塞）'),
        ('Release a spinlock', '释放自旋锁'),
        ('Acquire lock (blocks if unavailable)', '获取锁（如果不可用则阻塞）'),
        ('Try to acquire (non-blocking)', '尝试获取（非阻塞）'),
        ('Release lock', '释放锁'),
        ('Initialize the spinlock', '初始化自旋锁'),
        ('Acquire the spinlock', '获取自旋锁'),
        ('Spinlock acquired successfully', '自旋锁获取成功'),
        ('Failed to acquire spinlock', '获取自旋锁失败'),
        ('Inside spinlock', '在自旋锁内'),
        ('Release the spinlock', '释放自旋锁'),
        ('Spinlock released successfully', '自旋锁释放成功'),
        ('The receiver side enter, start the receiver program. The receiver is now\nwaiting to receive data on the configured serial port.',
         '接收端输入并启动接收程序。接收器现在正在等待从配置的串口接收数据。'),
        ('On the sender side start the sender program. This will send data to the\nreceiver which will verify that no data is lost.',
         '在发送端启动发送程序。这将向接收器发送数据，接收器将验证没有数据丢失。'),
        ('On Linux, you can alternatively do:', '在 Linux 上，您也可以执行：'),
        ('This application demonstrates', '此应用程序演示'),
        ('simple test', '简单测试'),
        ('Simple test', '简单测试'),
    ]

    for eng, chn in additional:
        text = text.replace(eng, chn)

    return text


def main():
    src_base = os.path.expanduser('~/workspace/nuttx-docs-zh/_upstream/applications/examples')
    dst_base = os.path.expanduser('~/workspace/nuttx-docs-zh/applications/examples')

    # Get first 65 files
    files = []
    for root, dirs, fnames in os.walk(src_base):
        for fname in fnames:
            if fname.endswith('.rst'):
                files.append(os.path.join(root, fname))
    files.sort()
    files = files[:65]

    print(f"Processing {len(files)} files...")

    for src in files:
        rel = os.path.relpath(src, src_base)
        dst = os.path.join(dst_base, rel)
        print(f"  Translating: {rel}")
        translate_file(src, dst)

    print(f"\nDone! Translated {len(files)} files.")


if __name__ == '__main__':
    main()
