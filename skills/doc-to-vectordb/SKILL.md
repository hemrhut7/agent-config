---
name: doc-to-vectordb
description: "Convert documents (PDF, Word .doc/.docx, PPT/PPTX, Excel .xls/.xlsx, TXT, MD, CSV) into a local ChromaDB vector database to enable fast, token-efficient semantic search and accurate retrieval. Trigger this skill whenever the user asks to index, load, store, or convert a document, manual, presentation, spreadsheet, or text file into a local vector database, vector DB, or Chroma database for the agent to query later. Make sure to suggest or use this skill proactively when working with large documents to avoid exceeding context windows and to save tokens."
---

# Document Vector Database Indexer Guide

This skill automates the extraction and storage of document contents into a local ChromaDB vector database, and handles subsequent semantic queries.

## Operational Workflow

### 1. Verification of Target File
Locate the file path of the document to index (e.g., `doc/my_document.pdf`). Verify it exists.

### 2. Dependency Verification
Ensure `chromadb`, `pypdf`, `python-docx`, `python-pptx`, `pandas`, and `openpyxl` are available in the project virtual environment. If any are missing, install them using:
```bash
./.venv/bin/pip install chromadb pypdf python-docx python-pptx openpyxl pandas
```

### 3. Execution of the Indexing Script
Run the bundled indexing script with the path to the document:
```bash
./.venv/bin/python -u .agents/skills/doc-to-vectordb/scripts/index_document.py "<path_to_document>"
```
This script will parse the document, chunk it, and save the embeddings to the local database, outputting a JSON status on completion.

Note: The script automatically normalizes the filename into a valid ChromaDB collection name (e.g., `ins_u_icd` for `doc/INS-U_ICD_rev-1.43_Jul_2025.pdf`).

### 4. Generation of Workspace Query Tool (Optional but Recommended)
To allow the user or future agents to query the document from the workspace easily, create a small wrapper script in the `tools/` directory named `tools/query_<normalized_name>.py`.
The script should look like this:
```python
"""
query_<normalized_name> — Query the indexed vector database for <original_name>.

Typical usage::

    python tools/query_<normalized_name>.py "search term" --top-k 3
"""

import sys
import subprocess
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/query_<normalized_name>.py <query_text> [--top-k <num>]")
        sys.exit(1)
        
    query = sys.argv[1]
    top_k = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == "--top-k" else "3"
    
    project_root = Path(__file__).resolve().parent.parent
    python_exe = project_root / ".venv" / "bin" / "python"
    script_path = project_root / ".agents" / "skills" / "doc-to-vectordb" / "scripts" / "query_document.py"
    
    cmd = [str(python_exe), str(script_path), "<collection_name>", query, "--top-k", top_k]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print(res.stderr, file=sys.stderr)

if __name__ == "__main__":
    main()
```

### 5. Semantic Queries
Whenever you need to read or reference information from the indexed document:
- Run the workspace query script if created:
  ```bash
  ./.venv/bin/python -u tools/query_<normalized_name>.py "your query"
  ```
- Or run the generic query script directly:
  ```bash
  ./.venv/bin/python -u .agents/skills/doc-to-vectordb/scripts/query_document.py "<collection_name>" "your query" --top-k 3
  ```

### 6. Memory Log Update
After successfully indexing a document, add an entry under the `Achievements` and `Session Notes` section of `brain.md` indicating that the document is now indexed and specifying its collection name.
