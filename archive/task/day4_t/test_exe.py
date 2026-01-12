import sys
import os
import time

def resource_path(relative_path):
    if hasattr(sys,"_MEIPASS"):
        return os.path.join(sys._MEIPASS,relative_path)
    
    return os.path.join(os.path.abspath("."),relative_path)

print("===EXE化テストツール===")
print(f"現在の実行モード:{'EXE実行' if hasattr(sys,'_MEIPATH') else '通常実行'}")
print("3秒後に終了します")

time.sleep(3)