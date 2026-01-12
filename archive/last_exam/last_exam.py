from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv
import pickle


op = Options()
op.add_argument("--headless=new")
op.add_argument("--window-size=1920,1080")
op.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options = op)
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


    quote_tag =[]
    while True:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".quote")))
        all_elems = driver.find_elements(By.CSS_SELECTOR,".quote")
        for elem in all_elems:
            tag_e = elem.find_elements(By.CSS_SELECTOR,".tag")
            tag_elems = []
            for t in tag_e:
                tag_text = t.text
                tag_elems.append(tag_text)
            quote_tag.extend(tag_elems)
            
        print(f"保存成功:{len(all_elems)}件")

        next_btn = driver.find_elements(By.CSS_SELECTOR,"li.next > a")
        if len(next_btn) > 0:
            next_btn[0].click()
            print("次のページへ移動します...")
        else:
            print("全ページ取得完了")
            break

    with open("all_tags.csv","w",encoding="utf-8-sig",newline="") as f:
        writer = csv.writer(f,delimiter="\t")
        writer.writerow(["タグ名"])
        for tag in quote_tag:
            writer.writerow([tag])
        print("'all_tags.csv'に保存完了")

except Exception as e:
    print(f"エラー発生:{e}")
    driver.save_screenshot("error_scrern.png")



finally:
    driver.quit()
    print("ブラウザを閉じました")

