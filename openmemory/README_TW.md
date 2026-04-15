# OpenMemory

OpenMemory 是您的 LLM 個人記憶層——私密、可攜帶且開源。您的記憶保存在本地，讓您完全掌控自己的資料。在建立具有個人化記憶的 AI 應用程式的同時確保資料安全。

![OpenMemory](https://github.com/user-attachments/assets/3c701757-ad82-4afa-bfbe-e049c2b4320b)

## 簡易設定

### 前置條件
- Docker
- OpenAI API Key

您可以透過執行以下命令快速執行 OpenMemory：

```bash
curl -sL https://raw.githubusercontent.com/mem0ai/mem0/main/openmemory/run.sh | bash
```

您應該將 `OPENAI_API_KEY` 設為全域環境變數：

```bash
export OPENAI_API_KEY=your_api_key
```

您也可以將 `OPENAI_API_KEY` 作為腳本參數設定：

```bash
curl -sL https://raw.githubusercontent.com/mem0ai/mem0/main/openmemory/run.sh | OPENAI_API_KEY=your_api_key bash
```

## 前置條件

- Docker 和 Docker Compose
- Python 3.9+（用於後端開發）
- Node.js（用於前端開發）
- OpenAI API Key（用於 LLM 互動，執行 `cp api/.env.example api/.env` 然後將 **OPENAI_API_KEY** 改為您的）

## 快速開始

### 1. 設定環境變數

執行專案之前，您需要為 API 和 UI 配置環境變數。

您可以透過以下方式之一執行：

- **手動**：  
  在以下每個目錄中建立 `.env` 檔案：
  - `/api/.env`
  - `/ui/.env`

- **使用 `.env.example` 檔案**：  
  複製並重新命名範例檔案：

  ```bash
  cp api/.env.example api/.env
  cp ui/.env.example ui/.env
  ```

 - **使用 Makefile**（如果支援）：  
   執行：
  
   ```bash
   make env
   ```
- #### 範例 `/api/.env`

```env
OPENAI_API_KEY=sk-xxx
USER=<user-id> # The User Id you want to associate the memories with
```

- #### LLM 配置（可選）

預設情況下，OpenMemory 使用 OpenAI（`gpt-4o-mini`）作為 LLM 和嵌入器。您可以在 `/api/.env` 中使用這些環境變數配置不同的提供者：

| 變數 | 說明 | 預設值 |
|---|---|---|
| `LLM_PROVIDER` | LLM 提供者（`openai`、`ollama`、`anthropic`、`groq`、`together`、`deepseek` 等）| `openai` |
| `LLM_MODEL` | LLM 提供者的模型名稱 | `gpt-4o-mini` (OpenAI) / `llama3.1:latest` (Ollama) |
| `LLM_API_KEY` | LLM 提供者的 API 金鑰 | `OPENAI_API_KEY` 環境變數 |
| `LLM_BASE_URL` | LLM API 的自訂基礎 URL | 提供者預設 |
| `OLLAMA_BASE_URL` | Ollama 特定的基礎 URL（對於 Ollama 優先於 `LLM_BASE_URL`）| `http://localhost:11434` |
| `EMBEDDER_PROVIDER` | 嵌入器提供者（當 LLM 是 Ollama 時預設為 `ollama`，否則為 `openai`）| `openai` |
| `EMBEDDER_MODEL` | 嵌入器的模型名稱 | `text-embedding-3-small` (OpenAI) / `nomic-embed-text` (Ollama) |
| `EMBEDDER_API_KEY` | 嵌入器提供者的 API 金鑰 | `OPENAI_API_KEY` 環境變數 |
| `EMBEDDER_BASE_URL` | 嵌入器 API 的自訂基礎 URL | 提供者預設 |

**範例：使用 Ollama（完全本地）**
```env
LLM_PROVIDER=ollama
LLM_MODEL=llama3.1:latest
EMBEDDER_PROVIDER=ollama
EMBEDDER_MODEL=nomic-embed-text
OLLAMA_BASE_URL=http://localhost:11434
```

**範例：使用 Anthropic**
```env
LLM_PROVIDER=anthropic
LLM_MODEL=claude-sonnet-4-20250514
LLM_API_KEY=sk-ant-xxx
```
- #### 範例 `/ui/.env`

```env
NEXT_PUBLIC_API_URL=http://localhost:8765
NEXT_PUBLIC_USER_ID=<user-id> # Same as the user id for environment variable in api
```

### 2. 建置並執行專案

您可以使用以下兩個命令執行專案：
```bash
make build # 建置 mcp 伺服器和 ui
make up  # 執行 openmemory mcp 伺服器和 ui
```

執行這些命令後，您將擁有：
- OpenMemory MCP 伺服器執行於：http://localhost:8765（API 文件於 http://localhost:8765/docs）
- OpenMemory UI 執行於：http://localhost:3000

#### UI 在 `localhost:3000` 無法運作？

如果 UI 在 [http://localhost:3000](http://localhost:3000) 無法正常啟動，請嘗試手動執行：

```bash
cd ui
pnpm install
pnpm dev
```

### MCP 用戶端設定

使用以下一步命令將 OpenMemory Local MCP 配置到用戶端。一般命令格式如下：

```bash
npx @openmemory/install local http://localhost:8765/mcp/<client-name>/sse/<user-id> --client <client-name>
```

將 `<client-name>` 替換為所需的用戶端名稱，`<user-id>` 替換為您在環境變數中指定的值。

## 專案結構

- `api/` - 後端 API + MCP 伺服器
- `ui/` - 前端 React 應用程式

## 貢獻

我們是一個對 AI 和開源軟體未來充滿熱情的開發團隊。多年在這兩個領域的經驗，我們相信社群驅動開發的力量，並很高興能建立使 AI 更易於存取和個人化的工具。

我們歡迎各種形式的貢獻：
- 錯誤回報和功能請求
- 文件改進
- 程式碼貢獻
- 測試和回饋
- 社群支援

如何貢獻：

1. 分叉儲存庫
2. 建立您的功能分支（`git checkout -b openmemory/feature/amazing-feature`）
3. 提交您的更改（`git commit -m 'Add some amazing feature'`）
4. 推送到分支（`git push origin openmemory/feature/amazing-feature`）
5. 開啟 Pull Request

加入我們一起建立 AI 記憶管理的未來！您的貢獻可以幫助每個人讓 OpenMemory 变得更好。