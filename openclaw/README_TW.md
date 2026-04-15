# @mem0/openclaw-mem0

[OpenClaw](https://github.com/openclaw/openclaw) 代理程式的長期記憶，由 [Mem0](https://mem0.ai) 提供支援。

您的代理程式在會話之間會忘記一切。此外掛可以修復這個問題——它會監看對話、擷取重要資訊，並在相關時自動帶回。

## 快速開始

```bash
openclaw plugins install @mem0/openclaw-mem0
```

### 平台（Mem0 雲端）

從 [app.mem0.ai](https://app.mem0.ai) 取得 API 金鑰：

```bash
openclaw mem0 init --api-key <your-key> --user-id <your-user-id>
```

或在 `openclaw.json` 中手動配置：

```json5
"openclaw-mem0": {
  "enabled": true,
  "config": {
    "apiKey": "${MEM0_API_KEY}",
    "userId": "alice"
  }
}
```

### 開源（自托管）

不需要 Mem0 金鑰。預設需要 `OPENAI_API_KEY` 用於嵌入和 LLM。

```json5
"openclaw-mem0": {
  "enabled": true,
  "config": {
    "mode": "open-source",
    "userId": "alice"
  }
}
```

透過 `oss` 區塊自訂嵌入器、向量儲存庫或 LLM：

```json5
"config": {
  "mode": "open-source",
  "userId": "alice",
  "oss": {
    "embedder": { "provider": "openai", "config": { "model": "text-embedding-3-small" } },
    "vectorStore": { "provider": "qdrant", "config": { "host": "localhost", "port": 6333 } },
    "llm": { "provider": "openai", "config": { "model": "gpt-4o" } }
  }
}
```

所有 `oss` 欄位都是可選的。請參閱 [Mem0 OSS 文件](https://docs.mem0.ai/open-source/node-quickstart) 取得支援的提供者。

##運作原理

<p align="center">
  <img src="https://raw.githubusercontent.com/mem0ai/mem0/main/docs/images/openclaw-architecture.png" alt="Architecture" width="800" />
</p>

**自動回憶** — 代理程式回應前，外掛會搜尋 Mem0 中的相關記憶並將它們注入上下文。

**自動擷取** — 代理程式回應後，對話會透過噪音消除管道過濾並傳送至 Mem3。新的事實會被儲存、過時的會被更新、重複的會被合併。

兩者都安靜地執行。不需要提示詞，也不需要手動呼叫。

### 記憶範圍

| 範圍 | 說明 |
|-------|-------------|
| **會話（短期）** | 透過 `run_id` 作用域限定為目前對話的記憶。會與長期記憶一起自動回憶。 |
| **用戶（長期）** | 跨所有會話的持久化記憶。透過 `memory_add` 儲存，`longTerm: true`（這是預設值）。 |

在自動回憶期間，兩個範圍都會被搜尋並分開呈現——先長期，然後會話——這樣代理程式就有完整的上下文。

### 多代理程式隔離

在多代理程式設定中，每個代理程式都會自動取得自己的記憶命名空間。符合 `agent:<name>:<uuid>` 的會話金鑰會將記憶路由至 `userId:agent:<name>`。單一代理程式部署不受影響。

所有記憶工具都接受可選的 `agentId` 參數用於跨代理程式查詢：

```
memory_search({ query: "user's tech stack", agentId: "researcher" })
```

## 代理程式工具

會話期間有七個工具可供代理程式使用：

| 工具 | 說明 |
|------|-------------|
| **`memory_search`** | 以自然語言語查詢搜尋記憶。支援 `scope`（`session`、`long-term`、`all`）和 `agentId` 篩選。 |
| **`memory_add`** | 將事實儲存到記憶。支援 `category`、`importance`、`longTerm` 和 `agentId`。 |
| **`memory_get`** | 透過 ID 擷取特定記憶。 |
| **`memory_list`** | 列出儲存的記憶，可選 `userId`、`agentId` 和 `limit` 篩選。 |
| **`memory_update`** | 就地更新現有記憶的文字。保留編輯歷史。 |
| **`memory_delete`** | 透過 ID、搜尋查詢或大量刪除（`all: true`）。大量刪除需要 `confirm: true`。 |
| **`memory_history`** | 查看特定記憶的編輯歷史。 |

## CLI

所有命令都遵循模式 `openclaw mem0 <command>`。

### 記憶操作

```bash
# 新增記憶
openclaw mem0 add "User prefers TypeScript over JavaScript"

# 搜尋記憶
openclaw mem0 search "what languages does the user know"
openclaw mem0 search "preferences" --scope long-term
openclaw mem0 search "context" --scope session

# 取得、列出、更新、刪除
openclaw mem0 get <memory_id>
openclaw mem0 list --user-id alice --top-k 20
openclaw mem0 update <memory_id> "Updated preference text"
openclaw mem0 delete <memory_id>
openclaw mem0 delete --all --user-id alice --confirm

# 查看編輯歷史
openclaw mem0 history <memory_id>
```

### 管理

```bash
# 驗證和配置
openclaw mem0 init
openclaw mem0 init --api-key <key> --user-id alice

# 檢查連線
openclaw mem0 status

# 管理配置
openclaw mem0 config show
openclaw mem0 config get api_key
openclaw mem0 config set user_id alice

# 記憶整合（檢視、合併、修剪）
openclaw mem0 dream
openclaw mem0 dream --dry-run
```

## 配置參考

### 一般

| 金鑰 | 類型 | 預設值 | 說明 |
|-----|------|---------|-------------|
| `mode` | `"platform"` \| `"open-source"` | `"platform"` | 後端模式 |
| `userId` | `string` | `"default"` | 用戶的唯一識別碼。您定義的——儀表板中找不到。所有記憶都作用域於此值。 |
| `autoRecall` | `boolean` | `true` | 在每回合前注入相關記憶 |
| `autoCapture` | `boolean` | `true` | 每回合後擷取並儲存事實 |
| `topK` | `number` | `5` | 每次回憶傳回的最大記憶數量 |
| `searchThreshold` | `number` | `0.5` | 最低相似度分數 (0-1) |

### 平台模式

| 金鑰 | 類型 | 預設值 | 說明 |
|-----|------|---------|-------------|
| `apiKey` | `string` | — | **必填。** Mem0 API 金鑰（支援 `${MEM0_API_KEY}`）|
| `orgId` | `string` | — | 組織 ID |
| `projectId` | `string` | — | 專案 ID |
| `enableGraph` | `boolean` | `false` | 啟用實體圖進行關係追蹤 |
| `customInstructions` | `string` | *(內建)* | 自訂擷取規則，要儲存的內容和格式 |
| `customCategories` | `object` | *(12 個預設值)* | 記憶標籤的類別名稱至描述映射 |

### 開源模式

以下所有欄位都是可選的。預設使用 OpenAI 嵌入、記憶體向量儲存庫和 OpenAI LLM。

| 金鑰 | 類型 | 預設值 | 說明 |
|-----|------|---------|-------------|
| `customPrompt` | `string` | *(內建)* | 記憶處理的擷取提示詞 |
| `oss.embedder.provider` | `string` | `"openai"` | 嵌入提供者 |
| `oss.embedder.config` | `object` | — | 提供者配置（`apiKey`、`model`、`baseURL`）|
| `oss.vectorStore.provider` | `string` | `"memory"` | 向量儲存庫提供者 |
| `oss.vectorStore.config` | `object` | — | 提供者配置（`host`、`port`、`collectionName`）|
| `oss.llm.provider` | `string` | `"openai"` | LLM 提供者 |
| `oss.llm.config` | `object` | — | 提供者配置（`apiKey`、`model`、`baseURL`）|
| `oss.historyDbPath` | `string` | — | 記憶編輯歷史的 SQLite 路徑 |
| `oss.disableHistory` | `boolean` | `false` | 略過歷史 DB 初始化 |

支援的提供者：`openai`、`anthropic`、`ollama`、`lmstudio`、`qdrant`、`chroma` 等。請參閱 [Mem0 OSS 文件](https://docs.mem0.ai/open-source/node-quickstart) 取得完整清單。

## 授權

Apache 2.0