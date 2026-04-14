# Mem0：建構可擴展長期記憶的生產級 AI 代理程式

[![arXiv](https://img.shields.io/badge/arXiv-Paper-b31b1b.svg)](https://arxiv.org/abs/2504.19413)
[![Website](https://img.shields.io/badge/Website-Project-blue)](https://mem0.ai/research)

此儲存庫包含我們的論文程式碼和資料集：**Mem0：建構可擴展長期記憶的生產級 AI 代理程式**。

## 📋 概述

此專案評估 Mem0 並比較不同記憶和檢索技術在 AI 系統中的表現：

1. **既有的 LOCOMO 基準**：我們對文獻中的五種既有關方案進行評估：LoCoMo、ReadAgent、MemoryBank、MemGPT 和 A-Mem。
2. **開源記憶解決方案**：我們測試了有前景的開源記憶架構，包括 LangMem，提供靈活的記憶管理能力。
3. **RAG 系統**：我們實作了檢索增強生成並使用各種配置，測試不同的區塊大小和檢索數量以優化效能。
4. **完整上下文處理**：我們檢視了在 LLM 上下文視窗中傳遞整個對話歷史作為基線方法的有效性。
5. **專有記憶系統**：我們評估了 OpenAI 在其 ChatGPT 介面中提供的內建記憶功能，以與商業解決方案進行比較。
6. **第三方記憶提供者**：我們納入了 Zep，這是專為 AI 代理程式設計的專業記憶管理平台，以評估專用記憶基礎設施的效能。

我們在 LOCOMO 資料集上測試這些技術，該資料集包含各種問題類型的對話資料，用於評估記憶回憶和理解能力。

## 🔍 資料集

我們實驗中使用的 LOCOMO 資料集可從 Google Drive 儲存庫下載：

[下載 LOCOMO 資料集](https://drive.google.com/drive/folders/1L-cTjTm0ohMsitsHg4dijSPJtqNflwX-?usp=drive_link)

該資料集包含專為測試各種問題類型和複雜程度下的記憶回憶和理解能力而設計的對話資料。

將資料集檔案放在 `dataset/` 目錄中：
- `locomo10.json`：原始資料集
- `locomo10_rag.json`：為 RAG 實驗格式化的資料集

## 📁 專案結構

```
.
├── src/                  # 不同記憶技術的原始碼
│   ├── mem0/             # Mem0 技術的實作
│   ├── openai/           # OpenAI 記憶的實作
│   ├── zep/              # Zep 記憶的實作
│   ├── rag.py            # RAG 技術的實作
│   └── langmem.py        # 基於語言的記憶實作
├── metrics/              # 評估指標程式碼
├── results/              # 實驗結果
├── dataset/              # 資料集檔案
├── evals.py              # 評估腳本
├── run_experiments.py    # 執行實驗的腳本
├── generate_scores.py    # 從結果產生分數的腳本
└── prompts.py            # 用於模型的提示詞
```

## 🚀 開始使用

### 前置條件

建立包含您的 API 金鑰和配置的 `.env` 檔案。需要以下金鑰：

```
# 用於 GPT 模型和嵌入的 OpenAI API 金鑰
OPENAI_API_KEY="your-openai-api-key"

# Mem0 API 金鑰（用於 Mem0 和 Mem0+ 技術）
MEM0_API_KEY="your-mem0-api-key"
MEM0_PROJECT_ID="your-mem0-project-id"
MEM0_ORGANIZATION_ID="your-mem0-organization-id"

# 模型配置
MODEL="gpt-4o-mini"  # 或您偏好的模型
EMBEDDING_MODEL="text-embedding-3-small"  # 或您偏好的嵌入模型
ZEP_API_KEY="api-key-from-zep"
```

### 執行實驗

您可以使用提供的 Makefile 命令執行實驗：

#### 記憶技術

```bash
# 執行 Mem0 實驗
make run-mem0-add         # 使用 Mem0 新增記憶
make run-mem0-search      # 使用 Mem0 搜尋記憶

# 執行 Mem0+ 實驗（使用圖形基礎搜尋）
make run-mem0-plus-add    # 使用 Mem0+ 新增記憶
make run-mem0-plus-search # 使用 Mem0+ 搜尋記憶

# 執行 RAG 實驗
make run-rag              # 使用區塊大小 500 執行 RAG
make run-full-context     # 使用完整上下文執行 RAG

# 執行 LangMem 實驗
make run-langmem          # 執行 LangMem

# 執行 Zep 實驗
make run-zep-add          # 使用 Zep 新增記憶
make run-zep-search       # 使用 Zep 搜尋記憶

# 執行 OpenAI 實驗
make run-openai           # 執行 OpenAI 實驗
```

或者，您可以使用自訂參數直接執行實驗：

```bash
python run_experiments.py --technique_type [mem0|rag|langmem] [additional parameters]
```

#### 命令列參數：

| 參數 | 說明 | 預設值 |
|-----------|-------------|---------|
| `--technique_type` | 要使用的記憶技術 (mem0, rag, langmem) | mem0 |
| `--method` | 要使用的方法 (add, search) | add |
| `--chunk_size` | 處理的區塊大小 | 1000 |
| `--top_k` | 檢索的頂級記憶數量 | 30 |
| `--filter_memories` | 是否篩選記憶 | False |
| `--is_graph` | 是否使用圖形基礎搜尋 | False |
| `--num_chunks` | 要處理的 RAG 區塊數量 | 1 |

### 📊 評估

要評估結果，請執行：

```bash
python evals.py --input_file [path_to_results] --output_file [output_path]
```

此腳本：
1. 處理每個問答對
2. 自動計算 BLEU 和 F1 分數
3. 使用 LLM 判斷來評估答案正確性
4. 將合併結果儲存到輸出檔案

### 📈 產生分數

使用以下命令產生最終分數：

```bash
python generate_scores.py
```

此腳本：
1. 載入評估指標資料
2. 計算每個類别的平均分數（BLEU、F1、LLM）
3. 報告每個類别的問題數量
4. 計算所有類别的整體平均分數

範例輸出：
```
每類别平均分數：
         bleu_score  f1_score  llm_score  count
category                                       
1           0.xxxx    0.xxxx     0.xxxx     xx
2           0.xxxx    0.xxxx     0.xxxx     xx
3           0.xxxx    0.xxxx     0.xxxx     xx

整體平均分數：
bleu_score    0.xxxx
f1_score      0.xxxx
llm_score     0.xxxx
```

## 📏 評估指標

我們使用多個指標來評估不同記憶技術的效能：

1. **BLEU 分數**：測量模型回應與真實答案之間的相似度
2. **F1 分數**：測量精確率和召回率的調和平均值
3. **LLM 分數**：由 LLM 判斷確定的二元分數（0 或 1），評估回應的正確性
4. **Token 消耗**：產生最終答案所需的 tokens 數量。
5. **延遲**：搜尋和產生回應所需的時間。

## 📚 引用

如果您在研究中使用了此程式碼或資料集，請引用我們的論文：

```bibtex
@article{mem0,
  title={Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory},
  author={Chhikara, Prateek and Khant, Dev and Aryan, Saket and Singh, Taranjeet and Yadav, Deshraj},
  journal={arXiv preprint arXiv:2504.19413},
  year={2025}
}
```

## 📄 授權

[MIT 授權](LICENSE)

## 👥 貢獻者

- [Prateek Chhikara](https://github.com/prateekchhikara)
- [Dev Khant](https://github.com/Dev-Khant)
- [Saket Aryan](https://github.com/whysosaket)
- [Taranjeet Singh](https://github.com/taranjeet)
- [Deshraj Yadav](https://github.com/deshraj)