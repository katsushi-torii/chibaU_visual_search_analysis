#実験２の結果（反応時間と正解率）と色の物理的要素の相関関係を検証

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

# 平均値データの読み込みと前処理
means_df = pd.read_csv('./csv/colors/mean_std.csv', header=[0, 1], index_col=0)
means_df.index = means_df.index.map(color_mapping)  # 日本語名に変換
means = means_df['平均']  # 平均値だけを抽出

# nan を除外
means = means.dropna()

# データの結合
means.index.name = '色名'
combined_df = pd.merge(means, reaction_time_data, on='色名')
combined_df = pd.merge(combined_df, correct_rate_data, on='色名')

# 相関係数を計算
correlations = combined_df.corr(numeric_only=True)

# 各項目との相関を表示
print("各項目と反応時間の相関係数:")
print(correlations['反応時間'])

print("\n各項目と正解率の相関係数:")
print(correlations['正解率'])

# 平均値データの読み込みと前処理
means_df = pd.read_csv('./csv/colors/mean_std.csv', header=[0, 1], index_col=0)
means_df.index = means_df.index.map(color_mapping)  # 日本語名に変換
means = means_df['平均']  # 平均値だけを抽出

# nan を除外
means = means.dropna()

# 結合
means.index.name = '色名'
combined_df = pd.merge(means, reaction_time_data, on='色名')

# 相関係数を計算
correlations = combined_df.corr(numeric_only=True)

# 各項目と反応時間の相関を表示
print("各項目と反応時間の相関係数:")
print(correlations['反応時間'])
