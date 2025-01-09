import pandas as pd
import statsmodels.api as sm

# ファイルパス
reaction_time_6_path = "./csv/cleaned/reaction_times_6.csv"
reaction_time_8_path = "./csv/cleaned/reaction_times_8.csv"
accuracy_6_path = "./csv/cleaned/accuracy_rates_6.csv"
exp1_path = "./csv/cleaned/exp1.csv"

# データの読み込み
reaction_time_6 = pd.read_csv(reaction_time_6_path).rename(columns={"色名": "color"}).set_index("color")
reaction_time_8 = pd.read_csv(reaction_time_8_path).rename(columns={"色名": "color"}).set_index("color")
accuracy_6 = pd.read_csv(accuracy_6_path).rename(columns={"色名": "color"}).set_index("color")
exp1 = pd.read_csv(exp1_path).set_index("color")["total"]

# 正解率が文字列型の場合、数値型に変換
for col in accuracy_6.columns:
    accuracy_6[col] = accuracy_6[col].str.rstrip('%').astype(float) / 100  # パーセントを小数に変換

# 対象被験者の設定
selected_subjects_rt = {
    "SG1": ["被験者_1_mean", "被験者_7_mean"],
    "SG2": ["被験者_3_mean", "被験者_7_mean"]
}
selected_subjects_acc = ["被験者_1_accuracy"]  # 正解率のみ対象

# 単回帰分析用関数
def perform_regression(exp1, dependent_var):
    # データを結合し、数値型のみを保持
    data = pd.concat([exp1, dependent_var], axis=1).dropna()
    data.columns = ["total", "dependent"]
    X = sm.add_constant(data["total"])  # 定数項を追加
    y = data["dependent"]
    model = sm.OLS(y, X).fit()
    return {
        "coefficient": model.params["total"],
        "p_value": model.pvalues["total"],
        "r_squared": model.rsquared,
    }

# 反応時間と進出度の回帰分析
print("反応時間と進出度の回帰分析結果:")
for group, subjects in selected_subjects_rt.items():
    for subject in subjects:
        dependent_var = reaction_time_6[subject] if group == "SG2" else reaction_time_8[subject]
        result = perform_regression(exp1, dependent_var)
        print(f"グループ: {group}, 被験者: {subject}, 結果: {result}")

# 正解率と進出度の回帰分析
print("\n正解率と進出度の回帰分析結果:")
for subject in selected_subjects_acc:
    dependent_var = accuracy_6[subject]
    result = perform_regression(exp1, dependent_var)
    print(f"被験者: {subject}, 結果: {result}")
