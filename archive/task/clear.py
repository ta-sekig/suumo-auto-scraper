import gspread

gc = gspread.service_account("secret_key.json")
sh = gc.open_by_key("1Ziey5w9zArvQcv_VrEmY7_M9CnReO3rYa8GonZ6jc5Q")
work_sheet = sh.sheet1
work_sheet.clear()