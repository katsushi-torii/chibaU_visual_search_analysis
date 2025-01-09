#色ごとの補正後反応時間（被験者ごと）
import statsmodels.api as sm
import pandas as pd

# ファイルリスト
file_list = [f"./csv/main/answers_subject{i}.csv" for i in range(1, 8)]

# 被験者ごとの補正後反応時間を格納するリスト
subject_corrected_results = []

# 小数点以下を指定する桁数
ROUND_DECIMALS = 2

# ファイルごとに処理
for i, file_path in enumerate(file_list):
    try:
        # データの読み込み
        df = pd.read_csv(file_path)
        
        # 必要な列の整備
        df["responseTime"] = pd.to_numeric(df["responseTime"], errors="coerce")
        df["targetAmount"] = pd.to_numeric(df["targetAmount"], errors="coerce")  # 数値型に変換
        df["target_present"] = df["answerId"].apply(lambda x: "あり" if x != -1 else "なし")
        
        # ダミー変数の作成（基準条件: ターゲットあり、刺激数6個）
        X = pd.get_dummies(df[["targetAmount", "target_present"]], drop_first=True)
        X = sm.add_constant(X)  # 定数項を追加
        X = X.astype(float)  # 型を明示的にfloatに変換

        # 目的変数
        y = df["responseTime"]

        # 線形モデルの構築
        model = sm.OLS(y, X).fit()

        # 必要なモデル情報を出力
        print(f"\n被験者_{i+1}のモデル結果:")
        print(f"  定数項（基準条件）: {model.params.get('const', 0):.2f}")
        if "targetAmount_8" in model.params:
            print(f"  刺激数8の影響: {model.params.get('targetAmount_8', 0):.2f}")
        if "target_present_なし" in model.params:
            print(f"  ターゲットなしの影響: {model.params.get('target_present_なし', 0):.2f}")

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

        # 色ごとの補正後反応時間の平均と標準偏差を計算
        color_summary = (
            df.groupby("answer")["corrected_responseTime"]
            .agg(['mean', 'std'])  # 平均と標準偏差を計算
            .reset_index()
        )
        
        # 小数点以下を指定桁数で丸める
        color_summary["mean"] = color_summary["mean"].round(ROUND_DECIMALS)
        color_summary["std"] = color_summary["std"].round(ROUND_DECIMALS)
        
        # 被験者情報を追加
        color_summary["subject"] = f"被験者_{i+1}"
        
        # 結果を格納
        subject_corrected_results.append(color_summary)
    
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {file_path}")
    except Exception as e:
        print(f"エラーが発生しました（被験者_{i+1}）: {e}")

# 全被験者のデータを統合
if subject_corrected_results:
    all_corrected_summary = pd.concat(subject_corrected_results, ignore_index=True)
    
    # ピボットテーブル形式に変換
    corrected_time_table = all_corrected_summary.pivot(index="answer", columns="subject", values=["mean", "std"])
    
    # 結果を表示
    print("\n色ごとの補正後反応時間の平均と標準偏差 (被験者ごと):")
    print(corrected_time_table)
else:
    print("補正後のデータがありません。エラーを確認してください。")
