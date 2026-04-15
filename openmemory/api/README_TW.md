# OpenMemory API

此目錄包含 OpenMemory 的後端 API，使用 FastAPI 和 SQLAlchemy 建置。這也執行您可以與 MCP 用戶端一起使用的 Mem0 MCP 伺服器來記住事情。

## 使用 Docker 快速開始（推薦）

最簡單的開始方法是使用 Docker。確保您已安裝 Docker 和 Docker Compose。

1. 建置容器：
```bash
make build
```

2. 建立 `.env` 檔案：
```bash
make env
```

執行此命令後，編輯 `api/.env` 檔案並輸入 `OPENAI_API_KEY`。

3. 啟動服務：
```bash
make up
```

API 將可在 `http://localhost:8765` 使用。

### 常見 Docker 命令

- 查看日誌：`make logs`
- 在容器中開啟 shell：`make shell`
- 執行資料庫遷移：`make migrate`
- 執行測試：`make test`
- 執行測試並清理：`make test-clean`
- 停止容器：`make down`

## API 文件

伺服器執行後，您可以存取 API 文件於：
- Swagger UI：`http://localhost:8765/docs`
- ReDoc：`http://localhost:8765/redoc`

## 專案結構

- `app/`：主要應用程式碼
  - `models.py`：資料庫模型
  - `database.py`：資料庫配置
  - `routers/`：API 路由處理器
- `migrations/`：資料庫遷移檔案
- `tests/`：測試檔案
- `alembic/`：Alembic 遷移配置
- `main.py`：應用程式入口點

## 開發指南

- 遵循 PEP 8 風格指南
- 使用類型提示
- 為新功能撰寫測試
- 進行更改時更新文件
- 為資料庫更改執行遷移