#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量删除delete.txt记录的本地文件"""
import os
import sys
from datetime import datetime

# 配置文件路径
DELETE_LIST_FILE = r"D:\\tmp\\cc\\v2\\delete.txt"  # 存放要删除的文件路径列表
LOG_FILE = "delete.log"          # 日志文件


def log(msg: str):
    """写日志"""
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{time_str}] {msg}\n")
    print(msg)


def main():
    if not os.path.exists(DELETE_LIST_FILE):
        log(f"❌ 未找到 {DELETE_LIST_FILE} 文件")
        sys.exit(1)

    with open(DELETE_LIST_FILE, "r", encoding="utf-8") as f:
        files = [line.strip() for line in f if line.strip()]

    if not files:
        log("⚠️ delete.txt 为空，没有需要删除的文件")
        return

    for filepath in files:
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                log(f"✅ 已删除: {filepath}")
            else:
                log(f"⚠️ 文件不存在: {filepath}")
        except Exception as e:
            log(f"❌ 删除失败: {filepath}, 错误: {e}")


if __name__ == "__main__":
    main()
