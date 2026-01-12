from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

print("ブラウザを起動します。")
driver = webdriver.Chrome()
driver.get("https://www.yahoo.co.jp/")

search_box = driver.find_element(By.NAME,"p")
search_box.send_keys("Python スクレイピング")
time.sleep(0.5)
search_box.send_keys(Keys.RETURN)

print("検索完了。結果を読み取ります...")
time.sleep(3)
elems = driver.find_elements(By.CSS_SELECTOR,"sw-Card__title > a")
if not elems:
    print("クラス指定で見つかりませんでした。h3タグで再検索します...")
    elems = driver.find_elements(By.TAG_NAME,"h3")

print(f"---取得件数：{len(elems)}件---")

for elem in elems:
    title = elem.text
    try:
        link_tag = driver.find_element(By.TAG_NAME,"a")
        url = link_tag.get_attribute("href")
    except:
        url = "リンクなし"
    if title:
        print(f"タイトル:{title}")
        print(f"URL:{url}")
        print("-" * 20)

print("完了。5秒後に閉じます。")
time.sleep(5)
driver.quit()