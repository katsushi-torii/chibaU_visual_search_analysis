import pandas as pd

# === 1. ファイルパス ===
reaction_time_6_path = "./csv/cleaned/reaction_times_total_6.csv"
reaction_time_8_path = "./csv/cleaned/reaction_times_total_8.csv"
mean_std_path = "./csv/colors/mean_std.csv"

# === 2. データの読み込み ===
reaction_time_6 = pd.read_csv(reaction_time_6_path)
reaction_time_8 = pd.read_csv(reaction_time_8_path)
mean_std = pd.read_csv(mean_std_path, index_col=0)

# === 3. 列名を再設定（すべての24列を考慮） ===
mean_std.columns = [
    "輝度[cd/m2]", "放射輝度[mW/sr.m2]", "色度 x", "色度 y", "色度 u'", "色度 v'",
    "主波長[nm]", "刺激純度[%]", "相関色温度[K]", "Δuv", "ピーク波長", "ピーク値",
    "輝度[cd/m2] (SD)", "放射輝度[mW/sr.m2] (SD)", "色度 x (SD)", "色度 y (SD)",
    "色度 u' (SD)", "色度 v' (SD)", "主波長[nm] (SD)", "刺激純度[%] (SD)",
    "相関色温度[K] (SD)", "Δuv (SD)", "ピーク波長 (SD)", "ピーク値 (SD)"
]

# === 4. 12色の定義 (blue-purple → purple-blueに修正済) ===
valid_colors = [
    "gray", "red", "green", "blue", "yellow", "purple", "pink",
    "yellow-red", "yellow-green", "blue-green", "purple-blue", "red-purple"
]

# === 5. 平均値のみを抽出する列 ===
mean_columns = [
    "輝度[cd/m2]", "放射輝度[mW/sr.m2]", "色度 x", "色度 y", "色度 u'", "色度 v'",
    "主波長[nm]", "刺激純度[%]", "相関色温度[K]", "Δuv", "ピーク波長", "ピーク値"
]

# -----------------------------------------------------------------------------
#  (A) mean_std の確認
# -----------------------------------------------------------------------------
missing_in_mean_std = [c for c in valid_colors if c not in mean_std.index]
if missing_in_mean_std:
    print("【警告】mean_std から以下の色が見つかりません:", missing_in_mean_std)
else:
    print("mean_std には12色すべてが含まれています。")

# mean_stdから12色のみ抽出
psychological_features = mean_std.loc[valid_colors, mean_columns]

# -----------------------------------------------------------------------------
#  (B) reaction_time_6, reaction_time_8 の確認
# -----------------------------------------------------------------------------
missing_in_reaction_time_6 = [c for c in valid_colors if c not in reaction_time_6["color"].unique()]
if missing_in_reaction_time_6:
    print("【警告】reaction_time_6 に以下の色が含まれていません:", missing_in_reaction_time_6)
else:
    print("reaction_time_6 にも12色すべてが含まれています。")

missing_in_reaction_time_8 = [c for c in valid_colors if c not in reaction_time_8["color"].unique()]
if missing_in_reaction_time_8:
    print("【警告】reaction_time_8 に以下の色が含まれていません:", missing_in_reaction_time_8)
else:
    print("reaction_time_8 にも12色すべてが含まれています。")

# 必要な列を抽出して、colorをインデックスに
reaction_time_6 = reaction_time_6[["color", "mean"]].set_index("color")
reaction_time_8 = reaction_time_8[["color", "mean"]].set_index("color")

# -----------------------------------------------------------------------------
#  (C) 結合
# -----------------------------------------------------------------------------
data_6 = reaction_time_6.join(psychological_features, how="inner")
data_8 = reaction_time_8.join(psychological_features, how="inner")

# 結合後のデータが12色揃っているか確認
if len(data_6) < 12:
    print(f"【警告】data_6 の結合後の行数: {len(data_6)} (12色すべてではない可能性があります)")
else:
    print("data_6 の結合後データにも12色すべてが揃っています。")

if len(data_8) < 12:
    print(f"【警告】data_8 の結合後の行数: {len(data_8)} (12色すべてではない可能性があります)")
else:
    print("data_8 の結合後データにも12色すべてが揃っています。")

# -----------------------------------------------------------------------------
#  (D) 主波長列を数値に変換 & 負値除外
# -----------------------------------------------------------------------------
data_6["主波長[nm]"] = pd.to_numeric(data_6["主波長[nm]"], errors="coerce")
data_8["主波長[nm]"] = pd.to_numeric(data_8["主波長[nm]"], errors="coerce")

data_6_no_negative = data_6[data_6["主波長[nm]"] >= 0]
data_8_no_negative = data_8[data_8["主波長[nm]"] >= 0]

# -----------------------------------------------------------------------------
#  (E) 相関係数計算の関数
# -----------------------------------------------------------------------------
def calculate_correlations(data, specific_feature=None):
    """
    data: データフレーム
    specific_feature: 特定の列だけを対象にする場合はその列名(文字列)を指定
                      None の場合は mean_columns 全体に対して計算する
    """
    correlations = {}
    features = [specific_feature] if specific_feature else mean_columns
    for feature in features:
        correlation = data["mean"].corr(data[feature])
        correlations[feature] = round(correlation, 2)
    return correlations

# 全データでの相関係数
correlations_6 = calculate_correlations(data_6)
correlations_8 = calculate_correlations(data_8)

# 主波長の負値を除外したデータでの相関係数（主波長のみ）
correlations_6_no_negative_wavelength = calculate_correlations(
    data_6_no_negative, 
    specific_feature="主波長[nm]"
)
correlations_8_no_negative_wavelength = calculate_correlations(
    data_8_no_negative, 
    specific_feature="主波長[nm]"
)

# -----------------------------------------------------------------------------
#  (F) 結果の表示
# -----------------------------------------------------------------------------
print("\n===== 刺激数6の反応時間と心理量の相関係数 (全データ) =====")
for feature, corr in correlations_6.items():
    print(f"{feature}: {corr}")

print("\n===== 刺激数8の反応時間と心理量の相関係数 (全データ) =====")
for feature, corr in correlations_8.items():
    print(f"{feature}: {corr}")

print("\n===== 刺激数6の反応時間と主波長の相関係数 (主波長<0を除外) =====")
for feature, corr in correlations_6_no_negative_wavelength.items():
    print(f"{feature}: {corr}")

print("\n===== 刺激数8の反応時間と主波長の相関係数 (主波長<0を除外) =====")
for feature, corr in correlations_8_no_negative_wavelength.items():
    print(f"{feature}: {corr}")
