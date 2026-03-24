# PlatformIO 錯誤排查參考

當 `pio run` 失敗時，請根據以下錯誤訊息進行分析：

## 常見問題清單

### 1. 找不到開發平台 (Platform not found)
**原因**：未安裝對應的開發框架（如 `espressif32`）。
**對策**：執行 `pio pkg install` 或檢查 `platformio.ini` 中的 `platform` 欄位。

### 2. 缺少標頭檔 (Missing header files)
**原因**：未包含必要的庫或路徑錯誤。
**對策**：
- 檢查 `lib_deps` 是否包含該庫。
- 確認 `#include` 的名稱是否正確。

### 3. 配置錯誤 (Invalid platformio.ini)
**原因**：語法錯誤或不支援的開發板名稱。
**對策**：核對官方開發板清單，確保 `board` ID 正確。

## 驗證步驟
1. 閱讀錯誤訊息的最後 10 行。
2. 根據錯誤類型修改代碼或配置文件。
3. 重新運行 `pio run`。