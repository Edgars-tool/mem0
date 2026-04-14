# Mem0 - AI 應用程式的記憶層

<p align="center">
  <a href="https://github.com/mem0ai/mem0">
    <img src="docs/images/banner-sm.png" width="800px" alt="Mem0 - The Memory Layer for Personalized AI">
  </a>
</p>
<p align="center" style="display: flex; justify-content: center; gap: 20px; align-items: center;">
  <a href="https://trendshift.io/repositories/11194" target="blank">
    <img src="https://trendshift.io/api/badge/repositories/11194" alt="mem0ai%2Fmem0 | Trendshift" width="250" height="55"/>
  </a>
</p>

<p align="center">
  <a href="https://mem0.ai">Learn more</a>
  ·
  <a href="https://mem0.dev/DiG">Join Discord</a>
  ·
  <a href="https://mem0.dev/demo">Demo</a>
</p>

<p align="center">
  <a href="https://mem0.dev/DiG">
    <img src="https://img.shields.io/badge/Discord-%235865F2.svg?&logo=discord&logoColor=white" alt="Mem0 Discord">
  </a>
  <a href="https://pepy.tech/project/mem0ai">
    <img src="https://img.shields.io/pypi/dm/mem0ai" alt="Mem0 PyPI - Downloads">
  </a>
  <a href="https://github.com/mem0ai/mem0">
    <img src="https://img.shields.io/github/commit-activity/m/mem0ai/mem0?style=flat-square" alt="GitHub commit activity">
  </a>
  <a href="https://pypi.org/project/mem0ai" target="blank">
    <img src="https://img.shields.io/pypi/v/mem0ai?color=%2334D058&label=pypi%20package" alt="Package version">
  </a>
  <a href="https://www.npmjs.com/package/mem0ai" target="blank">
    <img src="https://img.shields.io/npm/v/mem0ai" alt="Npm package">
  </a>
  <a href="https://www.ycombinator.com/companies/mem0">
    <img src="https://img.shields.io/badge/Y%20Combinator-S24-orange?style=flat-square" alt="Y Combinator S24">
  </a>
</p>

<p align="center">
  <a href="https://mem0.ai/research"><strong>📄 Building Production-Ready AI Agents with Scalable Long-Term Memory →</strong></a>
</p>
<p align="center">
  <strong>⚡ +26% Accuracy vs. OpenAI Memory • 🚀 91% Faster • 💰 90% Fewer Tokens</strong>
</p>

> **🎉 mem0ai v1.0.0 現已推出！** 此重大更新包含 API 現代化、改進的向量儲存庫支援，以及增強的 GCP 整合。[查看遷移指南 →](MIGRATION_GUIDE_v1.0.md)

## 🔥 研究亮點
- **+26% 準確率** - 超越 OpenAI Memory 在 LOCOMO 基準上的表現
- **91% 更快的回應** - 比完整上下文更快，確保大規模低延遲
- **90% 更少的 Token 使用** - 比完整上下文更節省成本
- [閱讀完整論文](https://mem0.ai/research)

# 簡介

[Mem0](https://mem0.ai)（發音為 "mem-zero」）為 AI 助理和代理程式增強智慧記憶層，實現個人化 AI 互動。它會記住用戶偏好、適應個人需求，並持續隨時間學習 — 非常適合客戶支援聊天機器人、AI 助理和自主系統。

### 主要功能與使用場景

**核心功能：**
- **多層級記憶**：無縫保留用戶、會話和代理程式狀態，具備適應性個人化
- **開發者友善**：直覺式 API、跨平台 SDK 和完整托管服務選項

**應用場景：**
- **AI 助理**：一致、豐富上下文的對話
- **客戶支援**：回顧過往工單和用戶歷史以提供客製化幫助
- **醫療保健**：追蹤患者偏好和歷史以提供個人化照護
- **生產力與遊戲**：根據用戶行為自適應工作流程和環境

## 🚀 快速開始指南 <a name="quickstart"></a>

請選擇使用托管平台或自托管套件：

### 托管平台

只需幾分鐘即可開始使用，自動更新、分析和企業級安全性。

1. 在 [Mem0 平台](https://app.mem0.ai) 註冊
2. 透過 SDK 或 API 金鑰嵌入記憶層

### 自托管（開源）

透過 pip 安裝 SDK：

```bash
pip install mem0ai
```

透過 npm 安裝 SDK：
```bash
npm install mem0ai
```

### CLI

透過終端機管理記憶：

```bash
npm install -g @mem0/cli   # 或：pip install mem0-cli

mem0 init
mem0 add "Prefers dark mode and vim keybindings" --user-id alice
mem0 search "What does Alice prefer?" --user-id alice
```

請參閱 [CLI 文檔](https://docs.mem0.ai/platform/cli) 取得完整指令參考。

### 基本使用方式

Mem0 需要 LLM 才能運作，預設使用 OpenAI 的 `gpt-4.1-nano-2025-04-14`。不過，它支援多種 LLM；詳細資訊請參閱我們的[支援的 LLM 文檔](https://docs.mem0.ai/components/llms/overview)。

首先需要實例化記憶體：

```python
from openai import OpenAI
from mem0 import Memory

openai_client = OpenAI()
memory = Memory()

def chat_with_memories(message: str, user_id: str = "default_user") -> str:
    # 檢索相關記憶
    relevant_memories = memory.search(query=message, user_id=user_id, limit=3)
    memories_str = "\n".join(f"- {entry['memory']}" for entry in relevant_memories["results"])

    # 產生助理回應
    system_prompt = f"You are a helpful AI. Answer the question based on query and memories.\nUser Memories:\n{memories_str}"
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": message}]
    response = openai_client.chat.completions.create(model="gpt-4.1-nano-2025-04-14", messages=messages)
    assistant_response = response.choices[0].message.content

    # 從對話中建立新記憶
    messages.append({"role": "assistant", "content": assistant_response})
    memory.add(messages, user_id=user_id)

    return assistant_response

def main():
    print("Chat with AI (type 'exit' to quit)")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        print(f"AI: {chat_with_memories(user_input)}")

if __name__ == "__main__":
    main()
```

如需詳細的整合步驟，請參閱 [快速開始](https://docs.mem0.ai/quickstart) 和 [API 參考](https://docs.mem0.ai/api-reference)。

## 🔗 整合與示範

- **帶記憶的 ChatGPT**：由 Mem0 驅動的個人化聊天（[線上演示](https://mem0.dev/demo)）
- **瀏覽器擴充功能**：跨 ChatGPT、Perplexity 和 Claude 儲存記憶（[Chrome 擴充功能](https://chromewebstore.google.com/detail/onihkkbipkfeijkadecaafbgagkhglop?utm_source=item-share-cb)）
- **Langgraph 支援**：使用 Langgraph + Mem0 建立客戶機器人（[指南](https://docs.mem0.ai/integrations/langgraph)）
- **CrewAI 整合**：使用 Mem0 客製化 CrewAI 輸出（[範例](https://docs.mem0.ai/integrations/crewai)）

## 📚 文檔與支援

- 完整文檔：https://docs.mem0.ai
- 社群：[Discord](https://mem0.dev/DiG) · [X（前 Twitter）](https://x.com/mem0ai)
- 聯繫：founders@mem0.ai

## 引用

我們現在有一篇可供引用的論文：

```bibtex
@article{mem0,
  title={Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory},
  author={Chhikara, Prateek and Khant, Dev and Aryan, Saket and Singh, Taranjeet and Yadav, Deshraj},
  journal={arXiv preprint arXiv:2504.19413},
  year={2025}
}
```

## ⚖️ 授權

Apache 2.0 — 請參閱 [LICENSE](https://github.com/mem0ai/mem0/blob/main/LICENSE) 檔案取得詳細資訊。