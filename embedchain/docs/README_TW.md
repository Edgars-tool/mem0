# 為 embedchain 文件做出貢獻

### 👩‍💻 開發

安裝 [Mintlify CLI](https://www.npmjs.com/package/mintlify) 以在本地預覽文件變更。若要安裝，請使用以下命令

```
npm i -g mintlify
```

在您的文件根目錄（mint.json 所在的位置）執行以下命令

```
mintlify dev
```

### 😎 發布變更

您的 PR 合併到主分支後，變更會自動部署到正式環境。

#### 疑難排解

- Mintlify dev 未執行 - 執行 `mintlify install` 它會重新安裝依賴。
- 頁面載入為 404 - 確保您正在執行 `mintlify dev` 的資料夾中有 `mint.json`