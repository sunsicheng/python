#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import pandas as pd
from datetime import datetime
import time

# ========== 配置 =========
TARGET_LIST  = r"D:\tmp\cc\v2\target_files.txt"
CSV_DIR      = r"D:\tmp\cc\v2\bak_csv"
LOG_FILE     = r"D:\tmp\cc\v2\compare_log.txt"
# ==========================

BASE_MAPPING = {
    "数据id": "data_id",
    "资金方贷款结果": "fund_loan_result",
    "年利率": "annual_rate",
    "放款日期": "loan_date",
    "贷款ID": "loan_id",
    "贷款额度": "loan_amount",
    "贷款期数": "loan_periods",
    "放款时间": "loan_time",
    "月利率": "monthly_rate",
    "还款方式": "repay_method",
    "步骤状态": "step_status",
    "状态": "status",
    "应收担保费": "receivable_guarantee_fee",
    "所有期累计已还资金方金额和资金方总额差额之和": "total_amount_diff",
}

def log(msg: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}\n")
    print(msg)

def translate_headers(df: pd.DataFrame):
    cols = list(df.columns)
    def base_name(c: str) -> str:
        return re.sub(r"\.\d+$", "", str(c)).strip()
    def map_in_group(zh: str, n: str):
        if zh == "当前期数": return f"current_period_{n}"
        if zh == "还款日期": return f"repay_date_{n}"
        if zh == "资金方利息": return f"fund_interest_{n}"
        if zh == "资金方本金": return f"fund_principal_{n}"
        if zh == "资金方总额": return f"fund_total_{n}"
        if zh == "累计已还资金方金额": return f"cumulative_repaid_{n}"
        if zh.startswith("第") and "累计已还资金方金额和资金方总额差额" in zh: return f"period_diff_{n}"
        if zh.startswith("担保费"): return f"guarantee_fee_{n}"
        if zh.startswith("测算担保费"): return f"calculated_guarantee_fee_{n}"
        return None

    new_columns = cols[:]
    handled = set()

    for i, c in enumerate(cols):
        b = base_name(c)
        if b in BASE_MAPPING:
            new_columns[i] = BASE_MAPPING[b]
            handled.add(i)

    starts = [i for i, c in enumerate(cols) if base_name(c) == "当前期数"]
    starts.append(len(cols))

    for si in range(len(starts) - 1):
        g_start, g_end = starts[si], starts[si + 1]
        group_idx = list(range(g_start, g_end))
        n = None
        for j in group_idx:
            bj = base_name(cols[j])
            m = re.match(r"^第(\d+)期累计已还资金方金额和资金方总额差额$", bj)
            if m:
                n = m.group(1)
                break
        if not n:
            sample = [base_name(cols[k]) for k in group_idx[:8]]
            log(f"⚠️ 组[{g_start}:{g_end}) 未找到锚点列，原表头保留。样本: {sample}")
            continue
        for j in group_idx:
            if j in handled:
                continue
            bj = base_name(cols[j])
            en = map_in_group(bj, n)
            if en:
                new_columns[j] = en
                handled.add(j)

    for i, c in enumerate(cols):
        if i in handled:
            continue
        b = base_name(c)
        m = re.match(r"^第(\d+)期累计已还资金方金额和资金方总额差额$", b)
        if m:
            n = m.group(1)
            new_columns[i] = f"period_diff_{n}"
            handled.add(i)

    df.columns = new_columns
    return df

def compare_df(df_xlsx: pd.DataFrame, df_csv: pd.DataFrame, source_name: str):
    """
    返回本文件的差异统计
    比较所有公共列和所有行，记录差异日志
    """
    common_cols = [c for c in df_xlsx.columns if c in df_csv.columns]
    diff_count = 0

    if not common_cols:
        log(f"⚠️ {source_name} 没有公共列可比对")
        return diff_count

    min_rows = min(len(df_xlsx), len(df_csv))

    for i in range(min_rows):
        row_x = df_xlsx.iloc[i]
        row_c = df_csv.iloc[i]
        for col in common_cols:
            val_x = row_x[col]
            val_c = row_c[col]

            if pd.isna(val_x) and pd.isna(val_c):
                continue
            if str(val_x) != str(val_c):
                diff_count += 1
                msg = f"❌ {source_name} 行{i+1} 列[{col}] 不一致: Excel='{val_x}' vs CSV='{val_c}'"
                log(msg)

    return diff_count


def main():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"比对任务开始时间: {datetime.now():%Y-%m-%d %H:%M:%S}\n")

    print("=== 比对任务开始 ===")
    start_time = time.time()

    if not os.path.exists(TARGET_LIST):
        log(f"未找到目标列表文件：{TARGET_LIST}")
        return

    with open(TARGET_LIST, "r", encoding="utf-8") as f:
        files = [line.strip() for line in f if line.strip() and os.path.exists(line.strip())]

    total = len(files)
    print(f"待比对文件数: {total}")

    total_diffs = 0
    for idx, xlsx_file in enumerate(files, 1):
        print(f"[{idx}/{total}] 开始比对 {xlsx_file}")

        try:
            df_xlsx = pd.read_excel(xlsx_file, dtype=str, engine="openpyxl")
            df_xlsx = translate_headers(df_xlsx)
        except Exception as e:
            log(f"❌ 读取或转换 Excel 失败: {xlsx_file}, 错误: {e}")
            continue

        csv_file = os.path.join(CSV_DIR, os.path.splitext(os.path.basename(xlsx_file))[0] + ".csv")
        if not os.path.exists(csv_file):
            log(f"⚠️ 未找到对应 CSV 文件: {csv_file}")
            continue

        try:
            df_csv = pd.read_csv(csv_file, dtype=str, encoding="utf-8-sig")
        except Exception as e:
            log(f"❌ 读取 CSV 失败: {csv_file}, 错误: {e}")
            continue

        diff_count = compare_df(df_xlsx, df_csv, os.path.basename(xlsx_file))
        total_diffs += diff_count
        print(f"[{idx}/{total}] 完成比对 {xlsx_file}, 差异条目数: {diff_count}")

    elapsed = time.time() - start_time
    print("=== 比对任务结束 ===")
    print(f"总差异条目数: {total_diffs}")
    print(f"比对耗时: {elapsed:.2f} 秒")
    log(f"比对任务结束时间: {datetime.now():%Y-%m-%d %H:%M:%S}, 总差异条目数: {total_diffs}, 耗时: {elapsed:.2f} 秒")

if __name__ == "__main__":
    main()
