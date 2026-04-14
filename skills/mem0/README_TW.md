# Mem0 Skill for Claude

使用 [Mem0 平台](https://app.mem0.ai) 在幾分鐘內為任何 AI 應用程式新增持久化記憶。

## 此 Skill 的功能

安裝後，Claude 可以：

- 在您的 Python 或 TypeScript 專案中 **設定 Mem0**
- 將記憶 **整合** 到您現有的 AI 應用程式中（LangChain、CrewAI、Vercel AI、OpenAI Agents、LangGraph、LlamaIndex 等）
- 使用真實 API 參考和經過測試的模式 **產生可運作的程式碼**
- 按需 **搜尋即時文檔** 以取得最新的 Mem0 文件

## 安裝

### CLI（Claude Code、OpenCode、OpenClaw 或任何支援 skills 的工具）

```bash
npx skills add https://github.com/mem0ai/mem0 --skill mem0
```

### Claude.ai

1. 將此 `skills/mem0` 資料夾下載為 ZIP
2. 前往 **設定 > 功能 > Skills**
3. 點擊 **上傳 skill** 並選擇 ZIP

### Claude API（Skills API）

```bash
curl -X POST https://api.anthropic.com/v1/skills \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "mem0", "source": "https://github.com/mem0ai/mem0/tree/main/skills/mem0"}'
```

### 前置條件

- Mem0 平台 API 金鑰（[從這裡取得](https://app.mem0.ai/dashboard/api-keys)）
- Python 3.10+ 或 Node.js 18+
- 設定環境變數：

  ```bash
  export MEM0_API_KEY="m0-your-api-key"
  ```

## 快速開始

安裝後，只需詢問 Claude：

- 「在我的專案中設定 mem0」
- 「將記憶添加到我的聊天機器人」
- 「幫我搜尋帶有篩選器的用戶記憶」
- 「將 mem0 整合到我的 LangChain 應用程式中」
- 「新增圖形記憶來追蹤實體關係」

## 內含內容

```text
skills/mem0/
├── SKILL.md                    # Skill 定義和說明
├── README.md                   # 本檔案
├── LICENSE                     # Apache-2.0
├── scripts/
│   └── mem0_doc_search.py      # 按需搜尋即時 Mem0 文檔
└── references/                 # 文件（按需載入）
    ├── quickstart.md           # 完整快速開始（Python、TS、cURL）
    ├── sdk-guide.md            # 所有 SDK 方法（Python + TypeScript）
    ├── api-reference.md        # REST 端點、篩選器、記憶物件
    ├── architecture.md         # 處理管道、生命週期、範圍設定、效能
    ├── features.md             # 檢索、圖形、類別、MCP、Webhook、多模態
    ├── integration-patterns.md # LangChain、CrewAI、Vercel AI、LangGraph、LlamaIndex 等
    └── use-cases.md            # 7 個真實世界的模式，包含 Python + TypeScript 程式碼
```

## 連結

- [Mem0 平台儀表板](https://app.mem0.ai)
- [Mem0 文件](https://docs.mem0.ai)
- [Mem0 GitHub](https://github.com/mem0ai/mem0)
- [API 參考](https://docs.mem0.ai/api-reference)

## 授權

Apache-2.0