from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

try:
    driver = webdriver.Chrome()
    driver.get("http://quotes.toscrape.com/login")
    wait = WebDriverWait(driver,10)
    name_box = wait.until(EC.element_to_be_clickable((By.ID,"username")))
    name_box.send_keys("admin")
    pass_box = wait.until(EC.element_to_be_clickable((By.ID,"password")))
    pass_box.send_keys("password")
    login_btn = driver.find_element(By.CSS_SELECTOR,".btn-primary")
    login_btn.click()

    try:
        wait.until(EC.presence_of_element_located((By.LINK_TEXT,"Logout")))
        print("ログイン成功!")
    except:
        print("ログイン失敗...")

    time.sleep(3)
except Exception as e:
    print(f"エラー発生:{e}")

finally:
    driver.quit()