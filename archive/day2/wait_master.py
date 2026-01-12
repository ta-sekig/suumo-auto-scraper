from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://www.yahoo.co.jp/")
print("検索窓を探しています...")

try:
    wait = WebDriverWait(driver,10)
    search_box = wait.until(EC.presence_of_element_located((By.NAME,"p")))

    print("発見 !すぐに入力します")
    search_box.send_keys("Pyrhon WebDriverWait")
    search_box.send_keys(Keys.RETURN)
except:
    print("エラー:10秒待っても検索窓が見つかりませんでした")

try:
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,".sw-Card__title")))
    print("検索結果が表示されました")

except:
    print("エラー:検索結果の読み込みに失敗しました")

time.sleep(3)
driver.quit()