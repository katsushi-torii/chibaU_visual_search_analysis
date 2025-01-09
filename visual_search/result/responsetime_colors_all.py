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
overall_results = {6: {}, 8: {}}

# 刺激数6と8の全データを格納する辞書
all_data_count = {6: 0, 8: 0}  # 各刺激数のデータ総数

# データ処理
for i, file_path in enumerate(file_list):
    try:
        # データの読み込み
        df = pd.read_csv(file_path)

        # 必要な列の整備
        df["responseTime"] = pd.to_numeric(df["responseTime"], errors="coerce")
        df["targetAmount"] = pd.to_numeric(df["targetAmount"], errors="coerce")  # 数値型に変換

        # targetAmountが6と8の場合に分けて処理
        for target_amount in [6, 8]:
            # 該当するデータを抽出
            filtered_df = df[df["targetAmount"] == target_amount]

            # 全データ数をカウント
            all_data_count[target_amount] += len(filtered_df)

            # 色ごとにresponseTimeを集めて辞書に保存
            for color, times in filtered_df.groupby("answer")["responseTime"]:
                if color not in overall_results[target_amount]:
                    overall_results[target_amount][color] = []
                overall_results[target_amount][color].extend(times.dropna().tolist())  # 欠損値を除去して追加

    except FileNotFoundError:
        print(f"ファイルが見つかりません: {file_path}")
    except Exception as e:
        print(f"エラーが発生しました（被験者_{i + 1}）: {e}")

# 色ごとの全体平均と標準偏差を計算
summary_results = {6: {}, 8: {}}
for target_amount, data in overall_results.items():
    for color, times in data.items():
        if len(times) > 0:  # データがある場合のみ計算
            mean = np.mean(times)
            std = np.std(times, ddof=1)  # 標本標準偏差
            summary_results[target_amount][color] = {"mean": mean, "std": std}

# グラフ作成
plt.rcParams['font.family'] = 'Yu Gothic'  # 日本語フォント設定

for target_amount in [6, 8]:
    data = summary_results[target_amount]
    means = [data[color]["mean"] for color in color_order if color in data]
    stds = [data[color]["std"] for color in color_order if color in data]
    colors = [color_map[color] for color in color_order if color in data]

    plt.figure(figsize=(12, 8))
    plt.bar(color_order[:len(means)], means, yerr=stds, capsize=5, alpha=0.9, color=colors, label=f"刺激数 {target_amount}")
    plt.xticks(range(len(means)), [color_labels[color] for color in color_order[:len(means)]], fontsize=16)
    plt.yticks(fontsize=14)
    plt.ylabel("反応時間 (ms)", fontsize=16)
    plt.ylim(0, 2500)  # Y軸の範囲を固定
    plt.tight_layout()
    plt.show()
