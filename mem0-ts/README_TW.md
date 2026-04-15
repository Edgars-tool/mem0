# Mem0 - 您的 AI 應用程式的記憶層

Mem0 是一個用於 LLM 應用程式的自我改進記憶層，可提供節省成本且令人驚艷的個人化 AI 體驗。我們提供雲端和開源兩種解決方案，以滿足不同需求。

請參閱完整的[開源文檔](https://docs.mem0.ai/open-source/node-quickstart)。
請參閱完整的[平台 API 參考文檔](https://docs.mem0.ai/api-reference)。

## 1. 安裝

對於開源版本，您可以使用 npm 安裝 Mem0 套件：

```bash
npm i mem0ai
```

## 2. API 金鑰設置

對於雲端服務，請登入 [Mem0 平台](https://app.mem0.ai/dashboard/api-keys) 取得您的 API 金鑰。

## 3. 用戶端功能

### 雲端服務

雲端版本提供完整的功能，包括：

- **記憶操作**：對記憶執行 CRUD 操作。
- **搜尋功能**：使用進階篩選器搜尋相關記憶。
- **記憶歷史**：追蹤記憶的變更。
- **錯誤處理**：針對 API 相關問題的穩健錯誤處理。
- **Async/Await 支援**：所有方法都會回傳 Promise，方便整合。

### 開源服務

開源版本包含以下主要功能：

- **記憶管理**：新增、更新、刪除和擷取記憶。
- **向量儲存庫整合**：支援多種向量儲存庫供應商，以實現高效的記憶檢索。
- **LLM 支援**：與多個 LLM 提供商整合以產生回應。
- **可自訂配置**：輕鬆配置記憶設定和供應商。
- **SQLite 儲存**：使用 SQLite 進行記憶歷史管理。

## 4. 記憶操作

Mem0 提供簡單且可自訂的介面來執行記憶操作。您可以建立長期和短期記憶、搜尋相關記憶，以及管理記憶歷史。

## 5. 錯誤處理

MemoryClient 會針對任何 API 相關問題拋出錯誤。您可以有效地catch並處理這些錯誤。

## 6. 使用 async/await

MemoryClient 的所有方法都會回傳 Promise，允許與 async/await 語法無縫整合。

## 7. 測試用戶端

要在 Node.js 環境中測試 MemoryClient，您可以建立簡單的腳本來驗證記憶操作的功能。

## 取得協助

如果您有任何問題或需要協助，請聯繫我們：

- 電子郵件：founders@mem0.ai
- [加入我們的 discord 社群](https://mem0.ai/discord)
- GitHub Issues：[回報錯誤或請求功能](https://github.com/mem0ai/mem0/issues)