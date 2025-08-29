#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import pandas as pd
import logging

"""
因发现有部分组锚点不全，导致空列，故临时新增此程序，但是也引入了新问题，BASE_MAPPING 字段列名ChatGPT自己新取了，导致用此程序跑的数据列错位（未识别的列加到了source后面）
同时也漏掉了缺失字段补齐
"""
# ========= 日志配置 =========
LOG_FILE = r"D:\\tmp\\cc\\v2\\running.log"

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
    "年利率": "annual_interest_rate",
    "放款日期": "loan_date",
    "贷款ID": "loan_id",
    "贷款额度": "loan_amount",
    "贷款期数": "loan_term",
    "放款时间": "loan_time",
    "月利率": "monthly_interest_rate",
    "还款方式": "repayment_method",
    "步骤状态": "step_status",
    "状态": "status",
    "应收担保费": "receivable_guarantee_fee",
}

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
        if zh.startswith("第") and "累计已还资金方金额和资金方总额差额" in zh:
            return f"period_diff_{n}"
        if zh.startswith("担保费"): return f"guarantee_fee_{n}"
        if zh.startswith("测算担保费"): return f"calculated_guarantee_fee_{n}"
        return None

    new_columns = cols[:]
    handled = set()

    # 1) 先处理基础字段
    for i, c in enumerate(cols):
        b = base_name(c)
        if b in BASE_MAPPING:
            new_columns[i] = BASE_MAPPING[b]
            handled.add(i)

    # 2) 找出每组的起点
    starts = [i for i, c in enumerate(cols) if base_name(c) == "当前期数"]
    starts.append(len(cols))

    last_n = 0  # 上一个期次号
    # 3) 逐组处理
    for si in range(len(starts) - 1):
        g_start, g_end = starts[si], starts[si + 1]
        group_idx = list(range(g_start, g_end))

        # 找锚点
        n = None
        for j in group_idx:
            bj = base_name(cols[j])
            m = re.match(r"^第(\d+)期累计已还资金方金额和资金方总额差额$", bj)
            if m:
                n = int(m.group(1))
                break

        if not n:
            # 没有锚点 -> 顺势递增
            n = last_n + 1
            log(f"⚠️ 组[{g_start}:{g_end}) 未找到锚点列，顺势使用期次 {n}")

        last_n = n

        # 映射组
        for j in group_idx:
            if j in handled:
                continue
            bj = base_name(cols[j])
            en = map_in_group(bj, n)
            if en:
                new_columns[j] = en
                handled.add(j)

    df.columns = new_columns
    return df

# ========= 文件读取 =========
def read_file_to_list(filename):
    with open(filename, "r", encoding="utf-8") as f:
        files = [line.strip() for line in f if line.strip() and os.path.exists(line.strip())]
        for elem in files:
            log(f"找到文件: {elem}")
    return files

# ========= 主入口 =========
if __name__ == "__main__":
    ## 修复未找到锚点的数据，大概90个
    # list_file = r"D:\\tmp\\cc\\v2\\target_fix_bug.txt"
    # output_dir = r"D:\\tmp\\cc\\v2\\bak_csv_fix_bug"

    ## 修复一个担保费列名楼下
    list_file = r"D:\\tmp\\cc\\v2\\unnamed\\error_target_files.txt"
    output_dir = r"D:\\tmp\\cc\\v2\\bak_csv_fix_bug"
    os.makedirs(output_dir, exist_ok=True)

    files = read_file_to_list(list_file)
    for file in files:
        try:
            log(f"开始处理: {file}")
            df = pd.read_excel(file, dtype=str,engine="openpyxl")
            df = translate_headers(df)

            # 输出到 bak_csv_fix_bug
            base_name = os.path.splitext(os.path.basename(file))[0]
            csv_path = os.path.join(output_dir, f"{base_name}.csv")

            df.to_csv(csv_path, index=False, encoding="utf-8-sig")
            log(f"✅ 已保存 CSV: {csv_path}")

        except Exception as e:
            log(f"❌ 处理失败: {file}, 错误: {e}")
