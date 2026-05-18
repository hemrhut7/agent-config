"""
Recall_Background(topic) — Mandatory pre-task memory retrieval.

Scans the memory skill's file tree for relevant prior knowledge before starting
a new task. Uses a two-tier approach:
  1. Fast scan: reads the first line (scope comment) of each .md file
  2. Full read: loads matching files
  3. Fallback: searches archive/ via vector DB (stub) if no file match

Usage:
    python -u scripts/recall.py "EKF tuning"
    python -u scripts/recall.py "GNSS denied analysis" --memory-root /path/to/memory
"""

import argparse
import json
import sys
from pathlib import Path


def get_memory_root(override: str | None = None) -> Path:
    """Resolve the memory skill root directory."""
    if override:
        return Path(override)
    # Default: relative to this script's location
    return Path(__file__).resolve().parent.parent


def scan_first_lines(memory_root: Path) -> list[dict]:
    """Scan first lines of all .md files in the memory tree for scope comments."""
    results = []
    for md_file in memory_root.rglob("*.md"):
        # Skip archive for the fast scan pass
        if "archive" in md_file.parts:
            continue
        try:
            first_line = md_file.read_text(encoding="utf-8").split("\n", 1)[0]
            results.append({
                "path": str(md_file.relative_to(memory_root)),
                "scope": first_line.strip(),
                "absolute_path": str(md_file),
            })
        except (OSError, UnicodeDecodeError):
            continue
    return results


def match_topic(topic: str, file_entries: list[dict]) -> list[dict]:
    """Find files whose scope line contains any word from the topic query."""
    topic_words = set(topic.lower().split())
    matches = []
    for entry in file_entries:
        scope_lower = entry["scope"].lower()
        # Score by how many topic words appear in the scope line
        score = sum(1 for w in topic_words if w in scope_lower)
        if score > 0:
            entry["score"] = score
            matches.append(entry)
    # Sort by score descending
    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches


def read_full_file(path: str) -> str:
    """Read the full content of a matched file."""
    try:
        return Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return "(error reading file)"


def search_archive_vectordb(topic: str, memory_root: Path) -> dict:
    """
    Fallback: search archive via vector DB.
    Currently a stub — returns empty result with a guidance message.
    Will be replaced when ChromaDB integration is enabled.
    """
    try:
        from . import vectordb_manager
        return vectordb_manager.search(topic)
    except ImportError:
        try:
            import vectordb_manager
            return vectordb_manager.search(topic)
        except ImportError:
            pass
    except Exception:
        pass
    return {
        "source": "none",
        "content": "",
        "message": "Vector DB not available. Archive search skipped.",
    }


def recall_background(topic: str, memory_root: Path | None = None) -> dict:
    """
    Main entry point for Recall_Background.

    Returns:
        dict with keys: source, content, path, matches
    """
    root = memory_root or get_memory_root()

    # Step 1: Fast scan
    entries = scan_first_lines(root)

    # Step 2: Match
    matches = match_topic(topic, entries)

    if matches:
        best = matches[0]
        content = read_full_file(best["absolute_path"])
        return {
            "source": "file",
            "path": best["path"],
            "content": content,
            "all_matches": [
                {"path": m["path"], "score": m["score"]} for m in matches[:5]
            ],
        }

    # Step 3: Fallback to vector DB
    vdb_result = search_archive_vectordb(topic, root)
    if vdb_result.get("content"):
        return {
            "source": "vectordb",
            "path": vdb_result.get("path", "archive"),
            "content": vdb_result["content"],
            "all_matches": [],
        }

    return {
        "source": "none",
        "path": "",
        "content": "",
        "message": f"No prior knowledge found for topic: '{topic}'",
        "all_matches": [],
    }


def main():
    parser = argparse.ArgumentParser(description="Recall_Background — search memory for prior knowledge")
    parser.add_argument("topic", help="Topic or keywords to search for")
    parser.add_argument("--memory-root", help="Override memory skill root path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    result = recall_background(args.topic, Path(args.memory_root) if args.memory_root else None)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result["source"] == "none":
            print(f"[RECALL] No prior knowledge found for: '{args.topic}'")
            if result.get("message"):
                print(f"  → {result['message']}")
        else:
            print(f"[RECALL] Found in {result['source']}: {result['path']}")
            if result.get("all_matches"):
                print(f"  → {len(result['all_matches'])} total matches")
            print("---")
            # Print first 20 lines of content
            lines = result["content"].split("\n")
            for line in lines[:20]:
                print(line)
            if len(lines) > 20:
                print(f"  ... ({len(lines) - 20} more lines)")


if __name__ == "__main__":
    main()
