import pandas as pd
import scipy.stats as stats
import os

# 被験者リスト
subjects = ["subject1", "subject2", "subject3", "subject4", "subject5", "subject6"]
base_path = "./csv/same/"

# 結果を保存する辞書
results = {}

# 被験者ごとの処理
for subject in subjects:
    # データを読み込み
    file_path = os.path.join(base_path, f"answerssame_{subject}.csv")
    df = pd.read_csv(file_path)

    # -1 のデータを除外
    filtered_df = df[df["answerId"] != -1]

    # 結果を格納する辞書
    subject_results = {}

    # 色ごとの反応時間の比較（ANOVA）
    grouped_by_color = filtered_df.groupby("answer")["responseTime"].apply(list)
    if len(grouped_by_color) > 1:  # 比較可能なグループが2つ以上の場合のみ実行
        f_stat_color, p_value_color = stats.f_oneway(*grouped_by_color)
        subject_results["color_effect"] = {
            "F_stat": f_stat_color,
            "p_value": p_value_color,
            "significant": p_value_color < 0.05
        }
    else:
        subject_results["color_effect"] = "Insufficient groups for ANOVA"

    # 回答位置ごとの反応時間の比較（ANOVA）
    grouped_by_answerId = filtered_df.groupby("answerId")["responseTime"].apply(list)
    if len(grouped_by_answerId) > 1:  # 比較可能なグループが2つ以上の場合のみ実行
        f_stat_answerId, p_value_answerId = stats.f_oneway(*grouped_by_answerId)
        subject_results["answerId_effect"] = {
            "F_stat": f_stat_answerId,
            "p_value": p_value_answerId,
            "significant": p_value_answerId < 0.05
        }
    else:
        subject_results["answerId_effect"] = "Insufficient groups for ANOVA"

    # 結果を保存
    results[subject] = subject_results

# 結果の表示
for subject, result in results.items():
    print(f"Results for {subject}:")
    print(result)
