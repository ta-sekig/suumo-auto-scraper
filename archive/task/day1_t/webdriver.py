from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

op = Options()
op.add_argument("--headless=new")
op.add_argument("--window-size=1920,1080")
op.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

driver_path = ChromeDriverManager().install()
sv = Service(executable_path=driver_path)
driver = webdriver.Chrome(options=op,service=sv)

try:
    driver.get("https://www.yahoo.co.jp")
    wait = WebDriverWait(driver,10)
    wait.until(EC.presence_of_element_located((By.ID,"tabpanelTopics1")))

    news_text = driver.find_elements(By.CSS_SELECTOR,"#tabpanelTopics1 a")
    data_list =[]
    for i,elem in enumerate(news_text):
        try:
            link = elem.get_attribute("href")
            title_elem = elem.find_element(By.CSS_SELECTOR,"h1 span")
            title = title_elem.text
            data_list.append({"No": i+1,"Title": title,"URL": link})
        except Exception:
            continue
    print("ニュースタイトル取得成功")

    df = pd.DataFrame(data_list)
    df.to_csv("Yahoo_news.csv",index=False,encoding="utf-8-sig")
except Exception as e:
    print(f"エラー発生:{e}")

finally:
    print("ブラウザを閉じます")
    driver.quit()

