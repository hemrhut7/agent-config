---
name: git-committer
description: 分析 Git 暫存區變更、生成符合規範的提交訊息並執行 commit。於用戶要求提交程式碼或完成任務後需存檔時使用。
---

# Git 提交管理工作流

## 核心規則
- **自動化優先**：優先調用 `.agents/skills/git-committer/scripts/git_helper.py` 獲取變更內容。
- **分析全面**：在提交前，應分析包括已暫存（Staged）與未暫存（Unstaged）的所有變更，並參考最近的提交紀錄以確保上下文一致。
- **格式合規**：請區分用戶要使用中文還是英文進行訊息撰寫，若沒特別說明則預設使用英文，
   - 若判斷使用英文撰寫，訊息必須符合 [EN_FORMAT.md](EN_FORMAT.md) 的 規範。
   - 若判斷使用中文撰寫，訊息必須符合 [CH_FORMAT.md](CH_FORMAT.md) 的 規範。
- **提交確認**：執行 `commit` 前務必向使用者確認訊息內容是否需要調整。

## 分析變更範圍
在大型專案或變動較多時，**強烈建議使用暫存檔案模式**來執行以下指令，以避免 Agent 卡死：
1. **狀態摘要**：`python .agents/skills/git-committer/scripts/git_helper.py --action get_status --file .agent_scratchpad/status.txt`
2. **開發日誌**：`python .agents/skills/git-committer/scripts/git_helper.py --action get_log --file .agent_scratchpad/log.txt`
3. **完整變更分析**：`python .agents/skills/git-committer/scripts/git_helper.py --action get_all_diff --file .agent_scratchpad/all_diff.txt`

## 大型變更優化與安全讀取協議
對於任何可能產生大量輸出的指令，請遵循以下「安全讀取協議」：
1. **輸出重新導向**：一律加上 `--file .agent_scratchpad/[檔名].txt`。
2. **行數預檢**：讀取前先檢查檔案大小：`wc -l .agent_scratchpad/[檔名].txt`。
3. **分段讀取策略**：
   - 若行數 <= 100：可直接使用 `cat` 或 `view_file` 讀取。
   - 若行數 > 100：使用 `head -n 100` 了解概況，並配合 `view_file` 的行號範圍功能（如 `StartLine: 101, EndLine: 200`）進行分段深入分析。

## 執行工作流
1. **提取變更**：
   - 根據分析結果，將相關變更加入暫存區（`git add`）。
   - 對於大型變更，建議先執行 `get_diff --file [path]` 將最終提交內容暫存分析。
   - 運行 `python .agents/skills/git-committer/scripts/git_helper.py --action get_diff` 獲取最終提交內容。
2. **撰寫草稿**：根據 diff 內容（或暫存檔內容）與分析所得的上下文，參考 [EN_FORMAT.md](EN_FORMAT.md) 或 [CH_FORMAT.md](CH_FORMAT.md) 生成提交訊息。
3. **驗證與修訂**：
   - 檢查是否保留技術專有名詞（如 `EKF`, `DMA`）。
   - 確保訊息反映了「分析變更範圍」中發現的所有核心異動。
   - 驗證與修訂完後，須先向使用者進行內容確認。
4. **執行提交**：運行 `python .agents/skills/git-committer/scripts/git_helper.py --action commit --message "[訊息內容]"` 執行提交。
5. **確認提交**：執行提交後，使用 `git log -n 1` 確認完成提交。

## 錯誤處理
- 若無暫存變更（No staged changes），先執行 `git add`。
- 若腳本返回錯誤，分析錯誤訊息並修正（例如：解決檔案鎖定問題）。