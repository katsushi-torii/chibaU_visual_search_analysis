#一対比較法(Bradley-Terryモデル)、アイテムの強さを考慮した方法

import pandas as pd  # データ操作用
import numpy as np  # 数値計算用
import statsmodels.api as sm  # Bradley-Terryモデルの適用用
from sklearn.preprocessing import StandardScaler  # データの標準化用
from sklearn.linear_model import LogisticRegression  # 正則化付きロジスティック回帰用

#csvファイルの指定
df = pd.read_csv("./csv/comparision_subject3.csv")

colors = ['gray', 'red', 'green', 'blue', 'yellow', 'purple', 'pink', 'yellow-red', 'yellow-green', 'blue-green', 'purple-blue', 'red-purple']
color_dict = {color: i for i, color in enumerate(colors)}

#勝者と敗者を含むデータを構築
data = []
for _, row in df.iterrows():
    color_a = color_dict[row['colorA']]
    color_b = color_dict[row['colorB']]
    selected = color_dict[row['selectedColor']]
    
    #選択された色が勝者、もう一方が敗者
    if selected == color_a:
        data.append([color_a, color_b, 1])  #color_aが勝者
        data.append([color_b, color_a, 0])  #color_bが敗者
    else:
        data.append([color_b, color_a, 1])  #color_bが勝者
        data.append([color_a, color_b, 0])  #color_aが敗者

#表に整理：勝者、敗者、結果
data = pd.DataFrame(data, columns=['winner', 'loser', 'outcome'])

#特徴行列の作成、列は各色、行は各比較。勝者は+1、敗者は-1、登場していないほか１０色は0に変換される。
X = np.zeros((len(data), len(colors)))
for i, row in data.iterrows():
    X[i, row['winner']] = 1
    X[i, row['loser']] = -1

#目的変数（勝敗の結果）を定義
y = data['outcome']

#Bradley-Terryモデルの適用：正則化付きロジスティック回帰を使用、ここが全く分からない
model = LogisticRegression(penalty='l2', C=1e6, solver='liblinear')
model.fit(X, y)

#各色の進出度スコアを取得-
strengths = model.coef_[0]
#各色のスコアを最も大きな絶対値で割ることで、全スコアが-1から+1に収まる
strengths = strengths / np.max(np.abs(strengths))  

#結果を強さ順にソートして表示
sorted_strengths = sorted(zip(colors, strengths), key=lambda x: x[1], reverse=True)

for color, score in sorted_strengths:
    print(f"{color}: {score:.4f}")
