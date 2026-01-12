import gspread

gc = gspread.service_account(filename="secret_key.json")
SPREADSHEET_KEY = "1Ziey5w9zArvQcv_VrEmY7_M9CnReO3rYa8GonZ6jc5Q"

try:
    sh = gc.open_by_key(SPREADSHEET_KEY)
    worksheet = sh.sheet1
    worksheet.update_acell("A1","完全理解")
    worksheet.update_acell("B1","成功")

    print("書き込み成功")
except Exception as e:
    print(f"エラー発生:{e}")