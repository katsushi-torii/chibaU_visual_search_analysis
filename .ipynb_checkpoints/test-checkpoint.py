import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


# # CSVファイルからデータを読み込む
data = pd.read_csv('./csv/oshida_answers.csv')

# # データの基本情報を確認
print(data.head())        # 先頭5行を表示
print(data.info())        # データの概要情報を表示
print(data.describe())    # 数値データの統計情報を表示

# # 例: 反応時間の分布をヒストグラムで表示
# plt.hist(data['responseTime'], bins=30)
# plt.xlabel('Reaction Time (ms)')
# plt.ylabel('Frequency')
# plt.title('Distribution of Reaction Time')
# plt.show()
