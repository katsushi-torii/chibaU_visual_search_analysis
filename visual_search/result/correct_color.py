#各色の正解率と試行数

import pandas as pd

# 被験者データのCSVファイルパスリスト
file_list = [f"./csv/main/answers_subject{i}.csv" for i in range(1, 8)]

# 指定された色の順番
color_order = [
    "red", "red-purple", "pink", "purple", "purple-blue",
    "blue", "blue-green", "green", "yellow-green",
    "yellow", "yellow-red", "gray"
]

# 被験者ごとの結果を格納するリスト
subject_results = []

# 各被験者のデータを処理
for i, file in enumerate(file_list, start=1):
    # データを読み込む
    df = pd.read_csv(file)
    df["correct"] = df["correct"].astype(int)
    
    # 色ごとの正解数と出現回数を集計
    color_summary = df.groupby("answer").agg(
        total_correct=("correct", "sum"),
        total_presented=("answer", "count")
    ).reset_index()
    
    # 正解率を計算
    color_summary["correct_rate"] = color_summary["total_correct"] / color_summary["total_presented"]
    color_summary["subject"] = f"Subject_{i}"  # 被験者IDを追加
    
    # 結果を格納
    subject_results.append(color_summary)

# 全被験者の結果を統合
all_subjects_summary = pd.concat(subject_results, ignore_index=True)

# 全体の正解率と試行数を計算
overall_summary = all_subjects_summary.groupby("answer").agg(
    total_correct=("total_correct", "sum"),
    total_presented=("total_presented", "sum")
).reset_index()
overall_summary["correct_rate"] = overall_summary["total_correct"] / overall_summary["total_presented"]
overall_summary["subject"] = "Overall"

# 全体の結果を被験者ごとの結果に追加
all_subjects_summary = pd.concat([all_subjects_summary, overall_summary], ignore_index=True)

# 正解率のピボットテーブル
correct_rate_table = all_subjects_summary.pivot(index="answer", columns="subject", values="correct_rate")

# 試行数のピボットテーブル
trial_count_table = all_subjects_summary.pivot(index="answer", columns="subject", values="total_presented")

# 指定された色順に並べ替え
correct_rate_table_ordered = correct_rate_table.reindex(color_order)
trial_count_table_ordered = trial_count_table.reindex(color_order)

# 結果を表示
print("正解率の表 (被験者ごと + 全体):")
print(correct_rate_table_ordered)

print("\n試行数の表 (被験者ごと + 全体):")
print(trial_count_table_ordered)

# 最終結果を返す
correct_rate_table_ordered, trial_count_table_ordered
