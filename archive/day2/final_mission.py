from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

print("ステルスモード起動中...")
op = Options()
op.add_argument("--headless=new")
op.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options = op)
print("ブラウザ起動完了")

try:
    url = "https://news.yahoo.co.jp/categories/it"
    driver.get(url)
    wait = WebDriverWait(driver,10)
    wait.unti(EC.visibility_of_element_located((By.CSS_SELECTOR,".sw-Card__title")))
    all_elements = driver.find_elements(By.CSS_SELECTOR,".sw-Card__title")
    top5_elements = all_elements[:5]
    print(f"---取得したニュース:{len(top5_elements)}件---")

    save_data = []
    for elem in top5_elements:
        title = elem.text
        print(title)
        save_data.append(title)

    with open("it_news.txt","w",encoding = "utf-8") as f:
        f.write("【ニュースタイトル一覧】\n")
        for title in save_data:
            f.write(title + "\n")

    print("ファイル保存完了 it_news.txt")

except Exception as e:
    print(f"エラー発生:{e}")

finally:
    driver.quit()
    print("ブラウザを閉じました")