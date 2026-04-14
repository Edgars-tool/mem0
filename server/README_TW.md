# Mem0 REST API 伺服器

Mem0 提供 REST API 伺服器（使用 FastAPI 編寫）。使用者可以透過 REST 端點執行所有操作。API  also includes OpenAPI documentation, accessible at `/docs` when the server is running.

## 功能

- **建立記憶：** 根據用戶、代理程式或執行的訊息建立記憶。
- **擷取記憶：** 取得指定用戶、代理程式或執行的所有記憶。
- **搜尋記憶：** 根據查詢搜尋儲存的記憶。
- **更新記憶：** 更新現有記憶。
- **刪除記憶：** 刪除特定記憶或用戶、代理程式或執行的所有記憶。
- **重置記憶：** 重置用戶、代理程式或執行的所有記憶。
- **OpenAPI 文件：** 可透過 `/docs` 端點存取。

## 執行伺服器

請按照[文件](https://docs.mem0.ai/open-source/features/rest-api)中的說明執行伺服器。