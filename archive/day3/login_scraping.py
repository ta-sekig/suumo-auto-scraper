from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import pickle
import time

driver = webdriver.Chrome()
driver.get("http://quotes.toscrape.com/")

try:
    with open("my_cookies.pkl","rb") as f:
        cookies = pickle.load(f)
        for c in cookies:
            driver.add_cookie(c)
        driver.refresh()
        wait = WebDriverWait(driver,10)
        wait.until(EC.presence_of_element_located((By.LINK_TEXT,"Logout")))
        print("ログイン成功")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".quote")))
        
    quote_data = []
    whole_elements = driver.find_elements(By.CSS_SELECTOR,".quote")
    for elem in whole_elements:
        text_elem = elem.find_element(By.CSS_SELECTOR,".text").text
        author = elem.find_element(By.CSS_SELECTOR,".author").text
        quote_data.append([text_elem,author])

    with open("secret_quotes.csv","w",encoding = "utf-8",newline = "") as f:
        writer = csv.writer(f)
        writer.writerow(["名言","著者名"])
        writer.writerows(quote_data)
        print("データを保存しました")

except Exception as e:
    print(f"エラー発生:{e}")

finally:
    driver.quit()