#!/usr/bin/env python3
"""
sync.py — NuttX 文档增量同步工具

功能：
  1. snapshot: 快照当前上游 NuttX 文档的 SHA，用于后续对比
  2. diff:     对比上游变更，标记需重新翻译的文件
  3. status:   显示翻译进度

用法：
  python3 sync.py snapshot --upstream ~/workspace/nuttx/Documentation
  python3 sync.py diff     --upstream ~/workspace/nuttx/Documentation
  python3 sync.py status
"""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

UPSTREAM_DIR = "_upstream"
SNAPSHOT_FILE = os.path.join(UPSTREAM_DIR, "sha_snapshot.json")
STATUS_FILE = "TRANSLATION_STATUS.json"


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def scan_rst_files(root: str) -> dict[str, str]:
    """扫描目录下所有 .rst 文件，返回 {相对路径: sha256}"""
    result = {}
    for dirpath, _, filenames in os.walk(root):
        for f in sorted(filenames):
            if not f.endswith(".rst"):
                continue
            full = os.path.join(dirpath, f)
            rel = os.path.relpath(full, root)
            result[rel] = sha256_file(full)
    return result


def load_json(path: str) -> dict:
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}


def save_json(path: str, data: dict):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, sort_keys=True)


def cmd_snapshot(args):
    """快照上游文档 SHA"""
    upstream = args.upstream
    if not os.path.isdir(upstream):
        print(f"❌ 上游目录不存在: {upstream}")
        sys.exit(1)

    files = scan_rst_files(upstream)
    save_json(SNAPSHOT_FILE, files)
    print(f"✅ 快照完成: {len(files)} 个 rst 文件 -> {SNAPSHOT_FILE}")


def cmd_diff(args):
    """对比上游变更"""
    upstream = args.upstream
    old = load_json(SNAPSHOT_FILE)
    if not old:
        print("❌ 没有快照，请先运行: python3 sync.py snapshot --upstream <path>")
        sys.exit(1)

    new = scan_rst_files(upstream)

    added = set(new) - set(old)
    removed = set(old) - set(new)
    modified = {f for f in set(new) & set(old) if new[f] != old[f]}

    status = load_json(STATUS_FILE)

    print(f"\n📊 上游变更报告:")
    print(f"   新增: {len(added)} 个文件")
    print(f"   删除: {len(removed)} 个文件")
    print(f"   修改: {len(modified)} 个文件")

    if added:
        print(f"\n🟢 新增文件:")
        for f in sorted(added):
            print(f"   + {f}")
            status[f] = {"state": "new", "upstream_sha": new[f]}

    if removed:
        print(f"\n🔴 删除文件:")
        for f in sorted(removed):
            print(f"   - {f}")
            status.pop(f, None)

    if modified:
        print(f"\n🟡 修改文件（需重新翻译）:")
        for f in sorted(modified):
            print(f"   ~ {f}")
            status[f] = {"state": "needs_update", "upstream_sha": new[f]}

    if not added and not removed and not modified:
        print("\n✅ 无变更")

    save_json(STATUS_FILE, status)
    print(f"\n状态已保存到 {STATUS_FILE}")


def cmd_status(args):
    """显示翻译进度"""
    status = load_json(STATUS_FILE)
    if not status:
        print("❌ 没有翻译状态，请先运行 sync.py snapshot + diff")
        sys.exit(1)

    total = len(status)
    done = sum(1 for v in status.values() if v.get("state") == "done")
    in_progress = sum(1 for v in status.values() if v.get("state") == "in_progress")
    needs_update = sum(1 for v in status.values() if v.get("state") == "needs_update")
    new_files = sum(1 for v in status.values() if v.get("state") == "new")
    pending = total - done - in_progress - needs_update - new_files

    print(f"\n📊 翻译进度:")
    print(f"   总计:      {total}")
    print(f"   已完成:    {done} ({done*100//total if total else 0}%)")
    print(f"   翻译中:    {in_progress}")
    print(f"   需更新:    {needs_update}")
    print(f"   新增待翻:  {new_files}")
    print(f"   未开始:    {pending}")

    if needs_update > 0:
        print(f"\n🟡 需重新翻译的文件:")
        for f, v in sorted(status.items()):
            if v.get("state") == "needs_update":
                print(f"   ~ {f}")


def cmd_mark_done(args):
    """标记文件为已翻译"""
    status = load_json(STATUS_FILE)
    for f in args.files:
        if f in status:
            status[f]["state"] = "done"
            print(f"  ✅ {f}")
        else:
            print(f"  ⚠️ {f} 不在状态文件中")
    save_json(STATUS_FILE, status)


def main():
    parser = argparse.ArgumentParser(description="NuttX 文档增量同步工具")
    sub = parser.add_subparsers(dest="cmd")

    p_snap = sub.add_parser("snapshot", help="快照上游文档 SHA")
    p_snap.add_argument("--upstream", required=True, help="上游 NuttX Documentation 目录")

    p_diff = sub.add_parser("diff", help="对比上游变更")
    p_diff.add_argument("--upstream", required=True, help="上游 NuttX Documentation 目录")

    sub.add_parser("status", help="显示翻译进度")

    p_mark = sub.add_parser("mark-done", help="标记文件为已翻译")
    p_mark.add_argument("files", nargs="+", help="文件路径")

    args = parser.parse_args()
    if args.cmd == "snapshot":
        cmd_snapshot(args)
    elif args.cmd == "diff":
        cmd_diff(args)
    elif args.cmd == "status":
        cmd_status(args)
    elif args.cmd == "mark-done":
        cmd_mark_done(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
