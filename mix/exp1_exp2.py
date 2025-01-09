#進出度と正解率・反応時間をピアソン相関係数で出力（被験者ごとと全体で）

import pandas as pd
from scipy.stats import pearsonr

# データ読み込み
response_time = pd.read_csv("./csv/cleaned/responseTime.csv")
expansion = pd.read_csv("./csv/cleaned/exp1.csv")
correct_rate = pd.read_csv("./csv/cleaned/correctRate.csv")

# 色名を日本語のまま扱う
response_time.rename(columns={response_time.columns[0]: "色名"}, inplace=True)
expansion.rename(columns={expansion.columns[0]: "色名"}, inplace=True)
correct_rate.rename(columns={correct_rate.columns[0]: "色名"}, inplace=True)

# データを色名でマージ
merged = pd.merge(expansion, response_time, on="色名")
merged = pd.merge(merged, correct_rate, on="色名", suffixes=("_exp", "_correct"))

# 被験者ごとに進出度と正解率、進出度と反応時間の相関を計算
subjects = [col for col in expansion.columns if col.startswith("sub")]
subjects.append("total")  # 全体列を追加
correlations_exp_correct = {}
correlations_exp_response = {}

for subject in subjects:
    expansion_values = merged[f"{subject}_exp"]
    correct_rate_values = merged[f"{subject}_correct"]
    response_time_values = merged[f"{subject}_avg"]

    # 進出度と正解率の相関
    correlation_correct, _ = pearsonr(expansion_values, correct_rate_values)
    correlations_exp_correct[subject] = correlation_correct

    # 進出度と反応時間の相関
    correlation_response, _ = pearsonr(expansion_values, response_time_values)
    correlations_exp_response[subject] = correlation_response

# 結果をデータフレームに変換
correlations_exp_correct_df = pd.DataFrame.from_dict(correlations_exp_correct, orient='index', columns=['進出度と正解率のピアソン相関'])
correlations_exp_response_df = pd.DataFrame.from_dict(correlations_exp_response, orient='index', columns=['進出度と反応時間のピアソン相関'])

# # 結果を表示
# print("進出度と正解率のピアソン相関:")
# print(correlations_exp_correct_df)

# print("\n進出度と反応時間のピアソン相関:")
# print(correlations_exp_response_df)

import pandas as pd
from scipy.stats import pearsonr

# データ読み込み
response_time = pd.read_csv("./csv/cleaned/responseTime.csv")
expansion = pd.read_csv("./csv/cleaned/exp1.csv")
correct_rate = pd.read_csv("./csv/cleaned/correctRate.csv")

# 色名を日本語のまま扱う
response_time.rename(columns={response_time.columns[0]: "色名"}, inplace=True)
expansion.rename(columns={expansion.columns[0]: "色名"}, inplace=True)
correct_rate.rename(columns={correct_rate.columns[0]: "色名"}, inplace=True)

# データを色名でマージ
merged = pd.merge(expansion, response_time, on="色名")
merged = pd.merge(merged, correct_rate, on="色名", suffixes=("_exp", "_correct"))

# 不備の可能性を再確認
# 1. 各列の値を個別に比較（視覚的確認用）
print("[進出度データ]")
print(expansion)
print("\n[反応時間データ]")
print(response_time)
print("\n[正解率データ]")
print(correct_rate)

# 2. 欠損値の再確認
print("\n[欠損値の再確認]")
print(merged.isnull().sum())

# 3. 色名の再確認
print("\n[色名の確認]")
print("進出度データの色名:", expansion["色名"].tolist())
print("反応時間データの色名:", response_time["色名"].tolist())
print("正解率データの色名:", correct_rate["色名"].tolist())

# 4. マージ後のデータ内容確認
print("\n[マージ後のデータ内容確認]")
print(merged.head())

# 5. 各被験者のデータが対応しているか詳細チェック
subjects = [col for col in expansion.columns if col.startswith("sub")]
subjects.append("total")
for subject in subjects:
    print(f"\n[被験者 {subject} のデータ詳細確認]")
    print("進出度:", merged[f"{subject}_exp"].tolist())
    print("正解率:", merged[f"{subject}_correct"].tolist())
    print("反応時間:", merged[f"{subject}_avg"].tolist())

# 6. サンプル計算の詳細確認
print("\n[サンプル相関計算詳細確認: sub1]")
expansion_values = merged["sub1_exp"]
correct_rate_values = merged["sub1_correct"]
response_time_values = merged["sub1_avg"]
print("進出度:", expansion_values.tolist())
print("正解率:", correct_rate_values.tolist())
print("反応時間:", response_time_values.tolist())

correlation_correct, _ = pearsonr(expansion_values, correct_rate_values)
correlation_response, _ = pearsonr(expansion_values, response_time_values)
print(f"進出度と正解率の相関 (sub1): {correlation_correct}")
print(f"進出度と反応時間の相関 (sub1): {correlation_response}")
