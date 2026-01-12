from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time

driver = webdriver.Chrome()
driver.get("http://quotes.toscrape.com/login")

try:
    wait = WebDriverWait(driver,10)
    wait.until(EC.element_to_be_clickable((By.ID,"username"))).send_keys("admin")
    driver.find_element(By.ID,"password").send_keys("password")
    driver.find_element(By.CSS_SELECTOR,".btn-primary").click()

    wait.until(EC.presence_of_element_located((By.LINK_TEXT,"Logout")))
    print("ログイン成功。cookiesを保存します。")

    cookies = driver.get_cookies()
    with open("my_cookies.pkl","wb") as f:
        pickle.dump(cookies,f)

    print("保存完了")
except Exception as e:
    print(f"失敗:{e}")

finally:
    driver.quit()