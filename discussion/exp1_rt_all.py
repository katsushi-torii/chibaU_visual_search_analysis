import pandas as pd
import matplotlib.pyplot as plt

# ファイルパス
reaction_time_6_path = "./csv/cleaned/reaction_times_total_6.csv"
reaction_time_8_path = "./csv/cleaned/reaction_times_total_8.csv"
exp1_path = "./csv/cleaned/exp1.csv"

# データの読み込み
reaction_time_6 = pd.read_csv(reaction_time_6_path)
reaction_time_8 = pd.read_csv(reaction_time_8_path)
exp1 = pd.read_csv(exp1_path)

# 必要な列の抽出
reaction_time_6 = reaction_time_6[["color", "mean"]]
reaction_time_8 = reaction_time_8[["color", "mean"]]
exp1 = exp1[["color", "total"]]

# 色名の一致を確認して結合
data_6 = pd.merge(exp1, reaction_time_6, on="color")
data_8 = pd.merge(exp1, reaction_time_8, on="color")

# 相関係数の計算
correlation_6 = round(data_6["total"].corr(data_6["mean"]), 2)
correlation_8 = round(data_8["total"].corr(data_8["mean"]), 2)
print(f"刺激数6の相関係数: {correlation_6}")
print(f"刺激数8の相関係数: {correlation_8}")

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

# 散布図の作成
plt.rcParams['font.family'] = 'Yu Gothic'  # 日本語フォント設定

# 刺激数6の散布図
plt.figure(figsize=(9, 6))
for _, row in data_6.iterrows():
    plt.scatter(row["total"], row["mean"], color=color_map.get(row["color"], "black"), label=row["color"])
plt.xlabel("進出度", fontsize=14)
plt.ylabel("平均反応時間（ms）", fontsize=14)
plt.xlim(-1, 1)
plt.ylim(1200, 1750)
plt.grid()
plt.tight_layout()
plt.show()

# 刺激数8の散布図
plt.figure(figsize=(9, 6))
for _, row in data_8.iterrows():
    plt.scatter(row["total"], row["mean"], color=color_map.get(row["color"], "black"), label=row["color"])
plt.xlabel("進出度", fontsize=14)
plt.ylabel("平均反応時間（ms）", fontsize=14)
plt.xlim(-1, 1)
plt.ylim(1200, 1750)
plt.grid()
plt.tight_layout()
plt.show()
