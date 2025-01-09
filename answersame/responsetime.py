import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# 日本語フォントの設定
plt.rcParams['font.family'] = 'Yu Gothic'

# 実験3と実験2のファイルパス
experiment3_base_path = "./csv/same/answerssame_subject"
experiment3_subjects = [f"{experiment3_base_path}{i}.csv" for i in range(1, 8)]

experiment2_base_path = "./csv/main/answers_subject"
experiment2_subjects = [f"{experiment2_base_path}{i}.csv" for i in range(1, 8)]

# 被験者ごとに反応時間を格納するリスト
subject_results = []
for subject in range(1, 8):
    # 実験3データ
    exp3_path = f"./csv/same/answerssame_subject{subject}.csv"
    exp3_data = pd.read_csv(exp3_path)
    
    # 実験2データ
    exp2_path = f"./csv/main/answers_subject{subject}.csv"
    exp2_data = pd.read_csv(exp2_path)
    
    subject_result = {'subject': subject}
    
    # 反応時間を取り出し
    response_times_6_exp3 = exp3_data[exp3_data['targetAmount'] == 6]['responseTime'].values
    response_times_8_exp3 = exp3_data[exp3_data['targetAmount'] == 8]['responseTime'].values
    response_times_6_exp2 = exp2_data[exp2_data['targetAmount'] == 6]['responseTime'].values
    response_times_8_exp2 = exp2_data[exp2_data['targetAmount'] == 8]['responseTime'].values
    
    # 平均反応時間を格納
    subject_result['exp3_6'] = response_times_6_exp3.mean()
    subject_result['exp3_8'] = response_times_8_exp3.mean()
    subject_result['exp2_6'] = response_times_6_exp2.mean()
    subject_result['exp2_8'] = response_times_8_exp2.mean()
    
    # 独立t検定（刺激数6と8の条件ごとに実施）
    t_stat_6, p_value_6 = ttest_ind(response_times_6_exp3, response_times_6_exp2, equal_var=False)
    t_stat_8, p_value_8 = ttest_ind(response_times_8_exp3, response_times_8_exp2, equal_var=False)
    
    print(f"Subject: {subject}, Target Amount: 6")
    print(f"Experiment 3 Mean: {response_times_6_exp3.mean():.2f} ms")
    print(f"Experiment 2 Mean: {response_times_6_exp2.mean():.2f} ms")
    print(f"T-statistic: {t_stat_6:.4f}, P-value: {p_value_6:.15f}")
    
    print(f"Subject: {subject}, Target Amount: 8")
    print(f"Experiment 3 Mean: {response_times_8_exp3.mean():.2f} ms")
    print(f"Experiment 2 Mean: {response_times_8_exp2.mean():.2f} ms")
    print(f"T-statistic: {t_stat_8:.4f}, P-value: {p_value_8:.15f}")
    print("---")
    
    subject_results.append(subject_result)

# 結果をDataFrameに変換
subject_results_df = pd.DataFrame(subject_results)

# 刺激数6のグラフ作成
plt.figure(figsize=(10, 6))
plt.plot(subject_results_df['subject'], subject_results_df['exp3_6'], marker='o', linestyle='-', color='black', label='実験3')
plt.plot(subject_results_df['subject'], subject_results_df['exp2_6'], marker='x', linestyle='--', color='black', label='実験2')
plt.ylabel("平均反応時間 (ms)", fontsize=14)
plt.xticks(subject_results_df['subject'], [f"被験者 {i}" for i in range(1, 8)], fontsize=12)
plt.yticks(fontsize=14)
# 縦軸の範囲を950msから1900msに設定
plt.ylim(950, 1900)

# レジェンドをグラフ内右上に配置
plt.legend(title="実験条件", loc='upper right', fontsize=14)
plt.tight_layout()
plt.show()

# 刺激数8のグラフ作成
plt.figure(figsize=(10, 6))
plt.plot(subject_results_df['subject'], subject_results_df['exp3_8'], marker='o', linestyle='-', color='black', label='実験3')
plt.plot(subject_results_df['subject'], subject_results_df['exp2_8'], marker='x', linestyle='--', color='black', label='実験2')
plt.ylabel("平均反応時間 (ms)", fontsize=14)
plt.xticks(subject_results_df['subject'], [f"被験者 {i}" for i in range(1, 8)], fontsize=12)
plt.yticks(fontsize=14)
# 縦軸の範囲を950msから1900msに設定
plt.ylim(950, 1900)

# レジェンドをグラフ内右上に配置
plt.legend(title="実験条件", loc='upper right', fontsize=14)
plt.tight_layout()
plt.show()
