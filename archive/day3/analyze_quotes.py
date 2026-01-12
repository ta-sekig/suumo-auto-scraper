import pandas as pd

print("データを読み込んでいます...")
df = pd.read_csv("secret_quotes.csv")

print("【著者ランキングtop5】")
author_counts = df["著者名"].value_counts()
print(author_counts.head(5))
print("-" * 30)

print("【'love'を含む名言集】")
love_quotes = df[df["名言"].str.contains("love",case=False)]
love_quotes = love_quotes[["著者名","名言"]]
print(f"発見数:{len(love_quotes)}")
for index,row in love_quotes.iterrows():
    print(f"{row['著者名']}:{row['名言'][:30]}...")

author_counts.to_csv("author_ranking.csv",encoding="utf-8-sig",header="名言数")
love_quotes.to_excel("love_quotes_report.xlsx",index=False)

print("-" * 30)
print("分析完了")