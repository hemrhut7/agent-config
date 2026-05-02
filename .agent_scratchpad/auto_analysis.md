# Git Analysis Report

## Status Summary

M  skills/git-committer/SKILL.md
M  skills/git-committer/scripts/git_helper.py

## Staged Changes Statistics

skills/git-committer/SKILL.md              |  86 +++++-----
 skills/git-committer/scripts/git_helper.py | 256 ++++++++++++++++++-----------
 2 files changed, 202 insertions(+), 140 deletions(-)

## Recent Commits Context

c2a4240 refactor(skills): optimize and consolidate agent skill infrastructure
99aa654 modify graphify skill
f22d0a8 make graphify can be run by global environment pyhon
8d577b1 feat(skills): add docx, pptx, web-artifacts-builder, webapp-testing, and xlsx skills
85e6a83 Merge branch 'main' of https://github.com/hemrhut7/agent-config

## Detailed Staged Diff

```diff
diff --git a/skills/git-committer/SKILL.md b/skills/git-committer/SKILL.md
index e7c3014..506335e 100644
--- a/skills/git-committer/SKILL.md
+++ b/skills/git-committer/SKILL.md
@@ -1,45 +1,41 @@
----
-name: git-committer
-description: 分析 Git 暫存區變更、生成符合規範的提交訊息並執行 commit。於用戶要求提交程式碼或完成任務後需存檔時使用。
----
-
-# Git 提交管理工作流
-
-## 核心規則
-- **自動化優先**：優先調用 `.agents/skills/git-committer/scripts/git_helper.py` 獲取變更內容。
-- **分析全面**：在提交前，應分析包括已暫存（Staged）與未暫存（Unstaged）的所有變更，並參考最近的提交紀錄以確保上下文一致。
-- **格式合規**：請區分用戶要使用中文還是英文進行訊息撰寫，若沒特別說明則預設使用英文，
-   - 若判斷使用英文撰寫，訊息必須符合 [EN_FORMAT.md](EN_FORMAT.md) 的 規範。
-   - 若判斷使用中文撰寫，訊息必須符合 [CH_FORMAT.md](CH_FORMAT.md) 的 規範。
-- **提交確認**：執行 `commit` 前務必向使用者確認訊息內容是否需要調整。
-
-## 分析變更範圍
-在大型專案或變動較多時，**強烈建議使用暫存檔案模式**來執行以下指令，以避免 Agent 卡死：
-1. **狀態摘要**：`python .agents/skills/git-committer/scripts/git_helper.py --action get_status --file .agent_scratchpad/status.txt`
-2. **開發日誌**：`python .agents/skills/git-committer/scripts/git_helper.py --action get_log --file .agent_scratchpad/log.txt`
-3. **完整變更分析**：`python .agents/skills/git-committer/scripts/git_helper.py --action get_all_diff --file .agent_scratchpad/all_diff.txt`
-
-## 大型變更優化與安全讀取協議
-對於任何可能產生大量輸出的指令，請遵循以下「安全讀取協議」：
-1. **輸出重新導向**：一律加上 `--file .agent_scratchpad/[檔名].txt`。
-2. **行數預檢**：讀取前先檢查檔案大小：`wc -l .agent_scratchpad/[檔名].txt`。
-3. **分段讀取策略**：
-   - 若行數 <= 100：可直接使用 `cat` 或 `view_file` 讀取。
-   - 若行數 > 100：使用 `head -n 100` 了解概況，並配合 `view_file` 的行號範圍功能（如 `StartLine: 101, EndLine: 200`）進行分段深入分析。
-
-## 執行工作流
-1. **提取變更**：
-   - 根據分析結果，將相關變更加入暫存區（`git add`）。
-   - 對於大型變更，建議先執行 `get_diff --file [path]` 將最終提交內容暫存分析。
-   - 運行 `python .agents/skills/git-committer/scripts/git_helper.py --action get_diff` 獲取最終提交內容。
-2. **撰寫草稿**：根據 diff 內容（或暫存檔內容）與分析所得的上下文，參考 [EN_FORMAT.md](EN_FORMAT.md) 或 [CH_FORMAT.md](CH_FORMAT.md) 生成提交訊息。
-3. **驗證與修訂**：
-   - 檢查是否保留技術專有名詞（如 `EKF`, `DMA`）。
-   - 確保訊息反映了「分析變更範圍」中發現的所有核心異動。
-   - 驗證與修訂完後，須先向使用者進行內容確認。
-4. **執行提交**：運行 `python .agents/skills/git-committer/scripts/git_helper.py --action commit --message "[訊息內容]"` 執行提交。
-5. **確認提交**：執行提交後，使用 `git log -n 1` 確認完成提交。
-
-## 錯誤處理
-- 若無暫存變更（No staged changes），先執行 `git add`。
-- 若腳本返回錯誤，分析錯誤訊息並修正（例如：解決檔案鎖定問題）。
\ No newline at end of file
+---
+name: git-committer
+description: 分析 Git 變更、生成符合規範的提交訊息並執行 commit。當用戶提到 'commit', '提交', '存檔', '把剛才的修改存起來'，或是一段長任務結束後需要推進版控時，強制觸發此工作流。
+---
+
+# Git 提交管理工作流
+
+## 核心規則
+- **自動化優先**：優先調用 `.agents/skills/git-committer/scripts/git_helper.py --action analyze_all` 一鍵獲取所有背景資訊。
+- **分析全面**：在提交前，應確認所有變更。腳本會自動檢測「已暫存 (Staged)」與「未暫存 (Unstaged)」變更、衝突狀態及子模組狀態。
+- **格式合規**：根據語境選擇語言（預設英文）。
+   - 英文訊息：符合 [EN_FORMAT.md](EN_FORMAT.md)。
+   - 中文訊息：符合 [CH_FORMAT.md](CH_FORMAT.md)。
+- **提交確認**：執行 `commit` 前務必向使用者確認訊息內容。
+
+## 執行工作流
+
+1. **一鍵提取分析**：
+   運行 `python .agents/skills/git-committer/scripts/git_helper.py --action analyze_all`。
+   - **注意**：若變更內容過大，腳本會自動將報告儲存至 `.agent_scratchpad/auto_analysis.md` 並在終端機顯示摘要。
+   - 請根據報告內容（若有暫存檔請讀取之）撰寫 Commit Message。
+
+2. **撰寫草稿**：
+   參考報告中的 `Detailed Staged Diff` 與 `Recent Commits Context` 生成提交訊息。
+
+3. **驗證與修訂**：
+   - 檢查是否保留技術專有名詞（如 `EKF`, `DMA`）。
+   - 確保訊息反映了報告中發現的所有核心異動。
+   - 驗證後，向使用者進行內容確認。
+
+4. **執行提交**：
+   運行 `python .agents/skills/git-committer/scripts/git_helper.py --action commit --message "[訊息內容]"`。
+   - **防護機制**：若存在未解決的衝突，腳本會自動中止提交。
+
+5. **確認提交**：
+   使用 `git log -n 1` 確認。
+
+## 錯誤處理
+- **No staged changes**：先執行 `git add`。
+- **衝突警告**：若腳本提示衝突，請先解決衝突後再重新執行 `analyze_all`。
+- **子模組 Dirty**：若子模組有變更，請先進入子模組目錄進行處理。
\ No newline at end of file
diff --git a/skills/git-committer/scripts/git_helper.py b/skills/git-committer/scripts/git_helper.py
index c479066..cc648e9 100644
--- a/skills/git-committer/scripts/git_helper.py
+++ b/skills/git-committer/scripts/git_helper.py
@@ -1,95 +1,161 @@
-import subprocess
-import sys
-import os
-
-def run_command(cmd):
-    try:
-        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
-        return result.stdout.strip()
-    except subprocess.CalledProcessError as e:
-        # Keep errors separate if needed, but for now we return None to let caller handle
-        sys.stderr.write(f"Error executing {' '.join(cmd)}: {e.stderr}\n")
-        return None
-    except UnicodeDecodeError:
-        # Fallback for systems with different default encodings
-        result = subprocess.run(cmd, capture_output=True, text=False, check=True)
-        return result.stdout.decode('utf-8', errors='replace').strip()
-
-def get_staged_diff():
-    # 僅獲取已暫存的變更內容
-    diff = run_command(["git", "diff", "--cached"])
-    if diff is None:
-        return "Error: Could not retrieve staged changes."
-    if not diff:
-        return ""
-    return diff
-
-def get_unstaged_diff():
-    # 獲取未暫存的變更內容
-    diff = run_command(["git", "diff"])
-    if diff is None:
-        return "Error: Could not retrieve unstaged changes."
-    return diff
-
-def get_status():
-    # 獲取 git 狀態摘要
-    status = run_command(["git", "status", "-s"])
-    if status is None:
-        return "Error: Could not retrieve git status."
-    return status
-
-def get_log():
-    # 獲取最近 5 條提交日誌
-    log = run_command(["git", "log", "-n", "5", "--oneline"])
-    if log is None:
-        return "Error: Could not retrieve git log."
-    return log
-
-def get_all_diff():
-    # 獲取自上次提交以來的所有變更（暫存 + 未暫存）
-    diff = run_command(["git", "diff", "HEAD"])
-    if diff is None:
-        return "Error: Could not retrieve all changes."
-    return diff
-
-def execute_commit(message):
-    # 執行提交
-    return run_command(["git", "commit", "-m", message])
-
-if __name__ == "__main__":
-    import argparse
-    parser = argparse.ArgumentParser()
-    parser.add_argument("--action", choices=["get_diff", "get_unstaged_diff", "get_status", "get_log", "get_all_diff", "commit"])
-    parser.add_argument("--message", type=str)
-    parser.add_argument("--file", type=str, help="Output the result to a specified file")
-    args = parser.parse_args()
-
-    result_text = ""
-    if args.action == "get_diff":
-        result_text = get_staged_diff()
-        if not result_text:
-            result_text = "No staged changes found. Please run 'git add' first."
-    elif args.action == "get_unstaged_diff":
-        result_text = get_unstaged_diff()
-    elif args.action == "get_status":
-        result_text = get_status()
-    elif args.action == "get_log":
-        result_text = get_log()
-    elif args.action == "get_all_diff":
-        result_text = get_all_diff()
-    elif args.action == "commit" and args.message:
-        result_text = execute_commit(args.message)
-
-    if result_text:
-        if args.file:
-            try:
-                # Ensure the parent directory exists
-                os.makedirs(os.path.dirname(os.path.abspath(args.file)), exist_ok=True)
-                with open(args.file, "w", encoding="utf-8") as f:
-                    f.write(result_text)
-                print(f"Results saved to {args.file}")
-            except Exception as e:
-                print(f"Error saving to file: {e}")
-                print(result_text)
-        else:
-            print(result_text)
\ No newline at end of file
+import subprocess
+import sys
+import os
+
+# Threshold for auto-redirection to prevent terminal hanging
+MAX_TERMINAL_OUTPUT = 5000 
+
+def run_command(cmd):
+    try:
+        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
+        return result.stdout.strip()
+    except subprocess.CalledProcessError as e:
+        sys.stderr.write(f"Error executing {' '.join(cmd)}: {e.stderr}\n")
+        return None
+    except UnicodeDecodeError:
+        result = subprocess.run(cmd, capture_output=True, text=False, check=True)
+        return result.stdout.decode('utf-8', errors='replace').strip()
+
+def get_staged_diff():
+    diff = run_command(["git", "diff", "--cached"])
+    if diff is None: return "Error: Could not retrieve staged changes."
+    return diff
+
+def get_unstaged_diff():
+    diff = run_command(["git", "diff"])
+    if diff is None: return "Error: Could not retrieve unstaged changes."
+    return diff
+
+def get_status():
+    status = run_command(["git", "status", "-s"])
+    if status is None: return "Error: Could not retrieve git status."
+    return status
+
+def get_log():
+    log = run_command(["git", "log", "-n", "5", "--oneline"])
+    if log is None: return "Error: Could not retrieve git log."
+    return log
+
+def get_diff_stat():
+    stat = run_command(["git", "diff", "--cached", "--stat"])
+    return stat if stat else ""
+
+def check_conflicts():
+    conflicts = run_command(["git", "ls-files", "-u"])
+    return conflicts if conflicts else None
+
+def check_submodules():
+    if os.path.exists(".gitmodules"):
+        status = run_command(["git", "submodule", "status"])
+        return status
+    return None
+
+def analyze_all():
+    report = []
+    report.append("# Git Analysis Report")
+    
+    # 1. Conflicts Pre-flight
+    conflicts = check_conflicts()
+    if conflicts:
+        report.append("## ⚠️ WARNING: Unmerged Conflicts Detected")
+        report.append("Please resolve these conflicts before committing:\n" + conflicts)
+    
+    # 2. Status
+    status = get_status()
+    report.append("## Status Summary")
+    report.append(status if status else "No changes detected.")
+    
+    # 3. Submodules
+    submodules = check_submodules()
+    if submodules:
+        report.append("## Submodule Status")
+        report.append(submodules)
+    
+    # 4. Diff Stat
+    stat = get_diff_stat()
+    if stat:
+        report.append("## Staged Changes Statistics")
+        report.append(stat)
+    
+    # 5. Recent Logs
+    log = get_log()
+    report.append("## Recent Commits Context")
+    report.append(log)
+    
+    # 6. Full Diff
+    diff = get_staged_diff()
+    if diff:
+        report.append("## Detailed Staged Diff")
+        # Use fenced code block for better readability in artifacts
+        report.append(f"```diff\n{diff}\n```")
+    
+    return "\n\n".join(report)
+
+def handle_output(content, output_file=None):
+    if not content:
+        return
+        
+    target_file = output_file
+    is_auto_redirected = False
+    
+    # Auto-redirect if content is too large and no file is specified
+    if not target_file and len(content) > MAX_TERMINAL_OUTPUT:
+        target_file = ".agent_scratchpad/auto_analysis.md"
+        is_auto_redirected = True
+        
+    if target_file:
+        try:
+            os.makedirs(os.path.dirname(os.path.abspath(target_file)), exist_ok=True)
+            with open(target_file, "w", encoding="utf-8") as f:
+                f.write(content)
+            
+            if is_auto_redirected:
+                print(f"⚠️ Output is too large ({len(content)} chars). Automatically saved to: {target_file}")
+                print("\n--- Summary Preview ---")
+                lines = content.split('\n')
+                # Show first 30 lines for context
+                for line in lines[:30]:
+                    print(line)
+                if len(lines) > 30:
+                    print("\n... (content truncated, please read the file for full details) ...")
+            else:
+                print(f"Results saved to {target_file}")
+        except Exception as e:
+            print(f"Error saving to file: {e}")
+            # Fallback to truncated stdout
+            print(content[:MAX_TERMINAL_OUTPUT] + "\n... (truncated due to error)")
+    else:
+        print(content)
+
+if __name__ == "__main__":
+    import argparse
+    parser = argparse.ArgumentParser()
+    parser.add_argument("--action", choices=["get_diff", "get_unstaged_diff", "get_status", "get_log", "get_all_diff", "commit", "analyze_all"])
+    parser.add_argument("--message", type=str)
+    parser.add_argument("--file", type=str, help="Output the result to a specified file")
+    args = parser.parse_args()
+
+    result_text = ""
+    if args.action == "get_diff":
+        result_text = get_staged_diff()
+        if not result_text.strip():
+            result_text = "No staged changes found. Please run 'git add' first."
+    elif args.action == "get_unstaged_diff":
+        result_text = get_unstaged_diff()
+    elif args.action == "get_status":
+        result_text = get_status()
+    elif args.action == "get_log":
+        result_text = get_log()
+    elif args.action == "get_all_diff":
+        result_text = run_command(["git", "diff", "HEAD"])
+    elif args.action == "analyze_all":
+        result_text = analyze_all()
+    elif args.action == "commit" and args.message:
+        # Check conflicts before commit
+        if check_conflicts():
+            result_text = "❌ ABORTED: Unmerged conflicts detected. Please resolve them first."
+        else:
+            result_text = run_command(["git", "commit", "-m", args.message])
+
+    if result_text:
+        handle_output(result_text, args.file)
\ No newline at end of file
```