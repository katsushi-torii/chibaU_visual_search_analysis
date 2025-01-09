import pandas as pd
import numpy as np
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

# ファイルリスト
file_list = [f"./csv/main/answers_subject{i}.csv" for i in range(1, 8)]

# 刺激数6と8のデータを格納する辞書
overall_accuracy = {6: {}, 8: {}}

# データ処理
for file_path in file_list:
    try:
        # データの読み込み
        df = pd.read_csv(file_path)

        # 必要な列の整備
        df["correct"] = pd.to_numeric(df["correct"], errors="coerce")
        df["targetAmount"] = pd.to_numeric(df["targetAmount"], errors="coerce")  # 数値型に変換

        # targetAmountが6と8の場合に分けて処理
        for target_amount in [6, 8]:
            # 該当するデータを抽出
            filtered_df = df[df["targetAmount"] == target_amount]

            # 色ごとの正解率を計算
            for color, correct_values in filtered_df.groupby("answer")["correct"]:
                if color not in overall_accuracy[target_amount]:
                    overall_accuracy[target_amount][color] = []
                overall_accuracy[target_amount][color].extend(correct_values.dropna().tolist())  # 欠損値を除去して追加

    except FileNotFoundError:
        print(f"ファイルが見つかりません: {file_path}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

# 色ごとの全体正解率を計算
summary_accuracy = {6: {}, 8: {}}
for target_amount, data in overall_accuracy.items():
    for color, correct_values in data.items():
        if len(correct_values) > 0:  # データがある場合のみ計算
            accuracy = np.mean(correct_values) * 100  # 正解率をパーセントに変換
            summary_accuracy[target_amount][color] = accuracy

# 結果をCSVに保存
for target_amount in [6, 8]:
    summary_df = pd.DataFrame.from_dict(summary_accuracy[target_amount], orient="index", columns=["accuracy"])
    summary_df.index.name = "color"
    summary_df.to_csv(f"./csv/cleaned/accuracy_total_{target_amount}.csv")

# 結果出力
for target_amount in [6, 8]:
    print(f"\n刺激数{target_amount}の正解率と試行数:")
    data = summary_accuracy[target_amount]
    trials = overall_accuracy[target_amount]
    for color in color_order:
        accuracy = data.get(color, 0)
        trial_count = len(trials.get(color, []))
        print(f"{color_labels[color]}: {accuracy:.2f}% ({trial_count} 試行)")

# 折れ線グラフ作成
plt.rcParams['font.family'] = 'Yu Gothic'  # 日本語フォント設定

plt.figure(figsize=(10, 6))

# 刺激数8の正解率
data_8 = [summary_accuracy[8].get(color, 0) for color in color_order]
plt.plot(range(len(color_order)), data_8, label="SG1", color="black", linestyle="-", linewidth=1.5)

# 刺激数6の正解率
data_6 = [summary_accuracy[6].get(color, 0) for color in color_order]
plt.plot(range(len(color_order)), data_6, label="SG2", color="black", linestyle="--", linewidth=1.5)

# 各データ点をプロット
for idx, (color, accuracy) in enumerate(zip(color_order, data_8)):
    plt.scatter(idx, accuracy, color=color_map[color], s=150, zorder=5)

for idx, (color, accuracy) in enumerate(zip(color_order, data_6)):
    plt.scatter(idx, accuracy, color=color_map[color], s=150, zorder=5)

plt.xticks(range(len(color_order)), [color_labels[color] for color in color_order], fontsize=16)
plt.yticks(fontsize=14)
plt.ylabel("正解率 (%)", fontsize=18)
plt.ylim(75, 102)  # Y軸の範囲を設定
plt.legend(fontsize=16)
plt.tight_layout()
plt.show()
