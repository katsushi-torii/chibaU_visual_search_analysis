#レンジグラフで一対比較法結果の各色の変動幅を表示

import matplotlib.pyplot as plt

# 色ごとのRGB値
color_rgb = {
    '赤': (227/255, 0, 38/255),
    '赤紫': (222/255, 0, 100/255),
    'ピンク': (208/255, 0, 159/255),
    '黄赤': (201/255, 68/255, 0),
    '青紫': (137/255, 63/255, 254/255),
    '紫': (182/255, 0, 229/255),
    '緑': (0, 129/255, 63/255),
    '青緑': (0, 127/255, 106/255),
    '青': (0, 119/255, 165/255),
    '黄緑': (91/255, 123/255, 0),
    '黄': (133/255, 111/255, 0),
    '灰': (120/255, 109/255, 113/255)  # "灰" を "グレー" に変更
}

# データ
colors = ['赤', '赤紫', 'ピンク', '黄赤', '青紫', '紫', '緑', '青緑', '青', '黄緑', '黄', '灰']
rank_min = [1, 2, 1, 3, 3, 3, 3, 6, 7, 6, 9, 11]
rank_max = [1, 3, 6, 6, 7, 9, 9, 10, 12, 10, 11, 12]


# データを逆順にする
colors = colors[::-1]
rank_min = rank_min[::-1]
rank_max = rank_max[::-1]

# 修正版グラフ作成
plt.figure(figsize=(10, 6))
for i, color in enumerate(colors):
    plt.plot([rank_min[i], rank_max[i]], [i, i], marker='s', color=color_rgb[color], linewidth=2)

# 軸ラベルとタイトル
plt.yticks(range(len(colors)), colors, fontname="Yu Gothic", fontsize=14)
plt.xticks(range(1, 13), fontsize=14)

# グリッド
plt.grid(axis='x', linestyle='--', alpha=0.7)

# 表示
plt.tight_layout()
plt.show()
