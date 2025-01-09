# 全体の正規化した進出度スコアを算出、棒グラフ作成

import numpy as np
import matplotlib.pyplot as plt

# 各被験者のデータ
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

# 順番を統一
ordered_colors = [
    'red', 'red-purple', 'pink', 'purple', 'purple-blue', 
    'blue', 'blue-green', 'green', 'yellow-green', 'yellow', 
    'yellow-red', 'gray'
]

# RGB値
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

# 平均スコア計算
average_scores = {color: np.mean([subject[color] for subject in data]) for color in ordered_colors}

# 日本語色名対応
color_name_dict = {
    'gray': '灰',
    'red': '赤',
    'green': '緑',
    'blue': '青',
    'yellow': '黄',
    'purple': '紫',
    'pink': 'ピンク',
    'yellow-red': '黄赤',
    'yellow-green': '黄緑',
    'blue-green': '青緑',
    'purple-blue': '青紫',
    'red-purple': '赤紫'
}

# グラフ作成
colors_jp = [color_name_dict[color] for color in ordered_colors]
scores = [average_scores[color] for color in ordered_colors]

plt.rcParams['font.family'] = 'Yu Gothic'  # 日本語フォント
plt.figure(figsize=(10, 5))
plt.xlim(-1, 1)
plt.barh(
    colors_jp, 
    scores, 
    align='center', 
    color=[color_rgb[color] for color in ordered_colors]
)
plt.xlabel('正規化した進出度スコア', fontsize=14)
plt.yticks(fontsize=14)
plt.gca().invert_yaxis()
plt.show()
