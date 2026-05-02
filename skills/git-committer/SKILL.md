---
name: git-committer
description: 分析 Git 變更、生成符合規範的提交訊息並執行 commit。當用戶提到 'commit', '提交', '存檔', '把剛才的修改存起來'，或是一段長任務結束後需要推進版控時，強制觸發此工作流。
---

# Git 提交管理工作流

## 核心規則
- **自動化優先**：優先調用 `.agents/skills/git-committer/scripts/git_helper.py --action analyze_all` 一鍵獲取所有背景資訊。
- **分析全面**：在提交前，應確認所有變更。腳本會自動檢測「已暫存 (Staged)」與「未暫存 (Unstaged)」變更、衝突狀態及子模組狀態。
- **格式合規**：根據語境選擇語言（預設英文）。
   - 英文訊息：符合 [EN_FORMAT.md](EN_FORMAT.md)。
   - 中文訊息：符合 [CH_FORMAT.md](CH_FORMAT.md)。
- **提交確認**：執行 `commit` 前務必向使用者確認訊息內容。

## 執行工作流

1. **一鍵提取分析**：
   運行 `python .agents/skills/git-committer/scripts/git_helper.py --action analyze_all`。
   - **注意**：若變更內容過大，腳本會自動將報告儲存至 `.agent_scratchpad/auto_analysis.md` 並在終端機顯示摘要。
   - 請根據報告內容（若有暫存檔請讀取之）撰寫 Commit Message。

2. **撰寫草稿**：
   參考報告中的 `Detailed Staged Diff` 與 `Recent Commits Context` 生成提交訊息。

3. **驗證與修訂**：
   - 檢查是否保留技術專有名詞（如 `EKF`, `DMA`）。
   - 確保訊息反映了報告中發現的所有核心異動。
   - 驗證後，向使用者進行內容確認。

4. **執行提交**：
   運行 `python .agents/skills/git-committer/scripts/git_helper.py --action commit --message "[訊息內容]"`。
   - **防護機制**：若存在未解決的衝突，腳本會自動中止提交。

5. **確認提交**：
   使用 `git log -n 1` 確認。

## 錯誤處理
- **No staged changes**：先執行 `git add`。
- **衝突警告**：若腳本提示衝突，請先解決衝突後再重新執行 `analyze_all`。
- **子模組 Dirty**：若子模組有變更，請先進入子模組目錄進行處理。