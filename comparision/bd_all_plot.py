# 正規化したスコアの散布図を生成
import numpy as np
import matplotlib.pyplot as plt

data = [
    {"red": 0.4367, "red-purple": 0.3954, "pink": 0.2969, "purple": 0.2688, "yellow-red": 0.2155,
     "purple-blue": 0.1634, "blue": 0.1099, "green": 0.0811, "blue-green": 0.0111, "yellow-green": -0.4894,
     "yellow": -0.4894, "gray": -1.0000},  # 被験者1
    {"red": 1.0000, "red-purple": 0.2039, "pink": 0.0672, "purple": 0.0345, "yellow-red": -0.0485,
     "green": -0.0734, "purple-blue": -0.0977, "blue": -0.1458, "blue-green": -0.1703, "yellow-green": -0.1958,
     "yellow": -0.2517, "gray": -0.3224},  # 被験者2
    {"red": 1.0000, "red-purple": 0.1605, "purple": 0.0867, "purple-blue": 0.0556, "yellow-red": 0.0263,
     "pink": -0.0296, "blue": -0.0570, "green": -0.1697, "blue-green": -0.1697, "yellow-green": -0.2316,
     "yellow": -0.2659, "gray": -0.4057},  # 被験者3
    {"red": 0.5615, "pink": 0.5615, "red-purple": 0.3330, "yellow-green": 0.1211, "purple-blue": 0.1211,
     "purple": 0.1211, "blue-green": 0.0170, "yellow-red": 0.0170, "green": -0.0877, "yellow": -0.0877,
     "gray": -0.6782, "blue": -1.0000},  # 被験者4
    {"red": 1.0000, "red-purple": 0.5031, "pink": -0.0383, "yellow-red": -0.0595, "purple": -0.0786,
     "yellow-green": -0.0964, "purple-blue": -0.1465, "blue": -0.1631, "green": -0.1800, "blue-green": -0.1977,
     "yellow": -0.2166, "gray": -0.3264},  # 被験者5
    {"red": 0.7865, "pink": 0.5816, "yellow-red": 0.3849, "red-purple": 0.3849, "green": 0.3849,
     "purple-blue": 0.1934, "blue": 0.0042, "blue-green": -0.1851, "purple": -0.3772, "yellow-green": -0.3772,
     "yellow": -0.7809, "gray": -1.0000},  # 被験者6
    {"red": 0.3984, "red-purple": 0.2666, "purple-blue": 0.2061, "purple": 0.1787, "pink": 0.1521,
     "yellow-red": 0.1258, "green": 0.0992, "blue": -0.0176, "blue-green": -0.0512, "yellow-green": -0.1278,
     "yellow": -0.2302, "gray": -1.0000},  # 被験者7
]

# 平均値（手動で提供された値）
average_scores = {
    'red': 0.74, 'red-purple': 0.32, 'pink': 0.23, 'purple': 0.03, 'yellow-red': 0.09,
    'purple-blue': 0.07, 'green': 0.01, 'blue-green': -0.11, 'blue': -0.18, 'yellow-green': -0.20,
    'yellow': -0.33, 'gray': -0.68
}

# 色を平均スコアの降順にソート
sorted_colors = sorted(average_scores.keys(), key=lambda x: average_scores[x], reverse=True)

# RGB値と日本語ラベル
color_rgb = {
    'red': (227/255, 0, 38/255),
    'red-purple': (222/255, 0, 100/255),
    'pink': (208/255, 0, 159/255),
    'purple': (182/255, 0, 229/255),
    'purple-blue': (137/255, 63/255, 254/255),
    'blue': (0, 119/255, 165/255),
    'blue-green': (0, 127/255, 106/255),
    'green': (0, 129/255, 63/255),
    'yellow-green': (91/255, 123/255, 0),
    'yellow': (133/255, 111/255, 0),
    'yellow-red': (201/255, 68/255, 0),
    'gray': (120/255, 109/255, 113/255)
}
color_name_dict = {
    'gray': '灰', 'red': '赤', 'green': '緑', 'blue': '青', 'yellow': '黄', 'purple': '紫',
    'pink': 'ピンク', 'yellow-red': '黄赤', 'yellow-green': '黄緑', 'blue-green': '青緑',
    'purple-blue': '青紫', 'red-purple': '赤紫'
}

# 被験者ごとのマーカー形状
markers = ['o', 's', 'D', '^', 'v', '<', '>']

# 散布図を描画
plt.figure(figsize=(10, 7))
plt.rcParams['font.family'] = 'Yu Gothic'  # 日本語フォント

# 被験者データをプロット
for subject_idx, subject_data in enumerate(data, start=1):
    for color_idx, color in enumerate(sorted_colors):
        plt.scatter(
            color_idx,  # 色ごとの位置
            subject_data[color],  # スコア
            color=color_rgb[color],  # 色そのもの
            marker=markers[subject_idx - 1],  # 被験者のマーカー
            label=f"被験者{subject_idx}" if color_idx == 0 else "",  # 重複しない凡例
            s=100,  # 点のサイズ
            alpha=0.8
        )

# 平均値をプロット（太い線で目立たせる）
average_values = [average_scores[color] for color in sorted_colors]
plt.plot(
    range(len(sorted_colors)),  # x 軸
    average_values,  # 平均スコア
    color='black', linestyle='-', linewidth=2.5, label="平均値"
)

# 軸と装飾
plt.xticks(range(len(sorted_colors)), [color_name_dict[color] for color in sorted_colors], fontsize=14)
plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
plt.ylabel("正規化した進出度スコア", fontsize=14)

# 凡例をカスタムハンドルで作成
legend_labels = [f"被{i+1}" for i in range(7)] + ["平均値"]  # 被験者ラベル + 平均値
markers += ['_']  # 平均値用の凡例

# カスタムハンドル（凡例用）を生成
handles = [
    plt.Line2D([0], [0], color='black' if i == len(legend_labels) - 1 else 'black',
               marker=markers[i], linestyle='-' if i == len(legend_labels) - 1 else 'None',
               markersize=10 if i != len(legend_labels) - 1 else 0, linewidth=2.5 if i == len(legend_labels) - 1 else 0)
    for i in range(len(legend_labels))
]

# 凡例を作成
plt.legend(
    handles,               # カスタムハンドル
    legend_labels,         # ラベルリストを指定
    fontsize=14,           # フォントサイズ
    loc='upper center',    # グラフの上部中央に配置
    bbox_to_anchor=(0.5, -0.05),  # グラフ下部に配置
    ncol=8,                # 横に並べる列数
    frameon=False,          # 枠を非表示
    handletextpad=0.5,       # アイコンと文字の間隔を狭める
    columnspacing=0.8        # 列間のスペースを調整
)

plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
