#進出後退度（全体）と物理的要素の相関関係

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

# CSVから進出後退度データを読み込み
progress_df = pd.read_csv('./csv/cleaned/exp1.csv')
progress_df['color'] = progress_df['color'].map(color_mapping)  # 英語名を日本語名に変換
progress_df.rename(columns={'color': '色名', 'total': '進出後退度'}, inplace=True)
progress_df = progress_df[['色名', '進出後退度']]  # 必要な列だけ抽出

# 平均値データの読み込み
means_df = pd.read_csv('./csv/colors/mean_std.csv', header=[0, 1], index_col=0)  # MultiIndex対応
means_df.index = means_df.index.map(color_mapping)  # 英語名を日本語名に変換
means = means_df['平均']  # 平均値だけを抽出

# 色名をインデックスに設定して進出後退度と結合
means.index.name = '色名'
combined_df = pd.merge(means, progress_df, on='色名')

# 主波長がマイナスのデータを除外
filtered_df = combined_df[combined_df['主波長[nm]'] > 0]

# 相関係数を計算
correlations = filtered_df.corr(numeric_only=True)  # 数値列のみで相関を計算

# 主波長と進出後退度の相関を表示
print("主波長と進出後退度の相関係数:")
print(correlations['進出後退度']['主波長[nm]'])

# 結果をプロット
# plt.scatter(filtered_df['主波長[nm]'], filtered_df['進出後退度'], color='blue')
# plt.xlabel('主波長')
# plt.ylabel('進出後退度')
# plt.title('主波長 vs 進出後退度')
# plt.show()
