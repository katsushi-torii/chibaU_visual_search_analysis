#刺激数６と８それぞれで各被験者の色ごとの反応時間を計算

import pandas as pd

# ファイルリスト
file_list = [f"./csv/main/answers_subject{i}.csv" for i in range(1, 8)]

# 刺激数6と8のデータを格納する辞書
results = {6: {}, 8: {}}

# 小数点以下を指定する桁数
ROUND_DECIMALS = 0

# ファイルごとに処理
for i, file_path in enumerate(file_list):
    try:
        # データの読み込み
        df = pd.read_csv(file_path)

        # 必要な列の整備
        df["responseTime"] = pd.to_numeric(df["responseTime"], errors="coerce")
        df["targetAmount"] = pd.to_numeric(df["targetAmount"], errors="coerce")  # 数値型に変換

        # targetAmountが6と8の場合に分けて集計
        for target_amount in [6, 8]:
            # 該当するデータを抽出
            filtered_df = df[df["targetAmount"] == target_amount]

            # 色ごとの反応時間の平均と標準偏差を計算
            color_summary = (
                filtered_df.groupby("answer")["responseTime"]
                .agg(['mean', 'std'])  # 平均と標準偏差を計算
                .round(ROUND_DECIMALS)  # 小数点以下を丸める
            )

            # データを辞書に格納
            for color, stats in color_summary.iterrows():
                if color not in results[target_amount]:
                    results[target_amount][color] = {}
                results[target_amount][color][f"被験者_{i + 1}_mean"] = int(stats['mean']) if not pd.isna(stats['mean']) else None
                results[target_amount][color][f"被験者_{i + 1}_std"] = int(stats['std']) if not pd.isna(stats['std']) else None

    except FileNotFoundError:
        print(f"ファイルが見つかりません: {file_path}")
    except Exception as e:
        print(f"エラーが発生しました（被験者_{i + 1}）: {e}")

# 結果をデータフレームに変換してCSVに保存
for target_amount, data in results.items():
    df = pd.DataFrame(data).transpose()
    output_csv_path = f"./reaction_times_{target_amount}.csv"
    df.to_csv(output_csv_path, index_label="色名")
    print(f"刺激数{target_amount}のデータをCSVに出力しました: {output_csv_path}")
