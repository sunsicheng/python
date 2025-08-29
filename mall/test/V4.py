#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import pandas as pd
import logging
from datetime import datetime

# ========= 日志配置 =========
LOG_FILE = r"D:\tmp\cc\v2\running.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__).info

# ========= 基础映射表 =========
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
    "所有期累计已还资金方金额和资金方总额差额之和":"total_amount_diff"
}

# ========= 组字段定义 =========
GROUP_FIELDS = [
    "current_period",
    "repay_date",
    "fund_interest",
    "fund_principal",
    "fund_total",
    "cumulative_repaid",
    "period_diff",
    "guarantee_fee",
    "calculated_guarantee_fee"
]
MAX_PERIOD = 24

#针对有列名为空的那个文件单独处理
# TARGET_LIST  = r"D:\\tmp\\cc\\v4\\unnamed\\error_target_files.txt"        # Excel 文件列表，每行一个路径
# OUTPUT_DIR   = r"D:\\tmp\\cc\\v4\\bak_csv" # 输出目录

# ========= 配置文件路径 =========
TARGET_LIST  = r"D:\\tmp\\cc\\v4\\target_files.txt"        # Excel 文件列表，每行一个路径
OUTPUT_DIR   = r"D:\\tmp\\cc\\v4\\bak_csv" # 输出目录

SORT_FILE    = r"D:\\tmp\\cc\\v4\\sort.txt"        # 列顺序文件

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ========= 加载 sort.txt =========
def load_sort_order():
    if not os.path.exists(SORT_FILE):
        return []
    with open(SORT_FILE, "r", encoding="utf-8-sig") as f:
        return [line.strip() for line in f if line.strip()]

SORT_ORDER = load_sort_order()

# ========= 列名翻译函数 =========
def translate_headers(df: pd.DataFrame):
    cols = list(df.columns)

    def base_name(c: str) -> str:
        return re.sub(r"\.\d+$", "", str(c)).strip()

    def map_in_group(zh: str, n: int):
        if zh == "当前期数": return f"current_period_{n}"
        if zh == "还款日期": return f"repay_date_{n}"
        if zh == "资金方利息": return f"fund_interest_{n}"
        if zh == "资金方本金": return f"fund_principal_{n}"
        if zh == "资金方总额": return f"fund_total_{n}"
        if zh == "累计已还资金方金额": return f"cumulative_repaid_{n}"
        if zh.startswith("第") and "累计已还资金方金额和资金方总额差额" in zh: return f"period_diff_{n}"
        if zh.startswith("担保费") and not zh.startswith("测算担保费"): return f"guarantee_fee_{n}"
        if zh.startswith("测算担保费"): return f"calculated_guarantee_fee_{n}"  # 自动扩展期次
        return None

    new_columns = cols[:]
    handled = set()

    # 1) 处理基础字段
    for i, c in enumerate(cols):
        b = base_name(c)
        if b in BASE_MAPPING:
            new_columns[i] = BASE_MAPPING[b]
            handled.add(i)

    # 2) 找出每组起点
    starts = [i for i, c in enumerate(cols) if base_name(c) == "当前期数"]
    starts.append(len(cols))

    last_n = 0
    for si in range(len(starts)-1):
        g_start, g_end = starts[si], starts[si+1]
        group_idx = list(range(g_start, g_end))

        n = None
        for j in group_idx:
            bj = base_name(cols[j])
            m = re.match(r"^第(\d+)期累计已还资金方金额和资金方总额差额$", bj)
            if m:
                n = int(m.group(1))
                break
        if not n:
            n = last_n + 1
            log(f"⚠️ 组[{g_start}:{g_end}) 未找到锚点列，顺势使用期次 {n}")
        last_n = n

        for j in group_idx:
            if j in handled:
                continue
            bj = base_name(cols[j])
            en = map_in_group(bj, n)
            if en:
                new_columns[j] = en
                handled.add(j)

    # 3) 散落的锚点列直接映射
    for i, c in enumerate(cols):
        if i in handled:
            continue
        b = base_name(c)
        m = re.match(r"^第(\d+)期累计已还资金方金额和资金方总额差额$", b)
        if m:
            n = m.group(1)
            new_columns[i] = f"period_diff_{n}"
            handled.add(i)

    # 映射列名
    df.columns = new_columns

    # 4) 补齐所有组字段到 24期（若原表少于24）
    for n in range(1, MAX_PERIOD+1):
        for f in GROUP_FIELDS:
            col_name = f"{f}_{n}"
            if col_name not in df.columns:
                df[col_name] = None

    return df

# ========= 处理单文件 =========
def process_file(file_path):
    try:
        log(f"开始处理: {file_path}")
        df = pd.read_excel(file_path, dtype=str, engine="openpyxl")
        df = translate_headers(df)

        # 添加 source 列
        df["source"] = os.path.basename(file_path)

        # 补齐 sort.txt 缺失列
        if SORT_ORDER:
            ordered = [c for c in SORT_ORDER if c in df.columns]

            if "source" not in ordered:
                ordered.append("source")  # 只在缺失时补上
            others = [c for c in df.columns if c not in ordered]
            df = df[ordered + others]

        # 输出 CSV
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        csv_path = os.path.join(OUTPUT_DIR, f"{base_name}.csv")
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        log(f"✅ 已保存 CSV: {csv_path}")

    except Exception as e:
        log(f"❌ 处理失败: {file_path}, 错误: {e}")

# ========= 主入口 =========
if __name__ == "__main__":
    if not os.path.exists(TARGET_LIST):
        log(f"未找到目标列表文件: {TARGET_LIST}")
    else:
        with open(TARGET_LIST, "r", encoding="utf-8") as f:
            files = [line.strip() for line in f if line.strip() and os.path.exists(line.strip())]
        total = len(files)
        log(f"📌 待处理文件数: {total}")
        for idx, file_path in enumerate(files, 1):
            log(f"[{idx}/{total}] 正在处理 {file_path}")
            process_file(file_path)
        log(f"任务完成: {datetime.now():%Y-%m-%d %H:%M:%S}")
