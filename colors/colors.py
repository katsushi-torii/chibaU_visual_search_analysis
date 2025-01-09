import pandas as pd
import matplotlib.pyplot as plt

# CSVファイルの読み込み
df_raw = pd.read_csv("./csv/colors/colors.csv", header=None)
df = df_raw.T
df.columns = df.iloc[0]  # 1行目を列名に設定
df = df[1:].reset_index(drop=True)  # 1行目を削除し、インデックスをリセット

# 色の配列
colors = df["色"].unique()

# "blue-purple" を "purple-blue" に変更
df["色"] = df["色"].replace("blue-purple", "purple-blue")

# 各列を数値に変換（色以外）
for col in df.columns[2:]:  # "色"以外の列を変換
    df[col] = pd.to_numeric(df[col])

# 平均値と標準偏差を計算
means = df.groupby("色").mean(numeric_only=True)
std_devs = df.groupby("色").std(numeric_only=True)

# 各色の登場回数を計算
color_counts = df["色"].value_counts()

# 小数点以下3桁に四捨五入
means_rounded = means.round(3)
std_devs_rounded = std_devs.round(3)

# 色の登場順に並べ替え
order = pd.Categorical(df["色"], categories=df["色"].unique(), ordered=True)
means_rounded = means_rounded.reindex(order.categories)
std_devs_rounded = std_devs_rounded.reindex(order.categories)

# 結果表示
# print("各色の登場回数:")
# print(color_counts)
print("\n平均値:")
print(means_rounded)
# print("\n標準偏差:")
# print(std_devs_rounded)

# 平均値と標準偏差の表を作成
mean_std_df = pd.concat([means_rounded, std_devs_rounded], axis=1, keys=['平均', '標準偏差'])
# print("\n平均値と標準偏差:")
# print(mean_std_df)

# 必要であれば、この結果をCSVファイルとして保存
mean_std_df.to_csv('./csv/colors/mean_std.csv', encoding='utf-8')
