from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

print("ブラウザを起動します...")
driver = webdriver.Chrome()
driver.get("https://www.google.com")
search_box = driver.find_element(By.NAME,"q")
search_box.send_keys("Python スクレイピング 最強")
search_box.send_keys(Keys.RETURN)

print("検索しました。5秒後に閉じます。")
time.sleep(5)

driver.quit()
