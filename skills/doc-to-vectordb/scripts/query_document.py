"""
query_document.py — Query the indexed vector database for a document.

Dependencies:
- chromadb
"""

import sys
import argparse
import json
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent.parent.parent

try:
    from scripts import vectordb_manager
except ImportError as e:
    print(json.dumps({"status": "error", "message": f"Could not import vectordb_manager: {e}"}))
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Query a local vector DB collection.")
    parser.add_argument("collection", type=str, help="ChromaDB collection name")
    parser.add_argument("query", type=str, help="Search query")
    parser.add_argument("--top-k", type=int, default=3, help="Number of matches to return")
    args = parser.parse_args()

    status = vectordb_manager.get_status(collection_name=args.collection)
    if not status.get("initialized"):
        print(json.dumps({"status": "error", "message": f"Collection '{args.collection}' not initialized."}))
        sys.exit(1)

    res = vectordb_manager.search(
        query=args.query,
        top_k=args.top_k,
        collection_name=args.collection
    )

    if res.get("source") == "none":
        print(json.dumps({"status": "success", "results": []}))
        return

    all_results = res.get("all_results", [])
    if not all_results and res.get("content"):
        all_results = [{"content": res["content"], "metadata": {}}]

    output_results = []
    for match in all_results:
        output_results.append({
            "content": match.get("content", ""),
            "metadata": match.get("metadata", {})
        })

    print(json.dumps({"status": "success", "results": output_results}, ensure_ascii=False))


if __name__ == "__main__":
    main()
