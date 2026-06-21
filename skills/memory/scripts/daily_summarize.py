"""
Daily Summarize & Archive — Time-gated brain.md settlement.

Extracts valuable knowledge from today's brain.md, writes it to topics/ or
user/preferences.md, then archives the raw content to archive/brain_YYYY-MM-DD.md
and resets brain.md to the empty template.

Time-gate: triggers auto-suggest if >8 hours since last brain.md modification.

Usage:
    python -u scripts/daily_summarize.py                    # Check + execute
    python -u scripts/daily_summarize.py --check-only       # Only check if due
    python -u scripts/daily_summarize.py --force             # Skip time gate
"""

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path


HOURS_THRESHOLD = 8

BRAIN_TEMPLATE = """<!-- SCOPE: Today's task log and working memory. Read at conversation start to resume context. -->
# Brain — Working Memory

## Last Updated: {timestamp}

### Active Tasks
- (See project-specific tasks in [task/{project_name}.md](task/{project_name}.md))

### Session Notes
- (fresh session)

### Pending Decisions
- (none)
"""


def get_memory_root() -> Path:
    return Path(__file__).resolve().parent.parent


def check_time_gate(brain_path: Path) -> dict:
    """Check if brain.md is older than the threshold."""
    if not brain_path.exists():
        return {"due": False, "reason": "brain.md does not exist"}

    mtime = datetime.fromtimestamp(os.path.getmtime(brain_path))
    age_hours = (datetime.now() - mtime).total_seconds() / 3600
    is_due = age_hours >= HOURS_THRESHOLD

    return {
        "due": is_due,
        "last_modified": mtime.isoformat(),
        "age_hours": round(age_hours, 1),
        "threshold_hours": HOURS_THRESHOLD,
    }


def extract_knowledge(brain_content: str) -> list[dict]:
    """
    Extract knowledge entries from brain.md content.

    Looks for patterns that indicate reusable knowledge:
    - Lines starting with "- Key finding:", "- Learned:", "- Rule:", "- Pitfall:"
    - Content under "### Session Notes"
    - Non-trivial bullet points (>20 chars)
    """
    knowledge = []
    in_notes = False

    for line in brain_content.split("\n"):
        stripped = line.strip()

        # Track section
        if stripped.startswith("### Session Notes"):
            in_notes = True
            continue
        elif stripped.startswith("### "):
            in_notes = False
            continue

        # Extract tagged knowledge
        for prefix in ["- Key finding:", "- Learned:", "- Rule:", "- Pitfall:", "- Discovery:"]:
            if stripped.lower().startswith(prefix.lower()):
                content = stripped[len(prefix):].strip()
                if content:
                    knowledge.append({
                        "type": prefix.strip("- :").lower(),
                        "content": content,
                    })
                break
        else:
            # Extract non-trivial session notes
            if in_notes and stripped.startswith("- ") and len(stripped) > 25:
                content = stripped[2:].strip()
                # Skip placeholder content
                if content not in ("(fresh session)", "(none yet)", "(none)"):
                    knowledge.append({
                        "type": "note",
                        "content": content,
                    })

    return knowledge


def archive_brain(brain_path: Path, archive_dir: Path) -> str:
    """Move current brain.md content to archive with date stamp."""
    archive_dir.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    archive_name = f"brain_{date_str}.md"
    archive_path = archive_dir / archive_name

    # Handle multiple archives on the same day
    counter = 1
    while archive_path.exists():
        counter += 1
        archive_name = f"brain_{date_str}_{counter}.md"
        archive_path = archive_dir / archive_name

    shutil.copy2(brain_path, archive_path)
    return str(archive_path)


def reset_brain(brain_path: Path, project_name: str):
    """Reset brain.md to the empty template."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    brain_path.write_text(BRAIN_TEMPLATE.format(timestamp=timestamp, project_name=project_name), encoding="utf-8")


def daily_summarize(memory_root: Path | None = None, force: bool = False) -> dict:
    """
    Main entry point for daily summarization.

    Returns:
        dict with action details including extracted knowledge and archive path
    """
    root = memory_root or get_memory_root()
    brain_path = root / "brain.md"
    archive_dir = root / "archive"

    # Check time gate
    if not force:
        gate = check_time_gate(brain_path)
        if not gate["due"]:
            return {
                "action": "skipped",
                "reason": f"brain.md is only {gate['age_hours']}h old (threshold: {HOURS_THRESHOLD}h)",
                "gate": gate,
            }

    if not brain_path.exists():
        return {"action": "error", "reason": "brain.md not found"}

    brain_content = brain_path.read_text(encoding="utf-8")

    # Extract knowledge
    knowledge = extract_knowledge(brain_content)

    # Save extracted knowledge to topics
    saved_entries = []
    if knowledge:
        # Group by type and save
        try:
            from . import save as save_module
        except ImportError:
            import save as save_module
        for entry in knowledge:
            tags = [entry["type"], "daily-summary"]
            result = save_module.save_to_longterm(
                tags=tags,
                content=entry["content"],
                storage_type="file",
                memory_root=root,
            )
            saved_entries.append({**entry, "save_result": result})

    # Archive
    archive_path = archive_brain(brain_path, archive_dir)

    # Reset with project name
    project_name = root.parent.parent.name
    task_dir = root / "task"
    task_dir.mkdir(exist_ok=True)
    project_task_file = task_dir / f"{project_name}.md"
    if not project_task_file.exists():
        project_task_file.write_text(f"# Active Tasks — {project_name}\n\n- [ ] (none yet)\n", encoding="utf-8")

    reset_brain(brain_path, project_name)

    return {
        "action": "completed",
        "knowledge_extracted": len(knowledge),
        "entries": saved_entries,
        "archived_to": archive_path,
        "brain_reset": True,
    }


def main():
    parser = argparse.ArgumentParser(description="Daily Summarize — archive brain.md and extract knowledge")
    parser.add_argument("--check-only", action="store_true", help="Only check if summarization is due")
    parser.add_argument("--force", action="store_true", help="Skip the time gate")
    parser.add_argument("--memory-root", help="Override memory skill root path")
    args = parser.parse_args()

    root = Path(args.memory_root) if args.memory_root else None

    if args.check_only:
        root = root or get_memory_root()
        gate = check_time_gate(root / "brain.md")
        print(json.dumps(gate, ensure_ascii=False, indent=2))
        return

    result = daily_summarize(memory_root=root, force=args.force)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
