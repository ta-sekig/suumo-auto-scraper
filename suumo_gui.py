import flet as ft
import time
import os
import sys
import requests
import json
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


#======================
#0.設定
#======================
webhook_url = "DISCODE_WEBHOOK_URL"

#======================
#1.EXE化
#======================
def resource_path(relative_path):
    if hasattr(sys,"_MEIPASS"):
        return os.path.join(sys._MEIPASS,relative_path)
    
    return os.path.join(".",relative_path)

#======================
#2.通知設定
#======================
def send_discode_notify(msg):
    data = {"content": msg}
    try:
        response = requests.post(webhook_url,data=json.dumps(data),headers={"Content-Type": "application/json"})
    except Exception:
        pass

#======================
#3.GUIメイン処理
#======================
def main(page: ft.Page):
    page.title = "Suumo_Auto_Scraper"
    page.window_width = 450
    page.window_height = 400
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    status_text = ft.Text(value = "準備完了、ボタンを押してください",size=20)
    log_text = ft.Text(value="",size=12,color="grey")

    def run_scraping(e):
        start_button.disabled = True
        start_button.text = "実行中..."
        status_text.value = "ブラウザを起動しています..."
        status_text.color = "blue"
        page.update()

        house_info = []
        driver = None
        try:
            op = Options()
            op.add_argument("--headless=new")
            op.add_argument("--window-size=1920,1080")
            op.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
            
            driver_path = ChromeDriverManager().install()
            sv = Service(executable_path=driver_path)
            driver = webdriver.Chrome(options=op,service=sv)

            for page_num in range(1,4):
                try:
                    driver.get(f"https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13112&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1&page={page_num}")
                    status_text.value = f"{page_num}ページを巡回中..."
                    page.update()
                    time.sleep(3)
                    house_elems = driver.find_elements(By.CSS_SELECTOR,".cassetteitem")
                    for i,elem in enumerate(house_elems,start=1):
                        try:
                            name = elem.find_element(By.CSS_SELECTOR,".cassetteitem_content-title").text
                            address = elem.find_element(By.CSS_SELECTOR,".cassetteitem_detail-col1").text
                            rooms = elem.find_elements(By.CSS_SELECTOR,".js-cassette_link")
                            for r,room in enumerate(rooms,start=1):
                                rent = room.find_element(By.CSS_SELECTOR,".cassetteitem_price.cassetteitem_price--rent").text
                                link = room.find_element(By.CSS_SELECTOR,".js-cassette_link_href.cassetteitem_other-linktext")
                                url = link.get_attribute("href")
                                house_info.append({"Name": name,"Address": address,"Rent": rent,"URL": url})
                                log_text.value = f"データ取得完了:{name}:{rent}"
                                msg_success = f"データ取得完了:{len(house_info)}件"
                                send_discode_notify
                                page.update()
                        except Exception:
                            continue
                except Exception:
                    continue
            
            if house_info:
                status_text.value = "スプレッドシートに保存中..." 
                page.update()
                df = pd.DataFrame(house_info)
                key_path = resource_path("secret_key.json")
                gc = gspread.service_account(key_path)
                sh = gc.open_by_key("SPREADSHEET_KEY")
                work_sheet = sh.sheet1
                work_sheet.clear()
                set_with_dataframe(work_sheet,df)
                final_msg = f"保存完了:{len(house_info)}件"
                send_discode_notify(final_msg)
                status_text.value = final_msg
                status_text.color = "green"
                page.update()
            else:
                status_text.value = "取得データが0件でした"
                status_text.color = "red"
                page.update()
        except Exception as err:
            status_text.value = "エラー発生"
            status_text.color = "red"
            log_text.value = str(err)
            page.update()
            send_discode_notify(f"エラー:{err}")

        finally:
            if driver:
                driver.quit()
        
        start_button.disabled = False
        start_button.text = "スクレイピング開始..."
        page.update()

    start_button = ft.ElevatedButton(text="スクレイピング開始...",on_click=run_scraping)
    page.add(
        ft.Row([status_text],alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([start_button],alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        ft.Row([log_text],alignment=ft.MainAxisAlignment.CENTER),
    )
ft.app(target=main)
            

