# 正解率と反応時間における刺激数での有意差を検証するコード

import pandas as pd
import numpy as np
from scipy.stats import f_oneway

# ファイルリスト
file_list = [f"./csv/main/answers_subject{i}.csv" for i in range(1, 8)]

# データを格納するリスト
response_time_data = {6: [], 8: []}
accuracy_data = {6: [], 8: []}

# データ処理
for i, file_path in enumerate(file_list):
    try:
        # データの読み込み
        df = pd.read_csv(file_path)

        # 必要な列の整備
        df["correct"] = pd.to_numeric(df["correct"], errors="coerce")
        df["responseTime"] = pd.to_numeric(df["responseTime"], errors="coerce")
        df["targetAmount"] = pd.to_numeric(df["targetAmount"], errors="coerce")  # 数値型に変換

        # 刺激数6と8のデータを集計
        for target_amount in [6, 8]:
            filtered_df = df[df["targetAmount"] == target_amount]

            # 反応時間データを追加
            response_time_data[target_amount].extend(filtered_df["responseTime"].dropna().tolist())

            # 正解率データを追加
            accuracy_data[target_amount].extend(filtered_df["correct"].dropna().tolist())

    except FileNotFoundError:
        print(f"ファイルが見つかりません: {file_path}")
    except Exception as e:
        print(f"エラーが発生しました（被験者_{i + 1}）: {e}")

# ANOVAを実施
print("\n刺激数での有意差の検証結果:")

# 反応時間のANOVA
if len(response_time_data[6]) > 0 and len(response_time_data[8]) > 0:
    response_time_anova_result = f_oneway(response_time_data[6], response_time_data[8])
    print("反応時間のANOVA結果:")
    print(f"  F値 = {response_time_anova_result.statistic:.2f}")
    print(f"  p値 = {response_time_anova_result.pvalue:.4e}")
    if response_time_anova_result.pvalue < 0.05:
        print("  → 刺激数間で反応時間に有意な差が認められました。")
    else:
        print("  → 刺激数間で反応時間に有意な差は認められませんでした。")
else:
    print("反応時間データが不足しています。")

# 正解率のANOVA
if len(accuracy_data[6]) > 0 and len(accuracy_data[8]) > 0:
    accuracy_anova_result = f_oneway(accuracy_data[6], accuracy_data[8])
    print("\n正解率のANOVA結果:")
    print(f"  F値 = {accuracy_anova_result.statistic:.2f}")
    print(f"  p値 = {accuracy_anova_result.pvalue:.4e}")
    if accuracy_anova_result.pvalue < 0.05:
        print("  → 刺激数間で正解率に有意な差が認められました。")
    else:
        print("  → 刺激数間で正解率に有意な差は認められませんでした。")
else:
    print("正解率データが不足しています。")
