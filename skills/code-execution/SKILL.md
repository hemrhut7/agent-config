---
name: code-execution
description: 使用 Python 腳本執行批量檔案操作或複雜多步驟工作流。當任務涉及 10+ 檔案的批量處理、資料轉換或自動化流程時使用。
---

# 批量程式碼執行

使用 Python 腳本處理涉及大量檔案或多步驟的批量操作，避免逐一手動處理。

## 適用時機

- 批量操作（10+ 檔案）
- 複雜多步驟工作流
- 跨多檔案的迭代處理

## 執行策略

### 1. 撰寫批量處理腳本
將批量邏輯寫入 `.agent_scratchpad/` 內的臨時 Python 腳本：

```python
# .agent_scratchpad/batch_process.py
from pathlib import Path
import re

results = {"modified": 0, "skipped": 0, "errors": []}

for py_file in Path("src").rglob("*.py"):
    content = py_file.read_text(encoding="utf-8")
    new_content = re.sub(r"old_pattern", "new_pattern", content)
    if new_content != content:
        py_file.write_text(new_content, encoding="utf-8")
        results["modified"] += 1
    else:
        results["skipped"] += 1

print(f"Modified: {results['modified']}, Skipped: {results['skipped']}")
```

### 2. 使用 venv 執行
遵循 `run-python` 技能的執行規範：
```bash
.\.venv\Scripts\python.exe -u .agent_scratchpad/batch_process.py
```

### 3. 回報摘要
返回統計摘要（修改了多少檔案、跳過了多少），而非完整檔案內容。

### 4. 清理臨時檔案
執行完畢後刪除 `.agent_scratchpad/` 中的臨時腳本。

## 最佳實踐

✅ 返回統計摘要，不返回完整檔案內容  
✅ 批量處理而非逐一操作  
✅ 使用 `pathlib` 進行跨平台路徑處理  
✅ 包含錯誤計數與處理  

❌ 不要將所有程式碼內容回傳到 context  
❌ 不要逐檔案使用編輯工具（> 10 個檔案時）  
