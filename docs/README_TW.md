# Mintlify 起始套件

點擊 `Use this template` 複製 Mintlify 起始套件。起始套件包含的範例包括

- 指南頁面
- 導航
- 自訂
- API 參考頁面
- 熱門元件的使用

### 開發

安裝 [Mintlify CLI](https://www.npmjs.com/package/mintlify) 以在本地預覽文件變更。若要安裝，請使用以下命令

```
npm i -g mintlify
```

在您的文件根目錄（mint.json 所在的位置）執行以下命令

```
mintlify dev
```

### 發布變更

安裝我們的 Github App 以自動將您 repo 的變更傳播到您的部署。推送到預設分支後，變更會自動部署到正式環境。在您的儀表板上找到安裝連結。

#### 疑難排解

- Mintlify dev 未執行 - 執行 `mintlify install` 它會重新安裝依賴。
- 頁面載入為 404 - 確保您正在執行 `mintlify dev` 的資料夾中有 `mint.json`