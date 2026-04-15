# Claude 的 Mem0 Skill

使用 [Mem0 Platform](https://app.mem0.ai) 在幾分鐘內為任何 AI 應用程式新增持久記憶功能。

## 這個 Skill 的功能

安裝後，Claude 可以：

- 在您的 Python 或 TypeScript 專案中 **設定 Mem0**
- 將記憶功能 **整合** 到您現有的 AI 應用程式中（LangChain、CrewAI、Vercel AI、OpenAI Agents、LangGraph、LlamaIndex 等）
- 使用真實的 API 參考和經過測試的 pattern **產生可運作的程式碼**
- 根據需求 **搜尋即時文件** 以取得最新的 Mem0 文件

## 安裝

安裝 Mem0 外掛時會自動包含此 skill：

```
/plugin marketplace add mem0ai/mem0
/plugin install mem0@mem0-plugins
```

請參考 [外掛 README](../../README.md) 取得完整的設定說明。

### 前置需求

- Mem0 Platform API 金鑰（[在此取得](https://app.mem0.ai/dashboard/api-keys)）
- Python 3.10+ 或 Node.js 18+
- 設定環境變數：

  ```bash
  export MEM0_API_KEY="m0-your-api-key"
  ```

## 快速開始

安裝後，只需詢問 Claude：

- 「在我的專案中設定 mem0」
- 「為我的聊天機器人新增記憶功能」
- 「幫我使用篩選器搜尋使用者記憶」
- 「將 mem0 整合到我的 LangChain 應用程式」
- 「新增圖形記憶來追蹤實體關係」

## 內容說明

```text
skills/mem0/
├── SKILL.md                    # Skill 定義和說明
├── README.md                   # 本檔案
├── LICENSE                     # Apache-2.0
├── scripts/
│   └── mem0_doc_search.py      # 按需求搜尋即時 Mem0 文件
└── references/                 # 文件（按需求載入）
    ├── quickstart.md           # 完整快速開始（Python、TS、cURL）
    ├── sdk-guide.md            # 所有 SDK 方法（Python + TypeScript）
    ├── api-reference.md        # REST 端點、篩選器、記憶物件
    ├── architecture.md         # 處理流程、生命週期、範圍設定、效能
    ├── features.md             # 擷取、圖形、類別、MCP、網頁钩子、多模態
    ├── integration-patterns.md # LangChain、CrewAI、Vercel AI、LangGraph、LlamaIndex 等
    └── use-cases.md            # 7 個真實世界範例（含 Python + TypeScript 程式碼）
```

## 相關連結

- [Mem0 Platform 控制面板](https://app.mem0.ai)
- [Mem0 文件](https://docs.mem0.ai)
- [Mem0 GitHub](https://github.com/mem0ai/mem0)
- [API 參考](https://docs.mem0.ai/api-reference)

## 授權

Apache-2.0