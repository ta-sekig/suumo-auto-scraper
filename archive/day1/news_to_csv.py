import requests
from bs4 import BeautifulSoup
import csv
import datetime

url = "https://news.yahoo.co.jp/"
response = requests.get(url)
soup = BeautifulSoup(response.text,"html.parser")
target_element = soup.select_one("main")

news_data = []
if target_element:
    links = target_element.select("a")
    for link in links:
        title = link.get_text().strip()
        article_url = link.get("href")
        if title and len(title) > 5:
            news_data.append([title,url])

today = datetime.date.today()
filename = f"news_{today}.csv"
with open(filename,"w",newline="",encoding="utf-8_sig")as f:
    writer= csv.writer(f)
    writer.writerow(["ニュースタイトル","記事URL"])
    writer.writerows(news_data)
print(f"*{filename}に保存しました！")