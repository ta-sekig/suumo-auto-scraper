import flet as ft

#=======================
#メイン関数定義
#=======================
def main(page: ft.Page):
    page.title = "Suumo_Scraper_GUI"
    page.window_width = 400
    page.window_height = 300
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    #テキスト設定
    status_text = ft.Text(value="準備完了",size=20)

    #=======================
    #ボタン入力時動作関数
    #=======================
    def on_click_start(e):
        status_text.value = "処理実行中..."
        status_text.color = "blue"
        page.update()

    start_button = ft.ElevatedButton(text="スクレイピング開始...",on_click=on_click_start)
    page.add(ft.Row([status_text],alignment=ft.MainAxisAlignment.CENTER),ft.Row([start_button],alignment=ft.MainAxisAlignment.CENTER))

ft.app(target=main)