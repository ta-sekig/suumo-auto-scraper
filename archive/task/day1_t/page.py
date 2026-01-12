from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

op = Options()
op.add_argument("--headless=new")
op.add_argument("--window-size=1920,1080")
op.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

driver_path = ChromeDriverManager().install()
sv = Service(executable_path=driver_path)
driver = webdriver.Chrome(options=op,service=sv)

try:
    news_data = []
    for page in range(1,30,10):
        driver.get(f"https://search.yahoo.co.jp/search?p=python&fr=top_ga1_sa&ei=UTF-8&ts=1376&aq=-1&oq=&at=&ai=78aecb12-dee6-47d0-a921-859312d9dee5&x=nl&b={page}")
        time.sleep(3)
        wait = WebDriverWait(driver,10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".sw-Card__title")))

        article_elems = driver.find_elements(By.CSS_SELECTOR,".sw-Card__title a")
        for elem in article_elems:
            link = elem.get_attribute("href")
            try:
                title = elem.find_element(By.CSS_SELECTOR,"h3 span").text
                current_count = len(news_data) + 1
                news_data.append({"No": current_count,"Title": title,"URL": link})
            except Exception:
                continue
    df = pd.DataFrame(news_data)
    df.to_csv("Yahoo_news.csv",index=False,encoding="utf-8-sig")
    print("データ保存完了")
except Exception as e:
    print(f"エラー発生:{e}")

finally:
    print("ブラウザを閉じます")
    driver.quit()
