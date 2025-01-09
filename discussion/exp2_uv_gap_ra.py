import pandas as pd
from scipy.stats import linregress
import numpy as np

# CSVファイルのパスを指定
file_reaction_6 = './csv/cleaned/reaction_times_total_6.csv'
file_reaction_8 = './csv/cleaned/reaction_times_total_8.csv'
file_accuracy_6 = './csv/cleaned/accuracy_total_6.csv'
file_accuracy_8 = './csv/cleaned/accuracy_total_8.csv'
file_uv = './csv/colors/mean_std.csv'

# 色の順番（隣接ペアを決定）
color_order = [
    "red", "red-purple", "pink", "purple", "purple-blue", "blue",
    "blue-green", "green", "yellow-green", "yellow", "yellow-red"
]

# Δuvを計算する関数
def calculate_delta_uv(data, color_order):
    delta_uv_list = []
    for i in range(len(color_order)):
        color1 = color_order[i]
        color2 = color_order[(i + 1) % len(color_order)]  # 隣接する次の色
        u1, v1 = data.loc[color1, ['色度 u\'', '色度 v\'']]
        u2, v2 = data.loc[color2, ['色度 u\'', '色度 v\'']]
        delta_uv = np.sqrt((u2 - u1)**2 + (v2 - v1)**2)
        delta_uv_list.append((color1, color2, delta_uv))
    return delta_uv_list

# ペアごとのデータを合計または平均計算
def calculate_pair_values(data, delta_uv_list, metric="sum"):
    pair_values = []
    for color1, color2, delta_uv in delta_uv_list:
        value1 = data.get(color1, 0)
        value2 = data.get(color2, 0)
        if metric == "sum":
            total_value = value1 + value2
        elif metric == "mean":
            total_value = (value1 + value2) / 2
        pair_values.append((color1, color2, delta_uv, total_value))
    return pair_values

# 単回帰分析を計算する関数
def calculate_regression(pair_values):
    delta_uv_values = [item[2] for item in pair_values]
    target_values = [item[3] for item in pair_values]
    slope, intercept, r_value, p_value, _ = linregress(delta_uv_values, target_values)
    return {
        'Coefficient': slope,
        'R_squared': r_value ** 2,
        'P_value': p_value
    }

# メイン処理
reaction_files = [file_reaction_6, file_reaction_8]
accuracy_files = [file_accuracy_6, file_accuracy_8]
results = {"Reaction": {}, "Accuracy": {}}

# Δuvデータを読み込む
uv_data = pd.read_csv(file_uv, skiprows=1, index_col=0)

for i in range(2):
    # 刺激数（6 or 8）
    stimulus_number = 6 if i == 0 else 8

    # 反応時間データを読み込む
    reaction_data = pd.read_csv(reaction_files[i]).set_index('color')['mean'].to_dict()

    # 正解率データを読み込む
    accuracy_data = pd.read_csv(accuracy_files[i]).set_index('color')['accuracy'].to_dict()

    # Δuvを計算
    delta_uv_list = calculate_delta_uv(uv_data, color_order)

    # ペアごとの反応時間合計を計算
    pair_reaction_times = calculate_pair_values(reaction_data, delta_uv_list, metric="sum")

    # ペアごとの正解率平均を計算
    pair_accuracy_means = calculate_pair_values(accuracy_data, delta_uv_list, metric="mean")

    # 単回帰分析を計算
    reaction_regression = calculate_regression(pair_reaction_times)
    accuracy_regression = calculate_regression(pair_accuracy_means)

    # 結果を保存
    results["Reaction"][f"Stimulus {stimulus_number}"] = reaction_regression
    results["Accuracy"][f"Stimulus {stimulus_number}"] = accuracy_regression

# 単回帰分析結果を出力
for key, value in results.items():
    print(f"\n{key}:")
    for stimulus, regression in value.items():
        print(f"{stimulus}: Coefficient = {regression['Coefficient']:.7f}, R_squared = {regression['R_squared']:.7f}, P_value = {regression['P_value']:.7f}")

