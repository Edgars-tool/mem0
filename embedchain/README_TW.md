<p align="center">
  <img src="docs/logo/dark.svg" width="400px" alt="Embedchain Logo">
</p>

<p align="center">
  <a href="https://pypi.org/project/embedchain/">
    <img src="https://img.shields.io/pypi/v/embedchain" alt="PyPI">
  </a>
  <a href="https://pepy.tech/project/embedchain">
    <img src="https://static.pepy.tech/badge/embedchain" alt="Downloads">
  </a>
  <a href="https://embedchain.ai/slack">
    <img src="https://img.shields.io/badge/slack-embedchain-brightgreen.svg?logo=slack" alt="Slack">
  </a>
  <a href="https://embedchain.ai/discord">
    <img src="https://dcbadge.vercel.app/api/server/6PzXDgEjG5?style=flat" alt="Discord">
  </a>
  <a href="https://twitter.com/embedchain">
    <img src="https://img.shields.io/twitter/follow/embedchain" alt="Twitter">
  </a>
  <a href="https://colab.research.google.com/drive/138lMWhENGeEu7Q1-6lNbNTHGLZXBBz_B?usp=sharing">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab">
  </a>
  <a href="https://codecov.io/gh/embedchain/embedchain">
    <img src="https://codecov.io/gh/embedchain/embedchain/graph/badge.svg?token=EMRRHZXW1Q" alt="codecov">
  </a>
</p>

<hr />

## 什麼是 Embedchain？

Embedchain 是一個用於個人化 LLM 回應的開源框架。它讓建立和部署個人化 AI 應用程式變得輕鬆。在核心上，Embedchain 遵循「常規但可設定」的設計原則，以服務軟體工程師和機器學習工程師。

Embedchain 簡化了個人化 LLM 應用程式的建立，提供無縫的流程來管理各種類型的非結構化資料。它能有效地將資料分割成可管理的區塊，產生相關的嵌入，並將它們儲存在向量資料庫中以優化檢索。透過多樣化的 API 套件，它讓使用者能夠擷取上下文資訊、找到精確的答案，或進行互動式的聊天對話，所有這些都根據他們自己的資料量身定制。

## 🔧 快速安裝

### Python API

```bash
pip install embedchain
```

## ✨ 即時演示

查看我們使用 Embedchain 建立的[與 PDF 聊天](https://embedchain.ai/demo/chat-pdf)即時演示。您可以在[這裡](https://github.com/mem0ai/mem0/tree/main/embedchain/examples/chat-pdf)找到原始碼。

## 🔍 使用方式

<!-- Demo GIF 或圖片 -->
<p align="center">
  <img src="docs/images/cover.gif" width="900px" alt="Embedchain Demo">
</p>

例如，您可以使用以下程式碼建立一個 Elon Musk 機器人：

```python
import os
from embedchain import App

# 建立機器人實例
os.environ["OPENAI_API_KEY"] = "<YOUR_API_KEY>"
app = App()

# 嵌入線上資源
app.add("https://en.wikipedia.org/wiki/Elon_Musk")
app.add("https://www.forbes.com/profile/elon-musk")

# 查詢應用程式
app.query("Elon Musk 經營多少家公司？請列出這些公司名稱？")
# 答案：Elon Musk 目前經營多家公司。根據我的知識，他是 SpaceX 的執行長和首席設計師、 Tesla, Inc. 的執行長和產品架構師、Neuralink 的執行長和創辦人，以及 The Boring Company 的執行長和創辦人。然而，請注意此資訊可能會隨時間變化，因此最好驗證最新更新。
```

您也可以在瀏覽器中使用 Google Colab 試用：

[![在 Colab 中開啟](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/17ON1LPonnXAtLaZEebnOktstB_1cJJmh?usp=sharing)

## 📖 文件

提供全面的指南和 API 文件，幫助您充分利用 Embedchain：

- [介紹](https://docs.embedchain.ai/get-started/introduction#what-is-embedchain)
- [快速開始](https://docs.embedchain.ai/get-started/quickstart)
- [範例](https://docs.embedchain.ai/examples)
- [支援的資料類型](https://docs.embedchain.ai/components/data-sources/overview)

## 🔗 加入社群

* 透過加入我們的 [Slack 社群](https://embedchain.ai/slack) 或 [Discord 社群](https://embedchain.ai/discord) 與其他開發者聯繫。

* 深入了解 [GitHub Discussions](https://github.com/embedchain/embedchain/discussions)、提出問題，或分享您的經驗。

## 🤝 預約一對一會議

與創辦人預約[一對一會議](https://cal.com/taranjeetio/ec)，討論任何問題、提供回饋，或探索我們如何為您改進 Embedchain。

## 🌐 歡迎貢獻

歡迎貢獻！請查看 repository 上的問題，並隨意開啟 pull request。
如需更多資訊，請參閱[貢獻指南](CONTRIBUTING.md)。

如需更多參考，請閱讀[開發指南](https://docs.embedchain.ai/contribution/dev)和[文件指南](https://docs.embedchain.ai/contribution/docs)。

<a href="https://github.com/embedchain/embedchain/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=embedchain/embedchain" />
</a>

## 匿名遙測

我們收集匿名使用指標來提升套件的品質和使用者體驗。這包括資料使用頻率和系統資訊等資料，但從不包含個人詳細資料。這些資料幫助我們確定改進的優先順序並確保相容性。如果您想退出，請設定環境變數 `EC_TELEMETRY=false`。我們優先考慮資料安全，不會與外部共享這些資料。

## 引用

如果您使用此 repository，請考慮引用：

```
@misc{embedchain,
  author = {Taranjeet Singh, Deshraj Yadav},
  title = {Embedchain: The Open Source RAG Framework},
  year = {2023},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/embedchain/embedchain}},
}
```