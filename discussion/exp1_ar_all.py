import pandas as pd
import matplotlib.pyplot as plt

# ファイルパス
accuracy_6_path = "./csv/cleaned/accuracy_total_6.csv"
accuracy_8_path = "./csv/cleaned/accuracy_total_8.csv"
exp1_path = "./csv/cleaned/exp1.csv"

# データの読み込み
accuracy_6 = pd.read_csv(accuracy_6_path)
accuracy_8 = pd.read_csv(accuracy_8_path)
exp1 = pd.read_csv(exp1_path)

# 必要な列の整備
accuracy_6 = accuracy_6.set_index("color")
accuracy_8 = accuracy_8.set_index("color")
exp1 = exp1.set_index("color")

# データの結合
data_6 = pd.merge(exp1, accuracy_6, left_index=True, right_index=True)
data_8 = pd.merge(exp1, accuracy_8, left_index=True, right_index=True)

# 相関係数の計算
correlation_6 = round(data_6["total"].corr(data_6["accuracy"]), 2)
correlation_8 = round(data_8["total"].corr(data_8["accuracy"]), 2)
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
    plt.scatter(row["total"], row["accuracy"], color=color_map.get(row.name, "black"), label=row.name)
plt.xlabel("進出度", fontsize=14)
plt.ylabel("正解率（%）", fontsize=14)
plt.xlim(-1, 1)
plt.ylim(75, 101)
plt.grid()
plt.tight_layout()
plt.show()

# 刺激数8の散布図
plt.figure(figsize=(9, 6))
for _, row in data_8.iterrows():
    plt.scatter(row["total"], row["accuracy"], color=color_map.get(row.name, "black"), label=row.name)
plt.xlabel("進出度", fontsize=14)
plt.ylabel("正解率（%）", fontsize=14)
plt.xlim(-1, 1)
plt.ylim(75, 101)
plt.grid()
plt.tight_layout()
plt.show()
