import requests
from bs4 import BeautifulSoup

url = "https://news.yahoo.co.jp/"
response = requests.get(url)
soup = BeautifulSoup(response.text,"html.parser")
target_element = soup.select_one("main")
if target_element:
    print("===Yahoo!ニュース 速報===")
    links = target_element.select("a")

    count = 0
    for link in links:
        title = link.get_text().strip()
        if title and count < 5:
            print(f"・{title}")
            count += 1

else:
    print("要素が見つかりませんでした。")