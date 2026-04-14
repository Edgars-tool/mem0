# mem0 CLI (Node.js)

這是 [mem0](https://mem0.ai) 的官方命令列介面 — AI 代理的記憶層。TypeScript 實作。

> **專為 AI 代理設計。** 在任何命令上傳遞 `--agent`（或 `--json`）作為全域旗標，可獲得專為程式化設計的結構化 JSON 輸出 — 清理過的欄位、沒有顏色或旋轉指示器，錯誤也以 JSON 呈現。

## 前置條件

- pnpm (`npm install -g pnpm`) — 僅用於開發

## 安裝

```bash
npm install -g @mem0/cli
```

## 快速開始

```bash
# 互動式設定精靈
mem0 init

# 或透過電子郵件登入
mem0 init --email alice@company.com

# 或使用現有的 API 金鑰進行身份驗證
mem0 init --api-key m0-xxx

# 新增記憶
mem0 add "I prefer dark mode and use vim keybindings" --user-id alice

# 搜尋記憶
mem0 search "What are Alice's preferences?" --user-id alice

# 列出使用者的所有記憶
mem0 list --user-id alice

# 取得特定記憶
mem0 get <memory-id>

# 更新記憶
mem0 update <memory-id> "I switched to light mode"

# 刪除記憶
mem0 delete <memory-id>
```

## 命令

### `mem0 init`

互動式設定精靈。提示輸入您的 API 金鑰和預設使用者 ID。

```bash
mem0 init
mem0 init --api-key m0-xxx --user-id alice
mem0 init --email alice@company.com
```

如果偵測到現有設定，CLI 會在覆蓋前詢問確認。使用 `--force` 跳過提示（在 CI/CD 中很有用）。

```bash
mem0 init --api-key m0-xxx --user-id alice --force
```

| 旗標 | 說明 |
------|-------------|
| `--api-key` | API 金鑰（跳過提示） |
| `-u, --user-id` | 預設使用者 ID（跳過提示） |
| `--email` | 透過電子郵件驗證碼登入 |
| `--code` | 驗證碼（與 `--email` 搭配使用以進行非互動式登入） |
| `--force` | 覆寫現有設定而不需確認 |

### `mem0 add`

從文字、JSON 訊息陣列、檔案或標準輸入新增記憶。

```bash
mem0 add "I prefer dark mode" --user-id alice
mem0 add --file conversation.json --user-id alice
echo "Loves hiking on weekends" | mem0 add --user-id alice
```

| 旗標 | 說明 |
------|-------------|
| `-u, --user-id` | 限定於某個使用者 |
| `--agent-id` | 限定於某個代理 |
| `--messages` | 作為 JSON 的對話訊息 |
| `-f, --file` | 從 JSON 檔案讀取訊息 |
| `-m, --metadata` | 作為 JSON 的自訂中繼資料 |
| `--categories` | 類別（JSON 陣列或逗號分隔） |
| `--graph / --no-graph` | 啟用或停用圖形記憶擷取 |
| `-o, --output` | 輸出格式：`text`、`json`、`quiet` |

### `mem0 search`

使用自然語言搜尋記憶。

```bash
mem0 search "dietary restrictions" --user-id alice
mem0 search "preferred tools" --user-id alice --output json --top-k 5
```

| 旗標 | 說明 |
------|-------------|
| `-u, --user-id` | 按使用者篩選 |
| `-k, --top-k` | 結果數量（預設：10） |
| `--threshold` | 最小相似度分數（預設：0.3） |
| `--rerank` | 啟用重新排序 |
| `--keyword` | 使用關鍵字搜尋而非語義搜尋 |
| `--filter` | 進階篩選表達式（JSON） |
| `--graph / --no-graph` | 在搜尋中啟用或停用圖形 |
| `-o, --output` | 輸出格式：`text`、`json`、`table` |

### `mem0 list`

列出記憶，可選用篩選和分頁。

```bash
mem0 list --user-id alice
mem0 list --user-id alice --category preferences --output json
mem0 list --user-id alice --after 2024-01-01 --page-size 50
```

| 旗標 | 說明 |
------|-------------|
| `-u, --user-id` | 按使用者篩選 |
| `--page` | 頁碼（預設：1） |
| `--page-size` | 每頁結果數（預設：100） |
| `--category` | 按類別篩選 |
| `--after` | 建立於此日期之後（YYYY-MM-DD） |
| `--before` | 建立於此日期之前（YYYY-MM-DD） |
| `-o, --output` | 輸出格式：`text`、`json`、`table` |

### `mem0 get`

透過 ID 擷取特定記憶。

```bash
mem0 get 7b3c1a2e-4d5f-6789-abcd-ef0123456789
mem0 get 7b3c1a2e-4d5f-6789-abcd-ef0123456789 --output json
```

### `mem0 update`

更新現有記憶的文字或中繼資料。

```bash
mem0 update <memory-id> "Updated preference text"
mem0 update <memory-id> --metadata '{"priority": "high"}'
echo "new text" | mem0 update <memory-id>
```

### `mem0 delete`

刪除單一記憶、某個範圍內的所有記憶或整個實體。

```bash
# 刪除單一記憶
mem0 delete <memory-id>

# 刪除使用者的所有記憶
mem0 delete --all --user-id alice --force

# 刪除整個專案的所有記憶
mem0 delete --all --project --force

# 預覽將被刪除的內容
mem0 delete --all --user-id alice --dry-run
```

| 旗標 | 說明 |
------|-------------|
| `--all` | 刪除所有符合範圍篩選條件的記憶 |
| `--entity` | 刪除實體及其所有記憶 |
| `--project` | 搭配 `--all`：刪除整個專案的所有記憶 |
| `--dry-run` | 預覽而不刪除 |
| `--force` | 跳過確認提示 |

### `mem0 import`

從 JSON 檔案大量匯入記憶。

```bash
mem0 import data.json --user-id alice
```

該檔案應該是一個 JSON 陣列，其中每個項目都有 `memory`（或 `text` 或 `content`）欄位，以及選用的 `user_id`、`agent_id` 和 `metadata` 欄位。

### `mem0 config`

查看或修改本機 CLI 設定。

```bash
mem0 config show              # 顯示目前設定（隱藏密鑰）
mem0 config get api_key       # 取得特定值
mem0 config set user_id bob   # 設定值
```

### `mem0 entity`

列出或刪除實體（使用者、代理、應用程式、執行）。

```bash
mem0 entity list users
mem0 entity list agents --output json
mem0 entity delete --user-id alice --force
```

### `mem0 event`

檢視由非同步操作建立的背景處理事件（例如大量刪除、大型新增任務）。

```bash
# 列出最近的事件
mem0 event list

# 檢查特定事件的狀態
mem0 event status <event-id>
```

| 旗標 | 說明 |
------|-------------|
| `-o, --output` | 輸出格式：`text`、`json` |

### `mem0 status`

驗證您的 API 連線並顯示目前專案。

```bash
mem0 status
```

### `mem0 version`

顯示 CLI 版本。

```bash
mem0 version
```

## 代理模式

在任何命令上傳遞 `--agent`（或其別名 `--json`）作為**全域旗標**，以獲得專為 AI 代理工具循環設計的輸出：

```bash
mem0 --agent search "user preferences" --user-id alice
mem0 --agent add "User prefers dark mode" --user-id alice
mem0 --agent list --user-id alice
mem0 --agent delete --all --user-id alice --force
```

每個命令都會回傳相同形狀的信封：

```json
{
  "status": "success",
  "command": "search",
  "duration_ms": 134,
  "scope": { "user_id": "alice" },
  "count": 2,
  "data": [
    { "id": "abc-123", "memory": "User prefers dark mode", "score": 0.97, "created_at": "2026-01-15", "categories": ["preferences"] }
  ]
}
```

代理模式與 `--output json` 的不同之處：

- **清理過的 `data`**：僅包含代理需要的欄位（id、memory、score 等）— 沒有內部 API 雜訊
- **沒有人類輸出**：完全抑制旋轉指示器、顏色和橫幅
- **錯誤以 JSON 呈現**：錯誤以 `{"status": "error", "command": "...", "error": "..."}` 輸出到標準輸出，並附帶非零退出碼

使用 `mem0 help --json` 取得完整的命令樹狀結構 JSON — 對需要自我發現可用命令的代理很有用。

## 輸出格式

使用 `--output` 控制結果的顯示方式：

| 格式 | 說明 |
--------|-------------|
| `text` | 人類可讀，含顏色和格式（預設） |
| `json` | 結構化 JSON，可 pipe 到 `jq`（原始 API 回應） |
| `table` | 表格格式（`list` 的預設） |
| `quiet` | 極簡 — 僅 ID 或狀態碼 |
| `agent` | 結構化 JSON 信封，含清理過的欄位（由 `--agent`/`--json` 設定） |

## 全域旗標

這些旗標可用於所有命令：

| 旗標 | 說明 |
------|-------------|
| `--json` | 啟用代理模式：結構化 JSON 信封輸出，沒有顏色或旋轉指示器 |
| `--agent` | `--json` 的別名 |
| `--api-key` | 覆寫此請求的已設定 API 金鑰 |
| `--base-url` | 覆寫此請求的已設定 API 基礎 URL |
| `-o, --output` | 設定輸出格式 |

## 環境變數

| 變數 | 說明 |
----------|-------------|
| `MEM0_API_KEY` | API 金鑰（覆蓋設定檔） |
| `MEM0_BASE_URL` | API 基礎 URL |
| `MEM0_USER_ID` | 預設使用者 ID |
| `MEM0_AGENT_ID` | 預設代理 ID |
| `MEM0_APP_ID` | 預設應用程式 ID |
| `MEM0_RUN_ID` | 預設執行 ID |
| `MEM0_ENABLE_GRAPH` | 啟用圖形記憶（`true` / `false`） |

環境變數優先於設定檔中的值，設定檔中的值優先於預設值。

## 開發

```bash
cd cli/node
pnpm install

# 開發模式（直接執行 TypeScript，不需建置）
pnpm dev --help
pnpm dev add "test memory" --user-id alice
pnpm dev search "test" --user-id alice

# 或先建置，然後執行編譯後的 JS
pnpm build
node dist/index.js --help
```

## 文件

完整文件可在 [docs.mem0.ai/platform/cli](https://docs.mem0.ai/platform/cli) 取得。

## 授權

Apache-2.0