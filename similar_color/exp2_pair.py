import pandas as pd

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

# ペアと選ばれた回数のデータ
pairs_data = {
    'ペア': [
        ('緑', '青緑'),
        ('ピンク', '赤紫'),
        ('紫', 'ピンク'),
        ('青紫', '紫'),
        ('赤', '赤紫'),
        ('黄', '黄緑')
    ],
    '選ばれた回数': [3, 3, 2, 2, 1, 1]
}
pairs_df = pd.DataFrame(pairs_data)

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

# ペアごとの反応時間と正解率を計算
pair_reaction_times = []
pair_correct_rates = []
for pair in pairs_df['ペア']:
    color1, color2 = pair
    time1 = reaction_time_data.loc[reaction_time_data['色名'] == color1, '反応時間'].values
    time2 = reaction_time_data.loc[reaction_time_data['色名'] == color2, '反応時間'].values
    rate1 = correct_rate_data.loc[correct_rate_data['色名'] == color1, '正解率'].values
    rate2 = correct_rate_data.loc[correct_rate_data['色名'] == color2, '正解率'].values

    if len(time1) > 0 and len(time2) > 0:
        pair_reaction_times.append(time1[0] + time2[0])
    else:
        pair_reaction_times.append(None)  # データが見つからない場合

    if len(rate1) > 0 and len(rate2) > 0:
        pair_correct_rates.append((rate1[0] + rate2[0]) / 2)  # 正解率の平均
    else:
        pair_correct_rates.append(None)  # データが見つからない場合

# ペアごとの反応時間と正解率をデータフレームに追加
pairs_df['ペアの反応時間'] = pair_reaction_times
pairs_df['ペアの正解率'] = pair_correct_rates

# 欠損値を除外
pairs_df = pairs_df.dropna()

# 相関係数を計算
correlation_reaction_time = pairs_df['選ばれた回数'].corr(pairs_df['ペアの反応時間'])
correlation_correct_rate = pairs_df['選ばれた回数'].corr(pairs_df['ペアの正解率'])

# 結果を表示
print("ペアごとのデータ:")
print(pairs_df)
print("\n選ばれた回数とペアの反応時間の相関係数:", correlation_reaction_time)
print("\n選ばれた回数とペアの正解率の相関係数:", correlation_correct_rate)

# グラフをプロット（必要に応じて）
# import matplotlib.pyplot as plt
# plt.figure(figsize=(12, 6))

# plt.subplot(1, 2, 1)
# plt.scatter(pairs_df['ペアの反応時間'], pairs_df['選ばれた回数'], color='blue')
# plt.xlabel('ペアの反応時間')
# plt.ylabel('選ばれた回数')
# plt.title('選ばれた回数 vs ペアの反応時間')

# plt.subplot(1, 2, 2)
# plt.scatter(pairs_df['ペアの正解率'], pairs_df['選ばれた回数'], color='green')
# plt.xlabel('ペアの正解率')
# plt.ylabel('選ばれた回数')
# plt.title('選ばれた回数 vs ペアの正解率')

# plt.tight_layout()
# plt.show()