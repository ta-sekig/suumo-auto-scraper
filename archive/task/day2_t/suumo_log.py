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


#========================
# 1.ロギング設定
#========================
#ロガーの定義:コンソールにはINFO以上、ファイルにはERROR以上を出力する設定
logger = logging.getLogger("suumo_log")
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]')

#ファイルハンドラ
file_handler = logging.FileHandler("error_log.txt",encoding="utf-8")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

#ストリームハンドラ
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

#=========================
#2.変数・ブラウザ設定
#=========================
#ドライバの初期値を"None"にしネットエラー時にもfinallyでクラッシュしない設計
driver = None

op = Options()
op.add_argument("--headless=new")#バックグラウンド実行
op.add_argument("--window-size=1920,1080")
#一般的なブラウザに見せかけるエージェント設定
op.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

house_info =[]
#==========================
#3.メイン処理
#==========================
logger.info("スクレイピングを開始します")

try:
    #--ブラウザ起動--
    #接続不良の場合はここでエラーが出る
    driver_path = ChromeDriverManager().install()
    sv = Service(executable_path=driver_path)

    driver = webdriver.Chrome(options=op,service=sv)
    #ページループ処理
    for page in range(1,4):
        driver.get(f"https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13112&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1&page={page}")
        time.sleep(3)#サーバー負担軽減とBAN対策
        logger.info(f"{page}目の物件を処理中...")
        house_elems = driver.find_elements(By.CSS_SELECTOR,".cassetteitem")
        #物件ごとの処理
        for i,elem in enumerate(house_elems,start=1):
            try:
                name = elem.find_element(By.CSS_SELECTOR,".cassetteitem_content-title").text
                address = elem.find_element(By.CSS_SELECTOR,".cassetteitem_detail-col1").text
                rooms = elem.find_elements(By.CSS_SELECTOR,".js-cassette_link")
                #部屋ごとの処理
                for r,room in enumerate(rooms,start=1):
                    rent = room.find_element(By.CSS_SELECTOR,".cassetteitem_price.cassetteitem_price--rent").text
                    link_e = room.find_element(By.CSS_SELECTOR,".ui-text--midium.ui-text--bold > a")
                    url = link_e.get_attribute("href")
                    house_info.append({"Name": name,"Address": address,"Rent": rent,"URL": url})
                    logger.info(f"{page}ページ-物件{i}:「{name}」-部屋{r}の情報を記録しました")
            except Exception as e:
                #データ取得時のエラーでもクラッシュしない設計
                logger.error(f"{page}ページ目-建物{i}でエラー発生:{e}",exc_info=True)
                continue
    
    #==========================
    #4.データ保存
    #==========================
    #ループ終了後データがある場合のみ保存（API節約）
    if house_info:
        df = pd.DataFrame(house_info)
        gc = gspread.service_account("secret_key.json")
        sh = gc.open_by_key("1Ziey5w9zArvQcv_VrEmY7_M9CnReO3rYa8GonZ6jc5Q")
        work_sheet = sh.sheet1
        work_sheet.clear()
        set_with_dataframe(work_sheet,df)
        logger.info("スプレッドシートに記入完了")
    else:
        logger.warning("取得データが0件です")
except Exception as e:
    #ネットワーク接続エラー等をここでキャッチ
    logger.critical(f"予期せぬエラー発生:{e}",exc_info=True)

finally:
    #=======================
    #5.終了処理
    #=======================
    if driver:
        logger.info("ブラウザを閉鎖します")
        driver.quit()
    else:
        logger.info("ブラウザは起動されませんでした")




