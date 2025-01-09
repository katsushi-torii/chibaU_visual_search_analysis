#ターゲットの位置の違いによる有意差を検証

import pandas as pd
import os
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.formula.api import mixedlm

# CSVファイルパスのフォーマット
base_path = "./csv/same/answerssame_subject"
subjects = [f"{base_path}{i}.csv" for i in range(1, 8)]

# 結果を格納するリスト
individual_results = []
overall_results = []

# 被験者ごとの分析
for subject in subjects:
    # データの読み込み
    df = pd.read_csv(subject)
    
    for target_amount in [6, 8]:
        # targetAmountごとにデータをフィルタリング
        subset = df[df['targetAmount'] == target_amount]
        
        if subset.empty:
            continue
        
        # ANOVAによる位置(answerId)ごとの有意差の検定
        model = ols('responseTime ~ C(answerId)', data=subset).fit()
        anova_table = sm.stats.anova_lm(model, typ=2)
        individual_results.append({
            "subject": subject,
            "targetAmount": target_amount,
            "anova_table": anova_table
        })
        
        print(f"Subject: {subject}, TargetAmount: {target_amount}")
        print(anova_table)

# 全体のデータを統合
all_data = pd.concat([pd.read_csv(subject) for subject in subjects], ignore_index=True)

# targetAmountごとの全体分析
for target_amount in [6, 8]:
    subset = all_data[all_data['targetAmount'] == target_amount]
    
    if subset.empty:
        continue
    
    # 線形混合モデル
    model = mixedlm("responseTime ~ C(answerId)", subset, groups=subset["id"]).fit()
    overall_results.append({
        "targetAmount": target_amount,
        "model_summary": model.summary()
    })
    
    print(f"Overall Analysis, TargetAmount: {target_amount}")
    print(model.summary())
