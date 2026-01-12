from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

print("ステルスモードで起動中...")
options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)
print("ブラウザ起動完了(画面は出ません)")

try:
    driver.get("https://www.yahoo.co.jp/")
    wait = WebDriverWait(driver,10)
    search_box = wait.until(EC.presence_of_element_located((By.NAME,"p")))
    search_box.send_keys("Python Headless Mode")
    search_box.send_keys(Keys.RETURN)

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,".sw-Card__title")))
    print("検索完了。証拠写真を撮ります...")
    driver.save_screenshot("stealth_result.png")
    print("撮影完了:stealth_result.png")
except Exception as e:
    print(f"エラー発生:{e}")

finally:
    driver.quit()