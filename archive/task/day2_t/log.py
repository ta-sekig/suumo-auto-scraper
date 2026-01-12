import logging

logger = logging.getLogger("practice_log")

logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]')

file_handler = logging.FileHandler("suumo_scraping.log",encoding="utf-8")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.info("これはテストです。ファイルには記録されません")
logger.error("エラー発生。これは記録されます")

