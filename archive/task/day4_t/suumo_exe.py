import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import csv
import time
import logging
import requests
import json
import gspread
from gspread_dataframe import set_with_dataframe

#====================
#0.設定
#====================
webhook_url = "DISCODEURL"

#====================
#1.EXE化設定
#====================
def resource_path(relative_path):
    if hasattr(sys,'_MEIPASS'):
        return os.path.join(sys._MEIPASS,relative_path)
    
    return os.path.join(os.path.abspath('.'),relative_path)

#====================
#2.ロガー設定
#====================
logger = logging.getLogger("suumo_log")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s][[%(levelname)s][%(message)s]")

file_handler = logging.FileHandler("error_get.txt",encoding="utf-8")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

#====================
#3.通知設定
#====================
def send_discode_notify(msg):
    data = {"content": msg}
    try:
        response = requests.post(webhook_url,data=json.dumps(data),headers={"Content-Type": "application/json"})
        if response.status_code == 204:
            logger.info("送信成功")
        else:
            logger.warning(f"送信失敗:{response.status_code}-{response.text}")
    except Exception as e:
        logger.error(f"メッセージ送信時にエラー発生:{e}")

#====================
#４。ブラウザ設定
#====================
op = Options()
op.add_argument("--headless=new")
op.add_argument("--window-size=1920,1080")
op.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

#====================
#5.メイン処理
#====================
house_info =[]
logger.info("スクレイピング開始...")
try:
    driver_path = ChromeDriverManager().install()
    sv = Service(executable_path = driver_path)
    driver = webdriver.Chrome(options=op,service=sv)
    logger.info("ページ巡回開始")
    for page in range(1,4):
        try:
            driver.get(f"https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13112&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1&page={page}")
            logger.info(f"{page}ページの処理開始...")
            time.sleep(3)
            house_elems = driver.find_elements(By.CSS_SELECTOR,".cassetteitem")
            for i,elem in enumerate(house_elems,start=1):
                try:
                    name =elem.find_element(By.CSS_SELECTOR,".cassetteitem_content-title").text
                    address = elem.find_element(By.CSS_SELECTOR,".cassetteitem_detail-col1").text
                    rooms = elem.find_elements(By.CSS_SELECTOR,".js-cassette_link")
                    #部屋ごと処理
                    for r,room in enumerate(rooms,start=1):
                        rent = room.find_element(By.CSS_SELECTOR,".cassetteitem_price.cassetteitem_price--rent").text
                        link = room.find_element(By.CSS_SELECTOR,".js-cassette_link_href.cassetteitem_other-linktext")
                        url = link.get_attribute("href")
                        house_info.append({"Name": name,"Address": address,"Rent": rent,"URL": url})
                    logger.info(f"{page}ページ-物件{i}.[{name}]-{r}のデータ取得成功")
                except Exception as e:
                    logger.error(f"{page}の物件{i}.[{name}]のデータ取得に失敗しました")
                    continue
        except Exception as e:
            logger.error(f"{page}ページの取得に失敗しました...")
            continue

    #=========================
    #6.データ保存
    #=========================
    if house_info:
        df = pd.DataFrame(house_info)
        key_path = resource_path("secret_key.json")
        logger.info(f"鍵ファイルのパス:{key_path}")
        gc = gspread.service_account(key_path)
        sh = gc.open_by_key("SHEET")
        work_sheet = sh.sheet1
        work_sheet.clear()
        set_with_dataframe(work_sheet,df)
        logger.info("スプレッドシートに記入完了")
        msg = f"{len(house_info)}件のデータ取得成功"
        send_discode_notify(msg)
    else:
        logger.warning("取得データが0件です")
        msg_no = "取得データが0件です"
        send_discode_notify(msg_no)

except Exception as e:
    logger.critical(f"想定外のエラー発生:{e}")
    msg_error = f"想定外のエラーにより処理が停止しました:{e}"
    send_discode_notify(msg_error)

finally:
    if driver:
        driver.quit()
        logger.info("ブラウザを閉鎖しました")
    else:
        logger.info("ブラウザは開かれませんでした")