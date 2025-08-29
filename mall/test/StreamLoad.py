#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import glob
import time

# ========== 配置参数 ==========
fe_host = ""
fe_http_port = ""
username = ""
password = ""
data_dir = ""  # CSV 文件目录
database = ""
table = "financial_regulatory_data"
label_prefix = "1_label_financial_regulatory_data"  # label 前缀，每个文件拼接唯一序号

# ========== 主逻辑 ==========
def stream_load(file_path, label):
    curl_cmd = [
        "curl",
        "--location-trusted",
        "-u", f"{username}:{password}",
        "-H", f"label:{label}",
        "-H", "Expect:100-continue",
        "-H", "column_separator:,",
        "-H", "format:csv",
        "-T", file_path,
        "-XPUT",
        f"http://{fe_host}:{fe_http_port}/api/{database}/{table}/_stream_load"
    ]

    try:
        result = subprocess.run(
            curl_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            encoding="utf-8",
            errors="ignore",
            timeout=120
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)


if __name__ == "__main__":
    files = sorted(glob.glob(os.path.join(data_dir, "*.csv")))
    total = len(files)

    if total == 0:
        print(f"❌ 目录下没有找到 CSV 文件: {data_dir}")
        exit(1)

    print(f"共发现 {total} 个 CSV 文件，开始导入...")

    for idx, file_path in enumerate(files, start=1):
        label = f"{label_prefix}_{idx:03d}"  # 确保每个 label 唯一
        remaining = total - idx
        print(f"\n▶️ 正在处理文件 [{idx}/{total}] : {os.path.basename(file_path)} (剩余 {remaining} 个)")

        code, out, err = stream_load(file_path, label)

        print(f"Exit Code: {code}")
        if out.strip():
            print(f"Output: {out.strip()}")
        if err.strip():
            print(f"Error: {err.strip()}")

        # 每次执行完停 1 秒
        time.sleep(5)

    print("\n✅ 全部文件已处理完成！")