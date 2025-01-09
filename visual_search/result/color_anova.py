# 正解率と反応時間において、色間で有意差があるか、全体で調べる。一元配置分散分析を使用

import pandas as pd
import numpy as np
from scipy.stats import f_oneway

# ファイルリスト
file_list = [f"./csv/main/answers_subject{i}.csv" for i in range(1, 8)]

# 色順
color_order = [
    "red", "red-purple", "pink", "purple", "purple-blue", "blue",
    "blue-green", "green", "yellow-green", "yellow", "yellow-red", "gray"
]

# 刺激数6と8のデータを格納する辞書
overall_results = {6: {color: [] for color in color_order},
                   8: {color: [] for color in color_order}}
response_time_results = {6: {color: [] for color in color_order},
                         8: {color: [] for color in color_order}}

# データ処理
for i, file_path in enumerate(file_list):
    try:
        # データの読み込み
        df = pd.read_csv(file_path)

        # 必要な列の整備
        df["correct"] = pd.to_numeric(df["correct"], errors="coerce")
        df["responseTime"] = pd.to_numeric(df["responseTime"], errors="coerce")
        df["targetAmount"] = pd.to_numeric(df["targetAmount"], errors="coerce")  # 数値型に変換

        # 刺激数6と8のデータを色ごとに集計
        for target_amount in [6, 8]:
            filtered_df = df[df["targetAmount"] == target_amount]

            for color, correct_values in filtered_df.groupby("answer")["correct"]:
                if color in color_order:
                    overall_results[target_amount][color].extend(correct_values.dropna().tolist())  # 欠損値を除去して追加

            for color, response_times in filtered_df.groupby("answer")["responseTime"]:
                if color in color_order:
                    response_time_results[target_amount][color].extend(response_times.dropna().tolist())  # 欠損値を除去して追加

    except FileNotFoundError:
        print(f"ファイルが見つかりません: {file_path}")
    except Exception as e:
        print(f"エラーが発生しました（被験者_{i + 1}）: {e}")

# ANOVAを刺激数6と8に分けて実施
for target_amount in [6, 8]:
    print(f"\n刺激数 {target_amount} の分析結果:")

    # 正解率のANOVA
    correct_data_by_color = [overall_results[target_amount][color] for color in color_order if len(overall_results[target_amount][color]) > 0]
    if len(correct_data_by_color) > 1:
        correct_anova_result = f_oneway(*correct_data_by_color)
        print(f"  正解率のANOVA結果:")
        print(f"    F値 = {correct_anova_result.statistic:.2f}")
        print(f"    p値 = {correct_anova_result.pvalue:.4e}")
        if correct_anova_result.pvalue < 0.05:
            print(f"    → 色間に有意な差が認められました。")
        else:
            print(f"    → 色間に有意な差は認められませんでした。")
    else:
        print(f"  正解率の比較可能なデータが不足しています。")

    # 反応時間のANOVA
    response_time_data_by_color = [response_time_results[target_amount][color] for color in color_order if len(response_time_results[target_amount][color]) > 0]
    if len(response_time_data_by_color) > 1:
        response_time_anova_result = f_oneway(*response_time_data_by_color)
        print(f"  反応時間のANOVA結果:")
        print(f"    F値 = {response_time_anova_result.statistic:.2f}")
        print(f"    p値 = {response_time_anova_result.pvalue:.4e}")
        if response_time_anova_result.pvalue < 0.05:
            print(f"    → 色間に有意な差が認められました。")
        else:
            print(f"    → 色間に有意な差は認められませんでした。")
    else:
        print(f"  反応時間の比較可能なデータが不足しています。")

for target_amount in [6, 8]:
    total_data_points_correct = sum(len(overall_results[target_amount][color]) for color in color_order)
    total_data_points_response_time = sum(len(response_time_results[target_amount][color]) for color in color_order)
    print(f"刺激数 {target_amount} の正解率データ点数: {total_data_points_correct}")
    print(f"刺激数 {target_amount} の反応時間データ点数: {total_data_points_response_time}")
