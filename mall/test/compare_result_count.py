#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
比较结果的数量
    数据集1来自SR表，group by count  统计
    数据集2来自Python程序读取csv文件不为空行数
"""
import pandas as pd
import os
from datetime import datetime

# ========= 配置 =========
EXCEL_FILE = r"D:\tmp\cc\v4\compare\csv_real_count.csv"  # Excel 文件路径
TXT_FILE = r"D:\tmp\cc\v4\compare\re2.txt"  # TXT 文件路径
OUTPUT_FILE = r"D:\tmp\cc\v4\compare\compare_diff.xlsx"  # 输出结果


def validate_files():
    """验证输入文件是否存在"""
    missing_files = []
    if not os.path.exists(EXCEL_FILE):
        missing_files.append(f"Excel文件: {EXCEL_FILE}")
    if not os.path.exists(TXT_FILE):
        missing_files.append(f"TXT文件: {TXT_FILE}")

    if missing_files:
        print("❌ 以下文件不存在:")
        for file in missing_files:
            print(f"   {file}")
        return False
    return True


def read_excel_data():
    """读取Excel/CSV文件"""
    try:
        print(f"📖 正在读取Excel文件: {EXCEL_FILE}")
        df_excel = pd.read_csv(EXCEL_FILE, encoding="utf-8-sig")

        # 自动检测列名或使用前两列
        if len(df_excel.columns) >= 2:
            df_excel = df_excel.iloc[:, [0, 1]]  # 取前两列
            df_excel.columns = ["FileName", "ExcelNumber"]
        else:
            raise ValueError("Excel文件至少需要两列数据")

        # 数据清洗
        df_excel = df_excel.dropna()  # 删除空行
        df_excel["FileName"] = df_excel["FileName"].astype(str).str.strip()
        df_excel["ExcelNumber"] = pd.to_numeric(df_excel["ExcelNumber"], errors='coerce')
        df_excel = df_excel.dropna()  # 删除数量转换失败的行

        print(f"✅ Excel文件读取成功，有效数据: {len(df_excel)} 行")
        return df_excel

    except Exception as e:
        print(f"❌ 读取Excel文件失败: {e}")
        return None


def read_txt_data():
    """读取TXT文件"""
    try:
        print(f"📖 正在读取TXT文件: {TXT_FILE}")
        txt_data = []
        invalid_lines = []

        with open(TXT_FILE, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:  # 跳过空行
                    continue

                if "=" not in line:
                    invalid_lines.append(f"第{line_num}行: {line} (缺少等号)")
                    continue

                try:
                    file, num = line.split("=", 1)
                    file = file.strip()
                    num = num.strip()

                    if not file:
                        invalid_lines.append(f"第{line_num}行: {line} (文件名为空)")
                        continue

                    # 处理数字格式（去掉千分位逗号等）
                    num_val = int(num.replace(",", "").replace(" ", ""))
                    txt_data.append([file, num_val])

                except ValueError as e:
                    invalid_lines.append(f"第{line_num}行: {line} (数字格式错误: {e})")
                except Exception as e:
                    invalid_lines.append(f"第{line_num}行: {line} (解析错误: {e})")

        # 显示无效行信息
        if invalid_lines:
            print(f"⚠️  发现 {len(invalid_lines)} 行格式异常:")
            for invalid in invalid_lines[:5]:  # 只显示前5个错误
                print(f"   {invalid}")
            if len(invalid_lines) > 5:
                print(f"   ... 还有 {len(invalid_lines) - 5} 行错误")

        df_txt = pd.DataFrame(txt_data, columns=["FileName", "TxtNumber"])
        print(f"✅ TXT文件读取成功，有效数据: {len(df_txt)} 行")
        return df_txt

    except Exception as e:
        print(f"❌ 读取TXT文件失败: {e}")
        return None


def analyze_differences(df_merge):
    """分析差异并生成统计信息"""
    print("\n" + "=" * 60)
    print("📊 数据比较分析结果")
    print("=" * 60)

    # 基础统计
    total_files = len(df_merge)
    excel_only = df_merge["TxtNumber"].isna().sum()
    txt_only = df_merge["ExcelNumber"].isna().sum()
    both_exist = total_files - excel_only - txt_only
    equal_count = df_merge["Equal"].sum()
    different_count = both_exist - equal_count

    print(f"📋 总文件数: {total_files}")
    print(f"🟢 数量一致: {equal_count} ({equal_count / total_files * 100:.1f}%)")
    print(f"🔴 数量不一致: {different_count} ({different_count / total_files * 100:.1f}%)")
    print(f"🔵 仅Excel存在: {excel_only} ({excel_only / total_files * 100:.1f}%)")
    print(f"🟡 仅TXT存在: {txt_only} ({txt_only / total_files * 100:.1f}%)")

    # 显示数量不一致的文件
    if different_count > 0:
        print(f"\n🔍 数量不一致的文件 (前10个):")
        print("-" * 60)
        different_files = df_merge[
            (df_merge["ExcelNumber"].notna()) &
            (df_merge["TxtNumber"].notna()) &
            (~df_merge["Equal"])
            ].head(10)

        for _, row in different_files.iterrows():
            diff = int(row["ExcelNumber"] - row["TxtNumber"])
            print(f"📁 {row['FileName']}")
            print(f"   Excel: {int(row['ExcelNumber']):,} | TXT: {int(row['TxtNumber']):,} | 差值: {diff:+,}")

    # 显示仅在一边存在的文件
    if excel_only > 0:
        print(f"\n📊 仅Excel中存在的文件 (前5个):")
        excel_only_files = df_merge[df_merge["TxtNumber"].isna()].head(5)
        for _, row in excel_only_files.iterrows():
            print(f"   📁 {row['FileName']}: {int(row['ExcelNumber']):,}")
        if excel_only > 5:
            print(f"   ... 还有 {excel_only - 5} 个文件")

    if txt_only > 0:
        print(f"\n📄 仅TXT中存在的文件 (前5个):")
        txt_only_files = df_merge[df_merge["ExcelNumber"].isna()].head(5)
        for _, row in txt_only_files.iterrows():
            print(f"   📁 {row['FileName']}: {int(row['TxtNumber']):,}")
        if txt_only > 5:
            print(f"   ... 还有 {txt_only - 5} 个文件")


def save_results(df_merge):
    """保存结果到Excel文件"""
    try:
        print(f"\n💾 正在保存结果到: {OUTPUT_FILE}")

        # 确保输出目录存在
        output_dir = os.path.dirname(OUTPUT_FILE)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 添加差值列
        df_merge["Difference"] = df_merge.apply(
            lambda row: int(row["ExcelNumber"] - row["TxtNumber"])
            if pd.notna(row["ExcelNumber"]) and pd.notna(row["TxtNumber"])
            else None, axis=1
        )

        # 添加状态列
        def get_status(row):
            if pd.isna(row["ExcelNumber"]):
                return "仅TXT存在"
            elif pd.isna(row["TxtNumber"]):
                return "仅Excel存在"
            elif row["Equal"]:
                return "数量一致"
            else:
                return "数量不一致"

        df_merge["Status"] = df_merge.apply(get_status, axis=1)

        # 重新排列列顺序
        column_order = ["FileName", "ExcelNumber", "TxtNumber", "Difference", "Equal", "Status"]
        df_merge = df_merge[column_order]

        # 保存到Excel，包含多个工作表
        with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl') as writer:
            # 全部结果
            df_merge.to_excel(writer, sheet_name='全部比较结果', index=False)

            # 数量不一致
            different = df_merge[df_merge["Status"] == "数量不一致"]
            if not different.empty:
                different.to_excel(writer, sheet_name='数量不一致', index=False)

            # 仅Excel存在
            excel_only = df_merge[df_merge["Status"] == "仅Excel存在"]
            if not excel_only.empty:
                excel_only.to_excel(writer, sheet_name='仅Excel存在', index=False)

            # 仅TXT存在
            txt_only = df_merge[df_merge["Status"] == "仅TXT存在"]
            if not txt_only.empty:
                txt_only.to_excel(writer, sheet_name='仅TXT存在', index=False)

        print(f"✅ 结果保存成功!")
        return True

    except Exception as e:
        print(f"❌ 保存结果失败: {e}")
        return False


def main():
    print("🚀 开始执行文件数量比较程序")
    print(f"⏰ 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 验证文件存在性
    if not validate_files():
        return

    # 读取数据
    df_excel = read_excel_data()
    if df_excel is None:
        return

    df_txt = read_txt_data()
    if df_txt is None:
        return

    # 合并比较
    print(f"\n🔄 正在合并数据进行比较...")
    df_merge = pd.merge(df_excel, df_txt, on="FileName", how="outer")
    df_merge["Equal"] = (
            (df_merge["ExcelNumber"].notna()) &
            (df_merge["TxtNumber"].notna()) &
            (df_merge["ExcelNumber"] == df_merge["TxtNumber"])
    )

    # 分析结果
    analyze_differences(df_merge)

    # 保存结果
    if save_results(df_merge):
        print(f"\n🎉 程序执行完成! 详细结果请查看: {OUTPUT_FILE}")

    # 显示前几行数据预览
    print(f"\n📋 数据预览 (前5行):")
    print("-" * 60)
    preview = df_merge.head()
    for col in ['ExcelNumber', 'TxtNumber']:
        if col in preview.columns:
            preview[col] = preview[col].apply(lambda x: f"{int(x):,}" if pd.notna(x) else "N/A")
    print(preview.to_string(index=False))


if __name__ == "__main__":
    main()