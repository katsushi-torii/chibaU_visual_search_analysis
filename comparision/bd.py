#一対比較法(Bradley-Terryモデル)、アイテムの強さを考慮した方法

import pandas as pd  #データ操作用
import numpy as np  #数値計算用
import statsmodels.api as sm  #Bradley-Terryモデルの適用用
from sklearn.linear_model import LogisticRegression  #正則化付きロジスティック回帰用

df = pd.read_csv("./csv/comparision/comparision_subject3.csv")
colors = ['gray', 'red', 'green', 'blue', 'yellow', 'purple', 'pink', 'yellow-red', 'yellow-green', 'blue-green', 'purple-blue', 'red-purple']
color_dict = {color: i for i, color in enumerate(colors)}

#勝者と敗者を含むデータを構築
data = []
for _, row in df.iterrows(): #iterrows():各行を取り出す
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

#Dataframeは表に整理：勝者・敗者・結果が列、試行回数が行
data = pd.DataFrame(data, columns=['winner', 'loser', 'outcome'])

#特徴行列の作成、列は各色、行は各比較。特徴行列の各行において、勝者は+1、敗者は-1、登場していない10色は0に変換される。
X = np.zeros((len(data), len(colors))) #zerosで全ての値が0の表を作成、引数で行と列の長さを指定
for i, row in data.iterrows():
    X[i, row['winner']] = 1
    X[i, row['loser']] = -1

#目的変数（勝敗の結果）を定義
y = data['outcome']

#ロジスティック回帰は２つの選択肢のうちどちらが選ばれるかの確立を予測する手法。進出度スコアの差に基づいて勝率を得る
#penaltyはデータの偏りが大きすぎるのを抑えるための正則化項。l2正則化はスコアの2乗の合計にペナルティをかける方式
#cは正則化の強さを指定するパラメータ。値が大きいほどペナルティが弱くなり、元のデータに近くなる。1e6は10の6乗
#なぜ正則化しているのにその後弱めのペナルティを指定？極度に偏ったスコアが発生した場合でもモデルが安定して学習できるようにしたいが、元のデータの情報は最大限残したいため。
#solverでロジスティック回帰の計算方法の指定。liblinearはシンプルな線形分類の計算アルゴリズム。
model = LogisticRegression(penalty='l2', C=1e6, solver='liblinear')

#fit()はロジスティック回帰を用いて、観測された勝敗データyと特徴行列Xで進出度スコアの最適化。データ全体での傾向を学習して、スコアを調整。要するにデータの学習。
model.fit(X, y)

#coefで学習された各色の進出度スコアを格納
strengths = model.coef_[0]
print(strengths)

#各色のスコアを最も大きな絶対値で割ることで、全スコアが-1から+1に収まる
# strengths = strengths / np.max(np.abs(strengths))  

#結果を強さ順にソートして表示
sorted_strengths = sorted(zip(colors, strengths), key=lambda x: x[1], reverse=True)

# for color, score in sorted_strengths:
#     print(f"{color}: {score:.4f}")



#図示
# import matplotlib.pyplot as plt

# colors と strengths は Bradley-Terry モデルで計算した色とスコアのリストを想定
# sorted_strengths は (color, score) のタプルで色とスコアが強さ順に並んでいるもの

# 色とスコアをそれぞれリストに分ける
# colors, scores = zip(*sorted_strengths)

# # 可視化
# plt.figure(figsize=(10, 6))
# plt.barh(colors, scores, align='center')
# plt.xlabel('進出度スコア')
# plt.title('Bradley-Terryモデルによる進出度スコア')
# plt.gca().invert_yaxis()  # スコアが高い順に上から並べる
# plt.show()
