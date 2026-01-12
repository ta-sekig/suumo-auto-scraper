# 🏠 Suumo Auto Scraper (GUI Desktop App)

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Flet](https://img.shields.io/badge/Flet-GUI-purple?logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-Automation-43B02A?logo=selenium&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data_Processing-150458?logo=pandas&logoColor=white)
![Google Sheets API](https://img.shields.io/badge/Google_Cloud-Sheets_API-4285F4?logo=google-cloud&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

賃貸物件情報の収集・分析を完全自動化するデスクトップアプリケーション。
指定した条件の物件情報をSUUMOからリアルタイムで取得し、Googleスプレッドシートへ即時同期します。

---

## 📸 デモ・動作イメージ

<video src="https://github.com/user-attachments/assets/4b2be085-d2c7-4cea-bd0a-ef3f12f6eaec" controls="controls" width="100%"></video>

---

## ✨ Key Features (特徴)

ただのスクレイピングツールではなく、**「現場での実用性」**を徹底追求しました。

### 1. 🚀 EXEファイルによる簡単導入
* Python環境がないPCでも動作するように、`PyInstaller`を用いて**exe化（実行ファイル化）**を実現。
* ユーザーはファイルをダブルクリックするだけで、即座にツールを利用可能です。

### 2. 📊 Googleスプレッドシート連携（API）
* ローカルのCSV保存だけでなく、**Google Sheets API**を活用してクラウドへ直接データを書き込み。
* これにより、チームメンバーとのリアルタイム共有や、スマホからのデータ確認が可能になりました。

### 3. 🖥 モダンで直感的なGUI (Flet採用)
* エンジニア以外でも操作できるよう、コマンドラインではなく**Flet**を用いたGUIを実装。
* エリア選択、家賃条件などを直感的に設定し、「開始ボタン」一つで自動化がスタートします。

---

## 🛠 Tech Stack (使用技術)

| Category | Technology | Usage |
| --- | --- | --- |
| **Language** | Python 3.11 | メインロジック |
| **GUI Framework** | Flet | フロントエンド・UI構築 |
| **Scraping** | Selenium (Chrome) | ブラウザ操作・DOM解析 |
| **Data Processing** | Pandas | データ整形・クリーニング |
| **Cloud/API** | Google Sheets API | データベース連携 |
| **Distribution** | PyInstaller | アプリケーション化(exe) |

---

## 📂 Directory Structure (構成)

```text
suumo-auto-scraper/
├── suumo_gui.py        # アプリケーションのエントリーポイント（GUI・ロジック統合）
├── requirements.txt    # 依存ライブラリ一覧
├── .gitignore          # 機密情報（APIキー等）の除外設定
├── README.md           # プロダクト仕様書（本ファイル）
└── (secret_key.json)   # Google API認証キー（※セキュリティ保護のためGit管理対象外）
```

## ⚙️ Installation (導入方法)

ソースコードから実行する場合の手順です。

1. **リポジトリのクローン**
   ```bash
   git clone https://github.com/ta-sekig/suumo-auto-scraper.git
   cd suumo-auto-scraper
   ```

2. **依存ライブラリのインストール**
   ```bash
   pip install -r requirements.txt
   ```

## 🔑 Configuration (設定)

本アプリは **Google Sheets API** を使用してデータを書き込みます。利用には以下の事前設定が必要です。

### 1. Google Cloud設定と鍵の発行
1. [Google Cloud Console](https://console.cloud.google.com/) にアクセスし、新しいプロジェクトを作成します。
2. 左メニューの「APIとサービス」→「ライブラリ」から、以下の2つを検索して**有効化**してください。
   * **Google Sheets API**
   * **Google Drive API**
3. 「認証情報」→「認証情報の作成」→「サービスアカウント」を選択し、アカウントを作成します。
4. 作成したサービスアカウントを選択し、「キー」タブから **「鍵を追加」→「新しい鍵を作成」→「JSON」** を選択します。
5. 自動的にダウンロードされたJSONファイルを、**`secret_key.json`** という名前に変更してください。

### 2. ファイルの配置
リネームした `secret_key.json` を、`suumo_gui.py` と同じフォルダ（プロジェクトのルート）に配置してください。

> **⚠️ 重要:** `secret_key.json` にはパスワード情報が含まれます。**絶対にGitHubへアップロードしないでください。**（`.gitignore` に除外設定済みであることを確認してください）

### 3. スプレッドシートの権限付与
これを行わないと「書き込み権限エラー」になります。

1. データを書き込みたい Googleスプレッドシート を新規作成（または開く）します。
2. ダウンロードした `secret_key.json` をテキストエディタで開き、`client_email` の横にあるメールアドレス（例: `xxx@project-name.iam.gserviceaccount.com`）をコピーします。
3. スプレッドシート右上の **「共有」** ボタンを押し、そのメールアドレスを貼り付けます。
4. 権限を **「編集者」** に設定して「送信」を押します。
5. スプレッドシートのURLから **スプレッドシートID**（`/d/` と `/edit` の間の文字列）をコピーし、コード内の設定箇所に貼り付けます。

## 🚀 Usage (利用方法)

### A. Pythonで直接起動する場合
開発環境で動作確認をする場合は以下のコマンドを実行します。
```bash
python suumo_gui.py
```

### B. EXEファイルを作成する場合 (Windows向け)
自身で実行ファイルをビルドしたい場合は、以下のコマンドを実行します。
```bash
pyinstaller --name="SuumoScraper" --onefile --noconsole --add-data "secret_key.json;." suumo_gui.py
```
実行後、`dist` フォルダの中に `SuumoScraper.exe` が生成されます。