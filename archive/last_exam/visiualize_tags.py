import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

print("データを読み込んでいます...")

df = pd.read_csv("all_tags.csv",sep="\t")

print("タグランキング top10")
tag_ran = df["タグ名"].value_counts().head(10)

tag_ran.to_excel("tag_ranking.xlsx")

print("-" * 20)

print("グラフを作成中...")
plt.figure(figsize=(10,6))
plt.bar(tag_ran.index,tag_ran.values,color="orange",alpha=0.9)
plt.title("タグ数ランキング",fontsize=16)
plt.xlabel("タグ名",fontsize=12)
plt.ylabel("個数",fontsize=12)
plt.grid(axis="y",linestyle="--",alpha=0.9)


