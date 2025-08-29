#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
监控 bak_csv 目录，一旦有新的 CSV 文件生成，自动与源 Excel 文件比对。
"""

import os
import time
from datetime import datetime
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ========= 配置 =========
mapping_file   = r"D:\tmp\cc\v2\mapping.txt"   # 映射文件
sort_file      = r"D:\tmp\cc\v2\sort.txt"      # 列顺序文件
target_files   = r"D:\tmp\cc\v2\target_files.txt"  # Excel 源文件全路径
bak_csv_dir    = r"D:\tmp\cc\v2\bak_csv"       # 监控目录
result_file    = r"D:\tmp\cc\v2\check_result.txt" # 输出比对结果
# ========= 配置结束 =========

# 加载映射文件
def load_mapping(mapping_file):
    mapping_dict = {}
    with open(mapping_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "=" not in line:
                continue
            cn, en = line.split("=", 1)
            mapping_dict[cn.strip()] = en.strip()
    return mapping_dict

# 加载排序列
def load_sort(sort_file):
    with open(sort_file, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# 列名映射（处理担保费特殊规则）
def map_column(col_name, mapping_dict):
    if col_name.startswith("担保费"):
        if col_name != "担保费" and col_name[3:].isdigit():
            idx = int(col_name[3:])
            return f"guarantee_fee_{idx}"
        if col_name == "担保费":
            return "guarantee_fee_1"
        if col_name.startswith("担保费.") and col_name[4:].isdigit():
            idx = int(col_name[4:]) + 1
            return f"guarantee_fee_{idx}"
    return mapping_dict.get(col_name, col_name)

# 等待文件写入完成
def wait_for_complete(file_path, timeout=10):
    last_size = -1
    for _ in range(timeout * 2):  # 每 0.5 秒检测一次
        if not os.path.exists(file_path):
            time.sleep(0.5)
            continue
        size = os.path.getsize(file_path)
        if size == last_size and size > 0:
            return True
        last_size = size
        time.sleep(0.5)
    return False

# 根据 CSV 文件找到对应的 Excel 文件
def find_excel(csv_file_name, excel_files_dict):
    base_name = os.path.splitext(csv_file_name)[0]
    return excel_files_dict.get(base_name)

# 核心比对逻辑
def compare_files(excel_file, csv_file, mapping_dict, sort_cols):
    start_time = time.time()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_lines = [f"\n[{now_str}] 开始比对 Excel={excel_file}, CSV={csv_file}"]
    try:
        # 读取 Excel 并映射列名
        df_excel = pd.read_excel(excel_file, dtype=str, engine="openpyxl")
        df_excel.rename(columns=lambda x: map_column(str(x), mapping_dict), inplace=True)

        # 读取 CSV 并去掉 source
        df_csv = pd.read_csv(csv_file, dtype=str, encoding="utf-8-sig")
        if "source" in df_csv.columns:
            df_csv = df_csv.drop(columns=["source"])

        # 只保留公共列并排序
        common_cols = [c for c in sort_cols if c in df_excel.columns and c in df_csv.columns]
        df_excel = df_excel[common_cols].reset_index(drop=True)
        df_csv   = df_csv[common_cols].reset_index(drop=True)

        # 行数对比
        if len(df_excel) != len(df_csv):
            log_lines.append(f"⚠️ 行数不一致: Excel={len(df_excel)}, CSV={len(df_csv)}")

        # 内容对比
        if df_excel.equals(df_csv):
            log_lines.append("✅ 两个文件数据完全一致（除列名、顺序、source列）")
        else:
            log_lines.append("⚠️ 数据不一致，差异如下：")
            diff = (df_excel != df_csv) & ~(df_excel.isna() & df_csv.isna())
            rows, cols = diff.to_numpy().nonzero()
            for r, c in zip(rows, cols):
                log_lines.append(f"  行 {r+2}, 列 {df_excel.columns[c]}: Excel='{df_excel.iat[r,c]}', CSV='{df_csv.iat[r,c]}'")
    except Exception as e:
        log_lines.append(f"❌ 处理失败: {e}")

    end_time = time.time()
    duration = round(end_time - start_time, 2)
    log_lines.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 完成比对，耗时 {duration} 秒")
    print("\n".join(log_lines))

    # 写入结果文件
    with open(result_file, "a", encoding="utf-8") as f:
        f.write("\n".join(log_lines) + "\n")

# 事件处理器
class CsvHandler(FileSystemEventHandler):
    def __init__(self, excel_files_dict, mapping_dict, sort_cols):
        super().__init__()
        self.excel_files_dict = excel_files_dict
        self.mapping_dict = mapping_dict
        self.sort_cols = sort_cols

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".csv"):
            csv_name = os.path.basename(event.src_path)
            print(f"\n检测到新 CSV 文件: {csv_name}")
            if wait_for_complete(event.src_path):
                excel_file = find_excel(csv_name, self.excel_files_dict)
                if excel_file:
                    compare_files(excel_file, event.src_path, self.mapping_dict, self.sort_cols)
                else:
                    print(f"⚠️ 未找到对应的 Excel 文件: {csv_name}")
            else:
                print(f"⚠️ 文件未完成写入，跳过比对: {csv_name}")

def main():
    mapping_dict = load_mapping(mapping_file)
    sort_cols = load_sort(sort_file)

    # 读取源 Excel 文件路径
    with open(target_files, "r", encoding="utf-8") as f:
        excel_files_list = [line.strip() for line in f if line.strip()]
    # 生成 dict: key=Excel 文件名（不带扩展），value=Excel 全路径
    excel_files_dict = {os.path.splitext(os.path.basename(f))[0]: f for f in excel_files_list}

    event_handler = CsvHandler(excel_files_dict, mapping_dict, sort_cols)
    observer = Observer()
    observer.schedule(event_handler, path=bak_csv_dir, recursive=False)
    observer.start()
    print(f"📌 开始监控目录: {bak_csv_dir}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
