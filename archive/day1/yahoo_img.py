import requests
from bs4 import BeautifulSoup
import time
import os

url = "https://news.yahoo.co.jp/"
response = requests.get(url)
soup = BeautifulSoup(response.text,"html.parser")
target_element = soup.select_one("main")

if target_element:
    images = target_element.select("img")
    print(f"画像が{len(images)}枚見つかりました。ダウンロードを開始します...")

    count = 0
    for image in images:
        img_url = image.get("src")
        if img_url:
            try:
                img_response = requests.get(img_url)
                file_name = f"image_{count}.png"
                save_path = os.path.join("downloaded_img",file_name)
                with open(save_path,"wb") as f:
                    f.write(img_response.content)
                print(f"[{count}]保存完了:{img_url}")
                count += 1
                time.sleep(1)

                if count >= 5:
                    break
            except Exception as e:
                print(f"エラー発生:{e}")
        else:
            print("メインエリアが見つかりませんでした")
