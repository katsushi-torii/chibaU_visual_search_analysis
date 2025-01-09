#ターゲット色が呈示されているときのペア色：呈示されているvs呈示されていない

import pandas as pd
import statsmodels.api as sm
import numpy as np
from scipy.stats import ttest_ind

# ファイルリスト（被験者データ）
file_list = [f"./csv/main/answers_subject{i}.csv" for i in range(1, 8)]

# ペアの定義
pairs = [
    ("red-purple", "pink"),
    ("green", "blue-green"),
    ("purple", "pink"),
    ("purple-blue", "purple"),
    ("red", "red-purple"),
    ("yellow", "yellow-green"),
]

# 小数点以下の桁数
ROUND_DECIMALS = 2
ROUND_DECIMALS_TSTAT_PVALUE = 3

# 全データを統合
all_data = []
for file_path in file_list:
    try:
        df = pd.read_csv(file_path)
        all_data.append(df)
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {file_path}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

# データを結合
if all_data:
    df = pd.concat(all_data, ignore_index=True)

    # 必要な列を数値型に変換
    df["responseTime"] = pd.to_numeric(df["responseTime"], errors="coerce")
    df["targetAmount"] = pd.to_numeric(df["targetAmount"], errors="coerce")

    # ターゲット有りの試行を抽出
    df_filtered = df[df["answerId"] != -1].copy()

    # 刺激数ごとに分けて処理
    target_amounts = [6, 8]
    results_all = {}

    for target_amount in target_amounts:
        df_target = df_filtered[df_filtered["targetAmount"] == target_amount].copy()
        results = []

        for pair in pairs:
            # 条件ごとの分類
            def classify_condition(row):
                colors_set = set(row["colors"].split("|"))
                if row["answer"] == pair[0]:
                    if pair[1] in colors_set:
                        return "target_pair_present"
                    else:
                        return "target_pair_absent"
                elif row["answer"] == pair[1]:
                    if pair[0] in colors_set:
                        return "pair_target_present"
                    else:
                        return "pair_target_absent"
                return None

            df_target["condition"] = df_target.apply(classify_condition, axis=1)

            # 条件が None でないデータを抽出
            df_target_valid = df_target[df_target["condition"].notna()].copy()

            # 線形モデルによる補正
            X = pd.get_dummies(df_target_valid["targetAmount"], drop_first=True)
            X = sm.add_constant(X)
            y = df_target_valid["responseTime"]

            # 明示的に数値型へ変換
            X = np.asarray(X, dtype=float)
            y = np.asarray(y, dtype=float)

            model = sm.OLS(y, X).fit()

            # 補正後の反応時間を計算
            df_target_valid["corrected_responseTime"] = df_target_valid["responseTime"]

            # 条件ごとの統計量を計算
            summary = (
                df_target_valid.groupby("condition")["corrected_responseTime"]
                .agg(["mean", "std", "count"])
                .reset_index()
            )
            summary["pair"] = f"{pair[0]}-{pair[1]}"
            summary["targetAmount"] = target_amount

            # 有意差検定
            target_pair_present = df_target_valid[df_target_valid["condition"] == "target_pair_present"]["corrected_responseTime"]
            target_pair_absent = df_target_valid[df_target_valid["condition"] == "target_pair_absent"]["corrected_responseTime"]
            pair_target_present = df_target_valid[df_target_valid["condition"] == "pair_target_present"]["corrected_responseTime"]
            pair_target_absent = df_target_valid[df_target_valid["condition"] == "pair_target_absent"]["corrected_responseTime"]

            t_stat_1, p_value_1 = ttest_ind(target_pair_present, target_pair_absent, equal_var=False)
            t_stat_2, p_value_2 = ttest_ind(pair_target_present, pair_target_absent, equal_var=False)

            summary["t_stat_target"] = [
                round(t_stat_1, ROUND_DECIMALS_TSTAT_PVALUE) if cond.startswith("target_pair") else round(t_stat_2, ROUND_DECIMALS_TSTAT_PVALUE)
                for cond in summary["condition"]
            ]
            summary["p_value_target"] = [
                round(p_value_1, ROUND_DECIMALS_TSTAT_PVALUE) if cond.startswith("target_pair") else round(p_value_2, ROUND_DECIMALS_TSTAT_PVALUE)
                for cond in summary["condition"]
            ]

            # 結果を格納
            results.append(summary)

        # 全ペアの結果を結合
        final_results = pd.concat(results, ignore_index=True)

        # 小数点以下の桁数を制限
        final_results["mean"] = final_results["mean"].round(ROUND_DECIMALS)
        final_results["std"] = final_results["std"].round(ROUND_DECIMALS)
        final_results["t_stat_target"] = final_results["t_stat_target"].round(ROUND_DECIMALS_TSTAT_PVALUE)
        final_results["p_value_target"] = final_results["p_value_target"].round(ROUND_DECIMALS_TSTAT_PVALUE)

        # 結果を格納
        results_all[target_amount] = final_results

    # 結果を表示
    for target_amount, result in results_all.items():
        print(f"\n刺激数 {target_amount} の結果:")
        print(result)
else:
    print("全ファイルが読み込めなかったため、分析を実行できません。")
