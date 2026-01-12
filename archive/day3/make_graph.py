import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

print("データを読み込み中...")
df = pd.read_csv("secret_quotes.csv")
author_counts = df["著者名"].value_counts().head(10)

print("グラフを作成中...")
plt.figure(figsize=(10,6))
plt.barh(author_counts.index,author_counts.values,color="orange",alpha=0.9)
plt.title("Webサイト上の著者別・名言数ランキング(top 10)",fontsize = 16)
plt.xlabel("名言数",fontsize=12)
plt.ylabel("著者名",fontsize=12)
plt.grid(axis="x",linestyle="--",alpha=0.7)
plt.tight_layout()

plt.savefig("author_graph.png")
print("完了")