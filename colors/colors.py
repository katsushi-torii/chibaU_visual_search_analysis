import pandas as pd

#header=Noneで列名を読み込まない、Tで転置
df_raw = pd.read_csv("./csv/colors.csv", header=None)
df = df_raw.T
df.columns = df.iloc[0]  #1行目を列名に設定
df = df[1:].reset_index(drop=True)  #1行目を削除し、インデックスをリセット

#色の配列
colors = df["色"].unique()
#各色の測定回数（同じ回数になるかチェック）
color_counts = df["色"].value_counts()
# print(color_counts)

#df内のデータを文字列から数値に変換
for col in df.columns[2:]:  #インデックス0である"色"以外の列を変換
    df[col] = pd.to_numeric(df[col])


#平均値の表を生成、numericonlyで測定日を排除
means = df.groupby("色").mean(numeric_only=True)

#色の登場順に並べ替え
order = pd.Categorical(df["色"], categories=df["色"].unique(), ordered=True)
means = means.reindex(order.categories)

print(means)
