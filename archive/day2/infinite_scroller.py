from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://yahoo.co.jp/categories/business")

print("ページを開きました。ボタン攻略を開始します...")
time.sleep(2)

while True:
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(1)
    try:
        more_btn = driver.find_element(By.XPATH,"//*[contains(text(),'もっと見る')]")
        print("「もっと見る」ボタンを発見。クリックします。")
        more_btn.click()
        time.sleep(3)
    except:
        print("ボタンが見つかりませんでした。全件表示完了、または最下部到達")
        break

print("完了。5秒後に閉じます。")
time.sleep(5)
driver.quit()