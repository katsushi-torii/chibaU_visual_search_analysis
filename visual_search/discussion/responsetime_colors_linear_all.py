import statsmodels.api as sm
import pandas as pd

# ファイルリスト
file_list = [f"./csv/main/answers_subject{i}.csv" for i in range(1, 8)]

# 小数点以下を指定する桁数
ROUND_DECIMALS = 2

# 全被験者分の補正後データを格納するリスト
all_corrected_data = []

# ファイルごとに処理
for i, file_path in enumerate(file_list):
    try:
        # データの読み込み
        df = pd.read_csv(file_path)
        
        # 必要な列の整備
        df["responseTime"] = pd.to_numeric(df["responseTime"], errors="coerce")
        df["targetAmount"] = pd.to_numeric(df["targetAmount"], errors="coerce")
        df["target_present"] = df["answerId"].apply(lambda x: "あり" if x != -1 else "なし")
        
        # ダミー変数の作成
        X = pd.get_dummies(df[["targetAmount", "target_present"]], drop_first=True)
        X = sm.add_constant(X)
        X = X.astype(float)

        # 目的変数
        y = df["responseTime"]

        # 線形モデルの構築
        model = sm.OLS(y, X).fit()

        # 各条件の補正値を取得し適用
        df["targetAmount_adjustment"] = df["targetAmount"].apply(
            lambda x: float(model.params.get(f"targetAmount_{int(x)}", 0))
        )
        df["target_present_adjustment"] = df["target_present"].apply(
            lambda x: float(model.params.get(f"target_present_{x}", 0))
        )

        # 補正後の反応時間を計算
        df["corrected_responseTime"] = (
            df["responseTime"]
            - df["targetAmount_adjustment"]
            - df["target_present_adjustment"]
        )
        
        # 被験者の補正後データを格納
        all_corrected_data.append(df[["answer", "corrected_responseTime"]])

    except FileNotFoundError:
        print(f"ファイルが見つかりません: {file_path}")
    except Exception as e:
        print(f"エラーが発生しました（被験者_{i+1}）: {e}")

# 全被験者のデータを統合
if all_corrected_data:
    combined_data = pd.concat(all_corrected_data, ignore_index=True)
    
    # 色ごとの全体平均と標準偏差を計算
    overall_summary = combined_data.groupby("answer")["corrected_responseTime"]\
        .agg(['mean', 'std'])\
        .reset_index()
    
    # 小数点以下を指定桁数で丸める
    overall_summary["mean"] = overall_summary["mean"].round(ROUND_DECIMALS)
    overall_summary["std"] = overall_summary["std"].round(ROUND_DECIMALS)
    
    # 結果を表示
    print("\n色ごとの全体補正後反応時間の平均と標準偏差:")
    print(overall_summary)
else:
    print("補正後のデータがありません。エラーを確認してください。")
