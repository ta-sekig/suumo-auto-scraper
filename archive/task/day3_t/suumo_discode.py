from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import gspread
from gspread_dataframe import set_with_dataframe
import time
import pandas as pd
import csv
import logging
import requests
import json

#=========================
#0.設定エリア
#=========================
webhook_url = "https://discordapp.com/api/webhooks/1459514443292606710/qFHNtMukyEMNJ1C2biyS6x2SYTredyt20ufwnn3sxJzhgCgU0yWc4tehIeteKuqXSoZ-"

#=========================
#1.ロガー設定
#=========================
logger = logging.getLogger("suumo_log")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s][%(levelname)s][%(message)s]")

file_handler = logging.FileHandler("suumo_log.txt",encoding="utf-8")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
#==========================
#2.関数定義
#==========================
def send_discode_notify(message):
    data = {"content": message}
    print("こんにちは")
    try:
        response = requests.post(webhook_url,data=json.dumps(data),headers={"Content-Type": "application/json"})
    
        if response.status_code == 204:
            logger.info("送信成功")
        else:
            logger.warning(f"送信失敗:{response.status_code}")
            logger.warning(response.text)
        
    except Exception as e:
        logger.error(f"メッセージ送信時にエラー発生:{e}",exc_info=True)

#==========================
#3.ドライバー設定
#==========================
driver = None
op = Options()
op.add_argument("--headless=new")
op.add_argument("--window-size=1920,1080")
op.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

driver_path = ChromeDriverManager().install()
sv = Service(executable_path=driver_path)

#==========================
#4.スクレイピング処理
#==========================
house_info = []
logger.info("スクレイピングを開始します")
try:
    driver_path = ChromeDriverManager().install()
    sv = Service(executable_path=driver_path)
    driver = webdriver.Chrome(options=op,service=sv)
    for page in range(1,4):
        try:
            driver.get(f"https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13112&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1&page={page}")
            time.sleep(3)
            logger.info(f"{page}ページ目の物件を処理中...")
            house_element = driver.find_elements(By.CSS_SELECTOR,".cassetteitem")
            for i,elem in enumerate(house_element,start=1):#各物件ごとに処理
                try:
                    name = elem.find_element(By.CSS_SELECTOR,".cassetteitem_content-title").text
                    address = elem.find_element(By.CSS_SELECTOR,".cassetteitem_detail-col1").text
                    rooms = elem.find_elements(By.CSS_SELECTOR,".js-cassette_link")
                    for r,room in enumerate(rooms,start=1):
                        rent = room.find_element(By.CSS_SELECTOR,".cassetteitem_price.cassetteitem_price--rent").text
                        link = room.find_element(By.CSS_SELECTOR,".js-cassette_link_href.cassetteitem_other-linktext")
                        url = link.get_attribute("href")
                        house_info.append({"Name": name,"Address": address,"Rent": rent,"URL": url})
                        logger.info(f"{page}ページ:物件{i}「{name}」-部屋{r}の情報を取得しました")
                except Exception as e:
                    logger.error(f"{page}ページ目の物件{i}-[{name}]のデータ取得時にエラー発生:{e}",exc_info=True)
                    continue
        except Exception as e:
            logger.error(f"{page}ページ処理中にエラー発生:{e}",exc_info=True)

    #========================
    #5.　データ保存
    #========================
    if house_info:
        df = pd.DataFrame(house_info)
        gc = gspread.service_account("secret_key.json")
        sh = gc.open_by_key("1Ziey5w9zArvQcv_VrEmY7_M9CnReO3rYa8GonZ6jc5Q")
        worksheet = sh.sheet1
        worksheet.clear()
        set_with_dataframe(worksheet,df)
        logger.info("スプレッドシートに記入完了")

        #Discodeに送る
        msg = f"スクレイピング完了\n取得件数{len(house_info)}件\nスプレッドシートを更新しました"
        send_discode_notify(msg)
    else:
        logger.warning("取得データが0件です")
        msg = "データは0件でした"
        send_discode_notify(msg)

except Exception as e:
    logger.critical(f"想定外のエラー発生:{e}",exc_info=True)
    error_msg = f"エラー発生\n処理が停止しました\nエラー:{e}"
    send_discode_notify(error_msg)

finally:
    if driver:
        driver.quit()
        logger.info("ブラウザを閉じます")
    else:
        logger.info("ブラウザは開かれませんでした")




    


