# mem0 CLI

這是 [mem0](https://mem0.ai) 的官方命令列介面 — AI 代理的記憶層。適用於 Mem0 Platform API。提供 Python 和 Node.js 兩種版本。

> **針對 AI 代理：** 在任何命令上傳遞 `--agent`（或 `--json`）可獲得專為工具循環設計的結構化 JSON 輸出 — 清理過的欄位、沒有顏色或旋轉指示器、錯誤以 JSON 格式呈獻。請參閱下面的[代理模式](#agent-mode)。

## 安裝

```bash
npm install -g @mem0/cli
```

```bash
pip install mem0-cli
```

這兩個套件都會安裝具有相同行為的 `mem0` 二進位檔。

## 快速開始

```bash
# 互動式設定精靈
mem0 init

# 或透過電子郵件登入（取得新的 API 金鑰）
mem0 init --email alice@company.com

# 或使用現有的 API 金鑰進行身份驗證
mem0 init --api-key m0-xxx

# 新增記憶
mem0 add "I prefer dark mode and use vim keybindings" --user-id alice

# 搜尋記憶
mem0 search "What are Alice's preferences?" --user-id alice

# 列出使用者的所有記憶
mem0 list --user-id alice

# 更新記憶
mem0 update <memory-id> "I switched to light mode"

# 刪除記憶
mem0 delete <memory-id>
```

## 命令

| 命令 | 說明 |
|---------|-------------|
| `mem0 init` | 設定精靈 — 透過電子郵件登入或手動設定 API 金鑰 |
| `mem0 add` | 從文字、JSON 訊息、檔案或標準輸入新增記憶 |
| `mem0 search` | 使用自然語言搜尋記憶 |
| `mem0 list` | 列出記憶，可選用篩選和分頁 |
| `mem0 get` | 透過 ID 擷取特定記憶 |
| `mem0 update` | 更新記憶的文字或中繼資料 |
| `mem0 delete` | 刪除單一記憶、某個範圍內的所有記憶或實體 |
| `mem0 import` | 從 JSON 檔案大量匯入記憶 |
| `mem0 config` | 查看或修改 CLI 設定 |
| `mem0 entity` | 列出或刪除實體（使用者、代理、應用程式、執行） |
| `mem0 event` | 檢視背景處理事件（大量刪除、大型新增任務） |
| `mem0 status` | 驗證 API 連線並顯示目前專案 |
| `mem0 version` | 顯示 CLI 版本 |

執行 `mem0 <command> --help` 以取得任何命令的詳細使用說明。

## 代理模式

在任何命令上傳遞 `--agent`（或其別名 `--json」）作為**全域旗標**，以獲得專為 AI 代理工具循環設計的輸出：

```bash
mem0 --agent search "user preferences" --user-id alice
mem0 --agent add "User prefers dark mode" --user-id alice
mem0 --agent list --user-id alice
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

## 實作

| 語言 | 目錄 | 套件 | 文件 |
----------|-----------|---------|------|
| TypeScript | [`node/`](./node/) | `@mem0/cli` | [README](./node/README.md) |
| Python | [`python/`](./python/) | `mem0-cli` | [README](./python/README.md) |

## 文件

完整文件可在 [docs.mem0.ai/platform/cli](https://docs.mem0.ai/platform/cli) 取得。

## 授權

Apache-2.0