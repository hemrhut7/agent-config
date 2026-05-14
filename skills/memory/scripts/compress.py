"""
Line-Limit Enforcement — compress files that exceed their line limits.

Enforced limits:
  - SKILL.md          ≤ 60 lines
  - user/preferences.md ≤ 40 lines
  - topics/*.md       ≤ 100 lines per file

When a file exceeds its limit, the older half of the content is summarized
and moved to archive/, keeping the file under its threshold.

Usage:
    python -u scripts/compress.py                     # Check all files
    python -u scripts/compress.py --fix               # Auto-compress violations
    python -u scripts/compress.py --file topics/ekf.md  # Check specific file
"""

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path


# Line limits by file pattern
LINE_LIMITS = {
    "SKILL.md": 60,
    "user/preferences.md": 40,
    "topics/": 100,   # per file
    "brain.md": 200,   # generous for working memory
}


def get_memory_root() -> Path:
    return Path(__file__).resolve().parent.parent


def get_line_limit(filepath: Path, memory_root: Path) -> int:
    """Determine the line limit for a file based on its relative path."""
    try:
        rel = str(filepath.relative_to(memory_root))
    except ValueError:
        return 200

    if rel == "SKILL.md":
        return LINE_LIMITS["SKILL.md"]
    elif rel.startswith("user/"):
        return LINE_LIMITS["user/preferences.md"]
    elif rel.startswith("topics/"):
        return LINE_LIMITS["topics/"]
    elif rel == "brain.md":
        return LINE_LIMITS["brain.md"]
    return 200


def check_file(filepath: Path, memory_root: Path) -> dict:
    """Check a single file against its line limit."""
    if not filepath.exists():
        return {"path": str(filepath), "status": "not_found"}

    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")
    line_count = len(lines)
    limit = get_line_limit(filepath, memory_root)

    return {
        "path": str(filepath.relative_to(memory_root)),
        "line_count": line_count,
        "limit": limit,
        "over": max(0, line_count - limit),
        "status": "ok" if line_count <= limit else "over_limit",
    }


def check_all(memory_root: Path) -> list[dict]:
    """Check all managed files against their limits."""
    results = []

    # Check SKILL.md
    skill_md = memory_root / "SKILL.md"
    if skill_md.exists():
        results.append(check_file(skill_md, memory_root))

    # Check user/preferences.md
    prefs = memory_root / "user" / "preferences.md"
    if prefs.exists():
        results.append(check_file(prefs, memory_root))

    # Check brain.md
    brain = memory_root / "brain.md"
    if brain.exists():
        results.append(check_file(brain, memory_root))

    # Check all topics
    topics_dir = memory_root / "topics"
    if topics_dir.exists():
        for md_file in topics_dir.glob("*.md"):
            results.append(check_file(md_file, memory_root))

    return results


def compress_file(filepath: Path, memory_root: Path) -> dict:
    """
    Compress a file that exceeds its line limit.

    Strategy:
    - Keep the first line (scope comment) and the most recent content
    - Archive the older portion to archive/compressed/
    """
    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")
    limit = get_line_limit(filepath, memory_root)

    if len(lines) <= limit:
        return {"action": "skipped", "reason": "File is within limit"}

    # Archive the full content first
    archive_dir = memory_root / "archive" / "compressed"
    archive_dir.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    rel_name = filepath.relative_to(memory_root).as_posix().replace("/", "_")
    archive_path = archive_dir / f"{rel_name}_{date_str}.md"
    shutil.copy2(filepath, archive_path)

    # Keep: first line (scope) + last (limit - 5) lines
    # This preserves the most recent entries
    keep_lines = limit - 5  # Leave room for a compression notice
    first_line = lines[0]
    kept_content = lines[-keep_lines:]

    # Build compressed file
    compressed = [
        first_line,
        "",
        f"> [!NOTE]",
        f"> Compressed on {date_str}. Older content archived to `{archive_path.relative_to(memory_root)}`.",
        "",
        *kept_content,
    ]

    filepath.write_text("\n".join(compressed), encoding="utf-8")

    return {
        "action": "compressed",
        "path": str(filepath.relative_to(memory_root)),
        "original_lines": len(lines),
        "compressed_lines": len(compressed),
        "archived_to": str(archive_path.relative_to(memory_root)),
    }


def compress_all_violations(memory_root: Path) -> list[dict]:
    """Find and compress all files exceeding their limits."""
    checks = check_all(memory_root)
    results = []

    for check in checks:
        if check["status"] == "over_limit":
            filepath = memory_root / check["path"]
            result = compress_file(filepath, memory_root)
            results.append(result)

    return results


def main():
    parser = argparse.ArgumentParser(description="Line-Limit Enforcement — check and compress files")
    parser.add_argument("--fix", action="store_true", help="Auto-compress files exceeding limits")
    parser.add_argument("--file", help="Check a specific file (relative to memory root)")
    parser.add_argument("--memory-root", help="Override memory skill root path")
    args = parser.parse_args()

    root = Path(args.memory_root) if args.memory_root else get_memory_root()

    if args.file:
        filepath = root / args.file
        result = check_file(filepath, root)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.fix:
        results = compress_all_violations(root)
        if results:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print("All files are within their line limits.")
    else:
        results = check_all(root)
        print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
