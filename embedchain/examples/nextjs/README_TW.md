在 [Github](https://github.com/embedchain/embedchain) 上 fork 此 repo，以建立由 Embedchain 應用程式驅動您自己的 NextJS Discord 和 Slack 機器人。

如果您在 fork 時遇到問題，請參考 [github docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) 來 fork repo。

我們將在 examples/nextjs 資料夾中工作，因此請執行命令 `cd <your_forked_repo>/examples/nextjs` 來更改您目前的工作目錄。

# 安裝

首先，讓我們開始安裝所有必需的套件和依賴。

- 執行 `pip install -r requirements.txt` 來安裝所有必需的 Python 套件。

- 我們將使用 [Fly.io](https://fly.io/) 來部署我們的 embedchain 應用程式和 discord/slack 機器人。按照第一步安裝 [Fly.io CLI](https://docs.embedchain.ai/deployment/fly_io#step-1-install-flyctl-command-line)。

# 開發

## Embedchain 應用程式

首先，讓我們開始建立一個由 NextJS 知識驅動的 Embedchain 應用程式。我們已經在 `ec_app` 資料夾中為您使用 FastAPI 建立了 embedchain 應用程式。請隨意攝入您選擇的資料來驅動應用程式。

---
**注意**

在此資料夾中建立 `.env` 檔案，並按照 `.env.example` 檔案所示設定您的 OpenAI API 金鑰。如果您想使用其他開源模型，請隨意在 `app.py` 中變更應用程式配置。有關使用 Embedchain 應用程式的自訂配置的更多詳細資訊[可在這裡取得](https://docs.embedchain.ai/api-reference/advanced/configuration)。

---

在執行 ec 命令來開發/部署應用程式之前，請打開 `fly.toml` 檔案並將 `name` 變數更新為唯一的名稱。這很重要，因為 `fly.io` 要求使用者提供全球唯一的部署應用程式名稱。

現在，我們需要使用 fly.io 啟動此應用程式。您可以在 [fly.io dashboard](https://fly.io/dashboard) 上看到您的應用程式。執行以下命令在 fly.io 上啟動您的應用程式：
```bash
fly launch --no-deploy
```

若要在開發環境中執行應用程式：

```bash
ec dev  #若要在開發環境中執行應用程式
```

執行 `ec deploy` 將您的應用程式部署到 Fly.io。部署應用程式後，儲存我們的 Discord 和 Slack 機器人將發送請求的端點。

## Discord 機器人

對於 Discord 機器人，您需要在 Discord 開發者入口網站上建立機器人，並取得 Discord 機器人權杖和您的 Discord 機器人名稱。

牢記以下注意要點，按照我們的 [discord 機器人文件](https://docs.embedchain.ai/examples/discord_bot) 中的說明建立 Discord 機器人，並取得 Discord 機器人權杖。

---
**注意**

您不需要設定 `OPENAI_API_KEY` 即可執行此 Discord 機器人。按照剩餘說明建立 Discord 機器人應用程式。我們建議您提供以下機器人權限集合，以確保 Discord 機器人無錯誤地執行：

```
（一般權限）
讀取訊息/檢視頻道

（文字權限）
傳送訊息
建立公開討論串
建立私人討論串
在討論串中傳送訊息
管理討論串
嵌入連結
讀取訊息歷史
```
---

一旦您有了 Discord 機器人權杖和 Discord 應用程式名稱。導航至 `nextjs_discord` 資料夾，並建立 `.env` 檔案，按照 `.env.example` 檔案所示定義您的 Discord 機器人權杖、Discord 機器人名稱和您的 embedchain 應用程式端點。

若要在開發環境中執行應用程式：

```bash
python app.py  #若要在開發環境中執行應用程式
```

在部署應用程式之前，請打開 `fly.toml` 檔案並將 `name` 變數更新為唯一的名稱。這很重要，因為 `fly.io` 要求使用者提供全球唯一的部署應用程式名稱。

現在，我們需要使用 fly.io 啟動此應用程式。您可以在 [fly.io dashboard](https://fly.io/dashboard) 上看到您的應用程式。執行以下命令在 fly.io 上啟動您的應用程式：
```bash
fly launch --no-deploy
```

執行 `ec deploy` 將您的應用程式部署到 Fly.io。部署應用程式後，您的 Discord 機器人將上線！

## Slack 機器人

對於 Slack 機器人，您需要在 Slack 開發者入口網站上建立機器人，並取得 Slack 機器人權杖和 Slack 應用程式權杖。

### 設定

- 如果您還沒有工作區，請點擊[這裡](https://slack.com/intl/en-in/)建立一個 Slack 工作區。
- 前往[這裡](https://api.slack.com/apps)在您的 Slack 帳戶上建立新的應用程式。
- 選擇「從頭開始」，然後輸入機器人名稱並選擇您的工作區。
- 從左側邊欄進入「基本資訊」標籤的「應用程式憑證」部分，建立您的應用程式權杖並將其儲存在您的 `.env` 檔案中作為 `SLACK_APP_TOKEN`。
- 從左側邊欄進入「Socket Mode」標籤，啟用 Socket Mode 以監聽來自您工作區的 Slack 訊息。
- （選用）在「應用程式首頁」標籤下，您可以變更應用程式的顯示名稱和預設名稱。
- 導航至「事件訂閱」標籤，啟用事件訂閱，以便我們可以監聽 Slack 事件。
- 一旦啟用事件訂閱，您將需要訂閱機器人事件，以授權機器人監聽機器人的應用程式提及事件。透過點擊「新增機器人使用者事件」按鈕並選擇 `app_mention` 來完成此操作。
- 在左側邊欄上，前往「OAuth 和權限」，並在「機器人權杖權限」下新增以下範圍：
```text
app_mentions:read
channels:history
channels:read
chat:write
emoji:read
reactions:write
reactions:read
```
- 現在選擇「安裝到工作區」選項，完成後，複製「機器人使用者 OAuth 權杖」並將其設定在您的 `.env` 檔案中作為 `SLACK_BOT_TOKEN`。

一旦您有了 Slack 機器人權杖和 Slack 應用程式權杖。導航至 `nextjs_slack` 資料夾，並建立 `.env` 檔案，按照 `.env.example` 檔案所示定義您的 Slack 機器人權杖、Slack 應用程式權杖和您的 embedchain 應用程式端點。

若要在開發環境中執行應用程式：

```bash
python app.py  #若要在開發環境中執行應用程式
```

在部署應用程式之前，請打開 `fly.toml` 檔案並將 `name` 變數更新為唯一的名稱。這很重要，因為 `fly.io` 要求使用者提供全球唯一的部署應用程式名稱。

現在，我們需要使用 fly.io 啟動此應用程式。您可以在 [fly.io dashboard](https://fly.io/dashboard) 上看到您的應用程式。執行以下命令在 fly.io 上啟動您的應用程式：
```bash
fly launch --no-deploy
```

執行 `ec deploy` 將您的應用程式部署到 Fly.io。部署應用程式後，您的 Slack 機器人將上線！