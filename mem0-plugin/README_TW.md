# Mem0 Plugin for Claude Code, Claude Cowork, Cursor & Codex

為您的 AI 工作流程新增持久化記憶。使用 Mem0 平台跨會話儲存、檢索和管理記憶。適用於 **Claude Code**（CLI）、**Claude Cowork**（桌面應用程式）、**Cursor** 和 **Codex**。

## 步驟 1：設置您的 API 金鑰

> **您必須先完成此步驟才能安裝外掛。**

1. 如果您還沒有帳戶，請在 [app.mem0.ai](https://app.mem0.ai) 註冊
2. 前往 [app.mem0.ai/dashboard/api-keys](https://app.mem0.ai/dashboard/api-keys)
3. 點擊 **建立 API 金鑰** 並複製金鑰（以 `m0-` 開頭）
4. 將其添加到您的 shell 配置檔：

   ```bash
   # For zsh (預設在 macOS)
   echo 'export MEM0_API_KEY="m0-your-api-key"' >> ~/.zshrc
   source ~/.zshrc

   # For bash
   echo 'export MEM0_API_KEY="m0-your-api-key"' >> ~/.bashrc
   source ~/.bashrc
   ```

5. 確認已設定：

   ```bash
   echo $MEM0_API_KEY
   # 應該會印出：m0-your-api-key
   ```

## 步驟 2：安裝外掛

請選擇以下選項之一。所有選項都需要先設定 `MEM0_API_KEY`（請參閱上方）。

### Claude Code (CLI) / Claude Cowork (Desktop)

Claude Code 和 Claude Cowork 使用相同的外掛系統。

**CLI：**

```
/plugin marketplace add mem0ai/mem0
/plugin install mem0@mem0-plugins
```

**Cowork 桌面應用程式：** 開啟 Cowork 標籤，在側邊欄中點擊 **自訂**，點擊 **瀏覽外掛**，然後安裝 Mem0。

這會安裝完整的外掛，包含 MCP 伺服器、生命周期鉤子（自動記憶擷取）和 Mem0 SDK skill。

### Codex

**選項 A — 儲存庫市集**（建議團隊使用）：

將外掛市集添加到您的儲存庫根目錄（已包含在此儲存庫中）：

```
.agents/plugins/marketplace.json
```

然後在 Codex 中，瀏覽儲存庫的外掛目錄並安裝 Mem0。

**選項 B — 個人市集**：

添加到 `~/.agents/plugins/marketplace.json`：

```json
{
  "name": "mem0-plugins",
  "interface": {
    "displayName": "Mem0 Plugins"
  },
  "plugins": [
    {
      "name": "mem0",
      "source": {
        "source": "local",
        "path": "/path/to/mem0/mem0-plugin"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

**選項 C — 手動 MCP 配置**：

添加到您的 Codex MCP 配置：

```json
{
  "mcpServers": {
    "mem0": {
      "type": "http",
      "url": "https://mcp.mem0.ai/mcp/",
      "headers": {
        "Authorization": "Token ${MEM0_API_KEY}"
      }
    }
  }
}
```

這會安裝 MCP 伺服器和 Mem0 SDK skill。Codex 使用基於 skill 的記憶協定，而非生命周期鉤子。

### Cursor

> **已設定 `mem0` 為 MCP 伺服器？** 在安裝前從您的 Cursor MCP 設定中移除現有項目，以避免重複的工具。

**選項 A — 一鍵 deep deeplink**（僅安裝 MCP 伺服器）：

[在 Cursor 中安裝 Mem0 MCP](cursor://anysphere.cursor-deeplink/mcp/install?name=mem0&config=eyJtY3BTZXJ2ZXJzIjp7Im1lbTAiOnsidXJsIjoiaHR0cHM6Ly9tY3AubWVtMC5haS9tY3AvIiwiaGVhZGVycyI6eyJBdXRob3JpemF0aW9uIjoiVG9rZW4gJHtlbnY6TUVNMF9BUElfS0VZfSJ9fX19)

**選項 B — 手動配置**（僅 MCP 伺服器）：

將以下內容添加到您的 `.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "mem0": {
      "url": "https://mcp.mem0.ai/mcp/",
      "headers": {
        "Authorization": "Token ${env:MEM0_API_KEY}"
      }
    }
  }
}
```

**選項 C — Cursor 市集**（包含 hooks 和 skills 的完整外掛）：

從 [Cursor 市集](https://cursor.com/marketplace) 安裝，以獲得包含生命周期鉤子和 Mem0 SDK skill 的完整體驗。

## 驗證是否正常運作

安裝後，確認 MCP 伺服器已連線：

1. 開始新會話（或重新啟動當前會話）
2. 詢問：「列出我的 mem0 實體」或「搜尋我的記憶 hello」
3. 如果 `mem0` 工具出現並回應，表示設定完成

## 包含的內容

| 元件 | Claude Code / Cowork | Cursor (市集) | Cursor (Deeplink/手動) | Codex |
|-----------|:--------------------:|:--------------------:|:------------------------:|:-----:|
| MCP 伺服器 | Yes | Yes | Yes | Yes |
| 生命周期鉤子 | Yes | Yes | No | No |
| Mem0 SDK Skill | Yes | Yes | No | Yes |
| 記憶協定 Skill | No | No | No | Yes |

- **MCP 伺服器** — 連線至 Mem0 遠端 MCP 伺服器 (`mcp.mem0.ai`)，提供新增、搜尋、更新和刪除記憶的工具。无需本地依賴。
- **生命周期鉤子** — 在關鍵點自動擷取記憶：會話開始、上下文壓縮、任務完成和會話結束。（僅適用於 Claude Code/Cursor）
- **Mem0 SDK Skill** — 指導 AI 如何將 Mem0 SDK（Python 和 TypeScript）整合到您的應用程式中。
- **記憶協定 Skill** — Codex 專用的 skill，指示代理程式在任務開始時檢索相關記憶、在完成時儲存學習成果，並在上下文丟失前擷取會話狀態。在不支援生命周期鉤子的平台上取代它們。

## MCP 工具

安裝後，以下工具可用：

| 工具 | 說明 |
|------|-------------|
| `add_memory` | 儲存用戶/代理程式的文字或對話歷史 |
| `search_memories` | 跨記憶進行語義搜尋（可篩選） |
| `get_memories` | 列出記憶（可篩選和分頁） |
| `get_memory` | 透過 ID 擷取特定記憶 |
| `update_memory` | 透過 ID 覆寫記憶的文字 |
| `delete_memory` | 透過 ID 刪除單一記憶 |
| `delete_all_memories` | 大量刪除範圍內的所有記憶 |
| `delete_entities` | 刪除用戶/代理程式/應用程式/執行實體及其記憶 |
| `list_entities` | 列出儲存在 Mem0 中的用戶/代理程式/應用程式/執行 |

## 授權

Apache-2.0