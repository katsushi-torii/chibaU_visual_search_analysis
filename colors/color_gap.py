from colormath.color_objects import xyYColor, LabColor
from colormath.color_conversions import convert_color
import numpy as np

# delta_e_cie2000 の再実装
def delta_e_cie2000(lab1, lab2):
    """
    Calculate the color difference using CIEDE2000.
    This is a re-implementation to bypass numpy.asscalar issues.
    """
    L1, a1, b1 = lab1.lab_l, lab1.lab_a, lab1.lab_b
    L2, a2, b2 = lab2.lab_l, lab2.lab_a, lab2.lab_b

    # CIEDE2000 constants
    kL = kC = kH = 1

    # Delta L'
    delta_L_prime = L2 - L1
    L_bar = (L1 + L2) / 2

    # Calculate C1, C2, C_bar, and Delta C'
    C1 = np.sqrt(a1**2 + b1**2)
    C2 = np.sqrt(a2**2 + b2**2)
    C_bar = (C1 + C2) / 2
    delta_C_prime = C2 - C1

    # Calculate a_prime and h_prime
    a1_prime = a1 + (a1 / 2) * (1 - np.sqrt((C_bar**7) / (C_bar**7 + 25**7)))
    a2_prime = a2 + (a2 / 2) * (1 - np.sqrt((C_bar**7) / (C_bar**7 + 25**7)))

    C1_prime = np.sqrt(a1_prime**2 + b1**2)
    C2_prime = np.sqrt(a2_prime**2 + b2**2)
    C_bar_prime = (C1_prime + C2_prime) / 2

    # Calculate delta h_prime
    delta_h_prime = b2 - b1
    delta_H_prime = 2 * np.sqrt(C1_prime * C2_prime) * np.sin(delta_h_prime / 2)

    # T
    T = 1 - 0.17 * np.cos(L_bar - 30) + 0.24 * np.cos(2 * L_bar) + \
        0.32 * np.cos(3 * L_bar + 6) - 0.20 * np.cos(4 * L_bar - 63)

    # Delta E 2000
    delta_E = np.sqrt(
        (delta_L_prime / kL)**2 +
        (delta_C_prime / kC)**2 +
        (delta_H_prime / kH)**2 +
        T
    )

    return float(delta_E)

# 各色のxy値を辞書形式で定義（日本語の色名を使用）
colors = {
    "赤": (0.587, 0.328),
    "赤紫": (0.498, 0.275),
    "ピンク": (0.379, 0.205),
    "紫": (0.266, 0.138),
    "青紫": (0.215, 0.128),
    "青": (0.218, 0.252),
    "青緑": (0.263, 0.379),
    "緑": (0.297, 0.473),
    "黄緑": (0.376, 0.504),
    "黄": (0.432, 0.464),
    "黄赤": (0.549, 0.378),
    "灰色": (0.326, 0.332),  # 灰色も追加
}

# xy値をLab値に変換する関数
def xy_to_lab(x, y, Y=1.0, illuminant="d65"):
    # xy値からXYZに変換
    X = (Y / y) * x
    Z = (Y / y) * (1 - x - y)
    xyz_color = xyYColor(X, Y, Z)
    # XYZからLabに変換
    lab_color = convert_color(xyz_color, LabColor, target_illuminant=illuminant)
    return lab_color

# 色差を計算する関数
def calculate_color_difference(lab1, lab2):
    return delta_e_cie2000(lab1, lab2)

# 隣り合う色の色差を計算
results = []
ordered_colors = ["赤", "赤紫", "ピンク", "紫", "青紫", "青", "青緑", "緑", "黄緑", "黄", "黄赤", "赤"]  # 順序
for i in range(len(ordered_colors) - 1):
    color1 = ordered_colors[i]
    color2 = ordered_colors[i + 1]
    lab1 = xy_to_lab(*colors[color1])
    lab2 = xy_to_lab(*colors[color2])
    delta_e = calculate_color_difference(lab1, lab2)
    results.append((color1, color2, delta_e))

# 灰色と全ての色の色差を計算
gray_lab = xy_to_lab(*colors["灰色"])
for color, xy in colors.items():
    if color != "灰色":
        lab = xy_to_lab(*xy)
        delta_e = calculate_color_difference(gray_lab, lab)
        results.append(("灰色", color, delta_e))

# 結果を表示
for color1, color2, delta_e in results:
    print(f"ΔE between {color1} and {color2}: {delta_e:.2f}")
