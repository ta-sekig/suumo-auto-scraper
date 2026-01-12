import requests
import json
import logging

#=====================
#1.設定エリア
#=====================
logger = logging.getLogger("discode_log")
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]')

file_handler = logging.FileHandler("error_discode.text",encoding="utf-8")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

webhook_url = "https://discordapp.com/api/webhooks/1459213911982215252/5mkjbgRfzxZsgEtF89iM213Knx83OfRh1URD3x7u0bIbaI5DTPeUimaz3sc73vScX32h"

#=====================
#2.送信ロジック
#=====================
def send_discode_notify(message):
    data = {"content": message}
    try:
        response = requests.post(webhook_url,data=json.dumps(data),headers={"Content-Type": "application/json"})
        #サーバーから送られてくる結果によって成功と失敗を分岐
        if response.status_code == 204:
            logger.info("送信成功!")
        else:
            logger.warning(f"送信失敗:{response.status_code}")
            logger.warning(response.text)#エラー内容表示
    except Exception as e:
        logger.error(f"エラー発生:{e}",exc_info=True)


#======================
#3.実行制御
#======================
if __name__ == "__main__":
    logger.info("Discodeへの通知テストを開始...")
    send_discode_notify("テスト通知です。\nPythonからこんにちは!\nこれは成功の証です。")

