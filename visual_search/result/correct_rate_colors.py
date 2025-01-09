# 刺激数６と８それぞれで各被験者の色ごとの正解率（パーセント）を計算

import pandas as pd

# ファイルリスト
file_list = [f"./csv/main/answers_subject{i}.csv" for i in range(1, 8)]

# 刺激数6と8のデータを格納する辞書
accuracy_results = {6: {}, 8: {}}

# 小数点以下を指定する桁数
ROUND_DECIMALS = 2

# ファイルごとに処理
for i, file_path in enumerate(file_list):
    try:
        # データの読み込み
        df = pd.read_csv(file_path)

        # 必要な列の整備
        df["correct"] = pd.to_numeric(df["correct"], errors="coerce")
        df["targetAmount"] = pd.to_numeric(df["targetAmount"], errors="coerce")  # 数値型に変換

        # targetAmountが6と8の場合に分けて集計
        for target_amount in [6, 8]:
            # 該当するデータを抽出
            filtered_df = df[df["targetAmount"] == target_amount]

            # 色ごとの正解率を計算（パーセントに変換）
            color_accuracy = (
                filtered_df.groupby("answer")["correct"]
                .mean()  # 正解率を計算
                .mul(100)  # パーセントに変換
                .round(ROUND_DECIMALS)  # 小数点以下を丸める
            )

            # データを辞書に格納
            for color, accuracy in color_accuracy.items():
                if color not in accuracy_results[target_amount]:
                    accuracy_results[target_amount][color] = {}
                accuracy_results[target_amount][color][f"被験者_{i + 1}_accuracy"] = (
                    f"{accuracy:.2f}%" if not pd.isna(accuracy) else None
                )

    except FileNotFoundError:
        print(f"ファイルが見つかりません: {file_path}")
    except Exception as e:
        print(f"エラーが発生しました（被験者_{i + 1}）: {e}")

# 結果をデータフレームに変換してCSVに保存
for target_amount, data in accuracy_results.items():
    df = pd.DataFrame(data).transpose()
    output_csv_path = f"./accuracy_rates_{target_amount}.csv"
    df.to_csv(output_csv_path, index_label="色名")
    print(f"刺激数{target_amount}のデータをCSVに出力しました: {output_csv_path}")
