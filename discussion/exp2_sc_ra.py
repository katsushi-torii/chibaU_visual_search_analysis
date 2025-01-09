import pandas as pd
from sklearn.linear_model import LinearRegression
from scipy.stats import linregress

# CSVファイルのパスを指定
file_reaction_6 = './csv/cleaned/reaction_times_total_6.csv'
file_reaction_8 = './csv/cleaned/reaction_times_total_8.csv'
file_accuracy_6 = './csv/cleaned/accuracy_total_6.csv'
file_accuracy_8 = './csv/cleaned/accuracy_total_8.csv'

# 類似性データ
similarity_counts = {
    'single': {'pink': 5, 'purple': 4, 'red-purple': 4, 'blue-green': 3, 'green': 3, 'purple-blue': 2, 'yellow': 1, 'yellow-green': 1, 'red': 1}
}

# 平均反応時間または正解率を計算する関数
def calculate_means(data, value_column):
    means = {}
    for _, row in data.iterrows():
        color_name = row['color']
        mean_value = row[value_column]
        means[color_name] = mean_value
    return means

# 単回帰分析を行う関数
def perform_regression(x, y):
    # 線形回帰を計算
    slope, intercept, r_value, p_value, _ = linregress(x, y)
    return {
        'Coefficient': slope,
        'Intercept': intercept,
        'R_squared': r_value ** 2,
        'P_value': p_value
    }

# シングルデータに基づく回帰分析を計算する関数
def calculate_single_regression(file_reaction, file_accuracy, similarity_counts):
    # ファイルを読み込む
    reaction_times = pd.read_csv(file_reaction)
    accuracy = pd.read_csv(file_accuracy)

    # 列名を確認して必要に応じて修正
    if 'color' not in reaction_times.columns or 'color' not in accuracy.columns:
        print("Columns in Reaction CSV:", reaction_times.columns)
        print("Columns in Accuracy CSV:", accuracy.columns)
        raise KeyError("The expected column 'color' was not found in one of the CSV files.")

    # 平均反応時間と正解率を計算
    reaction_means = calculate_means(reaction_times, 'mean')
    accuracy_means = calculate_means(accuracy, 'accuracy')

    # 全色リストを作成
    all_colors = list(set(reaction_means.keys()).union(set(accuracy_means.keys())))

    # 類似性スコアと反応時間の対応
    similarity_scores = [similarity_counts['single'].get(color, 0) for color in all_colors]
    reaction_values = [reaction_means.get(color, 0) for color in all_colors]
    accuracy_values = [accuracy_means.get(color, 0) for color in all_colors]

    # 回帰分析
    reaction_regression = perform_regression(similarity_scores, reaction_values)
    accuracy_regression = perform_regression(similarity_scores, accuracy_values)

    return reaction_regression, accuracy_regression

# 使用例
reaction_reg_6, accuracy_reg_6 = calculate_single_regression(file_reaction_6, file_accuracy_6, similarity_counts)
reaction_reg_8, accuracy_reg_8 = calculate_single_regression(file_reaction_8, file_accuracy_8, similarity_counts)

# 結果を出力
print("Stimulus 6 - Reaction Time Regression:", reaction_reg_6)
print("Stimulus 6 - Accuracy Regression:", accuracy_reg_6)
print("Stimulus 8 - Reaction Time Regression:", reaction_reg_8)
print("Stimulus 8 - Accuracy Regression:", accuracy_reg_8)
