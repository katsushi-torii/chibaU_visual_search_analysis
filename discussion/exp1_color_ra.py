import pandas as pd
import statsmodels.api as sm

# --- 1. ファイルの読み込み ---
advancement_path = "./csv/cleaned/exp1.csv"
mean_std_path = "./csv/colors/mean_std.csv"

advancement = pd.read_csv(advancement_path)
mean_std = pd.read_csv(mean_std_path, index_col=0)

# 列名の設定
mean_std.columns = [
    "輝度[cd/m2]", "放射輝度[mW/sr.m2]", "色度 x", "色度 y", "色度 u'", "色度 v'",
    "主波長[nm]", "刺激純度[%]", "相関色温度[K]", "Δuv", "ピーク波長", "ピーク値",
    "輝度[cd/m2] (SD)", "放射輝度[mW/sr.m2] (SD)", "色度 x (SD)", "色度 y (SD)",
    "色度 u' (SD)", "色度 v' (SD)", "主波長[nm] (SD)", "刺激純度[%] (SD)",
    "相関色温度[K] (SD)", "Δuv (SD)", "ピーク波長 (SD)", "ピーク値 (SD)"
]

# 必要な色の定義
valid_colors = [
    "gray", "red", "green", "blue", "yellow", "purple", "pink",
    "yellow-red", "yellow-green", "blue-green", "purple-blue", "red-purple"
]

# データ整合性の確認
if any(color not in mean_std.index for color in valid_colors):
    raise ValueError("mean_stdに12色が揃っていません。")

if any(color not in advancement["color"].values for color in valid_colors):
    raise ValueError("advancementに12色が揃っていません。")

# データの結合
advancement = advancement[["color", "total"]].set_index("color")
psychological_features = mean_std.loc[valid_colors]
data = advancement.join(psychological_features, how="inner")

# --- 数値型への変換 ---
data = data.apply(pd.to_numeric, errors="coerce")

# --- 単回帰分析をループで実行 ---
results = []
for feature in [
    "輝度[cd/m2]", "放射輝度[mW/sr.m2]", "色度 x", "色度 y", "色度 u'", "色度 v'",
    "主波長[nm]", "刺激純度[%]", "相関色温度[K]", "Δuv", "ピーク波長", "ピーク値"
]:
    # 特殊処理: 主波長の負の値を除外
    if feature == "主波長[nm]":
        filtered_data = data[data[feature] >= 0]
    else:
        filtered_data = data

    X = filtered_data[[feature]]  # 説明変数
    y = filtered_data["total"]  # 目的変数

    # 定数項を追加
    X = sm.add_constant(X)

    # 回帰モデルを作成
    model = sm.OLS(y, X).fit()

    # 必要な値を保存
    r_squared = model.rsquared  # 決定係数
    coef = model.params[feature]  # 回帰係数
    p_value = model.pvalues[feature]  # p値

    results.append({
        "feature": feature,
        "R-squared": r_squared,
        "coefficient": coef,
        "p-value": p_value
    })

# --- 結果を表示 ---
print("\n========== 各特性値の単回帰分析結果 ==========")
for result in results:
    print(f"特性: {result['feature']}\n  決定係数 (R-squared): {result['R-squared']:.3f}\n  回帰係数: {result['coefficient']:.3f}\n  p値: {result['p-value']:.3f}\n")
