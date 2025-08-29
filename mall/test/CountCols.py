#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
import time
from datetime import datetime

# ========== 配置 ==========
OUTPUT_FILE = r"D:\\tmp\\cc\\excel_columns.txt"       # 每个文件的列信息
UNION_FILE = r"D:\\tmp\\cc\\all_columns_union.txt"    # 所有文件字段的并集
FILE_LIST = r"D:\\tmp\\cc\\target_files.txt"          # 存放需要处理的500个文件（全路径，每行一个）
# ========== 配置结束 ==========

def main():
    # 读取目标文件路径（全路径）
    with open(FILE_LIST, "r", encoding="utf-8") as f:
        target_files = [line.strip() for line in f if line.strip()]

    start_time = time.time()
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    results = []
    union_cols = set()   # 存放并集字段

    for file_path in target_files:
        print(file_path)
        if not os.path.exists(file_path):
            results.append(f"{file_path} -> 文件不存在")
            continue
        try:
            # 读取第一行作为表头
            df = pd.read_excel(file_path, engine="openpyxl", header=0)
            cols = df.columns.tolist()
            union_cols.update(cols)  # 加入并集
            results.append(f"{file_path} -> (总列数: {len(cols)}, 列: {cols})")
        except Exception as e:
            results.append(f"{file_path} -> 读取失败: {str(e)}")

    # 保存逐个文件结果
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(results))

    # 保存并集结果
    with open(UNION_FILE, "w", encoding="utf-8") as f:
        f.write(f"字段总数: {len(union_cols)}\n")
        f.write("字段列表:\n")
        f.write("\n".join(sorted(union_cols)))

    end_time = time.time()
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"总耗时: {end_time - start_time:.2f} 秒")
    print(f"文件结果已写入: {OUTPUT_FILE}")
    print(f"字段并集已写入: {UNION_FILE}")

if __name__ == "__main__":
    main()
