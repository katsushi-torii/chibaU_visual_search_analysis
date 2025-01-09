#刺激数とターゲット有無が反応時間に与える効果量を検証
from scipy.stats import ttest_ind
import numpy as np
import pandas as pd

# ファイルリスト
file_list = [f"./csv/main/answers_subject{i}.csv" for i in range(1, 8)]

# 効果量を保存する辞書
effect_sizes = {
    "ターゲットの有無_反応時間": {},
    "ターゲット数_反応時間": {},
    "ターゲットの有無_正解数": {},
    "ターゲット数_正解数": {},
}

# 被験者ごとに処理
for file in file_list:
    # データ読み込み
    df = pd.read_csv(file)
    
    # 被験者ID
    subject_id = file.split("_")[-1].split(".")[0]
    
    # 効果量の計算関数
    def calculate_cohens_d(group1, group2):
        mean1, mean2 = group1.mean(), group2.mean()
        std_pooled = np.sqrt((group1.var(ddof=1) + group2.var(ddof=1)) / 2)
        return (mean1 - mean2) / std_pooled

    # ターゲットの有無 (反応時間)
    times_present = df[df["answerId"] != -1]["responseTime"]
    times_absent = df[df["answerId"] == -1]["responseTime"]
    if len(times_present) > 1 and len(times_absent) > 1:  # データが十分にある場合のみ計算
        effect_sizes["ターゲットの有無_反応時間"][subject_id] = calculate_cohens_d(times_present, times_absent)
    
    # ターゲット数 (反応時間)
    if len(df["targetAmount"].unique()) == 2:  # ターゲット数が2条件ある場合
        times_6 = df[df["targetAmount"] == 6]["responseTime"]
        times_8 = df[df["targetAmount"] == 8]["responseTime"]
        if len(times_6) > 1 and len(times_8) > 1:  # データが十分にある場合のみ計算
            effect_sizes["ターゲット数_反応時間"][subject_id] = calculate_cohens_d(times_6, times_8)

    # ターゲットの有無 (正解数)
    correct_present = df[df["answerId"] != -1]["correct"]
    correct_absent = df[df["answerId"] == -1]["correct"]
    if len(correct_present) > 1 and len(correct_absent) > 1:  # データが十分にある場合のみ計算
        effect_sizes["ターゲットの有無_正解数"][subject_id] = calculate_cohens_d(correct_present, correct_absent)
    
    # ターゲット数 (正解数)
    if len(df["targetAmount"].unique()) == 2:  # ターゲット数が2条件ある場合
        correct_6 = df[df["targetAmount"] == 6]["correct"]
        correct_8 = df[df["targetAmount"] == 8]["correct"]
        if len(correct_6) > 1 and len(correct_8) > 1:  # データが十分にある場合のみ計算
            effect_sizes["ターゲット数_正解数"][subject_id] = calculate_cohens_d(correct_6, correct_8)

# 効果量の判定
print("効果量(Cohen's d):")
split_criteria = {}
for factor, subjects in effect_sizes.items():
    print(f"\n--- {factor} ---")
    for subject, effect in subjects.items():
        print(f"被験者_{subject}: {effect:.3f}")

