from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import csv

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
        print("ログイン完了")

    quote_data = []
    while True:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".quote")))
        whole_elems = driver.find_elements(By.CSS_SELECTOR,".quote")
        print(f"現在処理中のページから{len(whole_elems)}件取得中...")
        for elem in whole_elems:
            text_e = elem.find_element(By.CSS_SELECTOR,".text").text
            author_e = elem.find_element(By.CSS_SELECTOR,".author").text
            quote_data.append([text_e,author_e])

        next_btn = driver.find_elements(By.CSS_SELECTOR,"li.next > a")
        if len(next_btn) > 0:
            next_btn[0].click()
            print("次のページへ移動します")
        else:
            print("全ページ取得完了")
            break

    with open("secret_quotes.csv","w",encoding = "utf-8",newline = "") as f:
        writer = csv.writer(f)
        writer.writerow(["名言","著者名"])
        writer.writerows(quote_data)
        print("合計{len(quote_data)}件のデータを保存しました")

except Exception as e:
    print(f"エラー発生:{e}")

finally:
    driver.quit()