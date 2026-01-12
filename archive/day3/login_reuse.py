from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time

driver = webdriver.Chrome()
driver.get("http://quotes.toscrape.com/")
print("現在は未ログインです。")

try:
    with open("my_cookies.pkl","rb") as f:
        cookies = pickle.load(f)

        for c in cookies:
            driver.add_cookie(c)

        print("cookieを設定完了")
        driver.refresh()

        wait = WebDriverWait(driver,10)
        wait.until(EC.presence_of_element_located((By.LINK_TEXT,"Logout")))
        print("裏口入学に成功")

        time.sleep(3)
except Exception as e:
    print(f"エラー発生:{e}")

finally:
    driver.quit()