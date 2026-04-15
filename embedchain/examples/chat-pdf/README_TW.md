# Embedchain 與 PDF 聊天應用程式

您可以輕鬆建立並部署自己的「與 PDF 聊天」應用程式使用 Embedchain。

查看我們為[與 PDF 聊天](https://embedchain.ai/demo/chat-pdf)建立的即時演示。

以下是如何建立和部署應用程式的簡單步驟：

1. 從 [Github](https://github.com/embedchain/embedchain) fork embedchain repo。

如果您在 fork 時遇到問題，請參考 [github docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) 來 fork repo。

2. 從您的 fork repo 導航到 `chat-pdf` 範例應用程式：

```bash
cd <your_fork_repo>/examples/chat-pdf
```

3. 使用簡單的命令在開發環境中執行您的應用程式

```bash
pip install -r requirements.txt
ec dev
```

歡迎改進我們簡單的 `chat-pdf` streamlit 應用程式，並在此處建立 pull request 來展示您的應用程式[這裡](https://docs.embedchain.ai/examples/showcase)。

4. 您可以輕鬆使用 Streamlit 介面部署您的應用程式

將您的 Github 帳戶與 Streamlit 連接，並參考此[指南](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)來部署您的應用程式。

您也可以使用執行 `ec dev` 命令時從 streamlit 網站看到的部署按鈕。