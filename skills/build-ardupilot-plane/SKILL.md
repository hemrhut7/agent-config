---
name: build-ardupilot-plane
description: 使用 waf 構建 Ardupilot Plane 韌體，具備狀態監控與自動錯誤分析功能。採用增量編譯優先，並優化輸出處理以防止 Terminal 卡頓。
---

# Build Ardupilot Plane Skill (Monitored Version)

此技能專為大規模 Ardupilot 編譯設計，解決因 verbose 輸出導致的 Agent 響應中斷問題。

## 執行邏輯

### 1. 啟動編譯 (非同步優化)
- **指令執行**：執行 `./waf configure --board sitl && ./waf plane`，以及 `./waf configure --board CubeOrangePlus-CIRC && ./waf plane`，確認可以在實體飛控與軟模擬環境都可以正常編譯。
- **紀錄輸出**：建議將輸出導向至臨時記錄檔，或使用 `--summary` 旗標（若支援）以減少實時文字流。
- **防止卡頓**：Agent 應避免逐行讀取數千行的編譯輸出，而是採用「追蹤模式」。

### 2. 狀態監控 (每 5 秒循環)
在編譯執行期間，Agent 必須維持以下監控循環：
- **心跳檢查**：每 5 秒確認一次後台進程是否仍在運行。
- **狀態判定**：
  - **編譯中**：進程活動正常且 CPU 有負載。
  - **編譯完成**：進程結束且回傳碼為 0。
  - **編譯錯誤**：進程結束且回傳碼非 0。

### 3. 異常處理與 Fallback
- **初次失敗**：若 `./waf plane` 報錯，自動執行 `./waf clean` 並再次嘗試 `./waf plane`。
- **二次失敗**：若重試後依然失敗，進入「錯誤分析模式」。

### 4. 錯誤分析模式
當編譯中斷時，Agent **不應讀取全部日誌**，而是：
- **關鍵提取**：僅抓取日誌最後 50-100 行內容。
- **特徵搜尋**：尋找 `error:`、`fatal error:` 或 `recipe for target ... failed`。
- **成因分析**：針對缺少依賴、語法錯誤或路徑問題提供繁體中文建議。

## 指令建議 (避免 Buffer 溢位)
```bash
# 建議將輸出最小化或背景執行
./waf plane > build_log.txt 2>&1 &