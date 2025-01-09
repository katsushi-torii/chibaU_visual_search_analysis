import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import colour

# フォント設定: Yu Gothic
plt.rcParams['font.family'] = 'Yu Gothic'

# u'v'色度図を生成する関数
def plot_uv_chromaticity_diagram_without_spectral_locus():
    # CIE 1976 UCSの色度図をプロット（スペクトル軌跡を非表示）
    colour.plotting.plot_chromaticity_diagram_CIE1976UCS(
        standalone=False,
        show_spectral_locus=False  # スペクトル軌跡を非表示に設定
    )

    # 軸範囲を設定
    plt.xlabel("u'", fontsize=16)
    plt.ylabel("v'", fontsize=16)  # 確実に縦向きに設定
    plt.xlim(0, 0.65)  # 0以下の余白を削除
    plt.ylim(0, 0.65)  # 0以下の余白を削除

    # 現在の軸を取得し再設定
    ax = plt.gca()
    ax.yaxis.label.set_rotation(90)  # ラベルを縦向きに確実に設定
    ax.set_title("")  # タイトルを空に設定

    # 0.1刻みの点線を追加
    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
    ax.grid(which='major', color='gray', linestyle='--', linewidth=0.5)

# 色データ
colors_data = {
    "赤": (0.41, 0.51),
    "赤紫": (0.38, 0.47),
    "ピンク": (0.32, 0.39),
    "紫": (0.26, 0.30),
    "青紫": (0.21, 0.28),
    "青": (0.16, 0.41),
    "青緑": (0.15, 0.49),
    "緑": (0.15, 0.53),
    "黄緑": (0.18, 0.55),
    "黄": (0.22, 0.54),
    "黄赤": (0.34, 0.53),
    "灰": (0.21, 0.47)
}

# u'v'色度図をプロット
plot_uv_chromaticity_diagram_without_spectral_locus()

# 色データをプロット
for color_name, (u, v) in colors_data.items():
    if color_name == "青紫":
        # 点から線を引き、ラベルを外側に配置
        plt.plot([u, u - 0.11], [v, v - 0.10], color="black", linewidth=0.8)
        plt.text(u - 0.16, v - 0.11, color_name, fontsize=14, ha="left", va="center")
    elif color_name == "紫":
        # 点から線を引き、ラベルを外側に配置
        plt.plot([u, u + 0.14], [v, v - 0.15], color="black", linewidth=0.8)
        plt.text(u + 0.14, v - 0.16, color_name, fontsize=14, ha="left", va="center")   
    elif color_name == "黄緑":
        plt.text(u + 0.007, v + 0.01, color_name, fontsize=14, ha="left", va="center")  # 右上に調整
    else:
        # 通常のラベル配置
        plt.text(u + 0.007, v, color_name, fontsize=14, ha="left", va="center")

    # 黒い点をプロット
    plt.scatter(u, v, color="black")

# プロットを表示
plt.show()
