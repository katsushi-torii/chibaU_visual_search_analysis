import pandas as pd
import numpy as np

# 英語と日本語の色名の対応付け
color_mapping = {
    'red': '赤',
    'red-purple': '赤紫',
    'pink': 'ピンク',
    'yellow-red': '黄赤',
    'purple-blue': '青紫',
    'purple': '紫',
    'green': '緑',
    'blue-green': '青緑',
    'blue': '青',
    'yellow-green': '黄緑',
    'yellow': '黄',
    'gray': '灰'
}

# 反応時間データの読み込みと前処理
reaction_time_data = pd.read_csv('./csv/cleaned/responseTime.csv')
reaction_time_data.rename(columns={'color': '色名'}, inplace=True)
reaction_time_data['色名'] = reaction_time_data['色名'].map(color_mapping)  # 日本語名に変換
reaction_time_data = reaction_time_data[['色名', 'total_avg']]
reaction_time_data.columns = ['色名', '反応時間']

# 正解率データの読み込みと前処理
correct_rate_data = pd.read_csv('./csv/cleaned/correctRate.csv')
correct_rate_data.rename(columns={'color': '色名'}, inplace=True)
correct_rate_data['色名'] = correct_rate_data['色名'].map(color_mapping)  # 日本語名に変換
correct_rate_data = correct_rate_data[['色名', 'total']]
correct_rate_data.columns = ['色名', '正解率']

# アンケートデータの作成
survey_data = {
    '色名': ['ピンク', '紫', '赤紫', '青緑', '緑', '青紫', '黄', '黄緑', '赤', '灰', '黄赤', '青'],
    'アンケート値': [5, 4, 4, 3, 3, 2, 1, 1, 1, 0, 0, 0]  # 灰、黄赤、青は0
}
survey_df = pd.DataFrame(survey_data)

# データフレームの結合
combined_df = pd.merge(reaction_time_data, correct_rate_data, on='色名', how='inner')
combined_df = pd.merge(combined_df, survey_df, on='色名', how='inner')

# デバッグ: 結合後のデータフレーム確認
print("\n結合後のデータフレーム:")
print(combined_df)

# 相関係数を計算
correlations = combined_df.corr(numeric_only=True)

# 結果の出力
print("\n反応時間とアンケート値の相関係数:")
print(correlations['反応時間']['アンケート値'])

print("\n正解率とアンケート値の相関係数:")
print(correlations['正解率']['アンケート値'])



import matplotlib.pyplot as plt
from matplotlib import rcParams


# グラフ出力
# 反応時間 vs アンケート値
plt.figure(figsize=(8, 6))
plt.scatter(combined_df['アンケート値'], combined_df['反応時間'], color='blue')
plt.xlabel('Counts')
plt.ylabel('Response Time')
plt.grid(True)
plt.legend()
# plt.savefig('./output/reaction_time_vs_survey.png')
plt.show()

# 正解率 vs アンケート値
plt.figure(figsize=(8, 6))
plt.scatter(combined_df['アンケート値'], combined_df['正解率'], color='green')
plt.xlabel('Counts')
plt.ylabel('Correct Rate')
plt.grid(True)
plt.legend()
# plt.savefig('./output/correct_rate_vs_survey.png')
plt.show()
