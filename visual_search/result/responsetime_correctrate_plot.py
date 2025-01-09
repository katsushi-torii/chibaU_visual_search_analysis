# 各被験者の色ごとの平均反応時間と正解率を散布図でプロット

import pandas as pd
import matplotlib.pyplot as plt

# 色順とRGB対応
color_order = [
    "red", "red-purple", "pink", "purple", "purple-blue", "blue",
    "blue-green", "green", "yellow-green", "yellow", "yellow-red", "gray"
]
color_map = {
    "red": (227/255, 0, 38/255),
    "red-purple": (222/255, 0, 100/255),
    "pink": (208/255, 0, 159/255),
    "purple": (182/255, 0, 229/255),
    "purple-blue": (137/255, 63/255, 254/255),
    "blue": (0, 119/255, 165/255),
    "blue-green": (0, 127/255, 106/255),
    "green": (0, 129/255, 63/255),
    "yellow-green": (91/255, 123/255, 0),
    "yellow": (133/255, 111/255, 0),
    "yellow-red": (201/255, 68/255, 0),
    "gray": (120/255, 109/255, 113/255)
}

# 日本語ラベル
color_labels = {
    "red": "赤", "red-purple": "赤紫", "pink": "ピンク", "purple": "紫",
    "purple-blue": "青紫", "blue": "青", "blue-green": "青緑",
    "green": "緑", "yellow-green": "黄緑", "yellow": "黄",
    "yellow-red": "黄赤", "gray": "灰"
}

# 被験者ごとのマーカー形状
markers = ['o', 's', 'D', '^', 'v', '<', '>']

# 散布図を作成する関数
def plot_scatter(data, metric, ylabel, title, ylim=None):
    plt.figure(figsize=(10, 6))
    plt.rcParams['font.family'] = 'Yu Gothic'  # 日本語フォント設定

    # 色をソート（反応時間または正解率に基づく）
    average_values = {
        color: sum(subject_data[color][metric] for subject_data in data if color in subject_data) / len(data)
        for color in color_order
    }
    sorted_colors = sorted(average_values.keys(), key=lambda x: average_values[x], reverse=("正解率" in ylabel))

    for subject_idx, subject_data in enumerate(data, start=1):
        for color_idx, color in enumerate(sorted_colors):
            if color in subject_data:
                plt.scatter(
                    color_idx,  # 色ごとの位置
                    subject_data[color][metric],  # 指定されたメトリック（平均値）
                    color=color_map[color],
                    marker=markers[subject_idx - 1],
                    s=100,  # 点のサイズ
                    label=f"被験者{subject_idx}" if color_idx == 0 else "",
                    alpha=0.8
                )

    # 平均値をプロット
    sorted_average_values = [average_values[color] for color in sorted_colors]
    plt.plot(
        range(len(sorted_colors)),  # x 軸
        sorted_average_values,  # 平均スコア
        color='black', linestyle='-', linewidth=2.5, label="平均値"
    )

    plt.xticks(range(len(sorted_colors)), [color_labels[color] for color in sorted_colors], fontsize=14)
    if ylim:
        plt.ylim(ylim)
    plt.ylabel(ylabel, fontsize=14)
    plt.grid(alpha=0.3)

    # 凡例をカスタムハンドルで作成
    legend_labels = [f"被{i+1}" for i in range(7)] + ["平均値"]
    custom_handles = [
        plt.Line2D([0], [0], marker=markers[i], color='black', markerfacecolor='black', markersize=10, linestyle='None')
        for i in range(7)
    ] + [
        plt.Line2D([0], [0], color='black', linewidth=2.5, linestyle='-')
    ]

    plt.legend(
        custom_handles, legend_labels, fontsize=12,
        loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=8, frameon=False  # 凡例とグラフの間隔をさらに狭める
    )

    plt.tight_layout()
    plt.show()

# CSVファイルからデータを読み込む関数
def load_csv_data(filepath):
    df = pd.read_csv(filepath, index_col="色名")
    data = []
    for subject_idx in range(1, 8):  # 被験者1～7
        subject_data = {}
        for color in color_order:
            if color in df.index:
                # 正解率の場合、パーセント記号を削除してfloatに変換
                col_name = f"被験者_{subject_idx}_accuracy" if "accuracy" in filepath else f"被験者_{subject_idx}_mean"
                if col_name in df.columns:
                    value = df.loc[color, col_name]
                    if isinstance(value, str) and "%" in value:
                        value = float(value.replace("%", ""))
                    subject_data[color] = {"mean": value}
        data.append(subject_data)
    return data

# データ読み込み
reaction_time_data_6 = load_csv_data("./csv/cleaned/reaction_times_6.csv")
reaction_time_data_8 = load_csv_data("./csv/cleaned/reaction_times_8.csv")
accuracy_data_6 = load_csv_data("./csv/cleaned/accuracy_rates_6.csv")
accuracy_data_8 = load_csv_data("./csv/cleaned/accuracy_rates_8.csv")

# 散布図をプロット
plot_scatter(reaction_time_data_6, "mean", "反応時間 (ms)", "刺激数6の反応時間", ylim=(900, 2350))
plot_scatter(reaction_time_data_8, "mean", "反応時間 (ms)", "刺激数8の反応時間", ylim=(900, 2350))
plot_scatter(accuracy_data_6, "mean", "正解率 (%)", "刺激数6の正解率", ylim=(35, 102))
plot_scatter(accuracy_data_8, "mean", "正解率 (%)", "刺激数8の正解率", ylim=(35, 102))
