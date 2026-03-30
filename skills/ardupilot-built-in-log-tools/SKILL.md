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

### 功能 3：特定資料處理（以 ATT 為例）
針對特定類型執行輸出、存檔或繪圖操作：

- **模式 A：終端輸出（前 50 筆）**
  使用 `mavlogdump.py` 過濾類型並配合 `head`。
  ```bash
  python3 mavlogdump.py --types ATT data/flight.bin | head -n 50
  ```

- **模式 B：另存為 CSV 檔案**
  利用 `mavlogdump.py` 的格式化功能。
  ```bash
  python3 mavlogdump.py --types ATT --format csv data/flight.bin > export_ATT.csv
  ```

- **模式 C：繪製趨勢圖表 (PNG)**
  使用 `mavgraph.py` 進行視覺化。注意：必須指定輸出路徑。
  ```bash
  # 繪製 Roll 與 Pitch 的對比圖
  python3 mavgraph.py data/flight.bin "ATT.Roll" "ATT.Pitch" --output plot_ATT.png
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