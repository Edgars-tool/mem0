# 私人 AI

在此範例中，我們將使用 embedchain 建立私人 AI。

當您想與您的資料聊天且不想花錢，且您的資料應該保存在您的機器上時，私人 AI 非常有用。

## 如何安裝

首先建立虛擬環境並透過執行以下命令安裝需求

```bash
pip install -r requirements.txt
```

## 如何使用

* 現在開啟 privateai.py 檔案並修改 `app.add` 行指向您的目錄或資料來源。
* 如果您想新增任何其他資料類型，您可以在[這裡](https://docs.embedchain.ai/components/data-sources/overview)瀏覽支援的資料類型

* 現在只需執行該檔案

```bash
python privateai.py
```

* 現在您可以輸入並向您的資料詢問任何問題。