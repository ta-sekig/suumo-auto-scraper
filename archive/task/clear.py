import gspread

gc = gspread.service_account("secret_key.json")
sh = gc.open_by_key("SHEET")
work_sheet = sh.sheet1
work_sheet.clear()