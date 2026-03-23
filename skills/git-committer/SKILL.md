---
name: managing-git-commits
description: 分析 Git 暫存區變更、生成符合規範的提交訊息並執行 commit。於用戶要求提交程式碼或完成任務後需存檔時使用。
---

# Git 提交管理工作流

## 核心規則
- **自動化優先**：優先調用 `scripts/git_helper.py` 獲取變更內容。
- **格式合規**：訊息必須符合 [FORMAT.md](FORMAT.md) 的 Conventional Commits 規範。
- **提交確認**：執行 `commit` 前務必向使用者確認訊息內容是否需要調整。

## 執行工作流
1. **提取變更**：運行 `python scripts/git_helper.py --action get_diff`。
2. **撰寫草稿**：根據 diff 內容，參考 [FORMAT.md](FORMAT.md) 生成提交訊息。
3. **驗證與修訂**：
   - 檢查是否保留技術專有名詞（如 `EKF`, `DMA`）。
4. **執行提交**：運行 `python scripts/git_helper.py --action commit --message "[訊息內容]"`，執行提交前請先進行確認。

## 錯誤處理
- 若無暫存變更（No staged changes），先執行 `git add`。
- 若腳本返回錯誤，分析錯誤訊息並修正（例如：解決檔案鎖定問題）。