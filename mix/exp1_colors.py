#進出後退度（全体）と物理的要素の相関関係

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

# CSVファイルパス
progress_file = './csv/cleaned/exp1.csv'  # 進出度データのCSVファイル
mean_std_file = './csv/colors/mean_std.csv'  # 平均値データのCSVファイル

# 進出度データの読み込み
progress_df = pd.read_csv(progress_file)
progress_df['color'] = progress_df['color'].map(color_mapping)  # 英語名を日本語名に変換
progress_df.rename(columns={'color': '色名', 'total': '進出後退度'}, inplace=True)
progress_df = progress_df[['色名', '進出後退度']]  # 必要な列のみを保持

# 平均値データの読み込み
means_df = pd.read_csv(mean_std_file, header=[0, 1], index_col=0)  # MultiIndex対応
means_df.index = means_df.index.map(color_mapping)  # 英語名を日本語名に変換
means = means_df['平均']  # 平均値だけを抽出

# 色名をインデックスに設定して進出後退度と結合
means.index.name = '色名'
combined_df = pd.merge(means, progress_df, on='色名')

# 相関係数を計算
correlations = combined_df.corr(numeric_only=True)  # 数値列のみで相関を計算

# 進出後退度との相関を表示
print("進出後退度との相関係数:")
print(correlations['進出後退度'])

# 結果をプロット（必要に応じて）
# for column in means.columns:
#     plt.scatter(combined_df[column], combined_df['進出後退度'], label=column)
#     plt.xlabel(column)
#     plt.ylabel("進出後退度")
#     plt.title(f"{column} vs 進出後退度")
#     plt.legend()
#     plt.show()
