import pandas as pd
import statsmodels.api as sm

# === 1. ファイルパス ===
accuracy_6_path = "./csv/cleaned/accuracy_total_6.csv"
accuracy_8_path = "./csv/cleaned/accuracy_total_8.csv"
mean_std_path = "./csv/colors/mean_std.csv"

# === 2. データの読み込み ===
accuracy_6 = pd.read_csv(accuracy_6_path)
accuracy_8 = pd.read_csv(accuracy_8_path)
mean_std = pd.read_csv(mean_std_path, index_col=0)

# === 3. 列名を再設定 ===
mean_std.columns = [
    "輝度[cd/m2]", "放射輝度[mW/sr.m2]", "色度 x", "色度 y", "色度 u'", "色度 v'",
    "主波長[nm]", "刺激純度[%]", "相関色温度[K]", "Δuv", "ピーク波長", "ピーク値",
    "輝度[cd/m2] (SD)", "放射輝度[mW/sr.m2] (SD)", "色度 x (SD)", "色度 y (SD)",
    "色度 u' (SD)", "色度 v' (SD)", "主波長[nm] (SD)", "刺激純度[%] (SD)",
    "相関色温度[K] (SD)", "Δuv (SD)", "ピーク波長 (SD)", "ピーク値 (SD)"
]

# === 4. 必要な色の定義 ===
valid_colors = [
    "gray", "red", "green", "blue", "yellow", "purple", "pink",
    "yellow-red", "yellow-green", "blue-green", "purple-blue", "red-purple"
]

# === 5. データ整合性の確認 ===
if any(color not in mean_std.index for color in valid_colors):
    raise ValueError("mean_stdに12色が揃っていません。")

if any(color not in accuracy_6["color"].values for color in valid_colors):
    raise ValueError("accuracy_6に12色が揃っていません。")

if any(color not in accuracy_8["color"].values for color in valid_colors):
    raise ValueError("accuracy_8に12色が揃っていません。")

# === 6. データの結合 ===
accuracy_6 = accuracy_6[["color", "accuracy"]].set_index("color")
accuracy_8 = accuracy_8[["color", "accuracy"]].set_index("color")
psychological_features = mean_std.loc[valid_colors]

data_6 = accuracy_6.join(psychological_features, how="inner")
data_8 = accuracy_8.join(psychological_features, how="inner")

# 数値型への変換
data_6 = data_6.apply(pd.to_numeric, errors="coerce")
data_8 = data_8.apply(pd.to_numeric, errors="coerce")

# === 7. 単回帰分析 ===
def perform_regression(data, target):
    results = []
    for feature in [
        "輝度[cd/m2]", "放射輝度[mW/sr.m2]", "色度 x", "色度 y", "色度 u'", "色度 v'",
        "主波長[nm]", "刺激純度[%]", "相関色温度[K]", "Δuv", "ピーク波長", "ピーク値"
    ]:
        # 特殊処理: 主波長の負値を除外
        if feature == "主波長[nm]":
            filtered_data = data[data[feature] >= 0]
        else:
            filtered_data = data

        X = filtered_data[[feature]]  # 説明変数
        y = filtered_data[target]  # 目的変数

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
    return results

# 刺激数6の回帰分析
results_6 = perform_regression(data_6, target="accuracy")

# 刺激数8の回帰分析
results_8 = perform_regression(data_8, target="accuracy")

# === 8. 結果の表示 ===
print("\n========== 刺激数6: 各特性値の単回帰分析結果 ==========")
for result in results_6:
    print(f"特性: {result['feature']}")
    print(f"  決定係数 (R-squared): {result['R-squared']:.3f}")
    print(f"  回帰係数: {result['coefficient']:.3f}")
    print(f"  p値: {result['p-value']:.3f}\n")

print("\n========== 刺激数8: 各特性値の単回帰分析結果 ==========")
for result in results_8:
    print(f"特性: {result['feature']}")
    print(f"  決定係数 (R-squared): {result['R-squared']:.3f}")
    print(f"  回帰係数: {result['coefficient']:.3f}")
    print(f"  p値: {result['p-value']:.3f}\n")
