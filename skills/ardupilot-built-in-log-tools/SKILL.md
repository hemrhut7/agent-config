---
name: ardupilot-built-in-log-tools
description: 使用 pymavlink 內建工具對 ArduPilot 日誌（.bin, .tlog）進行深度分析。支援參數提取、訊息過濾、CSV 導出與趨勢繪圖。
---

# ArduPilot 內建工具管理技能

此技能讓 Agent 能夠直接調用 `agents/skills/ardupilot-built-in-log-tools/scripts` 中的腳本，進行高效的日誌處理。

## 工具目錄規範
內建工具位於：`agents/skills/ardupilot-built-in-log-tools/scripts`
執行時應切換至該目錄或使用完整路徑。

## 核心工作流與指令

### 功能 1：列出資料類型與統計
使用 `mavmsgstats.py` 獲取日誌中所有標籤的頻率。
```bash
python3 mavmsgstats.py data/flight.bin
```

### 功能 2：提取載具參數表
使用 `mavparms.py` 讀取完整配置。
```bash
python3 mavparms.py data/flight.bin
```

### 功能 3：進階高效繪圖 (新增)
這是一個比 `mavgraph.py` 更高效的通用型繪圖工具。它採用 Single-pass 解析，並自動處理數據對齊與斷點偵測。

- **用法**：`python3 fast_plot.py <日誌路徑> "MSG1.Field1" "MSG2.Field2" ...`
- **範例**：繪製 Roll 與 Pitch 的對比圖
  ```bash
  python3 fast_plot.py data/flight.bin "ATT.Roll" "ATT.Pitch" --output output/fast_plot.png  ```

### 功能 4：統一分析入口與快取架構 (最強效能型 - 新增)
為解決反覆解析巨大日誌的耗時問題，請使用 `auto_analysis.py` 處理複合任務：
1. **日誌快取**：首次執行會將日誌緩存為 `.pkl` (存於 `.logcache/`)，後續載入僅需毫秒級。
2. **一體化流程**：單一指令完成對齊、PVA 誤差計算與圖表報表生成。
3. **智慧降採樣**：自動優化繪圖點數，防止 Matplotlib 渲染卡死。

- **用法**：`python3 auto_analysis.py <日誌路徑> --task pva --out <輸出前綴>`
- **範例**：
  ```bash
  python3 auto_analysis.py data/flight.bin --task pva --out output/pva_report
  ```


## 輔助功能：快速摘要
若需快速了解飛行狀況（如總飛行時間），請執行：
```bash
python3 mavsummarize.py data/flight.bin
```


## 漸進式揭露
若不清楚特定訊息（如 NKF1）的含義，請閱讀 [MESSAGE_REFERENCE.md](MESSAGE_REFERENCE.md)。

## 注意事項
- **繪圖限制**：`mavgraph.py` 繪圖時，欄位名稱需符合 "TYPE.Field" 格式（例如 `ATT.Roll`）。
- **路徑規範**：一律使用正斜杠 `/`，路徑中若有空格請加引號。