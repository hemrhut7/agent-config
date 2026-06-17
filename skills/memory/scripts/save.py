"""
Save_To_LongTerm(tags, content, storage_type) — Persist knowledge to memory.

Called when:
  - A task is completed and produced reusable knowledge
  - The user corrects the agent (learn from correction)
  - A new rule or pitfall is discovered
  - A new script or pattern is established

Usage:
    python -u scripts/save.py --tags "EKF,tuning" --content "..." --type file
    python -u scripts/save.py --tags "error,pymavlink" --content "..." --type auto
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


def get_memory_root() -> Path:
    """Resolve the memory skill root directory."""
    return Path(__file__).resolve().parent.parent


def sanitize_filename(name: str) -> str:
    """Convert a tag or title into a safe filename."""
    name = name.lower().strip()
    name = re.sub(r"[^a-z0-9\-_]", "-", name)
    name = re.sub(r"-+", "-", name).strip("-")
    return name or "untitled"


def determine_target_file(tags: list[str], memory_root: Path) -> Path:
    """Decide which file to write to based on tags."""
    user_tags = {"preference", "habit", "communication", "workflow", "user"}
    if any(t.lower() in user_tags for t in tags):
        return memory_root / "user" / "preferences.md"

    # Map specific tags to consolidated files
    tag_mapping = {
        "ekf": "navigation-estimation",
        "navigation": "navigation-estimation",
        "slam": "navigation-estimation",
        "estimation": "navigation-estimation",
        "calibration": "navigation-estimation",
        "uavlogviewer": "ui-ux",
        "plotly": "ui-ux",
        "pyside6": "ui-ux",
        "ui-ux": "ui-ux",
    }

    primary_tag = tags[0].lower() if tags else "general"
    consolidated_tag = tag_mapping.get(primary_tag, primary_tag)
    
    topic_name = f"topic-{sanitize_filename(consolidated_tag)}.md"
    return memory_root / "topics" / topic_name


def check_line_limit(filepath: Path, limit: int) -> bool:
    """Check if a file is within its line limit."""
    if not filepath.exists():
        return True
    line_count = len(filepath.read_text(encoding="utf-8").split("\n"))
    return line_count <= limit


def get_line_limit(filepath: Path, memory_root: Path) -> int:
    """Get the line limit for a given file based on its location."""
    rel = filepath.relative_to(memory_root)
    parts = rel.parts
    if rel.name == "SKILL.md":
        return 60
    if "user" in parts:
        return 40
    if "topics" in parts:
        return 100
    return 200  # default generous limit


def append_to_file(filepath: Path, content: str, tags: list[str]) -> dict:
    """Append content to a markdown file with metadata header."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    tag_str = ", ".join(tags)

    entry = f"\n### [{timestamp}] Tags: {tag_str}\n{content}\n"

    if not filepath.exists():
        # Create with scope comment as first line
        scope = f"<!-- SCOPE: Knowledge about {tags[0] if tags else 'general topics'}. Read when related tasks arise. -->"
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(f"{scope}\n# {tags[0].title() if tags else 'General'}\n{entry}", encoding="utf-8")
    else:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(entry)

    return {
        "action": "appended",
        "path": str(filepath),
        "timestamp": timestamp,
    }


def save_to_vector(tags: list[str], content: str, memory_root: Path) -> dict:
    """
    Save content to vector DB for fuzzy retrieval.
    Currently a stub — logs intention and returns guidance.
    """
    try:
        from . import vectordb_manager
        return vectordb_manager.add_document(content, {"tags": tags})
    except (ImportError, Exception):
        return {
            "action": "skipped",
            "reason": "Vector DB not available. Content was NOT persisted to vector storage.",
            "suggestion": "Install chromadb to enable vector storage: pip install chromadb",
        }


def auto_determine_type(content: str) -> str:
    """
    Heuristic to decide storage type.
    Structured/factual content → file; long narrative → vector.
    """
    lines = content.strip().split("\n")
    # Short, structured content goes to files
    if len(lines) <= 15:
        return "file"
    # Content with many bullet points or headers is structured
    structured_markers = sum(1 for l in lines if l.strip().startswith(("-", "#", "*", ">")))
    if structured_markers / max(len(lines), 1) > 0.3:
        return "file"
    # Long unstructured text goes to vector
    return "vector"


def save_to_longterm(
    tags: list[str],
    content: str,
    storage_type: str = "auto",
    memory_root: Path | None = None,
) -> dict:
    """
    Main entry point for Save_To_LongTerm.

    Args:
        tags: List of topic tags for categorization
        content: The knowledge content to save
        storage_type: "file", "vector", or "auto"
        memory_root: Override memory root path

    Returns:
        dict with action details
    """
    root = memory_root or get_memory_root()

    if storage_type == "auto":
        storage_type = auto_determine_type(content)

    if storage_type == "file":
        target = determine_target_file(tags, root)
        limit = get_line_limit(target, root)

        result = append_to_file(target, content, tags)

        # Check if we exceeded line limit
        if not check_line_limit(target, limit):
            result["warning"] = f"File exceeds {limit}-line limit. Run compress.py to enforce."

        return result

    elif storage_type == "vector":
        return save_to_vector(tags, content, root)

    else:
        return {"action": "error", "reason": f"Unknown storage_type: {storage_type}"}


def main():
    parser = argparse.ArgumentParser(description="Save_To_LongTerm — persist knowledge to memory")
    parser.add_argument("--tags", required=True, help="Comma-separated tags (e.g. 'EKF,tuning')")
    parser.add_argument("--content", required=True, help="Content to save")
    parser.add_argument("--type", choices=["file", "vector", "auto"], default="auto",
                        help="Storage type (default: auto)")
    parser.add_argument("--memory-root", help="Override memory skill root path")
    args = parser.parse_args()

    tags = [t.strip() for t in args.tags.split(",")]
    result = save_to_longterm(
        tags=tags,
        content=args.content,
        storage_type=args.type,
        memory_root=Path(args.memory_root) if args.memory_root else None,
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
