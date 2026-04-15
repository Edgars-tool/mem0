## Unacademy UPSC AI

此目錄包含用於實作 [Unacademy UPSC AI](https://unacademy-ai.streamlit.app/) 的程式碼，使用 Embedchain。它建構於 16,000 多部 YouTube 影片和 800 多個 Unacademy 網站課程頁面。您可以在[這裡](https://gist.github.com/deshraj/7714feadccca13cefe574951652fa9b2)找到完整的資料來源列表。

## 在本機執行

您可以使用以下命令以 streamlit 應用程式的形式在本機執行 Unacademy AI：

```bash
export OPENAI_API_KEY=sk-xxx
pip install -r requirements.txt
streamlit run app.py
```

注意：請記得設定您的 `OPENAI_API_KEY`。

## 部署到生產環境

您可以使用[我們的文件](https://docs.embedchain.ai/get-started/deployment)中提供的多種部署方法之一，在生產環境中建立您自己的 Unacademy AI 或類似的 RAG 應用程式。