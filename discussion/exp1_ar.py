import pandas as pd

# ファイルパス
accuracy_6_path = "./csv/cleaned/accuracy_rates_6.csv"
accuracy_8_path = "./csv/cleaned/accuracy_rates_8.csv"
exp1_path = "./csv/cleaned/exp1.csv"

# データの読み込み
accuracy_6 = pd.read_csv(accuracy_6_path)
accuracy_8 = pd.read_csv(accuracy_8_path)
exp1 = pd.read_csv(exp1_path)

# 必要な列の整備
accuracy_6 = accuracy_6.set_index("色名")
accuracy_8 = accuracy_8.set_index("色名")
exp1 = exp1.set_index("color")

# 被験者ごとの列名マッピング
subject_map = {
    "被験者_1_accuracy": "sub1",
    "被験者_2_accuracy": "sub2",
    "被験者_3_accuracy": "sub3",
    "被験者_4_accuracy": "sub4",
    "被験者_5_accuracy": "sub5",
    "被験者_6_accuracy": "sub6",
    "被験者_7_accuracy": "sub7"
}

# 被験者ごとの相関係数を計算
def calculate_correlations(accuracy_df, exp1_df, subject_map):
    correlations = {}
    for accuracy_col, exp1_col in subject_map.items():
        if exp1_col in exp1_df.columns and accuracy_col in accuracy_df.columns:
            # 正解率を数値型に変換（パーセントから小数に）
            accuracy_df[accuracy_col] = accuracy_df[accuracy_col].str.rstrip('%').astype(float) / 100.0
            correlation = exp1_df[exp1_col].corr(accuracy_df[accuracy_col])
            correlations[exp1_col] = round(correlation, 2)
    return correlations

# 刺激数6と8の相関係数を計算
correlations_6 = calculate_correlations(accuracy_6, exp1, subject_map)
correlations_8 = calculate_correlations(accuracy_8, exp1, subject_map)

# 結果を表示
def display_results(correlations, label):
    print(f"\n{label} の相関係数")
    if correlations:
        for subject, corr in correlations.items():
            print(f"{subject}: {corr}")
    else:
        print("相関係数を計算できるデータがありません。")

display_results(correlations_6, "刺激数6")
display_results(correlations_8, "刺激数8")
