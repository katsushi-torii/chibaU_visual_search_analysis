import pandas as pd

# --- 1. ファイルパスの指定 ---
advancement_path = "./csv/cleaned/exp1.csv"
mean_std_path = "./csv/colors/mean_std.csv"

# --- 2. データの読み込み ---
advancement = pd.read_csv(advancement_path)
mean_std = pd.read_csv(mean_std_path, index_col=0)

# --- 3. 列名を再設定（すべての24列を考慮） ---
mean_std.columns = [
    "輝度[cd/m2]", "放射輝度[mW/sr.m2]", "色度 x", "色度 y", "色度 u'", "色度 v'",
    "主波長[nm]", "刺激純度[%]", "相関色温度[K]", "Δuv", "ピーク波長", "ピーク値",
    "輝度[cd/m2] (SD)", "放射輝度[mW/sr.m2] (SD)", "色度 x (SD)", "色度 y (SD)",
    "色度 u' (SD)", "色度 v' (SD)", "主波長[nm] (SD)", "刺激純度[%] (SD)",
    "相関色温度[K] (SD)", "Δuv (SD)", "ピーク波長 (SD)", "ピーク値 (SD)"
]

# --- 4. 12色を定義 (blue-purple → purple-blue へ修正済) ---
valid_colors = [
    "gray", "red", "green", "blue", "yellow", "purple", "pink",
    "yellow-red", "yellow-green", "blue-green", "purple-blue", "red-purple"
]

# --- 5. 平均値のみを抽出する列 ---
mean_columns = [
    "輝度[cd/m2]", "放射輝度[mW/sr.m2]", "色度 x", "色度 y", "色度 u'", "色度 v'",
    "主波長[nm]", "刺激純度[%]", "相関色温度[K]", "Δuv", "ピーク波長", "ピーク値"
]

# ========== 追加: mean_std から12色がちゃんと取得できているか確認 ==========

# 5-1. mean_stdに12色すべてが存在するかをチェック
missing_in_mean_std = [c for c in valid_colors if c not in mean_std.index]
if missing_in_mean_std:
    print("【警告】mean_std から以下の色データが見つかりません:", missing_in_mean_std)
else:
    print("mean_std には12色すべてが含まれています。")

# 5-2. mean_std から12色のみ抽出（12色以外は無視）
psychological_features = mean_std.loc[valid_colors, mean_columns]

# --- 6. 進出度データを取得 ---
advancement = advancement[["color", "total"]].set_index("color")

# ========== 追加: advancement から12色がちゃんと存在するか確認 ==========

missing_in_advancement = [c for c in valid_colors if c not in advancement.index]
if missing_in_advancement:
    print("【警告】advancement(進出度データ) に以下の色が含まれていません:", missing_in_advancement)
else:
    print("進出度データにも12色すべてが含まれています。")

# --- 7. データを結合 ---
data = advancement.join(psychological_features, how="inner")
# how="inner" を使うと、両方に存在する color だけが残る

# ========== 追加: 結合結果に12色が揃っているか確認 ==========
if len(data) < 12:
    print(f"【警告】結合後のデータ数が {len(data)} 行になっています。12色すべてではない可能性があります。")
else:
    print("結合後のデータにも12色すべてが揃っています。")

# --- 8. 主波長列を数値に変換（エラー防止のため） ---
data["主波長[nm]"] = pd.to_numeric(data["主波長[nm]"], errors="coerce")

# --- 9. 主波長の値が負の行を除外 ---
data_no_negative = data[data["主波長[nm]"] >= 0]

# --- 10. 各心理量と進出度の相関係数を計算 ---
def calculate_correlations(data):
    correlations = {}
    for feature in mean_columns:
        correlation = data["total"].corr(data[feature])
        correlations[feature] = round(correlation, 2)
    return correlations

# 全データでの相関係数
correlations = calculate_correlations(data)

# 主波長の負値を除外したデータでの相関係数（主波長のみ）
def calculate_correlation_for_wavelength(data):
    if "主波長[nm]" in data.columns:
        correlation = data["total"].corr(data["主波長[nm]"])
        return round(correlation, 2)
    return None

correlation_no_negative_wavelength = calculate_correlation_for_wavelength(data_no_negative)

# --- 11. 結果を表示 ---
print("\n========== 相関係数の結果 ==========")
print("■ 進出度と心理量の相関係数 (全データ):")
for feature, corr in correlations.items():
    print(f"{feature}: {corr}")

print("\n■ 進出度と主波長の相関係数 (主波長<0を除外したデータ):")
print(f"主波長[nm]: {correlation_no_negative_wavelength}")
