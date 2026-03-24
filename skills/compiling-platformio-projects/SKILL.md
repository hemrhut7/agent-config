---
name: compiling-platformio-projects
description: 使用 PlatformIO (PIO) 編譯與構建嵌入式開發專案。當用戶要求編譯代碼、執行構建、運行 pio run 或處理 .ino/.cpp 硬體專案時使用。
---
# PlatformIO 編譯技能

此技能負責執行 PlatformIO 專案的構建流程，並確保編譯產出物正確生成。

## 核心工作流

1. **環境驗證**：檢查當前目錄是否存在 `platformio.ini` 配置文件。
2. **執行編譯**：運行 `pio run` 指令。
3. **結果分析**：
   - 若編譯成功，確認 `.pio/build/` 目錄下生成的二進制文件。
   - 若編譯失敗，分析終端輸出並參考 [TROUBLESHOOTING.md](TROUBLESHOOTING.md) 進行修正。

## 常用命令

### 執行標準編譯

```bash
pio run
```

### 清理並重新編譯

```bash
pio run -t clean
pio run
```

### 指定特定環境編譯（若配置文件有多個環境）

```bash
# 假設環境名稱為 esp32dev
pio run -e esp32dev
```

## 注意事項

- **路徑規範**：始終使用正斜杠 `/` 處理專案路徑。
- **相依性**：若提示缺少庫，應優先檢查 `lib_deps` 設置。
- **反饋循環**：若編譯失敗，請修正代碼或配置後重新執行步驟 2，直到驗證通過。
