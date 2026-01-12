from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import gspread
from gspread_dataframe import set_with_dataframe
import logging

logger = logging.getLogger("suumo_sc")
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]')

file_handler = logging.FileHandler("suumo_sc.log",encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

op = Options()
op.add_argument("--headless=new")
op.add_argument("--window-size=1920,1080")
op.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

driver_path = ChromeDriverManager().install()
sv = Service(executable_path = driver_path)

driver = webdriver.Chrome(options=op,service=sv)


house_info = []
logger.info("スクレイピングを開始します")
try:
    for page in range(1,4):
        try:
            driver.get(f"https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13112&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1&page={page}")
            time.sleep(3)
            logger.info(f"{page}目の物件を処理中...")
            house_elems = driver.find_elements(By.CSS_SELECTOR,".cassetteitem")
            for i,elem in enumerate(house_elems,start=1):
                try:
                    name = elem.find_element(By.CSS_SELECTOR,".cassetteitem_content-title").text
                    address = elem.find_element(By.CSS_SELECTOR,".cassetteitem_content-body .cassetteitem_detail-col1").text
                    rooms = elem.find_elements(By.CSS_SELECTOR,".js-cassette_link") # または .js-cassette_link
                    for r,room in enumerate(rooms,start=1): 
                        rent = room.find_element(By.CSS_SELECTOR,".cassetteitem_price.cassetteitem_price--rent").text
                        url_elem = room.find_element(By.CSS_SELECTOR,".js-cassette_link_href.cassetteitem_other-linktext")
                        url = url_elem.get_attribute("href")
                        house_info.append({"Name": name,"Address": address,"Rent": rent,"URL": url})
                        logger.info(f"{page}目-建物{i}:{name}-部屋{r}のデータ取得成功!")
                except Exception as e:
                    logger.error(f"{page}ページ目-建物{i}の部屋{r}でエラー発生:{e}",exc_info=True)
                    continue
        except Exception as e:
            logger.error(f"{page}ページ目処理中にエラー発生:{e}",exc_info=True)
            continue

    if house_info:
        df = pd.DataFrame(house_info)
        gc = gspread.service_account("secret_key.json")
        sh = gc.open_by_key("SHEET")
        worksheet = sh.sheet1
        worksheet.clear()
        set_with_dataframe(worksheet,df)
        print("スプレッドシートに記入完了")
    else:
        logger.warning("取得データが0件です")

except Exception as e:
    logger.critical(f"重大なエラー発生:{e}",exc_info=True)



finally:
    logger.info("ブラウザを閉鎖します")
    driver.quit()


   





