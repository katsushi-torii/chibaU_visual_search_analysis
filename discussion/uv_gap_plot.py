import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

# データ
colors = [
    "赤 & 赤紫", "赤紫 & ピンク", "ピンク & 紫",
    "紫 & 青紫", "青紫 & 青", "青 & 青緑",
    "青緑 & 緑", "緑 & 黄緑", "黄緑 & 黄",
    "黄 & 黄赤", "黄赤 & 赤"
]
delta_uv = [0.0558, 0.0913, 0.1118, 0.0533, 0.1367, 0.0802, 0.0411, 0.0394, 0.0433, 0.1177, 0.0691]
rgb_values = [
    [(227, 0, 38), (222, 0, 100)], [(222, 0, 100), (208, 0, 159)], [(208, 0, 159), (182, 0, 229)],
    [(182, 0, 229), (137, 63, 254)], [(137, 63, 254), (0, 119, 165)], [(0, 119, 165), (0, 127, 106)],
    [(0, 127, 106), (0, 129, 63)], [(0, 129, 63), (91, 123, 0)], [(91, 123, 0), (133, 111, 0)],
    [(133, 111, 0), (201, 68, 0)], [(201, 68, 0), (227, 0, 38)]
]

# フォント設定
font_path = font_manager.findfont("Yu Gothic")
plt.rcParams['font.family'] = 'Yu Gothic'

# グラフ作成
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.8
x_positions = np.arange(len(colors))

for i, (color_pair, uv, rgb_pair) in enumerate(zip(colors, delta_uv, rgb_values)):
    left_color = tuple(c / 255 for c in rgb_pair[0])
    right_color = tuple(c / 255 for c in rgb_pair[1])
    # 棒グラフの左側
    ax.bar(x_positions[i] - bar_width / 4, uv, width=bar_width / 2, color=left_color, align='center')
    # 棒グラフの右側
    ax.bar(x_positions[i] + bar_width / 4, uv, width=bar_width / 2, color=right_color, align='center')

# グラフの設定
ax.set_xticks(x_positions)
ax.set_xticklabels(["\n".join(color.split(" & ")) for color in colors], rotation=0, ha="center", fontsize=14)
ax.set_ylabel("Δu'v'", fontsize=14)
plt.tight_layout()

# 表示
plt.show()
