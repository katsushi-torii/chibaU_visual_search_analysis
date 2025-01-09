import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

# CSVファイルのパスを指定
file_reaction_6 = './csv/cleaned/reaction_times_total_6.csv'
file_reaction_8 = './csv/cleaned/reaction_times_total_8.csv'
file_accuracy_6 = './csv/cleaned/accuracy_total_6.csv'
file_accuracy_8 = './csv/cleaned/accuracy_total_8.csv'

# 類似性データ
similarity_counts = {
    'single': {'pink': 5, 'purple': 4, 'red-purple': 4, 'blue-green': 3, 'green': 3, 'purple-blue': 2, 'yellow': 1, 'yellow-green': 1, 'red': 1}
}

# 各色のRGB値
color_rgb = {
    'red': (227, 0, 38),
    'red-purple': (222, 0, 100),
    'pink': (208, 0, 159),
    'purple': (182, 0, 229),
    'purple-blue': (137, 63, 254),
    'blue': (0, 119, 165),
    'blue-green': (0, 127, 106),
    'green': (0, 129, 63),
    'yellow-green': (91, 123, 0),
    'yellow': (133, 111, 0),
    'yellow-red': (201, 68, 0),
    'gray': (120, 109, 113)
}

# 平均反応時間または正解率を計算する関数
def calculate_means(data, value_column):
    means = {}
    for _, row in data.iterrows():
        color_name = row['color']
        mean_value = row[value_column]
        means[color_name] = mean_value
    return means

# 相関データを準備する関数
def prepare_correlation_data(means, similarity_counts, all_colors):
    # 単体の色（スコアがない場合は0に設定）
    single_color_data = [(color, similarity_counts['single'].get(color, 0), means.get(color, 0)) 
                         for color in all_colors]
    return single_color_data

# シングルデータに基づく相関係数を計算する関数
def calculate_single_correlation(file_reaction, file_accuracy, similarity_counts):
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

    # 相関データを準備（反応時間）
    single_reaction_data = prepare_correlation_data(reaction_means, similarity_counts, all_colors)
    single_reaction_df = pd.DataFrame(single_reaction_data, columns=['Color', 'Similarity_Score', 'Reaction_Time'])
    reaction_correlation = single_reaction_df[['Similarity_Score', 'Reaction_Time']].corr().iloc[0, 1]

    # 相関データを準備（正解率）
    single_accuracy_data = prepare_correlation_data(accuracy_means, similarity_counts, all_colors)
    single_accuracy_df = pd.DataFrame(single_accuracy_data, columns=['Color', 'Similarity_Score', 'Accuracy'])
    accuracy_correlation = single_accuracy_df[['Similarity_Score', 'Accuracy']].corr().iloc[0, 1]

    return single_reaction_df, single_accuracy_df, reaction_correlation, accuracy_correlation

# 散布図を作成する関数
def plot_scatter(df, x_column, y_column, x_label, y_label, y_min, y_max):
    font_path = font_manager.findfont("Yu Gothic")
    plt.rcParams['font.family'] = 'Yu Gothic'

    plt.figure(figsize=(8, 6))
    for i, row in df.iterrows():
        color_name = row['Color']
        rgb = color_rgb.get(color_name, (0, 0, 0))  # デフォルトは黒
        color = tuple(c / 255 for c in rgb)
        plt.scatter(row[x_column], row[y_column], color=color, alpha=0.7, edgecolors='k', s=100)  # 点を大きく
    plt.ylim(y_min, y_max + 2)  # 余白を追加
    plt.xlabel(x_label, fontsize=14)
    plt.ylabel(y_label, fontsize=14)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

# 使用例
reaction_df_6, accuracy_df_6, reaction_corr_6, accuracy_corr_6 = calculate_single_correlation(file_reaction_6, file_accuracy_6, similarity_counts)
reaction_df_8, accuracy_df_8, reaction_corr_8, accuracy_corr_8 = calculate_single_correlation(file_reaction_8, file_accuracy_8, similarity_counts)

print(f"相関係数 (反応時間, 刺激数6): {reaction_corr_6}")
print(f"相関係数 (正解率, 刺激数6): {accuracy_corr_6}")
print(f"相関係数 (反応時間, 刺激数8): {reaction_corr_8}")
print(f"相関係数 (正解率, 刺激数8): {accuracy_corr_8}")

# 散布図の描画
plot_scatter(reaction_df_6, 'Similarity_Score', 'Reaction_Time', "近似色として選ばれた回数", "反応時間 (ms)", 1200, 1750)
plot_scatter(accuracy_df_6, 'Similarity_Score', 'Accuracy', "近似色として選ばれた回数", "正解率 (%)", 75, 100)  # 上限に余白
plot_scatter(reaction_df_8, 'Similarity_Score', 'Reaction_Time', "近似色として選ばれた回数", "反応時間 (ms)", 1200, 1750)
plot_scatter(accuracy_df_8, 'Similarity_Score', 'Accuracy', "近似色として選ばれた回数", "正解率 (%)", 75, 100)  # 上限に余白
