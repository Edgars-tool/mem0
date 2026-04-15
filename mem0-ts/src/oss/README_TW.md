# mem0-ts

使用 OpenAI 嵌入和完成的 mem0 記憶系統的 TypeScript 實作。

## 功能

- 使用向量嵌入進行記憶儲存和檢索
- 使用 GPT-4 從文字中提取事實
- 基於 SQLite 的歷史追蹤
- 可選的圖形基礎記憶關係
- TypeScript 類型安全
- 內建 OpenAI 整合與預設配置
- 記憶體向量儲存庫實作
- 可擴展的架構，配有用於自訂實作的介面

## 安裝

1. 複製儲存庫：

```bash
git clone <repository-url>
cd mem0-ts
```

2. 安裝依賴：

```bash
npm install
```

3. 設置環境變數：

```bash
cp .env.example .env
# 編輯 .env 填入您的 OpenAI API 金鑰
```

4. 建置專案：

```bash
npm run build
```

## 使用方式

### 基本範例

```typescript
import { Memory } from "mem0-ts";

// 使用預設 OpenAI 配置建立記憶實例
const memory = new Memory();

// 或使用最小配置（僅 API 金鑰）
const memory = new Memory({
  embedder: {
    config: {
      apiKey: process.env.OPENAI_API_KEY,
    },
  },
  llm: {
    config: {
      apiKey: process.env.OPENAI_API_KEY,
    },
  },
});

// 或使用自訂配置
const memory = new Memory({
  embedder: {
    provider: "openai",
    config: {
      apiKey: process.env.OPENAI_API_KEY,
      model: "text-embedding-3-small",
    },
  },
  vectorStore: {
    provider: "memory",
    config: {
      collectionName: "custom-memories",
    },
  },
  llm: {
    provider: "openai",
    config: {
      apiKey: process.env.OPENAI_API_KEY,
      model: "gpt-4-turbo-preview",
    },
  },
});

// 新增記憶
await memory.add("The sky is blue", "user123");

// 搜尋記憶
const results = await memory.search("What color is the sky?", "user123");
```

### 預設配置

記憶系統附帶合理的預設值：

- 使用 `text-embedding-3-small` 模型的 OpenAI 嵌入
- 記憶體向量儲存庫
- 用於 LLM 操作的 OpenAI GPT-4 Turbo
- 用於歷史追蹤的 SQLite

您只需要提供 API 金鑰 - 所有其他設定可選。

### 方法

- `add(messages: string | Message[], userId?: string, ...): Promise<SearchResult>`
- `search(query: string, userId?: string, ...): Promise<SearchResult>`
- `get(memoryId: string): Promise<MemoryItem | null>`
- `update(memoryId: string, data: string): Promise<{ message: string }>`
- `delete(memoryId: string): Promise<{ message: string }>`
- `deleteAll(userId?: string, ...): Promise<{ message: string }>`
- `history(memoryId: string): Promise<any[]>`
- `reset(): Promise<void>`

### 嘗試範例

我們在 `examples/basic.ts` 中提供了一個展示所有功能的綜合範例，包括：

- 預設配置使用
- 記憶體向量儲存庫
- PGVector 儲存庫（使用 PostgreSQL）
- Qdrant 向量儲存庫
- Redis 向量儲存庫
- 記憶操作（新增、搜尋、更新、刪除）

要執行範例：

```bash
npm run example
```

您可以使用此範例作為模板並根據您的需要進行修改。範例包括：

- 不同的向量儲存庫配置
- 各種記憶操作
- 錯誤處理
- 環境變數使用

## 開發

1. 建置專案：

```bash
npm run build
```

2. 清理建置檔案：

```bash
npm run clean
```

## 擴展

系統設計為可擴展的。您可以實作自己的：

- 透過實作 `Embedder` 介面來實作嵌入器
- 透過實作 `VectorStore` 介面來實作向量儲存庫
- 透過實作 `LLM` 介面來實作語言模型

## 授權

MIT

## 貢獻

1. 分叉儲存庫
2. 建立您的功能分支
3. 提交您的更改
4. 推送到分支
5. 建立新的 Pull Request