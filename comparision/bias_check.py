#実験1において、左右に偏りがないか検証

import pandas as pd
from collections import defaultdict
from scipy.stats import binomtest

df = pd.read_csv("./csv/comparision/comparision_subject7.csv")
left_selected = 0
right_selected = 0

for _, row in df.iterrows():
    if row['selectedColor'] == row['colorA']:
        left_selected += 1  # 左側が選ばれた場合
    elif row['selectedColor'] == row['colorB']:
        right_selected += 1  # 右側が選ばれた場合

total_trials = left_selected + right_selected

#二項検定を実施
result = binomtest(left_selected, n=total_trials, p=0.5, alternative='two-sided')

#結果の表示

print(f"左: {left_selected}", f"右: {right_selected}")
print(f"p値: {result.pvalue}")
if result.pvalue < 0.05:
    print("有意な偏りがあります（帰無仮説を棄却）")
else:
    print("有意な偏りはありません（帰無仮説を採択）")

