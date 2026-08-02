"""
index_document.py — Index PDF, Word, PPT, Excel, and Text files into a local vector database.

Dependencies:
- pypdf
- python-docx
- python-pptx
- pandas
- openpyxl
- chromadb
"""

import sys
import os
import re
import argparse
import json
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent.parent.parent

try:
    from scripts import vectordb_manager
except ImportError as e:
    print(json.dumps({"status": "error", "message": f"Could not import vectordb_manager: {e}"}))
    sys.exit(1)


def normalize_collection_name(name: str) -> str:
    """Normalize a string to a valid ChromaDB collection name."""
    # ChromaDB collection naming rules:
    # 1. 3-63 characters long
    # 2. Starts and ends with alphanumeric
    # 3. Contains only alphanumeric, hyphens, underscores, dots
    # 4. No consecutive dots
    cleaned = re.sub(r'[^a-zA-Z0-9\-_.]', '_', name.lower())
    cleaned = re.sub(r'\.+', '.', cleaned)
    cleaned = cleaned.strip('_-.')
    if len(cleaned) < 3:
        cleaned = cleaned + "_col"
    return cleaned[:63]


def parse_pdf(file_path: Path) -> list[dict]:
    from pypdf import PdfReader
    reader = PdfReader(file_path)
    chunks = []
    for idx, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        text = text.strip()
        if text:
            chunks.append({
                "text": text,
                "metadata": {"page": idx + 1, "type": "pdf"}
            })
    return chunks


def parse_docx(file_path: Path) -> list[dict]:
    import docx
    doc = docx.Document(file_path)
    chunks = []
    current_chunk = []
    current_len = 0
    chunk_idx = 1
    
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        current_chunk.append(text)
        current_len += len(text)
        
        # Chunk size threshold ~1000 characters
        if current_len >= 1000:
            chunks.append({
                "text": "\n".join(current_chunk),
                "metadata": {"chunk": chunk_idx, "type": "docx"}
            })
            chunk_idx += 1
            current_chunk = []
            current_len = 0
            
    if current_chunk:
        chunks.append({
            "text": "\n".join(current_chunk),
            "metadata": {"chunk": chunk_idx, "type": "docx"}
        })
    return chunks


def parse_pptx(file_path: Path) -> list[dict]:
    from pptx import Presentation
    prs = Presentation(file_path)
    chunks = []
    for idx, slide in enumerate(prs.slides):
        slide_text = []
        for shape in slide.shapes:
            if hasattr(shape, "text") and shape.text.strip():
                slide_text.append(shape.text.strip())
        text = "\n".join(slide_text).strip()
        if text:
            chunks.append({
                "text": text,
                "metadata": {"slide": idx + 1, "type": "pptx"}
            })
    return chunks


def parse_excel(file_path: Path) -> list[dict]:
    import pandas as pd
    excel_file = pd.ExcelFile(file_path)
    chunks = []
    for sheet_name in excel_file.sheet_names:
        df = excel_file.parse(sheet_name)
        if df.empty:
            continue
        # Convert sheet to CSV-like string
        text_content = df.to_csv(index=False)
        lines = text_content.strip().split("\n")
        header = lines[0]
        # Chunk row data in groups of 20 rows
        row_groups = [lines[i:i+20] for i in range(1, len(lines), 20)]
        for idx, group in enumerate(row_groups):
            chunk_text = f"Sheet: {sheet_name}\n{header}\n" + "\n".join(group)
            chunks.append({
                "text": chunk_text,
                "metadata": {"sheet": sheet_name, "chunk": idx + 1, "type": "excel"}
            })
    return chunks


def parse_text(file_path: Path) -> list[dict]:
    text = file_path.read_text(encoding="utf-8", errors="ignore")
    paragraphs = text.strip().split("\n\n")
    chunks = []
    current_chunk = []
    current_len = 0
    chunk_idx = 1
    
    for para in paragraphs:
        para_stripped = para.strip()
        if not para_stripped:
            continue
        current_chunk.append(para_stripped)
        current_len += len(para_stripped)
        
        if current_len >= 1000:
            chunks.append({
                "text": "\n\n".join(current_chunk),
                "metadata": {"chunk": chunk_idx, "type": "text"}
            })
            chunk_idx += 1
            current_chunk = []
            current_len = 0
            
    if current_chunk:
        chunks.append({
            "text": "\n\n".join(current_chunk),
            "metadata": {"chunk": chunk_idx, "type": "text"}
        })
    return chunks


def main():
    parser = argparse.ArgumentParser(description="Index a document into a local vector database.")
    parser.add_argument("file_path", type=str, help="Path to the file to index")
    parser.add_argument("--collection", type=str, default=None, help="ChromaDB collection name override")
    args = parser.parse_args()

    file_path = Path(args.file_path)
    if not file_path.exists():
        print(json.dumps({"status": "error", "message": f"File not found: {file_path}"}))
        sys.exit(1)

    suffix = file_path.suffix.lower()
    
    try:
        if suffix == ".pdf":
            chunks = parse_pdf(file_path)
        elif suffix == ".docx":
            chunks = parse_docx(file_path)
        elif suffix == ".pptx":
            chunks = parse_pptx(file_path)
        elif suffix in [".xlsx", ".xls"]:
            chunks = parse_excel(file_path)
        elif suffix in [".txt", ".md", ".csv"]:
            chunks = parse_text(file_path)
        elif suffix in [".doc", ".ppt"]:
            msg = f"Old binary formats (.doc, .ppt) are not supported directly. Please convert '{file_path.name}' to modern XML formats (.docx, .pptx) first."
            print(json.dumps({"status": "error", "message": msg}))
            sys.exit(1)
        else:
            chunks = parse_text(file_path)
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"Failed to parse document: {str(e)}"}))
        sys.exit(1)

    if not chunks:
        print(json.dumps({"status": "error", "message": "No text content could be extracted from the document."}))
        sys.exit(1)

    collection_name = args.collection
    if not collection_name:
        collection_name = normalize_collection_name(file_path.stem)

    vectordb_manager.init_db(collection_name=collection_name)
    
    indexed_count = 0
    for chunk in chunks:
        meta = chunk["metadata"]
        meta["source"] = file_path.name
        
        res = vectordb_manager.add_document(
            text=chunk["text"],
            metadata=meta,
            collection_name=collection_name
        )
        if res.get("status") == "stored":
            indexed_count += 1

    result = {
        "status": "success",
        "file_name": file_path.name,
        "collection_name": collection_name,
        "total_chunks": len(chunks),
        "indexed_chunks": indexed_count
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
