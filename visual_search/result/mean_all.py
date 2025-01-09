import pandas as pd

# ファイルパスのテンプレート
file_template = "./csv/main/answers_subject{}.csv"

# すべてのデータを格納するリスト
all_data = []

# ファイルをループ処理してデータを結合
for subject_id in range(1, 8):
    # ファイルパスを生成
    file_path = file_template.format(subject_id)
    
    # CSVファイルを読み込み
    df = pd.read_csv(file_path)
    
    # データをリストに追加
    all_data.append(df)

# 全体データフレームを作成
all_df = pd.concat(all_data, ignore_index=True)

# 全体の計算
mean_response_time_all = all_df['responseTime'].mean()
std_response_time_all = all_df['responseTime'].std()

# targetAmount=6 の場合の計算
target_6 = all_df[all_df['targetAmount'] == 6]
mean_response_time_6 = target_6['responseTime'].mean()
std_response_time_6 = target_6['responseTime'].std()

# targetAmount=8 の場合の計算
target_8 = all_df[all_df['targetAmount'] == 8]
mean_response_time_8 = target_8['responseTime'].mean()
std_response_time_8 = target_8['responseTime'].std()

# 結果を表示
print("=== 全体の結果 ===")
print(f"全体の平均: {mean_response_time_all:.2f}, 標準偏差: {std_response_time_all:.2f}")
print("\n=== targetAmount=6 の結果 ===")
print(f"平均: {mean_response_time_6:.2f}, 標準偏差: {std_response_time_6:.2f}")
print("\n=== targetAmount=8 の結果 ===")
print(f"平均: {mean_response_time_8:.2f}, 標準偏差: {std_response_time_8:.2f}")
