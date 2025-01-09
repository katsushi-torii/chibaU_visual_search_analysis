import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import f_oneway

# 日本語フォント設定
plt.rcParams['font.family'] = 'Yu Gothic'

# ファイルリスト
file_list = [f"./csv/main/answers_subject{i}.csv" for i in range(1, 8)]

# 刺激数とターゲット有無のデータを格納する辞書
results = {6: {"target_present": [], "target_absent": []}, 8: {"target_present": [], "target_absent": []}}
correct_results = {6: {"target_present": [], "target_absent": []}, 8: {"target_present": [], "target_absent": []}}

# データ処理
for i, file_path in enumerate(file_list):
    try:
        # データの読み込み
        df = pd.read_csv(file_path)

        # 必要な列の整備
        df["responseTime"] = pd.to_numeric(df["responseTime"], errors="coerce")
        df["targetAmount"] = pd.to_numeric(df["targetAmount"], errors="coerce")
        df["answerId"] = pd.to_numeric(df["answerId"], errors="coerce")
        df["correct"] = pd.to_numeric(df["correct"], errors="coerce")

        # ターゲット有無を判定する列を追加
        df["target_present"] = df["answerId"] != -1

        # 刺激数とターゲットの有無でデータを分けて処理
        for target_amount in [6, 8]:
            for target_status, group_name in [(True, "target_present"), (False, "target_absent")]:
                # 該当するデータを抽出
                filtered_df = df[(df["targetAmount"] == target_amount) & (df["target_present"] == target_status)]

                # 反応時間をリストに保存
                results[target_amount][group_name].extend(filtered_df["responseTime"].dropna().tolist())

                # 正解率をリストに保存
                correct_results[target_amount][group_name].extend(filtered_df["correct"].dropna().tolist())

    except FileNotFoundError:
        print(f"ファイルが見つかりません: {file_path}")
    except Exception as e:
        print(f"エラーが発生しました（被験者_{i + 1}）: {e}")

# 刺激数ごとの全体平均と標準偏差、正解率を計算
summary_results = {6: {"target_present": {}, "target_absent": {}}, 8: {"target_present": {}, "target_absent": {}}}
for target_amount, target_data in results.items():
    for target_status, times in target_data.items():
        if len(times) > 0:  # データがある場合のみ計算
            mean = np.mean(times)
            std = np.std(times, ddof=1)  # 標本標準偏差
            accuracy = np.mean(correct_results[target_amount][target_status]) * 100  # 正解率（%）
            count = len(times)  # データ数
            summary_results[target_amount][target_status] = {"mean": mean, "std": std, "accuracy": accuracy, "count": count}


