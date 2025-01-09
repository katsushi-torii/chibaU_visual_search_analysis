import pandas as pd
import matplotlib.pyplot as plt

# ファイルパス
reaction_time_6_path = "./csv/cleaned/reaction_times_6.csv"
reaction_time_8_path = "./csv/cleaned/reaction_times_8.csv"
exp1_path = "./csv/cleaned/exp1.csv"

# データの読み込み
reaction_time_6 = pd.read_csv(reaction_time_6_path)
reaction_time_8 = pd.read_csv(reaction_time_8_path)
exp1 = pd.read_csv(exp1_path)

# 必要な列の整備
reaction_time_6 = reaction_time_6.set_index("色名")
reaction_time_8 = reaction_time_8.set_index("色名")
exp1 = exp1.set_index("color")

# 被験者ごとの列名マッピング
subject_map = {
    "sub1": "被験者_1_mean",
    "sub2": "被験者_2_mean",
    "sub3": "被験者_3_mean",
    "sub4": "被験者_4_mean",
    "sub5": "被験者_5_mean",
    "sub6": "被験者_6_mean",
    "sub7": "被験者_7_mean"
}

# 被験者ごとの相関係数を計算
def calculate_correlations(reaction_time, exp1, subject_map):
    correlations = {}
    for subject, reaction_column in subject_map.items():
        if subject in exp1.columns and reaction_column in reaction_time.columns:
            correlation = exp1[subject].corr(reaction_time[reaction_column])
            correlations[subject] = round(correlation, 2)
    return correlations

# 刺激数6と8の相関係数を計算
correlations_6 = calculate_correlations(reaction_time_6, exp1, subject_map)
correlations_8 = calculate_correlations(reaction_time_8, exp1, subject_map)

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

# カラーマップ
color_map = {
    "red": (227/255, 0/255, 38/255),
    "red-purple": (222/255, 0/255, 100/255),
    "pink": (208/255, 0/255, 159/255),
    "purple": (182/255, 0/255, 229/255),
    "purple-blue": (137/255, 63/255, 254/255),
    "blue": (0/255, 119/255, 165/255),
    "blue-green": (0/255, 127/255, 106/255),
    "green": (0/255, 129/255, 63/255),
    "yellow-green": (91/255, 123/255, 0/255),
    "yellow": (133/255, 111/255, 0/255),
    "yellow-red": (201/255, 68/255, 0/255),
    "gray": (120/255, 109/255, 113/255)
}

# 被験者ごとの色ごとの値をプロット
def plot_subject_data(reaction_time, exp1, subject_map, title):
    plt.figure(figsize=(12, 8))
    for subject, reaction_column in subject_map.items():
        if subject in exp1.columns and reaction_column in reaction_time.columns:
            merged_data = pd.merge(exp1[[subject]], reaction_time[[reaction_column]], left_index=True, right_index=True)
            for color_name, row in merged_data.iterrows():
                plt.scatter(
                    row[subject], 
                    row[reaction_column], 
                    color=color_map.get(color_name, "black"), 
                    label=color_name
                )
    plt.xlabel("進出度", fontsize=14)
    plt.ylabel("反応時間", fontsize=14)
    plt.title(title, fontsize=16)
    plt.grid()
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
    plt.tight_layout()
    plt.show()

# 刺激数6のプロット
plot_subject_data(reaction_time_6, exp1, subject_map, "刺激数6の被験者ごとの色ごとの値")

# 刺激数8のプロット
plot_subject_data(reaction_time_8, exp1, subject_map, "刺激数8の被験者ごとの色ごとの値")
