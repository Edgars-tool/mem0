## Sadhguru AI

此目錄包含用於實作 [Sadhguru AI](https://sadhguru-ai.streamlit.app/) 的程式碼，使用 Embedchain。它建構於 3,000 多部影片和 1,000 多篇文章之上。您可以在[這裡](https://gist.github.com/deshraj/50b0597157e04829bbbb7bc418be6ccb)找到完整的資料來源列表。

## 在本機執行

您可以使用以下命令以 streamlit 應用程式的形式在本機執行 Sadhguru AI：

```bash
export OPENAI_API_KEY=sk-xxx
pip install -r requirements.txt
streamlit run app.py
```

注意：請記得設定您的 `OPENAI_API_KEY`。

## 部署到生產環境

您可以使用[我們的文件](https://docs.embedchain.ai/get-started/deployment)中提供的多種部署方法之一，在生產環境中建立您自己的 Sadhguru AI 或類似的 RAG 應用程式。