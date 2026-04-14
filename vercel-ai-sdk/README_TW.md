# Mem0 AI SDK 提供者

**Mem0 AI SDK 提供者**是由 [Mem0](https://mem0.ai/) 開發的社群維護 library，用於與 Vercel AI SDK 整合。這個 library 透過引入持久記憶功能來增強 AI 互動能力。使用 Mem0，語言模型對話可以擁有記憶功能，根據過去的互動提供更具情境化且個人化的回應。

在 [GitHub](https://github.com/mem0ai/mem0) 上探索更多 **Mem0** 的資訊。
參考 [Mem0 文件](https://docs.mem0.ai/overview) 以深入了解如何更靈活地管理您的記憶。

如需有關使用 Vercel AI SDK 的詳細資訊，請參考 Vercel 的 [API 參考](https://sdk.vercel.ai/docs/reference) 和[文件](https://sdk.vercel.ai/docs)。

## 功能特點

- 🧠 AI 對話的持久記憶儲存
- 🔄 與 Vercel AI SDK 無縫整合
- 🚀 支援多種 LLM 提供者
- 📝 豐富的訊息格式支援
- ⚡ 串流功能
- 🔍 情境感知回應

## 安裝

```bash
npm install @mem0/vercel-ai-provider
```

## 開始之前

### 設定 Mem0

1. 從 Mem0 控制面板取得您的 [Mem0 API 金鑰](https://app.mem0.ai/dashboard/api-keys)。

2. 初始化 Mem0 用戶端：

```typescript
import { createMem0 } from "@mem0/vercel-ai-provider";

const mem0 = createMem0({
  provider: "openai",
  mem0ApiKey: "m0-xxx",
  apiKey: "openai-api-key",
  config: {
    compatibility: "strict",
    // 可在此處新增其他模型特定設定選項。
  },
});
```

### 說明

預設使用 `openai` 提供者，因此指定它是可選的：
```typescript
const mem0 = createMem0();
```
為了更好的安全性，請考慮將 `MEM0_API_KEY` 和 `OPENAI_API_KEY` 設為環境變數。

3. 新增記憶以增強上下文：

```typescript
import { LanguageModelV1Prompt } from "ai";
import { addMemories } from "@mem0/vercel-ai-provider";

const messages: LanguageModelV1Prompt = [
  {
    role: "user",
    content: [
      { type: "text", text: "我喜歡紅色的車。" },
      { type: "text", text: "我喜歡 Toyota 的車。" },
      { type: "text", text: "我偏好 SUV。" },
    ],
  },
];

await addMemories(messages, { user_id: "borat" });
```

這些記憶現在已儲存在您的個人檔案中。您可以在 [Mem0 控制面板](https://app.mem0.ai/dashboard/users) 查看和管理它們。

### 說明：

對於獨立功能，例如 `addMemories` 和 `retrieveMemories`，
您必須將 `MEM0_API_KEY` 設為環境變數，或直接在函式呼叫中傳遞。

範例：

```typescript
await addMemories(messages, { user_id: "borat", mem0ApiKey: "m0-xxx", org_id: "org_xx", project_id: "proj_xx" });
await retrieveMemories(prompt, { user_id: "borat", mem0ApiKey: "m0-xxx", org_id: "org_xx", project_id: "proj_xx" });
await getMemories(prompt, { user_id: "borat", mem0ApiKey: "m0-xxx", org_id: "org_xx", project_id: "proj_xx" });
```

### 說明：

`retrieveMemories` 會根據您個人檔案中的相關記憶來豐富提示，而 `getMemours` 以陣列格式回傳記憶，可用於進一步處理。

## 使用範例

### 1. 基本文字生成（含記憶上下文）

```typescript
import { generateText } from "ai";
import { createMem0 } from "@mem0/vercel-ai-provider";

const mem0 = createMem0();

const { text } = await generateText({
  model: mem0("gpt-4-turbo", {
    user_id: "borat",
  }),
  prompt: "Suggest me a good car to buy!",
});
```

### 2. 結合 OpenAI 提供者與記憶工具

```typescript
import { generateText } from "ai";
import { openai } from "@ai-sdk/openai";
import { retrieveMemories } from "@mem0/vercel-ai-provider";

const prompt = "Suggest me a good car to buy.";
const memories = await retrieveMemories(prompt, { user_id: "borat" });

const { text } = await generateText({
  model: openai("gpt-4-turbo"),
  prompt: prompt,
  system: memories,
});
```

### 3. 含記憶的結構化訊息格式

```typescript
import { generateText } from "ai";
import { createMem0 } from "@mem0/vercel-ai-provider";

const mem0 = createMem0();

const { text } = await generateText({
  model: mem0("gpt-4-turbo", {
    user_id: "borat",
  }),
  messages: [
    {
      role: "user",
      content: [
        { type: "text", text: "Suggest me a good car to buy." },
        { type: "text", text: "Why is it better than the other cars for me?" },
        { type: "text", text: "Give options for every price range." },
      ],
    },
  ],
});
```

### 4. 進階記憶整合（含 OpenAI）

```typescript
import { generateText, LanguageModelV1Prompt } from "ai";
import { openai } from "@ai-sdk/openai";
import { retrieveMemories } from "@mem0/vercel-ai-provider";

// 使用 system 參數進行記憶上下文的新格式
const messages: LanguageModelV1Prompt = [
  {
    role: "user",
    content: [
      { type: "text", text: "Suggest me a good car to buy." },
      { type: "text", text: "Why is it better than the other cars for me?" },
      { type: "text", text: "Give options for every price range." },
    ],
  },
];

const memories = await retrieveMemories(messages, { user_id: "borat" });

const { text } = await generateText({
  model: openai("gpt-4-turbo"),
  messages: messages,
  system: memories,
});
```

### 5. 含記憶上下文的串流回應

```typescript
import { streamText } from "ai";
import { createMem0 } from "@mem0/vercel-ai-provider";

const mem0 = createMem0();

const { textStream } = await streamText({
  model: mem0("gpt-4-turbo", {
    user_id: "borat",
  }),
  prompt:
    "Suggest me a good car to buy! Why is it better than the other cars for me? Give options for every price range.",
});

for await (const textPart of textStream) {
  process.stdout.write(textPart);
}
```

## 核心函式

- `createMem0()`: 使用可選設定初始化新的 mem0 提供者實例
- `retrieveMemories()`: 用相關記憶豐富提示
- `addMemories()`: 將記憶新增至您的個人檔案
- `getMemories()`: 以陣列格式從您的個人檔案取得記憶

## 設定選項

```typescript
const mem0 = createMem0({
  config: {
    ...
    // 可在此處新增其他模型特定設定選項。
  },
});
```

## 最佳實踐

1. **使用者識別**：始終提供唯一的 `user_id` 識別碼以確保一致的記憶擷取
2. **上下文管理**：使用適當的上下文視窗大小來平衡效能和記憶
3. **錯誤處理**：為記憶操作實作適當的錯誤處理
4. **記憶清理**：定期清理未使用的記憶上下文以優化效能

我們也支援 `agent_id`、`app_id` 和 `run_id`。請參考[文件](https://docs.mem0.ai/api-reference/memory/add-memories)。

## 注意事項

- 需要為底層提供者（如 OpenAI）正確設定 API 金鑰
- 記憶功能需透過 `user_id` 正確識別使用者
- 支援串流和非串流回應
- 與所有 Vercel AI SDK 功能和模式相容