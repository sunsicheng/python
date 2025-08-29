#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统计 CSV 文件中 data_id 列不为空的行数，并打印进度"""

import os
import pandas as pd

# ===== 配置 =====
TARGET_DIR = r"D:\\tmp\\cc\\v4\\bak_csv_v2"   # 要统计的目录
OUTPUT_FILE = r"D:\\tmp\\cc\\v4\\compare\\csv_real_count.csv"  # 保存结果
ENCODINGS = ['utf-8', 'GBK']  # 尝试编码顺序
CHUNK_SIZE = 100000  # 分块读取，支持大文件

def count_data_id_nonempty(directory):
    results = []
    # 收集所有 CSV 文件路径
    all_csv_files = [
        os.path.join(root, file)
        for root, dirs, files in os.walk(directory)
        for file in files
        if file.lower().endswith(".csv")
    ]
    total_files = len(all_csv_files)

    for idx, file_path in enumerate(all_csv_files, start=1):
        file_name = os.path.basename(file_path)
        remaining = total_files - idx
        percent = idx / total_files * 100
        print(f"[{percent:.2f}%] 正在处理: {file_name}，剩余文件: {remaining}")

        line_count = 0
        success = False
        for enc in ENCODINGS:
            try:
                # 分块读取 CSV
                for chunk in pd.read_csv(file_path, chunksize=CHUNK_SIZE, dtype=str, encoding=enc):
                    if 'data_id' in chunk.columns:
                        # 统计 data_id 列不为空的行
                        line_count += chunk['data_id'].notna().sum()
                success = True
                break
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"读取错误: {file_name}, {e}")
                break
        if success:
            results.append((file_name, line_count))
        else:
            results.append((file_name, "编码或读取错误"))

    return results

if __name__ == "__main__":
    data = count_data_id_nonempty(TARGET_DIR)

    # 保存结果到 CSV
    df = pd.DataFrame(data, columns=["文件名", "data_id非空行数"])
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"统计完成，结果已保存到: {OUTPUT_FILE}")
